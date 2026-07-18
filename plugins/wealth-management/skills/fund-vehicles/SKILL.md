---
name: fund-vehicles
description: "Compare and select investment vehicles including mutual funds, ETFs, index funds, and separately managed accounts. Use when the user asks about ETF vs mutual fund, expense ratios, fund tax efficiency, ETF creation/redemption, tracking error, or share class comparisons. Also trigger when users mention 'which fund should I buy', 'Vanguard vs Fidelity', 'index fund costs', '12b-1 fees', 'load vs no-load', 'SMA vs ETF', 'fund turnover ratio', 'securities lending', or ask how fees compound over time."
---

# Fund Vehicles

## Core Concepts

### Vehicle Comparison: Decision-Relevant Differences
- **Trading:** ETFs trade intraday at market prices that can deviate from NAV (premiums/discounts, especially in volatile markets or for illiquid underlying assets); mutual funds transact once daily at NAV.
- **Tax efficiency:** ETFs generally distribute far fewer capital gains than mutual funds (mechanism below); SMAs allow lot-level tax-loss harvesting that pooled vehicles cannot.
- **Customization:** SMAs hold individual securities directly, so investors can exclude stocks/sectors and harvest specific lots; minimums are typically $100K-$1M+ with fees above index ETFs.
- **Cost:** broad index ETFs and index mutual funds cost as little as 0.01-0.05%; active mutual funds commonly cost 0.50-1.00%+ before any loads.

### Expense Ratios
Total annual cost as a percentage of AUM, deducted from fund returns. Includes management fees, administrative costs, and sometimes 12b-1 distribution fees. The expense ratio is the single most predictive factor of future fund performance — lower-cost funds consistently outperform higher-cost funds within the same category.

### Tracking Difference
The actual return gap between a fund and its benchmark index over a period. Tracking difference = Fund Return - Index Return. Expense ratio is a floor for tracking difference, but additional factors (securities lending income, sampling, cash drag, trading costs) can make tracking difference better or worse than the expense ratio.

### Tax Efficiency and the Creation/Redemption Mechanism
The general tax-efficiency hierarchy: ETFs > index mutual funds > actively managed mutual funds.

Authorized Participants (APs) create ETF shares by delivering a basket of the underlying securities in-kind, and redeem by receiving securities in-kind. These in-kind transfers do not trigger capital gains, so ETFs rarely distribute gains. Mutual funds must sell securities to meet redemptions, distributing the resulting gains to all remaining shareholders — taxable events even for buy-and-hold investors.

### Securities Lending Revenue
Funds can lend their holdings to short sellers in exchange for a fee. This revenue can partially or fully offset fund expenses, sometimes resulting in tracking difference better than the expense ratio. Large index funds are major securities lenders.

### Turnover Ratio
Measures how frequently a fund buys and sells its holdings. Higher turnover leads to more taxable capital gains distributions, higher transaction costs, and greater market impact. Typical turnover: index funds 3-10%, active funds 50-200%+.

### 12b-1 Fees and Loads
- **12b-1 fees:** annual distribution and marketing fees (0.25-1.0%), included in the expense ratio.
- **Front-end loads:** one-time sales charge at purchase (typically 3-5.75%), reducing the initial investment.
- **Back-end loads (CDSCs):** Contingent Deferred Sales Charges paid upon redemption, typically declining to 0% over 5-7 years.

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| Expense Drag (annual) | AUM × Expense Ratio | Annual cost of fund ownership |
| Tracking Difference | Fund Return - Index Return | Actual cost of indexing |
| Fee Impact (compounded) | FV = PV × (1 + r - ER)^n vs PV × (1 + r)^n | Long-term fee drag |
| Tax Cost Ratio | Pre-Tax Return - After-Tax Return | Tax efficiency measure |
| NAV | (Total Assets - Liabilities) / Shares Outstanding | Fund share value |

## Worked Examples

