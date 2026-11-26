"""Property-based tests for the savings-goals script."""

import math

from hypothesis import assume, given
from hypothesis import strategies as st

from conftest import load_script

SG = load_script("savings-goals").SavingsGoals

goal = st.floats(1_000.0, 5e6)
rate = st.floats(0.0, 0.12)
years = st.integers(1, 50)
savings = st.floats(0.0, 1e6)


def close(a: float, b: float, rel: float = 1e-9, abs_: float = 1e-9) -> bool:
    return math.isclose(a, b, rel_tol=rel, abs_tol=abs_)


# Saving the required monthly amount reaches the goal exactly (or the goal is
# already covered by existing savings alone).
@given(goal, rate, years, savings)
def test_required_savings_reaches_goal(fv, r, n, pv):
    pmt = SG.required_monthly_savings(fv, r, n, pv)
    assert pmt >= 0
    projected = SG.future_value_with_contributions(pv, pmt, r, n)
    if pmt > 0:
        assert close(projected, fv, rel=1e-9)
    else:
        assert projected >= fv * (1 - 1e-12)


# A higher return or a longer horizon never raises the required savings.
@given(goal, rate, rate, years, years, savings)
def test_required_savings_falls_with_rate_and_horizon(fv, r1, r2, n1, n2, pv):
    lo_r, hi_r = sorted((r1, r2))
    short, long_ = sorted((n1, n2))
    assert (SG.required_monthly_savings(fv, hi_r, short, pv)
            <= SG.required_monthly_savings(fv, lo_r, short, pv) * (1 + 1e-12))
    assert (SG.required_monthly_savings(fv, lo_r, long_, pv)
            <= SG.required_monthly_savings(fv, lo_r, short, pv) * (1 + 1e-12))


# At a near-zero rate compounding vanishes: required savings approach
# goal / months and the annuity future value approaches the plain sum.
@given(st.floats(0.0, 1e-6), goal, years, st.floats(1.0, 10_000.0))
def test_near_zero_rate_approaches_undiscounted(r, fv, n, pmt):
    assert close(SG.required_monthly_savings(fv, r, n), fv / (12 * n), rel=1e-3)
    assert close(SG.future_value_with_contributions(0.0, pmt, r, n), pmt * 12 * n, rel=1e-3)


# time_to_goal inverts the future-value projection: contributing for the
# returned horizon lands on the goal. Includes negative (real) returns, where
# the balance tends to PMT/|r| and the goal may still be reachable.
@given(goal, st.floats(-0.05, 0.12), st.floats(10.0, 20_000.0), st.floats(0.0, 0.9))
def test_time_to_goal_round_trip(fv, r, pmt, pv_share):
    pv = fv * pv_share
    t = SG.time_to_goal(fv, pmt, r, pv)
    if math.isinf(t):
        # Unreachable only when the long-run balance PMT/|r| stays below the goal.
        assert r < 0 and pmt / (-r / 12) <= fv * (1 + 1e-9)
        return
    assume(t <= 200)  # keep (1+r)^n well inside float range for the check
    # future_value_with_contributions takes years and multiplies by 12, so a
    # fractional horizon is fine.
    assert close(SG.future_value_with_contributions(pv, pmt, r, t), fv, rel=1e-7)


# Saving more each month never lengthens the time to the goal.
@given(goal, rate, st.floats(10.0, 20_000.0), st.floats(1.0, 5_000.0), savings)
def test_time_to_goal_falls_as_contribution_rises(fv, r, pmt, bump, pv):
    assert SG.time_to_goal(fv, pmt + bump, r, pv) <= SG.time_to_goal(fv, pmt, r, pv) * (1 + 1e-12)


# Fisher relation: (1 + real)(1 + inflation) = 1 + nominal, and an
# inflation-adjusted goal grows by (1 + inflation) each year.
@given(st.floats(-0.05, 0.15), st.floats(-0.02, 0.10), goal, st.integers(0, 40))
def test_real_rate_and_inflation_adjustment(nominal, infl, cost, n):
    real = SG.real_rate_of_return(nominal, infl)
    assert close((1 + real) * (1 + infl), 1 + nominal, rel=1e-12)
    assert close(SG.inflation_adjusted_goal(cost, infl, n + 1),
                 SG.inflation_adjusted_goal(cost, infl, n) * (1 + infl), rel=1e-12)


# The retirement target is spending capitalized at the withdrawal rate.
@given(st.floats(10_000.0, 500_000.0), st.floats(0.02, 0.06))
def test_retirement_target_times_swr_is_spending(spend, swr):
    assert close(SG.retirement_target(spend, swr) * swr, spend)


# A plan is on track exactly when the current contribution covers the
# required contribution, and then no additional saving is needed.
@given(goal, rate, years, savings, st.floats(0.0, 20_000.0))
def test_shortfall_on_track_consistency(fv, r, n, pv, monthly):
    res = SG.contribution_shortfall(fv, r, n, pv, monthly)
    required = SG.required_monthly_savings(fv, r, n, pv)
    # Skip near-ties, where rounding to cents decides the answer.
    assume(abs(required - monthly) > 0.01)
    assert res["on_track"] == (monthly > required)
    assert (res["additional_monthly_needed"] == 0) == res["on_track"]


# Education costs rise each year with positive inflation, and with a
# non-negative return the amount needed at enrollment is no more than the sum
# of nominal costs.
@given(st.floats(5_000.0, 100_000.0), st.integers(1, 20), st.integers(1, 6),
       st.floats(0.001, 0.08), rate)
def test_education_plan_costs(cost, until, length, infl, r):
    plan = SG.education_funding_plan(cost, until, length, infl, r)
    by_year = plan["cost_by_year"]
    assert all(b >= a for a, b in zip(by_year, by_year[1:]))
    # Needed-at-enrollment is built from cost_by_year, each rounded to cents.
    assert plan["total_needed_at_enrollment"] <= plan["total_cost_nominal"] + 0.01 * length
