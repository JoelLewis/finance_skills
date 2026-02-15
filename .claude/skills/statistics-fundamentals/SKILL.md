---
name: statistics-fundamentals
description: "Statistical methods for financial data: distributions, covariance matrices, regression, bootstrapping, shrinkage estimators. Use when a user needs to analyze return distributions, estimate correlations, or test hypotheses about financial data."
allowed-tools: Bash(python *)
---

# Statistics Fundamentals

## Purpose

This skill provides the statistical toolkit for financial data analysis. It answers the question: **"What are the statistical properties of this data?"**

Financial decision-making relies on estimating parameters (expected returns, volatilities, correlations) from observed data. This skill covers the methods for doing so correctly, including the pitfalls unique to financial data such as fat tails, non-stationarity, and estimation error in high-dimensional covariance matrices.

## Direction

**Primarily retrospective** -- estimating statistical properties from observed historical data. However, the outputs of this skill (estimated means, covariances, distribution parameters) feed directly into prospective models for risk forecasting, portfolio optimization, and scenario analysis.

## Core Concepts

### 1. Distributions in Finance

**Normal (Gaussian) distribution:**
- The workhorse assumption. Fully described by mean and variance.
- Central Limit Theorem justifies its use for aggregated returns over longer horizons.

**Log-normal distribution:**
- If log returns are normal, prices are log-normal: `ln(P_t/P_0) ~ N(mu*t, sigma^2*t)`
- Ensures prices remain non-negative.
- Foundation of the Black-Scholes model.

**Student-t distribution:**
- Heavier tails than normal, controlled by degrees of freedom parameter (nu).
- Better fits empirical return distributions, especially at daily frequency.
- As nu approaches infinity, converges to the normal distribution.

**Why financial returns are not normal:**
- **Excess kurtosis** (fat tails): extreme events occur far more frequently than a normal distribution predicts. A "6-sigma" equity market move that should occur once in 4 million years happens roughly once per decade.
- **Negative skewness**: large negative returns are more common than large positive returns for most equity markets.
- **Volatility clustering**: periods of high and low volatility tend to persist (captured by GARCH models).
- **Time-varying parameters**: mean, variance, and correlations are not constant.

### 2. Moments of a Distribution

**Mean (first moment):**
```
mu = E[X] = (1/n) * sum(x_i)
```

