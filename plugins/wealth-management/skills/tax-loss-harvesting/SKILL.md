---
name: tax-loss-harvesting
description: "Execute a complete tax-loss harvesting workflow from candidate identification through post-harvest monitoring. Use when the user asks about finding TLH candidates, gain/loss budgeting, replacement security selection, wash-sale compliance, or harvest execution planning. Also trigger when users mention 'unrealized losses in my portfolio', 'swap ETFs for tax purposes', 'harvest losses before year-end', 'substantially identical security', 'wash-sale window', 'NIIT offset', 'loss carryforward', or ask how much tax they can save by harvesting."
---

# Tax-Loss Harvesting

## Core Concepts

### Candidate Identification
Scan the portfolio for positions with unrealized losses that meet all three filters:

- **Materiality threshold:** Minimum absolute loss (e.g., $2,000) or minimum loss-to-value ratio (e.g., loss exceeds 5% of position market value). Harvesting a $200 loss on a $50,000 portfolio is not worth the operational cost.
- **Holding period filter:** Positions held less than 31 days may not have meaningful losses and create short-term wash-sale complexity. Positions approaching the one-year mark (days 335-365) may benefit from waiting to convert a short-term loss into a long-term loss only if the position is expected to continue declining.
- **Loss magnitude ranking:** Rank candidates by Tax Benefit = Unrealized Loss * Applicable Tax Rate. Prioritize short-term losses (taxed at ordinary rates up to 37%) over long-term losses (taxed at capital gains rates of 15-20%) when gain/loss budget allows.

### Gain/Loss Budgeting
Before harvesting, build the year-to-date tax budget:

1. **Realized gains YTD:** Sum all short-term and long-term capital gains already realized (including fund distributions).
2. **Planned gain exposure:** Estimate gains from pending rebalancing trades, planned liquidations, or expected fund capital gain distributions.
3. **Loss carryforward balance:** Check prior-year unused capital loss carryforwards (these offset gains before new harvests do).
4. **Target harvest amount:** Target Harvest = (Realized Gains YTD + Planned Gains) - Loss Carryforward + $3,000 ordinary income offset. Harvesting this amount offsets all expected gains AND captures the full $3,000 annual deduction against ordinary income; harvest more to build carryforward for future years.

### Replacement Security Selection
The replacement must maintain market exposure without being "substantially identical":

- **ETF-to-ETF swaps:** Switch between funds tracking different indices (e.g., Vanguard Total Stock Market to Schwab Broad Market, or S&P 500 to Russell 1000). Different index methodology is generally sufficient.
- **Individual stock replacement:** Replace a single stock with a sector ETF or a peer company. Example: sell Apple, buy Technology Select Sector SPDR (XLK).
- **Tracking error budget:** The replacement should have a correlation of 0.95+ and tracking error under 2% annualized relative to the original holding. Wider tracking error is acceptable for larger tax benefits.
- **Expense ratio delta:** Ensure the replacement does not have meaningfully higher expenses. A 10 bps cost increase on a $100K position held for 30 days costs roughly $8 — negligible against a $2,000+ tax benefit.

### Wash-Sale Compliance
The wash-sale rule (IRC Section 1091) disallows a loss if a substantially identical security is acquired within the 61-day window (30 days before + sale date + 30 days after):

- **Cross-account scope:** The rule applies across ALL accounts owned by the taxpayer: taxable brokerage, Traditional IRA, Roth IRA, 401(k), HSA, and spouse's accounts. A purchase in any of these accounts triggers wash-sale disallowance.
- **IRA wash-sale trap:** If a wash sale is triggered by a purchase in an IRA, the disallowed loss is permanently lost — it cannot be added to the IRA cost basis. This is the most dangerous wash-sale scenario.
- **DRIP suspension:** Automatic dividend reinvestment (DRIP) in the sold security or a substantially identical fund must be suspended during the 61-day window. Reinvesting even a small dividend triggers a partial wash sale.
- **Spouse coordination:** Purchases in a spouse's accounts (including retirement accounts) trigger wash-sale rules. Both spouses' automatic investments, 401(k) contributions, and DRIP settings must be reviewed.

