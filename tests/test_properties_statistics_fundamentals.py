"""Property-based tests for statistics-fundamentals (core plugin)."""

import math

import numpy as np
from hypothesis import assume, given
from hypothesis import strategies as st

from conftest import load_script

stats_mod = load_script("statistics-fundamentals")
SF = stats_mod.StatisticsFundamentals

# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

ret = st.floats(-0.2, 0.2, allow_nan=False)


def close(a: float, b: float, rel: float = 1e-9, abs_: float = 1e-9) -> bool:
    return math.isclose(a, b, rel_tol=rel, abs_tol=abs_)


@st.composite
def series(draw, min_size: int = 4, max_size: int = 60) -> np.ndarray:
    """A 1-D return series with non-trivial dispersion.

    The dispersion floor keeps higher moments away from catastrophic
    cancellation (near-constant series make skew/kurtosis numerically noise).
    """
    x = np.array(draw(st.lists(ret, min_size=min_size, max_size=max_size)))
    assume(np.std(x) > 1e-3)
    return x


@st.composite
def panel(draw, min_obs: int = 3) -> np.ndarray:
    """(n_obs, n_assets) return matrix, each column with non-trivial dispersion."""
    p = draw(st.integers(1, 5))
    n = draw(st.integers(max(min_obs, p + 1), 40))
    flat = draw(st.lists(ret, min_size=n * p, max_size=n * p))
    x = np.array(flat).reshape(n, p)
    assume(np.all(x.std(axis=0) > 1e-3))
    return x


# ---------------------------------------------------------------------------
# Descriptive statistics
# ---------------------------------------------------------------------------

# Order statistics bracket the location measures; std is non-negative.
@given(series(min_size=3))
def test_descriptive_stats_bounds(x):
    d = SF.descriptive_stats(x)
    assert d["std"] > 0
    assert d["min"] <= d["median"] <= d["max"]
    assert d["min"] - 1e-15 <= d["mean"] <= d["max"] + 1e-15


# Location-scale: y = a + b*x scales mean/std by b (|b|), leaves excess
# kurtosis unchanged and multiplies skewness by sign(b).
@given(series(), st.floats(-0.05, 0.05), st.floats(0.1, 10.0), st.booleans())
def test_descriptive_stats_affine_equivariance(x, a, b, flip):
    k = -b if flip else b
    d0 = SF.descriptive_stats(x)
    d1 = SF.descriptive_stats(a + k * x)
    assert close(d1["mean"], a + k * d0["mean"], rel=1e-9, abs_=1e-12)
    assert close(d1["std"], abs(k) * d0["std"], rel=1e-9)
    assert close(d1["skew"], math.copysign(1, k) * d0["skew"], rel=1e-6, abs_=1e-6)
    assert close(d1["kurtosis"], d0["kurtosis"], rel=1e-6, abs_=1e-6)


# ---------------------------------------------------------------------------
# Covariance / correlation / shrinkage
# ---------------------------------------------------------------------------

# A sample covariance matrix is symmetric PSD with the (n-1) variances on its
# diagonal.
@given(panel())
def test_covariance_matrix_symmetric_psd(x):
    c = np.atleast_2d(SF.covariance_matrix(x))
    assert np.allclose(c, c.T)
    assert np.linalg.eigvalsh(c).min() >= -1e-12
    assert np.allclose(np.diag(c), x.var(axis=0, ddof=1))


# Correlations lie in [-1, 1] with ones on the diagonal, and correlation is
# the covariance normalised by the volatilities.
@given(panel())
def test_correlation_matrix_bounds_and_consistency(x):
    r = np.atleast_2d(SF.correlation_matrix(x))
    c = np.atleast_2d(SF.covariance_matrix(x))
    assert np.all(np.abs(r) <= 1 + 1e-12)
    assert np.allclose(np.diag(r), 1.0)
    vol = np.sqrt(np.diag(c))
    assert np.allclose(r, c / np.outer(vol, vol), atol=1e-10)


# Shrinkage is a convex blend of PSD matrices, so it is symmetric PSD, and it
# preserves what the target shares with the sample matrix: the trace for the
# scaled-identity target, the whole diagonal for the diagonal target.
@given(panel(), st.sampled_from(["identity", "diagonal"]))
def test_shrunk_covariance_is_psd_blend(x, target):
    s = np.atleast_2d(SF.covariance_matrix(x))
    shrunk = SF.shrunk_covariance(x, shrinkage_target=target)
    assert np.allclose(shrunk, shrunk.T)
    assert np.linalg.eigvalsh(shrunk).min() >= -1e-12
    if target == "identity":
        assert close(np.trace(shrunk), np.trace(s), rel=1e-9, abs_=1e-15)
    else:
        assert np.allclose(np.diag(shrunk), np.diag(s))
    # Shrinking never moves the matrix further from the target than the sample.
    if target == "identity":
        f = np.trace(s) / s.shape[0] * np.eye(s.shape[0])
    else:
        f = np.diag(np.diag(s))
    assert np.linalg.norm(shrunk - f) <= np.linalg.norm(s - f) + 1e-12


