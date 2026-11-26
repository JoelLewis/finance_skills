"""Property-based tests for volatility-modeling (wealth-management plugin)."""

import math

import numpy as np
from hypothesis import assume, given, settings
from hypothesis import strategies as st

from conftest import load_script

vm = load_script("volatility-modeling")
VM = vm.VolatilityModeling

# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

daily_ret = st.floats(-0.1, 0.1, allow_nan=False)
lam = st.floats(0.5, 0.995)


def close(a: float, b: float, rel: float = 1e-9, abs_: float = 1e-9) -> bool:
    return math.isclose(a, b, rel_tol=rel, abs_tol=abs_)


@st.composite
def returns(draw, min_size: int = 3, max_size: int = 80) -> np.ndarray:
    x = np.array(draw(st.lists(daily_ret, min_size=min_size, max_size=max_size)))
    # Non-degenerate series: the default EWMA seed is a sample variance.
    assume(np.std(x[:20]) > 1e-4)
    return x


@st.composite
def garch_params(draw):
    """Stationary GARCH(1,1) parameters (alpha + beta < 1)."""
    omega = draw(st.floats(1e-7, 1e-4))
    alpha = draw(st.floats(0.0, 0.3))
    beta = draw(st.floats(0.0, 0.99 - alpha))
    return omega, alpha, beta


# ---------------------------------------------------------------------------
# EWMA
# ---------------------------------------------------------------------------

# Each EWMA update is a convex combination of the previous variance and the
# previous squared return, so every estimate stays positive and inside the
# hull of the seed and the squared returns.
@given(returns(), lam, st.floats(1e-6, 1e-2))
def test_ewma_variance_is_convex_combination(x, l, v0):
    v = VM(x).ewma_variance(lam=l, initial_var=v0)
    assert len(v) == len(x)
    assert v[0] == v0
    lo = min(v0, float((x[:-1] ** 2).min()))
    hi = max(v0, float((x[:-1] ** 2).max()))
    assert np.all(v > 0)
    assert np.all(v >= lo * (1 - 1e-12)) and np.all(v <= hi * (1 + 1e-12))


# Scaling returns by k scales EWMA volatility by |k| (the default seed is a
# sample variance, which scales by k^2); annualisation multiplies by sqrt(ppy).
@given(returns(), lam, st.floats(0.1, 10.0), st.booleans(), st.sampled_from([12, 52, 252]))
def test_ewma_volatility_scale_equivariance(x, l, k, flip, ppy):
    kk = -k if flip else k
    base = VM(x, periods_per_year=ppy).ewma_volatility(lam=l, annualized=False)
    scaled = VM(kk * x, periods_per_year=ppy).ewma_volatility(lam=l, annualized=False)
    ann = VM(x, periods_per_year=ppy).ewma_volatility(lam=l, annualized=True)
    assert np.allclose(scaled, abs(kk) * base, rtol=1e-9)
    assert np.allclose(ann, base * math.sqrt(ppy), rtol=1e-12)


# Effective window 1/(1 - lambda) is at least 1 and grows with lambda.
@given(st.floats(0.01, 0.99), st.floats(0.01, 0.99))
def test_ewma_effective_window_monotone(l1, l2):
    w1, w2 = VM.ewma_effective_window(l1), VM.ewma_effective_window(l2)
    assert w1 >= 1
    assert (w1 <= w2) == (l1 <= l2) or close(w1, w2)


# ---------------------------------------------------------------------------
# GARCH(1,1)
# ---------------------------------------------------------------------------

# Conditional variance is positive and starts at the long-run variance
# V_L = omega / (1 - alpha - beta).
@given(returns(min_size=2), garch_params())
def test_garch_variance_series_positive_from_long_run(x, params):
    omega, alpha, beta = params
    v = VM.garch11_variance_series(x, omega, alpha, beta)
    assert np.all(v > 0)
    assert close(v[0], omega / (1 - alpha - beta), rel=1e-12)


# V_L is a fixed point: if every squared return equals V_L, the conditional
# variance stays at V_L forever.
@given(garch_params(), st.lists(st.booleans(), min_size=2, max_size=60))
def test_garch_long_run_variance_is_fixed_point(params, signs):
    omega, alpha, beta = params
    v_l = omega / (1 - alpha - beta)
    x = np.where(signs, 1.0, -1.0) * math.sqrt(v_l)
    v = VM.garch11_variance_series(x, omega, alpha, beta)
    assert np.allclose(v, v_l, rtol=1e-9)


# Multi-step forecasts start at the current variance (h = 0), move
# monotonically toward V_L, never overshoot it, and converge to it.
@given(garch_params(), st.floats(1e-6, 1e-2))
def test_garch_forecast_mean_reverts_monotonically(params, current):
    omega, alpha, beta = params
    v_l = omega / (1 - alpha - beta)
    h = np.arange(0, 200)
    f = VM.garch11_forecast(current, omega, alpha, beta, h)
    assert close(f[0], current, rel=1e-12)
    lo, hi = min(current, v_l), max(current, v_l)
    assert np.all(f >= lo * (1 - 1e-12)) and np.all(f <= hi * (1 + 1e-12))
    gaps = np.abs(f - v_l)
    assert np.all(np.diff(gaps) <= 1e-18)
    far = VM.garch11_forecast(current, omega, alpha, beta, [100_000])
    assert close(far[0], v_l, rel=1e-9)


