"""Property-based tests for the performance-metrics script (PerformanceScorecard)."""

import math

import numpy as np
from hypothesis import assume, given
from hypothesis import strategies as st

from conftest import load_script

pm = load_script("performance-metrics")
PS = pm.PerformanceScorecard

# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

# Daily/monthly-scale returns; a series needs at least 3 points for a
# meaningful sample standard deviation. Subnormal floats are excluded:
# scaling them by k underflows to 0 and flips a return's sign class.
period_return = st.floats(-0.1, 0.1, allow_nan=False, allow_subnormal=False)
rf = st.floats(0.0, 0.005, allow_nan=False)
ppy = st.sampled_from([12, 52, 252])


def series(min_size: int = 3, max_size: int = 60):
    return st.lists(period_return, min_size=min_size, max_size=max_size).map(np.array)


@st.composite
def paired_series(draw, min_size: int = 3, max_size: int = 60):
    n = draw(st.integers(min_size, max_size))
    p = np.array(draw(st.lists(period_return, min_size=n, max_size=n)))
    b = np.array(draw(st.lists(period_return, min_size=n, max_size=n)))
    return p, b


def close(a: float, b: float, rel: float = 1e-9, abs_: float = 1e-9) -> bool:
    return math.isclose(a, b, rel_tol=rel, abs_tol=abs_)


def non_degenerate(x: np.ndarray) -> bool:
    # Excludes (near-)constant series, where std is rounding noise and the
    # ratios are not meaningful.
    return float(np.std(x)) > 1e-6


# ---------------------------------------------------------------------------
# Sharpe / Sortino
# ---------------------------------------------------------------------------

@given(series(), rf, st.floats(0.1, 10.0), ppy)
def test_sharpe_invariant_to_scaling_excess_returns(excess, r_f, k, n):
    # Levering the excess return by k > 0 scales both mean excess and
    # volatility by k, so the Sharpe ratio is unchanged.
    assume(non_degenerate(excess))
    s1 = PS(r_f + excess, risk_free_rate=r_f, periods_per_year=n).sharpe_ratio()
    s2 = PS(r_f + k * excess, risk_free_rate=r_f, periods_per_year=n).sharpe_ratio()
    assert close(s1, s2, rel=1e-6, abs_=1e-9)


@given(series(), rf, ppy)
def test_sharpe_sign_matches_mean_excess_return(excess, r_f, n):
    # Volatility is positive, so Sharpe has the sign of the mean excess return.
    assume(non_degenerate(excess))
    mean_ex = float(np.mean(excess))
    assume(abs(mean_ex) > 1e-9)
    s = PS(r_f + excess, risk_free_rate=r_f, periods_per_year=n).sharpe_ratio()
    assert np.sign(s) == np.sign(mean_ex)


@given(series(), rf, ppy)
def test_sharpe_annualizes_with_sqrt_of_periods(excess, r_f, n):
    # SR_annual = SR_per_period * sqrt(N), not * N.
    assume(non_degenerate(excess))
    s1 = PS(r_f + excess, risk_free_rate=r_f, periods_per_year=1).sharpe_ratio()
    sn = PS(r_f + excess, risk_free_rate=r_f, periods_per_year=n).sharpe_ratio()
    assert close(sn, s1 * math.sqrt(n), rel=1e-9, abs_=1e-12)


@given(series(), rf, ppy)
def test_sortino_at_least_sharpe_when_mean_excess_positive(excess, r_f, n):
    # With MAR = R_f and positive mean excess, every below-MAR return is
    # closer to MAR than to the (higher) mean, so downside deviation
    # <= total volatility and therefore Sortino >= Sharpe.
    assume(non_degenerate(excess))
    assume(float(np.mean(excess)) > 0)
    sc = PS(r_f + excess, risk_free_rate=r_f, periods_per_year=n)
    assert sc.sortino_ratio() >= sc.sharpe_ratio() - 1e-9


@given(series(), rf, st.floats(0.1, 10.0), ppy)
def test_sortino_invariant_to_scaling_excess_returns(excess, r_f, k, n):
    # Downside deviation is positively homogeneous in the excess return.
    assume(float(np.min(excess)) < -1e-6)
    s1 = PS(r_f + excess, risk_free_rate=r_f, periods_per_year=n).sortino_ratio()
    s2 = PS(r_f + k * excess, risk_free_rate=r_f, periods_per_year=n).sortino_ratio()
    assert close(s1, s2, rel=1e-6, abs_=1e-9)


