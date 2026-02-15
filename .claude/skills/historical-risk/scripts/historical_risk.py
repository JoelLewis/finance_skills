"""
Historical Risk Analyzer
=========================
Backward-looking risk measurement from observed return data.
Computes volatility estimators, drawdown analysis, historical VaR,
downside deviation, tracking error, and semi-variance.

Part of Layer 1a (Retrospective) in the finance skills framework.
"""

import numpy as np


class HistoricalRiskAnalyzer:
    """Compute realized risk metrics from historical return series.

    Parameters
    ----------
    returns : np.ndarray
        Array of periodic simple returns (e.g., daily returns as decimals:
        0.01 = 1% gain). Must be a 1-D array.
    periods_per_year : int, optional
        Number of periods in a year for annualization. Default is 252
        (trading days). Use 52 for weekly, 12 for monthly.
    """

    def __init__(self, returns: np.ndarray, periods_per_year: int = 252):
        self.returns = np.asarray(returns, dtype=np.float64)
        self.periods_per_year = periods_per_year

    def annualized_volatility(self) -> float:
        """Compute annualized close-to-close volatility.

        Returns
        -------
        float
            Annualized standard deviation of returns.
            sigma = std(returns) * sqrt(periods_per_year)
        """
        return float(np.std(self.returns, ddof=1) * np.sqrt(self.periods_per_year))

    def parkinson_volatility(self, highs: np.ndarray, lows: np.ndarray) -> float:
        """Compute Parkinson volatility estimator from high/low prices.

        Uses intraday price range for a more efficient volatility estimate
        (approximately 5x more efficient than close-to-close).

        Parameters
        ----------
        highs : np.ndarray
            Array of high prices for each period.
        lows : np.ndarray
            Array of low prices for each period.

        Returns
        -------
        float
            Annualized Parkinson volatility.
            sigma_P = sqrt(1/(4*n*ln2) * sum(ln(H/L)^2)) * sqrt(periods_per_year)
        """
        highs = np.asarray(highs, dtype=np.float64)
        lows = np.asarray(lows, dtype=np.float64)
        n = len(highs)
        log_hl = np.log(highs / lows)
        sigma_p = np.sqrt(np.sum(log_hl ** 2) / (4.0 * n * np.log(2.0)))
        return float(sigma_p * np.sqrt(self.periods_per_year))

    def drawdown_series(self) -> np.ndarray:
        """Compute the running drawdown series from cumulative returns.

        Returns
        -------
        np.ndarray
            Array of drawdowns at each point in time, expressed as negative
            fractions (e.g., -0.10 means 10% below the peak).
        """
        cumulative = np.cumprod(1.0 + self.returns)
        running_max = np.maximum.accumulate(cumulative)
        drawdowns = (cumulative - running_max) / running_max
        return drawdowns

    def max_drawdown(self) -> dict:
        """Compute maximum drawdown with timing information.

        Returns
        -------
        dict
            - 'depth': float, magnitude of maximum drawdown (negative number)
            - 'start_idx': int, index of the peak before the drawdown
            - 'trough_idx': int, index of the trough (maximum drawdown point)
            - 'recovery_idx': int or None, index where cumulative returns
              first exceed the prior peak. None if not yet recovered.
        """
        cumulative = np.cumprod(1.0 + self.returns)
        running_max = np.maximum.accumulate(cumulative)
        drawdowns = (cumulative - running_max) / running_max

        trough_idx = int(np.argmin(drawdowns))
        depth = float(drawdowns[trough_idx])

        # Find the peak that precedes the trough
        start_idx = int(np.argmax(cumulative[:trough_idx + 1]))

        # Find recovery: first index after trough where cumulative >= prior peak
        peak_value = cumulative[start_idx]
        recovery_idx = None
        for i in range(trough_idx + 1, len(cumulative)):
            if cumulative[i] >= peak_value:
                recovery_idx = int(i)
                break

        return {
            "depth": depth,
            "start_idx": start_idx,
            "trough_idx": trough_idx,
            "recovery_idx": recovery_idx,
        }

    def historical_var(self, confidence: float = 0.95) -> float:
        """Compute historical Value at Risk (non-parametric).

        VaR is the loss threshold at the given confidence level. Reported
        as a positive number representing a loss.

        Parameters
        ----------
        confidence : float, optional
            Confidence level, default 0.95 (95% VaR).

        Returns
        -------
        float
            Historical VaR as a positive loss magnitude.
            E.g., 0.023 means the portfolio lost more than 2.3% only
            (1 - confidence)% of the time.
        """
        alpha = 1.0 - confidence
        var_value = -float(np.percentile(self.returns, alpha * 100.0))
        return var_value

    def downside_deviation(self, threshold: float = 0.0) -> float:
        """Compute annualized downside deviation.

        Only returns below the threshold contribute to the calculation.

        Parameters
        ----------
        threshold : float, optional
            Minimum acceptable return. Default is 0.0. Common alternatives
            include the risk-free rate per period.

        Returns
        -------
        float
            Annualized downside deviation.
            DD = sqrt(mean(min(r - threshold, 0)^2)) * sqrt(periods_per_year)
        """
        downside = np.minimum(self.returns - threshold, 0.0)
        dd = np.sqrt(np.mean(downside ** 2))
        return float(dd * np.sqrt(self.periods_per_year))

    def tracking_error(self, benchmark_returns: np.ndarray) -> float:
        """Compute annualized tracking error relative to a benchmark.

        Parameters
        ----------
        benchmark_returns : np.ndarray
            Array of benchmark periodic returns, same length as self.returns.

        Returns
        -------
        float
            Annualized tracking error.
            TE = std(r_portfolio - r_benchmark) * sqrt(periods_per_year)
        """
        benchmark_returns = np.asarray(benchmark_returns, dtype=np.float64)
        active_returns = self.returns - benchmark_returns
        return float(np.std(active_returns, ddof=1) * np.sqrt(self.periods_per_year))

    def semi_variance(self) -> float:
        """Compute semi-variance (variance of below-mean returns).

        Returns
        -------
        float
            Semi-variance. For a symmetric distribution, this equals
            approximately half the full variance.
            SemiVar = (1/n) * sum(min(r_i - mean(r), 0)^2)
        """
        mean_return = np.mean(self.returns)
        below_mean = np.minimum(self.returns - mean_return, 0.0)
        return float(np.mean(below_mean ** 2))

    def rolling_volatility(self, window: int = 63) -> np.ndarray:
        """Compute rolling annualized volatility.

        Parameters
        ----------
        window : int, optional
            Rolling window size in periods. Default is 63 (approx. 1 quarter
            of trading days).

        Returns
        -------
        np.ndarray
            Array of annualized rolling volatility values. The first
            (window - 1) elements are NaN (insufficient data).
        """
        n = len(self.returns)
        result = np.full(n, np.nan)
        for i in range(window - 1, n):
            window_returns = self.returns[i - window + 1 : i + 1]
            result[i] = np.std(window_returns, ddof=1) * np.sqrt(self.periods_per_year)
        return result


