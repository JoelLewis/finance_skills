---
name: performance-metrics
description: "Evaluate investment performance on a risk-adjusted basis using industry-standard ratios and capture analysis. Use when the user asks about Sharpe ratio, Sortino ratio, Information Ratio, Treynor ratio, Calmar ratio, Omega ratio, or upside/downside capture. Also trigger when users mention 'risk-adjusted returns', 'return per unit of risk', 'M-squared', 'is this fund worth the volatility', 'how to compare two managers', 'capture ratio', or ask which investment performed better after accounting for risk."
---

# Performance Metrics

## Core Concepts

### Sharpe Ratio
The most widely used risk-adjusted performance measure. It divides excess return (over the risk-free rate) by total volatility.

```
SR = (R_p - R_f) / sigma_p
```

- R_p: annualized portfolio return
- R_f: annualized risk-free rate
- sigma_p: annualized portfolio volatility (standard deviation of returns)

A higher Sharpe ratio indicates more return per unit of total risk. Typical benchmarks: SR < 0.5 is poor, 0.5-1.0 is acceptable, > 1.0 is strong, > 2.0 is exceptional.

**Annualization:** If computed from monthly data, SR_annual = SR_monthly * sqrt(12).

### Sortino Ratio
Replaces total volatility with downside deviation, penalizing only harmful volatility (returns below a Minimum Acceptable Return).

```
Sortino = (R_p - R_f) / sigma_downside
```

where sigma_downside = sqrt((1/n) * sum(min(R_i - MAR, 0)^2)).

Common MAR choices: 0%, risk-free rate, or a target return. Always state which MAR is used, and use the same reference point in the numerator as in the downside deviation: if the MAR is not the risk-free rate, the numerator should be (R_p - MAR), not (R_p - R_f). Mixing reference points makes the ratio internally inconsistent.

### Information Ratio
Measures active return (alpha) per unit of active risk (tracking error) relative to a benchmark.

```
IR = (R_p - R_b) / TE
```

where TE = std(R_p - R_b) * sqrt(N).

An IR above 0.5 is generally considered good; above 1.0 is exceptional and difficult to sustain.

### Treynor Ratio
Measures excess return per unit of systematic risk (beta) rather than total risk.

```
Treynor = (R_p - R_f) / beta_p
```

Useful for evaluating diversified portfolios where idiosyncratic risk has been diversified away. For undiversified holdings, the Sharpe ratio is more appropriate.

### Calmar Ratio
Relates annualized return to the worst peak-to-trough drawdown.

```
Calmar = CAGR / |MaxDrawdown|
```

A Calmar ratio above 1.0 means the annualized return exceeds the maximum drawdown. This ratio is popular among CTAs and hedge fund investors. Typically computed over a 3-year window.

### Omega Ratio
A gain-loss ratio that considers the entire return distribution above and below a threshold tau.

```
Omega(tau) = integral from tau to +inf of [1 - F(r)] dr
             / integral from -inf to tau of F(r) dr
```

where F(r) is the cumulative distribution function of returns.

In practice, this is computed as:

```
Omega(tau) = sum(max(R_i - tau, 0)) / sum(max(tau - R_i, 0))
```

Omega > 1 means expected gains above tau exceed expected losses below tau. Unlike Sharpe, Omega captures the full shape of the distribution (skewness, kurtosis).

### Upside and Downside Capture Ratios
Measure how the portfolio participates in benchmark up and down markets.

```
Up Capture   = R_p(in up months) / R_b(in up months) * 100
Down Capture = R_p(in down months) / R_b(in down months) * 100
Capture Ratio = Up Capture / Down Capture
```

Ideal profile: Up Capture > 100% and Down Capture < 100%, yielding a Capture Ratio > 1. "Up months" and "down months" are defined by the benchmark return being positive or negative, respectively.

### M-Squared (Modigliani-Modigliani)
Expresses risk-adjusted return in the same units as return, by leveraging or deleveraging the portfolio to match benchmark volatility.

```
M^2 = R_f + SR_p * sigma_b
    = R_f + ((R_p - R_f) / sigma_p) * sigma_b
```

Interpretation: "If this portfolio were scaled to have the same volatility as the benchmark, it would have returned M-squared." This makes it directly comparable to benchmark returns.

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| Sharpe Ratio | (R_p - R_f) / sigma_p | Return per unit of total risk |
| Sortino Ratio | (R_p - R_f) / sigma_downside | Return per unit of downside risk |
| Information Ratio | (R_p - R_b) / TE | Active return per unit of active risk |
| Treynor Ratio | (R_p - R_f) / beta_p | Return per unit of systematic risk |
| Calmar Ratio | CAGR / |MaxDD| | Return per unit of drawdown risk |
| Omega Ratio | sum(max(R_i - tau, 0)) / sum(max(tau - R_i, 0)) | Full-distribution gain-loss ratio |
| Up Capture | R_p(up) / R_b(up) * 100 | Participation in rising markets |
| Down Capture | R_p(down) / R_b(down) * 100 | Participation in falling markets |
| M-Squared | R_f + SR_p * sigma_b | Risk-adjusted return in return units |

