# /// script
# dependencies = ["numpy"]
# requires-python = ">=3.11"
# ///
"""
Performance Attribution
========================
Decompose portfolio returns into explainable components: Brinson-Fachler
equity attribution (allocation, selection, interaction effects), factor-based
attribution, and multi-period geometric linking (Carino method).

Part of Layer 5 (Policy & Planning) in the finance skills framework.
"""

import argparse
import math
import sys

import numpy as np


class BrinsonFachler:
    """Brinson-Fachler single-period equity attribution.

    Decomposes active return (portfolio minus benchmark) into allocation,
    selection, and interaction effects by sector.

    Parameters
    ----------
    portfolio_weights : np.ndarray
        Portfolio weight in each sector (must sum to 1.0).
    benchmark_weights : np.ndarray
        Benchmark weight in each sector (must sum to 1.0).
    portfolio_returns : np.ndarray
        Portfolio return in each sector.
    benchmark_returns : np.ndarray
        Benchmark return in each sector.
    sector_names : list[str] or None, optional
        Human-readable sector labels. Default is None (uses numeric indices).
    """

    def __init__(
        self,
        portfolio_weights: np.ndarray,
        benchmark_weights: np.ndarray,
        portfolio_returns: np.ndarray,
        benchmark_returns: np.ndarray,
        sector_names: list[str] | None = None,
    ):
        self.w_p = np.asarray(portfolio_weights, dtype=np.float64)
        self.w_b = np.asarray(benchmark_weights, dtype=np.float64)
        self.r_p = np.asarray(portfolio_returns, dtype=np.float64)
        self.r_b = np.asarray(benchmark_returns, dtype=np.float64)
        self.sector_names = sector_names or [
            f"Sector_{i}" for i in range(len(self.w_p))
        ]

        n = len(self.w_p)
        if not (len(self.w_b) == len(self.r_p) == len(self.r_b) == n):
            raise ValueError(
                "All input arrays must have the same length (one entry per sector)."
            )

    def total_benchmark_return(self) -> float:
        """Compute the total benchmark return.

        Returns
        -------
        float
            R_b = sum(w_b,i * R_b,i)
        """
        return float(np.dot(self.w_b, self.r_b))

    def total_portfolio_return(self) -> float:
        """Compute the total portfolio return.

        Returns
        -------
        float
            R_p = sum(w_p,i * R_p,i)
        """
        return float(np.dot(self.w_p, self.r_p))

    def total_active_return(self) -> float:
        """Compute the total active return.

        Returns
        -------
        float
            R_p - R_b
        """
        return self.total_portfolio_return() - self.total_benchmark_return()

    def allocation_effects(self) -> np.ndarray:
        """Compute the allocation effect for each sector.

        Returns
        -------
        np.ndarray
            A_i = (w_p,i - w_b,i) * (R_b,i - R_b)
            Rewards overweighting sectors that outperform the total benchmark.
        """
        r_b_total = self.total_benchmark_return()
        return (self.w_p - self.w_b) * (self.r_b - r_b_total)

    def selection_effects(self) -> np.ndarray:
        """Compute the selection effect for each sector.

        Returns
        -------
        np.ndarray
            S_i = w_b,i * (R_p,i - R_b,i)
            Rewards outperforming the sector benchmark regardless of weight.
        """
        return self.w_b * (self.r_p - self.r_b)

    def interaction_effects(self) -> np.ndarray:
        """Compute the interaction effect for each sector.

        Returns
        -------
        np.ndarray
            I_i = (w_p,i - w_b,i) * (R_p,i - R_b,i)
            Captures the joint benefit of overweighting and outperforming.
        """
        return (self.w_p - self.w_b) * (self.r_p - self.r_b)

    def summary(self) -> dict:
        """Compute full Brinson-Fachler attribution breakdown.

        Returns
        -------
        dict
            Contains sector-level effects and aggregate totals.
            Keys: 'sectors' (list of dicts per sector), 'total_allocation',
            'total_selection', 'total_interaction', 'total_active_return',
            'portfolio_return', 'benchmark_return'.
        """
        alloc = self.allocation_effects()
        select = self.selection_effects()
        interact = self.interaction_effects()

        sectors = []
        for i, name in enumerate(self.sector_names):
            sectors.append({
                "name": name,
                "portfolio_weight": float(self.w_p[i]),
                "benchmark_weight": float(self.w_b[i]),
                "portfolio_return": float(self.r_p[i]),
                "benchmark_return": float(self.r_b[i]),
                "allocation": float(alloc[i]),
                "selection": float(select[i]),
                "interaction": float(interact[i]),
                "total": float(alloc[i] + select[i] + interact[i]),
            })

        return {
            "sectors": sectors,
            "total_allocation": float(np.sum(alloc)),
            "total_selection": float(np.sum(select)),
            "total_interaction": float(np.sum(interact)),
            "total_active_return": self.total_active_return(),
            "portfolio_return": self.total_portfolio_return(),
            "benchmark_return": self.total_benchmark_return(),
        }