# ---------------------------------------------------------------------------
# Regression
# ---------------------------------------------------------------------------

# OLS normal equations: residuals sum to zero and are orthogonal to x;
# R^2 lies in [0, 1] and equals the squared sample correlation.
@given(series(min_size=3), st.data())
def test_ols_normal_equations(x, data):
    y = np.array(data.draw(st.lists(ret, min_size=len(x), max_size=len(x))))
    assume(np.std(y) > 1e-3)
    res = SF.ols_regression(y, x)
    e = res["residuals"]
    assert abs(e.sum()) <= 1e-10
    assert abs(e @ x) <= 1e-10
    assert -1e-12 <= res["r_squared"] <= 1 + 1e-12
    rho = np.corrcoef(x, y)[0, 1]
    assert close(res["r_squared"], rho**2, abs_=1e-9)
    assert 0.0 <= res["p_values"]["beta"] <= 1.0


# Noise-free data y = a + b*x is fitted exactly.
@given(series(min_size=3), st.floats(-0.02, 0.02), st.floats(-3, 3))
def test_ols_recovers_exact_line(x, a, b):
    res = SF.ols_regression(a + b * x, x)
    assert close(res["alpha"], a, abs_=1e-10)
    assert close(res["beta"], b, abs_=1e-9)


# Rolling OLS returns one fit per window, and the last window equals a plain
# OLS on the trailing observations.
@given(series(min_size=5, max_size=40), st.data())
def test_rolling_regression_matches_last_window(x, data):
    n = len(x)
    y = np.array(data.draw(st.lists(ret, min_size=n, max_size=n)))
    w = data.draw(st.integers(3, n))
    assume(np.std(x[-w:]) > 1e-3)
    assume(all(np.std(x[i:i + w]) > 1e-6 for i in range(n - w + 1)))
    roll = SF.rolling_regression(y, x, w)
    assert len(roll["beta"]) == n - w + 1
    last = SF.ols_regression(y[-w:], x[-w:])
    assert close(roll["beta"][-1], last["beta"], abs_=1e-12)
    assert close(roll["alpha"][-1], last["alpha"], abs_=1e-12)


# ---------------------------------------------------------------------------
# Bootstrap and Jarque-Bera
# ---------------------------------------------------------------------------

# With a fixed seed the resampled means are identical, so a higher
# confidence level can only widen the percentile interval; the interval sits
# inside the data range.
@given(series(min_size=3, max_size=30), st.floats(0.5, 0.9), st.floats(0.0, 0.09))
def test_bootstrap_ci_nested_by_confidence(x, c_lo, gap):
    lo = SF.bootstrap_mean(x, n_samples=500, confidence=c_lo, seed=7)
    hi = SF.bootstrap_mean(x, n_samples=500, confidence=c_lo + gap, seed=7)
    assert lo["ci_lower"] <= lo["ci_upper"]
    assert hi["ci_lower"] <= lo["ci_lower"] + 1e-15
    assert hi["ci_upper"] >= lo["ci_upper"] - 1e-15
    assert x.min() - 1e-15 <= hi["ci_lower"] and hi["ci_upper"] <= x.max() + 1e-15
    assert lo["std_error"] >= 0
    assert close(lo["mean"], float(np.mean(x)))


# JB is a non-negative statistic with a p-value in [0, 1], invariant to any
# affine transform of the data (it depends on skew^2 and kurtosis only).
@given(series(), st.floats(-0.05, 0.05), st.floats(0.1, 10.0), st.booleans())
def test_jarque_bera_bounds_and_invariance(x, a, b, flip):
    k = -b if flip else b
    j0 = SF.jarque_bera_test(x)
    j1 = SF.jarque_bera_test(a + k * x)
    assert j0["statistic"] >= 0
    assert 0.0 <= j0["p_value"] <= 1.0
    assert close(j0["statistic"],
                 len(x) / 6 * (j0["skewness"] ** 2 + j0["kurtosis"] ** 2 / 4))
    assert close(j1["statistic"], j0["statistic"], rel=1e-6, abs_=1e-6)
