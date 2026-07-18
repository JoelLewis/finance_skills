---
name: margin-operations
description: "Guide margin lending, margin requirements, and margin call operations for brokerage and advisory accounts. Use when calculating Reg T initial margin or buying power, determining maintenance margin or house requirements, evaluating portfolio margin eligibility under OCC TIMS, generating or resolving margin calls (fed call, house call, exchange call, day-trade call), designing forced liquidation waterfall logic, structuring securities-backed lines of credit (SBLOC), computing margin interest impact on returns, assessing concentrated position margin, understanding pattern day trader rules, or reviewing FINRA 4210 and Reg U requirements. Also covers SMA calculations and short margin mechanics. For OTC derivatives margin (variation/initial margin, CSAs, SIMM) see counterparty-risk."
---

# Margin Operations

## Core Concepts

### Regulation T Initial Margin
The Federal Reserve's Regulation T establishes the initial margin requirement for purchasing securities on credit. Key provisions:

- **50% initial margin requirement:** An investor must deposit at least 50% of the purchase price of marginable securities. For a $100,000 purchase, the investor must deposit $50,000 (cash or marginable securities); the broker-dealer may lend the remaining $50,000.
- **Reg T buying power:** The maximum dollar amount a client can purchase given their available equity. Buying power = SMA x 2 (for equity securities under Reg T). If a client deposits $100,000 cash in a new margin account, buying power is $200,000.
- **Special Memorandum Account (SMA):** A bookkeeping entry that tracks the client's excess Reg T equity. SMA increases when: the account has excess equity above 50%, securities are sold, dividends or cash are deposited. SMA decreases when used to purchase securities or withdraw cash. SMA is a high-water mark — it does not decrease when market values decline (unless used).
- **Reg T extension procedures:** When a client fails to meet the initial margin requirement by settlement date, the broker-dealer must request an extension from a self-regulatory organization (SRO). Extensions are typically granted for 1-5 business days. Failure to meet the call results in forced liquidation and a 90-day freeze (restricted account).
- **Exempt securities:** U.S. government bonds, municipal bonds, and certain agency securities are exempt from Reg T margin requirements — they can be purchased with lower or no initial margin.
- **Day-trade margin:** FINRA Rule 4210 provides pattern day traders (4+ day trades in 5 business days) with 4:1 intraday buying power (25% margin) but requires a minimum equity of $25,000 — day-trade buying power = (equity - $25,000 minimum) × 4. Overnight positions revert to standard 2:1 Reg T buying power.

### Maintenance Margin
After the initial purchase, ongoing maintenance margin requirements determine the minimum equity the account must maintain:

- **FINRA Rule 4210 minimum:** 25% equity for long positions. Account equity = market value of securities minus debit balance. If equity falls below 25% of market value, a maintenance margin call is triggered.
- **House maintenance requirements:** Most broker-dealers impose requirements above the FINRA minimum, typically 30-40% for diversified accounts. House requirements vary by firm and may change based on market conditions.
- **Concentrated position margin:** Single-stock positions exceeding a threshold (e.g., 40-60% of account value) face elevated margin requirements, often 50-75% or higher. This discourages excessive concentration in margin accounts.
- **Long margin formula:** Maintenance call triggered when equity / market value < maintenance requirement, where account equity = market value - debit balance. Equivalently, a call is triggered when market value falls to: debit balance / (1 - maintenance requirement). The call amount due is (maintenance requirement × market value) - equity.
- **Short margin requirements:** Short positions require initial margin of 50% (Reg T) and maintenance of 30% of market value (FINRA minimum). Short account equity = credit balance - market value of short securities. A short squeeze (rising prices) increases the maintenance requirement.
- **Options margin:** Options strategies have specific margin requirements under FINRA Rule 4210 and exchange rules. Covered calls require no additional margin (shares serve as collateral). Naked short options require substantial margin — typically the greater of: (a) option premium + 20% of underlying value - out-of-the-money amount, or (b) option premium + 10% of underlying value. Spreads have defined-risk margin equal to the maximum loss.

### Portfolio Margin
A risk-based margining methodology that can significantly reduce margin requirements for hedged or diversified portfolios:

