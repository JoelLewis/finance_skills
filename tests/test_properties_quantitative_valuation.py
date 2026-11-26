"""Property-based tests for the quantitative-valuation script."""

import math

import numpy as np
from hypothesis import given
from hypothesis import strategies as st

from conftest import load_script

qv = load_script("quantitative-valuation")

# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

cash_flow = st.floats(1.0, 1e4, allow_nan=False)
growth = st.floats(-0.05, 0.25, allow_nan=False)
# Stable growth and discount rates kept at least 1% apart: as r - g -> 0 a
# perpetuity explodes and relative rounding error grows with it.
stable_growth = st.floats(-0.02, 0.04, allow_nan=False)
discount_rate = st.floats(0.05, 0.20, allow_nan=False)
years = st.integers(1, 15)


def close(a: float, b: float, rel: float = 1e-9, abs_: float = 1e-9) -> bool:
    return math.isclose(a, b, rel_tol=rel, abs_tol=abs_)


# ---------------------------------------------------------------------------
# Dividend discount models
# ---------------------------------------------------------------------------

@given(cash_flow, discount_rate, stable_growth)
def test_gordon_growth_is_d1_over_r_minus_g(d1, r, g):
    # P = D1 / (r - g), equivalently the price grows at g and yields r.
    p = qv.DividendDiscount.gordon_growth(d1, r, g)
    assert close(p, d1 / (r - g), rel=1e-12)
    assert close(d1 / p + g, r, rel=1e-9, abs_=1e-12)


@given(cash_flow, discount_rate, discount_rate, stable_growth)
def test_gordon_value_falls_as_required_return_rises(d1, r1, r2, g):
    lo, hi = sorted([r1, r2])
    v_lo = qv.DividendDiscount.gordon_growth(d1, lo, g)
    v_hi = qv.DividendDiscount.gordon_growth(d1, hi, g)
    assert v_hi <= v_lo


@given(cash_flow, stable_growth, discount_rate, years)
def test_two_stage_with_equal_growth_reduces_to_gordon(d0, g, r, n):
    # If stage 1 grows at the stable rate, the two-stage DDM is a single
    # Gordon growth perpetuity on D1 = D0 (1 + g).
    two = qv.DividendDiscount.two_stage_ddm(d0, g, g, r, n)
    one = qv.DividendDiscount.gordon_growth(d0 * (1 + g), r, g)
    assert close(two, one, rel=1e-9)


@given(cash_flow, growth, growth, stable_growth, discount_rate, years)
def test_two_stage_increasing_in_high_growth_rate(d0, g1a, g1b, g2, r, n):
    # Faster stage-1 dividend growth makes every later dividend larger.
    lo, hi = sorted([g1a, g1b])
    v_lo = qv.DividendDiscount.two_stage_ddm(d0, lo, g2, r, n)
    v_hi = qv.DividendDiscount.two_stage_ddm(d0, hi, g2, r, n)
    assert v_hi >= v_lo * (1 - 1e-12)


# ---------------------------------------------------------------------------
# DCF
# ---------------------------------------------------------------------------

@st.composite
def dcf_inputs(draw):
    n = draw(years)
    rates = draw(st.lists(growth, min_size=n, max_size=n))
    return draw(cash_flow), rates, draw(discount_rate), draw(stable_growth)


@given(cash_flow, stable_growth, discount_rate, years)
def test_constant_growth_dcf_equals_gordon(fcf0, g, wacc, n):
    # When explicit-period growth equals terminal growth, EV is a single
    # growing perpetuity: FCF0 (1 + g) / (WACC - g), whatever the horizon.
    ev = qv.DCF(fcf0, [g] * n, wacc, terminal_growth=g).enterprise_value()
    assert close(ev, fcf0 * (1 + g) / (wacc - g), rel=1e-9)


@given(dcf_inputs(), discount_rate)
def test_dcf_value_falls_as_wacc_rises(inputs, wacc2):
    # Positive cash flows are worth less at a higher discount rate.
    fcf0, rates, wacc1, tg = inputs
    lo, hi = sorted([wacc1, wacc2])
    ev_lo = qv.DCF(fcf0, rates, lo, terminal_growth=tg).enterprise_value()
    ev_hi = qv.DCF(fcf0, rates, hi, terminal_growth=tg).enterprise_value()
    assert ev_hi <= ev_lo * (1 + 1e-12)


