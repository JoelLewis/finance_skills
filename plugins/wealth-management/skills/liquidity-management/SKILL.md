---
name: liquidity-management
description: "Plan and manage cash flow to ensure adequate liquidity while minimizing opportunity cost of excess cash. Use when the user asks about cash flow forecasting, CD or bond laddering, liquidity tiers, income smoothing for variable earners, or sweep strategies. Also trigger when users mention 'T-bill ladder', 'where to park cash', 'irregular income budgeting', 'freelancer cash management', 'lumpy expenses', 'liquidity ratio', 'how much cash to hold', or ask how to plan for large upcoming expenses."
---

# Liquidity Management

## Core Concepts

### Cash Flow Forecasting
Project income and expenses monthly for 12+ months:
- **Income sources**: salary, business income, investment income, rental income, side gigs
- **Fixed expenses**: mortgage/rent, insurance, subscriptions, loan payments
- **Variable expenses**: food, utilities, discretionary spending
- **Periodic lumpy expenses**: property taxes, insurance premiums, tuition, estimated taxes
- **Net cash flow**: income - expenses per period → identifies surplus/deficit months

### Income Smoothing (Variable Earners)
For commission, freelance, seasonal, or bonus-heavy income:
- Compute trailing 12-month average income as "base salary equivalent"
- Budget based on base amount, not peak months
- Buffer surplus months into a smoothing reserve (separate from emergency fund)
- Target smoothing reserve: 2-3 months of base expenses
- Draw from reserve in below-average months

### Liquidity Tiers
Classify investable assets by time to access:

| Tier | Access Time | Examples | Typical Yield |
|------|------------|---------|---------------|
| Tier 1 — Immediate | Same day | Checking and savings at your primary bank, money market funds | Low |
| Tier 2 — Short-term | 1-3 business days | High-yield savings at an online bank, brokerage sweep cash, T-bills, bond funds and bond ETFs | Moderate |
| Tier 3 — Medium-term | 1-4 weeks (or penalty cost) | CDs (early-withdrawal penalty), I-bonds (after 1-year lockup) | Moderate-High |
| Tier 4 — Long-term | 30+ days | Real estate, PE/VC, locked alternatives, retirement accounts (pre-59½) | Highest |

Tier notes:
- **Tier 1 vs Tier 2 savings:** the distinction is transfer time, not product type. A savings account at your primary bank offers same-day access (Tier 1); a high-yield savings account at an online bank typically requires a 1-3 business day ACH transfer to reach your checking account (Tier 2).
- **Bond funds and bond ETFs:** both settle T+1 (the US moved to T+1 settlement in May 2024 for equities, ETFs, and mutual funds), so sale proceeds are available in roughly 1-3 business days including transfer to a bank. They belong in Tier 2 for access time — though, unlike deposits, the sale price is subject to market risk.

### CD Laddering
Stagger CD maturities for regular access + higher yields:
- Example: $60K split into 6 CDs maturing every 2 months
- As each CD matures: either use the cash or reinvest at the longest rung
- Benefit: captures term premium while maintaining periodic liquidity
- Variant: 3/6/9/12-month ladder, renewing each at 12 months

### Bond Laddering
Similar concept with Treasury or corporate bonds:
- Annual maturities across 1-5 or 1-10 years
- Provides predictable cash flows and interest rate diversification
- Rungs mature and are reinvested at prevailing rates (automatic rate averaging)

### T-Bill Ladder
Short-duration, high-liquidity ladder:
- 4/8/13/26-week T-bills rolling continuously
- Purchased at Treasury Direct or through brokerage
- State tax exempt (federal only)
- Highly liquid: can sell on secondary market before maturity

### Liquidity Metrics
- **Liquidity ratio**: liquid assets / monthly expenses (target ≥ 3-6)
- **Cash reserve ratio**: cash + near-cash / total portfolio
- **Current ratio** (business): current assets / current liabilities (target > 1.5)
- **Quick ratio** (business): (current assets - inventory) / current liabilities

