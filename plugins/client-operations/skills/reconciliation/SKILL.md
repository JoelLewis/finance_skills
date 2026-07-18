---
name: reconciliation
description: "Design and operate reconciliation processes across portfolio management, custodian, and clearing systems. Use when building a daily position, cash, or transaction reconciliation process, investigating discrepancies between internal records and custodian records, diagnosing recurring break patterns from corporate actions or pricing differences, setting tolerance thresholds for position, cash, or market value matching, implementing three-way reconciliation, designing break investigation workflows with aging and escalation, normalizing multi-custodian feeds from Schwab, Fidelity, or Pershing, reconciling cost basis or accrued income, or preparing for examinations on books and records accuracy."
---

# Reconciliation

## Core Concepts

### 1. Reconciliation Types and Hierarchy

Reconciliation is the systematic comparison of records across two or more systems to identify and resolve discrepancies. In securities operations, reconciliation ensures that the firm's internal records (the investment book of record, or IBOR) match the custodian's official records (the official book of record, or OBOR) and, where applicable, the clearing firm's records. The reconciliation hierarchy proceeds from the most fundamental data element (positions) through increasingly derived data elements.

**Position Reconciliation.** The foundational reconciliation. Compares the number of shares or units held for each security in each account between the firm's portfolio management system (PMS) and the custodian. Position reconciliation is typically zero-tolerance: any share count difference, no matter how small, constitutes a break. Fractional share differences (common with dividend reinvestment plans) must also be identified and resolved. Position reconciliation is performed daily, using end-of-day files from the custodian compared against the PMS position ledger.

**Cash Reconciliation.** Compares cash balances between the PMS and the custodian, accounting for settled cash, pending settlements, accrued income, and pending fee debits. Cash reconciliation is more nuanced than position reconciliation because timing differences are inherent — a trade executed on day T settles on T+1, and the PMS and custodian may record the cash impact on different dates. Cash tolerance thresholds are common, typically a small dollar amount (e.g., $0.50 to $5.00) to accommodate rounding differences across systems. Balances outside the tolerance require investigation.

**Transaction Reconciliation.** Compares individual transactions (trades, dividends, interest payments, transfers, fees) recorded in the PMS against the custodian's transaction ledger. Transaction reconciliation operates at the trade level, matching on security, quantity, price, trade date, and settlement date. Unmatched transactions on either side constitute breaks. Transaction reconciliation is typically performed on a T+1 basis — comparing yesterday's activity after the custodian's end-of-day file is received.

**Market Value Reconciliation.** Compares the total market value of each position and each account between systems. Market value breaks often result from pricing differences — the PMS and custodian may source prices from different vendors or apply different pricing hierarchies for thinly traded or illiquid securities. Market value tolerance is typically expressed in basis points (e.g., 5-10 bps of account value) rather than absolute dollars, because a $100 difference on a $50,000 account is more significant than a $100 difference on a $5,000,000 account.

**Accrued Income Reconciliation.** Compares accrued interest on fixed-income holdings and declared-but-unpaid dividends. Accrued income differences frequently arise from day-count convention differences (actual/actual vs. 30/360), ex-date vs. record-date timing, or different treatment of defaulted bonds. This reconciliation is particularly important for fixed-income-heavy portfolios where accrued income is a material component of total value.

**Cost Basis Reconciliation.** Compares the tax lot-level cost basis for each position between the PMS and the custodian. Cost basis discrepancies are among the most difficult to resolve because they may originate from historical corporate actions (splits, mergers, spin-offs, return of capital adjustments) that were processed differently in each system. Since the custodian reports cost basis to the IRS on Form 1099-B, cost basis discrepancies can result in incorrect tax reporting if not resolved. Cost basis reconciliation is typically performed less frequently than position reconciliation — monthly or quarterly — but with zero tolerance for discrepancies.

### 2. Three-Way Reconciliation

For advisory firms that use a portfolio management system separate from both the custodian and any clearing firm, three-way reconciliation is the standard of practice. The three records being compared are:

