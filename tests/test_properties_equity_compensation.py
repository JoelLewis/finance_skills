"""Property-based tests for the equity-compensation script."""

import inspect
import math

from hypothesis import given
from hypothesis import strategies as st

from conftest import load_script

EC = load_script("equity-compensation").EquityCompensation

shares = st.integers(1, 100_000)
price = st.floats(0.5, 1_000.0)
tax_rate = st.floats(0.0, 0.5)
amti = st.floats(0.0, 2e6)


def close(a: float, b: float, rel: float = 1e-9, abs_: float = 1e-6) -> bool:
    return math.isclose(a, b, rel_tol=rel, abs_tol=abs_)


# RSU vest: income is shares x FMV, withheld plus net shares is every share,
# and the withholding gap is income x (marginal - withholding rate).
@given(shares, price, tax_rate, tax_rate)
def test_rsu_vest_identities(n, fmv, marginal, withholding):
    res = EC.rsu_vest(n, fmv, marginal, withholding)
    assert close(res["ordinary_income"], n * fmv)
    assert close(res["shares_withheld"] + res["net_shares"], n)
    assert 0 <= res["net_shares"] <= n
    assert close(res["withholding_gap"], n * fmv * (marginal - withholding), abs_=1e-6 * n * fmv)


# Pin the documented supplemental withholding default: 22% as of 2026.
def test_rsu_default_supplemental_rate_as_of_2026():
    default = inspect.signature(EC.rsu_vest).parameters["withholding_rate"].default
    assert default == 0.22


# NSO spread is (FMV - strike) x shares, zero when underwater; tax is
# non-negative and total outlay is exercise cost plus tax.
@given(shares, price, price, tax_rate)
def test_nso_spread_and_outlay(n, strike, fmv, rate):
    res = EC.nso_exercise(n, strike, fmv, rate)
    assert close(res["spread_income"], n * max(fmv - strike, 0.0))
    if fmv <= strike:
        assert res["spread_income"] == 0
    assert res["tax"] >= 0
    assert close(res["total_outlay"], n * strike + res["tax"])


@st.composite
def amt_params(draw):
    return dict(
        other_amti=draw(amti),
        regular_tax=draw(st.floats(0.0, 500_000.0)),
        amt_exemption=draw(st.floats(50_000.0, 150_000.0)),
        phaseout_threshold=draw(st.one_of(st.none(), st.floats(200_000.0, 1.5e6))),
        phaseout_rate=draw(st.sampled_from([0.25, 0.5])),
        bracket_breakpoint=draw(st.floats(150_000.0, 300_000.0)),
    )


# The ISO spread is the AMT preference (zero when underwater); AMT due is
# non-negative, equals the credit carryforward, and the exemption stays
# between zero and its full amount.
@given(shares, price, price, amt_params())
def test_iso_amt_basic_rules(n, strike, fmv, params):
    res = EC.iso_exercise_amt(n, strike, fmv, **params)
    assert close(res["amt_preference"], n * max(fmv - strike, 0.0))
    assert close(res["amti"], params["other_amti"] + res["amt_preference"])
    assert 0 <= res["exemption_used"] <= params["amt_exemption"]
    assert res["amt_due"] >= 0
    assert res["amt_credit"] == res["amt_due"]
    assert close(res["amt_due"], max(0.0, res["tentative_minimum_tax"] - params["regular_tax"]),
                 abs_=1e-6)


# Exercising more shares (a larger spread) never lowers AMTI, the tentative
# minimum tax, or AMT due.
@given(shares, shares, price, st.floats(0.0, 500.0), amt_params())
def test_iso_amt_monotone_in_spread(n1, n2, strike, gain, params):
    lo, hi = sorted((n1, n2))
    fmv = strike + gain
    a = EC.iso_exercise_amt(lo, strike, fmv, **params)
    b = EC.iso_exercise_amt(hi, strike, fmv, **params)
    assert a["amti"] <= b["amti"]
    assert a["exemption_used"] >= b["exemption_used"]
    assert a["tentative_minimum_tax"] <= b["tentative_minimum_tax"] + 1e-6
    assert a["amt_due"] <= b["amt_due"] + 1e-6


