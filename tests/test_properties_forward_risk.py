"""Property-based tests for forward-risk (wealth-management plugin)."""

import math

import numpy as np
from hypothesis import given, settings
from hypothesis import strategies as st

from conftest import load_script

fr = load_script("forward-risk")
FR = fr.ForwardRisk

# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

confidence = st.floats(0.6, 0.995)
value = st.floats(1e3, 1e9)


def close(a: float, b: float, rel: float = 1e-9, abs_: float = 1e-9) -> bool:
    return math.isclose(a, b, rel_tol=rel, abs_tol=abs_)


@st.composite
def weights(draw, n: int) -> np.ndarray:
    """Long-only weights that sum to 1."""
    raw = np.array(draw(st.lists(st.floats(0.01, 1.0), min_size=n, max_size=n)))
    return raw / raw.sum()


@st.composite
def annual_cov(draw, n: int) -> np.ndarray:
    """Positive-definite annualised covariance: A A' + eps I.

    Entries of A up to 0.3 give asset vols up to roughly 0.3 * sqrt(n).
    """
    a = np.array(draw(st.lists(st.floats(-0.3, 0.3), min_size=n * n, max_size=n * n)))
    a = a.reshape(n, n)
    return a @ a.T + 1e-3 * np.eye(n)


@st.composite
def portfolio(draw):
    n = draw(st.integers(1, 6))
    return draw(weights(n)), draw(annual_cov(n)), draw(value)


# ---------------------------------------------------------------------------
# Parametric VaR / ES
# ---------------------------------------------------------------------------

# VaR rises with confidence; ES (average loss beyond VaR) is at least VaR.
@given(portfolio(), confidence, confidence)
def test_parametric_var_monotone_and_es_dominates(p, c1, c2):
    w, cov, pv = p
    model = FR(w, cov, pv)
    lo, hi = sorted((c1, c2))
    assert model.parametric_var(lo) <= model.parametric_var(hi) * (1 + 1e-12)
    for c in (lo, hi):
        assert model.conditional_var_parametric(c) >= model.parametric_var(c) * (1 - 1e-12)
        assert model.parametric_var(c) > 0


# Square-root-of-time: h-day VaR and ES are sqrt(h) times the 1-day figure,
# matching scale_var; VaR is homogeneous of degree one in portfolio value.
@given(portfolio(), confidence, st.integers(1, 250), st.floats(0.1, 10.0))
def test_parametric_var_sqrt_time_and_linear_in_value(p, c, h, k):
    w, cov, pv = p
    model = FR(w, cov, pv)
    v1 = model.parametric_var(c, 1)
    assert close(model.parametric_var(c, h), v1 * math.sqrt(h), rel=1e-12)
    assert close(FR.scale_var(v1, h), v1 * math.sqrt(h), rel=1e-12)
    assert close(model.conditional_var_parametric(c, h),
                 model.conditional_var_parametric(c, 1) * math.sqrt(h), rel=1e-12)
    assert close(FR(w, cov, k * pv).parametric_var(c), k * v1, rel=1e-12)


# Long-only portfolio volatility never exceeds the weighted sum of asset
# volatilities (correlations are at most 1), so diversified VaR is at most
# the sum of stand-alone VaRs.
@given(portfolio())
def test_portfolio_vol_subadditive(p):
    w, cov, pv = p
    model = FR(w, cov, pv)
    assert model.portfolio_volatility() <= w @ np.sqrt(np.diag(cov)) * (1 + 1e-12)
    assert close(model.portfolio_volatility(False),
                 model.portfolio_volatility() / math.sqrt(252), rel=1e-12)


# Euler allocation: component VaRs sum to total 1-day parametric VaR, and
# component VaR_i = w_i * marginal VaR_i * W.
@given(portfolio(), confidence)
def test_component_var_sums_to_total(p, c):
    w, cov, pv = p
    model = FR(w, cov, pv)
    comp = model.component_var(c)
    total = model.parametric_var(c)
    assert close(comp.sum(), total, rel=1e-9)
    assert np.allclose(comp, w * model.marginal_var(c) * pv, rtol=1e-9)


# Marginal VaR is the gradient of per-dollar VaR, z * sqrt(w' S w / 252),
# with respect to the weights (checked by central differences).
@given(portfolio(), confidence)
def test_marginal_var_is_gradient(p, c):
    w, cov, _ = p
    m = FR(w, cov, 1.0).marginal_var(c)
    eps = 1e-6
    for i in range(len(w)):
        up, dn = w.copy(), w.copy()
        up[i] += eps
        dn[i] -= eps
        g = (FR(up, cov, 1.0).parametric_var(c) - FR(dn, cov, 1.0).parametric_var(c)) / (2 * eps)
        assert close(m[i], g, rel=1e-5, abs_=1e-9)


# ---------------------------------------------------------------------------
# Historical / empirical VaR and ES
# ---------------------------------------------------------------------------

hist = st.lists(st.floats(-0.2, 0.2), min_size=2, max_size=300).map(np.array)