**Advisor System (PMS / Portfolio Accounting).** The firm's investment book of record (IBOR), maintained in the portfolio management system (Orion, Black Diamond, Tamarac, Addepar, or similar). This is the record the firm uses for performance reporting, billing, rebalancing, and client-facing communications. The advisor system reflects the firm's understanding of what each client owns.

**Custodian Records.** The official book of record (OBOR), maintained by the custodian (Schwab, Fidelity, Pershing, or similar). This is the legally authoritative record of client assets. The custodian is responsible for safekeeping assets, settling transactions, and reporting to the IRS. When the advisor system and custodian disagree, the custodian record is presumed correct unless the firm can demonstrate otherwise.

**Clearing Firm Records.** For firms that clear through a separate entity (introducing broker-dealers that clear through a correspondent clearing firm), the clearing firm maintains its own record of positions and transactions. The clearing firm processes settlements, maintains margin calculations, and generates customer statements. In a fully disclosed arrangement, the clearing firm's records should match the custodian's, but discrepancies can arise from timing, corporate action processing, or data feed errors.

**Authoritative Source by Data Element.** Different systems serve as the authoritative source for different data elements:

| Data Element | Authoritative Source | Reason |
|---|---|---|
| Share/unit count | Custodian | Custodian holds the securities in legal custody |
| Settled cash balance | Custodian | Custodian controls the cash account |
| Trade execution details | Executing broker / custodian | Trade occurred on their platform |
| Cost basis (for tax reporting) | Custodian | Custodian reports 1099-B to IRS |
| Performance returns | Advisor system (PMS) | PMS maintains the calculation methodology |
| Model assignment and drift | Advisor system (PMS) | PMS manages the investment process |
| Fee schedule and billing | Advisor system (PMS) | PMS calculates fees per advisory agreement |
| Corporate action elections | Custodian | Custodian processes the action |

**Reconciliation Frequency.** The standard frequencies are:
- Position reconciliation: daily (end of each business day)
- Cash reconciliation: daily
- Transaction reconciliation: T+1 (one business day after the trade or event)
- Market value reconciliation: daily
- Accrued income reconciliation: daily or weekly, depending on portfolio composition
- Cost basis reconciliation: monthly or quarterly

### 3. Break Identification

A break is any discrepancy identified during reconciliation between two or more records. Break identification is the process of detecting, classifying, and prioritizing breaks for investigation and resolution.

**Tolerance Thresholds.** Not all discrepancies warrant investigation. Tolerance thresholds define the minimum discrepancy that constitutes a reportable break:

| Reconciliation Type | Typical Tolerance | Rationale |
|---|---|---|
| Position (shares/units) | Zero (exact match required) | Any share difference indicates a missing or erroneous transaction |
| Cash balance | $0.50 - $5.00 | Small rounding differences across systems are expected |
| Market value | 5-10 bps of account value | Pricing source differences create small value discrepancies |
| Accrued income | $0.01 - $1.00 | Day-count and rounding conventions vary across systems |
| Cost basis | Zero (exact match required) | Any basis difference affects tax reporting accuracy |
| Transaction matching | Exact match on key fields | Unmatched transactions require investigation |

**Break Categorization.** Breaks are classified by root cause to enable pattern analysis and systemic remediation:

- **Timing differences.** The most common category. Arise when the PMS and custodian record the same event on different dates. Examples: a trade executed late in the day may appear in the PMS on trade date but in the custodian file the following day; a dividend may post in the custodian on the pay date but in the PMS on the record date. Timing breaks typically self-resolve within one to two business days.
- **Pricing differences.** Occur when the PMS and custodian use different pricing sources or apply different pricing hierarchies. Most common for fixed-income securities, international equities (with exchange rate differences), and illiquid or thinly traded securities.
- **Corporate action differences.** Arise when a corporate action (stock split, merger, spin-off, dividend reinvestment) is processed in one system but not the other, or processed with different terms (different exchange ratio, different effective date). Corporate actions are the single largest cause of position breaks that do not self-resolve.
- **Missing transactions.** A transaction appears in one system but not the other. Common causes: a trade placed directly at the custodian without going through the PMS, a manual journal entry in one system, or a data feed failure that dropped a transaction.
- **Duplicate transactions.** The same transaction is recorded twice in one system. Can result from data feed reprocessing, manual entry combined with automated feed, or system errors during corporate action processing.
- **Data quality issues.** Security identifiers do not match across systems (CUSIP changes, ticker symbol changes), account numbers are mapped incorrectly, or data feed parsing errors corrupt field values.

