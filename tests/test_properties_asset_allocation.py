"""Property-based tests for the asset-allocation script.

Each test states a rule from portfolio theory that must hold for every valid
input (see the asset-allocation SKILL.md), then checks it on random inputs.
"""

import math

import numpy as np
from hypothesis import given, settings
from hypothesis import strategies as st

from conftest import load_script

aa = load_script("asset-allocation")

MVO = aa.MeanVarianceOptimizer
BL = aa.BlackLitterman
RP = aa.RiskParity

# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------


def close(a: float, b: float, rel: float = 1e-9, abs_: float = 1e-9) -> bool:
    return math.isclose(a, b, rel_tol=rel, abs_tol=abs_)


@st.composite
def cov_matrix(draw, n: int) -> np.ndarray:
    """Positive-definite covariance with realistic scale.

    Volatilities 3%-40% and a random correlation matrix built as
    normalized A @ A.T, mixed with the identity so the smallest eigenvalue
    stays away from zero (keeps the optimizers well-conditioned).
    """
    vols = np.array(draw(st.lists(st.floats(0.03, 0.40), min_size=n, max_size=n)))
    a = np.array(draw(st.lists(st.floats(-1, 1), min_size=n * n, max_size=n * n))).reshape(n, n)
    g = a @ a.T + 1e-3 * np.eye(n)
    d = np.sqrt(np.diag(g))
    corr = 0.8 * g / np.outer(d, d) + 0.2 * np.eye(n)
    return np.outer(vols, vols) * corr


@st.composite
def weights(draw, n: int) -> np.ndarray:
    """Non-negative weights that sum to 1."""
    raw = np.array(draw(st.lists(st.floats(0.0, 1.0), min_size=n, max_size=n))) + 1e-6
    return raw / raw.sum()


@st.composite
def universe(draw, min_n: int = 2, max_n: int = 6):
    n = draw(st.integers(min_n, max_n))
    # Distinct expected returns on a 1 bp grid: if every asset has the same
    # mean the frontier collapses to one point and its two equality
    # constraints become linearly dependent (SLSQP reports a singular matrix).
    bps = draw(st.lists(st.integers(0, 1500), min_size=n, max_size=n, unique=True))
    mu = np.array(bps) / 10_000
    return mu, draw(cov_matrix(n))


def variance(w: np.ndarray, cov: np.ndarray) -> float:
    return float(w @ cov @ w)


# SLSQP solves are ~ms each; the frontier runs one per point, so optimizer
# tests use fewer examples to keep the file under ~30 s on the ci profile.
OPT = settings(max_examples=200)
FRONTIER = settings(max_examples=60)

# ---------------------------------------------------------------------------
# Mean-variance optimization
# ---------------------------------------------------------------------------


@OPT
@given(universe(), st.floats(0.5, 10.0))
def test_mvo_weights_fully_invested_and_long_only(u, lam):
    # Long-only MVO: weights sum to 1 and each lies in [0, 1].
    mu, cov = u
    w = MVO(mu, cov, risk_aversion=lam).optimal_weights(long_only=True)
    assert close(w.sum(), 1.0, abs_=1e-6)
    assert np.all(w >= -1e-8) and np.all(w <= 1 + 1e-8)


@OPT
@given(universe(), st.floats(0.5, 10.0), st.data())
def test_mvo_utility_beats_any_feasible_portfolio(u, lam, data):
    # The optimum maximizes w'mu - (lambda/2) w'Sigma w over the simplex, so
    # no other long-only fully invested portfolio has higher utility.
    mu, cov = u
    opt = MVO(mu, cov, risk_aversion=lam)
    w_star = opt.optimal_weights(long_only=True)
    w_other = data.draw(weights(len(mu)))
    # Small tolerance for SLSQP convergence slack.
    assert opt.portfolio_stats(w_star)["utility"] >= opt.portfolio_stats(w_other)["utility"] - 1e-9


