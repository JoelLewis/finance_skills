---
name: post-trade-compliance
description: "Guide post-trade compliance monitoring and trade surveillance system design. Use when building alert logic to detect churning, front-running, cherry-picking, layering, spoofing, wash trading, or marking the close, implementing post-trade best execution review, evaluating allocation fairness with pro-rata verification or dispersion analysis, designing exception-based monitoring workflows with escalation paths, correlating trading with MNPI events for insider trading detection, building personal trading surveillance for preclearance and blackout enforcement, determining SAR or blue sheet or CAT reporting triggers, or tuning surveillance thresholds to reduce false positives. Also covers turnover ratios, cost-to-equity ratios, and investigation case management."
---

# Post-Trade Compliance

## Core Concepts

### Trade Surveillance Framework
Trade surveillance is the systematic, ongoing monitoring of executed transactions to detect potential violations of securities laws, firm policies, and regulatory rules. A surveillance program operates across multiple time horizons:

- **T+0 (same-day) monitoring** — Real-time or end-of-day reviews targeting time-sensitive patterns such as front-running (trading ahead of a customer block order), late trading (mutual fund orders placed after the 4:00 p.m. ET NAV pricing cutoff), and marking the close (orders placed to influence the closing price). T+0 alerts require immediate investigation because the regulatory harm is ongoing or the evidence window is narrow.
- **T+1 through T+3 monitoring** — Next-day and settlement-window reviews for patterns that emerge across a short sequence of events: allocation fairness on block trades, partial fill distribution, and settlement failures. These alerts align with the trade settlement cycle and CAT error correction windows.
- **T+N rolling-window monitoring** — Longer-horizon reviews (weekly, monthly, quarterly) for patterns that only become visible over time: churning and excessive trading (turnover ratios measured over months), coordinated trading across accounts, systematic favoritism in allocations, and insider trading correlations (trading patterns around earnings announcements or M&A events). Rolling windows must be calibrated to the specific pattern — churning detection typically requires 3-12 months of data, while insider trading correlation windows may span 30-90 days around a material event.

**Surveillance scope** varies by firm type and business activity. A full-service broker-dealer conducting equities, fixed income, and derivatives trading must maintain surveillance across all asset classes. An RIA managing model portfolios may focus surveillance on allocation fairness, best execution, and personal trading. The surveillance program must cover both customer/client accounts and proprietary/firm accounts.

**Alert generation** is the process of applying quantitative thresholds, pattern matching rules, or scoring models to transaction data to produce alerts requiring human review. Effective alert generation requires clean, normalized data from multiple sources: order management systems, execution management systems, account master data, market data, and — for insider trading detection — corporate event calendars and restricted lists.

**Investigation workflow** follows a standard lifecycle:

1. Alert generation
2. Initial triage and prioritization
3. Investigation and fact gathering
4. Disposition (close with no finding, close with finding, escalate)
5. Escalation to senior compliance or legal
6. Regulatory filing if warranted (SAR, STR, or self-report)

Each stage must be documented in a case management system with timestamps, analyst notes, evidence, and supervisory sign-off.

**Disposition and escalation** decisions are among the most consequential in a compliance program. A disposition of "no finding" must be supported by documented analysis — regulators will review closed alerts during examinations. Escalation criteria should be defined in written procedures: escalate when the pattern is consistent with a securities law violation, when the activity involves a senior person or high-risk account, when the dollar amount exceeds a defined threshold, or when a pattern recurs after a prior warning.

