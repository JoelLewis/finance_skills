---
name: forward-risk
description: "Project future risk: parametric VaR, Monte Carlo VaR, CVaR/Expected Shortfall, scenario analysis, stress testing, factor-based risk decomposition. Use when a user wants to estimate potential future losses or stress-test a portfolio."
allowed-tools: Bash(python *)
---

# Forward Risk Estimation

## Purpose

Forward-looking risk estimation that projects potential future losses under various assumptions. This skill answers the fundamental question: **"How much could we lose?"**

Unlike historical risk (which measures what happened), forward risk uses models, simulations, and scenarios to estimate what might happen. Every output is an estimate conditional on assumptions that must be documented and understood. Forward risk is essential for portfolio construction, regulatory compliance (Basel III, Solvency II), risk budgeting, and capital allocation.

## Direction

**Prospective.** All outputs are forward-looking estimates. They depend critically on the assumptions made about return distributions, correlations, market regimes, and holding periods. These assumptions must always be stated explicitly alongside the results.

## Core Concepts

### 1. Parametric VaR (Variance-Covariance Method)

Assumes returns follow a known distribution (typically normal) and computes VaR analytically:

**Single asset:**
```
VaR_alpha = -(mu + z_alpha * sigma)
```

Where:
- `mu` = expected return over the holding period
- `z_alpha` = z-score for the confidence level (e.g., -1.645 for 95%, -2.326 for 99%)
- `sigma` = standard deviation of returns over the holding period

**Portfolio:**
```
VaR_portfolio = z_alpha * sqrt(w' * Sigma * w)
```

Where:
- `w` = vector of portfolio weights
- `Sigma` = covariance matrix of asset returns

**Holding period scaling (square root of time):**
```
VaR_T = VaR_1 * sqrt(T)
```

This assumes returns are i.i.d. -- a strong assumption that breaks down for longer horizons.

**Properties:**
- Fast to compute (closed-form solution)
- Easily decomposed into component and marginal VaR
- Requires only means, variances, and covariances
- Fails badly for non-normal distributions (fat tails, skewness)
- Underestimates tail risk for most financial return series

### 2. Monte Carlo VaR

Simulates a large number of return paths from an assumed distribution and computes VaR from the simulated distribution:

```
1. Estimate parameters (mu, sigma, or full distribution)
2. Generate N simulated returns from the distribution
3. For portfolios: simulate correlated returns using Cholesky decomposition
4. Compute portfolio return for each simulation
5. VaR = -Percentile(simulated_returns, 1 - confidence)
```

**Properties:**
- Can accommodate any distribution (normal, Student-t, skewed, etc.)
- Can model non-linear positions (options, structured products)
- Computationally expensive (requires thousands of simulations for stable estimates)
- Quality depends entirely on the assumed distribution -- garbage in, garbage out
- Confidence intervals around the VaR estimate can be computed from simulation uncertainty

### 3. CVaR / Expected Shortfall (ES)

The expected loss given that the loss exceeds VaR. Also called Conditional VaR or Expected Tail Loss:

```
CVaR_alpha = E[Loss | Loss > VaR_alpha]
```

For a continuous distribution:
```
CVaR_alpha = (1/alpha) * integral from -inf to VaR_alpha of x * f(x) dx
```

For the normal distribution, CVaR has a closed-form solution:
```
CVaR_alpha = mu + sigma * phi(z_alpha) / alpha
```

Where `phi` is the standard normal PDF.

**Properties:**
- A coherent risk measure (satisfies subadditivity, unlike VaR)
- Always greater than or equal to VaR
- Tells you the expected severity of losses in the worst alpha% of scenarios
- Required by Basel III for market risk capital (replaced VaR in the Fundamental Review of the Trading Book)
- More sensitive to tail assumptions than VaR

### 4. Scenario Analysis

Apply specific, predefined market shocks and compute the portfolio impact:

```
Portfolio_impact = sum(weight_i * beta_ij * shock_j)
```

Where:
- `weight_i` = portfolio weight of asset i
- `beta_ij` = sensitivity of asset i to factor j
- `shock_j` = assumed change in factor j (e.g., rates +200bps, equities -30%, oil +50%)

**Types of scenarios:**
- **Regulatory scenarios**: prescribed by regulators (e.g., CCAR stress tests)
- **Historical scenarios**: replay of specific historical episodes (2008 GFC, 2020 COVID crash, 1997 Asian crisis)
- **Hypothetical scenarios**: custom-designed to test specific vulnerabilities (e.g., simultaneous rate rise and credit spread widening)

**Properties:**
- Transparent and easy to communicate to stakeholders
- Does not require distributional assumptions
- Limited by imagination -- only tests the specific scenarios designed
- Cannot assign probabilities to outcomes (unlike VaR)