## Worked Examples

### Example 1: Sharpe Ratio Calculation
**Given:** A fund returned 12% annualized, the risk-free rate is 4%, and the fund's annualized volatility is 15%.

**Calculate:** Sharpe Ratio.

**Solution:**

```
SR = (0.12 - 0.04) / 0.15
   = 0.08 / 0.15
   = 0.533
```

The fund earned 0.533 units of excess return per unit of risk. This is in the "acceptable" range but below 1.0.

### Example 2: Comparing Funds with Sharpe and Sortino
**Given:**
- Fund A: Sharpe = 0.8, Sortino = 1.2
- Fund B: Sharpe = 0.7, Sortino = 1.5

**Calculate:** Which fund is better for a downside-averse investor?

**Solution:**

Fund A has a higher Sharpe ratio (0.8 vs 0.7), indicating better total-risk-adjusted performance. However, Fund B has a notably higher Sortino ratio (1.5 vs 1.2), meaning it delivers significantly more return per unit of downside risk.

The divergence implies Fund B's volatility is more skewed to the upside -- its total volatility includes more "good" volatility (gains), while its downside volatility is relatively contained.

**For a downside-averse investor, Fund B is preferable** because the Sortino ratio better captures the risk they care about (losses), and Fund B's superior Sortino indicates better downside risk management.

### Example 3: Information Ratio
**Given:** A portfolio returned 10% annualized, its benchmark returned 8%, and the tracking error is 4%.

**Calculate:** Information Ratio.

**Solution:**

```
IR = (0.10 - 0.08) / 0.04
   = 0.02 / 0.04
   = 0.50
```

The manager generated 0.50 units of active return per unit of active risk. This is generally considered a good IR, suggesting consistent alpha generation relative to benchmark deviations.

## Common Pitfalls
- **Annualizing Sharpe incorrectly:** The Sharpe ratio scales by sqrt(N) where N is the number of periods per year. SR_annual = SR_monthly * sqrt(12), not * 12. The excess return and volatility must be in consistent units before dividing.
- **Using wrong risk-free rate frequency:** If computing monthly Sharpe, use the monthly risk-free rate (annual rate / 12), not the annual rate directly.
- **Sortino MAR ambiguity:** The Sortino ratio result changes significantly depending on whether MAR = 0, MAR = risk-free rate, or MAR = some target return. Always state the MAR assumption explicitly.
- **Small sample sizes making ratios unreliable:** Ratios computed from fewer than 36 monthly observations are statistically unreliable. A Sharpe ratio from 12 months of data has a standard error of approximately sqrt((1 + SR^2/2) / 12), which is very wide.
- **Comparing Sharpe ratios across different time periods:** A Sharpe of 1.0 in a low-vol environment is not the same as 1.0 in a high-vol environment. Performance ratios are period-specific and not directly comparable across different market regimes.

## Cross-References
- **historical-risk** (wealth-management plugin, Layer 1a): Provides the risk measures (volatility, drawdown, downside deviation, tracking error) used as denominators in these performance ratios.
- **performance-reporting** (wealth-management plugin, Layer 8) and **return-calculations** (core plugin, Layer 0): For TWR/MWR calculation methodology and reporting presentation, see performance-reporting and core/return-calculations.
- **forward-risk** (wealth-management plugin, Layer 1b): Forward-looking risk measures (VaR, CVaR) complement retrospective performance assessment by estimating future potential losses.
- **volatility-modeling** (wealth-management plugin, Layer 1b): Volatility forecasts from GARCH or EWMA can be used to compute forward-looking or conditional Sharpe ratios.

## Running the script
Run with `uv run scripts/performance_metrics.py` (the PEP 723 header resolves numpy automatically) or with `python3 scripts/performance_metrics.py` after `pip install numpy scipy`. A bare run prints a full scorecard (Sharpe, Sortino, Information Ratio, Calmar, Treynor, Omega, capture ratios, batting average, win/loss) on seeded synthetic portfolio and benchmark data. Use `--verify` to assert outputs match this skill's worked examples and the demo's expected values (exit code 0 on PASS) and `--help` for an overview of the class. The file is primarily meant to be imported as a module (e.g., `from performance_metrics import PerformanceScorecard`).
