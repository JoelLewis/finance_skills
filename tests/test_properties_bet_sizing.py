"""Property-based tests for the bet-sizing script (Kelly and position sizing)."""

import math

import numpy as np
from hypothesis import given
from hypothesis import strategies as st

from conftest import load_script

bs = load_script("bet-sizing")
KC = bs.KellyCriterion
PSz = bs.PositionSizer

# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

win_prob = st.floats(0.01, 0.99, allow_nan=False)
odds = st.floats(0.1, 10.0, allow_nan=False)
excess = st.floats(-0.2, 0.3, allow_nan=False)
vol = st.floats(0.02, 0.8, allow_nan=False)
fraction = st.floats(0.0, 1.0, allow_nan=False)


def close(a: float, b: float, rel: float = 1e-9, abs_: float = 1e-9) -> bool:
    return math.isclose(a, b, rel_tol=rel, abs_tol=abs_)


def log_growth(p: float, b: float, f: float) -> float:
    """Expected log growth of a binary bet staking fraction f of wealth."""
    return p * math.log1p(b * f) + (1 - p) * math.log1p(-f)


# ---------------------------------------------------------------------------
# Discrete Kelly
# ---------------------------------------------------------------------------

@given(win_prob, odds, st.floats(0.001, 0.2))
def test_discrete_kelly_maximizes_expected_log_growth(p, b, step):
    # The Kelly fraction is the argmax of E[log wealth]; any nearby stake
    # (still inside [0, 1)) grows wealth no faster.
    f = bs.KellyCriterion.discrete_kelly(p, b)
    assert 0.0 <= f < 1.0
    g_star = log_growth(p, b, f)
    for g in (f - step, f + step):
        if 0.0 <= g < 1.0:
            assert log_growth(p, b, g) <= g_star + 1e-12


@given(win_prob, odds)
def test_discrete_kelly_zero_without_edge(p, b):
    # No bet when the expected profit per dollar, b p - q, is not positive.
    f = KC.discrete_kelly(p, b)
    if b * p - (1 - p) <= 0:
        assert f == 0.0
    else:
        assert f > 0.0


@given(odds)
def test_discrete_kelly_fair_bet_is_zero(b):
    # At the fair win probability p = 1 / (1 + b) the edge is exactly zero.
    p = 1.0 / (1.0 + b)
    assert abs(KC.discrete_kelly(p, b)) <= 1e-12


@given(win_prob, win_prob, odds)
def test_discrete_kelly_monotone_in_win_probability(p1, p2, b):
    # A better chance of winning never calls for a smaller stake.
    lo, hi = sorted([p1, p2])
    assert KC.discrete_kelly(lo, b) <= KC.discrete_kelly(hi, b) + 1e-15


# ---------------------------------------------------------------------------
# Continuous Kelly
# ---------------------------------------------------------------------------

@given(excess, vol, st.floats(-3.0, 3.0))
def test_continuous_kelly_maximizes_growth_rate(mu, sigma, f):
    # g(f) = f mu - f^2 sigma^2 / 2 is maximized at f* = mu / sigma^2 with
    # g(f*) = mu^2 / (2 sigma^2).
    k = KC(mu, sigma)
    f_star = k.continuous_kelly()
    assert close(k.growth_rate(f_star), k.max_growth_rate(), rel=1e-9, abs_=1e-15)
    assert k.growth_rate(f) <= k.max_growth_rate() + 1e-12


@given(excess, vol, st.floats(0.0, 2.0))
def test_fractional_kelly_growth_is_2c_minus_c_squared(mu, sigma, c):
    # Staking c f* earns (2c - c^2) g*: half Kelly keeps 75% of the growth.
    k = KC(mu, sigma)
    g = k.growth_rate(k.fractional_kelly(c))
    g_star = k.max_growth_rate()
    # Absolute tolerance scales with g*: near c = 2 the two terms of g(f)
    # cancel and leave rounding noise of order eps * g*.
    assert close(g, (2 * c - c * c) * g_star, rel=1e-9, abs_=1e-12 * (1 + g_star))


@given(excess, vol, fraction, fraction)
def test_fractional_kelly_is_linear_in_fraction(mu, sigma, a, b):
    # f(a) + f(b) = f(a + b), and f(1) is full Kelly.
    k = KC(mu, sigma)
    assert close(k.fractional_kelly(a) + k.fractional_kelly(b),
                 k.fractional_kelly(a + b), rel=1e-12, abs_=1e-15)
    assert k.fractional_kelly(1.0) == k.continuous_kelly()


@given(vol)
def test_zero_edge_means_zero_allocation(sigma):
    # No expected excess return -> no position and no growth.
    k = KC(0.0, sigma)
    assert k.continuous_kelly() == 0.0
    assert k.max_growth_rate() == 0.0


@given(excess, vol, st.floats(0.1, 10.0))
def test_kelly_scales_with_inverse_variance(mu, sigma, s):
    # Doubling volatility quarters the Kelly allocation (f* ~ 1 / sigma^2).
    a = KC(mu, sigma).continuous_kelly()
    b = KC(mu, sigma * s).continuous_kelly()
    assert close(b * s * s, a, rel=1e-9, abs_=1e-15)


# ---------------------------------------------------------------------------
# Position sizing
# ---------------------------------------------------------------------------

@given(st.floats(0.001, 0.2), vol, st.floats(1e3, 1e9), st.floats(1.0, 3.0))
def test_volatility_target_and_var_consistent(target, sigma, value, z):
    # A position sized to target risk contributes exactly target * z * V of VaR.
    w = PSz.volatility_target_size(target, sigma)
    assert close(w * sigma, target, rel=1e-12)
    var = PSz.position_var(w, sigma, value, z)
    assert close(var, target * z * value, rel=1e-9)


@given(st.floats(0.01, 0.5), vol, st.floats(1.0, 4.0))
def test_drawdown_sizing_hits_drawdown_budget(max_dd, sigma, m):
    # Expected max drawdown of the position (w * m * sigma) equals the budget.
    w = PSz.max_drawdown_size(max_dd, sigma, m)
    assert close(w * m * sigma, max_dd, rel=1e-12)


@st.composite
def conviction(draw):
    n = draw(st.integers(1, 20))
    e = np.array(draw(st.lists(st.floats(0.0, 5.0), min_size=n, max_size=n)))
    c = np.array(draw(st.lists(st.floats(0.0, 5.0), min_size=n, max_size=n)))
    return e, c


@given(conviction(), st.floats(0.01, 0.25))
def test_conviction_sizes_proportional_and_capped(ec, cap):
    # Weights are proportional to edge x certainty, top idea gets the cap.
    e, c = ec
    w = PSz.conviction_weighted_sizes(e, c, cap)
    raw = e * c
    if raw.max() == 0:
        # No conviction anywhere -> no positions.
        assert np.all(w == 0)
        return
    assert close(float(w.max()), cap, rel=1e-12)
    assert np.all(w >= 0) and np.all(w <= cap * (1 + 1e-12))
    assert np.allclose(w * raw.max(), raw * cap, rtol=1e-9, atol=1e-15)
