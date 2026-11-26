"""Property-based tests for diversification (wealth-management plugin)."""

import math

import numpy as np
from hypothesis import given
from hypothesis import strategies as st

from conftest import load_script

dv = load_script("diversification")
DA = dv.DiversificationAnalyzer

# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------


def close(a: float, b: float, rel: float = 1e-9, abs_: float = 1e-9) -> bool:
    return math.isclose(a, b, rel_tol=rel, abs_tol=abs_)


@st.composite
def weights(draw, n: int) -> np.ndarray:
    """Long-only weights that sum to 1."""
    raw = np.array(draw(st.lists(st.floats(0.01, 1.0), min_size=n, max_size=n)))
    return raw / raw.sum()


@st.composite
def cov(draw, n: int) -> np.ndarray:
    """Positive-definite covariance A A' + eps I (annual vols up to ~0.3 sqrt(n))."""
    a = np.array(draw(st.lists(st.floats(-0.3, 0.3), min_size=n * n, max_size=n * n)))
    a = a.reshape(n, n)
    return a @ a.T + 1e-3 * np.eye(n)


@st.composite
def portfolio(draw):
    n = draw(st.integers(1, 8))
    return draw(weights(n)), draw(cov(n))


# ---------------------------------------------------------------------------
# Properties
# ---------------------------------------------------------------------------

# Correlations are at most 1, so long-only portfolio vol is at most the
# weighted-average vol: DR >= 1 and the diversification benefit >= 0.
@given(portfolio())
def test_portfolio_vol_below_weighted_average(p):
    a = DA(*p)
    assert a.portfolio_volatility() <= a.weighted_average_volatility() * (1 + 1e-12)
    assert a.diversification_ratio() >= 1 - 1e-12
    assert a.diversification_benefit() >= -1e-12
    assert close(a.portfolio_volatility() ** 2, a.portfolio_variance(), rel=1e-12)


# DR equals sqrt(n) for equal-weight, equal-vol, uncorrelated assets, and 1
# for perfectly correlated assets.
@given(st.integers(1, 20), st.floats(0.01, 0.8))
def test_diversification_ratio_extremes(n, vol):
    w = np.full(n, 1.0 / n)
    a = DA(w, vol**2 * np.eye(n))
    assert close(a.diversification_ratio(), math.sqrt(n), rel=1e-9)
    vols = np.linspace(0.5, 1.5, n) * vol
    b = DA(w, np.outer(vols, vols))
    assert close(b.diversification_ratio(), 1.0, rel=1e-9)


# Euler decomposition: volatility is homogeneous of degree one in weights,
# so risk contributions sum to portfolio vol and percentages sum to 1.
@given(portfolio())
def test_risk_contributions_sum_to_volatility(p):
    a = DA(*p)
    assert close(a.risk_contribution().sum(), a.portfolio_volatility(), rel=1e-9)
    assert close(a.risk_contribution_pct().sum(), 1.0, rel=1e-9)


# Marginal contribution to risk is the gradient of portfolio vol with
# respect to the weights (central differences).
@given(portfolio())
def test_marginal_contribution_is_gradient(p):
    w, c = p
    mrc = DA(w, c).marginal_contribution_to_risk()
    eps = 1e-6
    for i in range(len(w)):
        up, dn = w.copy(), w.copy()
        up[i] += eps
        dn[i] -= eps
        g = (DA(up, c).portfolio_volatility() - DA(dn, c).portfolio_volatility()) / (2 * eps)
        assert close(mrc[i], g, rel=1e-5, abs_=1e-9)


# HHI lies in [1/n, 1], so the effective number of assets lies in [1, n];
# equal weights attain n.
@given(portfolio())
def test_effective_number_of_assets_bounds(p):
    w, c = p
    n = len(w)
    a = DA(w, c)
    assert 1 / n - 1e-12 <= a.hhi_concentration() <= 1 + 1e-12
    assert 1 - 1e-9 <= a.effective_number_of_assets() <= n + 1e-9
    assert close(DA(np.full(n, 1 / n), c).effective_number_of_assets(), n, rel=1e-9)


# Derived correlations lie in [-1, 1] with unit diagonal, and
# build_covariance_matrix inverts the volatility / correlation split.
@given(portfolio())
def test_correlation_round_trip(p):
    w, c = p
    a = DA(w, c)
    corr = a.correlation_matrix()
    assert np.all(np.abs(corr) <= 1 + 1e-12)
    assert np.allclose(np.diag(corr), 1.0)
    rebuilt = dv.build_covariance_matrix(a.asset_volatilities(), corr)
    assert np.allclose(rebuilt, c, rtol=1e-12, atol=1e-15)


# The minimum-variance portfolio is fully invested and no fully invested
# portfolio has lower variance.
@given(portfolio(), st.data())
def test_minimum_variance_weights_minimise_variance(p, data):
    w, c = p
    n = len(w)
    w_mv = DA(w, c).minimum_variance_weights()
    assert close(w_mv.sum(), 1.0, rel=1e-9)
    var_mv = DA(w_mv, c).portfolio_variance()
    other = np.array(data.draw(st.lists(st.floats(-1, 1), min_size=n, max_size=n)))
    other = other - other.mean() + 1.0 / n  # any fully invested portfolio
    assert var_mv <= DA(w, c).portfolio_variance() * (1 + 1e-9)
    assert var_mv <= DA(other, c).portfolio_variance() * (1 + 1e-9)