- **Methodology:** Uses the Options Clearing Corporation's Theoretical Intermarket Margin System (OCC TIMS) to compute margin based on the theoretical maximum loss of the portfolio under a range of stress scenarios, rather than applying fixed percentage requirements to each position independently.
- **Eligibility requirements:** Minimum account equity of $100,000 (FINRA Rule 4210(g)), options trading approval (typically Level 3 or 4), and the firm may impose additional requirements such as minimum net worth, trading experience, or completion of a portfolio margin agreement.
- **Stress test scenarios:** The OCC TIMS model evaluates portfolio profit and loss under standardized moves:
  - Large-cap equities: +/- 15% (with intermediate points at +/- 5%, +/- 10%)
  - Small-cap equities: +/- 10% higher stress (effectively +/- 25%)
  - Broad market indices: +/- 8% to +/- 15%
  - High-volatility securities: firm-specific add-ons
  - The largest theoretical loss across all scenarios becomes the margin requirement
- **Portfolio margin vs Reg T comparison:** A hedged equity portfolio with offsetting options positions might require 50% margin under Reg T (applied position-by-position) but only 10-20% under portfolio margin (reflecting the actual net risk). Conversely, a concentrated, unhedged portfolio may see little benefit from portfolio margin.
- **Benefits:** More efficient use of capital, margin requirements that reflect actual portfolio risk, ability to maintain larger or more complex positions, and alignment between margin and true economic risk.
- **Risks:** Lower margin requirements increase leverage, amplifying both gains and losses. A sudden correlation shift or gap move can produce losses exceeding the stress test scenarios. Portfolio margin accounts can experience rapid, severe margin calls during market dislocations.

### Margin Call Types
Multiple types of margin calls can arise, each with distinct triggers, deadlines, and resolution procedures:

- **Reg T initial call (federal call):** Triggered when a client purchases marginable securities and the account does not have sufficient equity to satisfy the 50% Reg T requirement. Must be met by settlement date (T+1 for most securities). Met by depositing cash or fully paid marginable securities. Failure to meet triggers liquidation and potential 90-day account restriction.
- **Maintenance margin call (house call):** Triggered when account equity falls below the firm's house maintenance requirement (typically 30-40%). The client is typically given T+5 business days (or less, at the firm's discretion) to deposit funds or securities, or the firm will liquidate positions. Unlike Reg T calls, there is no SRO extension mechanism for house calls — the timeline is at the firm's discretion.
- **Exchange minimum call:** Triggered when account equity falls below the FINRA/exchange minimum of 25%. These calls demand immediate attention and may be subject to same-day or next-day resolution.
- **Day-trade call:** Triggered when a pattern day trader's account equity falls below the $25,000 minimum or when day-trade buying power is exceeded. Must be met within 5 business days. Failure restricts the account to cash-available trading.
- **Concentration call:** Triggered when a single position exceeds the firm's concentration threshold and the account's equity is insufficient to meet the elevated requirement. Common in accounts holding large positions in a single stock.

### Margin Call Procedures
The end-to-end process from call generation through resolution:

- **Call generation:** Margin calls are generated during the end-of-day mark-to-market process. The firm's margin system reprices all positions at closing market values, recalculates equity and margin requirements, and identifies accounts in deficit. Intraday monitoring may generate real-time alerts for large deficits.
- **Notification requirements:** FINRA requires prompt notification to the customer. Firms typically notify via multiple channels: automated system alerts, email, phone calls from the margin department. Written notification must document the call amount, the positions involved, and the deadline for resolution.
- **Client communication:** The margin department communicates the amount due, the deadline, and the options available: deposit cash, deposit marginable securities, liquidate positions, or some combination. Best practice is to confirm the client's intentions in writing.
- **Call resolution tracking:** The margin system tracks each open call, the deadline, any partial payments received, and escalation status. Calls are resolved when equity is restored to or above the required level.
- **Extension requests:** For Reg T calls, the firm may request an extension from its designated examining authority (DEA) or SRO — typically 1-5 business days. Extensions are not automatic and are granted based on the circumstances (e.g., pending settlement of a sale, wire transfer in process). Repeated extension requests for the same account may trigger regulatory scrutiny.
- **Automatic liquidation triggers:** If the call is not met by the deadline and no extension is granted, the firm is obligated to liquidate sufficient positions to bring the account into compliance. Many firms have automated systems that initiate liquidation at a specified time on the deadline day.
- **Partial call satisfaction:** A client may partially satisfy a call through a combination of deposits and sales. The margin system must track partial payments and recalculate the remaining call amount after each action.

### Forced Liquidation
When a margin call is not met, the broker-dealer must liquidate positions to bring the account into compliance:

