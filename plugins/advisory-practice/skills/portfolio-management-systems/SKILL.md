---
name: portfolio-management-systems
description: "Select, configure, and operate portfolio management systems for advisory firms, covering model portfolios, UMA/sleeve management, drift monitoring, rebalancing, and custodian data feeds. Use when the user asks about choosing a PMS platform, building or distributing model portfolios, implementing UMA or sleeve-based management, setting drift monitoring thresholds, aggregating held-away assets, reconciling PMS with custodian records, configuring PMS-based billing, or troubleshooting custodian feed issues. Also trigger when users mention 'portfolio management system', 'Orion', 'Black Diamond', 'Tamarac', 'Addepar', 'Advent APX', 'model portfolio', 'sleeve management', 'rebalancing engine', 'custodian feed', or 'PMS migration'."
---

# Portfolio Management Systems

## Core Concepts

> Expanded detail for each numbered section below lives in
> [references/platform-details.md](references/platform-details.md). Load it when the task needs:
> §1 the platform comparison table or IBOR/OBOR reconciliation dimensions; §2 full model
> specification, governance steps, or marketplace detail; §3 UMA cash-waterfall rules or the
> UMA/SMA/wrap comparison table; §4 drift measurement formulas, threshold configurations, or
> tax-aware rebalancing logic; §5 aggregation data sources and data-quality failure modes;
> §6 break-resolution workflow, corporate-action types, or cost basis methods; §8 daily vs.
> monthly calculation and benchmark tracking detail; §10 the custodian data-flow table,
> integration methods, and feed timing. (Reference §7 trading and §9 billing are pointers to
> the order-management-advisor and fee-billing skills — load those skills directly instead.)

### 1. Portfolio Management System Architecture

The PMS is the operational nerve center of an advisory practice, orchestrating data flow between custodians, trading platforms, reporting engines, CRM, and planning tools. Core functions include portfolio construction, model management, rebalancing, trading, performance reporting, and billing. Major platforms: Orion, Black Diamond, Tamarac, Addepar, Morningstar Direct, Advent/APX. The PMS serves as the firm's Investment Book of Record (IBOR), which must be reconciled daily against the custodian's Official Book of Record (OBOR).

### 2. Model Portfolio Management

Model portfolios define target allocations (asset classes, securities, weights) applied consistently across client accounts. Types include strategic (SAA), tactical (TAA overlays), and specialty models (income, ESG, tax-managed). Firms typically use a two-tier hierarchy (firm-level + advisor-customized). Model changes trigger versioning, account identification, trade proposal generation, and tax-aware transition. Third-party model marketplaces (BlackRock, DFA, Vanguard, PIMCO) allow smaller firms to access institutional-quality investment management.

### 3. Sleeve-Based and UMA Architecture

Unified Managed Accounts (UMAs) divide a single custodial account into virtual sub-accounts (sleeves), each following its own strategy or manager. Benefits: cross-sleeve tax optimization, simplified reporting, reduced account proliferation, and unified cash management. Cash waterfall rules govern deposits, withdrawals, and income allocation across sleeves. UMAs differ from SMAs (single-strategy, one manager) and mutual fund wraps (indirect ownership, limited customization). Typical minimums: $250K-$1M+.

### 4. Drift Monitoring and Rebalancing

Drift is the divergence of actual weights from targets caused by differential returns and cash flows. Measured as absolute drift (percentage-point difference) or relative drift (percentage of target). Threshold configurations range from conservative (3%/15%) to permissive (7%/30%). Rebalancing approaches: calendar-based, threshold-based, opportunistic (cash-flow-directed), and hybrid. Tax-aware rebalancing incorporates capital gains minimization, loss harvesting, wash sale avoidance, and gain budgets.

### 5. Held-Away Asset Aggregation

A complete client picture requires visibility into all assets, including employer plans, stock options, RSUs, bank accounts, and accounts at other custodians. Data sources: aggregation services (Plaid, Yodlee, MX, ByAllAccounts), custodian feeds, manual entry, and employer plan integrations. Challenges include data staleness, categorization errors, and broken connections. The PMS should provide both managed-only and total-household reporting views.

### 6. Portfolio Accounting and Reconciliation

Portfolio accounting tracks positions, transactions, cost basis, cash flows, and accrued income. Daily reconciliation compares PMS against custodian across three dimensions: positions, transactions, and cash. Breaks require classification, root-cause diagnosis, correction, and documentation. Common break sources: corporate actions (splits, mergers, spin-offs, DRIP), trade settlement timing, and data feed issues. Cost basis methods: specific identification, FIFO, and average cost.

### 7. Trading and Order Management Integration

The PMS generates trade proposals from model changes, rebalancing triggers, cash flows, and ad-hoc instructions. In larger firms, trades flow through a separate OMS for compliance checks, block aggregation, and execution routing. Block trading aggregates orders across accounts for best execution with pro-rata allocation. Pre-trade checks cover restricted securities, concentration limits, client restrictions, regulatory limits, and cash minimums. Implementation methods: direct custodian trading, third-party EMS, and mutual fund trading platforms.

### 8. Performance Calculation Engine

The PMS computes returns at multiple levels: security, sleeve, account, household, model, composite, and firm. TWR (time-weighted) eliminates cash flow impact for manager evaluation and GIPS compliance. MWR (money-weighted/IRR) reflects the investor's actual experience. Daily performance provides the most precise TWR; monthly uses approximations like Modified Dietz. Benchmarks (primary, blended, custom) must be tracked at the same frequency as portfolio returns.

### 9. Billing and Fee Calculation

