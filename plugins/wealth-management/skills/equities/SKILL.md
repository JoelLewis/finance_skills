---
name: equities
description: "Analyze equity securities, factor models, and equity portfolio construction. Use when the user asks about stocks, equity valuation ratios, index construction methods, or style analysis. Also trigger when users mention 'P/E ratio', 'growth vs value', 'market cap weighting', 'sector allocation', 'GICS classification', 'earnings per share', 'Fama-French factors', 'CAPM', 'dividend yield', 'PEG ratio', 'EV/EBITDA', or ask which factors explain equity returns."
---

# Equities

This skill is a decision procedure: which valuation metric to use for which company, which index methodology fits which mandate, and the order of operations for analyzing a stock. It assumes the user can look up definitions; the value here is choosing the right tool.

## Core Concepts

### Choosing the Valuation Metric

Match the metric to the sector and capital structure — using the wrong one is the most common equity-analysis error.

| Situation | Use | Avoid | Why |
|-----------|-----|-------|-----|
| Financials (banks, insurers) | P/B, P/TBV, ROE vs P/B | EV/EBITDA | Debt is raw material, not financing — EV and EBITDA are meaningless; book value is marked closer to fair value |
| Capital-intensive (industrials, telecom, energy) | EV/EBITDA, EV/EBIT | P/E alone | Neutralizes depreciation policy and leverage differences across peers |
| Mature dividend payers (utilities, staples) | Dividend yield + payout sustainability, P/E | PEG | Growth is low and stable; income and coverage matter most |
| High-growth, low/no earnings | EV/Sales, PEG (if earnings exist), unit economics | P/E, P/B | Earnings are depressed by reinvestment; book value is mostly intangibles |
| Cyclicals (autos, semis, materials) | Mid-cycle or normalized P/E, P/B at trough | Spot P/E | P/E is lowest at the cycle peak and highest at the trough — spot P/E inverts the buy/sell signal |
| Negative earnings, positive cash flow | EV/EBITDA, P/FCF | P/E, earnings yield | Ratio is undefined or misleading with negative denominator |
| REITs and listed real estate | P/FFO, P/AFFO, NAV | P/E | GAAP depreciation distorts earnings for property — handled in detail by the real-assets skill |
| Cross-border / different leverage | EV-based multiples | Equity multiples | Enterprise value normalizes for capital structure |

Cross-checks that apply everywhere:
- Use forward (next-12-month) estimates for the numerator decision when the business is changing; trailing figures when estimate quality is poor.
- Compare against the company's own history and a true peer set, not the whole market.
- Translate any multiple into its implied assumptions (growth, margin, required return) before declaring cheap/expensive — a low multiple usually encodes a real problem.

### Choosing the Index Methodology

| Mandate | Methodology | Trade-off to flag |
|---------|-------------|-------------------|
| Cheap, tax-efficient market exposure | Cap-weighted (S&P 500, total market) | Momentum-chasing by construction; concentration in mega-caps — a single sector can exceed 30% |
| Reduce concentration / small-cap tilt | Equal-weighted | Higher turnover and rebalancing cost; structural size and contrarian tilt |
| Break the price-weight link | Fundamental-weighted (revenue, earnings, book) | Effectively a value tilt with extra steps; compare cost vs an explicit value fund |
| Explicit factor exposure | Factor/style index (value, momentum, quality, low vol) | Verify the factor definition and rebalance rules; factor timing rarely works |
| Avoid | Price-weighted (DJIA-style) | Weight proportional to share price is economically arbitrary — legacy only |

Selection rules: default to cap-weighted for core beta; add equal- or fundamental-weighted only when the user explicitly wants the embedded tilt and accepts the turnover; treat any "smart beta" product as a factor portfolio and evaluate its factor loadings, not its marketing name.

### Security Analysis Sequence