### Example 1: Long-Term Fee Impact
**Given:** $100,000 invested for 30 years at 8% gross return. Fund A: 0.03% expense ratio. Fund B: 0.75% expense ratio.
**Calculate:** Final values and fee drag for each fund
**Solution:**
Fund A: $100,000 × (1 + 0.08 - 0.0003)^30 = $100,000 × (1.0797)^30 = $997,914
Fund B: $100,000 × (1 + 0.08 - 0.0075)^30 = $100,000 × (1.0725)^30 = $816,430
Difference: $997,914 - $816,430 = $181,484

The 0.72% annual fee difference (0.75% - 0.03%) compounds to $181,484 over 30 years — approximately 18% of the low-cost fund's terminal value. This is wealth destroyed by fees for an identical gross return.

### Example 2: ETF vs Mutual Fund Tax Efficiency
**Given:** Identical S&P 500 portfolios, $100,000 invested for 20 years. Gross return 10%, expense ratio 0.03% for both, so both grow at 9.97% before distribution taxes. The ETF distributes $0 in capital gains (in-kind redemptions). The mutual fund distributes 2% of NAV in long-term capital gains each year-end. The investor is in the 20% LTCG bracket.

**Assumptions:** Distributions are taxed at 20% in the year received; the after-tax remainder is reinvested and adds to cost basis. Both positions are liquidated after year 20, with remaining unrealized gains taxed at 20%.

**Calculate:** After-tax liquidation values
**Solution:**

ETF — all gains deferred until sale:
- Pre-tax terminal value: $100,000 × (1.0997)^20 = $669,090
- Liquidation tax: ($669,090 - $100,000) × 20% = $113,818
- **After-tax value: $555,272**

Mutual fund — year-by-year, each year the position grows 9.97%, distributes 2% of NAV, and pays 20% tax on the distribution (equivalent to multiplying by 1.0997 × 0.996 each year):
- Pre-liquidation value after 20 years: $617,549
- Taxes paid on distributions along the way: $23,888 (on $119,442 of cumulative distributions)
- Cost basis: $100,000 + $95,554 reinvested after-tax distributions = $195,554
- Liquidation tax: ($617,549 - $195,554) × 20% = $84,399
- **After-tax value: $617,549 - $84,399 = $533,150**

The ETF's tax deferral advantage is $555,272 - $533,150 = **$22,122** over 20 years on this $100,000 investment — the cost of paying tax annually instead of letting the full balance compound until sale.

## Common Pitfalls
- Ignoring tracking difference — it can be worse than the expense ratio due to cash drag, sampling, and trading costs
- Not considering tax efficiency when comparing returns — pre-tax fund returns overstate what taxable investors actually keep
- Confusing NAV with market price for ETFs — ETFs can trade at premiums or discounts to NAV, especially in volatile markets or for illiquid underlying assets
- Overlooking securities lending income that offsets expenses — some index funds achieve tracking difference better than their expense ratio

## Cross-References
- **equities** (wealth-management plugin): equity fund selection and equity index tracking
- **fixed-income-sovereign** (wealth-management plugin): bond fund considerations (see also **fixed-income-corporate** (wealth-management plugin))
- **tax-efficiency** (wealth-management plugin): comprehensive after-tax investment analysis
- **asset-allocation** (wealth-management plugin): selecting vehicles within an asset allocation
- **factor-investing** (wealth-management plugin): evaluating factor ETFs and smart-beta funds on factor purity, turnover, capacity, and fee per unit of loading
## Running the script

```
uv run scripts/fund_vehicles.py
```

The PEP 723 header resolves the numpy dependency automatically. Alternatively run `python3 scripts/fund_vehicles.py` after `pip install numpy`.

- Bare run prints a demo covering fee impact, tracking error, NAV premium/discount, fund overlap, and ETF-vs-mutual-fund tax efficiency.
- `--verify` re-runs the demo computations and asserts the outputs match this skill's worked examples (prints PASS/FAIL, nonzero exit on mismatch).
- `--help` lists the available classes.

The file is primarily meant to be imported as a module, e.g. `from fund_vehicles import ExpenseAnalysis, TrackingAnalysis, TaxEfficiency`.
