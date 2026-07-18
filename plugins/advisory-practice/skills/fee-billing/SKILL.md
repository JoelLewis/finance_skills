---
name: fee-billing
description: "Build and manage advisory fee billing operations from fee schedule design through calculation, collection, revenue recognition, and compliance disclosure. Use when the user asks about tiered or breakpoint fee schedules, billing cycle configuration, AUM valuation for billing, direct-debit vs invoice collection, GAAP revenue recognition for fees, ADV Part 2A or Reg BI fee disclosure, diagnosing billing exceptions or refunds, migrating from spreadsheet billing to automated systems, or forecasting advisory revenue. Also trigger when users mention 'fee calculation', 'billing engine', 'effective fee rate', 'household billing aggregation', 'mid-period adjustment', 'billing in advance vs arrears', 'fee compression', or 'ERISA 408(b)(2)'."
---

# Fee Billing

## Core Concepts

### 1. Fee Schedule Structures

Advisory firms employ a range of fee structures, often combining several within a single practice.

**Flat Fee (Fixed Dollar).** A predetermined dollar amount charged per period regardless of account size. Common for financial planning engagements or retainer-based advice. Straightforward to bill but disconnected from asset growth.

**AUM-Based (Percentage of Assets).** The most prevalent model for registered investment advisers. A single percentage (e.g., 1.00%) is applied to the market value of managed assets. Simple to communicate but can become expensive for large portfolios and cheap for small ones.

**Tiered / Breakpoint (Declining Rate).** A graduated schedule where successive tiers of assets are billed at progressively lower rates. For example:

| Tier | AUM Range | Annual Rate |
|------|-----------|-------------|
| 1 | First $500,000 | 1.00% |
| 2 | Next $500,000 | 0.80% |
| 3 | Next $1,000,000 | 0.60% |
| 4 | Over $2,000,000 | 0.40% |

Under a true tiered schedule each dollar is billed at the rate for the tier it falls within. Under a breakpoint schedule the entire balance is billed at the rate corresponding to the highest tier reached. The distinction matters significantly for large accounts and must be clearly defined in the advisory agreement.

**Flat-Plus-AUM Hybrid.** Combines a fixed planning fee with a lower AUM percentage. Useful for firms that want to be compensated for planning work independently of portfolio size.

**Hourly.** Charges based on advisor time. Rarely used as the sole billing method for ongoing relationships but common for project-based planning engagements.

**Financial Planning Fees.** One-time or recurring fees for plan creation and updates, often billed separately from investment management fees.

**Performance-Based Fees.** Permitted only for "qualified clients" under SEC Rule 205-3. Under the SEC's 2026 inflation adjustment (order issued April 2026, effective June 29, 2026), a qualified client must have at least $1.4 million in AUM with the adviser or a net worth exceeding $2.7 million — up from the $1.1 million / $2.2 million thresholds set in 2021. The SEC adjusts these thresholds for inflation every five years, and prior thresholds generally continue to apply to pre-existing contracts; verify current values. Requires a high-water mark or similar mechanism to prevent double-charging after drawdowns. Rarely used by typical RIAs due to complexity and regulatory constraints.

**Family / Household Billing Aggregation.** Assets across related accounts (spouses, trusts, custodial accounts, IRAs) are combined for fee-tier determination, then the calculated fee is allocated back to individual accounts. This gives the household the benefit of breakpoint pricing. The aggregation definition (who qualifies as "household") must be documented in the advisory agreement.

### 2. AUM Valuation for Billing

The accuracy and consistency of AUM valuation directly determines billing accuracy.

**Valuation Date Selection.** The most common approaches are:
- **Quarter-end value:** Assets valued as of the last business day of the billing quarter. Simple and widely used.
- **Prior quarter-end value:** Assets valued as of the end of the preceding quarter. Avoids billing on unrealized gains or losses that occurred during the period just ended. Common for advance billing.
- **Period average:** The average of daily or month-end values across the billing period. Smooths volatility but is operationally complex.