### Execution Planning
Translate candidates into an actionable trade list:

- **Lot selection method:** Use Specific Identification (Spec ID) to select the highest-cost-basis lots first (HIFO). This maximizes the realized loss per share sold. If only partial harvesting is needed, sell only the lots with cost basis above current market price.
- **Coordination with rebalancing:** If the portfolio also needs rebalancing, combine TLH sells with rebalance sells to reduce total trade count. A position that is both overweight and at a loss is the ideal candidate — the harvest and rebalance are the same trade.
- **Timing strategy:** Year-end harvesting (October-December) captures the full year's losses but faces market timing risk. Opportunistic harvesting throughout the year during drawdowns of 5%+ captures losses that may recover by year-end.
- **Trade list fields:** Security, account, action (sell/buy), shares, lot IDs, estimated loss, replacement security, wash-sale window start/end dates.

### Tax Savings Calculation
Quantify the dollar value of each proposed harvest:

- **Federal rate selection:** Short-term losses offset short-term gains first (up to 37% ordinary rate). Long-term losses offset long-term gains (15-20% rate). Net losses of either type can cross over to offset the other, then up to $3,000 offsets ordinary income.
- **State tax impact:** Most states tax capital gains as ordinary income (rates range from 0% up to California's top statutory rate on investment income of 13.3%; California's effective top rate on wage income is 14.4%+ since the 2024 SDI uncapping). Include state tax savings in the calculation; for a California resident at the 13.3% bracket, state tax roughly doubles the benefit of each harvest.
- **NIIT interaction:** The 3.8% Net Investment Income Tax (IRC Section 1411) applies to the lesser of net investment income or MAGI exceeding $250,000 (MFJ) — a statutory threshold that is not inflation-indexed. Harvested losses reduce net investment income, potentially eliminating NIIT exposure.

### Post-Harvest Monitoring
After executing the harvest:

- **Wash-sale window tracking:** Maintain a calendar of open wash-sale windows with security identifiers and expiration dates. Flag any pending purchases (including automated ones) that would violate the window.
- **Replacement performance:** Monitor tracking error between the replacement and original security. If the replacement significantly underperforms (>3% divergence), evaluate whether the tax benefit justified the swap.
- **Cost basis updates:** Verify that broker statements reflect the new (lower) cost basis on replacement securities. The replacement's basis equals purchase price, not the original security's basis.
- **Swap-back timing:** After the 31st day, the investor may sell the replacement and repurchase the original security if desired. Evaluate whether the swap-back itself triggers a taxable gain on the replacement position.

### Household-Level Coordination
TLH across a household with multiple accounts requires centralized tracking:

- **Account type matrix:** Taxable accounts are the only accounts where TLH generates direct tax benefits. Retirement accounts have no realized gains/losses for tax purposes, but they can trigger wash sales in taxable accounts.
- **Advisor-managed vs held-away:** If the client has accounts at other institutions (401(k) plan, outside brokerage), the advisor cannot control purchases. Document held-away holdings and instruct the client to avoid purchasing substantially identical securities during open wash-sale windows.
- **Spousal coordination checklist:** (1) Review spouse's 401(k) fund lineup for overlap, (2) suspend DRIP in spouse's accounts for harvested securities, (3) coordinate any year-end tax trades across both spouses.

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| Tax Benefit | Benefit = Realized_Loss * Applicable_Tax_Rate | Dollar value of a single harvest |
| Net Tax Alpha | Alpha = Tax_Savings - Tracking_Error_Cost - Transaction_Costs | True value after implementation costs |
| Break-Even Holding Period | T_be = Tax_Savings / (Annual_Tracking_Error_Cost + Annual_Expense_Delta) | How long replacement can be held before costs exceed benefit |
| Wash-Sale Adjusted Basis | New_Basis = Replacement_Purchase_Price + Disallowed_Loss | Cost basis when wash sale is triggered |
| Annual TLH Capacity | Capacity = Portfolio_Value * Expected_Volatility * Loss_Capture_Rate | Estimate of harvestable losses per year |
| Target Harvest Amount | Target = Realized_Gains_YTD + Planned_Gains - Loss_Carryforward + 3000 | Harvest needed to offset all gains plus the $3,000 ordinary-income deduction |

