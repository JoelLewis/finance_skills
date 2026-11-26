"""Property-based tests for the emergency-fund script."""

import math

import numpy as np
from hypothesis import given
from hypothesis import strategies as st

from conftest import load_script

EF = load_script("emergency-fund").EmergencyFund

expenses = st.floats(500.0, 30_000.0)
months = st.integers(1, 24)
fund = st.floats(1_000.0, 500_000.0)
yield_ = st.floats(0.0, 0.06)


def close(a: float, b: float, rel: float = 1e-9, abs_: float = 1e-9) -> bool:
    return math.isclose(a, b, rel_tol=rel, abs_tol=abs_)


# The expense-based target scales linearly with expenses and with months.
@given(expenses, months, st.floats(0.1, 10.0), st.integers(1, 24))
def test_target_scales_with_expenses_and_months(exp, m, k, extra):
    base = EF.expense_based_fund(exp, m)
    assert close(EF.expense_based_fund(exp * k, m), base * k)
    assert EF.expense_based_fund(exp, m + extra) > base
    assert close(EF.income_based_fund(exp, m), base)


# Riskier circumstances never lower the recommended coverage, and the
# recommended level is never below the minimum.
@given(st.booleans(), st.booleans(), st.booleans(), st.booleans())
def test_recommended_months_ordering(dual, stable, variable, search):
    lo, hi = EF.recommended_months(dual, stable, variable, search)
    assert 3 <= lo <= hi <= 12
    risky_lo, risky_hi = EF.recommended_months(dual, stable, True, search)
    assert (risky_lo, risky_hi) >= (lo, hi)
    single_lo, single_hi = EF.recommended_months(False, stable, variable, search)
    assert single_lo >= lo and single_hi >= hi


# Tiers sum to the fund; tier 1 holds at most one month, tier 2 at most three,
# and tier 3 is used only once the first two tiers are full.
@given(fund, expenses)
def test_tiered_allocation_partitions_fund(total, exp):
    alloc = EF.tiered_allocation(total, exp)
    t1, t2, t3 = (alloc[k]["amount"] for k in ("tier_1", "tier_2", "tier_3"))
    assert abs(t1 + t2 + t3 - total) <= 0.015  # each tier rounded to cents
    assert 0 <= t1 <= exp + 0.005
    assert 0 <= t2 <= 3 * exp + 0.005
    if t3 > 0.005:
        assert close(t1, exp, abs_=0.01) and close(t2, 3 * exp, abs_=0.01)


# A weighted average yield lies between the lowest and highest tier yield.
# Amounts are 0 or at least a cent (subnormal amounts underflow the product).
cents = st.one_of(st.just(0.0), st.floats(0.01, 1e6))


@given(st.lists(st.tuples(cents, st.floats(0.0, 0.08)), min_size=1, max_size=5))
def test_blended_yield_within_tier_range(tiers):
    amounts = [a for a, _ in tiers]
    yields = [y for _, y in tiers]
    b = EF.blended_yield(amounts, yields)
    if sum(amounts) > 0:
        assert min(yields) - 1e-12 <= b <= max(yields) + 1e-12
    else:
        assert b == 0.0


# Opportunity cost is never negative and equals balance x spread when the
# investment return beats the cash yield.
@given(fund, yield_, st.floats(0.0, 0.12))
def test_opportunity_cost(balance, cash, inv):
    cost = EF.opportunity_cost(balance, cash, inv)
    assert cost >= 0
    if inv > cash:
        assert close(cost, balance * (inv - cash))


# With no yield the fund lasts balance / draw months (rounded up); with a
# yield it lasts at least as long; withdrawals equal balance plus interest.
@given(fund, st.floats(0.02, 0.5), yield_)
def test_drawdown_duration_consistent_with_balance_and_burn(balance, draw_share, y):
    draw = balance * draw_share  # 2 to 50 months of runway
    no_yield = EF.drawdown_duration(balance, draw, 0.0)
    assert math.ceil(balance / draw) - 1 <= no_yield <= math.ceil(balance / draw)
    with_yield = EF.drawdown_duration(balance, draw, y)
    assert with_yield >= no_yield
    rows = EF.drawdown_schedule(balance, draw, y)
    paid_out = float(rows["withdrawal"].sum())
    assert abs(paid_out - (balance + float(rows["interest_earned"].sum()))) <= 0.005 + 1e-9 * balance
    assert rows["remaining_balance"][-1] <= 0.005


# When the yield covers the draw the fund never depletes: the duration is
# infinite and the schedule is capped rather than looping forever.
@given(fund, st.floats(0.01, 0.06), st.floats(0.0, 1.0))
def test_drawdown_never_depletes_when_yield_covers_draw(balance, y, frac):
    draw = balance * y / 12.0 * frac
    assert math.isinf(EF.drawdown_duration(balance, draw, y))
    assert len(EF.drawdown_schedule(balance, draw, y)) <= 1200


# Rebuilding: the fund reaches the target in the reported month and not
# before; with no yield that is ceil(shortfall / contribution); a larger
# contribution never takes longer.
@given(st.floats(0.0, 50_000.0), st.floats(1_000.0, 100_000.0), st.floats(100.0, 10_000.0),
       yield_, st.floats(1.0, 5_000.0))
def test_replenishment_reaches_target(current, gap, contrib, y, bump):
    target = current + gap
    res = EF.replenishment_schedule(current, target, contrib, y)
    n = res["months_to_rebuild"]
    r = y / 12.0
    bal = current
    for _ in range(n - 1):
        bal += bal * r + contrib
    assert bal < target - 0.005
    bal += bal * r + contrib
    assert bal >= target - 0.005
    if y == 0:
        assert math.ceil(gap / contrib) - 1 <= n <= math.ceil(gap / contrib)
    assert EF.replenishment_schedule(current, target, contrib + bump, y)["months_to_rebuild"] <= n


# Variable-income statistics are ordered and the buffer is 2 or 3 months.
@given(st.lists(st.floats(0.0, 50_000.0), min_size=2, max_size=36), expenses)
def test_variable_income_buffer(incomes, exp):
    res = EF.variable_income_buffer(np.array(incomes), exp)
    assert res["min_income"] <= res["average_income"] + 0.01
    assert res["average_income"] <= res["max_income"] + 0.01
    assert res["recommended_buffer_months"] in (2, 3)
    assert close(res["recommended_buffer"], round(exp * res["recommended_buffer_months"], 2))
    assert 0 <= res["months_below_expenses"] <= len(incomes)
