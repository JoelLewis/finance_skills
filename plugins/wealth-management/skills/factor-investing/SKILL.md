---
name: factor-investing
description: "Apply factor models to portfolio construction and fund evaluation, from CAPM through the Fama-French 3- and 5-factor models plus momentum. Use when the user asks about 'Fama-French', 'value factor', 'smart beta', 'factor tilt', 'momentum exposure', or the 'factor zoo', wants to run or interpret a factor regression (loadings, alpha after controlling for factors, R-squared, t-stats), decompose a manager's returns into factor exposures versus skill, or asks 'is my fund closet indexing'. Also trigger on SMB, HML, RMW, CMA, UMD, size/value/quality/profitability/low-vol premia, factor ETF or smart-beta product evaluation (factor purity, turnover, capacity, fees), factor cyclicality and the danger of factor timing, factor crowding, long-short academic factors versus long-only implementable tilts, and post-publication factor decay."
---

# Factor Investing

## Core Concepts

### From CAPM to Multifactor Models

CAPM prices a single source of risk: `E(R_i) - R_f = beta * (E(R_m) - R_f)`. Persistent anomalies — small caps, cheap (high book-to-market) stocks, and recent winners earning more than beta predicts — motivated adding factors. Fama-French (1993) added size and value to the market factor (3-factor model); Carhart (1997) added momentum; Fama-French (2015) added profitability and investment (5-factor model):

```
R_i - R_f = alpha + b_MKT*MKT + b_SMB*SMB + b_HML*HML [+ b_RMW*RMW + b_CMA*CMA] [+ b_UMD*UMD] + epsilon
```

The key reinterpretation: a manager's CAPM alpha may be nothing more than static factor exposure. Alpha only means skill *after* controlling for the factors an investor could buy cheaply. Single-factor OLS mechanics, t-statistics, and the CAPM regression itself live in the statistics-fundamentals skill; this skill generalizes to K regressors and interprets the output.

### The Canonical Factors

| Factor | Construction (long-short) | Rationale: risk-based | Rationale: behavioral | Approx. premium* |
|--------|---------------------------|----------------------|----------------------|------------------|
| MKT | Market minus risk-free | Non-diversifiable macro risk | — | 6-7%/yr |
| SMB (size) | Small caps minus big caps | Illiquidity, distress sensitivity | Neglect of small firms | 1.5-2%/yr |
| HML (value) | High book/market minus low | Distress risk, cyclical cash flows | Overextrapolation of growth | 2.5-3%/yr |
| RMW (profitability) | Robust minus weak operating profitability | Compensation for cash-flow risk | Underreaction to quality | ~3%/yr |
| CMA (investment) | Conservative minus aggressive asset growth | Q-theory: high investment implies low expected return | Empire-building overinvestment | ~3%/yr |
| UMD (momentum, Carhart) | Past 12-1 month winners minus losers | Crash risk (violent reversals) | Underreaction, herding | 6-7%/yr |

*Approximate annualized US long-short premia over the 1963-2024 sample, Ken French data library, as of 2026. Long-run averages, not forecasts; realized decade-long stretches deviate wildly (see cyclicality below).

The rationale matters for durability: risk-based premia should persist (someone must bear the risk); behavioral premia survive only while limits to arbitrage prevent them from being competed away — and are more vulnerable to crowding.

### Reading a Factor Regression

Run OLS of fund *excess* returns on the factor return series. Interpret:

- **Loadings (b_k):** exposure per unit of factor. b_HML = 0.45 means the fund behaves like it holds a 0.45-weight position in the value long-short portfolio. Judge each by its t-stat (|t| above roughly 2 for 5% significance).
- **Alpha:** average return unexplained by the factors — the only defensible claim to skill. A positive alpha with |t| < 2 is not evidence of skill (see statistics-fundamentals on t-statistics); most funds' alpha turns insignificant once value or momentum loadings are added.
- **R-squared:** fraction of return variance the factors explain. Diversified equity funds typically show R-squared of 0.90-0.99 against 3-4 factors. Use adjusted R-squared when comparing models with different factor counts — R-squared mechanically rises with every added regressor.
- **Stability:** run rolling windows; loadings that drift signal style drift or factor timing rather than a stable tilt.

