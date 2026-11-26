"""Property-based tests for the performance-reporting script."""

import math

import numpy as np
from hypothesis import assume, given
from hypothesis import strategies as st

from conftest import load_script

pr = load_script("performance-reporting")

# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

value = st.floats(1e3, 1e8, allow_nan=False)
period_return = st.floats(-0.5, 0.5, allow_nan=False)
daily_return = st.floats(-0.05, 0.05, allow_nan=False)
total_days = st.integers(1, 366)


def close(a: float, b: float, rel: float = 1e-9, abs_: float = 1e-9) -> bool:
    return math.isclose(a, b, rel_tol=rel, abs_tol=abs_)


@st.composite
def composite_inputs(draw):
    n = draw(st.integers(1, 30))
    r = np.array(draw(st.lists(period_return, min_size=n, max_size=n)))
    v = np.array(draw(st.lists(value, min_size=n, max_size=n)))
    return r, v


# ---------------------------------------------------------------------------
# Modified Dietz
# ---------------------------------------------------------------------------

@given(value, period_return, total_days)
def test_modified_dietz_without_flows_is_simple_return(v0, r, d):
    # With no external cash flows the Modified Dietz return is V_end / V_start - 1.
    md = pr.ModifiedDietz(v0, v0 * (1 + r), np.array([]), np.array([]), d)
    assert close(md.compute_return(), r, rel=1e-9, abs_=1e-12)


@given(value, st.floats(0.0, 1e7), period_return, total_days)
def test_modified_dietz_flow_at_start_is_return_on_total_capital(v0, cf, r, d):
    # A contribution on day 0 is invested the full period (weight 1), so the
    # return is earned on V_start + CF.
    v_end = (v0 + cf) * (1 + r)
    md = pr.ModifiedDietz(v0, v_end, np.array([cf]), np.array([0.0]), d)
    assert close(md.compute_return(), r, rel=1e-9, abs_=1e-12)


@given(value, st.floats(-1e7, 1e7), period_return, total_days)
def test_modified_dietz_flow_at_end_is_return_on_starting_capital(v0, cf, r, d):
    # A flow on the last day has weight 0: the return is earned on V_start
    # only and the flow is simply removed from V_end.
    v_end = v0 * (1 + r) + cf
    md = pr.ModifiedDietz(v0, v_end, np.array([cf]), np.array([float(d)]), d)
    assert close(md.compute_return(), r, rel=1e-9, abs_=1e-9)


@given(value, st.lists(st.tuples(st.floats(-1e6, 1e6), st.floats(0, 1)),
                       min_size=0, max_size=8), total_days)
def test_modified_dietz_weights_in_unit_interval(v0, flows, d):
    # Each weight is the fraction of the period a flow was invested.
    cf = np.array([f for f, _ in flows])
    days = np.array([u * d for _, u in flows])
    w = pr.ModifiedDietz(v0, v0, cf, days, d).weights()
    assert np.all((w >= -1e-12) & (w <= 1 + 1e-12))


# ---------------------------------------------------------------------------
# Time-weighted and money-weighted returns
# ---------------------------------------------------------------------------

@given(st.lists(period_return, min_size=1, max_size=20),
       st.lists(period_return, min_size=1, max_size=20))
def test_twr_links_across_subperiods(a, b):
    # Chain-linking: (1 + R_{a+b}) = (1 + R_a)(1 + R_b).
    ra = pr.TimeWeightedReturn(np.array(a)).cumulative_return()
    rb = pr.TimeWeightedReturn(np.array(b)).cumulative_return()
    rab = pr.TimeWeightedReturn(np.array(a + b)).cumulative_return()
    assert close(1 + rab, (1 + ra) * (1 + rb), rel=1e-9, abs_=1e-12)


@given(st.floats(-0.9, 5.0), st.floats(1.0, 30.0))
def test_annualize_round_trips_to_cumulative(cum, years):
    # Compounding the annualized return over the period recovers the
    # cumulative return. Years >= 1 matches the documented use (no
    # annualizing sub-year periods); for years << 1 the 1/years power
    # amplifies rounding error past any fixed tolerance.
    ann = pr.TimeWeightedReturn.annualize(cum, years)
    assert close((1 + ann) ** years, 1 + cum, rel=1e-9)