**Market Value vs. Cost Basis.** Nearly all advisory agreements specify market value. Cost basis would understate the true value being managed and is almost never used.

**Held-Away Assets.** Assets the adviser monitors but that are not custodied at the primary custodian (e.g., 401(k) plans, outside brokerage accounts, annuities). Whether these are included in the billable AUM depends on the advisory agreement. If included, obtaining timely and accurate valuations is a persistent operational challenge.

**Accrued Income.** Bond accrued interest and declared but unpaid dividends may be included or excluded. Most custodian feeds include accrued interest in the total market value, so the default is typically inclusion unless the fee schedule specifies otherwise.

**Margin Debit Treatment.** If a client uses margin, the question arises whether to bill on gross assets or net equity. The advisory agreement should specify. Most firms bill on net equity (gross market value minus margin balance).

**Cash Inclusion / Exclusion.** Some agreements exclude cash or money market positions from billable AUM, particularly if the adviser is not actively managing those balances. This is uncommon but must be handled when present.

**New Account Proration.** Accounts opened mid-period require proration. The standard method is to calculate the fee based on the number of days the account was open relative to the total days in the billing period. Some firms use a simpler approach and bill for the partial quarter only if the account was opened before the midpoint of the period.

### 3. Billing Cycle Mechanics

**Quarterly Billing.** The dominant cycle for RIAs. Billing quarters typically align with calendar quarters (Jan-Mar, Apr-Jun, Jul-Sep, Oct-Dec), though some firms use fiscal quarters.

**Monthly Billing.** Less common for investment management but used for financial planning retainers or firms that want to smooth revenue. Requires more operational overhead.

**Annual Billing.** Occasionally used for flat-fee or financial-planning-only arrangements. May be billed as a single payment or split into installments.

**Advance vs. Arrears Billing.**
- **Advance (in advance):** Fees are billed at the start of the period for services to be rendered. Creates a deferred revenue liability on the firm's balance sheet. Requires refund calculation for accounts terminated mid-period. Most common for RIAs.
- **Arrears (in arrears):** Fees are billed at the end of the period for services already rendered. Simpler from a revenue-recognition standpoint (revenue is earned when billed) but delays cash collection. Growing in popularity due to its alignment with the service delivery timeline.

**Pro-Ration Rules.** Events requiring proration include:
- Account openings mid-period
- Account closings or terminations mid-period
- Large contributions (some firms apply a materiality threshold, e.g., only prorate for contributions exceeding $10,000 or 10% of account value)
- Large withdrawals (same materiality threshold logic)
- Transfers between accounts within the same household (should be revenue-neutral)

The standard proration formula is:

```
Prorated Fee = Full-Period Fee * (Days in Period Account Was Active / Total Days in Period)
```

**Billing Period Alignment.** When a firm converts billing cycles (e.g., from quarterly to monthly), a transition period is needed. Clients should not be double-billed or under-billed during the switch. A reconciliation calculation comparing what was billed under the old cycle against what is owed under the new cycle is essential.

### 4. Fee Calculation Engine

A systematic fee calculation follows these steps:

**Step 1: Determine Household Composition.** Identify all accounts linked to the billing household. Include all account types per the advisory agreement (individual, joint, IRA, Roth IRA, trust, UGMA/UTMA, entity accounts).

**Step 2: Retrieve Account Valuations.** Pull market values as of the valuation date from the custodian or portfolio management system. Apply any exclusions (cash exclusion, held-away asset inclusion, margin debit netting).

**Step 3: Aggregate Household AUM.** Sum the billable market values across all accounts in the household to determine the household-level AUM for tier determination.

**Step 4: Apply Fee Schedule.** Using the household's assigned fee schedule, calculate the annual fee. For a tiered schedule:

```
Household AUM: $1,800,000
Tier 1: $500,000 * 1.00% = $5,000
Tier 2: $500,000 * 0.80% = $4,000
Tier 3: $800,000 * 0.60% = $4,800
Annual Fee: $13,800
Effective Rate: 0.767%
```