# Empirical VaR rises with confidence, lies within the observed loss range,
# and empirical ES (mean of the tail) is at least VaR.
@given(hist, confidence, confidence, value)
def test_historical_var_monotone_and_es_dominates(r, c1, c2, pv):
    model = FR(np.array([1.0]), np.array([[0.04]]), pv)
    lo, hi = sorted((c1, c2))
    v_lo, v_hi = model.historical_var(r, lo), model.historical_var(r, hi)
    assert v_lo <= v_hi + 1e-9 * pv
    assert -r.max() * pv - 1e-9 * pv <= v_hi <= -r.min() * pv + 1e-9 * pv
    for c in (lo, hi):
        assert model.conditional_var_empirical(r, c) >= model.historical_var(r, c) - 1e-9 * pv


# A (T, n) asset-return matrix is collapsed through the weights, giving the
# same VaR/ES as passing the portfolio return series directly.
@given(st.integers(1, 5).flatmap(lambda n: st.tuples(
    weights(n),
    st.lists(st.lists(st.floats(-0.2, 0.2), min_size=n, max_size=n), min_size=2, max_size=100),
)), confidence)
def test_historical_var_matrix_input_uses_weights(wr, c):
    w, rows = wr
    asset_r = np.array(rows)
    model = FR(w, np.eye(len(w)) * 0.04, 1e6)
    port = asset_r @ w
    assert close(model.historical_var(asset_r, c), model.historical_var(port, c), abs_=1e-6)
    assert close(model.conditional_var_empirical(asset_r, c),
                 model.conditional_var_empirical(port, c), abs_=1e-6)


# ---------------------------------------------------------------------------
# Monte Carlo VaR
# ---------------------------------------------------------------------------

# With a fixed seed the simulated scenarios are identical, so MC VaR is
# monotone in confidence; with zero means it is close to parametric VaR.
# 20k simulations per call, so examples are capped to keep runtime low.
@settings(max_examples=200)
@given(portfolio(), st.floats(0.8, 0.99), st.floats(0.8, 0.99), st.integers(0, 2**32 - 1))
def test_monte_carlo_var_monotone_and_near_parametric(p, c1, c2, seed):
    w, cov, pv = p
    model = FR(w, cov, pv)
    lo, hi = sorted((c1, c2))
    mc_lo = model.monte_carlo_var(lo, n_simulations=20_000, seed=seed)
    mc_hi = model.monte_carlo_var(hi, n_simulations=20_000, seed=seed)
    assert mc_lo <= mc_hi + 1e-9 * pv
    # Sampling error of a tail quantile at 20k draws is a few percent; 15%
    # leaves a wide margin at the 99% tail.
    assert close(mc_hi, model.parametric_var(hi), rel=0.15)


# ---------------------------------------------------------------------------
# Stress and factor decomposition
# ---------------------------------------------------------------------------

# Stress P&L is linear: a uniform shock s on a fully invested portfolio
# moves it by W * s, and P&L is additive across scenarios.
@given(st.integers(1, 8).flatmap(lambda n: st.tuples(
    weights(n),
    st.lists(st.floats(-0.5, 0.5), min_size=n, max_size=n),
    st.lists(st.floats(-0.5, 0.5), min_size=n, max_size=n),
)), value, st.floats(-0.5, 0.5))
def test_stress_scenario_linear(wab, pv, s):
    w, a, b = wab
    a, b = np.array(a), np.array(b)
    f = FR.stress_scenario
    assert close(f(w, pv, np.full(len(w), s)), pv * s, rel=1e-9, abs_=1e-6)
    assert close(f(w, pv, a + b), f(w, pv, a) + f(w, pv, b), rel=1e-9, abs_=1e-6)


# Factor variance plus idiosyncratic variance equals total, both are
# non-negative, the shares add to 100%, and the total matches w' S w for
# S = B F B' + diag(idio).
@given(st.integers(1, 6), st.integers(1, 4), st.data())
def test_factor_decomposition_adds_up(n, k, data):
    w = data.draw(weights(n))
    b = np.array(data.draw(st.lists(st.floats(-2, 2), min_size=n * k, max_size=n * k))).reshape(n, k)
    f = data.draw(annual_cov(k))
    idio = np.array(data.draw(st.lists(st.floats(0.0, 0.2), min_size=n, max_size=n)))
    out = FR.factor_risk_decomposition(w, b, f, idio)
    assert out["factor_variance"] >= -1e-15 and out["idiosyncratic_variance"] >= 0
    assert close(out["total_variance"], out["factor_variance"] + out["idiosyncratic_variance"])
    # Shares are defined only for a risky portfolio (zero total reports 0/0).
    if out["total_variance"] > 1e-12:
        assert close(out["factor_pct"] + out["idiosyncratic_pct"], 100.0, rel=1e-9)
    full = b @ f @ b.T + np.diag(idio)
    assert close(out["total_variance"], w @ full @ w, rel=1e-9, abs_=1e-15)
