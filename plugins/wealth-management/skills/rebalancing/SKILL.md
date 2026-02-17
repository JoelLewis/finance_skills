---
name: rebalancing
description: "Portfolio rebalancing: calendar-based, threshold-based, cost-aware rebalancing, tax-efficient approaches."
allowed-tools: ["Bash", "Read", "Write", "Edit"]
---

# Rebalancing

## Purpose
Provides frameworks for maintaining portfolio allocations over time as market movements cause weights to drift from targets. Covers calendar and threshold rebalancing strategies, optimal band widths, transaction cost considerations, tax-efficient approaches including tax-loss harvesting, and practical implementation across account types.

## Layer
4 — Portfolio Construction

## Direction
both

## When to Use
- Deciding when and how to rebalance a portfolio back to target weights
- Comparing calendar-based vs. threshold-based rebalancing strategies
- Setting optimal rebalancing bands that balance tracking error against transaction costs
- Implementing tax-efficient rebalancing and tax-loss harvesting
- Managing rebalancing across taxable and tax-deferred accounts
- Using cash flows (contributions/withdrawals) to rebalance opportunistically
- Evaluating the rebalancing premium and its contribution to portfolio returns

## Core Concepts

### Calendar Rebalancing
Rebalance at fixed time intervals regardless of drift magnitude:

- **Monthly:** Tightest tracking to targets; highest transaction costs
- **Quarterly:** Common institutional frequency; good balance of tracking and costs
- **Annually:** Lowest cost; may allow significant drift between dates

Calendar rebalancing is simple to implement and schedule but may miss large dislocations between dates or trigger unnecessary trades when drift is minimal.

### Threshold (Band) Rebalancing
Rebalance when any asset weight drifts beyond a defined tolerance band around its target:

- Monitor weights continuously (or at regular intervals)
- Trigger rebalancing when |w_actual - w_target| > tolerance
- Typical bands: +/- 3% to +/- 5% (absolute) or +/- 20% to +/- 25% (relative)

Threshold rebalancing is more responsive to market dislocations and avoids unnecessary trades when markets are calm. However, it requires more frequent monitoring.

### Optimal Band Width (Leland Model)
Leland (2000) derived the optimal no-trade band width as a function of transaction costs, risk aversion, and asset variance:

Band width proportional to (3 * transaction_cost / (2 * risk_aversion * variance))^(1/3)

Key intuition:
- Higher transaction costs → wider bands (trade less)
- Higher risk aversion → narrower bands (maintain target more tightly)
- Higher variance → narrower bands (drift happens faster, risk of deviation is greater)

### Rebalancing Premium
Systematic rebalancing generates a "volatility harvesting" or "rebalancing premium" through the buy-low/sell-high mechanism:

- When an asset rises, its weight increases → rebalancing sells some (sell high)
- When an asset falls, its weight decreases → rebalancing buys some (buy low)

This effect is sometimes called **Shannon's Demon**: in a two-asset portfolio with equal expected returns but independent volatility, the constantly rebalanced portfolio outperforms buy-and-hold. The rebalancing premium is larger when:
- Asset volatilities are higher
- Correlations are lower
- Assets have similar expected returns (so mean-reversion dominates trends)

Note: The rebalancing premium is not a free lunch — it underperforms in trending markets where winners keep winning.

### Transaction Costs
Costs incurred when rebalancing that reduce net returns:

- **Commissions:** Per-trade or per-share fees (increasingly zero for retail)
- **Bid-ask spread:** The cost of crossing the spread; wider for less liquid assets
- **Market impact:** Price movement caused by the trade itself; significant for large positions in less liquid markets
- **Opportunity cost:** Delay cost if rebalancing is deferred to avoid transaction costs

Total implementation cost = commissions + half-spread + market impact + opportunity cost

### Tax-Efficient Rebalancing
Strategies to minimize tax impact when rebalancing in taxable accounts:

1. **Use cash flows:** Direct new contributions to underweight assets and withdrawals from overweight assets
2. **Redirect dividends and interest:** Reinvest income from overweight assets into underweight assets
3. **Rebalance with new contributions:** The most tax-efficient method — no selling required
4. **Asset location:** Hold tax-inefficient assets (bonds, REITs) in tax-deferred accounts; rebalance these freely
5. **Selective lot identification:** When selling, choose tax lots with the highest cost basis (lowest gain) or lots held over one year (long-term capital gains rate)

### Tax-Loss Harvesting (TLH)
Proactively selling losing positions to realize capital losses that offset capital gains:

Tax benefit = Realized loss * Marginal tax rate

Rules and implementation:
- **Wash sale rule:** Cannot repurchase a "substantially identical" security within 30 days before or after the sale (61-day window total)
- **Replacement security:** Substitute a similar but not identical asset to maintain market exposure (e.g., sell one S&P 500 ETF, buy a total market ETF)
- **Timing:** Most opportunities arise during market drawdowns
- **Long-term benefit:** Harvested losses can offset current gains, and unused losses carry forward indefinitely. Up to $3,000 of net losses can offset ordinary income per year.

### Rebalancing Across Account Types
When an investor has multiple account types (taxable, IRA, 401k), optimize rebalancing by:

- **Tax-deferred accounts (IRA, 401k):** Rebalance freely — no tax consequences
- **Taxable accounts:** Minimize selling; use cash flows, TLH, and selective lot sales
- **Cross-account rebalancing:** Consider the aggregate portfolio across all accounts and rebalance within the most tax-efficient account