## Worked Examples

### Example 1: Single Position Harvest with Replacement Selection
**Given:**
- Client holds 500 shares of XYZ Corp purchased at $80/share ($40,000 cost basis), current price $62/share ($31,000 market value), held 8 months (short-term)
- Client has $12,000 in short-term realized gains YTD, marginal federal rate 35%, state rate 9.3%, NIIT applies (3.8%)
- Replacement candidate: Sector ETF (correlation 0.97, tracking error 1.4% annualized, expense ratio 0.10% vs 0% for individual stock)

**Calculate:** Tax benefit, net tax alpha, and break-even holding period for the replacement.

**Solution:**
1. **Unrealized loss:** $31,000 - $40,000 = -$9,000 (short-term)
2. **Applicable rate:** 35% federal + 9.3% state + 3.8% NIIT = 48.1% combined
3. **Tax benefit:** $9,000 * 48.1% = **$4,329**
4. **Transaction costs:** Commission $0 (zero-commission broker) + estimated spread cost 0.05% * $31,000 * 2 trades = $31
5. **Tracking error cost:** 1.4% annualized * $31,000 * (30/365) = **$36** (for the 30-day minimum hold)
6. **Net tax alpha:** $4,329 - $31 - $36 = **$4,262**
7. **Annual cost of replacement:** $31,000 * (0.10% expense + 1.4% tracking error drag estimate of 0.05%) = $46.50/year
8. **Break-even holding period:** $4,262 / $46.50 = **91.7 years** — the tax benefit overwhelmingly justifies the swap
9. **Action:** Sell XYZ Corp (Spec ID, all lots), buy Sector ETF. Set wash-sale window reminder for 31 calendar days. Suspend any XYZ DRIP in all household accounts.

### Example 2: Portfolio-Wide TLH Scan with Gain/Loss Budget
**Given:**
- $2M taxable portfolio, 15 equity positions, year is mid-October
- Realized gains YTD: $18,000 long-term, $5,000 short-term
- Loss carryforward from prior years: $0
- Planned rebalancing trades will realize approximately $4,000 in additional long-term gains
- Three positions show unrealized losses: Position A (-$14,000 LT), Position B (-$6,500 ST), Position C (-$2,100 LT)
- Federal LTCG rate 20%, ordinary rate 37%, state 5%, NIIT 3.8%

**Calculate:** Target harvest amount, prioritized trade list, and total tax savings.

**Solution:**
1. **Gain/loss budget:**
   - Total expected gains: $18,000 LT + $5,000 ST + $4,000 LT (planned) = $22,000 LT + $5,000 ST = $27,000
   - Loss carryforward: $0
   - Target harvest: $27,000 - $0 + $3,000 = **$30,000** to fully offset gains and capture the $3,000 ordinary income deduction
2. **Candidate ranking by tax benefit:**
   - Position B: $6,500 ST * (37% + 5% + 3.8%) = $6,500 * 45.8% = **$2,977** (highest rate — harvest first)
   - Position A: $14,000 LT * (20% + 5% + 3.8%) = $14,000 * 28.8% = **$4,032** (largest absolute benefit)
   - Position C: $2,100 LT * 28.8% = **$605**
3. **Harvest plan:** Harvest all three: $14,000 + $6,500 + $2,100 = $22,600 in total losses — $7,400 short of the $30,000 target, so every harvested dollar is consumed offsetting gains and the $3,000 ordinary-income offset is not reached
   - $5,000 ST losses offset $5,000 ST gains at 45.8% = $2,290 saved
   - $1,500 remaining ST losses cross over to offset LT gains at 28.8% = $432 saved
   - $16,100 LT losses ($14,000 A + $2,100 C) offset $16,100 of $22,000 LT gains at 28.8% = $4,637 saved
   - Remaining taxable LT gains: $22,000 - $16,100 - $1,500 = **$4,400** still taxable
   - **Total tax savings: $2,290 + $432 + $4,637 = $7,359**