**Variance (second central moment):**
```
sigma^2 = E[(X - mu)^2] = (1/n) * sum((x_i - mu)^2)
```
Sample variance uses `n-1` (Bessel's correction) for unbiased estimation.

**Skewness (third standardized moment):**
```
S = E[(X - mu)^3] / sigma^3
```
- S = 0: symmetric distribution
- S < 0: left tail is longer/fatter (negative skew, common in equities)
- S > 0: right tail is longer/fatter (positive skew)

**Kurtosis (fourth standardized moment, excess):**
```
K = E[(X - mu)^4] / sigma^4 - 3
```
- K = 0: normal distribution (mesokurtic)
- K > 0: heavier tails than normal (leptokurtic, typical for financial returns)
- K < 0: lighter tails than normal (platykurtic, rare in finance)

### 3. Covariance and Correlation

**Covariance:**
```
cov(X, Y) = E[(X - mu_X)(Y - mu_Y)]
```

**Correlation (Pearson):**
```
rho(X, Y) = cov(X, Y) / (sigma_X * sigma_Y)
```
- Bounded between -1 and +1.
- Measures linear dependence only. Two assets can have zero correlation but strong nonlinear dependence.

### 4. Sample vs Population Estimates

When estimating from a sample of size `n`:
- **Population mean**: divide by `n`
- **Sample variance**: divide by `n-1` (degrees of freedom correction / Bessel's correction)
- **Sample covariance**: divide by `n-1`

The distinction matters most for small samples. In finance, even "large" samples (e.g., 60 monthly returns) are small enough that the correction is material.

### 5. Covariance Matrix Estimation

For a portfolio of `p` assets observed over `n` periods, the sample covariance matrix is:

```
S = (1/(n-1)) * (X - X_bar)^T * (X - X_bar)
```

**Pitfalls of sample covariance:**
- When `p > n` (more assets than observations), the matrix is singular and non-invertible -- mean-variance optimization fails.
- Even when `p < n`, estimation error is large. Extreme eigenvalues of the sample covariance are biased (largest are too large, smallest are too small).
- Portfolio optimization amplifies estimation error: it maximizes the Sharpe ratio of the estimated (noisy) model, not the true Sharpe ratio.

**Ledoit-Wolf shrinkage:**
Combines the sample covariance with a structured target (e.g., scaled identity, single-factor model) using an optimal shrinkage intensity:

```
Sigma_shrunk = delta * Target + (1 - delta) * S_sample
```

Where `delta` is chosen to minimize expected loss. Benefits:
- Always invertible (even when `p > n`)
- Reduces extreme eigenvalue bias
- Empirically produces better out-of-sample portfolio performance

### 6. Regression

**Ordinary Least Squares (OLS):**
```
y = alpha + beta * x + epsilon
beta = (X^T X)^(-1) X^T y
```

In finance, the most common application is the market model / CAPM regression:
```
R_asset - R_f = alpha + beta * (R_market - R_f) + epsilon
```

- **alpha**: excess return not explained by the market (Jensen's alpha)
- **beta**: sensitivity to the market factor
- **R-squared**: proportion of variance explained by the model (0 to 1)
- **t-statistics**: test whether alpha and beta are significantly different from zero

**Rolling regression:**
Applies OLS over a moving window to capture time-varying relationships (e.g., rolling 60-month beta). Reveals regime changes, structural breaks, and evolving factor exposures.

### 7. Bootstrapping

A resampling technique for constructing confidence intervals without parametric assumptions:

1. Draw `n` observations with replacement from the original data
2. Compute the statistic of interest on the resampled data
3. Repeat steps 1-2 many times (e.g., 10,000)
4. Use the empirical distribution of the statistic for inference

**Block bootstrap for time series:**
- Standard bootstrap destroys autocorrelation structure
- Block bootstrap resamples contiguous blocks of observations to preserve serial dependence
- Block size selection is a bias-variance tradeoff

### 8. Hypothesis Testing

**Testing if mean return is significantly different from zero:**
```
t = (r_bar - 0) / (s / sqrt(n))
```
Compare to the t-distribution with `n-1` degrees of freedom.

**Testing significance of regression coefficients (alpha, beta):**
- The t-statistic for each coefficient tests whether it differs from zero
- Low p-value (< 0.05) suggests statistical significance
- In finance, economic significance and statistical significance are different -- a statistically significant alpha of 0.01% per month may not be economically meaningful after transaction costs

**Jarque-Bera test for normality:**
```
JB = (n/6) * [S^2 + (1/4)(K)^2]
```
Where S is skewness and K is excess kurtosis. Under the null of normality, JB follows a chi-squared distribution with 2 degrees of freedom. Rejection indicates non-normality.

### 9. Copulas (Brief Treatment)

Correlation captures only linear, symmetric dependence. In practice:
- Assets may exhibit stronger co-movement in crashes than in rallies (tail dependence)
- Correlation can be misleading during market stress

**Copulas** separate the marginal distributions from the dependence structure:
- **Gaussian copula**: no tail dependence (underestimates joint crash risk)
- **Clayton copula**: lower tail dependence (better captures joint downside risk)
- **t-copula**: symmetric tail dependence

Copulas are relevant when modeling joint extreme events, credit portfolio risk, and multi-asset tail risk.

## When to Use / When Not to Use

| Scenario | Recommended Approach |
|---|---|
| Estimating portfolio risk | Covariance matrix (preferably shrunk) |
| Testing if a fund has alpha | OLS regression + t-test on alpha |
| Checking if returns are normal | Jarque-Bera test, Q-Q plots |
| Confidence interval for mean return | Bootstrap |
| Input for mean-variance optimization | Shrunk covariance matrix |
| Time-varying beta estimation | Rolling regression |
| Joint tail risk modeling | Copulas |

**Common pitfalls:**
- Do NOT assume stationarity blindly. Financial parameters (mean, variance, correlation) change over time. Test for it and consider rolling windows.
- Do NOT use raw sample covariance for portfolio optimization when the number of assets is large relative to the sample size. Use shrinkage.
- Do NOT confuse statistical significance with economic significance. With enough data, tiny effects become "significant."
- Do NOT ignore the multiple testing problem. Testing many strategies/factors inflates false positives.
- Be cautious with correlation during crises -- correlations tend to spike toward 1 during market stress, exactly when diversification is needed most.

## Cross-References

- **Feeds into**: historical-risk, forward-risk, diversification, asset-allocation, volatility-modeling, performance-metrics, performance-attribution
- **Dependencies**: None (Layer 0 foundational skill)

## Reference Implementation

See `scripts/statistics_fundamentals.py` for functions covering descriptive statistics, covariance/correlation matrix estimation, Ledoit-Wolf shrinkage, OLS and rolling regression, bootstrapping, and the Jarque-Bera normality test.
