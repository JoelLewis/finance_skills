---
name: real-assets
description: "Analyze real estate and infrastructure investments including REITs, direct property valuation, and infrastructure assets. Use when the user asks about real estate investing, REITs, cap rates, NOI, FFO, AFFO, property valuation, or infrastructure investments. Also trigger when users mention 'rental property analysis', 'cash-on-cash return', 'gross rent multiplier', 'REIT dividends', 'real estate sectors', 'cell towers', 'toll roads', 'LTV ratio', 'DSCR', or ask whether to invest in real estate directly or through REITs."
---

# Real Assets

## Core Concepts

### Property Income and Return Metrics
- **NOI (Net Operating Income):** effective gross rental income (after vacancy) minus operating expenses; excludes debt service, capex, and depreciation.
- **Cap rate:** NOI divided by property value — the unlevered property yield; lower cap rates mean higher valuations.
- **Income-approach value:** NOI divided by the prevailing cap rate for comparable properties.
- **Cash-on-cash return:** annual pre-tax cash flow (NOI minus debt service) divided by total cash invested — the levered equity yield.
- **GRM (Gross Rent Multiplier):** price divided by gross annual rent; a quick screen that ignores expenses, vacancy, and financing.

### REITs and REIT Metrics
REITs must distribute 90%+ of taxable income as dividends and trade on exchanges like equities. Sectors include residential, office, retail, industrial, data center, healthcare, self-storage, and specialty.

- **FFO (Funds From Operations):** net income plus depreciation minus gains on property sales — the standard REIT earnings measure, since real estate depreciation overstates actual value decline.
- **AFFO (Adjusted FFO):** FFO minus maintenance capex and straight-line rent adjustments — the conservative measure of recurring distributable cash flow.
- **P/FFO and P/AFFO:** the REIT equivalents of P/E; compare within the same sector.
- **NAV premium/discount:** share price relative to per-share net asset value of the underlying properties; indicates market sentiment.

### Infrastructure Investments
Infrastructure assets include toll roads, utilities, pipelines, cell towers, airports, and ports. Characteristics: long asset lives, high barriers to entry, regulated or contracted revenue streams, and inflation-linked cash flows (many contracts include CPI adjustments). Infrastructure provides stable, bond-like income with equity-like upside from traffic/usage growth.

### Leverage in Real Estate
- **LTV (Loan-to-Value):** mortgage amount / property value. Higher LTV means more leverage and more risk. Typical commercial LTV is 60-75%.
- **DSCR (Debt Service Coverage Ratio):** NOI / annual debt service. Lenders typically require 1.20x-1.50x minimum. Higher DSCR means more cushion to service debt.

## Direct Real Estate vs REITs: Decision Checklist

Work through these factors before recommending a vehicle:

| Factor | Direct ownership | REITs |
|--------|------------------|-------|
| Liquidity | Sales take months; high transaction costs | Trade intraday on exchanges |
| Management | Active management required, or pay a property manager | Passive; professional management included |
| Leverage access | Non-recourse mortgage leverage at attractive LTVs (60-75%), chosen by the investor | Entity-level leverage set by REIT management; investors cannot choose property-level leverage |
| 1031 exchange | Eligible — defer capital gains by exchanging into like-kind property | Not eligible — REIT shares do not qualify |
| Diversification | Concentrated in one or a few properties | A REIT fund spreads across hundreds of properties and multiple sectors |
| Minimum check size | Typically $50K+ equity (down payment plus closing costs) | From one share |

Mapping investor situations to the preferred vehicle:

| Investor situation | Preferred vehicle |
|--------------------|-------------------|
| May need the money within months, or rebalances regularly | REITs |
| Wants control over leverage, tenants, and improvements | Direct |
| Holds appreciated property and wants tax-deferred reinvestment | Direct (1031 exchange) |
| Allocation under ~$50K, or wants broad diversification immediately | REITs |
| Willing to manage tenants and repairs (or pay a manager from rent) | Direct |
| Wants passive, hands-off exposure with no operational involvement | REITs |

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

### Example 1: Property Valuation Using Cap Rate
**Given:** NOI = $100,000 per year, prevailing cap rate for comparable properties = 6%
**Calculate:** Property value
**Solution:**
Value = NOI / Cap Rate = $100,000 / 0.06 = $1,666,667

The property is valued at approximately $1,666,667. If the cap rate compressed to 5% (e.g., in a hot market), the value would rise to $2,000,000 — a 20% increase from a 100bp cap rate decline. This illustrates the sensitivity of real estate values to cap rate changes.

### Example 2: Cash-on-Cash Return with Leverage
**Given:** Property value = $500,000, down payment = $200,000 (40%), mortgage = $300,000 at 6%, NOI = $35,000, annual debt service = $17,000
**Calculate:** Cash-on-cash return
**Solution:**
Annual pre-tax cash flow = NOI - Debt Service = $35,000 - $17,000 = $18,000
Cash-on-Cash Return = $18,000 / $200,000 = 9.0%

Compare to the unlevered cap rate: $35,000 / $500,000 = 7.0%. Leverage boosts the equity return from 7.0% to 9.0% because the cost of debt (6%) is below the cap rate (7.0%) — this is positive leverage. If the mortgage rate exceeded the cap rate, leverage would reduce returns (negative leverage).

## Common Pitfalls
- Confusing cap rate with total return — cap rate ignores appreciation, leverage effects, and capital expenditures
- Using P/E instead of P/FFO for REITs — depreciation distorts net income, making P/E misleading for real estate companies
- Ignoring vacancy rates in NOI calculation — always use effective gross income (after vacancy allowance), not gross potential rent
- Overstating returns by ignoring maintenance capex — use AFFO rather than FFO for a realistic view of distributable cash flow

## Cross-References
- **time-value-of-money** (core plugin): discounted cash flow analysis of property investments
- **equities** (wealth-management plugin): REIT stock analysis and equity market context
- **fixed-income-structured** (wealth-management plugin): MBS and the mortgage market underlying real estate
- **asset-allocation** (wealth-management plugin): real assets as a portfolio diversifier and inflation hedge

## Running the script

```
uv run scripts/real_assets.py
```

The PEP 723 header resolves the numpy dependency automatically. Alternatively run `python3 scripts/real_assets.py` after `pip install numpy`.

- Bare run prints a demo covering property valuation, cash-on-cash and leverage analysis, REIT metrics, and inflation-adjusted returns.
- `--verify` re-runs the demo computations and asserts the outputs match this skill's worked examples (prints PASS/FAIL, nonzero exit on mismatch).
- `--help` lists the available classes.

The file is primarily meant to be imported as a module, e.g. `from real_assets import PropertyValuation, LeverageMetrics, REITMetrics, RealReturn`.