# ---------------------------------------------------------------------------
# Benchmark-relative metrics
# ---------------------------------------------------------------------------

@given(paired_series(), ppy)
def test_information_ratio_is_active_return_over_tracking_error(pb, n):
    # IR = annualized active return / annualized tracking error.
    p, b = pb
    active = p - b
    assume(non_degenerate(active))
    ir = PS(p, b, periods_per_year=n).information_ratio()
    expected = (np.mean(active) * n) / (np.std(active, ddof=1) * math.sqrt(n))
    assert close(ir, expected, rel=1e-9, abs_=1e-12)


@given(paired_series(), ppy)
def test_information_ratio_antisymmetric(pb, n):
    # Swapping portfolio and benchmark negates the active return series.
    p, b = pb
    assume(non_degenerate(p - b))
    ir_pb = PS(p, b, periods_per_year=n).information_ratio()
    ir_bp = PS(b, p, periods_per_year=n).information_ratio()
    assert close(ir_pb, -ir_bp, rel=1e-9, abs_=1e-12)


@given(series(), rf, ppy)
def test_information_ratio_against_cash_equals_sharpe(r, r_f, n):
    # Against a constant risk-free benchmark, active return = excess return
    # and tracking error = total volatility, so IR = Sharpe.
    assume(non_degenerate(r))
    sc = PS(r, np.full_like(r, r_f), risk_free_rate=r_f, periods_per_year=n)
    assert close(sc.information_ratio(), sc.sharpe_ratio(), rel=1e-9, abs_=1e-12)


@given(series(), st.floats(0.2, 3.0), ppy)
def test_treynor_invariant_to_leverage_of_benchmark(b, k, n):
    # A portfolio that is k times the benchmark (R_f = 0) has beta k and
    # mean excess k * mean(b), so Treynor equals the benchmark's own
    # annualized mean return.
    assume(non_degenerate(b))
    t = PS(k * b, b, periods_per_year=n).treynor_ratio()
    assert close(t, float(np.mean(b)) * n, rel=1e-7, abs_=1e-9)


@given(series(), st.floats(0.1, 3.0))
def test_capture_ratios_of_scaled_benchmark_equal_scale(b, k):
    # A portfolio returning k * benchmark captures k of both up and down moves.
    sc = PS(k * b, b)
    if np.any(b > 0):
        assert close(sc.up_capture(), k, rel=1e-9)
    if np.any(b < 0):
        assert close(sc.down_capture(), k, rel=1e-9)


@given(paired_series())
def test_batting_averages_partition_periods(pb):
    # Outperform share + underperform share + tie share = 1.
    p, b = pb
    ba = PS(p, b).batting_average()
    ba_rev = PS(b, p).batting_average()
    ties = float(np.mean(p == b))
    assert 0.0 <= ba <= 1.0
    assert close(ba + ba_rev + ties, 1.0, abs_=1e-12)


# ---------------------------------------------------------------------------
# Omega / Calmar / win-loss
# ---------------------------------------------------------------------------

@given(series(min_size=1), st.floats(-0.02, 0.02))
def test_omega_above_one_iff_mean_above_threshold(r, tau):
    # gains - losses = sum(r - tau), so Omega > 1 exactly when mean(r) > tau.
    om = PS(r).omega_ratio(threshold=tau)
    excess_sum = float(np.sum(r - tau))
    assume(abs(excess_sum) > 1e-9)
    assert (om > 1.0) == (excess_sum > 0)


@given(st.lists(st.floats(0.0, 0.1), min_size=1, max_size=60).map(np.array), ppy)
def test_calmar_no_drawdown_when_all_returns_non_negative(r, n):
    # A path that never falls has zero drawdown; Calmar is inf for a
    # positive return and 0 when the return is zero. (Branch on the
    # compounded growth, since returns below ~1e-16 vanish in 1 + r.)
    c = PS(r, periods_per_year=n).calmar_ratio()
    if np.prod(1.0 + r) > 1.0:
        assert c == float("inf")
    else:
        assert c == 0.0


@given(series(), st.floats(0.1, 10.0))
def test_win_loss_ratio_scale_invariant(r, k):
    # Average win / average loss is a ratio of magnitudes, unchanged by k > 0.
    w1 = PS(r).win_loss_ratio()
    w2 = PS(k * r).win_loss_ratio()
    if math.isinf(w1):
        assert math.isinf(w2)
    else:
        assert close(w1, w2, rel=1e-9, abs_=1e-12)