class FactorAttribution:
    """Factor-based performance attribution.

    Decomposes portfolio returns into contributions from systematic risk
    factors and a residual alpha component.

    Parameters
    ----------
    portfolio_returns : np.ndarray
        Array of periodic portfolio excess returns (over the risk-free rate).
        Shape: (n_periods,).
    factor_returns : np.ndarray
        Array of periodic factor returns. Shape: (n_periods, n_factors).
    factor_names : list[str] or None, optional
        Human-readable factor labels. Default is None (uses numeric indices).
    """

    def __init__(
        self,
        portfolio_returns: np.ndarray,
        factor_returns: np.ndarray,
        factor_names: list[str] | None = None,
    ):
        self.portfolio_returns = np.asarray(portfolio_returns, dtype=np.float64)
        self.factor_returns = np.asarray(factor_returns, dtype=np.float64)

        if self.factor_returns.ndim == 1:
            self.factor_returns = self.factor_returns.reshape(-1, 1)

        n_periods, n_factors = self.factor_returns.shape
        if len(self.portfolio_returns) != n_periods:
            raise ValueError(
                f"portfolio_returns has {len(self.portfolio_returns)} periods but "
                f"factor_returns has {n_periods} periods."
            )

        self.factor_names = factor_names or [
            f"Factor_{i}" for i in range(n_factors)
        ]

    def estimate_loadings(self) -> tuple[np.ndarray, float]:
        """Estimate factor loadings (betas) via OLS regression.

        Fits R_p = alpha + sum(beta_k * F_k) + epsilon.

        Returns
        -------
        betas : np.ndarray
            Factor loadings, shape (n_factors,).
        alpha : float
            Intercept (residual alpha per period).
        """
        n_periods, _ = self.factor_returns.shape
        # Add intercept column
        X = np.column_stack([np.ones(n_periods), self.factor_returns])
        # OLS: beta = (X'X)^{-1} X'y
        coeffs, _, _, _ = np.linalg.lstsq(X, self.portfolio_returns, rcond=None)
        alpha = float(coeffs[0])
        betas = coeffs[1:]
        return betas, alpha

    def factor_contributions(
        self,
        betas: np.ndarray | None = None,
    ) -> np.ndarray:
        """Compute the return contribution of each factor over the full period.

        Parameters
        ----------
        betas : np.ndarray or None, optional
            Factor loadings. If None, estimated via OLS.

        Returns
        -------
        np.ndarray
            Contribution of each factor: beta_k * mean(F_k) * n_periods,
            or equivalently beta_k * sum(F_k). Shape: (n_factors,).
        """
        if betas is None:
            betas, _ = self.estimate_loadings()
        mean_factor_returns = np.mean(self.factor_returns, axis=0)
        return betas * mean_factor_returns

    def active_factor_contributions(
        self,
        portfolio_betas: np.ndarray,
        benchmark_betas: np.ndarray,
    ) -> np.ndarray:
        """Compute active factor contributions relative to a benchmark.

        Parameters
        ----------
        portfolio_betas : np.ndarray
            Portfolio factor loadings, shape (n_factors,).
        benchmark_betas : np.ndarray
            Benchmark factor loadings, shape (n_factors,).

        Returns
        -------
        np.ndarray
            Active contribution per factor: (beta_p,k - beta_b,k) * mean(F_k).
            Shape: (n_factors,).
        """
        p_betas = np.asarray(portfolio_betas, dtype=np.float64)
        b_betas = np.asarray(benchmark_betas, dtype=np.float64)
        mean_factor_returns = np.mean(self.factor_returns, axis=0)
        return (p_betas - b_betas) * mean_factor_returns

    def summary(self) -> dict:
        """Compute full factor attribution breakdown.

        Returns
        -------
        dict
            Contains factor loadings, per-period alpha, factor contributions,
            total factor-explained return, total alpha, and total portfolio
            return (mean per-period).
        """
        betas, alpha = self.estimate_loadings()
        contributions = self.factor_contributions(betas)
        mean_portfolio_return = float(np.mean(self.portfolio_returns))
        total_factor_explained = float(np.sum(contributions))

        factors = []
        for i, name in enumerate(self.factor_names):
            factors.append({
                "name": name,
                "beta": float(betas[i]),
                "mean_factor_return": float(np.mean(self.factor_returns[:, i])),
                "contribution": float(contributions[i]),
            })

        return {
            "factors": factors,
            "alpha_per_period": alpha,
            "total_factor_explained": total_factor_explained,
            "total_alpha": alpha,
            "mean_portfolio_return": mean_portfolio_return,
        }