### 5. Stress Testing

More comprehensive than simple scenario analysis. Combines multiple correlated shocks applied to the full portfolio:

**Historical stress test (replay):**
```
1. Select a historical crisis period (e.g., Sep 2008 - Mar 2009)
2. Extract actual factor returns during that period
3. Apply those returns to the current portfolio
4. Compute portfolio P&L
```

**Hypothetical stress test:**
```
1. Define a custom shock vector across all relevant risk factors
2. Propagate shocks through the portfolio using factor sensitivities
3. Include second-order effects (correlation changes, liquidity impact)
4. Compute total portfolio impact
```

**Properties:**
- Captures correlated, multi-factor moves that VaR models may miss
- Required by regulators for large financial institutions
- Results are scenario-specific, not probabilistic
- Should include both P&L impact and liquidity impact

### 6. Factor-Based Risk Decomposition

Decompose portfolio variance into systematic (factor) risk and idiosyncratic risk:

```
R_p = sum(beta_i * F_i) + epsilon

Var(R_p) = B' * Sigma_F * B + Sigma_epsilon
```

Where:
- `B` = vector of portfolio factor exposures (weighted sum of asset betas)
- `Sigma_F` = factor covariance matrix
- `Sigma_epsilon` = diagonal matrix of idiosyncratic variances

**Common factor models:**
- **Fama-French**: Market, Size (SMB), Value (HML), Profitability (RMW), Investment (CMA)
- **Barra/MSCI**: Industry factors + style factors (momentum, volatility, size, etc.)
- **Macroeconomic**: GDP growth, inflation, interest rates, credit spreads

This decomposition reveals:
- What percentage of portfolio risk comes from market exposure vs stock-specific risk
- Which factors contribute most to total risk
- Where the portfolio is concentrated in factor space

### 7. Regime-Switching (Brief Treatment)

Markets alternate between distinct regimes (e.g., low-volatility/bull and high-volatility/bear). A Hidden Markov Model (HMM) approach:

```
State S_t in {1, 2, ..., K} with transition probabilities P(S_t | S_{t-1})
Returns: r_t | S_t ~ N(mu_{S_t}, sigma_{S_t}^2)
```

**Key insight:** Risk estimates can differ dramatically depending on the current regime. A VaR computed using the full sample may underestimate risk if the market has just shifted into a high-volatility regime.

## Key Assumptions to Document

Every forward risk estimate should explicitly state:

| Assumption | What It Means | Risk If Violated |
|---|---|---|
| Distribution (normal, t, etc.) | Shape of return tails | VaR underestimation if tails are fatter |
| Stationarity | Parameters don't change over time | Regime shifts invalidate estimates |
| Correlation stability | Correlation matrix is constant | Diversification benefits evaporate in crisis |
| Holding period | Time horizon for the risk estimate | Longer horizons amplify model errors |
| Liquidity | Positions can be liquidated at model prices | Actual losses may exceed model losses |
| Independence | Returns are serially uncorrelated | Momentum/mean-reversion violates this |

## When to Use / When Not to Use

| Scenario | Recommended Method |
|---|---|
| Quick daily risk limit monitoring | Parametric VaR |
| Regulatory capital calculation (Basel III) | CVaR / Expected Shortfall |
| Portfolio with options/non-linear payoffs | Monte Carlo VaR |
| Board-level risk communication | Scenario analysis + stress testing |
| Understanding risk factor exposures | Factor-based decomposition |
| Short-term trading risk | VaR with recent volatility |
| Long-term strategic planning | Scenario analysis with multiple regimes |

**Common pitfalls:**
- Treating VaR as a worst case (it is a threshold, not a bound)
- Using normal distribution VaR for fat-tailed return series
- Assuming correlations remain stable during stress events
- Scaling VaR beyond a few days using the square-root-of-time rule
- Ignoring liquidity risk (model says you can sell, but the market may disagree)

## Cross-References

- **Dependencies**: statistics-fundamentals (distributional theory), return-calculations (return series construction)
- **Feeds into**: asset-allocation (risk budgeting), diversification (correlation-based), liquidity-management (stress liquidity)
- **Related retrospective skill**: historical-risk (measures what happened; forward-risk estimates what could happen)
- **Related**: volatility-modeling (provides volatility forecasts used as inputs to VaR)

## Reference Implementation

See `scripts/forward_risk.py` for a complete `RiskForecaster` class implementing parametric VaR, parametric CVaR, Monte Carlo VaR and CVaR, scenario analysis, historical stress testing, and portfolio VaR. The implementation uses numpy and scipy.stats.
