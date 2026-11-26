"""Property-based tests for the currencies-and-fx skill script."""

import math

from hypothesis import given
from hypothesis import strategies as st

from conftest import load_script

fx = load_script("currencies-and-fx")

FXForward = fx.FXForward
CrossRate = fx.CrossRate
IR = fx.InternationalReturn
RER = fx.RealExchangeRate

# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

spot = st.floats(0.001, 2000.0, allow_nan=False)
rate = st.floats(-0.01, 0.20, allow_nan=False)
tenor = st.floats(0.0, 10.0, allow_nan=False)
ret = st.floats(-0.6, 1.0, allow_nan=False)
price_level = st.floats(1.0, 1000.0, allow_nan=False)


def close(a: float, b: float, rel: float = 1e-9, abs_: float = 1e-9) -> bool:
    return math.isclose(a, b, rel_tol=rel, abs_tol=abs_)


# ---------------------------------------------------------------------------
# Covered interest parity
# ---------------------------------------------------------------------------

@given(spot, rate, rate, tenor)
def test_cip_forward_has_no_arbitrage(s, rd, rf, t):
    # CIP (domestic per foreign quote): one unit of foreign currency invested
    # abroad and sold forward returns F (1+rf)^t domestic, which must equal
    # converting at spot and investing at home, S (1+rd)^t.
    f = FXForward.forward_rate(s, rd, rf, t)
    assert close(f * (1 + rf) ** t, s * (1 + rd) ** t, rel=1e-12)


@given(spot, rate, rate, tenor)
def test_forward_of_inverse_quote_is_inverse_forward(s, rd, rf, t):
    # Quoting the pair the other way round (swap currencies and rates) must
    # give the reciprocal forward.
    f = FXForward.forward_rate(s, rd, rf, t)
    f_inv = FXForward.forward_rate(1.0 / s, rf, rd, t)
    assert close(f * f_inv, 1.0, rel=1e-12)


@given(spot, rate, rate)
def test_one_year_premium_matches_rate_formula(s, rd, rf):
    # Over one year, (F - S)/S = (1+rd)/(1+rf) - 1 = (rd - rf)/(1 + rf).
    f = FXForward.forward_rate(s, rd, rf, 1.0)
    assert close(FXForward.forward_premium(s, f),
                 FXForward.forward_premium_from_rates(rd, rf), rel=1e-9, abs_=1e-12)


@given(spot, rate, rate, st.floats(0.01, 10.0))
def test_forward_premium_sign_follows_rate_differential(s, rd, rf, t):
    # The higher-yielding currency trades at a forward discount; the
    # approximate hedging benefit has the same sign as the premium.
    f = FXForward.forward_rate(s, rd, rf, t)
    prem = FXForward.forward_premium(s, f)
    if rd > rf + 1e-9:
        assert prem > 0 and FXForward.hedging_cost(rd, rf) > 0
    elif rf > rd + 1e-9:
        assert prem < 0 and FXForward.hedging_cost(rd, rf) < 0


# ---------------------------------------------------------------------------
# Cross rates
# ---------------------------------------------------------------------------

@given(spot, spot, spot)
def test_cross_rates_chain_consistently(a_c, b_c, d_c):
    # (A/B) * (B/D) = A/D when all are derived from a common currency C,
    # and the derived triangle shows no arbitrage.
    ab = CrossRate.compute(a_c, b_c)
    bd = CrossRate.compute(b_c, d_c)
    ad = CrossRate.compute(a_c, d_c)
    assert close(ab * bd, ad, rel=1e-12)
    check = CrossRate.triangular_arbitrage_check(ab, bd, ad, tolerance=1e-9 * ad)
    assert not check["arbitrage_exists"]


@given(spot, spot)
def test_cross_rate_inverts_when_legs_swap(a_c, b_c):
    # A/B and B/A are reciprocals; inverting twice returns the quote.
    ab = CrossRate.compute(a_c, b_c)
    ba = CrossRate.compute(b_c, a_c)
    assert close(ab * ba, 1.0, rel=1e-12)
    assert close(CrossRate.compute(1.0, CrossRate.compute(1.0, ab)), ab, rel=1e-12)


@given(spot, spot, st.floats(0.01, 0.5))
def test_mispriced_triangle_flags_arbitrage(ab, bc, gap):
    # Quoting A/C away from A/B * B/C by more than the tolerance is flagged.
    implied = ab * bc
    check = CrossRate.triangular_arbitrage_check(ab, bc, implied * (1 + gap),
                                                 tolerance=1e-6 * implied)
    assert check["arbitrage_exists"]
    assert close(check["implied_ac"], implied)


# ---------------------------------------------------------------------------
# International returns
# ---------------------------------------------------------------------------

@given(ret, ret)
def test_unhedged_return_decomposition_sums(rl, rc):
    # R_total = R_local + R_currency + R_local * R_currency equals the
    # multiplicative unhedged return.
    d = IR.return_decomposition(rl, rc)
    assert close(d["local_return"] + d["currency_return"] + d["interaction_term"],
                 d["total_return"], abs_=1e-12)
    assert close(d["total_return"], IR.unhedged_return(rl, rc), abs_=1e-12)


@given(spot, st.floats(-0.5, 1.0), ret)
def test_currency_round_trip_returns_zero(s0, move, rl):
    # Moving the spot from S0 to S1 and back yields a combined currency
    # return of zero, so the investor is left with the local return. The
    # move is capped at -50% / +100% per leg: larger swings lose absolute
    # precision near a -100% return.
    s1 = s0 * (1.0 + move)
    up = IR.currency_return(s0, s1)
    down = IR.currency_return(s1, s0)
    assert close((1 + up) * (1 + down), 1.0, rel=1e-12)
    assert close(IR.unhedged_return(IR.unhedged_return(rl, up), down), rl,
                 rel=1e-9, abs_=1e-12)


@given(ret, rate)
def test_hedged_return_equals_local_when_rates_equal(rl, r):
    # With no interest differential, hedging neither costs nor earns.
    assert close(IR.hedged_return(rl, r, r), rl, abs_=1e-15)


# ---------------------------------------------------------------------------
# Real exchange rate / PPP
# ---------------------------------------------------------------------------

@given(price_level, price_level, st.floats(0.01, 100.0))
def test_real_rate_is_one_at_ppp(p_dom, p_for, k):
    # At the PPP-implied nominal rate the real exchange rate is exactly 1;
    # a nominal rate k times PPP gives a real rate of k.
    s_ppp = RER.ppp_implied_rate(p_dom, p_for)
    assert close(RER.real_rate(s_ppp, p_for, p_dom), 1.0, rel=1e-12)
    assert close(RER.real_rate(k * s_ppp, p_for, p_dom), k, rel=1e-12)