# Tentative minimum tax is continuous across the 26%/28% breakpoint and the
# marginal rate on AMT base is 26% below it and 28% above it.
@given(st.floats(150_000.0, 300_000.0), st.floats(1.0, 10_000.0))
def test_tmt_two_rate_schedule(breakpoint_, step):
    def tmt(base):
        return EC.iso_exercise_amt(0, 1.0, 1.0, base, 0.0, 0.0,
                                   bracket_breakpoint=breakpoint_)["tentative_minimum_tax"]
    assert close(tmt(breakpoint_), 0.26 * breakpoint_)
    assert close(tmt(breakpoint_ + step) - tmt(breakpoint_), 0.28 * step, rel=1e-6)
    assert close(tmt(breakpoint_) - tmt(breakpoint_ - step), 0.26 * step, rel=1e-6)


# A sale splits the total gain into ordinary income plus capital gain; taxes
# are non-negative; a disqualifying sale's ordinary income is capped by both
# the exercise spread and the actual gain.
@given(shares, price, price, price, st.booleans(), tax_rate, tax_rate, tax_rate, st.booleans())
def test_iso_disposition_splits_gain(n, strike, fmv, sale, qualifying, ord_r, st_r, lt_r, lt_cap):
    res = EC.iso_disposition(n, strike, fmv, sale, qualifying, ord_r, st_r, lt_r, lt_cap)
    assert close(res["total_gain"], n * (sale - strike), abs_=1e-6 * n * max(sale, strike))
    assert close(res["ordinary_income"] + res["capital_gain"], res["total_gain"],
                 abs_=1e-6 * n * max(sale, strike))
    assert res["ordinary_tax"] >= 0 and res["capital_tax"] >= 0
    assert close(res["total_tax"], res["ordinary_tax"] + res["capital_tax"])
    assert res["ordinary_income"] <= n * max(fmv - strike, 0.0) + 1e-6
    assert res["ordinary_income"] <= n * max(sale - strike, 0.0) + 1e-6
    # After-tax proceeds never exceed gross proceeds.
    assert n * sale - res["total_tax"] <= n * sale


# When long-term rates are no higher than ordinary and short-term rates, a
# qualifying disposition never costs more tax than a disqualifying one.
@given(shares, price, price, price, tax_rate, tax_rate, st.floats(0.0, 1.0))
def test_qualifying_never_costs_more(n, strike, fmv, sale, ord_r, st_r, lt_share):
    lt_r = min(ord_r, st_r) * lt_share
    cmp_ = EC.iso_disposition_comparison(n, strike, fmv, sale, ord_r, st_r, lt_r)
    assert cmp_["tax_difference"] >= -1e-6


# ESPP purchase price is at most (1 - discount) x purchase-date FMV, a
# lookback never raises it, and the bargain element is at least the discount.
@given(price, price, st.floats(0.0, 0.15))
def test_espp_purchase_price(offer, purchase, d):
    look = EC.espp_purchase(offer, purchase, d, lookback=True)
    plain = EC.espp_purchase(offer, purchase, d, lookback=False)
    assert look["purchase_price"] <= plain["purchase_price"] + 1e-12
    assert close(plain["purchase_price"], purchase * (1 - d))
    assert look["bargain_element"] >= d * purchase - 1e-9
    assert close(look["purchase_price"] + look["bargain_element"], purchase)


# ESPP sale: ordinary plus capital income equals sale price minus price paid,
# whichever holding period; a disqualifying sale's ordinary income is the full
# bargain element even at a loss; a qualifying sale's is capped by the offer-
# date discount and by the actual gain.
@given(price, price, price, st.booleans(), tax_rate, tax_rate, tax_rate,
       st.floats(0.0, 0.15), st.booleans())
def test_espp_disposition_splits_gain(offer, purchase, sale, qualifying, o, s, lt, d, lookback):
    res = EC.espp_disposition(offer, purchase, sale, qualifying, o, s, lt, d, lookback)
    price_paid = EC.espp_purchase(offer, purchase, d, lookback)["purchase_price"]
    assert close(res["purchase_price"], price_paid)
    assert close(res["ordinary_income"] + res["capital_gain"], sale - price_paid)
    assert res["ordinary_tax"] >= 0 and res["capital_tax"] >= 0
    if qualifying:
        assert 0 <= res["ordinary_income"] <= d * offer + 1e-9
        assert res["ordinary_income"] <= max(sale - price_paid, 0.0) + 1e-9
    else:
        assert close(res["ordinary_income"], purchase - price_paid)
