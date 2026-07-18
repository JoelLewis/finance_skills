# /// script
# dependencies = ["numpy", "scipy"]
# requires-python = ">=3.11"
# ///
"""
Factor Investing - Reference Implementation

Multifactor OLS regression (Fama-French style), expected-return decomposition
from factor loadings and premia, and closet-index diagnostics based on
R-squared and tracking-error decomposition.

Usage:
    uv run factor_investing.py            # demo + verification (default)
    python factor_investing.py --verify   # same as bare invocation
    python factor_investing.py --help     # list available functions

Dependencies:
    numpy, scipy
"""

import argparse
import sys

import numpy as np
from scipy import stats as sp_stats


class FactorInvesting:
    """Factor-model tools for portfolio construction and fund evaluation:
    multifactor OLS regression, expected-return decomposition from loadings
    and premia, and closet-index diagnostics."""

    @staticmethod
    def multifactor_regression(
        excess_returns: np.ndarray,
        factors: np.ndarray,
        factor_names: list[str] | None = None,
    ) -> dict:
        """Run a multifactor OLS regression of fund excess returns on factors.

        Estimates R_i - R_f = alpha + sum_k(b_k * F_k) + epsilon via numpy
        least squares. For single-factor (CAPM) mechanics and OLS derivations,
        see the statistics-fundamentals skill; this function generalizes its
        ols_regression to K regressors.

        Args:
            excess_returns: 1-D array of fund excess returns (length n).
            factors: 2-D array of factor returns, shape (n, k). Columns are
                long-short factor return series (e.g., MKT, SMB, HML).
            factor_names: Optional list of k factor names for the output
                dictionaries. Defaults to ["F1", ..., "Fk"].

        Returns:
            Dictionary with keys:
                - alpha: intercept (per-period, same units as inputs)
                - loadings: dict of factor name -> coefficient
                - t_stats: dict with "alpha" and each factor name
                - p_values: dict with "alpha" and each factor name
                - r_squared: coefficient of determination
                - adj_r_squared: adjusted for the number of regressors
                - residuals: 1-D array of residuals
                - residual_vol: per-period residual standard deviation
                  (root mean squared error with n - k - 1 dof)

        Raises:
            ValueError: If shapes are inconsistent, n <= k + 1, or the design
                matrix is rank-deficient (collinear factors).
        """
        y = np.asarray(excess_returns, dtype=float)
        F = np.asarray(factors, dtype=float)
        if F.ndim == 1:
            F = F.reshape(-1, 1)
        n, k = F.shape
        if len(y) != n:
            raise ValueError(f"Length mismatch: {len(y)} returns vs {n} factor rows.")
        if factor_names is None:
            factor_names = [f"F{i + 1}" for i in range(k)]
        if len(factor_names) != k:
            raise ValueError(f"Expected {k} factor names, got {len(factor_names)}.")
        if n <= k + 1:
            raise ValueError(
                f"Need more than k + 1 = {k + 1} observations for t-stats; got {n}."
            )

        # Design matrix with intercept; solve via least squares
        X = np.column_stack([np.ones(n), F])
        if np.linalg.matrix_rank(X) < X.shape[1]:
            raise ValueError(
                "Rank-deficient design matrix: factors are collinear (or a "
                "factor is constant), so coefficients are not identified."
            )
        beta_hat, _, _, _ = np.linalg.lstsq(X, y, rcond=None)

        # Residuals, R-squared, adjusted R-squared
        residuals = y - X @ beta_hat
        ss_res = float(np.sum(residuals**2))
        ss_tot = float(np.sum((y - np.mean(y)) ** 2))
        r_squared = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
        dof = n - k - 1
        adj_r_squared = 1.0 - (1.0 - r_squared) * (n - 1) / dof

        # Standard errors and t-statistics
        mse = ss_res / dof
        XtX_inv = np.linalg.inv(X.T @ X)
        se = np.sqrt(np.diag(XtX_inv) * mse)
        t_vals = np.divide(beta_hat, se, out=np.zeros_like(beta_hat), where=se > 0)
        p_vals = 2.0 * (1.0 - sp_stats.t.cdf(np.abs(t_vals), dof))

        keys = ["alpha"] + list(factor_names)
        return {
            "alpha": float(beta_hat[0]),
            "loadings": {name: float(b) for name, b in zip(factor_names, beta_hat[1:])},
            "t_stats": {key: float(t) for key, t in zip(keys, t_vals)},
            "p_values": {key: float(p) for key, p in zip(keys, p_vals)},
            "r_squared": r_squared,
            "adj_r_squared": adj_r_squared,
            "residuals": residuals,
            "residual_vol": float(np.sqrt(mse)),
        }

    @staticmethod
    def expected_return_decomposition(
        loadings: dict[str, float],
        premia: dict[str, float],
        risk_free: float = 0.0,
        realized_excess: float | None = None,
    ) -> dict:
        """Decompose expected return into factor contributions (loading x premium).

        E[R] = R_f + sum_k(b_k * lambda_k), where lambda_k is the assumed
        long-short premium for factor k. If a realized mean excess return is
        supplied, the residual (realized minus factor-implied excess) is
        reported as implied alpha.

        Args:
            loadings: Factor name -> estimated loading (from
                multifactor_regression or held constant by assumption).
            premia: Factor name -> assumed annualized premium, in the same
                units as risk_free (e.g., percent per year). Must contain
                every key in loadings.
            risk_free: Risk-free rate in the same units. Defaults to 0
                (decomposition of excess return only).
            realized_excess: Optional realized mean excess return of the fund;
                enables the implied-alpha output.

        Returns:
            Dictionary with keys:
                - contributions: dict of factor name -> b_k * lambda_k
                - factor_excess: sum of contributions (factor-implied excess)
                - total_expected: risk_free + factor_excess
                - implied_alpha: realized_excess - factor_excess (None when
                  realized_excess is not supplied)

        Raises:
            KeyError: If a loading has no corresponding premium.
        """
        contributions = {name: b * premia[name] for name, b in loadings.items()}
        factor_excess = float(sum(contributions.values()))
        return {
            "contributions": contributions,
            "factor_excess": factor_excess,
            "total_expected": risk_free + factor_excess,
            "implied_alpha": (
                None if realized_excess is None else realized_excess - factor_excess
            ),
        }

    @staticmethod
    def closet_index_diagnostics(
        benchmark_r_squared: float,
        fund_vol: float,
        fund_fee: float,
        index_fee: float,
        periods_per_year: int = 12,
        r_squared_threshold: float = 0.98,
        tracking_error_threshold: float = 2.0,
    ) -> dict:
        """Tracking-error decomposition and closet-index heuristic.

        Decomposes fund volatility into benchmark-explained and residual parts
        using the R-squared of a benchmark regression:
        residual_vol = fund_vol * sqrt(1 - R^2), annualized to a tracking
        error, then computes the information ratio the manager must generate
        just to earn back the fee gap versus an index fund
        (breakeven_ir = fee_gap / tracking_error).

        A fund is flagged as a probable closet indexer when R-squared meets
        r_squared_threshold and annualized tracking error is at or below
        tracking_error_threshold (defaults: R^2 >= 0.98 and TE <= 2%). This is
        a returns-based analog of the holdings-based active-share screen
        (active share below ~60% indicates closet indexing, per Cremers and
        Petajisto 2009).

        Args:
            benchmark_r_squared: R-squared from regressing the fund on its
                benchmark (0 to 1).
            fund_vol: Per-period fund return volatility, in percent (e.g.,
                monthly standard deviation when periods_per_year is 12).
            fund_fee: Fund annual expense ratio, in percent.
            index_fee: Comparable index fund expense ratio, in percent.
            periods_per_year: Periods per year for annualization. Default 12.
            r_squared_threshold: Flag threshold on R-squared. Default 0.98.
            tracking_error_threshold: Flag threshold on annualized tracking
                error, in percent. Default 2.0.

        Returns:
            Dictionary with keys:
                - residual_vol: per-period residual volatility (percent)
                - tracking_error: annualized tracking error (percent)
                - fee_gap: fund_fee - index_fee (percent per year)
                - breakeven_ir: fee_gap / tracking_error (information ratio
                  needed to break even on fees; inf when tracking error is 0)
                - closet_index_flag: True when both thresholds are met

        Raises:
            ValueError: If benchmark_r_squared is outside [0, 1] or fund_vol
                is negative.
        """
        if not 0.0 <= benchmark_r_squared <= 1.0:
            raise ValueError(f"R-squared must be in [0, 1]; got {benchmark_r_squared}.")
        if fund_vol < 0:
            raise ValueError(f"fund_vol must be non-negative; got {fund_vol}.")

        residual_vol = fund_vol * np.sqrt(1.0 - benchmark_r_squared)
        tracking_error = residual_vol * np.sqrt(periods_per_year)
        fee_gap = fund_fee - index_fee
        breakeven_ir = fee_gap / tracking_error if tracking_error > 0 else float("inf")
        return {
            "residual_vol": float(residual_vol),
            "tracking_error": float(tracking_error),
            "fee_gap": float(fee_gap),
            "breakeven_ir": float(breakeven_ir),
            "closet_index_flag": bool(
                benchmark_r_squared >= r_squared_threshold
                and tracking_error <= tracking_error_threshold
            ),
        }


