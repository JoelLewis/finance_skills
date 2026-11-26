"""Property-based tests for the real-assets skill script."""

import math

import numpy as np
from hypothesis import given
from hypothesis import strategies as st

from conftest import load_script

real_assets = load_script("real-assets")

PV = real_assets.PropertyValuation
LM = real_assets.LeverageMetrics
REIT = real_assets.REITMetrics
RR = real_assets.RealReturn

# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

value = st.floats(1e4, 1e9, allow_nan=False)
noi = st.floats(1e2, 1e8, allow_nan=False)
cap = st.floats(0.02, 0.15, allow_nan=False)
per_share = st.floats(0.05, 50.0, allow_nan=False)
price = st.floats(1.0, 500.0, allow_nan=False)
ret = st.floats(-0.3, 0.4, allow_nan=False)
infl = st.floats(-0.02, 0.15, allow_nan=False)


def close(a: float, b: float, rel: float = 1e-9, abs_: float = 1e-9) -> bool:
    return math.isclose(a, b, rel_tol=rel, abs_tol=abs_)


# ---------------------------------------------------------------------------
# Property valuation
# ---------------------------------------------------------------------------

@given(noi, cap)
def test_cap_rate_and_value_are_inverse(n, c):
    # Value = NOI / cap rate and cap rate = NOI / value invert each other.
    v = PV.value_from_cap_rate(n, c)
    assert close(PV.cap_rate(n, v), c, rel=1e-12)


@given(noi, cap, st.floats(0.0005, 0.03))
def test_value_falls_as_cap_rate_expands(n, c, bump):
    # Cap rate expansion at a constant NOI lowers the property value.
    assert PV.value_from_cap_rate(n, c + bump) < PV.value_from_cap_rate(n, c)


@given(st.floats(1e3, 1e8), st.floats(0.0, 0.5), st.floats(0.0, 0.5), st.floats(0.0, 0.3))
def test_noi_falls_with_vacancy_and_expenses(gri, opex_share, v1, v2):
    # Higher vacancy reduces effective gross income and so NOI; NOI never
    # exceeds gross income less operating expenses.
    opex = gri * opex_share
    lo, hi = sorted((v1, v2))
    assert PV.noi(gri, opex, hi) <= PV.noi(gri, opex, lo)
    assert PV.noi(gri, opex, lo) <= PV.noi(gri, opex, 0.0)
    assert close(PV.noi(gri, opex, 0.0), gri - opex, abs_=1e-6)


# ---------------------------------------------------------------------------
# Leverage
# ---------------------------------------------------------------------------

@given(value, cap, st.floats(0.1, 0.8), st.floats(0.03, 0.15))
def test_leverage_effect_sign_follows_debt_constant(v, c, ltv, debt_constant):
    # Leverage is positive (cash-on-cash beats the cap rate) exactly when the
    # cap rate exceeds the debt constant (annual debt service / loan).
    n = v * c
    loan = v * ltv
    ads = loan * debt_constant
    res = LM.levered_vs_unlevered(v, n, loan, ads)
    assert close(res["cap_rate"], c, rel=1e-12)
    assert close(res["cash_on_cash"],
                 PV.cash_on_cash_return(n - ads, res["equity_invested"]), rel=1e-12)
    if c > debt_constant * (1 + 1e-9):
        assert res["leverage_effect"] > 0
    elif c < debt_constant * (1 - 1e-9):
        assert res["leverage_effect"] < 0


@given(value, cap, st.floats(0.1, 0.8), st.floats(0.03, 0.15))
def test_dscr_ltv_identity(v, c, ltv, debt_constant):
    # DSCR * LTV * debt constant = cap rate, since
    # (NOI/ADS) * (L/V) * (ADS/L) = NOI/V.
    n = v * c
    loan = v * ltv
    ads = loan * debt_constant
    dscr = LM.debt_service_coverage(n, ads)
    assert close(dscr * LM.loan_to_value(loan, v) * debt_constant, c, rel=1e-9)


# ---------------------------------------------------------------------------
# REIT metrics
# ---------------------------------------------------------------------------

@given(per_share, price)
def test_ffo_yield_and_p_ffo_are_reciprocals(f, p):
    # FFO yield is the inverse of the P/FFO multiple.
    assert close(REIT.ffo_yield(f, p) * REIT.p_ffo(p, f), 1.0, rel=1e-12)


@given(st.floats(-1e6, 1e8), st.floats(0, 1e8), st.floats(0, 1e7),
       st.floats(0, 1e7), st.floats(0, 1e6), price, st.floats(1e5, 1e9))
def test_affo_never_exceeds_ffo(ni, dep, gains, mcapex, slr, p, shares):
    # FFO adds back depreciation and removes sale gains; AFFO further
    # deducts maintenance capex and straight-line rent, so AFFO <= FFO and
    # the AFFO yield never exceeds the FFO yield.
    f = REIT.ffo(ni, dep, gains)
    assert close(f, ni + dep - gains, abs_=1e-6)
    a = REIT.affo(f, mcapex, slr)
    assert a <= f
    assert REIT.affo_yield(a / shares, p) <= REIT.ffo_yield(f / shares, p)


@given(price, price)
def test_nav_premium_zero_at_nav_and_sign(p, nav):
    # Trading at NAV is a zero premium; above NAV positive, below negative.
    assert REIT.nav_premium_discount(nav, nav) == 0.0
    pd = REIT.nav_premium_discount(p, nav)
    assert (pd > 0) == (p > nav) and (pd < 0) == (p < nav)


# ---------------------------------------------------------------------------
# Real returns
# ---------------------------------------------------------------------------

@given(ret, infl)
def test_fisher_round_trip(n, i):
    # (1 + real) * (1 + inflation) = 1 + nominal.
    r = RR.inflation_adjusted_return(n, i)
    assert close((1 + r) * (1 + i), 1 + n, rel=1e-12)


@given(st.data(), st.integers(1, 40))
def test_cumulative_real_return_links_period_real_returns(data, k):
    # The cumulative real return equals the cumulative nominal return
    # deflated by cumulative inflation.
    n = np.array(data.draw(st.lists(ret, min_size=k, max_size=k)))
    i = np.array(data.draw(st.lists(infl, min_size=k, max_size=k)))
    cum = RR.cumulative_real_return(n, i)
    expected = np.prod(1 + n) / np.prod(1 + i) - 1
    assert close(cum, float(expected), rel=1e-9, abs_=1e-12)


@given(ret, st.floats(0.0, 0.15), st.integers(1, 50), st.floats(1e3, 1e7))
def test_purchasing_power_loss_depends_only_on_inflation(n, i, years, v0):
    # Real terminal = nominal terminal / (1+i)^n, so the purchasing-power
    # loss is 1 - (1+i)^-n whatever the nominal return, and it is
    # non-negative for non-negative inflation.
    res = RR.real_vs_nominal_comparison(n, i, years, v0)
    assert close(res["purchasing_power_loss"], 1 - (1 + i) ** -years,
                 rel=1e-9, abs_=1e-9)
    assert res["real_terminal"] <= res["nominal_terminal"] * (1 + 1e-12)