**Regulatory filing triggers** — Post-trade surveillance may identify activity that requires a SAR filing (for broker-dealers; FinCEN's 2024 rule extending AML program and SAR obligations to covered investment advisers, originally effective January 1, 2026, was postponed to January 1, 2028 by a final rule issued December 2025), an STR (Suspicious Transaction Report, the international equivalent under FATF standards), or a self-report to FINRA or the SEC. The decision to file a SAR based on surveillance findings must be made by the AML Compliance Officer in coordination with the surveillance team. The SAR tipping-off prohibition (31 U.S.C. Section 5318(g)(2)) applies — the subject of the surveillance alert must not be informed of a SAR filing.

### Pattern Detection
Surveillance systems must be designed to detect specific prohibited trading patterns. Each pattern has distinct data requirements, detection logic, and evidentiary standards:

**Churning / excessive trading** — Quantitative metrics include turnover ratio (aggregate purchases divided by average equity, with ratios above 6 presumptively excessive), cost-to-equity ratio (annualized costs as a percentage of average equity, with ratios above 20% generally excessive), and in-and-out trading frequency. Detection requires account-level transaction history, commission and fee data, and the customer's stated investment objectives. Churning surveillance is typically run on a rolling 3-12 month window.

**Front-running** — Trading in a firm or personal account ahead of a pending customer order that is expected to move the market. Detection requires correlating proprietary/personal trading activity with the timestamps of customer order receipt and execution. Key data elements: order receipt time (from CAT or order management system), execution time, account ownership, and the direction and size of the customer order. Front-running alerts are time-sensitive and should be generated on T+0 or T+1.

**Cherry-picking (favorable allocations)** — A pattern where an adviser or trader allocates profitable trades to favored accounts and unprofitable trades to disfavored accounts. Detection involves comparing the performance of allocations across accounts within a block trade or across trades over time. Statistical methods include comparing average returns by account against the expected distribution under fair allocation. Cherry-picking is a form of fraud that violates fiduciary duty and Section 10(b) of the Exchange Act.

**Insider trading** — Trading by persons with access to material non-public information (MNPI) ahead of corporate events such as earnings announcements, M&A transactions, FDA approvals, or regulatory actions. Detection requires correlating trading activity with an events calendar and identifying trades that are unusual in timing, size, or profitability relative to the trader's historical pattern. Insider trading surveillance often relies on restricted list and watch list monitoring, where securities of companies about which the firm possesses MNPI are placed on restricted or watch lists and trading activity is monitored or prohibited.

**Layering / spoofing** — Placing non-bona fide orders on one side of the order book to create a false impression of supply or demand, then executing on the opposite side and canceling the layered orders. Detection requires order-level data (not just executions) including order submissions, modifications, and cancellations with timestamps. Key indicators: high order-to-execution ratios, rapid cancellation patterns, and consistent profitability on the execution side when layered orders are present.

**Wash trading** — Simultaneously or near-simultaneously buying and selling the same security with no change in beneficial ownership, creating the appearance of market activity. Detection involves identifying offsetting transactions in the same security, same account (or related accounts), within a narrow time window. Wash trading can also occur across accounts controlled by the same beneficial owner.

**Marking the close** — Placing orders near the end of the trading session to influence the closing price. Detection requires analyzing order timestamps relative to market close, particularly for securities where the closing price affects portfolio valuations, options settlements, or performance calculations. Key indicator: late-session orders in securities where the firm or its clients have a valuation interest.

**Coordinated trading** — Multiple accounts trading the same securities in the same direction within a narrow time window, suggesting coordination or common direction. Detection involves clustering analysis across accounts by security, direction, and time, particularly when the accounts share a common adviser, trader, or beneficial owner.

**Late trading** — Submitting mutual fund orders after the 4:00 p.m. ET NAV pricing cutoff but receiving the current day's NAV. Detection requires comparing order entry timestamps with the 4:00 p.m. cutoff, with attention to time zone differences, system clock accuracy, and any manual order entry processes that could allow backdating.

### Best Execution Review
Best execution is the obligation to seek the most favorable terms reasonably available for client transactions. Post-trade best execution review measures execution quality after the fact and identifies systematic deficiencies.

**Benchmark comparison** — Each execution is compared against one or more benchmarks to measure quality. Common benchmarks include:

- **VWAP (Volume-Weighted Average Price)** — The average price weighted by volume over a defined period (typically the trading day). Executions below VWAP (for buys) or above VWAP (for sells) indicate favorable execution.
- **Arrival price** — The mid-quote at the time the order was received. Measures the cost of execution relative to the decision price, capturing both market impact and timing cost.
- **Closing price** — Used primarily for orders benchmarked to end-of-day pricing, such as index fund rebalancing.
- **Implementation shortfall** — The difference between the portfolio's paper return (using decision prices) and the actual return (using execution prices), capturing all explicit and implicit costs of execution.

**Outlier detection** — Identify executions that deviate significantly from the benchmark. Common approaches: flag executions more than a defined number of standard deviations from the mean benchmark deviation, or flag executions where the deviation exceeds a basis-point threshold (e.g., more than 50 basis points worse than VWAP). Outlier thresholds must be calibrated by asset class, order size, and market conditions — a 50 bps deviation may be normal for a small-cap equity but alarming for a large-cap liquid name.

**Venue analysis** — Compare execution quality across venues (exchanges, ATSs, market makers, OTC dealers) to determine whether the firm's order routing is systematically achieving best execution. Metrics include effective spread, fill rate, speed of execution, and price improvement. Venue analysis should account for order flow characteristics — routing difficult orders to one venue and easy orders to another will skew venue-level statistics.

**Review program and committee** — The systematic best-execution review program and best execution committee framework (quarterly reviews, committee composition, minutes, routing-arrangement evaluation) are owned by the trade-execution skill (trading-operations). Post-trade surveillance contributes the surveillance-side inputs: outlier executions flagged against benchmarks, venue-level exception statistics, and trend data feeding the committee's review.

### Allocation Fairness
When a single order is executed on behalf of multiple accounts (a block trade), the resulting executions must be allocated fairly. Allocation fairness monitoring detects systematic patterns of favoritism.

**Pro-rata allocation verification** — The standard method for block trade allocation is pro rata, where each participating account receives shares in proportion to its intended participation. Post-trade monitoring verifies that actual allocations match the pro-rata methodology by comparing each account's allocation percentage to its intended participation percentage. Deviations must be documented and justified (e.g., rounding, minimum lot sizes, odd-lot avoidance).

**Dispersion analysis** — Measures the distribution of execution prices across accounts within a block trade. In a fair allocation, all accounts should receive approximately the same average execution price. Dispersion analysis flags block trades where certain accounts received systematically better prices than others. The analysis should account for legitimate reasons for dispersion, such as different allocation methods (average price vs. sequential fill) and account-level constraints.

**Systematic favoritism detection** — Extends cherry-picking analysis across time to detect patterns where specific accounts consistently receive more favorable allocations. Statistical approaches include:

1. Comparing each account's average allocation quality (measured as deviation from benchmark) against the group mean over a rolling period
2. Rank-ordering accounts by allocation quality and testing whether the ranking is correlated with account type (e.g., proprietary accounts, performance-fee accounts, or accounts of firm principals)
3. Regression analysis testing whether account characteristics predict allocation quality after controlling for order characteristics

**IPO allocation rules** — FINRA Rules 5130 and 5131 restrict the allocation of new issues (IPOs, secondary offerings) to certain persons, including broker-dealer personnel, portfolio managers, and their immediate family members. Post-trade surveillance must verify that IPO allocations do not flow to restricted persons. Rule 5131 also prohibits quid pro quo allocations (conditioning allocations on the receipt of excessive compensation) and spinning (allocating hot IPOs to executives of investment banking clients).

**Trade rotation monitoring** — For firms that use a rotation system (where the first account to receive an allocation rotates across trades), post-trade monitoring verifies that the rotation is being followed. Deviations from the rotation schedule should be flagged and investigated.

**Partial fill allocation** — When a block order is only partially filled, the partial fill must be allocated fairly. Post-trade monitoring verifies that partial fills are allocated pro rata (or according to the firm's stated methodology) rather than being concentrated in favored accounts. Partial fill allocation is a common area of cherry-picking because partial fills on profitable trades are particularly valuable.

### Exception-Based Monitoring
Exception-based monitoring is the operational framework for managing the volume of alerts generated by surveillance systems.

**Alert tuning** — Surveillance systems generate alerts based on thresholds and rules. Alert tuning is the ongoing process of adjusting these parameters to optimize the trade-off between sensitivity (catching real violations) and specificity (minimizing false positives). A system that generates too many false positives overwhelms investigators and leads to alert fatigue, causing real violations to be missed. A system that is too conservative misses violations. Tuning involves analyzing historical alert data: review disposition outcomes (what percentage of alerts resulted in findings?), adjust thresholds based on statistical analysis, and implement machine learning or scoring models to prioritize alerts by risk.

**Alert prioritization** — Not all alerts are equally urgent or significant. Prioritization frameworks assign risk scores based on factors such as:

- The severity of the potential violation (insider trading is more serious than a minor allocation deviation)
- The dollar amount involved
- The account type (customer, proprietary, employee)
- The individual involved (senior personnel, repeat offenders)
- The time sensitivity (front-running requires immediate review)

High-priority alerts should be routed to senior investigators with defined response-time SLAs.

**Investigation workflow** — The standard investigation lifecycle is:

1. **Alert receipt** — the alert is generated and assigned to an investigator.
2. **Initial triage** — the investigator reviews the alert details and determines whether the alert warrants a full investigation or can be closed as a known false positive. Triage decisions must be documented.
3. **Full investigation** — the investigator gathers additional evidence: transaction records, communications (email, chat, phone records), account documentation, market data, and any relevant context (was the security on a restricted list? was there a pending corporate event?).
4. **Disposition** — the investigator documents findings and recommends a disposition: close with no finding, close with finding and corrective action, or escalate.
5. **Supervisory review** — a senior compliance officer reviews the investigation and approves the disposition.
6. **Escalation** — if warranted, the matter is escalated to the CCO, legal counsel, or senior management for determination of whether regulatory reporting or disciplinary action is required.

**Aging and SLA management** — Alerts must be investigated within defined timeframes. SLAs should be tiered by priority:

- High-priority alerts: within 2-5 business days
- Medium-priority alerts: within 10 business days
- Low-priority alerts: within 20 business days

An aging dashboard tracks open alerts against SLAs and flags overdue items. Persistent SLA breaches indicate insufficient staffing, poor alert tuning, or systemic workflow issues. Regulators expect that firms can demonstrate timely disposition of alerts — an examination finding of hundreds of unreviewed aged alerts is a serious supervisory deficiency.

**Alert documentation** — Every alert must be documented from generation through disposition. Documentation must include: the alert details (trigger, threshold, data), the investigator's analysis, evidence reviewed, disposition rationale, supervisory approval, and any follow-up actions. Documentation serves two purposes: it creates an examination-ready audit trail, and it provides data for alert tuning and program assessment.

### Personal Trading Surveillance
Firms must monitor the personal securities trading of employees, officers, and access persons to prevent conflicts of interest and insider trading.

**Employee trading monitoring** — Firms must receive and review reports of personal securities transactions by access persons. Under SEC Rule 204A-1 (for investment advisers) and FINRA rules (for broker-dealers), access persons must report holdings and transactions. Surveillance systems compare employee trading against restricted lists, watch lists, and client trading activity to detect potential front-running or trading on MNPI.

**Preclearance verification** — Many firms require employees to obtain preclearance before executing personal trades. Post-trade surveillance verifies that all personal trades were precleared by comparing executed trades against preclearance records. Trades executed without preclearance — or trades that differ from the precleared terms (different security, larger size, different direction) — must be flagged and investigated.

**Holding period compliance** — Firm codes of ethics commonly impose minimum holding periods (e.g., 30 or 60 days) to discourage short-term speculative trading that could conflict with client interests. Post-trade surveillance monitors buy-sell intervals for personal accounts and flags violations.

**Blackout period enforcement** — During blackout periods (typically around earnings announcements, fund portfolio rebalancing, or when the firm possesses MNPI about a security), employees are prohibited from trading the affected securities. Surveillance systems must cross-reference personal trading against active blackout periods and restricted lists.

**Reporting deadline monitoring** — Access persons must file:

- Initial holdings reports within 10 days of becoming an access person
- Annual holdings reports within 45 days of the reporting period end
- Quarterly transaction reports within 30 days of quarter end

Surveillance systems track filing compliance and flag late or missing reports.

### Regulatory Reporting Triggers
Post-trade surveillance activities may identify conditions that trigger specific regulatory reporting obligations.

**SAR filing thresholds** — Broker-dealers must file SARs for transactions of $5,000 or more that the firm knows, suspects, or has reason to suspect involve illegal activity, BSA evasion, or no apparent lawful purpose (31 CFR Section 1023.320). Post-trade surveillance findings — such as wash trading, layering, or unusual trading patterns with no economic rationale — may satisfy the suspicion element. The decision to file rests with the AML Compliance Officer, and the SAR tipping-off prohibition applies. FinCEN's investment adviser AML rule, which extends SAR filing requirements to covered investment advisers, has a postponed effective date of January 1, 2028 (delayed from January 1, 2026 by FinCEN's December 2025 final rule).

**Large trader reporting (Form 13H)** — Post-trade analysis may identify accounts or persons whose aggregate trading activity meets the large trader thresholds (2 million shares or $20 million in a single day, or 20 million shares or $200 million in a calendar month). Broker-dealers must monitor for customers who meet the threshold but have not self-identified with an LTID, and must maintain transaction records for all large trader accounts.

**Blue sheet requests** — Although blue sheet requests originate from the SEC, a firm's post-trade surveillance system must be capable of extracting and producing the required transaction data (customer identity, account, security, date, price, quantity, capacity) within the SEC's specified timeframe. Firms that discover potential issues during blue sheet preparation (e.g., trading by restricted persons, unreported large trader activity) should evaluate whether self-reporting is appropriate.

**CAT reporting obligations** — All reportable events in the order lifecycle — origination, routing, modification, cancellation, execution, and allocation — must be reported to CAT by 8:00 a.m. ET on T+1. Post-trade compliance processes must verify that CAT submissions are accurate and complete, and that errors are corrected within T+3.

**TRACE reporting (fixed income)** — OTC transactions in TRACE-eligible fixed income securities must be reported within 15 minutes of execution. Post-trade monitoring should verify that TRACE reports are timely and accurate, and flag late reports for remediation.

**Short interest reporting** — FINRA Rule 4560 requires semi-monthly reporting of short positions. Post-trade systems must accurately track and report short positions as of the designated settlement dates.

### Surveillance Technology
Effective post-trade compliance requires robust technology infrastructure.

**Data requirements** — Surveillance systems consume data from multiple sources:

- Order management systems (order details, timestamps, account identifiers)
- Execution management systems (fill prices, quantities, venues)
- Account master data (customer profiles, investment objectives, account type, relationships)
- Market data (prices, volumes, benchmarks)
- Corporate events data (earnings dates, M&A announcements, FDA actions)
- Communications data (email, chat, voice)
- Reference data (restricted lists, watch lists, employee rosters)

Data completeness and timeliness are foundational — surveillance analytics are only as good as the input data.

**Data normalization** — Transaction data from multiple source systems must be normalized to a common schema:

- Consistent security identifiers (mapping between CUSIPs, ISINs, tickers, and internal identifiers)
- Standardized timestamps (UTC or a single reference timezone with millisecond precision)
- Uniform account identifiers (mapping across systems that may use different account numbering)
- Consistent trade type classifications (buy, sell, short sale, cover)

Normalization failures are a leading cause of surveillance system false positives and missed detections.

**Analytics and scoring models** — Modern surveillance systems use a combination of rule-based alerts (threshold breaches, pattern matches) and statistical/machine learning models (anomaly detection, behavioral scoring). Rule-based alerts are transparent and auditable but rigid. Statistical models can detect novel patterns but require careful validation and explainability for regulatory purposes. A hybrid approach — using models to score and prioritize alerts generated by rules — is increasingly common. All models must be documented, validated, and subject to periodic review.

**Case management** — A case management system tracks each alert through its lifecycle: assignment, investigation, evidence attachment, disposition, supervisory review, and closure. The system must support workflow routing, SLA tracking, escalation, audit trails, and reporting. Case management data is the primary artifact reviewed during regulatory examinations of a firm's surveillance program.

**Regulatory examination support** — Surveillance systems must be able to produce examination-ready reports: alert volumes and disposition statistics, investigation timelines and outcomes, tuning history and rationale, coverage analysis (which patterns are monitored, which are not and why), and sample case files demonstrating the quality of investigations. Regulators — particularly the SEC's Division of Examinations and FINRA's Market Regulation department — evaluate not just whether a firm has a surveillance program, but whether it is effective, adequately staffed, and responsive to identified issues.

## Worked Examples

Worked examples are in [references/examples.md](references/examples.md) — load for an end-to-end scenario: (1) building a trade surveillance program for a mid-size broker-dealer, (2) implementing allocation fairness monitoring for an RIA managing model portfolios. For a best execution committee framework example, see the trade-execution skill (trading-operations).

## Common Pitfalls
- Running churning surveillance with a single fixed turnover threshold for all account types — thresholds must be calibrated to the customer's investment objectives, with lower thresholds for conservative and income-oriented accounts
- Monitoring allocations only at the block trade level without running longitudinal systematic favoritism analysis — a firm can produce fair individual allocations while still systematically favoring certain accounts over time through subtle selection of which accounts participate in which blocks
- Relying on end-of-day batch surveillance for time-sensitive patterns like front-running and marking the close — these patterns require T+0 or near-real-time detection to enable timely investigation and intervention
- Failing to integrate communications surveillance (email, chat, voice) with trade surveillance — insider trading and coordinated trading cases almost always require communications evidence; siloed systems miss these connections
- Setting alert thresholds too conservatively to minimize false positives, which creates under-detection of genuine violations — regulators view under-detection as a more serious deficiency than a high false positive rate, provided the firm can demonstrate timely disposition of alerts
- Treating alert disposition statistics as the measure of program effectiveness — a program that closes 99% of alerts with "no finding" may indicate poor calibration rather than a clean book of business
- Allowing a backlog of aged, uninvestigated alerts to accumulate — regulators consider a large backlog of open alerts to be evidence of an inadequate surveillance program, regardless of the firm's explanation for the backlog
- Excluding proprietary trading accounts and employee accounts from the surveillance scope — these accounts are higher-risk and should receive heightened, not reduced, scrutiny
- Conducting best execution reviews using only aggregate statistics without examining individual outlier executions — aggregate metrics can mask systematic issues with specific order types, securities, or venues
- Documenting investigation dispositions with conclusory statements ("no violation found") rather than substantive analysis — regulatory examiners expect to see the analytical work supporting the disposition
- Failing to update the surveillance risk assessment when the firm enters new business lines, launches new products, or experiences significant growth — the surveillance program must evolve with the firm's risk profile
- Neglecting personal trading surveillance for non-investment personnel who may nonetheless have access to MNPI (e.g., operations staff processing block orders, technology personnel with access to order management systems)

## Cross-References
- **pre-trade-compliance** (trading-operations plugin): Pre-trade checks (restricted list screening, position limits, margin requirements) are the first line of defense; post-trade surveillance catches what pre-trade controls miss and validates that pre-trade controls are functioning
- **trade-execution** (trading-operations plugin): Execution quality data feeds directly into best execution review; post-trade compliance evaluates whether the execution function is meeting its obligations
- **order-lifecycle** (trading-operations plugin): Post-trade surveillance depends on complete, accurate order lifecycle data from origination through execution and allocation; gaps in order lifecycle data create surveillance blind spots
- **sales-practices** (compliance plugin): Churning, unauthorized trading, and breakpoint abuse are sales practice violations detected through post-trade surveillance; the sales-practices skill covers the substantive rules, while this skill covers the detection methodology
- **anti-money-laundering** (compliance plugin): SAR filing obligations may be triggered by post-trade surveillance findings; the AML skill covers the substantive compliance framework, while this skill covers the surveillance detection that identifies reportable activity
- **books-and-records** (compliance plugin): Surveillance case files, alert documentation, investigation records, and committee minutes are books and records subject to retention requirements under SEC Rules 17a-3/17a-4 and Rule 204-2
- **regulatory-reporting** (compliance plugin): Post-trade surveillance may trigger regulatory reporting obligations (SARs, 13H filings, TRACE corrections, CAT error remediation); the regulatory-reporting skill covers the filing mechanics
- **conflicts-of-interest** (compliance plugin): Allocation fairness, cherry-picking, and personal trading surveillance all address conflicts of interest; the conflicts-of-interest skill covers the identification and mitigation framework, while this skill covers the post-trade detection methodology