Fee structures: AUM-based (flat or tiered/breakpoint), flat/retainer, performance-based (qualified clients only), and blended. Billing frequency: quarterly (most common), monthly, or annual. Advance billing requires proration; arrears billing delays revenue recognition. Billable AUM determination requires clear policies on included/excluded assets and household aggregation. Fee deduction via direct debit (most common) or invoice. Revenue tracking covers client, advisor, model, and strategy dimensions.

### 10. Custodian Integration and Data Feeds

Custodian integration provides the data backbone: positions, transactions, cash, cost basis, corporate actions, and new accounts flow from custodian to PMS; trade instructions and fee invoices flow from PMS to custodian. Integration methods: proprietary batch feeds (CSV/XML), FIX protocol, APIs, and third-party aggregators. Feed timing: EOD batch (most common), intraday updates, and real-time streaming. Multi-custodian management requires data normalization, consolidated views, custodian-specific trade routing, and separate reconciliation. Custodian transitions (e.g., TD Ameritrade to Schwab) require account mapping, feed migration, and historical data transfer.

## Worked Examples

See [references/examples.md](references/examples.md) for three end-to-end worked examples —
a PMS migration for a growing RIA, a UMA/sleeve implementation for HNW clients, and a
reconciliation break investigation. Load it when the user needs a full scenario walkthrough.

## Common Pitfalls

1. **Treating the PMS as the official record.** The custodian, not the PMS,
   maintains the legally authoritative record of client assets. When discrepancies
   exist, the custodian record governs. Firms that rely solely on PMS data without
   reconciliation risk reporting incorrect positions and performance.

2. **Neglecting daily reconciliation.** Firms that reconcile weekly or monthly
   allow breaks to compound, making root-cause diagnosis much harder. A corporate
   action missed on Monday may cause cascading errors in performance, billing,
   and rebalancing throughout the week.

3. **Over-engineering drift thresholds.** Setting drift bands too tight (e.g., 1%
   absolute) generates excessive trading, increasing costs and tax drag. Setting
   bands too loose (e.g., 10% absolute) allows portfolios to deviate significantly
   from the intended risk profile. Calibrate thresholds based on asset class
   volatility and client tax sensitivity.

4. **Ignoring wash sale rules across accounts.** Tax-loss harvesting in one account
   while purchasing substantially identical securities in another account with the
   same tax ID disallows the loss. The PMS must monitor wash sale windows across
   all accounts for a client or household.

5. **Stale held-away data.** Aggregated held-away data that has not refreshed in
   weeks or months can lead to materially incorrect total-household allocation views
   and flawed planning recommendations. Implement alerts for stale connections and
   establish a process for client re-authentication.

6. **Inconsistent model governance.** Allowing advisors to freely modify firm models
   without oversight creates style drift and compliance risk. Establish clear
   policies on which model elements advisors can customize and require documentation
   of deviations.

7. **Cost basis discrepancies between PMS and custodian.** The PMS and custodian may
   calculate cost basis differently, especially after corporate actions, transfers,
   or wash sale adjustments. If the firm relies on PMS cost basis for tax-loss
   harvesting decisions but the custodian reports different basis to the IRS
   (Form 1099-B), clients may face unexpected tax consequences.

8. **Billing on stale or unreconciled data.** Calculating fees on PMS positions that
   have not been reconciled against the custodian may result in over- or under-billing.
   Always reconcile before running billing.

9. **Failing to test custodian feed changes.** Custodians periodically update their
   data feed formats. Firms that do not monitor for format changes or test in a
   staging environment before production risk silent data-import failures.

10. **Overlooking performance calculation methodology.** Reporting MWR when TWR
    is appropriate (or vice versa) can mislead clients or violate GIPS standards.
    Understand when each methodology is appropriate and clearly label which method
    is used in client-facing reports.

## Cross-References

- **asset-allocation** (wealth-management plugin) — PMS implements the strategic
  and tactical asset allocation defined in the client's investment policy. Model
  portfolios in the PMS are the operational expression of asset allocation decisions.
- **rebalancing** (wealth-management plugin) — The PMS rebalancing engine applies
  rebalancing theory (threshold-based, calendar-based, opportunistic) to live client
  portfolios. The rebalancing skill defines the theory; this skill covers the
  system implementation.
- **tax-efficiency** (wealth-management plugin) — PMS tax-loss harvesting,
  wash sale monitoring, and tax-aware rebalancing apply the tax-efficiency
  principles defined in the tax-efficiency skill to operational workflows.
- **performance-metrics** (wealth-management plugin) — The PMS calculates the
  return metrics (TWR, MWR, alpha, Sharpe ratio) defined in the performance-metrics
  skill. That skill defines the math; this skill covers how the PMS implements the
  calculations.
- **performance-reporting** (wealth-management plugin) — The PMS generates the
  underlying performance data that feeds client-facing performance reports. The
  reporting skill covers presentation and communication; this skill covers
  calculation and data infrastructure.
- **gips-compliance** (compliance plugin) — PMS composite construction and
  performance calculation must satisfy GIPS requirements for firms that claim
  compliance. The GIPS skill defines the standards; this skill covers the PMS
  configuration needed to meet them.
- **order-management-advisor** (advisory-practice plugin) — The OMS receives
  trade lists generated by the PMS. This skill covers trade list generation; the
  OMS skill covers order routing, execution, and allocation.
- **financial-planning-integration** (advisory-practice plugin) — The PMS
  current portfolio (including held-away aggregation) feeds financial planning
  tools for projections and scenario analysis.
- **fee-billing** (advisory-practice plugin) — The PMS fee engine handles
  billing calculations described here. The fee-billing skill covers the broader
  billing operations workflow including invoicing, collections, and revenue
  recognition.
- **client-reporting-delivery** (advisory-practice plugin) — PMS performance
  data, portfolio holdings, and asset allocation feeds the client reporting and
  delivery workflow.
