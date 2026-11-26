"""Property-based tests for the debt-management script."""

import math

from hypothesis import given
from hypothesis import strategies as st

from conftest import load_script

dm = load_script("debt-management")
DM = dm.DebtManagement
Debt = dm.Debt

balance = st.floats(100.0, 500_000.0)
apr = st.floats(0.0, 0.30)
# Principal share of the payment on top of the first month's interest, so the
# payment always amortizes the debt (keeps payoff under ~200 months).
paydown = st.floats(0.005, 0.10)


def close(a: float, b: float, rel: float = 1e-9, abs_: float = 1e-9) -> bool:
    return math.isclose(a, b, rel_tol=rel, abs_tol=abs_)


def amortizing_payment(bal: float, rate: float, share: float) -> float:
    return bal * rate / 12.0 + bal * share


@st.composite
def debt_lists(draw):
    n = draw(st.integers(1, 5))
    debts = []
    for i in range(n):
        b = draw(st.floats(100.0, 50_000.0))
        r = draw(apr)
        m = amortizing_payment(b, r, draw(paydown))
        debts.append(Debt(f"d{i}", b, r, m))
    return debts, draw(st.floats(0.0, 2_000.0))


# The closed-form payoff month count matches the month-by-month schedule.
@given(balance, apr, paydown)
def test_months_to_payoff_matches_schedule(bal, rate, share):
    pmt = amortizing_payment(bal, rate, share)
    n = DM.months_to_payoff(bal, rate, pmt)
    rows = DM.amortization_schedule(bal, rate, pmt)
    # The schedule stops once less than half a cent remains, so it may end
    # one month before the exact closed-form ceiling.
    assert math.ceil(n - 1e-9) - 1 <= len(rows) <= math.ceil(n - 1e-9)


# Paying more each month never lengthens the payoff.
@given(balance, apr, paydown, st.floats(1.0, 5_000.0))
def test_payoff_time_falls_as_payment_rises(bal, rate, share, bump):
    pmt = amortizing_payment(bal, rate, share)
    assert DM.months_to_payoff(bal, rate, pmt + bump) <= DM.months_to_payoff(bal, rate, pmt)


# A payment that does not cover the interest never pays the debt off.
# frac stops short of 1: at exactly 1 the test's and the script's interest
# products round differently.
@given(balance, st.floats(0.01, 0.30), st.floats(0.0, 0.999))
def test_payment_below_interest_never_pays_off(bal, rate, frac):
    assert math.isinf(DM.months_to_payoff(bal, rate, bal * rate / 12.0 * frac))


# At a near-zero rate the payoff time approaches balance / payment.
@given(st.floats(0.0, 1e-9), balance, paydown)
def test_near_zero_rate_payoff_is_balance_over_payment(rate, bal, share):
    pmt = bal * share
    assert close(DM.months_to_payoff(bal, rate, pmt), bal / pmt, rel=1e-6)


# Every schedule row splits the payment into interest + principal + extra,
# principal repaid equals the balance, and schedule interest equals
# total_interest when there is no extra payment.
@given(balance, apr, paydown, st.floats(0.0, 1_000.0))
def test_amortization_schedule_identities(bal, rate, share, extra):
    pmt = amortizing_payment(bal, rate, share)
    rows = DM.amortization_schedule(bal, rate, pmt, extra)
    for row in rows:
        assert close(row["payment"],
                     row["interest"] + row["principal"] + row["extra_principal"],
                     rel=1e-12, abs_=1e-9)
    repaid = float(rows["principal"].sum() + rows["extra_principal"].sum())
    assert abs(repaid - bal) <= 0.005 + 1e-9 * bal
    if extra == 0:
        assert close(float(rows["interest"].sum()), DM.total_interest(bal, rate, pmt),
                     rel=1e-9, abs_=0.01)


# Multi-debt payoff: every debt reaches zero exactly once, and total paid is
# principal plus interest.
@given(debt_lists(), st.sampled_from(["avalanche", "snowball"]))
def test_multi_debt_payoff_clears_every_debt(inputs, strategy):
    debts, extra = inputs
    plan = DM(debts, extra)
    result = plan.payoff_avalanche() if strategy == "avalanche" else plan.payoff_snowball()
    names = [e["name"] for e in result["payoff_order"]]
    assert sorted(names) == sorted(d.name for d in debts)
    principal = sum(d.balance for d in debts)
    # Each debt may drop a sub-half-cent residual; totals are rounded to cents.
    tol = 0.005 * len(debts) + 0.02
    assert abs(result["total_paid"] - (principal + result["total_interest"])) <= tol
    assert result["total_interest"] >= 0


# Directing extra cash to the highest rate first minimizes interest, so the
# avalanche never pays more total interest than the snowball.
@given(debt_lists())
def test_avalanche_pays_no_more_interest_than_snowball(inputs):
    debts, extra = inputs
    cmp_ = DM(debts, extra).compare_strategies()
    assert cmp_["avalanche"]["total_interest"] <= cmp_["snowball"]["total_interest"] + 0.02


# Monthly compounding makes the effective rate at least the APR; a tax
# deduction lowers the rate in proportion to the marginal rate.
@given(apr, st.floats(0.0, 0.5))
def test_effective_and_after_tax_rates(rate, tax):
    # abs slack: a subnormal APR underflows to 0 when divided by 12.
    assert DM.apr_to_effective_rate(rate) >= rate * (1 - 1e-12) - 1e-300
    after = DM.after_tax_rate(rate, tax)
    assert 0.0 <= after <= rate
    assert close(after, rate * (1 - tax))


# Front-end DTI never exceeds back-end DTI when housing is part of total debt;
# refinance breakeven months times monthly savings recovers closing costs.
@given(st.floats(0.0, 10_000.0), st.floats(0.0, 10_000.0), st.floats(1_000.0, 50_000.0),
       st.floats(0.0, 20_000.0), st.floats(500.0, 5_000.0), st.floats(1.0, 1_000.0))
def test_dti_and_refinance_breakeven(housing, other, income, costs, old, saving):
    assert DM.front_end_dti(housing, income) <= DM.debt_to_income(housing + other, income)
    months = DM.refinance_breakeven(costs, old, old - saving)
    assert close(months * saving, costs, rel=1e-9, abs_=1e-6)
    assert math.isinf(DM.refinance_breakeven(costs, old, old + saving))