**Step 5: Convert to Billing Period.** Divide the annual fee by the number of billing periods (4 for quarterly, 12 for monthly).

```
Quarterly Fee: $13,800 / 4 = $3,450
```

**Step 6: Apply Overrides and Adjustments.** Check for negotiated rate overrides, minimum fee floors, fee caps, waivers, or credits. Apply in the correct order (typically: calculate standard fee, then apply negotiated rate, then apply minimum, then apply cap, then apply waivers).

**Step 7: Allocate to Accounts.** Distribute the household fee across individual accounts, typically pro-rata by market value:

```
Account A ($900,000 / $1,800,000) = 50% * $3,450 = $1,725.00
Account B ($500,000 / $1,800,000) = 27.78% * $3,450 = $958.33
Account C ($400,000 / $1,800,000) = 22.22% * $3,450 = $766.67
```

**Step 8: Apply Proration.** For any accounts opened or closed mid-period, prorate the allocated fee.

**Step 9: Rounding.** Apply consistent rounding rules (typically round to the nearest cent). Ensure rounding differences are allocated to a designated account (usually the largest) so the sum of account-level fees equals the household fee exactly.

**Step 10: Generate Billing Output.** Produce the custodian debit instruction file or invoice, the billing detail report, and the audit trail record.

**Minimum Fee Application.** Many firms set a minimum quarterly or annual fee (e.g., $250/quarter). If the calculated fee falls below the minimum, the minimum is charged instead. This should be applied at the household level, not the account level.

**Fee Cap Application.** Less common but sometimes offered to attract large accounts. A cap ensures the dollar fee does not exceed a maximum regardless of AUM growth.

**Negotiated Rate Overrides.** Individual clients or households may have rates that differ from the published fee schedule. The billing system must support per-household or per-account rate overrides while maintaining an audit trail of who authorized the deviation and when.

**Rounding Rules.** Define and document the rounding convention. Typical practice rounds each account fee to the nearest cent. Allocate any remainder (positive or negative) from rounding to the largest account in the household.

### 5. Collection Methods

**Direct Debit from Custodian Account.** The most common method for RIAs. The adviser sends fee debit instructions to the custodian (Schwab, Fidelity, Pershing, etc.), and the custodian debits the client's account directly. Requires:
- Written authorization in the advisory agreement or a separate billing authorization form
- Custodian-specific file format (varies by custodian; typically CSV or fixed-width)
- Submission within the custodian's billing window (often the first 10-15 business days of the quarter)
- The custodian sends a statement to the client showing the fee deduction, providing a layer of independent oversight

**Invoice Billing.** The adviser sends an invoice and the client pays by check, wire, or ACH. More common for institutional clients, financial planning fees, or clients who prefer not to authorize direct debits. Increases accounts receivable management burden.

**Split Billing Across Accounts.** When a household has multiple accounts, the fee can be debited from each account in proportion to its share of the household AUM (the most common approach) or debited entirely from one designated account.

**Billing from Specific Accounts.** Some clients designate a specific account for fee payment. Common when clients prefer fees to come from a taxable account (for potential tax deductibility) rather than a retirement account.

**Tax-Advantaged Account Billing Considerations.** Fees can be debited from IRAs and other tax-advantaged accounts, but there are considerations:
- IRA fee debits are not treated as distributions if the fee is for investment management of the IRA assets
- If the fee covers services beyond the IRA (e.g., financial planning for the household), the debit may be treated as a distribution
- Some practitioners recommend paying fees from taxable accounts when possible because the fee payment from an IRA reduces the tax-advantaged balance, whereas paying from a taxable account may be deductible (subject to limitations)
- ERISA plan accounts have additional rules under DOL guidance