### Alpha Decomposition and Closet-Index Detection

Two complementary uses of the same regression:

1. **Expected-return decomposition:** `E(R) = R_f + sum(b_k * lambda_k)`, where lambda_k are assumed factor premia. This tells you what the fund *should* earn from its exposures alone; realized excess return minus the factor-implied excess is the manager's implied alpha. If the implied alpha is near zero, the fund is a factor portfolio you could replicate with cheap factor ETFs.
2. **Closet-index screen:** a fund charging active fees while hugging its benchmark. Returns-based red flags: benchmark regression R-squared >= 0.98 and annualized tracking error <= 2%. The holdings-based analog is active share below ~60% (Cremers and Petajisto 2009). Then compute the breakeven Information Ratio: `IR_breakeven = (fund fee - index fee) / tracking error`. A closet indexer needs an implausibly high IR on a tiny active-risk budget just to earn back its fee gap (Information Ratio itself is covered in performance-metrics).

### Smart-Beta Product Evaluation

Treat every smart-beta product as a factor portfolio (the equities skill's rule) and evaluate the implementation, not the marketing name:

- **Factor purity:** regress the product on the academic factors. A "value" ETF with b_HML = 0.15 and b_MKT = 1.0 is expensive beta; look for the target loading to be significant and dominant, and for unintended loadings (e.g., a value fund's negative momentum exposure) to be modest.
- **Turnover:** momentum needs high turnover to exist (~100%+/yr); value needs little (~15-25%/yr). Turnover far above what the factor requires is cost drag; far below means stale exposure.
- **Capacity:** size and momentum degrade fastest with assets (small, illiquid names; high turnover). Mega-cap value and quality scale best.
- **Fees vs implementation quality:** the question is never "is 0.25% cheap?" but "what loading per basis point?" A 0.15% fund delivering b_HML = 0.20 is worse value than a 0.30% fund delivering b_HML = 0.50.

### Long-Short Academic Factors vs Long-Only Tilts

Published premia are measured on long-short, often leverage- and shorting-unconstrained portfolios rebalanced without costs. A long-only implementable tilt:

- captures roughly half of the paper premium (the short side, where mispricing is often larger, is unavailable; the overlap with the market portfolio dilutes the tilt);
- has loadings well below 1.0 on the academic factor (long-only value funds typically show b_HML of 0.3-0.5, not 1.0);
- pays real transaction costs and taxes the backtest ignored.

Scale expectations accordingly: a long-only value tilt with b_HML = 0.4 against a 2.5-3% premium is worth roughly 1.0-1.35%/yr before costs, not the headline long-short number.

### Factor Cyclicality and the Danger of Factor Timing

Every factor endures multi-year droughts: US value underperformed growth for roughly the 2017-2020 stretch, with a relative drawdown deep enough to end careers, before rebounding sharply in 2021-2022. Momentum crashes violently in sharp reversals (2009). Because droughts are long and turning points are unforecastable, factor *timing* — rotating into "cheap" factors — has a poor live record and adds turnover. The defensible uses of cyclicality are (a) diversifying across factors with low mutual correlation (value and momentum are natural complements) and (b) sizing tilts so the investor can survive a decade-long drought without capitulating at the bottom.

### The Factor Zoo, Crowding, and Replication

Hundreds of "significant" factors have been published — Cochrane's "factor zoo." Treat the zoo skeptically:

- **Multiple testing:** with hundreds of researchers mining the same data, t = 2 is far too weak; Harvey, Liu, and Zhu (2016) argue newly proposed factors should clear t > 3.
- **Post-publication decay:** McLean and Pontiff (2016) find anomaly returns roughly one-third lower out-of-sample and one-half lower post-publication — partly data-mining, partly investors crowding in and arbitraging the premium away.
- **Crowding:** popular factor trades unwind together under stress (August 2007 "quant quake"). Valuation spreads on a factor widening or compressing sharply indicate crowding in or out.
- Default to the handful of factors with decades of out-of-sample, out-of-country evidence and an economic rationale (market, value, momentum, profitability, size — in roughly that order of robustness); assume any newly marketed factor delivers materially less than its backtest.

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| 3-factor model | R_i - R_f = alpha + b_MKT*MKT + b_SMB*SMB + b_HML*HML + eps | Baseline equity attribution |
| Carhart 4-factor | 3-factor + b_UMD*UMD | Add momentum control |
| 5-factor model | 3-factor + b_RMW*RMW + b_CMA*CMA | Profitability and investment control |
| Expected-return decomposition | E(R) = R_f + sum(b_k * lambda_k) | Factor-implied return from loadings and premia |
| Implied alpha | realized excess mean - sum(b_k * lambda_k) | Skill after factor exposure |
| Significance rule | t = coefficient / SE; skill requires \|t(alpha)\| > ~2 | Separate luck from skill |
| Residual (active) vol | sigma_resid = sigma_fund * sqrt(1 - R^2) | Tracking-error decomposition |
| Breakeven IR | (fund fee - index fee) / tracking error | Closet-index fee test |

## Worked Examples

### Example 1: Is the "Value Fund" Adding Skill or Just Factor Exposure?

**Given:** 60 monthly excess returns of a US large-cap value fund regressed on MKT, SMB, HML (all in % per month):

```
alpha = 0.037  (t = 0.60)     -> 0.037 x 12 = 0.44% per year
b_MKT = 0.98   (t = 58.1)
b_SMB = 0.12   (t = 4.6)
b_HML = 0.45   (t = 23.1)
R^2   = 0.986   (residual vol 0.457% per month)
```

**Analysis:** The three factors explain 98.6% of the fund's return variance. The value loading of 0.45 is strong and highly significant (t = 23.1 >> 2) — this is a genuine, stable value tilt, typical of a long-only value fund (well below the 1.0 of the academic long-short HML portfolio). The market loading of 0.98 is ordinary full-invested equity exposure, and the small positive SMB loading shows a mild small-cap lean. Alpha is 0.44% per year with t = 0.60 < 2: statistically indistinguishable from zero.

**Verdict:** factor exposure, not skill. Everything this fund delivers could be replicated with a market fund plus a value-tilted index fund. Whether to own it now becomes a fee question (Example 3), not a skill question.

### Example 2: Expected-Return Decomposition from Loadings and Premia

**Given:** The Example 1 loadings, assumed forward-looking premia of MKT 6.5%, SMB 2.0%, HML 3.0% per year, a risk-free rate of 4.0% (assumption as of mid-2026), and a realized fund excess return of 8.4% per year.

```
MKT contribution = 0.98 x 6.5% = 6.37%
SMB contribution = 0.12 x 2.0% = 0.24%
HML contribution = 0.45 x 3.0% = 1.35%
Factor-implied excess return   = 6.37 + 0.24 + 1.35 = 7.96%
Total expected return          = 4.0% + 7.96% = 11.96%
Implied alpha                  = 8.4% - 7.96% = 0.44% per year
```

**Analysis:** Of the fund's 8.4% realized excess return, 7.96 points came from factor exposures and only 0.44 from anything unexplained — consistent with Example 1's insignificant regression alpha. Note also the implementability haircut: the fund's value tilt is worth 1.35%/yr (0.45 x 3.0%), roughly half the headline long-short HML premium, exactly as the long-only discussion above predicts.

### Example 3: Closet-Index Screen with Breakeven Information Ratio

**Given:** A fund with monthly volatility 4.30%, R-squared of 0.99 against its benchmark, a 0.85% expense ratio, and a 0.05% comparable index fund.

```
Residual vol   = 4.30% x sqrt(1 - 0.99) = 4.30% x 0.10 = 0.43% per month
Tracking error = 0.43% x sqrt(12) = 1.49% annualized
Fee gap        = 0.85% - 0.05% = 0.80% per year
Breakeven IR   = 0.80 / 1.49 = 0.54
```

**Analysis:** R-squared of 0.99 (>= 0.98) and tracking error of 1.49% (<= 2%) both trip the closet-index screen. Worse, on a 1.49% active-risk budget the manager must sustain an Information Ratio of 0.54 *just to break even on fees* — an IR that would rank among top-decile active managers, demanded here merely to match the index fund net of costs. **Verdict:** closet indexer; the rational holdings are the index fund, or a genuinely active fund whose tracking error is large enough to make its fee gap recoverable.

## Common Pitfalls

- **Calling CAPM alpha "skill":** most single-factor alpha is static size/value/momentum exposure; always control for the factors an investor can buy cheaply before crediting a manager.
- **Trusting a positive alpha with t < 2:** a 0.5%/yr alpha with t = 0.6 (Example 1) is noise, not evidence — the same rule statistics-fundamentals applies to CAPM alpha.
- **Expecting the academic premium from a long-only product:** long-only tilts load 0.3-0.5 on the factor and capture roughly half the paper premium, before the costs backtests ignore.
- **Timing factors:** decade-long droughts (value, 2017-2020) plus unforecastable turning points make factor rotation a reliable way to buy high and sell low; diversify across factors and size tilts for survivability instead.
- **Shopping the factor zoo:** hundreds of published factors fail the t > 3 multiple-testing bar; expect one-third to one-half post-publication decay (McLean and Pontiff 2016) and default to the handful with out-of-sample, out-of-country evidence.
- **Judging smart beta by fee alone:** compare loading delivered per basis point of fee; a cheap fund with a 0.15 target-factor loading is expensive beta in disguise.
- **Comparing R-squared across models with different factor counts:** R-squared rises mechanically with every regressor; use adjusted R-squared (statistics-fundamentals covers the overfitting guardrails).

## Cross-References

- **statistics-fundamentals** (core plugin): OLS regression mechanics, t-statistics, R-squared, and the single-factor CAPM regression that this skill's multifactor models extend
- **performance-metrics** (wealth-management plugin): Information Ratio and tracking error, used here in the closet-index breakeven test; risk-adjusted ratios complement factor attribution
- **equities** (wealth-management plugin): style and factor index construction; that skill's rule to evaluate smart-beta products as factor portfolios is executed here via loadings
- **asset-allocation** (wealth-management plugin): sizing factor tilts as deliberate, survivable deviations from the policy portfolio
- **diversification** (wealth-management plugin): low mutual correlation across factor premia (e.g., value and momentum) is a distinct diversification layer from asset classes
- **fund-vehicles** (wealth-management plugin): ETF, mutual fund, and SMA wrappers for factor exposure; fee, turnover, and capacity mechanics of the vehicles

## Running the Script

```bash
uv run scripts/factor_investing.py            # run the demo (uses PEP 723 inline deps)
uv run scripts/factor_investing.py --verify   # check outputs against the worked examples (exit 1 on mismatch)
python3 scripts/factor_investing.py           # alternative (requires: pip install numpy scipy)
```

`scripts/factor_investing.py` provides a `FactorInvesting` class with static methods `multifactor_regression` (K-factor OLS via numpy least squares, returning alpha, loadings, t-stats, p-values, R-squared, and residual vol), `expected_return_decomposition` (loadings x premia, with implied alpha), and `closet_index_diagnostics` (residual vol, tracking error, breakeven IR, closet-index flag). A bare run (or `--verify`) prints the demo on a deterministic seeded dataset **and** asserts the worked-example values above (Example 1 loadings/t-stats/R-squared, Example 2 decomposition, Example 3 diagnostics), exiting nonzero on any mismatch. Run `--help` for the method list. For programmatic use, import rather than run: `from factor_investing import FactorInvesting`.
