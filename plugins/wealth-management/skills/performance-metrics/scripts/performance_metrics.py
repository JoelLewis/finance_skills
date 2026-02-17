"""
Performance Scorecard
======================
Compute risk-adjusted performance ratios: Sharpe, Sortino, Information Ratio,
Calmar, Treynor, Omega, capture ratios, batting average, and win/loss ratio.

Part of Layer 1a (Retrospective) in the finance skills framework.
"""

import numpy as np


class PerformanceScorecard:
    """Compute risk-adjusted performance metrics from historical returns.

    Parameters
    ----------
    returns : np.ndarray
        Array of periodic portfolio simple returns (decimals, e.g., 0.01 = 1%).
    benchmark_returns : np.ndarray or None, optional
        Array of periodic benchmark returns. Required for Information Ratio,
        Treynor Ratio, capture ratios, and batting average. Default is None.
    risk_free_rate : float, optional
        Risk-free rate per period. Default is 0.0. For daily returns with an
        annual risk-free rate of 4%, use 0.04/252 ~ 0.000159.
    periods_per_year : int, optional
        Number of periods in a year for annualization. Default is 252
        (trading days). Use 52 for weekly, 12 for monthly.
    """

    def __init__(
        self,
        returns: np.ndarray,
        benchmark_returns: np.ndarray | None = None,
        risk_free_rate: float = 0.0,
        periods_per_year: int = 252,
    ):
        self.returns = np.asarray(returns, dtype=np.float64)
        self.benchmark_returns = (
            np.asarray(benchmark_returns, dtype=np.float64)
            if benchmark_returns is not None
            else None
        )
        self.risk_free_rate = risk_free_rate
        self.periods_per_year = periods_per_year

    def _require_benchmark(self, metric_name: str) -> np.ndarray:
        """Validate that benchmark returns are available."""
        if self.benchmark_returns is None:
            raise ValueError(
                f"{metric_name} requires benchmark_returns, but none were provided."
            )
        return self.benchmark_returns

    def sharpe_ratio(self) -> float:
        """Compute the annualized Sharpe ratio.

        Returns
        -------
        float
            Sharpe = (mean(R_p - R_f) / std(R_p)) * sqrt(periods_per_year)
        """
        excess = self.returns - self.risk_free_rate
        if np.std(self.returns, ddof=1) == 0:
            return 0.0
        sharpe = np.mean(excess) / np.std(self.returns, ddof=1)
        return float(sharpe * np.sqrt(self.periods_per_year))

    def sortino_ratio(self) -> float:
        """Compute the annualized Sortino ratio.

        Uses downside deviation (threshold = risk-free rate) as the
        denominator instead of total standard deviation.

        Returns
        -------
        float
            Sortino = (mean(R_p - R_f) / DD) * sqrt(periods_per_year)
        """
        excess = self.returns - self.risk_free_rate
        downside = np.minimum(excess, 0.0)
        dd = np.sqrt(np.mean(downside ** 2))
        if dd == 0:
            return float("inf") if np.mean(excess) > 0 else 0.0
        sortino = np.mean(excess) / dd
        return float(sortino * np.sqrt(self.periods_per_year))

    def information_ratio(self) -> float:
        """Compute the annualized Information Ratio.

        Requires benchmark returns.

        Returns
        -------
        float
            IR = (mean(R_p - R_b) * periods_per_year) / (std(R_p - R_b) * sqrt(periods_per_year))
               = (mean(R_p - R_b) / std(R_p - R_b)) * sqrt(periods_per_year)
        """
        benchmark = self._require_benchmark("Information Ratio")
        active_returns = self.returns - benchmark
        te = np.std(active_returns, ddof=1)
        if te == 0:
            return 0.0
        ir = np.mean(active_returns) / te
        return float(ir * np.sqrt(self.periods_per_year))

    def calmar_ratio(self) -> float:
        """Compute the Calmar ratio.

        Returns
        -------
        float
            Calmar = annualized_return / |max_drawdown|
        """
        # Annualized return via geometric compounding
        cumulative = np.prod(1.0 + self.returns)
        n_years = len(self.returns) / self.periods_per_year
        if n_years <= 0:
            return 0.0
        annualized_return = cumulative ** (1.0 / n_years) - 1.0

        # Maximum drawdown
        cumulative_series = np.cumprod(1.0 + self.returns)
        running_max = np.maximum.accumulate(cumulative_series)
        drawdowns = (cumulative_series - running_max) / running_max
        max_dd = abs(np.min(drawdowns))

        if max_dd == 0:
            return float("inf") if annualized_return > 0 else 0.0
        return float(annualized_return / max_dd)

    def treynor_ratio(self) -> float:
        """Compute the annualized Treynor ratio.

        Requires benchmark returns for beta calculation.

        Returns
        -------
        float
            Treynor = (annualized_excess_return) / beta
        """
        benchmark = self._require_benchmark("Treynor Ratio")
        # Beta = cov(r_p, r_b) / var(r_b)
        cov_matrix = np.cov(self.returns, benchmark)
        beta = cov_matrix[0, 1] / cov_matrix[1, 1]

        if beta == 0:
            return 0.0

        mean_excess = np.mean(self.returns - self.risk_free_rate)
        annualized_excess = mean_excess * self.periods_per_year
        return float(annualized_excess / beta)

    def omega_ratio(self, threshold: float = 0.0) -> float:
        """Compute the Omega ratio.

        The ratio of cumulative gains above the threshold to cumulative
        losses below the threshold.

        Parameters
        ----------
        threshold : float, optional
            Return threshold. Default is 0.0.

        Returns
        -------
        float
            Omega = sum(max(r_i - threshold, 0)) / sum(max(threshold - r_i, 0))
        """
        gains = np.sum(np.maximum(self.returns - threshold, 0.0))
        losses = np.sum(np.maximum(threshold - self.returns, 0.0))
        if losses == 0:
            return float("inf") if gains > 0 else 1.0
        return float(gains / losses)

    def up_capture(self) -> float:
        """Compute the up capture ratio.

        Requires benchmark returns.

        Returns
        -------
        float
            Up capture = mean(r_p | r_b > 0) / mean(r_b | r_b > 0)
            Expressed as a ratio (1.0 = 100% capture).
        """
        benchmark = self._require_benchmark("Up Capture")
        up_mask = benchmark > 0
        if not np.any(up_mask):
            return 0.0
        return float(np.mean(self.returns[up_mask]) / np.mean(benchmark[up_mask]))

    def down_capture(self) -> float:
        """Compute the down capture ratio.

        Requires benchmark returns.

        Returns
        -------
        float
            Down capture = mean(r_p | r_b < 0) / mean(r_b | r_b < 0)
            Expressed as a ratio. Values < 1.0 mean the portfolio loses
            less than the benchmark in down markets.
        """
        benchmark = self._require_benchmark("Down Capture")
        down_mask = benchmark < 0
        if not np.any(down_mask):
            return 0.0
        return float(np.mean(self.returns[down_mask]) / np.mean(benchmark[down_mask]))

    def batting_average(self) -> float:
        """Compute the batting average vs the benchmark.

        Requires benchmark returns.

        Returns
        -------
        float
            Fraction of periods where the portfolio outperformed the benchmark.
        """
        benchmark = self._require_benchmark("Batting Average")
        return float(np.mean(self.returns > benchmark))

    def win_loss_ratio(self) -> float:
        """Compute the win/loss ratio.

        Returns
        -------
        float
            Average win / average loss (magnitudes).
        """
        wins = self.returns[self.returns > 0]
        losses = self.returns[self.returns < 0]
        if len(losses) == 0:
            return float("inf") if len(wins) > 0 else 0.0
        if len(wins) == 0:
            return 0.0
        return float(np.mean(wins) / abs(np.mean(losses)))

    def summary(self) -> dict:
        """Compute all available metrics and return as a dictionary.

        Returns
        -------
        dict
            Dictionary of metric names to values. Metrics that require
            a benchmark will be None if no benchmark is provided.
        """
        result = {
            "sharpe_ratio": self.sharpe_ratio(),
            "sortino_ratio": self.sortino_ratio(),
            "calmar_ratio": self.calmar_ratio(),
            "omega_ratio": self.omega_ratio(),
            "win_loss_ratio": self.win_loss_ratio(),
        }

        # Benchmark-dependent metrics
        if self.benchmark_returns is not None:
            result["information_ratio"] = self.information_ratio()
            result["treynor_ratio"] = self.treynor_ratio()
            result["up_capture"] = self.up_capture()
            result["down_capture"] = self.down_capture()
            result["batting_average"] = self.batting_average()
        else:
            result["information_ratio"] = None
            result["treynor_ratio"] = None
            result["up_capture"] = None
            result["down_capture"] = None
            result["batting_average"] = None

        return result