**Third-Party Billing.** When the adviser bills through a TAMP (Turnkey Asset Management Platform) or sub-advisory arrangement, the TAMP may handle billing and remit the adviser's share. The adviser must reconcile the revenue received against the expected calculation.

### 6. Billing Exceptions and Adjustments

**Fee Waivers.** Common categories include:
- Employee and employee-family accounts (full or partial waiver)
- Charitable organization accounts (reduced rate or full waiver)
- Pro bono or scholarship accounts
- Accounts below a size threshold during an initial ramp-up period

All waivers should be documented with authorization and expiration (if applicable).

**Negotiated Rates.** Large clients or those with longstanding relationships may receive custom rates below the standard schedule. The billing system must store the effective date, the negotiated schedule, and the approving authority.

**Legacy Fee Schedules.** When a firm updates its published fee schedule, existing clients may be grandfathered on the old schedule. The billing system must support multiple active fee schedules concurrently. Over time, legacy schedules create operational complexity and should be periodically reviewed for consolidation.

**Retroactive Adjustments.** Occur when an error is discovered after billing has been processed. The adjustment should be applied in the next billing cycle (credit or additional debit) with clear documentation of the original error, the corrected calculation, and the net adjustment.

**Billing Disputes.** When a client disputes a fee, the process should include:
1. Immediate acknowledgment of the dispute
2. Detailed recalculation and documentation
3. Resolution within a defined timeframe (e.g., 30 days)
4. If the client is correct, issue a credit or refund
5. Maintain a dispute log for compliance review

**Refunds for Terminated Accounts.** For advance-billed accounts, calculate the unearned portion of the fee from the termination date through the end of the billing period and issue a refund. The advisory agreement should specify the refund methodology.

```
Refund = Quarterly Fee * (Remaining Days / Total Days in Quarter)
```

**Fee Reversals.** Full reversal of a fee debit at the custodian level. Typically used when a billing error is caught within the custodian's reversal window (often same-day or next-day). After the reversal window, the correction must be handled as a retroactive adjustment.

### 7. Revenue Recognition

**GAAP Treatment: Advance Billing.** When fees are billed at the start of a quarter, the firm recognizes a liability (deferred revenue or unearned fees) at the billing date. Revenue is then recognized ratably over the service period (the quarter). At the end of the quarter, all deferred revenue for that period has been earned and recognized.

**GAAP Treatment: Arrears Billing.** Revenue accrues over the service period. At the end of each month within the quarter, the firm recognizes one-third of the estimated quarterly fee as accrued revenue. When the fee is billed and collected at quarter-end, the accrual is reversed and replaced with recognized revenue.

**Revenue Per Client Metrics.** Key metrics include:
- Average revenue per household
- Average revenue per account
- Revenue per advisor
- Effective fee rate (total fees / total AUM) as a blended measure

**Revenue Concentration Analysis.** Regulators and business prudence demand awareness of concentration risk. If a single client or small group of clients represents a disproportionate share of revenue, the firm faces business risk. Common thresholds to monitor: no single household should exceed 5-10% of total revenue.

**Revenue Forecasting.** Forecast advisory revenue using:
- Current AUM multiplied by the blended effective fee rate
- Adjust for expected market appreciation or depreciation
- Adjust for expected net new assets (organic growth) or attrition
- Adjust for known fee schedule changes or renegotiations
- Sensitivity analysis across bull, base, and bear market scenarios

### 8. Compliance and Disclosure

**ADV Part 2A (Brochure) Fee Disclosure.** Item 5 of Form ADV Part 2A requires clear disclosure of:
- Fee schedules and how fees are calculated
- Whether fees are negotiable
- Billing frequency and collection method
- Whether fees are billed in advance or arrears
- Refund policy for terminated accounts
- Other costs clients may bear (custodian transaction fees, fund expenses, etc.)

The disclosure must be sufficiently detailed that a client can understand the total cost of the advisory relationship.