**Break Severity Levels.** Breaks are prioritized based on their operational impact:

- **Critical (must resolve same day).** Position breaks affecting client-facing reporting or imminent billing, cash breaks exceeding a material threshold (e.g., $10,000), and any break that would affect a trade if left unresolved.
- **High (must resolve within two business days).** Position breaks on any actively traded security, market value breaks exceeding the tolerance, and unmatched transactions from the prior day.
- **Medium (must resolve within five business days).** Accrued income differences, cost basis discrepancies identified in periodic reconciliation, and pricing breaks on less liquid securities.
- **Low (resolve within the current monthly cycle).** Minor rounding differences within tolerance, known timing differences expected to self-resolve, and informational discrepancies that do not affect reporting or billing.

### 4. Break Resolution Workflows

Once a break is identified and categorized, it enters a structured resolution workflow. Effective break resolution combines investigative rigor with operational efficiency.

**Investigation Procedures.** The standard investigation sequence for a position break is:

1. Verify the break is not a known timing difference by checking pending transactions and unsettled activity in both systems.
2. Review the transaction history for the affected security in both the PMS and custodian to identify the divergence point — the first date on which the records disagree.
3. Check for unprocessed corporate actions by reviewing the corporate action calendar for the security and confirming that all mandatory actions have been applied in both systems.
4. Check for missing or duplicate trades by comparing the trade blotter in the PMS against the custodian's trade confirmation file for the relevant dates.
5. Verify security identifier mapping — confirm that the CUSIP, ISIN, or ticker symbol in the PMS maps correctly to the custodian's security master.
6. If the cause remains unidentified, submit a custodian inquiry requesting the custodian's transaction history for the security and account over the period in question.

**Common Break Causes and Resolutions.**

| Break Cause | Resolution |
|---|---|
| Unprocessed stock split | Apply the split in the PMS (adjust shares and cost basis) |
| Missed dividend reinvestment | Add the reinvestment transaction in the PMS |
| Trade placed directly at custodian | Enter the trade retroactively in the PMS |
| Data feed failure (dropped transaction) | Re-import the affected date's custodian file |
| Duplicate trade entry | Remove the duplicate from the PMS |
| CUSIP change (corporate action) | Update the security mapping in the PMS |
| Pricing difference | Update the PMS pricing source or override the price |
| Cash posting timing | Confirm the break self-resolves the following day; mark as timing |

**Break Aging and Escalation.** Unresolved breaks must be tracked by age. The aging clock starts on the date the break is first identified. Escalation rules ensure that aging breaks receive management attention:

- 0-2 business days: Operations analyst investigates and resolves.
- 3-5 business days: Escalate to operations supervisor. Supervisor reviews investigation notes and may reassign or provide guidance.
- 6-10 business days: Escalate to operations manager. A written explanation is required for why the break remains open.
- Over 10 business days: Escalate to the chief operations officer or chief compliance officer. Breaks of this age may indicate a systemic issue requiring vendor engagement or system changes.

**Resolution Documentation.** Every resolved break must be documented with: the date the break was identified, the break category, the root cause determination, the corrective action taken, the system in which the correction was made, the date of resolution, and the identity of the person who resolved it. This documentation forms part of the firm's books and records and is subject to regulatory examination.

**Recurring Break Pattern Analysis.** Operations teams should review break data periodically (weekly or monthly) to identify recurring patterns. If the same type of break occurs repeatedly for the same security, account, or data feed, the root cause is likely systemic rather than transactional. Systemic causes require process or system changes, not repeated manual corrections. Examples of systemic patterns: a particular custodian feed consistently drops fractional shares, a specific security type (e.g., foreign ordinaries) always has pricing breaks, or corporate actions for a particular issuer are consistently delayed.

