"""
Statistics Fundamentals - Layer 0 (Mathematical Foundations)

A comprehensive reference implementation of statistical methods for financial
data analysis, including descriptive statistics, covariance estimation,
regression, bootstrapping, and hypothesis testing.

Usage:
    python statistics_fundamentals.py

Dependencies:
    numpy, scipy
"""

from typing import Optional

import numpy as np
from scipy import stats as sp_stats


# ---------------------------------------------------------------------------
# Descriptive Statistics
# ---------------------------------------------------------------------------

def descriptive_stats(returns: np.ndarray) -> dict:
    """Compute descriptive statistics for a return series.

    Calculates mean, standard deviation, skewness, excess kurtosis,
    minimum, maximum, and median.

    Args:
        returns: 1-D array of return observations.

    Returns:
        Dictionary with keys: mean, std, skew, kurtosis (excess),
        min, max, median.
    """
    returns = np.asarray(returns, dtype=float)
    n = len(returns)
    mean = float(np.mean(returns))
    std = float(np.std(returns, ddof=1))

    # Skewness: E[(X-mu)^3] / sigma^3, adjusted for sample bias
    if n >= 3 and std > 0:
        skew = float(sp_stats.skew(returns, bias=False))
    else:
        skew = 0.0

    # Excess kurtosis: E[(X-mu)^4] / sigma^4 - 3, adjusted for sample bias
    if n >= 4 and std > 0:
        kurtosis = float(sp_stats.kurtosis(returns, bias=False))
    else:
        kurtosis = 0.0

    return {
        "mean": mean,
        "std": std,
        "skew": skew,
        "kurtosis": kurtosis,
        "min": float(np.min(returns)),
        "max": float(np.max(returns)),
        "median": float(np.median(returns)),
    }


# ---------------------------------------------------------------------------
# Covariance and Correlation
# ---------------------------------------------------------------------------

def covariance_matrix(returns: np.ndarray) -> np.ndarray:
    """Compute the sample covariance matrix.

    Uses n-1 degrees of freedom (Bessel's correction).

    Args:
        returns: 2-D array of shape (n_observations, n_assets).

    Returns:
        Covariance matrix of shape (n_assets, n_assets).
    """
    returns = np.asarray(returns, dtype=float)
    return np.cov(returns, rowvar=False)


def correlation_matrix(returns: np.ndarray) -> np.ndarray:
    """Compute the sample correlation matrix.

    Args:
        returns: 2-D array of shape (n_observations, n_assets).

    Returns:
        Correlation matrix of shape (n_assets, n_assets).
    """
    returns = np.asarray(returns, dtype=float)
    return np.corrcoef(returns, rowvar=False)


def shrunk_covariance(
    returns: np.ndarray,
    shrinkage_target: str = "identity",
) -> np.ndarray:
    """Compute a shrinkage-estimated covariance matrix (Ledoit-Wolf style).

    Sigma_shrunk = delta * Target + (1 - delta) * S_sample

    The shrinkage intensity delta is estimated analytically following the
    Ledoit-Wolf (2004) approach (simplified implementation).

    Args:
        returns: 2-D array of shape (n_observations, n_assets).
        shrinkage_target: Type of structured target matrix.
            - "identity": scaled identity matrix (mu * I)
            - "diagonal": diagonal of the sample covariance

    Returns:
        Shrunk covariance matrix of shape (n_assets, n_assets).
    """
    returns = np.asarray(returns, dtype=float)
    n, p = returns.shape

    # Sample covariance
    sample_cov = np.cov(returns, rowvar=False)

    # Construct target
    if shrinkage_target == "diagonal":
        target = np.diag(np.diag(sample_cov))
    else:
        # Scaled identity: average variance on the diagonal
        mu = np.trace(sample_cov) / p
        target = mu * np.eye(p)

    # Estimate optimal shrinkage intensity (simplified Ledoit-Wolf)
    # Compute the squared Frobenius norm of (S - Target)
    x = returns - returns.mean(axis=0)

    # Sum of squared sample covariances (off-diagonal estimation error)
    # Approximation of the optimal shrinkage parameter
    sum_sq = 0.0
    for i in range(n):
        outer = np.outer(x[i], x[i])
        diff = outer - sample_cov
        sum_sq += np.sum(diff ** 2)
    phi_hat = sum_sq / (n ** 2)

    gamma_hat = np.sum((sample_cov - target) ** 2)

    if gamma_hat == 0:
        delta = 1.0
    else:
        delta = max(0.0, min(1.0, phi_hat / gamma_hat))

    return delta * target + (1.0 - delta) * sample_cov