**Fee-on-Fee Issues.** When an adviser charges an AUM-based fee on a portfolio that includes mutual funds or ETFs, the client pays both the advisory fee and the underlying fund expense ratio. This "fee on a fee" must be disclosed. Some advisers offset the fund expenses against the advisory fee or use the lowest-cost share classes available to mitigate this concern.

**Total Cost of Ownership Disclosure.** Best practice (and increasingly expected by regulators) is to present the client with a comprehensive view of all costs: advisory fees, fund expenses, custodian fees, transaction costs, and any other charges. This aligns with the SEC's guidance on adviser fiduciary duty.

**Regulation Best Interest (Reg BI) Cost Considerations.** For dual-registrant firms, Reg BI requires disclosure of material fees and costs and their impact on the client's investment. The cost comparison between advisory and brokerage accounts is a key element.

**ERISA 408(b)(2) Fee Disclosure.** For advisers serving retirement plans, ERISA Section 408(b)(2) requires detailed disclosure of all direct and indirect compensation received in connection with plan services. The disclosure must be provided before the engagement begins and updated within 60 days of any change.

**Fee Reasonableness Documentation.** Advisers should maintain documentation supporting the reasonableness of their fees. This includes periodic benchmarking against industry surveys (e.g., the annual RIA benchmarking studies from Schwab, Fidelity, or InvestmentNews), documentation of the services provided for the fee, and consideration of the client's total cost.

### 9. Billing System Architecture

**Core Components:**

- **Fee Schedule Repository.** A database of all fee schedules (standard and negotiated), including effective dates, tier structures, and associated metadata. Must support versioning so historical calculations can be recreated.

- **Account/Household Master.** Links accounts to billing households, assigns fee schedules, stores billing preferences (collection method, billing account designation, proration rules).

- **Valuation Engine.** Retrieves or calculates account market values as of the billing date. Sources include custodian position files, portfolio management systems, and manual entries for held-away assets.

- **Calculation Engine.** The core logic that executes the ten-step process described in Section 4. Must handle all fee schedule types, proration, overrides, minimums, caps, and rounding.

- **Custodian Debit Instruction Generator.** Produces the custodian-specific file format for fee debits. Each custodian (Schwab, Fidelity, Pershing, TD Ameritrade legacy, etc.) has its own format requirements, submission deadlines, and reversal procedures.

- **Invoice Generator.** For clients billed by invoice, produces statements with fee detail.

**Integration Points:**

- **Portfolio Management System (PMS).** The billing system pulls valuations and account structure from the PMS. In some platforms (e.g., Orion, Black Diamond, Tamarac), the billing engine is integrated into the PMS.
- **Custodian.** Bidirectional: the billing system sends debit instructions to the custodian and receives confirmation (or rejection) files back.
- **CRM.** Fee schedule assignments and negotiated rates may be managed in the CRM and synchronized to the billing system.
- **Accounting System.** Billing output feeds revenue entries in the firm's general ledger.

**Billing Preview and Approval Workflow.**
1. The billing engine runs in preview mode, producing a billing preview report.
2. Operations staff review the preview for anomalies (unusually large fees, negative fees, zero-dollar fees, fees that deviate significantly from the prior period).
3. Exceptions are investigated and resolved.
4. An authorized person approves the billing run.
5. The engine generates the final debit instructions or invoices.
6. Instructions are submitted to custodians.

**Audit Trail.** Every billing run must produce a complete audit trail including:
- Valuation date and source
- Fee schedule applied (with version identifier)
- Household AUM and per-account AUM
- Step-by-step calculation detail
- Any overrides, waivers, or adjustments applied
- The identity of the person who approved the billing run
- Timestamp of submission to the custodian

**Billing Reports.** Standard reports include:
- Billing summary by household (fee, effective rate, AUM)
- Billing detail by account
- Period-over-period comparison (fee change from prior quarter)
- Exception report (new accounts, terminated accounts, large variances)
- Revenue summary by advisor, team, or branch
- Accounts receivable aging (for invoice-billed clients)

## Worked Examples