### 5. Reconciliation Automation

Manual reconciliation — comparing records by hand in spreadsheets — is error-prone, time-consuming, and does not scale. Reconciliation automation reduces manual effort, increases accuracy, and enables exception-based processing where human attention is directed only to genuine breaks.

**Automated Matching Engines.** Reconciliation software compares records from two or more sources using configurable matching rules. The matching engine ingests data files from each source, normalizes the data into a common format, applies matching rules to pair records, and flags unmatched or out-of-tolerance items as exceptions.

**Rule-Based Auto-Resolution.** Beyond matching, advanced reconciliation systems can automatically resolve certain categories of breaks without human intervention:
- Timing breaks that match a known pattern (e.g., a transaction appears in the custodian file one day after it appears in the PMS) can be auto-resolved if the offsetting entry appears within a defined window.
- Rounding differences within tolerance can be auto-resolved and logged.
- Known pricing source differences for specific security types can be auto-resolved with the custodian price accepted as authoritative.

Auto-resolution rules must be carefully designed and regularly audited to ensure they are not masking genuine breaks. Each auto-resolved item should be logged for review.

**Exception-Based Processing.** The operational model for a mature reconciliation program is exception-based: the automated system handles the matching and auto-resolution of routine items, and human analysts focus exclusively on the exceptions. This model dramatically reduces the volume of items requiring manual review and allows operations teams to scale without proportional headcount growth.

A well-automated reconciliation program targets the following benchmarks:
- Auto-match rate (positions): 97-99% of position records match without intervention
- Auto-match rate (transactions): 90-95% of transactions match without intervention
- Exception rate: 1-5% of records require human review
- Same-day resolution rate: 80%+ of exceptions resolved on the day they are identified
- Break aging over 5 days: less than 0.5% of total accounts

**Data Normalization Across Sources.** A critical prerequisite for automated matching is data normalization — transforming records from different sources into a common format. Normalization challenges include:
- Security identifiers: the PMS may use CUSIP while the custodian uses ISIN or proprietary identifiers. The reconciliation system must maintain a cross-reference table.
- Account identifiers: the PMS account number may differ from the custodian account number. A mapping table is required.
- Transaction type codes: each system uses its own codes for buys, sells, dividends, etc. A translation table converts source-specific codes to a standard taxonomy.
- Date formats and conventions: different systems may use different date formats (MM/DD/YYYY vs. YYYY-MM-DD) or different date conventions (trade date vs. settlement date).
- Sign conventions: one system may represent sales as negative quantities while another uses positive quantities with a separate direction indicator.

**Reconciliation Scheduling.** The daily reconciliation cycle follows a predictable schedule:
1. Custodian end-of-day files are generated after market close and settlement processing (typically available between midnight and 6:00 AM the following business day).
2. The reconciliation system ingests the custodian files and the PMS end-of-day data.
3. Automated matching runs (typically completed by 7:00-8:00 AM).
4. Exception reports are generated and distributed to operations analysts.
5. Analysts investigate and resolve exceptions during the business day.
6. Resolved exceptions are documented and closed.
7. End-of-day reconciliation status report is produced for management review.

**STP Rate for Reconciliation.** Straight-through processing (STP) rate measures the percentage of reconciliation items that flow through the entire process — from data ingestion through matching to resolution — without manual intervention. A high STP rate indicates a well-automated, well-configured reconciliation operation. Industry benchmarks for mature operations: 95-99% STP rate for position reconciliation, 85-95% STP rate for transaction reconciliation, and 90-97% STP rate for cash reconciliation.

### 6. Corporate Action Reconciliation

Corporate actions are the single most frequent cause of position breaks that require manual resolution. A corporate action is any event initiated by the issuer of a security that affects the security's terms, structure, or ownership — including stock splits, reverse splits, mergers, acquisitions, spin-offs, tender offers, rights offerings, dividends (cash and stock), and return-of-capital distributions.