class MultiPeriodLinker:
    """Link single-period attribution effects across multiple periods.

    Uses the Carino smoothing method to scale arithmetic single-period
    effects so they sum exactly to the full-period active return
    (cumulative portfolio return minus cumulative benchmark return).

    Parameters
    ----------
    portfolio_returns : np.ndarray
        Total portfolio return for each period. Shape: (n_periods,).
    benchmark_returns : np.ndarray
        Total benchmark return for each period. Shape: (n_periods,).
    allocation_effects : np.ndarray
        Allocation effect for each period. Shape: (n_periods,).
    selection_effects : np.ndarray
        Selection effect for each period. Shape: (n_periods,).
    interaction_effects : np.ndarray
        Interaction effect for each period. Shape: (n_periods,).
    """

    def __init__(
        self,
        portfolio_returns: np.ndarray,
        benchmark_returns: np.ndarray,
        allocation_effects: np.ndarray,
        selection_effects: np.ndarray,
        interaction_effects: np.ndarray,
    ):
        self.r_p = np.asarray(portfolio_returns, dtype=np.float64)
        self.r_b = np.asarray(benchmark_returns, dtype=np.float64)
        self.alloc = np.asarray(allocation_effects, dtype=np.float64)
        self.select = np.asarray(selection_effects, dtype=np.float64)
        self.interact = np.asarray(interaction_effects, dtype=np.float64)

        n = len(self.r_p)
        if not (
            len(self.r_b) == len(self.alloc) == len(self.select)
            == len(self.interact) == n
        ):
            raise ValueError("All input arrays must have the same length.")

    @staticmethod
    def _carino_factor(r_p: float, r_b: float) -> float:
        """Compute the Carino smoothing factor for a portfolio/benchmark pair.

        k = [ln(1 + r_p) - ln(1 + r_b)] / (r_p - r_b)

        When r_p equals r_b the factor takes its limit, 1 / (1 + r_p).

        Parameters
        ----------
        r_p : float
            Portfolio return.
        r_b : float
            Benchmark return.

        Returns
        -------
        float
            The Carino factor k.
        """
        if abs(r_p - r_b) < 1e-12:
            return 1.0 / (1.0 + r_p)
        return (np.log1p(r_p) - np.log1p(r_b)) / (r_p - r_b)

    def cumulative_active_return(self) -> float:
        """Compute the full-period active return (cumulative difference).

        Returns
        -------
        float
            R_p_cum - R_b_cum, where R_cum = prod(1 + R_t) - 1
        """
        return float(np.prod(1.0 + self.r_p) - np.prod(1.0 + self.r_b))

    def geometric_active_return(self) -> float:
        """Compute the total geometric active return over all periods.

        Returns
        -------
        float
            (1+R_p_cum) / (1+R_b_cum) - 1
        """
        cum_p = float(np.prod(1.0 + self.r_p))
        cum_b = float(np.prod(1.0 + self.r_b))
        return cum_p / cum_b - 1.0

    def carino_link(self) -> dict:
        """Apply the Carino smoothing method for multi-period linking.

        Each period's arithmetic effects are scaled by c_t = k_t / K, where
        k_t is the Carino factor for period t and K is the Carino factor for
        the cumulative returns. When each period's effects sum to that
        period's active return (R_p,t - R_b,t), the linked effects sum
        exactly to the full-period active return R_p_cum - R_b_cum.

        Returns
        -------
        dict
            'linked_allocation', 'linked_selection', 'linked_interaction':
            linked effects that sum to 'cumulative_active_return'. Also
            includes 'geometric_active_return' (for reference) and
            'period_details' (per-period scaling factors).
        """
        n = len(self.r_p)
        cum_p = float(np.prod(1.0 + self.r_p) - 1.0)
        cum_b = float(np.prod(1.0 + self.r_b) - 1.0)

        k_total = self._carino_factor(cum_p, cum_b)
        k_t = np.array([
            self._carino_factor(float(rp), float(rb))
            for rp, rb in zip(self.r_p, self.r_b)
        ])
        c_t = k_t / k_total

        # Linked effects
        linked_alloc = float(np.sum(c_t * self.alloc))
        linked_select = float(np.sum(c_t * self.select))
        linked_interact = float(np.sum(c_t * self.interact))

        period_details = []
        for t in range(n):
            period_details.append({
                "period": t,
                "portfolio_return": float(self.r_p[t]),
                "benchmark_return": float(self.r_b[t]),
                "k_t": float(k_t[t]),
                "c_t": float(c_t[t]),
                "allocation": float(self.alloc[t]),
                "selection": float(self.select[t]),
                "interaction": float(self.interact[t]),
                "scaled_allocation": float(c_t[t] * self.alloc[t]),
                "scaled_selection": float(c_t[t] * self.select[t]),
                "scaled_interaction": float(c_t[t] * self.interact[t]),
            })

        return {
            "linked_allocation": linked_alloc,
            "linked_selection": linked_select,
            "linked_interaction": linked_interact,
            "cumulative_active_return": cum_p - cum_b,
            "geometric_active_return": self.geometric_active_return(),
            "sum_of_linked_effects": linked_alloc + linked_select + linked_interact,
            "period_details": period_details,
        }