- **Liquidation waterfall:** Firms establish a priority order for which positions to liquidate first. A common waterfall:
  1. Fully paid (non-margin) positions with no tax consequences if available for transfer
  2. Positions specifically identified by the client (if communicated in time)
  3. Most liquid positions (highest average daily volume, tightest bid-ask spreads)
  4. Positions with the lowest unrealized gain or highest unrealized loss (minimizing tax impact where feasible)
  5. Concentrated positions contributing most to the margin deficit
  6. Least liquid positions as a last resort
- **Liquidation priority rules:** The firm has discretion over which positions to liquidate and is not required to follow client preferences, though best practice is to accommodate client requests when operationally feasible. The firm's primary obligation is to reduce the margin deficit.
- **Client notification:** The firm should notify the client before or promptly after liquidation, though FINRA does not require prior consent for liquidation of margin-deficient accounts. The client cannot prevent the firm from liquidating.
- **Best execution in liquidation:** Forced liquidation must still comply with best execution obligations. Orders should be routed to obtain the best reasonably available price, even under time pressure. Market orders in illiquid securities during forced liquidation can create adverse price impact.
- **Restricted account status:** An account that fails to meet a Reg T call may be restricted for 90 days, during which the client must fully prepay any purchases (no margin extension). Subsequent violations may result in longer restrictions or account closure.
- **Close-out obligations:** Under SEC Rule 15c3-3 and SRO rules, the firm must close out fail-to-deliver positions within specified timeframes. Margin liquidation must be completed promptly, and any resulting short positions or failed deliveries must be resolved per regulatory requirements.

### Securities-Backed Lines of Credit (SBLOC)
Lending products that use an investment portfolio as collateral, distinct from traditional margin lending:

- **Non-purpose loans vs purpose loans:** An SBLOC is typically a non-purpose loan — the proceeds may be used for any purpose except purchasing, carrying, or trading securities. This distinction matters because non-purpose loans are governed by Regulation U (for banks) or Regulation T (for broker-dealers), with different requirements depending on the lender type.
- **Collateral requirements:** The investment portfolio secures the loan. Lenders apply loan-to-value (LTV) ratios to determine borrowing capacity:
  - Equities (large-cap, diversified): 50-70% LTV
  - Fixed income (investment grade): 70-90% LTV
  - Mutual funds/ETFs (broad market): 50-75% LTV
  - Cash and money market: 90-95% LTV
  - Concentrated single-stock positions: 30-50% LTV (reduced due to specific risk)
  - Alternative investments, restricted stock, penny stocks: 0% LTV (not accepted as collateral)
- **Concentration limits:** Lenders limit the percentage of the collateral portfolio that can be in a single security (typically 40-60% maximum). Positions exceeding the concentration limit receive reduced or zero LTV on the excess.
- **Maintenance and call procedures:** Similar to margin accounts, SBLOC facilities have maintenance requirements. If the portfolio value declines such that the LTV exceeds the maintenance threshold, the lender issues a collateral call. The borrower must deposit additional collateral, repay part of the loan, or face liquidation of the pledged portfolio.
- **Regulatory considerations:** Banks offering SBLOCs are subject to Regulation U (Fed), which imposes a 50% maximum LTV for purpose loans but has no specific LTV limit for non-purpose loans — the bank applies its own underwriting standards. Broker-dealers offering similar credit are subject to Regulation T. The distinction between purpose and non-purpose must be documented (Form U-1 for banks, Form T-4 for broker-dealers).
- **Risks to the borrower:** Portfolio declines can trigger collateral calls; forced liquidation of securities may occur at unfavorable prices and create taxable events; the interest rate is typically variable (prime + spread); and the borrower retains full investment risk on the pledged portfolio while adding debt service obligations.

### Margin Risk Management
Ongoing monitoring and management of margin-related risks across the firm and client accounts:

- **Portfolio-level margin monitoring:** The firm's risk management system continuously monitors aggregate margin exposure, identifying accounts approaching margin call thresholds, concentrated positions, and correlated risks across the client base. Real-time intraday monitoring supplements end-of-day calculations. FINRA Rule 4521 requires member firms to report aggregate margin balances and related data to FINRA.
- **Stress testing margin requirements:** The firm should stress test margin exposure under adverse scenarios — market declines of 10-20%, sector-specific shocks, volatility spikes, and correlation breakdowns. Stress tests reveal accounts and portfolios that would face large margin calls under stressed conditions.
- **Concentrated position risk:** Positions that represent a large percentage of account value or a large percentage of a security's outstanding shares create elevated margin risk. Firms typically impose higher margin requirements and may impose position limits or require diversification plans.
- **Margin impact on investment returns:** Margin amplifies both gains and losses — return on equity = (portfolio return × leverage) - (interest rate × (leverage - 1)). A 50% margin (2:1 leverage) doubles the percentage gain or loss:
  - Unleveraged: $100K invested, market +10% = $10K gain (10% return)
  - Leveraged at 2:1: $200K invested with $100K equity, market +10% = $20K gain minus interest = ~18% return on equity
  - Leveraged at 2:1: $200K invested with $100K equity, market -10% = $20K loss plus interest = ~-22% return on equity
- **Interest rate calculation on margin debit balances:** Margin interest is calculated daily on the outstanding debit balance:
  - Daily interest = debit balance x (annual rate / 360)
  - Interest is typically charged monthly (sum of daily accruals)
  - Rates are tiered by debit balance size: larger balances receive lower rates
  - Illustrative rate schedule: <$25K = broker call rate + 1.5%; $25K-$100K = call rate + 1.0%; >$100K = call rate + 0.5% (spreads and the call rate itself vary by firm and rate environment)
- **Tax treatment of margin interest:** Margin interest is deductible as investment interest expense on Schedule A (Form 1040), but only up to the amount of net investment income. Excess margin interest can be carried forward. Investment interest does not include qualified dividends or long-term capital gains unless the taxpayer elects to treat them as ordinary income. This deduction requires itemizing.

## Worked Examples

Three worked examples are in [references/examples.md](references/examples.md) — load for an end-to-end scenario: (1) calculating margin requirements and buying power for a new diversified account, (2) managing a margin call sequence from generation through resolution, (3) evaluating portfolio margin vs Reg T for an active options trader.

## Common Pitfalls
- Confusing SMA with account equity — SMA is a high-water mark that does not decline with market value drops, leading clients to believe they have more cushion than they do
- Failing to account for margin interest as a drag on returns — at the 7-8% margin rates typical of recent rate environments, the hurdle rate for margined positions is substantial
- Relying on Reg T buying power without monitoring maintenance levels — a position can be purchased within buying power but quickly trigger a maintenance call after a decline
- Assuming portfolio margin is always more favorable — concentrated, unhedged positions may receive similar or higher margin under portfolio margin stress tests
- Not planning for margin call deadlines — margin calls arrive during market stress when the client is least likely to have available cash
- Treating SBLOC as "free" liquidity — a market decline can trigger a collateral call simultaneously with the investment losses, creating a double impact
- Liquidating positions for margin calls without considering tax consequences — forced sales may realize gains or losses at inopportune times
- Pattern day trader margin surprise — accounts can be reclassified as pattern day trader and face the $25,000 minimum equity requirement unexpectedly
- Ignoring correlation between margin calls and market stress — the client's ability to deposit cash may be impaired at exactly the time a margin call demands it
- Assuming the firm must contact the client before liquidation — the firm has the right to liquidate margin-deficient accounts without prior notice or client consent
- Overlooking the purpose/non-purpose distinction in SBLOCs — using non-purpose loan proceeds to buy securities violates Regulation U and can result in regulatory action

## Cross-References
- **order-lifecycle** (trading-operations): Margin requirements are checked as part of the order validation and pre-trade process
- **trade-execution** (trading-operations): Forced liquidation requires best execution compliance even under time pressure
- **settlement-clearing** (trading-operations): Margin is settled as part of the trade settlement process; fails can trigger margin obligations
- **lending** (wealth-management): SBLOC products overlap with personal lending analysis; HELOC vs SBLOC comparison
- **liquidity-management** (wealth-management): Margin calls create sudden liquidity demands that must be anticipated in cash flow planning
- **pre-trade-compliance** (trading-operations): Pre-trade margin checks prevent orders that would exceed margin capacity
- **operational-risk** (trading-operations): Margin system failures, forced liquidation errors, and call processing breakdowns are key operational risks
- **counterparty-risk** (trading-operations): Margin lending creates counterparty exposure between the firm and the client
- **investment-suitability** (compliance): Margin accounts and leverage strategies require suitability assessment
- **diversification** (wealth-management): Concentrated position margin requirements reinforce diversification principles