4. **Coordinate with rebalancing:** Position A is also 2% overweight — its TLH sell doubles as a rebalance sell, saving one round-trip trade.

### Example 3: Wash-Sale Violation Across Accounts
**Given:**
- On November 5, client sells VTI (Vanguard Total Stock Market ETF) in taxable account for a $8,000 long-term loss
- On November 20 (15 days later), client's 401(k) makes its regular bi-weekly contribution, which includes an allocation to a Vanguard Total Stock Market Index Fund (institutional share class of the same fund)
- 401(k) contribution to the total stock market fund: $750

**Calculate:** Wash-sale impact and corrected cost basis.

**Solution:**
1. **Wash-sale triggered:** The 401(k) fund is substantially identical to VTI (same underlying index, same fund family). The purchase on November 20 falls within the 30-day post-sale window (November 5 + 30 = December 5).
2. **Disallowed loss:** The wash-sale disallowance is proportional to the replacement shares acquired. If 500 VTI shares were sold and the $750 401(k) purchase acquired the equivalent of approximately 3 shares at $250/share, then 3/500 = 0.6% of the loss is disallowed.
3. **Disallowed amount:** $8,000 * (3/500) = **$48 disallowed**
4. **Remaining allowable loss:** $8,000 - $48 = **$7,952** — still deductible
5. **Basis adjustment — 401(k) trap:** The $48 disallowed loss would normally be added to the replacement security's cost basis. However, because the replacement was purchased inside a 401(k), the cost basis adjustment provides NO future tax benefit (401(k) distributions are taxed as ordinary income regardless of basis). The $48 is permanently lost.
6. **Prevention:** Before executing TLH, review the client's 401(k) fund lineup and contribution schedule. If the 401(k) holds a substantially identical fund, either (a) temporarily redirect that 401(k) allocation to a non-identical fund during the wash-sale window, or (b) delay the TLH sale until after the next 401(k) contribution and ensure no contribution occurs for 30 days after.

## Common Pitfalls
- Harvesting losses without checking for substantially identical holdings in retirement accounts, triggering permanent loss disallowance in IRAs/401(k)s
- Forgetting to suspend DRIP on the sold security and related funds across all household accounts during the 61-day window
- Harvesting small losses (under $1,000) where transaction costs and operational complexity exceed the tax benefit
- Over-harvesting in early years, depressing cost basis so severely that future sales generate outsized gains (basis step-down compounding)
- Failing to coordinate with spouse's automated investments (401(k) payroll contributions, robo-advisor purchases)
- Selecting a replacement security that is substantially identical (same index, same fund family, different share class) — this does not avoid wash-sale rules
- Not tracking the holding period of replacement securities, leading to unintended short-term gains when the replacement is later sold
- Ignoring state tax differences when calculating harvest value — states with no income tax (FL, TX, NV) reduce the benefit by 5-13 percentage points versus high-tax states

## Cross-References
- **tax-efficiency** (wealth-management plugin): broader tax-aware investing context; TLH is one strategy within the overall tax-efficiency framework
- **rebalancing** (wealth-management plugin): TLH trades should be coordinated with rebalancing to minimize total transaction count
- **investment-suitability** (compliance plugin): replacement securities must still satisfy suitability requirements
- **investment-policy** (wealth-management plugin): IPS may specify TLH policy parameters (minimum loss threshold, approved replacement pairs)
- **performance-attribution** (wealth-management plugin): tax alpha from TLH should be tracked and attributed separately
- **client-review-prep** (advisory-practice plugin): TLH opportunities are flagged during periodic client review preparation
- **financial-planning-workflow** (advisory-practice plugin): TLH is a specific tax recommendation that may emerge from the financial plan