if __name__ == "__main__":
    # ----------------------------------------------------------------
    # Demo: Performance scorecard on synthetic data
    # ----------------------------------------------------------------
    np.random.seed(42)

    # Generate 2 years of daily returns
    n_days = 504

    # Portfolio: slightly positive alpha with moderate volatility
    portfolio_returns = np.random.normal(loc=0.0004, scale=0.013, size=n_days)

    # Benchmark: market returns
    benchmark_returns = np.random.normal(loc=0.0003, scale=0.011, size=n_days)

    # Risk-free rate: ~4% annualized -> daily
    rf_daily = 0.04 / 252

    scorecard = PerformanceScorecard(
        returns=portfolio_returns,
        benchmark_returns=benchmark_returns,
        risk_free_rate=rf_daily,
        periods_per_year=252,
    )

    print("=" * 60)
    print("Performance Scorecard - Demo")
    print("=" * 60)

    # Individual metrics
    print(f"\nSharpe Ratio:       {scorecard.sharpe_ratio():.4f}")
    print(f"Sortino Ratio:      {scorecard.sortino_ratio():.4f}")
    print(f"Information Ratio:  {scorecard.information_ratio():.4f}")
    print(f"Calmar Ratio:       {scorecard.calmar_ratio():.4f}")
    print(f"Treynor Ratio:      {scorecard.treynor_ratio():.4f}")
    print(f"Omega Ratio:        {scorecard.omega_ratio():.4f}")

    print(f"\nUp Capture:         {scorecard.up_capture():.4f} ({scorecard.up_capture()*100:.1f}%)")
    print(f"Down Capture:       {scorecard.down_capture():.4f} ({scorecard.down_capture()*100:.1f}%)")
    print(f"Batting Average:    {scorecard.batting_average():.4f} ({scorecard.batting_average()*100:.1f}%)")
    print(f"Win/Loss Ratio:     {scorecard.win_loss_ratio():.4f}")

    # Summary
    print("\n" + "-" * 40)
    print("Full Summary:")
    print("-" * 40)
    summary = scorecard.summary()
    for metric, value in summary.items():
        if value is not None:
            print(f"  {metric:25s}: {value:.4f}")
        else:
            print(f"  {metric:25s}: N/A (no benchmark)")

    # Context: annualized return and volatility
    cumulative = np.prod(1.0 + portfolio_returns)
    n_years = n_days / 252
    ann_return = cumulative ** (1.0 / n_years) - 1.0
    ann_vol = np.std(portfolio_returns, ddof=1) * np.sqrt(252)
    print(f"\n  Annualized Return:   {ann_return:.4f} ({ann_return*100:.2f}%)")
    print(f"  Annualized Volatility: {ann_vol:.4f} ({ann_vol*100:.2f}%)")

    print("\n" + "=" * 60)
    print("Demo complete.")
    print("=" * 60)
