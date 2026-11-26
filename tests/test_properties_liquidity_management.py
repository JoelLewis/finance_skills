"""Property-based tests for the liquidity-management script."""

import math

import numpy as np
from hypothesis import given
from hypothesis import strategies as st

from conftest import load_script

LM = load_script("liquidity-management").LiquidityManagement

assets = st.floats(1_000.0, 5e6)
burn = st.floats(100.0, 50_000.0)
# Subnormal yields (below ~2e-308) keep too few significant bits for a
# meaningful runway comparison and do not occur in practice.
yield_ = st.floats(0.0, 0.06, allow_subnormal=False)


def close(a: float, b: float, rel: float = 1e-9, abs_: float = 1e-9) -> bool:
    return math.isclose(a, b, rel_tol=rel, abs_tol=abs_)


# Removing inventory can only lower the ratio: quick ratio <= current ratio.
@given(st.floats(0.0, 1e7), st.floats(0.0, 1.0), st.floats(1.0, 1e7))
def test_quick_ratio_not_above_current_ratio(ca, inv_share, cl):
    inv = ca * inv_share
    assert LM.quick_ratio(ca, inv, cl) <= LM.current_ratio(ca, cl) + 1e-12
    assert close(LM.current_ratio(ca, cl) * cl, ca, abs_=1e-6)


# With no yield, runway is liquid assets / burn, which is also the liquidity
# ratio when burn equals expenses.
@given(assets, burn)
def test_zero_yield_runway_is_assets_over_burn(a, b):
    assert close(LM.cash_runway(a, b), a / b)
    assert close(LM.cash_runway(a, b), LM.liquidity_ratio(a, b))


# The runway is the month at which the balance, earning yield and paying the
# burn at month end, reaches exactly zero.
@given(assets, burn, st.floats(0.001, 0.06))
def test_runway_depletes_balance(a, b, y):
    n = LM.cash_runway(a, b, y)
    r = y / 12.0
    if a * r >= b:
        assert math.isinf(n)
        return
    g = (1 + r) ** n
    remaining = a * g - b * (g - 1) / r
    assert abs(remaining) <= 1e-7 * max(a * g, b / r * (g - 1))


# Yield on the reserve can only extend the runway, and more yield extends it
# further.
@given(assets, burn, yield_, yield_)
def test_runway_rises_with_yield(a, b, y1, y2):
    lo, hi = sorted((y1, y2))
    assert LM.cash_runway(a, b, 0.0) <= LM.cash_runway(a, b, lo) * (1 + 1e-12)
    assert LM.cash_runway(a, b, lo) <= LM.cash_runway(a, b, hi) * (1 + 1e-12)


# At a near-zero yield the runway approaches assets / burn. (The tolerance
# allows for the genuine yield effect, about r * n / 2, over runways of up to
# ~50,000 months.)
@given(st.floats(0.0, 1e-9, allow_subnormal=False), assets, burn)
def test_near_zero_yield_runway(y, a, b):
    assert close(LM.cash_runway(a, b, y), a / b, rel=1e-4)


# The projected balance is the starting cash plus cumulative net flows, and
# each month's net flow is income minus total expenses.
@given(st.data(), st.integers(1, 36), st.floats(-1e5, 1e5), st.floats(0.0, 20_000.0))
def test_cash_flow_projection_accumulates(data, n, start, fixed):
    money = st.floats(0.0, 50_000.0)
    income = np.array(data.draw(st.lists(money, min_size=n, max_size=n)))
    variable = np.array(data.draw(st.lists(money, min_size=n, max_size=n)))
    periodic = np.array(data.draw(st.lists(money, min_size=n, max_size=n)))
    rows = LM.cash_flow_projection(income, fixed, variable, periodic, start)
    assert np.allclose(rows["net_cash_flow"], rows["income"] - rows["total_expenses"])
    assert np.allclose(rows["total_expenses"], fixed + variable + periodic)
    expected_end = start + income.sum() - (fixed * n + variable.sum() + periodic.sum())
    assert close(float(rows["cumulative_balance"][-1]), expected_end, rel=1e-9, abs_=1e-6)


# Tier analysis: percentages sum to 1 and the blended yield and access days
# are weighted averages, so they lie within the tiers' range.
@st.composite
def tier_lists(draw):
    n = draw(st.integers(1, 6))
    return [
        {"name": f"t{i}", "amount": draw(st.floats(1.0, 1e6)),
         "yield_rate": draw(st.floats(0.0, 0.06)), "access_days": draw(st.integers(0, 90))}
        for i in range(n)
    ]


@given(tier_lists())
def test_tier_analysis_weighted_averages(tiers):
    res = LM.liquidity_tier_analysis(tiers)
    assert abs(sum(t["pct_of_total"] for t in res["tier_breakdown"]) - 1) <= 0.0001 * len(tiers)
    ys = [t["yield_rate"] for t in tiers]
    days = [t["access_days"] for t in tiers]
    assert min(ys) - 1e-6 <= res["blended_yield"] <= max(ys) + 1e-6
    assert min(days) - 0.05 <= res["weighted_avg_access_days"] <= max(days) + 0.05


# A CD ladder deploys the whole amount, has a rung maturing every interval
# (so each period's need is covered by a maturing rung), and its blended
# yield lies within the rung yields.
@given(st.floats(1_000.0, 1e6), st.integers(1, 12), st.integers(1, 12), st.data())
def test_cd_ladder_covers_each_interval(total, k, interval, data):
    yields = data.draw(st.lists(st.floats(0.0, 0.06), min_size=k, max_size=k))
    ladder = LM.cd_ladder(total, k, yields, interval)
    rungs = ladder["rungs"]
    assert abs(sum(r["amount"] for r in rungs) - total) <= 0.005 * k + 1e-9 * total
    assert [r["maturity_month"] for r in rungs] == [interval * (i + 1) for i in range(k)]
    assert min(yields) - 1e-6 <= ladder["blended_yield"] <= max(yields) + 1e-6


# Every month is classified as either a deficit or a surplus month.
@given(st.lists(st.floats(0.0, 50_000.0), min_size=1, max_size=36), st.floats(500.0, 20_000.0))
def test_income_smoothing_classifies_every_month(incomes, essentials):
    res = LM.income_smoothing(np.array(incomes), essentials)
    assert res["deficit_months"] + res["surplus_months"] == len(incomes)
    assert close(res["average_surplus"], round(res["average_income"] - essentials, 2), abs_=0.011)


# Holding a CD for the breakeven period leaves it, net of the early
# withdrawal penalty, exactly level with the savings account.
@given(st.floats(0.01, 0.08), st.floats(0.0, 0.08), st.integers(1, 12))
def test_cd_breakeven_penalty_equalizes(cd, sav, penalty):
    m = LM.cd_breakeven_penalty(cd, sav, penalty)
    if cd <= sav:
        assert math.isinf(m)
    else:
        assert close(m * cd - penalty * cd, m * sav, rel=1e-9, abs_=1e-12)