@given(value, st.floats(-0.5, 1.0), st.floats(0.25, 10.0))
def test_irr_of_single_investment_is_compound_growth_rate(v0, r, t):
    # Invest V0 at t=0 and receive V0 (1 + r)^t at t: the IRR is r.
    mwr = pr.MoneyWeightedReturn(np.array([-v0, v0 * (1 + r) ** t]),
                                 np.array([0.0, t]))
    assert close(mwr.compute_irr(), r, rel=1e-7, abs_=1e-9)


@given(value, st.lists(st.tuples(st.floats(1e2, 1e6), st.floats(0.05, 0.95)),
                       min_size=0, max_size=5),
       st.floats(-0.3, 0.5), st.floats(0.5, 5.0))
def test_irr_recovers_constant_growth_rate_with_contributions(v0, flows, r, t):
    # If every dollar (initial and contributed) grows at the same rate r,
    # the money-weighted return is r regardless of flow timing.
    times = [0.0] + [u * t for _, u in flows] + [t]
    cfs = [-v0] + [-c for c, _ in flows]
    end_value = sum(-c * (1 + r) ** (t - s) for c, s in zip(cfs, times[:-1]))
    mwr = pr.MoneyWeightedReturn(np.array(cfs + [end_value]), np.array(times))
    assert close(mwr.compute_irr(), r, rel=1e-7, abs_=1e-9)


# ---------------------------------------------------------------------------
# GIPS composite
# ---------------------------------------------------------------------------

@given(composite_inputs())
def test_composite_return_between_lowest_and_highest(inputs):
    # An asset-weighted average of portfolio returns lies within their range.
    r, v = inputs
    c = pr.CompositeReturn(r, v)
    aw = c.asset_weighted_return()
    assert r.min() - 1e-12 <= aw <= r.max() + 1e-12


@given(composite_inputs(), st.floats(1e-3, 1e3))
def test_composite_return_invariant_to_scaling_assets(inputs, k):
    # Only relative portfolio sizes matter for the asset-weighted return.
    r, v = inputs
    a = pr.CompositeReturn(r, v).asset_weighted_return()
    b = pr.CompositeReturn(r, k * v).asset_weighted_return()
    assert close(a, b, rel=1e-9, abs_=1e-12)


@given(st.lists(period_return, min_size=1, max_size=30), value)
def test_equal_assets_give_equal_weighted_return(r, v):
    # With identical portfolio sizes, asset- and equal-weighting coincide.
    r = np.array(r)
    c = pr.CompositeReturn(r, np.full_like(r, v))
    assert close(c.asset_weighted_return(), c.equal_weighted_return(),
                 rel=1e-9, abs_=1e-12)


@given(composite_inputs())
def test_dispersion_bounded_by_half_range(inputs):
    # A (weighted) standard deviation is non-negative and at most half the
    # range of the data (Popoviciu's inequality).
    r, v = inputs
    disp = pr.CompositeReturn(r, v).internal_dispersion()
    assert disp >= 0.0
    assert disp <= (r.max() - r.min()) / 2 + 1e-12


@given(period_return, composite_inputs())
def test_dispersion_zero_when_all_returns_equal(x, inputs):
    # Identical portfolio returns have no dispersion around the composite.
    _, v = inputs
    disp = pr.CompositeReturn(np.full(len(v), x), v).internal_dispersion()
    assert disp <= 1e-12


# ---------------------------------------------------------------------------
# Standard period returns
# ---------------------------------------------------------------------------

@given(st.lists(daily_return, min_size=1, max_size=600), st.data())
def test_trailing_and_earlier_periods_link_to_inception(r, data):
    # ITD growth = growth before the trailing window x growth within it.
    r = np.array(r)
    k = data.draw(st.integers(1, len(r)))
    p = pr.PeriodReturns(r)
    trailing = p.trailing_return(k)
    earlier = p.cumulative_return(r[: len(r) - k])
    itd = p.inception_to_date()["cumulative_return"]
    assert close(1 + itd, (1 + earlier) * (1 + trailing), rel=1e-9, abs_=1e-12)


@given(st.lists(daily_return, min_size=1, max_size=600))
def test_annualized_only_for_periods_of_at_least_a_year(r):
    # Periods under one year are reported cumulative only; longer periods
    # annualize consistently with the cumulative return.
    r = np.array(r)
    p = pr.PeriodReturns(r, periods_per_year=252)
    ann = p.annualized_return()
    if len(r) < 252:
        assert ann is None
    else:
        years = len(r) / 252
        assert close((1 + ann) ** years, 1 + p.cumulative_return(), rel=1e-9)