if __name__ == "__main__":
    # ----------------------------------------------------------------
    # Demo: Historical risk analysis on synthetic data
    # ----------------------------------------------------------------
    np.random.seed(42)

    # Generate 2 years of daily returns (approx 504 trading days)
    n_days = 504
    daily_returns = np.random.normal(loc=0.0003, scale=0.012, size=n_days)

    # Inject a drawdown event (days 200-220)
    daily_returns[200:220] = np.random.normal(loc=-0.02, scale=0.025, size=20)

    analyzer = HistoricalRiskAnalyzer(daily_returns, periods_per_year=252)

    print("=" * 60)
    print("Historical Risk Analysis - Demo")
    print("=" * 60)

    # Annualized volatility
    vol = analyzer.annualized_volatility()
    print(f"\nAnnualized Volatility (close-to-close): {vol:.4f} ({vol*100:.2f}%)")

    # Parkinson volatility (synthetic high/low data)
    prices = 100.0 * np.cumprod(1.0 + daily_returns)
    highs = prices * (1.0 + np.abs(np.random.normal(0, 0.005, n_days)))
    lows = prices * (1.0 - np.abs(np.random.normal(0, 0.005, n_days)))
    park_vol = analyzer.parkinson_volatility(highs, lows)
    print(f"Parkinson Volatility:                   {park_vol:.4f} ({park_vol*100:.2f}%)")

    # Maximum drawdown
    dd = analyzer.max_drawdown()
    print(f"\nMaximum Drawdown:")
    print(f"  Depth:        {dd['depth']:.4f} ({dd['depth']*100:.2f}%)")
    print(f"  Peak index:   {dd['start_idx']}")
    print(f"  Trough index: {dd['trough_idx']}")
    print(f"  Recovery idx: {dd['recovery_idx']}")

    # Historical VaR
    var_95 = analyzer.historical_var(confidence=0.95)
    var_99 = analyzer.historical_var(confidence=0.99)
    print(f"\nHistorical VaR:")
    print(f"  95% VaR: {var_95:.4f} ({var_95*100:.2f}%)")
    print(f"  99% VaR: {var_99:.4f} ({var_99*100:.2f}%)")

    # Downside deviation
    dd_zero = analyzer.downside_deviation(threshold=0.0)
    print(f"\nDownside Deviation (threshold=0): {dd_zero:.4f} ({dd_zero*100:.2f}%)")

    # Semi-variance
    sv = analyzer.semi_variance()
    full_var = np.var(daily_returns, ddof=0)
    print(f"\nSemi-Variance:  {sv:.8f}")
    print(f"Full Variance:  {full_var:.8f}")
    print(f"Ratio (SV/Var): {sv/full_var:.4f}  (0.50 = symmetric)")

    # Tracking error (synthetic benchmark)
    benchmark_returns = np.random.normal(loc=0.0003, scale=0.010, size=n_days)
    te = analyzer.tracking_error(benchmark_returns)
    print(f"\nTracking Error vs Benchmark: {te:.4f} ({te*100:.2f}%)")

    # Rolling volatility
    rolling_vol = analyzer.rolling_volatility(window=63)
    valid_vol = rolling_vol[~np.isnan(rolling_vol)]
    print(f"\nRolling Volatility (63-day window):")
    print(f"  Mean:  {np.mean(valid_vol):.4f}")
    print(f"  Min:   {np.min(valid_vol):.4f}")
    print(f"  Max:   {np.max(valid_vol):.4f}")

    # Drawdown series summary
    dd_series = analyzer.drawdown_series()
    print(f"\nDrawdown Series Summary:")
    print(f"  Current drawdown: {dd_series[-1]:.4f} ({dd_series[-1]*100:.2f}%)")
    print(f"  Max drawdown:     {np.min(dd_series):.4f} ({np.min(dd_series)*100:.2f}%)")
    print(f"  Periods in drawdown: {np.sum(dd_series < 0)} / {len(dd_series)}")

    print("\n" + "=" * 60)
    print("Demo complete.")
    print("=" * 60)