# ---------------------------------------------------------------------------
# Regression
# ---------------------------------------------------------------------------

def ols_regression(y: np.ndarray, x: np.ndarray) -> dict:
    """Perform OLS linear regression: y = alpha + beta * x + epsilon.

    Args:
        y: 1-D array of dependent variable observations.
        x: 1-D array of independent variable observations.

    Returns:
        Dictionary with keys:
            - alpha: intercept
            - beta: slope coefficient
            - r_squared: coefficient of determination
            - t_stats: dict with t-statistics for alpha and beta
            - p_values: dict with p-values for alpha and beta
            - residuals: 1-D array of residuals
    """
    y = np.asarray(y, dtype=float)
    x = np.asarray(x, dtype=float)
    n = len(y)

    # Design matrix with intercept
    X = np.column_stack([np.ones(n), x])

    # beta_hat = (X'X)^-1 X'y
    XtX_inv = np.linalg.inv(X.T @ X)
    beta_hat = XtX_inv @ X.T @ y

    alpha = float(beta_hat[0])
    beta = float(beta_hat[1])

    # Residuals and R-squared
    y_hat = X @ beta_hat
    residuals = y - y_hat
    ss_res = float(np.sum(residuals ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    r_squared = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0

    # Standard errors and t-statistics
    dof = n - 2  # degrees of freedom
    if dof > 0:
        mse = ss_res / dof
        se = np.sqrt(np.diag(XtX_inv) * mse)
        t_alpha = alpha / se[0] if se[0] > 0 else 0.0
        t_beta = beta / se[1] if se[1] > 0 else 0.0
        p_alpha = float(2.0 * (1.0 - sp_stats.t.cdf(abs(t_alpha), dof)))
        p_beta = float(2.0 * (1.0 - sp_stats.t.cdf(abs(t_beta), dof)))
    else:
        t_alpha = 0.0
        t_beta = 0.0
        p_alpha = 1.0
        p_beta = 1.0

    return {
        "alpha": alpha,
        "beta": beta,
        "r_squared": r_squared,
        "t_stats": {"alpha": float(t_alpha), "beta": float(t_beta)},
        "p_values": {"alpha": p_alpha, "beta": p_beta},
        "residuals": residuals,
    }


def rolling_regression(
    y: np.ndarray,
    x: np.ndarray,
    window: int,
) -> dict:
    """Perform rolling OLS regression over a moving window.

    Applies the ols_regression function over a sliding window of
    observations to capture time-varying relationships.

    Args:
        y: 1-D array of dependent variable observations.
        x: 1-D array of independent variable observations.
        window: Number of observations in each rolling window.

    Returns:
        Dictionary with keys:
            - alpha: list of rolling intercepts
            - beta: list of rolling slope coefficients
            - r_squared: list of rolling R-squared values

        Each list has length (n - window + 1), aligned to the end
        of each window.
    """
    y = np.asarray(y, dtype=float)
    x = np.asarray(x, dtype=float)
    n = len(y)

    alphas = []
    betas = []
    r_squareds = []

    for i in range(n - window + 1):
        result = ols_regression(y[i : i + window], x[i : i + window])
        alphas.append(result["alpha"])
        betas.append(result["beta"])
        r_squareds.append(result["r_squared"])

    return {
        "alpha": alphas,
        "beta": betas,
        "r_squared": r_squareds,
    }


# ---------------------------------------------------------------------------
# Bootstrapping
# ---------------------------------------------------------------------------

def bootstrap_mean(
    returns: np.ndarray,
    n_samples: int = 10000,
    confidence: float = 0.95,
) -> dict:
    """Estimate the mean return with bootstrapped confidence interval.

    Resamples the return series with replacement to construct an empirical
    distribution of the sample mean and derive a confidence interval.

    Args:
        returns: 1-D array of return observations.
        n_samples: Number of bootstrap resamples. Defaults to 10,000.
        confidence: Confidence level (e.g., 0.95 for 95%). Defaults to 0.95.

    Returns:
        Dictionary with keys:
            - mean: point estimate (sample mean)
            - ci_lower: lower bound of the confidence interval
            - ci_upper: upper bound of the confidence interval
            - std_error: bootstrap standard error of the mean
    """
    returns = np.asarray(returns, dtype=float)
    n = len(returns)

    # Generate all bootstrap samples at once for efficiency
    rng = np.random.default_rng(seed=42)
    indices = rng.integers(0, n, size=(n_samples, n))
    boot_means = np.mean(returns[indices], axis=1)

    alpha = (1.0 - confidence) / 2.0
    ci_lower = float(np.percentile(boot_means, 100 * alpha))
    ci_upper = float(np.percentile(boot_means, 100 * (1.0 - alpha)))

    return {
        "mean": float(np.mean(returns)),
        "ci_lower": ci_lower,
        "ci_upper": ci_upper,
        "std_error": float(np.std(boot_means, ddof=1)),
    }


# ---------------------------------------------------------------------------
# Hypothesis Testing
# ---------------------------------------------------------------------------

def jarque_bera_test(returns: np.ndarray) -> dict:
    """Perform the Jarque-Bera test for normality.

    JB = (n/6) * [S^2 + (1/4) * K^2]

    where S is sample skewness and K is excess kurtosis. Under the null
    hypothesis of normality, JB follows a chi-squared distribution with
    2 degrees of freedom.

    Args:
        returns: 1-D array of return observations.

    Returns:
        Dictionary with keys:
            - statistic: the Jarque-Bera test statistic
            - p_value: p-value (reject normality if small, e.g. < 0.05)
            - skewness: sample skewness
            - kurtosis: sample excess kurtosis
    """
    returns = np.asarray(returns, dtype=float)
    n = len(returns)

    skew = float(sp_stats.skew(returns, bias=False))
    kurtosis = float(sp_stats.kurtosis(returns, bias=False))

    # Jarque-Bera statistic
    jb_stat = (n / 6.0) * (skew ** 2 + (kurtosis ** 2) / 4.0)

    # p-value from chi-squared distribution with 2 degrees of freedom
    p_value = float(1.0 - sp_stats.chi2.cdf(jb_stat, df=2))

    return {
        "statistic": jb_stat,
        "p_value": p_value,
        "skewness": skew,
        "kurtosis": kurtosis,
    }


# ---------------------------------------------------------------------------
# Demonstration
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 60)
    print("Statistics Fundamentals - Reference Implementation Demo")
    print("=" * 60)

    # Set seed for reproducibility
    rng = np.random.default_rng(seed=42)

    # Generate synthetic return data for 3 assets, 252 trading days
    n_obs = 252
    n_assets = 3
    asset_names = ["Equity", "Bond", "Commodity"]

    # Correlated returns via Cholesky decomposition
    true_means = np.array([0.0004, 0.0001, 0.0003])  # daily means
    true_cov = np.array([
        [0.0004, 0.0001, 0.00015],
        [0.0001, 0.00005, 0.00002],
        [0.00015, 0.00002, 0.0003],
    ])
    L = np.linalg.cholesky(true_cov)
    z = rng.standard_normal((n_obs, n_assets))
    returns_2d = z @ L.T + true_means

    equity_returns = returns_2d[:, 0]
    market_returns = equity_returns + rng.normal(0, 0.005, n_obs)

    # 1. Descriptive Statistics
    print("\n1. Descriptive Statistics (Equity)")
    desc = descriptive_stats(equity_returns)
    for key, val in desc.items():
        print(f"   {key:>10}: {val:>12.6f}")

    # 2. Covariance Matrix
    print(f"\n2. Sample Covariance Matrix ({n_assets} assets):")
    cov_mat = covariance_matrix(returns_2d)
    header = "           " + "".join(f"{name:>12}" for name in asset_names)
    print(header)
    for i, name in enumerate(asset_names):
        row = f"   {name:>8}" + "".join(f"{cov_mat[i, j]:>12.7f}" for j in range(n_assets))
        print(row)

    # 3. Correlation Matrix
    print(f"\n3. Sample Correlation Matrix:")
    corr_mat = correlation_matrix(returns_2d)
    print(header)
    for i, name in enumerate(asset_names):
        row = f"   {name:>8}" + "".join(f"{corr_mat[i, j]:>12.4f}" for j in range(n_assets))
        print(row)

    # 4. Shrunk Covariance Matrix
    print(f"\n4. Shrunk Covariance Matrix (Ledoit-Wolf, identity target):")
    shrunk_cov = shrunk_covariance(returns_2d, shrinkage_target="identity")
    print(header)
    for i, name in enumerate(asset_names):
        row = f"   {name:>8}" + "".join(f"{shrunk_cov[i, j]:>12.7f}" for j in range(n_assets))
        print(row)

    # 5. OLS Regression (equity on market)
    print(f"\n5. OLS Regression: Equity = alpha + beta * Market + epsilon")
    reg = ols_regression(equity_returns, market_returns)
    print(f"   Alpha:     {reg['alpha']:.6f}  (t={reg['t_stats']['alpha']:.3f}, p={reg['p_values']['alpha']:.4f})")
    print(f"   Beta:      {reg['beta']:.6f}  (t={reg['t_stats']['beta']:.3f}, p={reg['p_values']['beta']:.4f})")
    print(f"   R-squared: {reg['r_squared']:.4f}")

    # 6. Rolling Regression
    print(f"\n6. Rolling Regression (60-day window):")
    rolling = rolling_regression(equity_returns, market_returns, window=60)
    print(f"   Number of windows: {len(rolling['beta'])}")
    print(f"   Beta range: [{min(rolling['beta']):.4f}, {max(rolling['beta']):.4f}]")
    print(f"   R-sq range: [{min(rolling['r_squared']):.4f}, {max(rolling['r_squared']):.4f}]")

    # 7. Bootstrap Mean
    print(f"\n7. Bootstrap Mean Estimate (Equity, 10k samples, 95% CI):")
    boot = bootstrap_mean(equity_returns, n_samples=10_000, confidence=0.95)
    print(f"   Mean:      {boot['mean']:.6f}")
    print(f"   95% CI:    [{boot['ci_lower']:.6f}, {boot['ci_upper']:.6f}]")
    print(f"   Std Error: {boot['std_error']:.6f}")

    # 8. Jarque-Bera Test
    print(f"\n8. Jarque-Bera Test for Normality (Equity):")
    jb = jarque_bera_test(equity_returns)
    print(f"   JB Statistic: {jb['statistic']:.4f}")
    print(f"   p-value:      {jb['p_value']:.4f}")
    print(f"   Skewness:     {jb['skewness']:.4f}")
    print(f"   Kurtosis:     {jb['kurtosis']:.4f}")
    normality = "REJECT" if jb["p_value"] < 0.05 else "FAIL TO REJECT"
    print(f"   Conclusion:   {normality} normality at 5% significance level")

    # Also test with known fat-tailed data
    print(f"\n   Jarque-Bera on Student-t(3) synthetic data:")
    fat_tailed = rng.standard_t(df=3, size=1000)
    jb_fat = jarque_bera_test(fat_tailed)
    print(f"   JB Statistic: {jb_fat['statistic']:.4f}")
    print(f"   p-value:      {jb_fat['p_value']:.6f}")
    normality_fat = "REJECT" if jb_fat["p_value"] < 0.05 else "FAIL TO REJECT"
    print(f"   Conclusion:   {normality_fat} normality at 5% significance level")

    print("\n" + "=" * 60)
    print("All calculations completed successfully.")
    print("=" * 60)