def run_demo() -> None:
    """Run the demonstration suite (default when executed with no arguments)."""
    # ----------------------------------------------------------------
    # Demo 1: Brinson-Fachler attribution (matches SKILL.md Example 1)
    # ----------------------------------------------------------------
    print("=" * 60)
    print("Demo 1: Brinson-Fachler Equity Attribution")
    print("=" * 60)

    # Two-sector portfolio from the SKILL.md worked example
    bf = BrinsonFachler(
        portfolio_weights=np.array([0.35, 0.65]),
        benchmark_weights=np.array([0.25, 0.75]),
        portfolio_returns=np.array([0.15, 0.08]),
        benchmark_returns=np.array([0.12, 0.06]),
        sector_names=["Tech", "Healthcare"],
    )

    result = bf.summary()
    print(f"\nPortfolio return:  {result['portfolio_return']:.4f} "
          f"({result['portfolio_return']*100:.2f}%)")
    print(f"Benchmark return:  {result['benchmark_return']:.4f} "
          f"({result['benchmark_return']*100:.2f}%)")
    print(f"Active return:     {result['total_active_return']:.4f} "
          f"({result['total_active_return']*100:.2f}%)")

    print(f"\n{'Sector':<15} {'Alloc':>8} {'Select':>8} {'Interact':>8} {'Total':>8}")
    print("-" * 52)
    for sector in result["sectors"]:
        print(f"{sector['name']:<15} "
              f"{sector['allocation']*100:>7.2f}% "
              f"{sector['selection']*100:>7.2f}% "
              f"{sector['interaction']*100:>7.2f}% "
              f"{sector['total']*100:>7.2f}%")
    print("-" * 52)
    print(f"{'Total':<15} "
          f"{result['total_allocation']*100:>7.2f}% "
          f"{result['total_selection']*100:>7.2f}% "
          f"{result['total_interaction']*100:>7.2f}% "
          f"{result['total_active_return']*100:>7.2f}%")

    # Verify: sum of effects equals active return
    check = (result["total_allocation"] + result["total_selection"]
             + result["total_interaction"])
    print(f"\nVerification: {check*100:.2f}% == {result['total_active_return']*100:.2f}% "
          f"{'(OK)' if abs(check - result['total_active_return']) < 1e-10 else '(MISMATCH)'}")

    # ----------------------------------------------------------------
    # Demo 2: Factor-based attribution (matches SKILL.md Example 2)
    # ----------------------------------------------------------------
    print("\n" + "=" * 60)
    print("Demo 2: Factor-Based Attribution")
    print("=" * 60)

    np.random.seed(42)
    n_periods = 60  # monthly

    # Simulate factor returns
    mkt = np.random.normal(0.05 / 12, 0.04, n_periods)
    smb = np.random.normal(0.02 / 12, 0.03, n_periods)
    hml = np.random.normal(-0.01 / 12, 0.03, n_periods)
    factor_returns = np.column_stack([mkt, smb, hml])

    # Simulate portfolio excess returns: known betas + alpha + noise
    true_betas = np.array([1.1, 0.3, -0.2])
    true_alpha = 0.007 / 12  # ~0.7% annualized alpha
    noise = np.random.normal(0, 0.005, n_periods)
    portfolio_excess = true_alpha + factor_returns @ true_betas + noise

    fa = FactorAttribution(
        portfolio_returns=portfolio_excess,
        factor_returns=factor_returns,
        factor_names=["MKT", "SMB", "HML"],
    )

    fa_result = fa.summary()
    print(f"\nEstimated factor loadings and contributions:")
    print(f"{'Factor':<10} {'Beta':>8} {'Mean Ret':>10} {'Contrib':>10}")
    print("-" * 42)
    for f in fa_result["factors"]:
        print(f"{f['name']:<10} {f['beta']:>8.4f} {f['mean_factor_return']*100:>9.4f}% "
              f"{f['contribution']*100:>9.4f}%")
    print("-" * 42)
    print(f"{'Alpha':<10} {fa_result['alpha_per_period']*100:>8.4f}%/period")
    print(f"\nTotal factor-explained (per period): "
          f"{fa_result['total_factor_explained']*100:.4f}%")
    print(f"Mean portfolio excess return:         "
          f"{fa_result['mean_portfolio_return']*100:.4f}%")

    # ----------------------------------------------------------------
    # Demo 3: Multi-period linking (Carino method)
    # ----------------------------------------------------------------
    print("\n" + "=" * 60)
    print("Demo 3: Multi-Period Linking (Carino Method)")
    print("=" * 60)

    # Simulate 4 quarterly periods
    np.random.seed(99)
    q_port = np.array([0.035, -0.012, 0.048, 0.021])  # quarterly portfolio returns
    q_bench = np.array([0.028, -0.008, 0.040, 0.015])  # quarterly benchmark returns

    # Generate per-period BF attribution for a 3-sector portfolio
    q_alloc = np.array([0.003, -0.001, 0.004, 0.002])
    q_select = np.array([0.003, -0.002, 0.003, 0.003])
    q_interact = np.array([0.001, -0.001, 0.001, 0.001])

    linker = MultiPeriodLinker(
        portfolio_returns=q_port,
        benchmark_returns=q_bench,
        allocation_effects=q_alloc,
        selection_effects=q_select,
        interaction_effects=q_interact,
    )

    link_result = linker.carino_link()
    cum_active = link_result["cumulative_active_return"]
    print(f"\nCumulative active return (R_p - R_b): {cum_active*100:.4f}%")
    print(f"\nLinked effects (Carino method):")
    print(f"  Allocation:   {link_result['linked_allocation']*100:.4f}%")
    print(f"  Selection:    {link_result['linked_selection']*100:.4f}%")
    print(f"  Interaction:  {link_result['linked_interaction']*100:.4f}%")
    print(f"  Sum:          {link_result['sum_of_linked_effects']*100:.4f}%")
    ok = abs(link_result["sum_of_linked_effects"] - cum_active) < 1e-12
    print(f"\nVerification: sum {link_result['sum_of_linked_effects']*100:.4f}% == "
          f"cumulative active {cum_active*100:.4f}% "
          f"{'(OK)' if ok else '(MISMATCH)'}")

    # Show the three ways of stating multi-period active return
    arith_active = float(np.sum(q_port - q_bench))
    print(f"\nSum of period active returns:    {arith_active*100:.4f}%")
    print(f"Cumulative active return:        {cum_active*100:.4f}%")
    print(f"Geometric active return:         "
          f"{link_result['geometric_active_return']*100:.4f}%")

    print("\n" + "=" * 60)
    print("Demo complete.")
    print("=" * 60)