@given(dcf_inputs(), st.floats(0.1, 10.0), st.floats(2.0, 25.0))
def test_dcf_linear_in_current_cash_flow(inputs, k, multiple):
    # Every projected cash flow, and the terminal value, scales with FCF0.
    fcf0, rates, wacc, tg = inputs
    for kw in ({"terminal_growth": tg}, {"exit_multiple": multiple}):
        a = qv.DCF(fcf0, rates, wacc, **kw).enterprise_value()
        b = qv.DCF(k * fcf0, rates, wacc, **kw).enterprise_value()
        assert close(b, k * a, rel=1e-9)


@given(dcf_inputs(), st.floats(-1e4, 1e4))
def test_ev_is_sum_of_parts_and_equity_bridge(inputs, net_debt):
    # EV = PV(explicit FCFs) + PV(TV); equity = EV - net debt.
    fcf0, rates, wacc, tg = inputs
    d = qv.DCF(fcf0, rates, wacc, terminal_growth=tg)
    ev = d.enterprise_value()
    n = len(rates)
    assert close(ev, d.pv_explicit_fcfs() + d.terminal_value() / (1 + wacc) ** n,
                 rel=1e-12)
    assert close(d.equity_value(net_debt), ev - net_debt, rel=1e-12, abs_=1e-9)


@given(dcf_inputs(), st.lists(discount_rate, min_size=1, max_size=4),
       st.lists(stable_growth, min_size=1, max_size=4))
def test_sensitivity_table_matches_point_valuations(inputs, waccs, gs):
    # Each cell is the EV re-run at that (WACC, g); the model's own inputs
    # are restored afterwards.
    fcf0, rates, wacc, tg = inputs
    d = qv.DCF(fcf0, rates, wacc, terminal_growth=tg)
    ev0 = d.enterprise_value()
    table = d.sensitivity_table(np.array(waccs), np.array(gs))
    for i, w in enumerate(waccs):
        for j, g in enumerate(gs):
            if g >= w:
                assert np.isnan(table[i, j])
            else:
                ev = qv.DCF(fcf0, rates, w, terminal_growth=g).enterprise_value()
                assert close(table[i, j], ev, rel=1e-12)
    assert (d.wacc, d.terminal_growth) == (wacc, tg)
    assert d.enterprise_value() == ev0


# ---------------------------------------------------------------------------
# WACC, residual income, multiples
# ---------------------------------------------------------------------------

@given(st.floats(0.0, 1.0), st.floats(0.05, 0.20), st.floats(0.02, 0.12),
       st.floats(0.0, 0.4))
def test_wacc_between_after_tax_debt_and_equity_cost(w_e, r_e, r_d, t):
    # With weights summing to 1, WACC is a weighted average of the two costs.
    w = qv.WACC(w_e, 1 - w_e, r_e, r_d, t).compute()
    lo, hi = sorted([r_d * (1 - t), r_e])
    assert lo - 1e-12 <= w <= hi + 1e-12


@given(st.floats(1.0, 500.0), discount_rate, st.integers(0, 10), stable_growth)
def test_residual_income_equals_book_when_roe_equals_cost_of_equity(bv, r, n, g):
    # Earning exactly the cost of equity creates no economic profit, so
    # intrinsic value equals book value.
    ri = qv.ResidualIncome(bv, [r] * n, r, terminal_roe=r, terminal_growth=g)
    assert close(ri.intrinsic_value(), bv, rel=1e-12)


@given(st.floats(1.0, 500.0), discount_rate, st.lists(st.floats(-0.1, 0.4),
       min_size=1, max_size=10))
def test_residual_income_premium_sign_follows_spread(bv, r, roes):
    # Value exceeds book iff the company earns above its cost of equity
    # (here uniformly above or uniformly below).
    above = qv.ResidualIncome(bv, [r + abs(x) + 0.01 for x in roes], r)
    below = qv.ResidualIncome(bv, [r - abs(x) - 0.01 for x in roes], r)
    assert above.intrinsic_value() > bv
    assert below.intrinsic_value() < bv


@given(st.floats(0.1, 1e4), st.lists(st.floats(1.0, 60.0), min_size=1, max_size=15),
       st.booleans())
def test_implied_value_within_peer_range(metric, multiples, use_median):
    # A median or mean peer multiple lies inside the peer range.
    v = qv.ComparableMultiples.implied_value(metric, multiples, use_median)
    assert metric * min(multiples) * (1 - 1e-12) <= v <= metric * max(multiples) * (1 + 1e-12)


@given(st.floats(1.0, 1e4), st.floats(1.0, 1e4))
def test_premium_discount_round_trip(price, implied):
    # price = implied * (1 + premium); premium > 0 iff price > implied.
    pd = qv.ComparableMultiples.premium_discount(price, implied)
    assert close(implied * (1 + pd), price, rel=1e-12)
    assert (pd > 0) == (price > implied)