**Why Corporate Actions Cause Breaks.** Corporate actions are problematic for reconciliation because:
- The custodian and the PMS may process the same action on different dates, especially when the event has multiple milestone dates (announcement, record, ex-date, pay date, effective date).
- Voluntary actions (tender offers, rights offerings) require an election from the account holder. If the election is recorded in one system but not the other, the position diverges.
- Complex actions (mergers with mixed consideration — part cash, part stock; spin-offs with fractional share treatment) require multi-step processing that may be handled differently across systems.
- Some PMS platforms process corporate actions from the custodian data feed automatically, while others require manual entry. If the manual entry is delayed or performed incorrectly, a break results.

**Corporate Action Event Processing Timing.** The reconciliation team must track the lifecycle of each corporate action:
- **Announcement date:** The issuer announces the action. The PMS should record the pending event.
- **Record date:** The date on which shareholders of record are determined. Affects who receives the action's benefits.
- **Ex-date:** The first date on which the security trades without the benefit of the action (e.g., without the dividend or split). The custodian typically adjusts positions as of the ex-date.
- **Pay date / effective date:** The date on which the action takes effect (cash is paid, new shares are delivered, the merger closes).

**Voluntary vs. Mandatory Action Reconciliation.** Mandatory actions (splits, mergers, cash dividends) apply to all holders automatically and should be processed in both systems without account-level intervention. Voluntary actions (tender offers, rights exercises, dividend reinvestment elections) require per-account decisions and are a higher-risk category for breaks because the election must be recorded consistently across systems.

**Dividend and Income Reconciliation.** Cash dividends are the most frequent corporate action. Reconciliation verifies: the correct per-share rate was applied, the share count as of the record date matches, the total dividend amount (rate times shares) matches, and the payment was posted on the correct date. Dividend reinvestment (DRIP) is a common source of fractional-share breaks because the PMS and custodian may calculate the reinvestment slightly differently based on the price used.

**Stock Split and Merger Adjustment Verification.** After a split or merger is processed, the reconciliation team must verify: the new share count equals the old share count times the split ratio (or exchange ratio for mergers), the cost basis per share has been adjusted inversely to the share adjustment, and any fractional shares or cash-in-lieu payments are correctly recorded.

### 7. Multi-Custodian Reconciliation

Many advisory firms custody client assets at two or more custodians (e.g., Schwab and Fidelity, or a primary custodian and a trust company). Multi-custodian operations introduce additional reconciliation complexity.

**Aggregating Positions Across Custodians.** The PMS must maintain a unified view of all positions across all custodians, which requires separate reconciliation against each custodian's records. A position break at one custodian does not affect the reconciliation at another, but the PMS must correctly attribute each position to the correct custodian.

**Held-Away Asset Reconciliation.** Assets that the advisor monitors but does not manage (e.g., employer 401(k) plans, outside brokerage accounts, annuities) present a reconciliation challenge because: the data source is often an aggregation feed (Plaid, Yodlee, ByAllAccounts) rather than a direct custodian feed, data may be delayed by one to three days, position data may lack the granularity needed for precise reconciliation (e.g., no lot-level cost basis), and feed connections can break when the client's credentials change or the institution updates its login process. Held-away assets are typically reconciled at a lower frequency (weekly or monthly) and with wider tolerances than managed assets, because the data quality does not support daily zero-tolerance matching.

**Custodian Data Feed Formats and Timing.** Each custodian delivers data in its own format and on its own schedule:

| Custodian | Typical File Format | Typical Delivery Time | Notes |
|---|---|---|---|
| Schwab | CSV, proprietary layout | 2:00-5:00 AM ET | Schwab Advisor Center feed |
| Fidelity | CSV, proprietary layout | 1:00-4:00 AM ET | Wealthscape data feed |
| Pershing | Fixed-width and CSV | 3:00-6:00 AM ET | NetX360 feed |

