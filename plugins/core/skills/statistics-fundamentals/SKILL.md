---
name: statistics-fundamentals
description: "Apply statistical methods to financial data including descriptive statistics, covariance estimation, regression, hypothesis testing, and resampling. Use when the user asks about return distributions, correlation between assets, building a covariance matrix, running a CAPM regression, testing whether alpha is significant, checking if returns are normal, or estimating confidence intervals. Also trigger when users mention 'volatility', 'how correlated are these', 'fat tails', 'skewness', 'R-squared', 'beta of a fund', 'bootstrap a Sharpe ratio', 'shrinkage estimator', 'Ledoit-Wolf', or ask why their optimizer produces unstable weights."
---

# Statistics Fundamentals

## Core Concepts

### Conventions and Decision Rules

### Sample variance: use n-1
When estimating variance or standard deviation from a sample of returns, divide by `n - 1` (Bessel's correction), not `n`. Dividing by `n` systematically underestimates dispersion. Standard deviation of returns is "volatility"; annualize with `sigma_annual = sigma_period * sqrt(periods_per_year)` (e.g., `* sqrt(12)` for monthly, `* sqrt(252)` for daily).

### Normality testing: Jarque-Bera and its limits
`JB = (n/6) * (skew^2 + excess_kurtosis^2 / 4)`, distributed chi-squared with 2 df under the null of normality (5% critical value: 5.99).

**Low-power caveat:** with small samples (n below roughly 50), JB rarely rejects even for clearly non-normal data — failing to reject is weak evidence of normality, not confirmation. With large samples, financial return series almost always reject due to fat tails and (for equities) negative skewness. Treat the test as a screen, and pair it with a look at the actual skew/kurtosis magnitudes and extreme observations.

### Covariance estimation and Ledoit-Wolf shrinkage
The sample covariance matrix `Sigma_hat = (1/(n-1)) (X - X_bar)^T (X - X_bar)` becomes poorly conditioned or singular when the number of assets `p` approaches the number of observations `n`. Plugging it into a mean-variance optimizer then produces extreme, unstable weights that flip with small data changes.

Shrinkage blends the sample matrix toward a structured target:

$$\hat{\Sigma}_{shrunk} = \delta \cdot F + (1 - \delta) \cdot \hat{\Sigma}$$

where `F` is the target (e.g., scaled identity) and `delta` is the shrinkage intensity. Ledoit-Wolf (2004) derives the `delta` that minimizes expected squared Frobenius distance to the true covariance matrix, trading a little bias for a large variance reduction — yielding better-conditioned, invertible matrices and stable portfolio weights.

**Note:** the bundled script's `shrunk_covariance` implements a *simplified* shrinkage-intensity estimate, not the full Ledoit-Wolf estimator. For production work use `sklearn.covariance.LedoitWolf`.

### Regression diagnostics (CAPM and factor models)
For the single-factor CAPM regression `R_i - R_f = alpha + beta * (R_m - R_f) + epsilon`:
- `beta = rho * sigma_i / sigma_m` (market sensitivity); `alpha` is the risk-adjusted excess return.
- In a single-factor regression, `R^2 = rho^2`.
- Judge coefficients by t-statistics (`t = coefficient / SE`); with `n - 2` df, |t| above roughly 2 indicates 5% significance. A positive alpha point estimate with |t| < 2 is not evidence of skill.
- Adding regressors always raises R-squared; use adjusted R-squared, AIC/BIC, or cross-validation to guard against overfitting.

### Bootstrap procedure
Non-parametric resampling for the sampling distribution of a statistic when analytical standard errors are unavailable (Sharpe ratio, alpha), the distribution is non-normal, or samples are small:

1. From the original `n` observations, draw `B` resamples of size `n` **with replacement** (B = 1,000-10,000).
2. Compute the statistic on each resample.
3. Percentile method: the `(1 - alpha)` confidence interval is the `alpha/2` and `1 - alpha/2` percentiles of the bootstrap distribution; the bootstrap standard error is the std of the `B` statistics.

Caveat: the i.i.d. bootstrap ignores autocorrelation and volatility clustering; use block bootstrap for serially dependent return series.

### Standard Analysis Workflow

Given a return series, run this sequence:

1. **Descriptive stats** — mean, volatility (n-1), skewness, excess kurtosis; annualize for reporting.
2. **Distribution checks** — Jarque-Bera (mind the low-power caveat), inspect skew/kurtosis magnitudes and largest outliers; decide whether normal-based methods (parametric VaR, t-tests) are defensible.
3. **Covariance/correlation** (multi-asset) — sample covariance and correlation matrices; if `p` is large relative to `n`, apply shrinkage before any optimization.
4. **Regression diagnostics** — CAPM or factor regression; report alpha/beta with t-stats and R-squared; check residuals for structure.
5. **Bootstrap CIs** — for statistics without clean analytical standard errors (Sharpe, alpha, drawdown), bootstrap confidence intervals rather than reporting bare point estimates.

## Worked Examples

### Example 1: Descriptive Statistics and Normality Test
**Given:** 12 monthly returns (%): `[2.1, -0.5, 1.8, -3.2, 4.5, 0.3, -1.1, 2.7, -0.8, 3.4, 1.2, -0.6]`

```
Mean      = 9.8 / 12 = 0.8167% per month  (~9.8% annualized, simple x12)
s^2       = 52.977 / 11 = 4.816   ->   s = 2.195% per month
Ann. vol  = 2.195% * sqrt(12) = 7.60%
Skewness  = -0.045  (bias-corrected; near symmetric)
Ex. kurt  = -0.42   (bias-corrected; lighter tails than normal)

JB = (12/6) * ((-0.045)^2 + (-0.42)^2 / 4) = 0.09
```

JB = 0.09 < 5.99 (chi-squared 5% critical, df=2): **fail to reject** normality. With only 12 observations the test has very low power — this is not evidence that the returns are truly normal.

### Example 2: CAPM Regression from Summary Statistics
**Given:** 24 monthly observations. Fund excess returns: mean 0.8%, std 4.2%. Market excess returns: mean 0.6%, std 3.8%. Correlation 0.85.

```
beta  = rho * sigma_i / sigma_m = 0.85 * 4.2 / 3.8 = 0.939
alpha = 0.8% - 0.939 * 0.6% = 0.236% per month (~2.84% annualized)
R^2   = rho^2 = 0.7225

Residual std = 4.2% * sqrt(1 - 0.7225) = 2.213%
SE(alpha) = 2.213% / sqrt(24) = 0.452%   ->  t(alpha) = 0.236 / 0.452 = 0.52
SE(beta)  = 2.213% / (3.8% * sqrt(23)) = 0.121  ->  t(beta) = 0.939 / 0.121 = 7.74
```

With 22 df, the 5% two-tailed critical t is 2.074. Beta is highly significant (7.74 >> 2.074); alpha is **not** significant (0.52 < 2.074) — despite the positive point estimate, the sample cannot distinguish it from zero.

## Common Pitfalls
- Using population variance instead of sample variance: always use `n - 1` (Bessel's correction) when estimating from a sample.
- Assuming normality when financial returns have fat tails: equity returns typically show negative skewness and positive excess kurtosis; normal-based models (standard VaR) underestimate tail risk. Use Student-t or non-parametric methods.
- Ignoring non-stationarity: return distributions shift over time (regime changes, volatility clustering). Rolling-window estimation or GARCH may be more appropriate than full-sample statistics.
- Overfitting with too many regressors: R-squared always rises with added factors; use adjusted R-squared, information criteria, or cross-validation.
- Unstable covariance matrices with small samples: when `p` approaches or exceeds `n`, apply Ledoit-Wolf shrinkage or factor-based covariance models before optimizing.

## Running the Script
`scripts/statistics_fundamentals.py` provides a `StatisticsFundamentals` class with static methods `descriptive_stats`, `covariance_matrix`, `correlation_matrix`, `shrunk_covariance` (simplified Ledoit-Wolf — see note above), `ols_regression`, `rolling_regression`, `bootstrap_mean`, and `jarque_bera_test`.

- Run: `uv run scripts/statistics_fundamentals.py` (PEP 723 inline metadata resolves numpy and scipy), or `python3 scripts/statistics_fundamentals.py` with numpy/scipy installed.
- Bare invocation (or `--verify`) prints a demo on synthetic data **and** asserts the Example 1 worked-example values above (mean 0.8167, std 2.195, JB 0.09 on the 12-month series), exiting nonzero on any mismatch.
- `--help` lists the available methods and import usage.
- For programmatic use, import rather than run: `from statistics_fundamentals import StatisticsFundamentals`, then call e.g. `StatisticsFundamentals.descriptive_stats(...)`.

## Cross-References
- **return-calculations** (core plugin): Arithmetic and geometric mean returns, log returns for statistical modeling
- **time-value-of-money** (core plugin): Discount rate estimation via CAPM regression; NPV and IRR calculations use statistical inputs
- **factor-investing** (wealth-management plugin): Extends the single-factor CAPM/OLS regression to Fama-French multifactor models for alpha attribution and fund evaluation
- **financial-statements** (wealth-management plugin): applies descriptive statistics and trend analysis to financial ratios and peer comparisons