def run_verify() -> int:
    """Assert the demo outputs against the SKILL.md worked-example numbers.

    Returns
    -------
    int
        0 if all checks pass, 1 otherwise.
    """
    failures = 0

    def check(name: str, actual: float, expected: float,
              rel_tol: float = 1e-6, abs_tol: float = 1e-9) -> None:
        nonlocal failures
        ok = math.isclose(actual, expected, rel_tol=rel_tol, abs_tol=abs_tol)
        status = "PASS" if ok else "FAIL"
        print(f"[{status}] {name}: actual={actual:.10g} expected={expected:.10g}")
        if not ok:
            failures += 1

    # SKILL.md Example 1: Brinson-Fachler attribution (Tech / Healthcare)
    bf = BrinsonFachler(
        portfolio_weights=np.array([0.35, 0.65]),
        benchmark_weights=np.array([0.25, 0.75]),
        portfolio_returns=np.array([0.15, 0.08]),
        benchmark_returns=np.array([0.12, 0.06]),
        sector_names=["Tech", "Healthcare"],
    )
    result = bf.summary()
    check("SKILL.md Ex1 portfolio return", result["portfolio_return"], 0.1045)
    check("SKILL.md Ex1 benchmark return", result["benchmark_return"], 0.0750)
    check("SKILL.md Ex1 total active return", result["total_active_return"],
          0.0295)
    check("SKILL.md Ex1 total allocation", result["total_allocation"], 0.0060)
    check("SKILL.md Ex1 total selection", result["total_selection"], 0.0225)
    check("SKILL.md Ex1 total interaction", result["total_interaction"],
          0.0010)
    tech, health = result["sectors"]
    check("SKILL.md Ex1 Tech allocation", tech["allocation"], 0.0045)
    check("SKILL.md Ex1 Tech selection", tech["selection"], 0.0075)
    check("SKILL.md Ex1 Tech interaction", tech["interaction"], 0.0030)
    check("SKILL.md Ex1 Healthcare allocation", health["allocation"], 0.0015)
    check("SKILL.md Ex1 Healthcare selection", health["selection"], 0.0150)
    check("SKILL.md Ex1 Healthcare interaction", health["interaction"],
          -0.0020)

    # SKILL.md Example 2: factor contributions with given betas
    # (single-period factor returns; contributions = beta_k * F_k)
    fa = FactorAttribution(
        portfolio_returns=np.array([0.07]),
        factor_returns=np.array([[0.05, 0.02, -0.01]]),
        factor_names=["MKT", "SMB", "HML"],
    )
    contributions = fa.factor_contributions(betas=np.array([1.1, 0.3, -0.2]))
    check("SKILL.md Ex2 MKT contribution", float(contributions[0]), 0.0550)
    check("SKILL.md Ex2 SMB contribution", float(contributions[1]), 0.0060)
    check("SKILL.md Ex2 HML contribution", float(contributions[2]), 0.0020)
    total_explained = float(np.sum(contributions))
    check("SKILL.md Ex2 factor-explained total", total_explained, 0.0630)
    check("SKILL.md Ex2 alpha", 0.07 - total_explained, 0.0070)

    # Demo 3: multi-period linking inputs (deterministic active returns)
    q_port = np.array([0.035, -0.012, 0.048, 0.021])
    q_bench = np.array([0.028, -0.008, 0.040, 0.015])
    linker = MultiPeriodLinker(
        portfolio_returns=q_port,
        benchmark_returns=q_bench,
        allocation_effects=np.array([0.003, -0.001, 0.004, 0.002]),
        selection_effects=np.array([0.003, -0.002, 0.003, 0.003]),
        interaction_effects=np.array([0.001, -0.001, 0.001, 0.001]),
    )
    check("Demo 3 geometric active return", linker.geometric_active_return(),
          0.0164362629)
    check("Demo 3 arithmetic active return", float(np.sum(q_port - q_bench)),
          0.0170)
    link = linker.carino_link()
    check("Demo 3 linked effects sum to cumulative active return",
          link["sum_of_linked_effects"], link["cumulative_active_return"],
          rel_tol=1e-12)

    if failures:
        print(f"\nFAIL: {failures} check(s) did not match expected values.")
        return 1
    print("\nPASS: all checks matched expected values.")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Performance attribution calculations: Brinson-Fachler "
            "allocation/selection/interaction effects (BrinsonFachler), "
            "OLS factor-based attribution (FactorAttribution), and "
            "multi-period Carino linking (MultiPeriodLinker)."
        ),
        epilog=(
            "Run with no arguments to print the demo suite. "
            "Import as a module: "
            "from performance_attribution import BrinsonFachler, "
            "FactorAttribution, MultiPeriodLinker"
        ),
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="assert demo outputs against the SKILL.md worked-example "
             "numbers; exits nonzero on mismatch",
    )
    args = parser.parse_args()

    if args.verify:
        sys.exit(run_verify())
    run_demo()


if __name__ == "__main__":
    main()
