---
name: real-assets
description: "Analyze real estate and infrastructure investments including REITs, direct property valuation, and infrastructure assets. Use when the user asks about real estate investing, REITs, cap rates, NOI, FFO, AFFO, property valuation, or infrastructure investments. Also trigger when users mention 'rental property analysis', 'cash-on-cash return', 'gross rent multiplier', 'REIT dividends', 'real estate sectors', 'cell towers', 'toll roads', 'LTV ratio', 'DSCR', or ask whether to invest in real estate directly or through REITs."
---

# Real Assets

## Purpose
Provide actionable workflows for analyzing direct property investments, REITs, and infrastructure assets using standard real estate valuation metrics.

## Layer
2 — Asset Classes

## Direction
both

## When to Use
- Property valuation, cap rate analysis, or cash-on-cash return calculation
- REIT evaluation using FFO, AFFO, P/FFO, or NAV premium/discount
- Direct vs REIT investment decision
- Leverage assessment (LTV, DSCR) for a property deal
- Infrastructure asset analysis (toll roads, utilities, cell towers)

## Core Concepts

### Decision Framework: Direct Property vs REIT

| Factor | Direct Property | REIT |
|--------|----------------|------|
| Liquidity | Low (months to sell) | High (exchange-traded) |
| Control | Full (operations, capex, tenants) | None |
| Minimum capital | High ($50K-$500K+ equity) | Low (single share) |
| Tax benefits | Depreciation pass-through, 1031 exchanges | 90%+ income distribution (taxed as ordinary) |
| Diversification | Concentrated (1-few properties) | Broad (portfolio of assets) |
| Key metrics | NOI, Cap Rate, Cash-on-Cash, GRM | FFO, AFFO, P/FFO, NAV premium/discount |

**Use direct property when:** investor wants control, tax benefits, or local market expertise advantage.
**Use REITs when:** investor needs liquidity, diversification, or sector exposure without operational burden.

### Direct Property Analysis Workflow

**Step 1 - Calculate NOI:**
- NOI = Effective Gross Income - Operating Expenses
- Effective Gross Income = Gross Potential Rent - Vacancy Allowance + Other Income
- Operating Expenses: taxes, insurance, maintenance, management, utilities (exclude debt service, capex, depreciation)

**Step 2 - Determine Cap Rate and Valuation:**
- Cap Rate = NOI / Property Value (unlevered yield)
- Value = NOI / Cap Rate (income approach valuation)
- Source cap rates from comparable recent sales in the same market/property type

**Step 3 - Screen with GRM:**
- GRM = Price / Gross Annual Rent (quick filter; ignores expenses and financing)

**Step 4 - Assess Leverage:**
- LTV = Loan Amount / Property Value (target: 60-75% commercial, up to 80% residential)
- DSCR = NOI / Annual Debt Service (minimum 1.20x-1.50x required by lenders)
- Positive leverage: mortgage rate < cap rate (leverage amplifies returns)
- Negative leverage: mortgage rate > cap rate (leverage erodes returns)

**Step 5 - Calculate Levered Return:**
- Cash-on-Cash = (NOI - Annual Debt Service) / Total Cash Invested

### REIT Evaluation Workflow

**Step 1 - Calculate FFO:**
- FFO = Net Income + Depreciation/Amortization - Gains on Property Sales
- Adds back depreciation (non-cash charge that overstates decline in property value)

**Step 2 - Calculate AFFO:**
- AFFO = FFO - Maintenance Capex - Straight-Line Rent Adjustments
- More conservative measure of recurring distributable cash flow

**Step 3 - Relative Valuation:**
- P/FFO: REIT equivalent of P/E; compare within same sector only
- P/AFFO: more conservative, accounts for maintenance capex
- NAV premium/discount = (Share Price - NAV per Share) / NAV per Share
  - Premium > 0: market values management/growth above asset value
  - Discount < 0: potential value opportunity or market concern about asset quality

**Step 4 - Assess Payout Sustainability:**
- AFFO payout ratio = Dividends per Share / AFFO per Share
- Ratio > 100% signals unsustainable distribution

### Infrastructure Assets
- Asset types: toll roads, utilities, pipelines, cell towers, airports, ports
- Revenue model: regulated/contracted with CPI-linked escalators
- Profile: long asset lives, high barriers to entry, stable bond-like income with usage-growth upside
- Evaluate using: DCF with contracted cash flows, regulated return on equity, dividend yield vs peers

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| NOI | Gross Rental Income - Operating Expenses | Property income measure |
| Cap Rate | NOI / Property Value | Unlevered property yield |
| Property Value | NOI / Cap Rate | Income-based valuation |
| Cash-on-Cash | Annual Cash Flow / Total Cash Invested | Levered equity return |
| GRM | Price / Gross Annual Rent | Quick screening metric |
| FFO | Net Income + Depreciation - Gains on Sales | REIT earnings measure |
| AFFO | FFO - Maintenance Capex - Straight-Line Rent Adj | Recurring cash flow |
| LTV | Loan Amount / Property Value | Leverage measure |
| DSCR | NOI / Annual Debt Service | Debt coverage measure |

## Worked Examples

### Example 1: Property Valuation and Cap Rate Sensitivity
**Given:** NOI = $100,000/yr, comparable cap rate = 6%
**Value** = $100,000 / 0.06 = **$1,666,667**
**Sensitivity:** Cap rate compresses to 5% -> Value = $2,000,000 (+20% from 100bp decline). Cap rates are highly sensitive — always stress-test +/- 50-100bp.

### Example 2: Levered vs Unlevered Return
**Given:** Property = $500K, equity = $200K (40%), mortgage = $300K at 6%, NOI = $35K, debt service = $17K/yr
- Unlevered cap rate: $35K / $500K = **7.0%**
- Cash flow after debt: $35K - $17K = $18K
- Cash-on-Cash: $18K / $200K = **9.0%**
- Positive leverage confirmed: debt cost (6%) < cap rate (7.0%), boosting equity return from 7.0% to 9.0%

### Example 3: REIT Valuation
**Given:** REIT reports Net Income = $50M, Depreciation = $30M, Gains on Sales = $5M, Maintenance Capex = $10M, Straight-Line Rent Adj = $2M, Shares = 20M, Share Price = $45, NAV/Share = $40
- FFO = $50M + $30M - $5M = **$75M** ($3.75/share)
- AFFO = $75M - $10M - $2M = **$63M** ($3.15/share)
- P/FFO = $45 / $3.75 = **12.0x**
- P/AFFO = $45 / $3.15 = **14.3x**
- NAV premium = ($45 - $40) / $40 = **+12.5%** (market values growth/management above asset base)

## Common Pitfalls
- Cap rate is not total return — it ignores appreciation, leverage, and capex
- Never use P/E for REITs — depreciation distorts net income; use P/FFO or P/AFFO
- Always use effective gross income (after vacancy allowance) for NOI, not gross potential rent
- Use AFFO, not FFO, to assess distributable cash flow — FFO ignores maintenance capex
- Comparing cap rates across different property types or markets without adjustment
- Ignoring negative leverage risk: if mortgage rate > cap rate, leverage destroys equity returns

## Cross-References
- **time-value-of-money** (core plugin, Layer 0): discounted cash flow analysis of property investments
- **equities** (wealth-management plugin, Layer 2): REIT stock analysis and equity market context
- **fixed-income-structured** (wealth-management plugin, Layer 2): MBS and the mortgage market underlying real estate
- **asset-allocation** (wealth-management plugin, Layer 3): real assets as a portfolio diversifier and inflation hedge

## Reference Implementation
See `scripts/real_assets.py` for computational helpers.