@OPT
@given(universe(), st.data())
def test_min_variance_below_any_feasible_portfolio(u, data):
    # The minimum-variance portfolio has variance no greater than any other
    # long-only fully invested portfolio, including each single asset.
    mu, cov = u
    w_mv = MVO(mu, cov).minimum_variance_weights(long_only=True)
    assert close(w_mv.sum(), 1.0, abs_=1e-6)
    assert np.all(w_mv >= -1e-8)
    w_other = data.draw(weights(len(mu)))
    v_mv = variance(w_mv, cov)
    assert v_mv <= variance(w_other, cov) + 1e-9
    assert v_mv <= float(np.min(np.diag(cov))) + 1e-9


@OPT
@given(universe(), st.floats(0.5, 10.0))
def test_higher_risk_aversion_never_raises_volatility(u, lam):
    # Doubling lambda penalizes variance more, so the optimal portfolio's
    # variance cannot increase (comparative statics of the MV utility).
    mu, cov = u
    w_lo = MVO(mu, cov, risk_aversion=lam).optimal_weights()
    w_hi = MVO(mu, cov, risk_aversion=2 * lam).optimal_weights()
    # Tolerance covers SLSQP's convergence slack on each solve.
    assert variance(w_hi, cov) <= variance(w_lo, cov) + 1e-9


@FRONTIER
@given(universe(max_n=5))
def test_efficient_frontier_risk_and_return_non_decreasing(u):
    # Along the frontier, target return rises from the min-variance return to
    # the max asset return, and the minimum variance needed rises with it.
    mu, cov = u
    risks, rets, all_w = MVO(mu, cov).efficient_frontier(n_points=8)
    assert np.all(np.diff(rets) >= -1e-6)
    assert np.all(np.diff(risks) >= -1e-6)
    assert np.allclose(all_w.sum(axis=1), 1.0, atol=1e-6)
    assert np.all(all_w >= -1e-8)
    assert close(rets[-1], float(mu.max()), abs_=1e-5)


# ---------------------------------------------------------------------------
# Black-Litterman
# ---------------------------------------------------------------------------


@given(universe(), st.data(), st.floats(0.5, 5.0))
def test_equilibrium_returns_recover_market_weights(u, data, lam):
    # Pi = lambda * Sigma * w_mkt is reverse optimization: unconstrained MV
    # weights under Pi, Sigma^-1 Pi / lambda, give back w_mkt.
    _, cov = u
    w_mkt = data.draw(weights(cov.shape[0]))
    pi = BL(cov, w_mkt, risk_aversion=lam).equilibrium_returns()
    assert np.allclose(np.linalg.solve(cov, pi) / lam, w_mkt, atol=1e-8)


@given(universe(), st.data(), st.floats(0.01, 0.1))
def test_bl_posterior_equals_prior_when_view_matches_equilibrium(u, data, tau):
    # A view whose return Q equals the equilibrium-implied P*Pi carries no new
    # information, so the posterior mean equals Pi.
    _, cov = u
    n = cov.shape[0]
    bl = BL(cov, data.draw(weights(n)), tau=tau)
    pi = bl.equilibrium_returns()
    i, j = data.draw(st.permutations(range(n)))[:2]
    p = np.zeros((1, n))
    p[0, i], p[0, j] = 1.0, -1.0
    post = bl.posterior_returns(p, p @ pi, np.array([data.draw(st.floats(1e-4, 0.1))]))
    assert np.allclose(post, pi, atol=1e-9)


@given(universe(), st.data(), st.floats(0.01, 0.1))
def test_bl_posterior_view_lies_between_prior_and_view(u, data, tau):
    # The posterior view portfolio return P*E(R) is a precision-weighted blend
    # of the prior P*Pi and the view Q, and it moves toward Q as confidence
    # rises (Omega falls).
    _, cov = u
    n = cov.shape[0]
    bl = BL(cov, data.draw(weights(n)), tau=tau)
    pi = bl.equilibrium_returns()
    i, j = data.draw(st.permutations(range(n)))[:2]
    p = np.zeros((1, n))
    p[0, i], p[0, j] = 1.0, -1.0
    q = np.array([data.draw(st.floats(-0.1, 0.1))])
    omega = data.draw(st.floats(1e-4, 0.1))
    prior_v, view = float((p @ pi)[0]), float(q[0])
    post_v = float((p @ bl.posterior_returns(p, q, np.array([omega])))[0])
    post_v_conf = float((p @ bl.posterior_returns(p, q, np.array([omega / 10])))[0])
    lo, hi = min(prior_v, view), max(prior_v, view)
    assert lo - 1e-9 <= post_v <= hi + 1e-9
    assert abs(post_v_conf - view) <= abs(post_v - view) + 1e-9