# After one half-life a shock has decayed by half: persistence^h = 1/2.
@given(st.floats(0.0, 0.3), st.floats(0.05, 0.69))
def test_garch_half_life_halves_shock(alpha, beta):
    p = alpha + beta
    h = VM.garch11_half_life(alpha, beta)
    assert h > 0
    assert close(p ** h, 0.5, rel=1e-9)
    assert VM.garch11_half_life(alpha, 1.0 - alpha) == float("inf")


# The MLE fit returns stationary parameters within the optimiser bounds and
# internally consistent derived quantities (V_L, half-life, annual vol).
# MLE runs a Python-loop likelihood per evaluation, so examples are capped.
@settings(max_examples=15)
@given(garch_params(), st.integers(0, 2**32 - 1))
def test_garch_fit_outputs_consistent(params, seed):
    omega, alpha, beta = params
    rng = np.random.default_rng(seed)
    n = 300
    r = np.empty(n)
    v = omega / (1 - alpha - beta)
    for t in range(n):
        r[t] = math.sqrt(v) * rng.standard_normal()
        v = omega + alpha * r[t] ** 2 + beta * v
    fit = VM(r).garch11_fit()
    assert fit["omega"] > 0 and fit["alpha"] >= 0 and fit["beta"] >= 0
    assert close(fit["persistence"], fit["alpha"] + fit["beta"], rel=1e-12)
    if fit["persistence"] < 1:
        assert close(fit["long_run_variance"],
                     fit["omega"] / (1 - fit["persistence"]), rel=1e-9)
        assert close(fit["long_run_annual_vol"],
                     math.sqrt(fit["long_run_variance"] * 252), rel=1e-9)
        assert close(fit["half_life"],
                     VM.garch11_half_life(fit["alpha"], fit["beta"]), rel=1e-9)


# ---------------------------------------------------------------------------
# Realized and range-based volatility
# ---------------------------------------------------------------------------

# Rolling close-to-close vol: first window-1 values are NaN, the rest are
# unchanged by a constant shift and scaled by |k| under scaling.
@given(returns(min_size=3), st.data(), st.floats(-0.01, 0.01), st.floats(0.1, 10.0))
def test_realized_volatility_shift_and_scale(x, data, c, k):
    w = data.draw(st.integers(2, len(x)))
    base = VM(x).realized_volatility(window=w)
    assert np.all(np.isnan(base[: w - 1]))
    assert np.all(base[w - 1:] >= 0)
    shifted = VM(x + c).realized_volatility(window=w)
    scaled = VM(-k * x).realized_volatility(window=w)
    assert np.allclose(shifted[w - 1:], base[w - 1:], rtol=1e-6, atol=1e-9)
    assert np.allclose(scaled[w - 1:], k * base[w - 1:], rtol=1e-9, atol=1e-12)


# Parkinson vol depends only on H/L, so rescaling prices leaves it unchanged;
# a zero range gives zero volatility.
@given(st.lists(st.tuples(st.floats(10, 500), st.floats(0.0, 0.1)), min_size=2, max_size=60),
       st.data(), st.floats(0.01, 100.0))
def test_parkinson_volatility_price_scale_invariant(bars, data, c):
    lows = np.array([b[0] for b in bars])
    highs = lows * (1 + np.array([b[1] for b in bars]))
    w = data.draw(st.integers(1, len(bars)))
    base = VM.parkinson_volatility(highs, lows, window=w)
    scaled = VM.parkinson_volatility(c * highs, c * lows, window=w)
    assert np.allclose(scaled[w - 1:], base[w - 1:], rtol=1e-9, atol=1e-12)
    assert np.all(base[w - 1:] >= 0)
    flat = VM.parkinson_volatility(lows, lows, window=w)
    assert np.all(flat[w - 1:] == 0)


# Term-structure points equal the realized vol of the trailing window, and
# windows longer than the data are dropped.
@given(returns(min_size=5, max_size=80))
def test_term_structure_matches_trailing_realized_vol(x):
    model = VM(x)
    windows = [2, 5, 10, len(x), len(x) + 1]
    ts = model.volatility_term_structure(windows=windows)
    assert len(x) + 1 not in ts
    for w, vol in ts.items():
        assert close(vol, model.realized_volatility(window=w)[-1], rel=1e-12)


# Cone percentiles are ordered and bracket the mean and current values.
@given(returns(min_size=10, max_size=80))
def test_volatility_cone_percentiles_ordered(x):
    cone = VM(x).volatility_cone(windows=[5, 10], percentiles=[0, 10, 25, 50, 75, 90, 100])
    for entry in cone.values():
        ps = [entry[f"p{p}"] for p in (0, 10, 25, 50, 75, 90, 100)]
        assert all(a <= b + 1e-15 for a, b in zip(ps, ps[1:]))
        assert ps[0] - 1e-12 <= entry["mean"] <= ps[-1] + 1e-12
        assert ps[0] - 1e-12 <= entry["current"] <= ps[-1] + 1e-12