# ---------------------------------------------------------------------------
# Demonstration and verification
# ---------------------------------------------------------------------------

_FUNCTIONS_HELP = """\
Available functions:
  FactorInvesting.multifactor_regression(excess_returns, factors, factor_names)
      # OLS of fund excess returns on K factor return series; returns alpha,
      # loadings, t-stats, p-values, R-squared, residual vol
  FactorInvesting.expected_return_decomposition(loadings, premia, risk_free=0.0,
                                                realized_excess=None)
      # E[R] = R_f + sum(b_k * lambda_k); implied alpha if realized supplied
  FactorInvesting.closet_index_diagnostics(benchmark_r_squared, fund_vol,
                                           fund_fee, index_fee,
                                           periods_per_year=12)
      # residual vol, tracking error, breakeven IR, closet-index flag

Import usage (preferred for programmatic work):
  from factor_investing import FactorInvesting
  FactorInvesting.multifactor_regression(y, factors, ["MKT", "SMB", "HML"])

Running bare (or with --verify) prints a demo on deterministic synthetic
data and asserts the worked-example values from SKILL.md, exiting nonzero
on any mismatch.
"""

_FACTOR_NAMES = ["MKT", "SMB", "HML"]

# SKILL.md Example 1 "true" parameters (percent per month)
_TRUE_ALPHA = 0.037
_TRUE_LOADINGS = np.array([0.98, 0.12, 0.45])
_TARGET_T_ALPHA = 0.6