### Seasonal and Tax Planning
- **Estimated taxes**: quarterly for self-employed (Q1: Apr 15, Q2: Jun 15, Q3: Sep 15, Q4: Jan 15)
- **Property taxes**: typically semi-annual — reserve monthly for escrow-like smoothing
- **Holiday/vacation**: set aside monthly into dedicated sub-account
- **Annual expenses**: insurance premiums, memberships → amortize monthly

### Margin of Safety
Maintain buffer above minimum liquidity requirements:
- Income uncertainty → larger buffer
- Known upcoming large expenses → pre-fund 2-3 months early
- Market correlation: income and portfolio may both decline in recession

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| Liquidity ratio | Liquid assets / monthly expenses | Adequacy check |
| Net cash flow | Σ income - Σ expenses | Monthly surplus/deficit |
| CD ladder yield | Weighted average of rung yields | Blended return on ladder |
| Smoothing reserve | Base monthly expenses × 2-3 | Buffer for variable income |
| Breakeven penalty | CD early withdrawal penalty / (CD rate - savings rate) | Whether to break CD |

## Worked Examples

### Example 1: CD Ladder Construction
**Given:** $60,000 to deploy, want liquidity every 2 months, 12-month CDs yielding 4.8%
**Calculate:** Ladder structure and blended yield
**Solution:**
- Split into 6 equal CDs of $10,000 each
- Stagger maturities: 2, 4, 6, 8, 10, 12 months
- Initial yields may vary by term: 2mo=4.2%, 4mo=4.4%, 6mo=4.5%, 8mo=4.6%, 10mo=4.7%, 12mo=4.8%
- Blended yield ≈ average = 4.53%
- Every 2 months one CD matures → reinvest at 12-month rate (4.8%) or use funds
- After full cycle (12 months), all CDs are 12-month earning 4.8%

### Example 2: Variable Income Smoothing
**Given:** Freelancer with monthly income ranging $3,000-$15,000, average $8,000. Monthly expenses $5,500.
**Calculate:** Base budget and smoothing reserve target
**Solution:**
- Base budget: $5,500/month (essential expenses)
- Average monthly surplus: $8,000 - $5,500 = $2,500
- Smoothing reserve target: $5,500 × 3 = **$16,500**
- In months earning >$8K: direct excess to smoothing reserve until funded
- In months earning <$5.5K: draw from smoothing reserve
- Once reserve is funded, excess above $8K goes to savings/investment goals

## Common Pitfalls
- Illiquidity surprise: needing cash when assets are locked in alternatives or retirement accounts
- Penalty drag from breaking CDs frequently (defeats the purpose of laddering)
- Over-optimizing yield at the expense of access (yield chasing in illiquid instruments)
- Not planning for estimated tax payments (large quarterly cash needs for self-employed)
- Ignoring correlation between income loss and market decline (both happen in recessions)
- Treating credit lines as liquidity (they can be revoked when most needed)

## Cross-References
- **emergency-fund** (wealth-management plugin): first tier of liquidity, must be funded before optimizing
- **lending** (wealth-management plugin): margin loans, HELOCs as backup liquidity (with risks)
- **time-value-of-money** (core plugin): CD/bond pricing, yield calculations
- **debt-management** (wealth-management plugin): debt payments are fixed cash flow obligations
- **savings-goals** (wealth-management plugin): multiple goals compete for available cash flow
- **tax-efficiency** (wealth-management plugin): estimated taxes, tax-loss harvesting timing
- **fixed-income-sovereign** (wealth-management plugin): T-bill ladder mechanics, Treasury Direct
- **financial-planning-workflow** (advisory-practice plugin): cash flow tier structure informs the liquidity analysis in comprehensive financial plans

## Running the script
Run the reference implementation directly:

```
uv run scripts/liquidity_management.py     # PEP 723 header resolves dependencies automatically
python3 scripts/liquidity_management.py    # after: pip install numpy scipy
```

A bare run prints a demo covering liquidity ratios, a 12-month cash flow projection, cash runway, liquidity tier analysis, CD ladder construction, income smoothing, and CD breakeven analysis. Use `--verify` to recompute the demo figures and assert they match this skill's worked examples (prints PASS/FAIL, exits nonzero on mismatch), and `--help` to list the available classes and functions. The file is primarily meant to be imported as a module (`from liquidity_management import LiquidityManagement`) rather than run standalone.
