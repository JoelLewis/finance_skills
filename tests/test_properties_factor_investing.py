"""Property-based tests for the factor-investing script (FactorInvesting)."""

import math

import numpy as np
from hypothesis import given
from hypothesis import strategies as st

from conftest import load_script

fi = load_script("factor-investing")
FI = fi.FactorInvesting

# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

loading = st.floats(-2.0, 2.0, allow_nan=False)
alpha_s = st.floats(-1.0, 1.0, allow_nan=False)


def close(a: float, b: float, rel: float = 1e-9, abs_: float = 1e-9) -> bool:
    return math.isclose(a, b, rel_tol=rel, abs_tol=abs_)


@st.composite
def regression_data(draw):
    """Well-conditioned factor matrix (percent per month) plus noise.

    Factors and noise come from a seeded Gaussian generator so the design
    matrix is full rank and reasonably conditioned; hand-picked float lists
    tend to be near-collinear, where OLS is legitimately ill-posed.
    """
    k = draw(st.integers(1, 4))
    n = draw(st.integers(k + 5, 120))
    seed = draw(st.integers(0, 2**32 - 1))
    rng = np.random.default_rng(seed)
    F = rng.normal(0.5, 4.0, size=(n, k))
    noise = rng.normal(0.0, 1.0, size=n)
    a = draw(alpha_s)
    b = np.array(draw(st.lists(loading, min_size=k, max_size=k)))
    noise_scale = draw(st.floats(0.01, 5.0))
    return F, a, b, noise * noise_scale


# ---------------------------------------------------------------------------
# multifactor_regression
# ---------------------------------------------------------------------------

@given(regression_data())
def test_noise_free_regression_recovers_true_coefficients(data):
    # With y = alpha + F b exactly, OLS recovers alpha and b, and R^2 = 1.
    F, a, b, _ = data
    y = a + F @ b
    reg = FI.multifactor_regression(y, F)
    assert close(reg["alpha"], a, rel=1e-8, abs_=1e-9)
    for i, bi in enumerate(b):
        assert close(reg["loadings"][f"F{i + 1}"], bi, rel=1e-8, abs_=1e-9)
    if np.std(y) > 1e-6:
        assert close(reg["r_squared"], 1.0, abs_=1e-9)


@given(regression_data())
def test_residuals_orthogonal_to_factors_and_mean_zero(data):
    # OLS normal equations: X'e = 0, i.e. residuals sum to zero (intercept)
    # and are uncorrelated with every factor.
    F, a, b, e = data
    reg = FI.multifactor_regression(a + F @ b + e, F)
    res = reg["residuals"]
    scale = np.linalg.norm(res) * (1 + np.abs(F).max()) * len(res)
    assert abs(res.sum()) <= 1e-9 * scale
    assert np.all(np.abs(F.T @ res) <= 1e-9 * scale)


@given(regression_data())
def test_r_squared_in_unit_interval_and_adjusted_not_larger(data):
    # R^2 is a share of variance explained; adjusting for regressors can
    # only lower it.
    F, a, b, e = data
    reg = FI.multifactor_regression(a + F @ b + e, F)
    assert -1e-12 <= reg["r_squared"] <= 1 + 1e-12
    assert reg["adj_r_squared"] <= reg["r_squared"] + 1e-12


@given(regression_data(), st.floats(0.1, 10.0))
def test_scaling_returns_scales_coefficients_not_t_stats(data, c):
    # Rescaling the fund's returns (e.g. decimals -> percent) scales alpha,
    # loadings and residual vol by c but leaves t-stats and R^2 unchanged.
    F, a, b, e = data
    y = a + F @ b + e
    r1 = FI.multifactor_regression(y, F)
    r2 = FI.multifactor_regression(c * y, F)
    assert close(r2["alpha"], c * r1["alpha"], rel=1e-7, abs_=1e-9)
    assert close(r2["residual_vol"], c * r1["residual_vol"], rel=1e-7)
    assert close(r2["r_squared"], r1["r_squared"], rel=1e-7, abs_=1e-9)
    for key in r1["t_stats"]:
        assert close(r2["t_stats"][key], r1["t_stats"][key], rel=1e-6, abs_=1e-6)
        assert 0.0 <= r1["p_values"][key] <= 1.0


# ---------------------------------------------------------------------------
# expected_return_decomposition
# ---------------------------------------------------------------------------

names = st.lists(st.sampled_from(["MKT", "SMB", "HML", "RMW", "CMA", "MOM"]),
                 min_size=1, max_size=6, unique=True)


@given(names, st.data(), st.floats(0.0, 6.0), st.floats(-5.0, 20.0))
def test_decomposition_adds_up(keys, data, rf, realized):
    # E[R] = R_f + sum(b_k * lambda_k), and implied alpha closes the gap to
    # the realized excess return.
    loadings = {k: data.draw(loading) for k in keys}
    premia = {k: data.draw(st.floats(-3.0, 10.0)) for k in keys}
    d = FI.expected_return_decomposition(loadings, premia, rf, realized)
    expected_excess = sum(loadings[k] * premia[k] for k in keys)
    assert close(d["factor_excess"], expected_excess, abs_=1e-12)
    assert close(d["total_expected"], rf + d["factor_excess"], abs_=1e-12)
    assert close(d["implied_alpha"] + d["factor_excess"], realized, abs_=1e-12)


# ---------------------------------------------------------------------------
# closet_index_diagnostics
# ---------------------------------------------------------------------------

# Volatility starts at 1e-4 percent per period: subnormal volatilities make
# fee_gap / TE overflow to inf, a float artefact, not a finance case.
@given(st.floats(0.0, 1.0), st.one_of(st.just(0.0), st.floats(1e-4, 10.0)),
       st.floats(0.0, 2.0), st.floats(0.0, 0.5), st.sampled_from([4, 12, 52, 252]))
def test_tracking_error_decomposition(r2, vol, fee, index_fee, ppy):
    # Residual variance = (1 - R^2) * total variance; TE annualizes by
    # sqrt(N); breakeven IR * TE recovers the fee gap.
    d = FI.closet_index_diagnostics(r2, vol, fee, index_fee, ppy)
    assert close(d["residual_vol"] ** 2, (1 - r2) * vol**2, rel=1e-9, abs_=1e-12)
    assert close(d["tracking_error"], d["residual_vol"] * math.sqrt(ppy), rel=1e-12)
    assert d["tracking_error"] <= vol * math.sqrt(ppy) + 1e-12
    if d["tracking_error"] > 0:
        assert close(d["breakeven_ir"] * d["tracking_error"], fee - index_fee,
                     rel=1e-9, abs_=1e-12)
    else:
        assert d["breakeven_ir"] == float("inf")


@given(st.floats(0.0, 1.0), st.floats(0.0, 1.0), st.floats(1e-4, 10.0))
def test_closet_flag_monotone_in_r_squared(r2a, r2b, vol):
    # Higher R^2 means lower tracking error, so it can only make the
    # closet-index flag more likely, never less.
    lo, hi = sorted([r2a, r2b])
    f_lo = FI.closet_index_diagnostics(lo, vol, 1.0, 0.05)["closet_index_flag"]
    f_hi = FI.closet_index_diagnostics(hi, vol, 1.0, 0.05)["closet_index_flag"]
    assert f_hi or not f_lo