def _example1_dataset() -> tuple[np.ndarray, np.ndarray]:
    """Construct the deterministic 60-month dataset behind SKILL.md Example 1.

    Factor returns are drawn from a fixed seed. Residuals are projected
    orthogonal to the design matrix (so OLS recovers alpha and the loadings
    exactly) and then scaled so that t(alpha) is exactly 0.6.

    Returns:
        Tuple of (fund excess returns, factor matrix of shape (60, 3)),
        both in percent per month.
    """
    rng = np.random.default_rng(seed=42)
    n = 60
    mkt = 0.60 + 4.5 * rng.standard_normal(n)
    smb = 0.15 + 3.0 * rng.standard_normal(n)
    hml = 0.25 + 3.0 * rng.standard_normal(n)
    factors = np.column_stack([mkt, smb, hml])

    X = np.column_stack([np.ones(n), factors])
    XtX_inv = np.linalg.inv(X.T @ X)

    # Residuals orthogonal to the design matrix -> exact coefficient recovery
    e_raw = rng.standard_normal(n)
    e_orth = e_raw - X @ (XtX_inv @ (X.T @ e_raw))

    # Scale residuals so t(alpha) = alpha / (s * sqrt(g00)) is exactly 0.6
    dof = n - 4
    s_target = _TRUE_ALPHA / (_TARGET_T_ALPHA * np.sqrt(XtX_inv[0, 0]))
    e_scaled = e_orth * (s_target * np.sqrt(dof) / np.linalg.norm(e_orth))

    y = X @ np.concatenate([[_TRUE_ALPHA], _TRUE_LOADINGS]) + e_scaled
    return y, factors