### Drift Tolerance Setting
Factors that determine optimal band width:

- **Tighter bands (e.g., +/- 2%):** Better risk control, higher costs, appropriate for low-cost/institutional settings
- **Wider bands (e.g., +/- 10%):** Lower costs, more drift risk, appropriate for taxable accounts with high tax impact
- **Asset-specific bands:** More volatile assets may need wider absolute bands but tighter relative bands

### Cash Flow Rebalancing
Use regular deposits or withdrawals to move toward target weights without explicit rebalancing trades:

- Calculate current vs. target weights
- Direct 100% of new contributions to the most underweight asset(s)
- Process withdrawals from the most overweight asset(s)
- This "natural rebalancing" is the most cost-effective and tax-efficient approach

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| Threshold Trigger | |w_actual - w_target| > tolerance | Rebalancing trigger condition |
| Optimal Band Width | band ~ (3*tc / (2*lambda*sigma^2))^(1/3) | Leland optimal no-trade zone |
| Tax-Loss Benefit | Benefit = Loss * Tax Rate | Value of harvested losses |
| Transaction Cost | TC = commission + spread/2 + impact | Total rebalancing cost |
| Drift | Drift_i = w_actual_i - w_target_i | Weight deviation from target |
| Trade Size | Trade_i = (w_target_i - w_actual_i) * Portfolio Value | Dollar amount to trade |
| Rebalancing Premium | RP ~ (1/2) * Σ w_i * sigma_i^2 - (1/2) * sigma_p^2 | Volatility harvesting estimate |

## Worked Examples

### Example 1: Threshold Rebalancing — 60/40 Portfolio
**Given:**
- Target: 60% equity / 40% bonds
- Rebalancing threshold: +/- 5% (absolute)
- Current portfolio value: $1,000,000
- After market movement: equity = $680,000 (68%), bonds = $320,000 (32%)

**Calculate:** Rebalancing trigger and required trades

**Solution:**

Check drift:
- Equity drift: 68% - 60% = +8% → exceeds +5% threshold → **TRIGGER**
- Bond drift: 32% - 40% = -8% → exceeds -5% threshold → **TRIGGER**

Target dollar amounts:
- Equity target: 60% * $1,000,000 = $600,000
- Bond target: 40% * $1,000,000 = $400,000

Required trades:
- Sell equity: $680,000 - $600,000 = **$80,000**
- Buy bonds: $400,000 - $320,000 = **$80,000**

Proceeds from equity sales fund the bond purchases. In a taxable account, check the cost basis of equity lots being sold to estimate tax impact before executing.

### Example 2: Tax-Loss Harvesting Benefit
**Given:**
- Position purchased for $50,000, current value $40,000
- Unrealized loss: $10,000
- Investor's marginal federal tax rate: 37% (ordinary income) / 20% (long-term capital gains)
- Investor has $15,000 in realized capital gains this year

**Calculate:** Tax benefit of harvesting the loss

**Solution:**

Realized loss from sale: **$10,000**

Tax benefit calculation:
- The $10,000 loss offsets $10,000 of the $15,000 in realized capital gains
- Tax saved: $10,000 * 20% = **$2,000** (assuming long-term gains rate)
- Remaining gains: $15,000 - $10,000 = $5,000 (still taxable)

If the investor had no capital gains to offset:
- First $3,000 offsets ordinary income: $3,000 * 37% = $1,110
- Remaining $7,000 carries forward to future years
- Total immediate benefit: $1,110; total eventual benefit up to $2,000+ depending on future gains

Implementation:
1. Sell the losing position for $40,000
2. Immediately purchase a similar but not substantially identical replacement (e.g., swap a total US stock ETF for an S&P 500 ETF)
3. Do NOT repurchase the original security within 30 days (wash sale rule)
4. After 31 days, may swap back to original security if preferred

Note: TLH creates a lower cost basis in the replacement security, so taxes are deferred, not eliminated. However, the time value of the tax deferral and the ability to offset gains at favorable rates makes TLH valuable.

## Common Pitfalls
- Over-rebalancing: trading too frequently erodes returns through transaction costs and taxes, especially in taxable accounts
- Under-rebalancing: allowing excessive drift exposes the portfolio to unintended risk levels and style drift
- Wash sale violations when tax-loss harvesting: purchasing a substantially identical security within the 61-day window triggers wash sale rules, disallowing the loss
- Ignoring tax impact of rebalancing in taxable accounts: rebalancing by selling winners generates taxable capital gains
- Calendar rebalancing may miss large dislocations between dates (e.g., a 20% market crash between quarterly rebalancing dates)
- Not accounting for the rebalancing premium when comparing strategies — buy-and-hold backtests may understate rebalanced portfolio returns
- Forgetting to consider the full 61-day wash sale window (30 days before and after the sale)
- Rebalancing into the wrong account: selling appreciated assets in taxable accounts when the same rebalancing could be done in tax-deferred accounts

## Cross-References
- **asset-allocation** (Layer 4): rebalancing maintains the target asset allocation over time
- **diversification** (Layer 4): rebalancing preserves the intended diversification structure
- **bet-sizing** (Layer 4): position sizes drift and need rebalancing to maintain conviction weighting
- **risk-return** (Layer 1): drift changes portfolio risk profile; rebalancing controls it
- **financial-statements** (Layer 2): tax implications of rebalancing require understanding of tax accounting

## Reference Implementation
See `scripts/rebalancing.py` for computational helpers.