**Normalization Challenges Across Custodians.** When reconciling across multiple custodians, the reconciliation system must normalize: security identifiers (one custodian may use CUSIP while another uses a proprietary ID), transaction type codes (each custodian has its own taxonomy for trades, dividends, fees, transfers), account number formats, date and time representations, and corporate action terminology and processing conventions. Maintaining and updating these normalization mappings is an ongoing operational task.

### 8. Regulatory and Fiduciary Requirements

Reconciliation is not merely an operational best practice — it is grounded in specific regulatory requirements and fiduciary obligations.

**SEC Rule 204-2 (Books and Records for Advisers).** Rule 204-2 under the Investment Advisers Act of 1940 requires SEC-registered investment advisers to maintain accurate books and records, including records of all securities transactions, client account positions, and supporting documentation. While the rule does not explicitly mandate a daily reconciliation process, the obligation to maintain accurate records effectively requires regular reconciliation against the custodian's official records. An adviser that reports positions or performance to clients based on unreconciled internal records risks producing inaccurate client communications, which is a violation of the adviser's fiduciary duty and a potential breach of the antifraud provisions of Section 206.

**Fiduciary Duty to Maintain Accurate Records.** Investment advisers owe a fiduciary duty to their clients, which includes the duty to provide accurate information. Reconciliation is the operational mechanism that ensures accuracy. If an adviser's internal records diverge from the custodian's records and the adviser relies on its internal records for billing, performance reporting, or investment decisions, the adviser may be billing incorrectly (overcharging or undercharging), reporting incorrect performance figures (misleading the client), or making investment decisions based on incorrect position data (breaching the duty of care). Regulators have brought enforcement actions against advisers whose failure to reconcile resulted in inaccurate client reporting or billing.

**ERISA Reconciliation Requirements.** For advisers managing ERISA-covered retirement plan assets, the fiduciary standard is heightened. ERISA fiduciaries must maintain accurate records of plan assets and ensure that all transactions are properly recorded. Reconciliation discrepancies that affect plan asset valuation can result in incorrect participant account balances, incorrect benefit calculations, and a breach of ERISA fiduciary duty. DOL audits of retirement plan service providers routinely examine reconciliation processes.

**Client Reporting Accuracy Obligations.** Client reports — whether quarterly statements, performance summaries, or online portal views — must reflect accurate, reconciled data. The SEC's examination priorities have repeatedly cited the accuracy of client reporting as a focus area. Firms that generate client reports from unreconciled data risk distributing misleading information, which can trigger enforcement action under the Investment Advisers Act's antifraud provisions.

**SOC 1 / SOC 2 Implications.** Many advisory firms and their service providers undergo SOC (System and Organization Controls) examinations. SOC 1 reports cover controls relevant to financial reporting, and SOC 2 reports cover security, availability, processing integrity, confidentiality, and privacy. Reconciliation processes are a key control tested in both SOC 1 and SOC 2 examinations. The examiner evaluates whether reconciliation is performed at the required frequency, whether breaks are investigated and resolved within defined timeframes, whether escalation procedures are followed, and whether the reconciliation process is documented and auditable. A reconciliation control failure can result in a qualified SOC opinion, which may cause downstream business consequences (clients and prospects may require an unqualified SOC report).

## Worked Examples

Three worked examples — a daily multi-custodian reconciliation design (ingestion schedule, auto-resolution rules, SOC 2 documentation, KPI targets), a root-cause investigation of a corporate-action break pattern (vendor delivery timing, cash-in-lieu gaps, spin-off basis), and a reconciliation automation build-out with exception-based processing — are in [references/examples.md](references/examples.md); load it when designing or troubleshooting a concrete reconciliation program.

## Common Pitfalls