def _demo() -> dict:
    print("=" * 60)
    print("Factor Investing - Reference Implementation Demo")
    print("=" * 60)

    # 1. Three-factor regression (SKILL.md Example 1 dataset, seed 42)
    y, factors = _example1_dataset()
    reg = FactorInvesting.multifactor_regression(y, factors, _FACTOR_NAMES)
    print("\n1. Fama-French 3-Factor Regression (60 months, % per month)")
    print(f"   Alpha:     {reg['alpha']:>8.4f}  (t={reg['t_stats']['alpha']:.2f},"
          f" p={reg['p_values']['alpha']:.4f})  ~{reg['alpha'] * 12:.2f}%/yr")
    for name in _FACTOR_NAMES:
        print(f"   {name}:       {reg['loadings'][name]:>8.4f}  "
              f"(t={reg['t_stats'][name]:.2f}, p={reg['p_values'][name]:.4f})")
    print(f"   R-squared: {reg['r_squared']:.4f}  (adj. {reg['adj_r_squared']:.4f})")
    print(f"   Residual vol: {reg['residual_vol']:.4f}% per month")

    # 2. Expected-return decomposition (SKILL.md Example 2)
    print("\n2. Expected-Return Decomposition (loadings x assumed premia)")
    premia = {"MKT": 6.5, "SMB": 2.0, "HML": 3.0}
    decomp = FactorInvesting.expected_return_decomposition(
        loadings={"MKT": 0.98, "SMB": 0.12, "HML": 0.45},
        premia=premia,
        risk_free=4.0,
        realized_excess=8.4,
    )
    for name, contrib in decomp["contributions"].items():
        print(f"   {name} contribution:  {contrib:>6.2f}%  (premium {premia[name]:.1f}%)")
    print(f"   Factor-implied excess return: {decomp['factor_excess']:.2f}%")
    print(f"   Total expected return (rf 4.0%): {decomp['total_expected']:.2f}%")
    print(f"   Implied alpha (realized 8.4% excess): {decomp['implied_alpha']:.2f}%/yr")

    # 3. Closet-index diagnostics (SKILL.md Example 3)
    print("\n3. Closet-Index Diagnostics")
    diag = FactorInvesting.closet_index_diagnostics(
        benchmark_r_squared=0.99, fund_vol=4.30, fund_fee=0.85, index_fee=0.05
    )
    print(f"   Residual vol:       {diag['residual_vol']:.2f}% per month")
    print(f"   Tracking error:     {diag['tracking_error']:.2f}% annualized")
    print(f"   Fee gap:            {diag['fee_gap']:.2f}%/yr")
    print(f"   Breakeven IR:       {diag['breakeven_ir']:.2f}")
    verdict = "CLOSET INDEXER" if diag["closet_index_flag"] else "genuinely active"
    print(f"   Verdict:            {verdict}")

    print("\n" + "=" * 60)
    print("All calculations completed successfully.")
    print("=" * 60)
    return {"regression": reg, "decomposition": decomp, "diagnostics": diag}