@given(universe(), st.data(), st.floats(0.01, 0.1))
def test_bl_posterior_covariance_between_sigma_and_prior_sigma(u, data, tau):
    # Posterior covariance = Sigma + M^-1 with 0 < M^-1 <= tau*Sigma: adding a
    # view can only shrink parameter uncertainty, so Sigma <= post <= (1+tau)Sigma
    # in the positive semi-definite order.
    _, cov = u
    n = cov.shape[0]
    bl = BL(cov, data.draw(weights(n)), tau=tau)
    p = np.zeros((1, n))
    p[0, data.draw(st.integers(0, n - 1))] = 1.0
    post = bl.posterior_covariance(p, np.array([data.draw(st.floats(1e-4, 0.1))]))
    scale = float(np.max(np.diag(cov)))
    assert np.min(np.linalg.eigvalsh(post - cov)) >= -1e-10 * scale
    assert np.min(np.linalg.eigvalsh((1 + tau) * cov - post)) >= -1e-10 * scale


# ---------------------------------------------------------------------------
# Risk parity
# ---------------------------------------------------------------------------


@given(universe(), st.data())
def test_risk_contributions_sum_to_portfolio_volatility(u, data):
    # Euler decomposition: sum_i w_i (Sigma w)_i / sigma_p = sigma_p.
    _, cov = u
    w = data.draw(weights(cov.shape[0]))
    rc = RP(cov).risk_contributions(w)
    assert close(rc.sum(), math.sqrt(variance(w, cov)), rel=1e-9)


@OPT
@given(universe(max_n=8))
def test_risk_parity_equalizes_risk_contributions(u):
    # Risk parity: RC_i = RC_j for all i, j, with long-only fully invested
    # weights (the long-only ERC portfolio exists and is unique for any
    # positive-definite Sigma).
    _, cov = u
    rp = RP(cov)
    w = rp.optimal_weights()
    assert close(w.sum(), 1.0, abs_=1e-9)
    assert np.all(w > 0)
    rc = rp.risk_contributions(w)
    share = rc / rc.sum()
    assert np.allclose(share, 1.0 / len(w), atol=1e-4)


@OPT
@given(st.floats(0.03, 0.40), st.floats(0.03, 0.40), st.floats(-0.9, 0.9))
def test_two_asset_risk_parity_inverse_volatility(s1, s2, rho):
    # With two assets, equal risk contribution means w_i proportional to
    # 1/sigma_i (for any correlation, the cross terms are shared equally).
    cov = np.array([[s1 * s1, rho * s1 * s2], [rho * s1 * s2, s2 * s2]])
    w = RP(cov).optimal_weights()
    expected = np.array([1 / s1, 1 / s2]) / (1 / s1 + 1 / s2)
    assert np.allclose(w, expected, atol=1e-4)


# ---------------------------------------------------------------------------
# Glide path
# ---------------------------------------------------------------------------


@given(
    st.lists(st.floats(18, 100), min_size=2, max_size=20),
    st.floats(0.5, 1.0),
    st.floats(0.0, 0.5),
    st.integers(20, 40),
    st.integers(5, 40),
)
def test_glide_path_bounded_and_non_increasing_in_age(ages, eq_start, eq_end, t0, span):
    # Equity share stays between the end and start allocations, equals them
    # outside the transition window, and never rises with age.
    t1 = t0 + span
    ages = np.sort(np.array(ages))
    eq = aa.glide_path(ages, eq_start, eq_end, t0, t1)
    assert np.all(eq <= eq_start + 1e-12) and np.all(eq >= eq_end - 1e-12)
    assert np.all(np.diff(eq) <= 1e-12)
    assert np.allclose(eq[ages < t0], eq_start)
    assert np.allclose(eq[ages > t1], eq_end)