- **Accepting timing breaks without verification.** It is tempting to classify all breaks as "timing" and assume they will self-resolve. While timing differences are common, labeling a genuine break as a timing difference delays resolution and can allow the break to compound. Every break classified as timing should be verified to have resolved within the expected window (typically one to two business days). If it does not resolve, it should be reclassified and investigated.
- **Reconciling positions but not cash or transactions.** Firms that reconcile only positions miss cash breaks (which can indicate missed dividends, incorrect fee debits, or unauthorized cash movements) and transaction breaks (which can indicate trades placed outside the PMS or duplicate entries). A complete reconciliation program covers all three dimensions.
- **Relying on the PMS as the source of truth.** The custodian, not the PMS, is the legally authoritative record of client assets. When a break is identified, the default assumption should be that the custodian is correct and the PMS needs updating — unless the firm has evidence to the contrary (such as a custodian processing error confirmed by the custodian's own inquiry process).
- **Ignoring cost basis reconciliation.** Because cost basis breaks do not affect current position counts or market values, they can be deprioritized until tax season, when they become urgent. By that point, historical cost basis discrepancies may be months or years old and extremely difficult to resolve. Regular cost basis reconciliation (monthly or quarterly) prevents this problem.
- **Setting auto-resolution tolerances too wide.** Overly generous auto-resolution rules can mask genuine breaks. For example, auto-resolving cash differences up to $100 may hide a pattern of missing dividend payments. Auto-resolution thresholds should be as tight as practical, and auto-resolved items should be sampled periodically for accuracy.
- **Not tracking break trends over time.** A reconciliation operation that resolves each day's breaks individually but never analyzes patterns over time will repeatedly fix the same types of breaks without addressing their systemic cause. Monthly break trend analysis is essential for continuous improvement.
- **Neglecting corporate action processing as a reconciliation input.** Corporate actions are the leading cause of non-timing breaks. Firms that treat corporate action processing and reconciliation as separate functions miss the opportunity to prevent breaks by ensuring timely and accurate corporate action processing upstream of the reconciliation cycle.
- **Underinvesting in data normalization.** Reconciliation automation is only as good as the data normalization layer. If security identifiers, transaction codes, or account mappings are incomplete or incorrect, the matching engine will generate false exceptions that waste analyst time and erode confidence in the system.
- **Failing to document break resolutions for audit purposes.** SOC auditors and SEC examiners expect to see documentation of every break: when it was identified, what caused it, what corrective action was taken, and when it was resolved. Undocumented resolutions are, from the auditor's perspective, the same as unresolved breaks.
- **Treating reconciliation as purely an operations function.** Reconciliation results directly affect compliance (accurate books and records), client reporting (accurate performance and positions), and revenue (accurate billing). The chief compliance officer and firm leadership should receive regular reconciliation reporting and be engaged when break rates deteriorate or systemic issues are identified.

## Cross-References

- **portfolio-management-systems** (advisory-practice plugin) — The PMS is one of the primary systems being reconciled. The PMS skill covers portfolio accounting, custodian data feeds, and the break identification process from the PMS perspective. This skill covers the broader reconciliation program design and operation.
- **settlement-clearing** (trading-operations plugin) — Settlement and clearing processes generate the transactions that are subsequently reconciled. Trade settlement failures and clearing discrepancies are a source of reconciliation breaks.
- **corporate-actions** (client-operations plugin) — Corporate action processing is the leading cause of non-timing reconciliation breaks. The corporate actions skill covers event processing; this skill covers the reconciliation of corporate action outcomes across systems.
- **books-and-records** (compliance plugin) — SEC Rule 204-2 and Rules 17a-3/17a-4 establish the recordkeeping obligations that reconciliation supports. Reconciliation documentation is itself part of the firm's books and records.
- **account-maintenance** (client-operations plugin) — Account-level changes (name changes, address updates, beneficiary changes, account re-registrations) can cause data discrepancies between systems if not synchronized, creating reconciliation breaks.
- **performance-reporting** (wealth-management plugin) — Performance calculations depend on accurate, reconciled position and transaction data. Unresolved reconciliation breaks can produce incorrect performance figures in client reports.
- **operational-risk** (trading-operations plugin) — Reconciliation failures are a category of operational risk. The operational risk skill covers the broader risk management framework; this skill covers the specific reconciliation controls that mitigate data accuracy risk.
- **fee-billing** (advisory-practice plugin) — Advisory fee billing depends on accurate AUM figures, which depend on reconciled position and market value data. Billing on unreconciled data risks overcharging or undercharging clients.