def _verify(results: dict) -> None:
    """Assert that key outputs match the SKILL.md worked examples."""
    # --- Example 1: 3-factor regression ---
    reg = results["regression"]
    assert abs(reg["alpha"] - 0.037) < 1e-9, f"Example 1 alpha mismatch: {reg['alpha']}"
    for name, expected in zip(_FACTOR_NAMES, _TRUE_LOADINGS):
        got = reg["loadings"][name]
        assert abs(got - expected) < 1e-9, f"Example 1 {name} loading mismatch: {got}"
    assert abs(reg["t_stats"]["alpha"] - 0.60) < 1e-9, (
        f"Example 1 t(alpha) mismatch: {reg['t_stats']['alpha']}"
    )
    assert abs(reg["alpha"] * 12 - 0.44) < 5e-3, (
        f"Example 1 annualized alpha mismatch: {reg['alpha'] * 12}"
    )
    assert abs(reg["t_stats"]["MKT"] - 58.1) < 0.05, (
        f"Example 1 t(MKT) mismatch: {reg['t_stats']['MKT']}"
    )
    assert abs(reg["t_stats"]["SMB"] - 4.6) < 0.05, (
        f"Example 1 t(SMB) mismatch: {reg['t_stats']['SMB']}"
    )
    assert abs(reg["t_stats"]["HML"] - 23.1) < 0.05, (
        f"Example 1 t(HML) mismatch: {reg['t_stats']['HML']}"
    )
    assert abs(reg["r_squared"] - 0.986) < 5e-4, (
        f"Example 1 R-squared mismatch: {reg['r_squared']}"
    )
    assert abs(reg["residual_vol"] - 0.457) < 5e-4, (
        f"Example 1 residual vol mismatch: {reg['residual_vol']}"
    )

    # --- Example 2: expected-return decomposition ---
    decomp = results["decomposition"]
    contribs = decomp["contributions"]
    assert abs(contribs["MKT"] - 6.37) < 1e-9, f"Example 2 MKT contribution: {contribs['MKT']}"
    assert abs(contribs["SMB"] - 0.24) < 1e-9, f"Example 2 SMB contribution: {contribs['SMB']}"
    assert abs(contribs["HML"] - 1.35) < 1e-9, f"Example 2 HML contribution: {contribs['HML']}"
    assert abs(decomp["factor_excess"] - 7.96) < 1e-9, (
        f"Example 2 factor excess mismatch: {decomp['factor_excess']}"
    )
    assert abs(decomp["total_expected"] - 11.96) < 1e-9, (
        f"Example 2 total expected mismatch: {decomp['total_expected']}"
    )
    assert abs(decomp["implied_alpha"] - 0.44) < 1e-9, (
        f"Example 2 implied alpha mismatch: {decomp['implied_alpha']}"
    )

    # --- Example 3: closet-index diagnostics ---
    diag = results["diagnostics"]
    assert abs(diag["residual_vol"] - 0.43) < 5e-4, (
        f"Example 3 residual vol mismatch: {diag['residual_vol']}"
    )
    assert abs(diag["tracking_error"] - 1.49) < 5e-3, (
        f"Example 3 tracking error mismatch: {diag['tracking_error']}"
    )
    assert abs(diag["breakeven_ir"] - 0.54) < 5e-3, (
        f"Example 3 breakeven IR mismatch: {diag['breakeven_ir']}"
    )
    assert diag["closet_index_flag"] is True, "Example 3 should flag closet indexing"

    print("\nVerification PASSED: outputs match SKILL.md worked examples")
    print(f"  Example 1 alpha/t(alpha):   {reg['alpha']:.3f}% per month / {reg['t_stats']['alpha']:.2f}")
    print(f"  Example 1 loadings:         MKT {reg['loadings']['MKT']:.2f}, "
          f"SMB {reg['loadings']['SMB']:.2f}, HML {reg['loadings']['HML']:.2f}")
    print(f"  Example 1 R-squared:        {reg['r_squared']:.3f}")
    print(f"  Example 2 factor excess:    {decomp['factor_excess']:.2f}% "
          f"(implied alpha {decomp['implied_alpha']:.2f}%)")
    print(f"  Example 3 TE/breakeven IR:  {diag['tracking_error']:.2f}% / "
          f"{diag['breakeven_ir']:.2f}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Factor investing reference implementation.",
        epilog=_FUNCTIONS_HELP,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="run the demo and assert outputs match the SKILL.md worked "
        "examples (this is also the default when run with no arguments)",
    )
    parser.parse_args()

    # Bare invocation and --verify behave identically: demo + verification.
    results = _demo()
    try:
        _verify(results)
    except AssertionError as exc:
        print(f"\nVerification FAILED: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
