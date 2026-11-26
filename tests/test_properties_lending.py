"""Property-based tests for the lending script."""

import math

from hypothesis import given
from hypothesis import strategies as st

from conftest import load_script

LA = load_script("lending").LendingAnalysis

principal = st.floats(1_000.0, 2e6)
apr = st.floats(0.0, 0.15)
term = st.integers(12, 480)


def close(a: float, b: float, rel: float = 1e-9, abs_: float = 1e-9) -> bool:
    return math.isclose(a, b, rel_tol=rel, abs_tol=abs_)


# The level payment is the one whose discounted stream equals the principal.
@given(principal, st.floats(0.001, 0.15), term)
def test_payment_pv_equals_principal(p, a, n):
    pmt = LA.monthly_payment(p, a, n)
    r = a / 12.0
    pv = sum(pmt / (1 + r) ** t for t in range(1, n + 1))
    assert close(pv, p, rel=1e-9)


# A higher rate raises the payment; a longer term lowers it.
@given(principal, apr, apr, term, term)
def test_payment_monotone_in_rate_and_term(p, a1, a2, n1, n2):
    lo, hi = sorted((a1, a2))
    short, long_ = sorted((n1, n2))
    assert LA.monthly_payment(p, lo, short) <= LA.monthly_payment(p, hi, short) * (1 + 1e-12)
    assert LA.monthly_payment(p, lo, long_) <= LA.monthly_payment(p, lo, short) * (1 + 1e-12)


# At a near-zero rate the payment approaches principal / term, and the
# remaining balance approaches straight-line paydown.
@given(st.floats(0.0, 1e-6), principal, term, st.data())
def test_near_zero_rate_is_straight_line(a, p, n, data):
    k = data.draw(st.integers(0, n))
    assert close(LA.monthly_payment(p, a, n), p / n, rel=1e-3)
    assert close(LA.remaining_balance(p, a, n, k), p * (1 - k / n), rel=1e-3, abs_=1e-6 * p)


# Remaining balance starts at the principal, ends at zero, and follows
# B_{k+1} = B_k (1 + r) - PMT.
@given(principal, apr, term, st.data())
def test_remaining_balance_recursion(p, a, n, data):
    k = data.draw(st.integers(0, n - 1))
    pmt = LA.monthly_payment(p, a, n)
    r = a / 12.0
    assert close(LA.remaining_balance(p, a, n, 0), p, rel=1e-12)
    assert abs(LA.remaining_balance(p, a, n, n)) <= 1e-9 * p
    b_k = LA.remaining_balance(p, a, n, k)
    b_next = LA.remaining_balance(p, a, n, k + 1)
    assert b_next < b_k
    assert close(b_next, b_k * (1 + r) - pmt, rel=1e-9, abs_=1e-8 * p)


# Total interest is non-negative and rises with the rate.
@given(principal, apr, apr, term)
def test_total_interest_rises_with_rate(p, a1, a2, n):
    lo, hi = sorted((a1, a2))
    i_lo = LA.total_interest(p, lo, n)
    assert i_lo >= -1e-9 * p
    assert i_lo <= LA.total_interest(p, hi, n) + 1e-9 * p


# The amortization schedule repays the principal over the term, and its
# interest column sums to total_interest.
@given(principal, apr, term)
def test_amortization_schedule_repays_principal(p, a, n):
    rows = LA.amortization_schedule(p, a, n)
    assert n - 1 <= len(rows) <= n  # final sub-half-cent residual may be dropped
    assert abs(float(rows["principal"].sum()) - p) <= 0.005 + 1e-9 * p
    assert abs(float(rows["interest"].sum()) - LA.total_interest(p, a, n)) <= 0.01 + 1e-9 * p


# Extra principal never adds interest or months, and more extra saves more.
@given(principal, st.floats(0.01, 0.15), st.integers(60, 360),
       st.floats(1.0, 2_000.0), st.floats(1.0, 2_000.0))
def test_extra_payments_save_interest_and_time(p, a, n, e1, e2):
    lo, hi = sorted((e1, e2))
    small = LA.extra_payment_savings(p, a, n, lo)
    big = LA.extra_payment_savings(p, a, n, hi)
    assert small["interest_saved"] >= -0.01 and small["months_saved"] >= 0
    assert big["new_interest"] <= small["new_interest"] + 0.01
    assert big["new_months"] <= small["new_months"]


# Ratio identities: CLTV >= LTV, LTV x value = loan, DSCR x debt = NOI.
@given(principal, st.floats(0.0, 5e5), st.floats(50_000.0, 5e6),
       st.floats(1_000.0, 1e6), st.floats(1_000.0, 1e6))
def test_ltv_and_dscr_identities(loan, heloc, value, noi, debt):
    ltv = LA.loan_to_value(loan, value)
    assert close(ltv * value, loan)
    assert LA.combined_ltv(loan, heloc, value) >= ltv
    assert close(LA.debt_service_coverage_ratio(noi, debt) * debt, noi)


# Points pay for themselves: breakeven months x monthly saving = points cost.
@given(principal, st.floats(0.25, 3.0), st.floats(0.001, 0.01), st.integers(120, 360),
       st.floats(0.03, 0.10))
def test_points_breakeven_recovers_cost(p, pts, cut, n, a):
    months = LA.points_breakeven(p, pts, cut, n, a)
    saving = LA.monthly_payment(p, a, n) - LA.monthly_payment(p, a - cut, n)
    assert close(months * saving, p * pts / 100, rel=1e-9)


# An ARM reset rate never exceeds the lifetime cap or the fully indexed rate,
# and the new payment is the level payment at the capped rate.
@given(principal, st.floats(0.0, 0.08), st.floats(0.01, 0.04), st.integers(60, 360),
       st.floats(0.01, 0.06), st.floats(0.02, 0.08))
def test_arm_reset_respects_cap(bal, index, margin, n, cap, initial):
    res = LA.arm_payment_after_reset(bal, index, margin, n, cap, initial)
    assert res["capped_rate"] <= min(index + margin, initial + cap) + 1e-6
    # capped_rate is reported rounded to 6 dp, so recompute it unrounded.
    capped = min(index + margin, initial + cap)
    assert close(res["new_payment"], round(LA.monthly_payment(bal, capped, n), 2), abs_=1e-9)
