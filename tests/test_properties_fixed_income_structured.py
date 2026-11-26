"""Property-based tests for the fixed-income-structured script."""

import math

import numpy as np
from hypothesis import assume, given
from hypothesis import strategies as st

from conftest import load_script

structured = load_script("fixed-income-structured")
PM = structured.PrepaymentModel
MortgageCashFlow = structured.MortgageCashFlow
SA = structured.StructuredAnalytics

# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

# PSA speeds up to 1000% (60% CPR at the plateau). Above 1666% PSA the CPR
# exceeds 100% and the model is undefined.
psa = st.floats(0.0, 1000.0)
cpr = st.floats(0.0, 0.99)
balance = st.floats(1_000.0, 1e8)
# Exactly zero or at least 0.0001%: below ~1e-16 a monthly rate rounds away in
# (1 + r)^n - 1 and the level-payment formula divides by zero (not a
# realistic mortgage rate).
mortgage_rate = st.one_of(st.just(0.0), st.floats(1e-6, 0.15))
term = st.sampled_from([60, 120, 180, 240, 360])


def close(a: float, b: float, rel: float = 1e-9, abs_: float = 1e-9) -> bool:
    return math.isclose(a, b, rel_tol=rel, abs_tol=abs_)


# ---------------------------------------------------------------------------
# PrepaymentModel
# ---------------------------------------------------------------------------

@given(cpr)
def test_cpr_smm_round_trip_and_bounds(c):
    # Twelve months of SMM compound to the CPR, and the monthly rate is
    # never above the annual one.
    smm = PM.smm_from_cpr(c)
    assert close(PM.cpr_from_smm(smm), c, abs_=1e-12)
    assert 0.0 <= smm <= c + 1e-15
    assert close((1 - smm) ** 12, 1 - c, abs_=1e-12)


@given(st.integers(1, 480), psa, psa)
def test_psa_cpr_scales_with_speed_and_ramps(month, s1, s2):
    # CPR is proportional to PSA speed, follows the 30-month ramp to
    # 6% x speed, and the vector schedule agrees with the single-month call.
    assert close(PM.psa_cpr(month, s1) * s2, PM.psa_cpr(month, s2) * s1, abs_=1e-12)
    assert close(PM.psa_cpr(month, 100.0), 0.06 * min(month, 30) / 30, abs_=1e-15)
    sched = PM.psa_cpr_schedule(month, s1)
    assert close(sched[-1], PM.psa_cpr(month, s1), abs_=1e-15)
    assert np.all(np.diff(sched) >= -1e-15)


# ---------------------------------------------------------------------------
# MortgageCashFlow
# ---------------------------------------------------------------------------

@given(balance, mortgage_rate, term, psa, st.floats(0.0, 0.01))
def test_cash_flows_account_for_the_whole_balance(b, r, n, speed, fee):
    # Balance roll-forward holds every month, principal paid sums to the
    # starting balance, and investor cash flow = pass-through interest + principal.
    pt = max(r - fee, 0.0)
    cf = MortgageCashFlow(b, r, n, passthrough_rate=pt).project(speed)
    beg, end = cf["beginning_balance"], cf["ending_balance"]
    tp = cf["total_principal"]
    assert np.allclose(tp, cf["scheduled_principal"] + cf["prepayment"], rtol=1e-12, atol=1e-9)
    assert np.allclose(beg - tp, end, rtol=0, atol=0.011)  # tail < 1 cent is written off
    assert np.allclose(beg[1:], end[:-1], rtol=0, atol=0)
    assert close(tp.sum(), b, rel=1e-9, abs_=0.011)
    assert end[-1] == 0.0
    assert np.allclose(cf["total_cash_flow"], beg * pt / 12 + tp, rtol=1e-12, atol=1e-9)
    # Last-month rounding can leave a balance of about -1e-9 to prepay.
    tol = 1e-12 * b
    assert np.all(cf["prepayment"] >= -tol) and np.all(cf["scheduled_principal"] >= -tol)


@given(balance, st.floats(0.0001, 0.15), term)
def test_zero_prepayment_is_a_level_payment_mortgage(b, r, n):
    # At 0% PSA the pool is a plain amortizing loan: constant payment over the
    # full term and interest = balance x monthly rate.
    cf = MortgageCashFlow(b, r, n).project(0.0)
    assert len(cf["month"]) == n
    assert np.allclose(cf["scheduled_payment"], cf["scheduled_payment"][0], rtol=1e-9)
    assert np.allclose(cf["interest"], cf["beginning_balance"] * r / 12, rtol=1e-12)
    assert np.all(cf["prepayment"] == 0.0)


@given(st.floats(1e6, 1e8), mortgage_rate, term, psa, st.floats(1.0, 100.0))
def test_cash_flows_scale_with_pool_size(b, r, n, speed, k):
    # Every dollar amount is proportional to the pool balance; WAL is not.
    # Pools start at $1M: the projection writes off a tail balance under one
    # cent, a fixed dollar amount that breaks exact scaling for tiny pools.
    small = MortgageCashFlow(b, r, n).project(speed)
    big = MortgageCashFlow(k * b, r, n).project(speed)
    m = min(len(small["month"]), len(big["month"]))
    assert np.allclose(big["total_principal"][:m - 1], k * small["total_principal"][:m - 1],
                       rtol=1e-8, atol=1e-6)
    w_small = SA.weighted_average_life(small["total_principal"], small["month"])
    w_big = SA.weighted_average_life(big["total_principal"], big["month"])
    assert close(w_small, w_big, rel=1e-6)


# ---------------------------------------------------------------------------
# StructuredAnalytics
# ---------------------------------------------------------------------------

# Payments are zero or at least one cent (subnormal floats underflow the sum).
@given(st.lists(st.one_of(st.just(0.0), st.floats(0.01, 1e6)), min_size=1, max_size=360),
       st.integers(0, 120))
def test_wal_lies_within_payment_dates(payments, start):
    # WAL is a principal-weighted average of payment times, so it lies
    # between the first and last payment date.
    p = np.array(payments)
    assume(p.sum() > 0)
    months = np.arange(start + 1, start + len(p) + 1)
    wal = SA.weighted_average_life(p, months)
    paid = months[p > 0]
    assert paid.min() / 12 - 1e-12 <= wal <= paid.max() / 12 + 1e-12


@given(st.floats(0.0001, 0.15), term, psa, psa)
def test_faster_prepayment_shortens_wal(r, n, s1, s2):
    # Faster prepayments return principal sooner, so WAL falls as PSA rises,
    # and never exceeds the zero-prepayment WAL or the loan term.
    assume(abs(s1 - s2) > 1.0)
    lo, hi = sorted((s1, s2))
    out = SA.wal_sensitivity(1_000_000.0, r, n, np.array([0.0, lo, hi]))
    w0, w_lo, w_hi = out["wal_years"]
    assert w_hi < w_lo <= w0 + 1e-12
    assert w0 <= n / 12
