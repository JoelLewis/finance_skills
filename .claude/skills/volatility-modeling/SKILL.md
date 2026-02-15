---
name: volatility-modeling
description: Model and forecast volatility: EWMA, GARCH(1,1), implied volatility, volatility surfaces, term structure, realized vs implied.
allowed-tools: ["Bash", "Read", "Write", "Edit"]
---

# Volatility Modeling

## Purpose
Model and forecast volatility using time-series methods (EWMA, GARCH) and market-implied measures. This skill bridges retrospective (realized) and prospective (implied, forecasted) volatility, enabling better risk management and options analysis.

## Layer
1b — Forward-Looking Risk

## Direction
Prospective (with retrospective inputs)

## When to Use
- Forecasting future volatility for risk management
- Building EWMA or GARCH volatility models
- Extracting or interpreting implied volatility from options
- Constructing volatility surfaces (strike × maturity)
- Comparing realized vs implied volatility (variance risk premium)
- Understanding VIX and volatility indices

## Core Concepts

### EWMA (Exponentially Weighted Moving Average)
Assigns exponentially declining weights to past squared returns:

σ²_t = λ σ²_{t-1} + (1-λ) r²_{t-1}

- RiskMetrics default: λ = 0.94 (daily), λ = 0.97 (monthly)
- No mean reversion — persistence parameter α+β = 1 implicitly
- Simple, one parameter, widely used in practice

### GARCH(1,1)
Generalizes EWMA with mean-reverting volatility:

σ²_t = ω + α r²_{t-1} + β σ²_{t-1}

- Stationarity requires: α + β < 1
- Long-run variance: V_L = ω / (1 - α - β)
- Half-life of volatility shocks: h = ln(2) / ln(α + β)
- Typical equity values: α ≈ 0.05-0.10, β ≈ 0.85-0.95

### Implied Volatility
The volatility σ that sets the Black-Scholes model price equal to the observed market price:

C_market = BS(S, K, T, r, σ_imp)

- Solved numerically (Newton-Raphson or bisection)
- Model-dependent: assumes log-normal returns (Black-Scholes)
- Different from realized volatility — the gap is the variance risk premium

### Volatility Smile and Skew
Implied volatility varies by strike price:
- **Smile**: IV higher for deep OTM puts and calls (common in FX)
- **Skew**: IV higher for OTM puts than OTM calls (common in equity indices)
- Reflects market pricing of tail risk and crash protection demand

### Volatility Term Structure
Implied volatility varies by expiration:
- Upward-sloping in calm markets (uncertainty increases with horizon)
- Inverted (downward-sloping) during stress (near-term fear dominates)

### Volatility Surface
Two-dimensional surface: IV as a function of both strike (or delta) and maturity.
- Used for pricing exotic options and interpolating IV for non-traded strikes/maturities
- Parameterized models: SVI (Stochastic Volatility Inspired), SABR

### Realized vs Implied Volatility
- **Variance Risk Premium (VRP)**: IV typically exceeds RV → VRP = σ²_imp - σ²_realized > 0
- VRP compensates option sellers for bearing volatility risk
- VRP varies over time and is larger during stress periods

### VIX
- CBOE Volatility Index: 30-day implied volatility of S&P 500 options
- Calculated from a strip of OTM options (model-free approach)
- Often called the "fear gauge" — spikes during market stress
- VIX futures are typically in contango (roll cost for long VIX positions)

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| EWMA | σ²_t = λσ²_{t-1} + (1-λ)r²_{t-1} | Simple volatility forecast |
| GARCH(1,1) | σ²_t = ω + αr²_{t-1} + βσ²_{t-1} | Mean-reverting volatility model |
| Long-run variance | V_L = ω / (1-α-β) | GARCH steady-state volatility |
| Half-life | h = ln(2) / ln(α+β) | Speed of mean reversion |
| Black-Scholes call | C = SN(d₁) - Ke^{-rT}N(d₂) | Option pricing for IV extraction |
| d₁ | d₁ = [ln(S/K) + (r+σ²/2)T] / (σ√T) | Black-Scholes intermediate |
| Variance risk premium | VRP = σ²_implied - σ²_realized | Compensation for vol risk |

## Worked Examples

### Example 1: EWMA Forecast
**Given:** Yesterday's variance σ²_{t-1} = 0.0004 (σ = 2%), today's return r = -3%, λ = 0.94
**Calculate:** Today's variance forecast
**Solution:**
σ²_t = 0.94 × 0.0004 + 0.06 × (-0.03)² = 0.000376 + 0.000054 = 0.000430
σ_t = √0.000430 = 2.07%
The large negative return increased the volatility estimate from 2.00% to 2.07%.

### Example 2: GARCH Long-Run Volatility
**Given:** ω = 0.000002, α = 0.08, β = 0.91
**Calculate:** Long-run annualized volatility and half-life of shocks
**Solution:**
- Check stationarity: α + β = 0.99 < 1 ✓
- Long-run daily variance: V_L = 0.000002 / (1 - 0.99) = 0.0002
- Long-run daily vol: √0.0002 = 1.414%
- Annualized: 1.414% × √252 = 22.4%
- Half-life: ln(2) / ln(0.99) = 69 days — shocks persist for months

## Common Pitfalls
- GARCH stationarity: α + β must be strictly < 1 (otherwise variance is non-stationary)
- EWMA has no mean reversion — it's actually IGARCH(1,1) where α + β = 1
- Implied volatility is model-dependent: Black-Scholes assumes log-normal returns
- Conflating historical/realized vol with implied/forward-looking vol
- Using daily GARCH for long-horizon forecasts without term structure adjustment
- VIX measures 30-day expected vol, not current instantaneous vol

## Cross-References
- **historical-risk** — realized volatility estimators (input to GARCH calibration)
- **forward-risk** — VaR and CVaR use volatility forecasts as inputs
- **statistics-fundamentals** — distribution fitting, maximum likelihood estimation
- **equities** — equity index volatility, factor vol
- **fixed-income-sovereign** — interest rate volatility, swaption vol

## Reference Implementation
See `scripts/volatility_modeling.py` for computational helpers.