See [references/examples.md](references/examples.md) for three end-to-end worked examples — a quarterly tiered-fee calculation for a five-account household, mid-quarter proration for contributions/transfers/terminations, and a spreadsheet-to-automated billing migration. Load it when the user needs a full numerical walkthrough.

## Common Pitfalls

- **Confusing tiered and breakpoint pricing.** A tiered schedule charges each dollar at the rate for its tier. A breakpoint schedule charges the entire balance at the rate for the highest tier reached. Mixing these up leads to significant billing errors, especially for large accounts.
- **Failing to prorate for mid-period events.** Not adjusting fees for material contributions, withdrawals, or account openings/closings results in overbilling or underbilling and invites client complaints.
- **Ignoring rounding allocation.** When per-account fees are rounded independently, the sum may not equal the household fee. Without a systematic rounding allocation, small discrepancies accumulate and create reconciliation headaches.
- **Billing retirement accounts for non-retirement services.** Debiting an IRA for advisory fees that cover financial planning or services unrelated to the IRA assets can trigger a taxable distribution. Always confirm that fees debited from tax-advantaged accounts correspond to services for those accounts.
- **Neglecting to update negotiated rates.** When a fee schedule is updated but negotiated rate clients are forgotten, those clients may continue paying outdated rates indefinitely. Maintain a review cadence for all non-standard arrangements.
- **Inadequate disclosure of fee-on-fee costs.** Failing to disclose that clients pay both the advisory fee and underlying fund expenses is a recurring SEC examination finding. Ensure ADV Part 2A and client communications address total cost clearly.
- **Missing the custodian billing window.** Each custodian has a defined window for accepting fee debit instructions. Missing the window delays fee collection by an entire quarter and disrupts cash flow.
- **Not reconciling custodian confirmations.** After submitting debit instructions, the custodian returns a confirmation file indicating which debits were processed and which were rejected (insufficient funds, account closed, etc.). Failing to review this file means rejected debits go uncollected.
- **Advance-billing refund errors on termination.** When an advance-billed account terminates mid-quarter, the firm owes a prorated refund. Incorrect day-count calculations or failing to issue the refund entirely creates compliance risk and client ill will.
- **Overcomplicating household definitions.** Overly broad household aggregation (e.g., including extended family members who are not part of the advisory relationship) can inflate tier benefits. Overly narrow definitions deprive clients of legitimate aggregation. The definition must match the advisory agreement.
- **Lack of billing audit trail.** Without a detailed record of every calculation input and output, the firm cannot defend its billing in the event of a client dispute or regulatory examination.
- **Revenue recognition timing errors.** Recognizing advance-billed fees as revenue immediately rather than deferring and recognizing ratably overstates revenue in the billing period and understates it in subsequent periods.

## Cross-References

- **fee-disclosure** (compliance plugin) — Detailed requirements for fee disclosure in client-facing documents and regulatory filings.
- **portfolio-management-systems** (advisory-practice plugin) — Integration between billing engines and PMS platforms for valuation and account data.
- **advisor-dashboards** (advisory-practice plugin) — Revenue metrics, billing status, and fee analytics displayed on advisor-facing dashboards.
- **client-reporting-delivery** (advisory-practice plugin) — Inclusion of fee summaries and performance-net-of-fee figures in client reports.
- **investment-policy** (wealth-management plugin) — Fee schedule terms as specified in the investment policy statement or advisory agreement.
- **reg-bi** (compliance plugin) — Regulation Best Interest cost disclosure obligations for dual-registrant firms.
- **fiduciary-standards** (compliance plugin) — Fiduciary duty to charge reasonable fees and act in the client's best interest regarding cost.
- **tax-efficiency** (wealth-management plugin) — Tax implications of fee payment source (taxable vs. tax-advantaged accounts) and deductibility considerations.
- **performance-reporting** (wealth-management plugin) — Gross-of-fee vs. net-of-fee performance calculation and the role of accurate fee data.
