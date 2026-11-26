# /// script
# dependencies = ["numpy", "scipy"]
# requires-python = ">=3.11"
# ///
"""
Asset Allocation Toolkit
=========================
Mean-variance optimization, efficient frontier construction, minimum variance
portfolio, Black-Litterman model, risk parity, and glide path generation.

Part of Layer 4 (Portfolio Construction) in the finance skills framework.
"""

import argparse
import sys
import numpy as np
from scipy.optimize import minimize

# Portfolio variances are O(1e-3 to 1e-2), so SLSQP's default ftol (1e-6) can
# stop at the equal-weight starting point well short of the optimum. A tight
# tolerance, with exact gradients so SLSQP can reach it, makes the solvers
# converge to the true constrained optimum.
_SLSQP_OPTIONS = {"ftol": 1e-12, "maxiter": 1000}


class MeanVarianceOptimizer:
    """Solve mean-variance optimization problems.

    Parameters
    ----------
    expected_returns : np.ndarray
        Array of expected returns for each asset.
    cov_matrix : np.ndarray
        n x n covariance matrix of asset returns.
    risk_aversion : float, optional
        Risk aversion parameter (lambda). Higher values penalize variance
        more heavily. Default is 2.0.
    """

    def __init__(
        self,
        expected_returns: np.ndarray,
        cov_matrix: np.ndarray,
        risk_aversion: float = 2.0,
    ):
        self.expected_returns = np.asarray(expected_returns, dtype=np.float64)
        self.cov_matrix = np.asarray(cov_matrix, dtype=np.float64)
        self.risk_aversion = risk_aversion
        self.n_assets = len(self.expected_returns)

    def optimal_weights(self, long_only: bool = True) -> np.ndarray:
        """Compute optimal portfolio weights maximizing risk-adjusted return.

        Solves: max w'*mu - (lambda/2) * w'*Sigma*w
        subject to: sum(w) = 1, w >= 0 (if long_only).

        Parameters
        ----------
        long_only : bool, optional
            If True, enforce non-negative weights. Default is True.

        Returns
        -------
        np.ndarray
            Optimal weight vector.
        """
        w0 = np.ones(self.n_assets) / self.n_assets

        def neg_utility(w: np.ndarray) -> float:
            ret = w @ self.expected_returns
            var = w @ self.cov_matrix @ w
            return -(ret - (self.risk_aversion / 2.0) * var)

        def neg_utility_grad(w: np.ndarray) -> np.ndarray:
            return -(self.expected_returns - self.risk_aversion * (self.cov_matrix @ w))

        constraints = [{"type": "eq", "fun": lambda w: np.sum(w) - 1.0,
                        "jac": lambda w: np.ones_like(w)}]
        bounds = [(0.0, 1.0)] * self.n_assets if long_only else [(None, None)] * self.n_assets

        result = minimize(
            neg_utility,
            w0,
            method="SLSQP",
            jac=neg_utility_grad,
            bounds=bounds,
            constraints=constraints,
            options=_SLSQP_OPTIONS,
        )
        if not result.success:
            raise RuntimeError(
                f"Mean-variance optimization failed to converge: {result.message}. "
                "Check that the covariance matrix is positive semi-definite and "
                "the constraints are feasible."
            )
        return result.x

    def minimum_variance_weights(self, long_only: bool = True) -> np.ndarray:
        """Compute the minimum variance portfolio weights.

        Solves: min w'*Sigma*w subject to: sum(w) = 1, w >= 0 (if long_only).

        Parameters
        ----------
        long_only : bool, optional
            If True, enforce non-negative weights. Default is True.

        Returns
        -------
        np.ndarray
            Minimum variance weight vector.
        """
        w0 = np.ones(self.n_assets) / self.n_assets

        def portfolio_variance(w: np.ndarray) -> float:
            return float(w @ self.cov_matrix @ w)

        def variance_grad(w: np.ndarray) -> np.ndarray:
            return 2.0 * (self.cov_matrix @ w)

        constraints = [{"type": "eq", "fun": lambda w: np.sum(w) - 1.0,
                        "jac": lambda w: np.ones_like(w)}]
        bounds = [(0.0, 1.0)] * self.n_assets if long_only else [(None, None)] * self.n_assets

        result = minimize(
            portfolio_variance,
            w0,
            method="SLSQP",
            jac=variance_grad,
            bounds=bounds,
            constraints=constraints,
            options=_SLSQP_OPTIONS,
        )
        if not result.success:
            raise RuntimeError(
                f"Minimum-variance optimization failed to converge: {result.message}. "
                "Check that the covariance matrix is positive semi-definite."
            )
        return result.x

    def efficient_frontier(
        self,
        n_points: int = 50,
        long_only: bool = True,
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Compute the efficient frontier by tracing optimal portfolios.

        Parameters
        ----------
        n_points : int, optional
            Number of points along the frontier. Default is 50.
        long_only : bool, optional
            If True, enforce non-negative weights. Default is True.

        Returns
        -------
        tuple[np.ndarray, np.ndarray, np.ndarray]
            - risks: array of portfolio volatilities
            - returns: array of portfolio expected returns
            - all_weights: (n_points x n_assets) matrix of weights
        """
        # Find return range: from min-variance portfolio to max-return asset
        mv_weights = self.minimum_variance_weights(long_only=long_only)
        min_ret = float(mv_weights @ self.expected_returns)
        max_ret = float(np.max(self.expected_returns))

        target_returns = np.linspace(min_ret, max_ret, n_points)
        risks = np.zeros(n_points)
        returns = np.zeros(n_points)
        all_weights = np.zeros((n_points, self.n_assets))

        for i, target in enumerate(target_returns):
            w0 = np.ones(self.n_assets) / self.n_assets

            def portfolio_variance(w: np.ndarray) -> float:
                return float(w @ self.cov_matrix @ w)

            def variance_grad(w: np.ndarray) -> np.ndarray:
                return 2.0 * (self.cov_matrix @ w)

            constraints = [
                {"type": "eq", "fun": lambda w: np.sum(w) - 1.0,
                 "jac": lambda w: np.ones_like(w)},
                {"type": "eq", "fun": lambda w, t=target: w @ self.expected_returns - t,
                 "jac": lambda w: self.expected_returns},
            ]
            bounds = [(0.0, 1.0)] * self.n_assets if long_only else [(None, None)] * self.n_assets

            result = minimize(
                portfolio_variance,
                w0,
                method="SLSQP",
                jac=variance_grad,
                bounds=bounds,
                constraints=constraints,
                options=_SLSQP_OPTIONS,
            )
            if not result.success:
                raise RuntimeError(
                    f"Efficient frontier optimization failed at target return "
                    f"{target:.4%}: {result.message}. The target may be "
                    "infeasible under the given constraints."
                )

            all_weights[i] = result.x
            risks[i] = np.sqrt(result.x @ self.cov_matrix @ result.x)
            returns[i] = result.x @ self.expected_returns

        return risks, returns, all_weights

    def portfolio_stats(self, weights: np.ndarray) -> dict:
        """Compute return, volatility, and Sharpe-like ratio for given weights.

        Parameters
        ----------
        weights : np.ndarray
            Portfolio weight vector.

        Returns
        -------
        dict
            - 'expected_return': float
            - 'volatility': float
            - 'utility': float (mean-variance utility)
        """
        w = np.asarray(weights, dtype=np.float64)
        ret = float(w @ self.expected_returns)
        vol = float(np.sqrt(w @ self.cov_matrix @ w))
        utility = ret - (self.risk_aversion / 2.0) * (vol ** 2)
        return {
            "expected_return": ret,
            "volatility": vol,
            "utility": utility,
        }


class BlackLitterman:
    """Implement the Black-Litterman model for blending equilibrium with views.

    Parameters
    ----------
    cov_matrix : np.ndarray
        n x n covariance matrix of asset returns.
    market_weights : np.ndarray
        Market capitalization weights of the assets.
    risk_aversion : float, optional
        Market risk aversion parameter (lambda). Default is 2.5.
    tau : float, optional
        Scalar uncertainty of equilibrium prior (typically 0.025-0.05).
        Default is 0.05.
    """

    def __init__(
        self,
        cov_matrix: np.ndarray,
        market_weights: np.ndarray,
        risk_aversion: float = 2.5,
        tau: float = 0.05,
    ):
        self.cov_matrix = np.asarray(cov_matrix, dtype=np.float64)
        self.market_weights = np.asarray(market_weights, dtype=np.float64)
        self.risk_aversion = risk_aversion
        self.tau = tau
        self.n_assets = len(self.market_weights)

    def equilibrium_returns(self) -> np.ndarray:
        """Compute implied equilibrium returns: Pi = lambda * Sigma * w_mkt.

        Returns
        -------
        np.ndarray
            Vector of implied equilibrium expected returns.
        """
        return self.risk_aversion * (self.cov_matrix @ self.market_weights)

    def posterior_returns(
        self,
        pick_matrix: np.ndarray,
        view_vector: np.ndarray,
        view_confidences: np.ndarray,
    ) -> np.ndarray:
        """Compute posterior expected returns blending equilibrium with views.

        E(R) = [(tau*Sigma)^(-1) + P'*Omega^(-1)*P]^(-1)
               * [(tau*Sigma)^(-1)*Pi + P'*Omega^(-1)*Q]

        Parameters
        ----------
        pick_matrix : np.ndarray
            k x n matrix where k is the number of views. Each row identifies
            the assets in a view (e.g., [1, 0, -1] for "asset 0 outperforms
            asset 2").
        view_vector : np.ndarray
            k-element vector of expected returns from views.
        view_confidences : np.ndarray
            k-element vector of view uncertainty variances. Lower values
            indicate higher confidence.

        Returns
        -------
        np.ndarray
            Posterior expected return vector.
        """
        P = np.asarray(pick_matrix, dtype=np.float64)
        Q = np.asarray(view_vector, dtype=np.float64)
        omega = np.diag(np.asarray(view_confidences, dtype=np.float64))

        pi = self.equilibrium_returns()
        tau_sigma = self.tau * self.cov_matrix
        tau_sigma_inv = np.linalg.inv(tau_sigma)
        omega_inv = np.linalg.inv(omega)

        # Posterior precision
        posterior_precision = tau_sigma_inv + P.T @ omega_inv @ P
        # Posterior mean
        posterior_mean = np.linalg.inv(posterior_precision) @ (
            tau_sigma_inv @ pi + P.T @ omega_inv @ Q
        )
        return posterior_mean

    def posterior_covariance(
        self,
        pick_matrix: np.ndarray,
        view_confidences: np.ndarray,
    ) -> np.ndarray:
        """Compute posterior covariance matrix.

        Parameters
        ----------
        pick_matrix : np.ndarray
            k x n pick matrix.
        view_confidences : np.ndarray
            k-element vector of view uncertainty variances.

        Returns
        -------
        np.ndarray
            Posterior covariance matrix (n x n).
        """
        P = np.asarray(pick_matrix, dtype=np.float64)
        omega = np.diag(np.asarray(view_confidences, dtype=np.float64))

        tau_sigma = self.tau * self.cov_matrix
        tau_sigma_inv = np.linalg.inv(tau_sigma)
        omega_inv = np.linalg.inv(omega)

        posterior_precision = tau_sigma_inv + P.T @ omega_inv @ P
        return np.linalg.inv(posterior_precision) + self.cov_matrix


class RiskParity:
    """Compute risk parity (equal risk contribution) portfolio weights.

    Parameters
    ----------
    cov_matrix : np.ndarray
        n x n covariance matrix of asset returns.
    """

    def __init__(self, cov_matrix: np.ndarray):
        self.cov_matrix = np.asarray(cov_matrix, dtype=np.float64)
        self.n_assets = self.cov_matrix.shape[0]

    def risk_contributions(self, weights: np.ndarray) -> np.ndarray:
        """Compute risk contribution of each asset.

        Parameters
        ----------
        weights : np.ndarray
            Portfolio weight vector.

        Returns
        -------
        np.ndarray
            RC_i = w_i * (Sigma * w)_i / sigma_p for each asset.
        """
        w = np.asarray(weights, dtype=np.float64)
        port_vol = np.sqrt(w @ self.cov_matrix @ w)
        if port_vol == 0:
            return np.zeros(self.n_assets)
        sigma_w = self.cov_matrix @ w
        return w * sigma_w / port_vol

    def optimal_weights(self) -> np.ndarray:
        """Find weights that equalize risk contributions across all assets.

        Solves the convex equal-risk-contribution problem (Maillard,
        Roncalli and Teiletche 2010; Spinu 2013):

            min_y  (1/2) * y'*Sigma*y - (1/n) * sum(ln y_i),  y > 0

        whose first-order condition y_i * (Sigma*y)_i = 1/n makes every risk
        contribution equal; the weights are w = y / sum(y). Unlike minimizing
        squared RC differences directly, this objective has a unique
        minimum, so the solver cannot stall at a spurious corner solution.

        Returns
        -------
        np.ndarray
            Risk parity weight vector (long-only, fully invested).
        """
        n = self.n_assets
        # ERC weights are invariant to scaling Sigma; normalize for a
        # well-scaled objective.
        sigma = self.cov_matrix / np.mean(np.diag(self.cov_matrix))

        def objective(y: np.ndarray) -> float:
            return float(0.5 * y @ sigma @ y - np.sum(np.log(y)) / n)

        def gradient(y: np.ndarray) -> np.ndarray:
            return sigma @ y - 1.0 / (n * y)

        y0 = np.ones(n) / np.sqrt(np.sum(sigma))
        result = minimize(
            objective,
            y0,
            jac=gradient,
            method="SLSQP",
            bounds=[(1e-12, None)] * n,
            options={"ftol": 1e-14, "maxiter": 1000},
        )
        if not result.success:
            raise RuntimeError(
                f"Risk parity optimization failed to converge: {result.message}. "
                "Check that the covariance matrix is positive definite and "
                "well-conditioned."
            )
        return result.x / np.sum(result.x)


def glide_path(
    ages: np.ndarray,
    equity_start: float = 0.90,
    equity_end: float = 0.30,
    transition_start: int = 25,
    transition_end: int = 65,
) -> np.ndarray:
    """Generate a glide path for age-based asset allocation.

    Linearly reduces equity allocation from equity_start to equity_end
    over the transition period. Holds constant outside the transition range.

    Parameters
    ----------
    ages : np.ndarray
        Array of ages at which to compute the equity allocation.
    equity_start : float, optional
        Equity allocation at the start of the transition period.
        Default is 0.90 (90%).
    equity_end : float, optional
        Equity allocation at the end of the transition period.
        Default is 0.30 (30%).
    transition_start : int, optional
        Age at which the glide path begins reducing equity. Default is 25.
    transition_end : int, optional
        Age at which the glide path reaches its minimum equity. Default is 65.

    Returns
    -------
    np.ndarray
        Array of equity allocations corresponding to each age.
    """
    ages = np.asarray(ages, dtype=np.float64)
    equity = np.full_like(ages, equity_start)

    in_transition = (ages >= transition_start) & (ages <= transition_end)
    progress = (ages[in_transition] - transition_start) / (transition_end - transition_start)
    equity[in_transition] = equity_start + progress * (equity_end - equity_start)

    equity[ages > transition_end] = equity_end
    return equity


def _demo() -> None:
    # ----------------------------------------------------------------
    # Demo: Asset allocation toolkit on a 3-asset universe
    # ----------------------------------------------------------------
    np.random.seed(42)

    asset_names = ["US Equity", "Intl Equity", "US Bonds"]
    expected_returns = np.array([0.08, 0.07, 0.03])
    volatilities = np.array([0.16, 0.18, 0.04])

    corr_matrix = np.array([
        [1.00, 0.75, 0.10],
        [0.75, 1.00, 0.05],
        [0.10, 0.05, 1.00],
    ])
    cov_matrix = np.outer(volatilities, volatilities) * corr_matrix

    print("=" * 60)
    print("Asset Allocation Toolkit - Demo")
    print("=" * 60)

    # --- Mean-Variance Optimization ---
    print("\n--- Mean-Variance Optimization ---")
    for lam in [2.0, 4.0, 8.0]:
        mvo = MeanVarianceOptimizer(expected_returns, cov_matrix, risk_aversion=lam)
        w = mvo.optimal_weights(long_only=True)
        stats = mvo.portfolio_stats(w)
        print(f"\nLambda = {lam}:")
        for i, name in enumerate(asset_names):
            print(f"  {name:15s}: {w[i]*100:6.2f}%")
        print(f"  Expected Return:  {stats['expected_return']*100:.2f}%")
        print(f"  Volatility:       {stats['volatility']*100:.2f}%")

    # --- Minimum Variance Portfolio ---
    print("\n--- Minimum Variance Portfolio ---")
    mvo = MeanVarianceOptimizer(expected_returns, cov_matrix)
    mv_w = mvo.minimum_variance_weights(long_only=True)
    mv_stats = mvo.portfolio_stats(mv_w)
    for i, name in enumerate(asset_names):
        print(f"  {name:15s}: {mv_w[i]*100:6.2f}%")
    print(f"  Volatility: {mv_stats['volatility']*100:.2f}%")

    # --- Efficient Frontier ---
    print("\n--- Efficient Frontier (5 sample points) ---")
    mvo = MeanVarianceOptimizer(expected_returns, cov_matrix, risk_aversion=2.0)
    risks, rets, all_w = mvo.efficient_frontier(n_points=5, long_only=True)
    print(f"  {'Return':>8s}  {'Risk':>8s}  ", end="")
    print("  ".join(f"{name:>12s}" for name in asset_names))
    for i in range(len(risks)):
        line = f"  {rets[i]*100:7.2f}%  {risks[i]*100:7.2f}%  "
        line += "  ".join(f"{all_w[i, j]*100:11.2f}%" for j in range(len(asset_names)))
        print(line)

    # --- Black-Litterman ---
    print("\n--- Black-Litterman Model ---")
    market_weights = np.array([0.55, 0.30, 0.15])
    bl = BlackLitterman(cov_matrix, market_weights, risk_aversion=2.5, tau=0.05)

    equil = bl.equilibrium_returns()
    print("Equilibrium Returns (Pi):")
    for i, name in enumerate(asset_names):
        print(f"  {name:15s}: {equil[i]*100:.2f}%")

    # View: Intl Equity outperforms US Bonds by 3%
    P = np.array([[0.0, 1.0, -1.0]])
    Q = np.array([0.03])
    omega = np.array([0.001])

    posterior = bl.posterior_returns(P, Q, omega)
    print("\nPosterior Returns (with view: Intl outperforms Bonds by 3%):")
    for i, name in enumerate(asset_names):
        print(f"  {name:15s}: {posterior[i]*100:.2f}% (was {equil[i]*100:.2f}%)")

    # --- Risk Parity ---
    print("\n--- Risk Parity ---")
    rp = RiskParity(cov_matrix)
    rp_w = rp.optimal_weights()
    rp_rc = rp.risk_contributions(rp_w)
    rp_vol = np.sqrt(rp_w @ cov_matrix @ rp_w)
    print("Risk Parity Weights and Risk Contributions:")
    for i, name in enumerate(asset_names):
        print(f"  {name:15s}: w = {rp_w[i]*100:6.2f}%,  RC = {rp_rc[i]:.6f}  "
              f"(%RC = {rp_rc[i]/rp_vol*100:5.1f}%)")
    print(f"  Portfolio Vol: {rp_vol*100:.2f}%")

    # --- Glide Path ---
    print("\n--- Glide Path ---")
    ages = np.array([20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75])
    equity_alloc = glide_path(ages)
    print(f"  {'Age':>5s}  {'Equity':>8s}  {'Bonds':>8s}")
    for age, eq in zip(ages, equity_alloc):
        print(f"  {age:5d}  {eq*100:7.1f}%  {(1-eq)*100:7.1f}%")

    print("\n" + "=" * 60)
    print("Demo complete.")
    print("=" * 60)

def _check(failures: list, name: str, actual: float, expected: float, tol: float) -> None:
    """Record a verification check result."""
    ok = abs(actual - expected) <= tol
    status = "PASS" if ok else "FAIL"
    print(f"  [{status}] {name}: actual={actual:.6g}, expected={expected:.6g}, tol={tol:.2g}")
    if not ok:
        failures.append(name)

def _verify() -> None:
    """Verify key outputs against the SKILL.md worked examples."""
    failures: list = []
    expected_returns = np.array([0.08, 0.07, 0.03])
    vols = np.array([0.16, 0.18, 0.04])
    corr = np.array([[1.0, 0.75, 0.10], [0.75, 1.0, 0.05], [0.10, 0.05, 1.0]])
    cov = np.outer(vols, vols) * corr

    # SKILL.md Example 1: MVO with lambda=4
    mvo = MeanVarianceOptimizer(expected_returns, cov, risk_aversion=4.0)
    w = mvo.optimal_weights(long_only=True)
    stats = mvo.portfolio_stats(w)
    _check(failures, "Ex1 weight US Equity", w[0], 0.519, 0.01)
    _check(failures, "Ex1 weight Intl Equity", w[1], 0.0, 0.01)
    _check(failures, "Ex1 weight US Bonds", w[2], 0.481, 0.01)
    _check(failures, "Ex1 expected return", stats["expected_return"], 0.0560, 5e-4)
    _check(failures, "Ex1 volatility", stats["volatility"], 0.0871, 5e-4)

    # SKILL.md Example 2: Black-Litterman
    bl = BlackLitterman(cov, np.array([0.55, 0.30, 0.15]), risk_aversion=2.5, tau=0.05)
    pi = bl.equilibrium_returns()
    _check(failures, "Ex2 equilibrium US", pi[0], 0.0516, 1e-4)
    _check(failures, "Ex2 equilibrium Intl", pi[1], 0.0541, 1e-4)
    _check(failures, "Ex2 equilibrium Bonds", pi[2], 0.0018, 1e-4)
    post = bl.posterior_returns(np.array([[0.0, 1.0, -1.0]]), np.array([0.03]), np.array([0.001]))
    _check(failures, "Ex2 posterior US", post[0], 0.0428, 1e-4)
    _check(failures, "Ex2 posterior Intl", post[1], 0.0407, 1e-4)
    _check(failures, "Ex2 posterior Bonds", post[2], 0.0023, 1e-4)

    if failures:
        print(f"\n{len(failures)} check(s) FAILED: {', '.join(failures)}")
        sys.exit(1)
    print("\nAll checks passed.")

def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__.strip().splitlines()[2] if __doc__ else "",
        epilog=(
            "Provides: MeanVarianceOptimizer, BlackLitterman, RiskParity, glide_path. "
            "For programmatic use, import this module (asset_allocation) instead of running it. "
            "Bare run executes a demo whose printed values match the SKILL.md worked examples; "
            "--verify asserts those values and exits nonzero on mismatch."
        ),
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="run the verification checks against the SKILL.md worked-example values",
    )
    args = parser.parse_args()
    if args.verify:
        _verify()
    else:
        _demo()


if __name__ == "__main__":
    main()