1. **Classify the business** — sector (GICS or equivalent), cyclical vs defensive, capital intensity, leverage. This determines the valuation toolkit (table above).
2. **Quality screen** — revenue trend, margin trend, ROIC vs cost of capital, balance-sheet risk (net debt/EBITDA, interest coverage), share count trajectory (dilution vs buybacks).
3. **Earnings basis** — pick trailing vs forward EPS, check for one-offs, use diluted share count. For cyclicals, normalize to mid-cycle.
4. **Value with the matched metric** — primary multiple from the table, one cross-check multiple, and where dividends are central a dividend-based check (Gordon growth: P = D1 / (r - g), valid only when g < r).
5. **Factor and style context** — regress (or eyeball) exposures to market beta, size, value, momentum, quality. Distinguish stock-specific thesis from a factor bet you could buy more cheaply via an index.
6. **Portfolio fit** — marginal effect on sector concentration and factor tilts; total return (price + dividends) is the comparison basis, never price return alone.

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| EV/EBITDA | (Market Cap + Debt - Cash) / EBITDA | Capital-structure-neutral valuation |
| Earnings Yield | EPS / Price | Compare equity vs bond yields |
| PEG | (P/E) / Earnings Growth Rate (in %) | Growth-adjusted valuation |
| Gordon Growth | P = D1 / (r - g) | Dividend-based intrinsic value |
| CAPM | E(R) = R_f + beta × (E(R_m) - R_f) | Required return input for valuation |
| Total Return | Price Return + Dividend Return | Performance comparison basis |

## Worked Examples

### Metric Selection and Valuation

**Given:** An industrial company with market cap $500M, total debt $100M, cash $50M, EBITDA $75M, EPS $7.50, price $150.
**Decide and calculate:**
1. Capital-intensive industrial → primary metric is EV/EBITDA (table above), with P/E as cross-check.
2. EV = $500M + $100M - $50M = $550M. EV/EBITDA = $550M / $75M = **7.33x**.
3. Cross-check: P/E = $150 / $7.50 = 20.0x; earnings yield = 7.50 / 150 = **5.0%**.
4. Interpretation: 7.33x EV/EBITDA is modest for an industrial if margins are stable — compare against the peer set and the company's own 5-10 year range. The 20x P/E looks richer than the EV multiple because the company carries little net debt; the EV multiple is the better cross-peer comparison.

## Common Pitfalls
- Applying EV/EBITDA to banks or P/E to REITs — metric/sector mismatch is the dominant error this skill exists to prevent
- Buying cyclicals on low trailing P/E at the cycle peak (the "value trap" inversion)
- Treating a fundamental-weighted or smart-beta index as alpha rather than a packaged factor tilt
- Confusing price return with total return — dividends compound to a large share of long-run equity returns
- Survivorship bias in backtested factor or screen results

## Cross-References
- **historical-risk** (wealth-management plugin): volatility and drawdown measurement for equity return series
- **statistics-fundamentals** (core plugin): beta estimation via CAPM regression
- **performance-metrics** (wealth-management plugin): Sharpe ratio and related risk-adjusted return measures
- **fund-vehicles**: equity fund selection (ETFs, mutual funds, SMAs)
- **currencies-and-fx**: international equity currency effects
- **asset-allocation**: equity allocation within multi-asset portfolios
- **real-assets**: REIT valuation (P/FFO, NAV) is owned by that skill
- **qualitative-valuation** and **quantitative-valuation**: deeper single-company valuation workflows

## Running the Script

```bash
uv run scripts/equities.py            # run the demo (uses PEP 723 inline deps)
uv run scripts/equities.py --verify   # check demo outputs against the worked example (exit 1 on mismatch)
python3 scripts/equities.py            # alternative (requires: pip install numpy)
```

The demo prints valuation metrics (including the worked example's EV/EBITDA and earnings yield), a factor regression on synthetic data, and sector concentration analysis. Run `--help` for a list of the classes and functions. For programmatic use, import the module rather than running it — the demo only executes under `python equities.py`.
