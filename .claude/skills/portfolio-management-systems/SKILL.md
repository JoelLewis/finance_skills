---
name: portfolio-management-systems
description: >
  Guidance on portfolio management system architecture, model portfolios, sleeve-based
  and UMA management, drift monitoring, rebalancing engines, held-away aggregation,
  portfolio accounting, trading integration, performance calculation, billing, and
  custodian data feeds for advisory practices.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
---

# Portfolio Management Systems

## Purpose

Enable Claude to advise on the selection, configuration, and operation of portfolio
management systems (PMS) within registered investment advisory firms. This skill covers
the full PMS lifecycle: platform architecture, model portfolio construction, sleeve-based
and UMA management, drift monitoring, rebalancing, held-away asset aggregation, portfolio
accounting, trading integration, performance calculation, billing, and custodian data
feeds. It equips Claude to guide advisors, operations teams, and technology leaders
through PMS implementation decisions, day-to-day operational workflows, and
troubleshooting reconciliation or data-quality issues.

## Layer

10 — Advisory Practice (Front Office)

## Direction

both

## When to Use

- An advisor or RIA asks about selecting or migrating to a portfolio management platform
- Questions arise about building, maintaining, or distributing model portfolios
- A firm wants to implement UMA or sleeve-based account management
- An operations team needs guidance on drift monitoring thresholds or rebalancing configuration
- A practice seeks to aggregate held-away assets for holistic financial planning views
- Questions involve daily reconciliation between a PMS and custodian records
- An advisor asks how trades flow from the PMS to the order management system or custodian
- Discussion involves PMS-based performance calculation (TWR, MWR) or composite construction
- A firm needs to configure fee schedules, billing runs, or billable-AUM calculations in the PMS
- Questions concern custodian data feeds, multi-custodian management, or feed troubleshooting
- Trigger phrases: "portfolio management system," "Orion," "Black Diamond," "Tamarac,"
  "Addepar," "model portfolio," "UMA," "sleeve," "rebalancing engine," "drift monitoring,"
  "held-away assets," "portfolio accounting," "reconciliation," "custodian feed," "PMS billing"

## Core Concepts

### 1. Portfolio Management System Architecture

The portfolio management system is the operational nerve center of an investment advisory
practice. It sits at the intersection of investment management, client servicing, and
compliance, orchestrating the flow of data between custodians, trading platforms, reporting
engines, CRM systems, and financial planning tools.

**Core PMS Functions:**

- **Portfolio construction** — Building and maintaining investment portfolios aligned with
  client objectives and firm models.
- **Model management** — Defining, versioning, and distributing model portfolios across
  the client base.
- **Rebalancing** — Detecting portfolio drift from targets and generating trade proposals
  to restore alignment.
- **Trading** — Producing trade lists, supporting block trading, and routing orders to
  custodians or execution platforms.
- **Performance reporting** — Calculating time-weighted and money-weighted returns at the
  security, account, household, and composite levels.
- **Billing** — Computing advisory fees based on AUM, generating invoices or direct-debit
  instructions, and tracking revenue.

**Major PMS Platforms:**

| Platform | Provider | Typical Firm Size | Key Strengths |
|---|---|---|---|
| Orion Portfolio Solutions | Orion Advisor Solutions | Mid to large RIAs | Deep rebalancing, compliance, and reporting; Eclipse trading engine |
| Black Diamond | SS&C Technologies | Mid-size RIAs | Strong performance reporting and client portal |
| Tamarac | Envestnet | Mid to large RIAs | Rebalancing, CRM integration (via Envestnet ecosystem) |
| Addepar | Addepar | Large RIAs, family offices | Complex asset support, alternatives, data visualization |
| Morningstar Direct | Morningstar | Research-oriented firms | Investment research integration, manager analysis |
| Advent/APX | SS&C Technologies | Large RIAs, institutional | Institutional-grade accounting and multi-currency support |

**Investment Book of Record (IBOR) vs. Official Book of Record:**

The PMS serves as the firm's investment book of record (IBOR), maintaining the advisory
firm's view of positions, transactions, cost basis, and performance. The custodian
maintains the official book of record (OBOR) — the legally authoritative record of client
assets. These two records must be reconciled daily to ensure accuracy. Discrepancies
(breaks) require investigation and resolution before reporting or billing can proceed
with confidence.

**Key reconciliation dimensions:**

- Position reconciliation — Do PMS and custodian agree on shares/units held?
- Transaction reconciliation — Are all trades, dividends, and corporate actions reflected
  in both systems?
- Cash reconciliation — Do cash balances match after accounting for pending settlements?

### 2. Model Portfolio Management

Model portfolios are the foundation of scalable portfolio management. A model defines a
target investment allocation — specifying asset classes, individual securities or funds,
and their target weights — that can be applied consistently across many client accounts.

**Defining a Model Portfolio:**

A model portfolio specification includes:

- **Target asset allocation** — The percentage assigned to each asset class (e.g., 60%
  equity, 35% fixed income, 5% alternatives).
- **Security selection** — The specific ETFs, mutual funds, or individual securities
  used to represent each asset class.
- **Target weights** — The precise weight for each security within the model (e.g.,
  VTI 30%, VXUS 15%, BND 25%, BNDX 10%, VNQ 5%, cash 5%, etc.).
- **Substitution rules** — Tax-efficient alternatives for taxable accounts, ESG
  substitutions, or client-specific restrictions.

**Model Types:**

- **Strategic models (SAA)** — Long-term, policy-driven allocations reflecting the firm's
  capital market assumptions. Changed infrequently (annually or less). Example: a
  "Moderate Growth" model targeting 60/40 equity/fixed income.
- **Tactical models (TAA overlays)** — Short-term tilts applied on top of strategic
  allocations to capitalize on market dislocations or risk management. Example:
  underweighting international equities by 5% during a dollar-strengthening cycle.
- **Specialty models** — Purpose-built allocations for specific objectives: income
  generation, ESG/SRI mandates, tax-managed (municipal bonds, low-turnover equity),
  concentrated stock diversification.

**Model Hierarchy:**

Most firms operate a two-tier model structure:

- **Firm-level models** — Centrally managed by the investment committee or CIO. These
  represent the firm's house view and ensure consistency.
- **Advisor-customized models** — Advisors may create variants of firm models with
  client-specific adjustments (e.g., excluding a sector due to concentrated employer
  stock, adding a charitable giving sleeve). The PMS should track these customizations
  and flag when they deviate materially from the base model.

**Model Changes and Governance:**

When the investment committee changes a model — whether adjusting allocation weights,
substituting a security, or adding a new asset class — the PMS must:

1. Version the model change with an effective date.
2. Identify all accounts assigned to the affected model.
3. Generate rebalancing trade proposals for those accounts.
4. Apply tax-aware logic to minimize the cost of transitioning.
5. Route trades through the trading workflow for review and execution.

**Model Marketplace:**

Major PMS and TAMP platforms offer access to third-party model portfolios from asset
managers such as BlackRock, DFA (Dimensional Fund Advisors), Vanguard, PIMCO, and
JP Morgan. Advisors can adopt these models wholesale or blend them with proprietary
models. This allows smaller firms to leverage institutional-quality investment management
without building in-house research capabilities.

### 3. Sleeve-Based and UMA Architecture

The Unified Managed Account (UMA) structure represents an evolution from single-strategy
managed accounts to multi-strategy, multi-manager portfolios held within a single
brokerage account.

**UMA Structure:**

A UMA divides a single custodial account into multiple virtual sub-accounts called
sleeves. Each sleeve follows its own investment strategy, model, or external manager,
but all sleeves share a single account number, tax ID, and custodial registration.

**Typical UMA Sleeve Examples:**

| Sleeve | Strategy | Manager/Model |
|---|---|---|
| Core U.S. Equity | Large-cap growth + value | Firm proprietary model |
| International Equity | Developed + emerging markets | DFA International Core model |
| Fixed Income | Investment-grade bonds | PIMCO model |
| Alternatives | Real assets, hedge fund replication | Third-party manager |
| Tactical Overlay | Short-term tilts | CIO tactical model |
| Cash/Liquidity | Money market, short-term | Cash management rules |

**Benefits of UMA/Sleeve Architecture:**

- **Tax efficiency** — The overlay manager or PMS can harvest losses in one sleeve and
  avoid realizing gains in another, optimizing the tax outcome at the account level. This
  cross-sleeve tax coordination is impossible when strategies are held in separate accounts.
- **Simplified reporting** — One account statement instead of multiple, with the option
  to show performance by sleeve or for the total account.
- **Reduced account proliferation** — A client who might otherwise need 5-6 separate
  managed accounts can consolidate into a single UMA, reducing operational complexity.
- **Unified cash management** — Cash flows (dividends, interest, withdrawals, deposits)
  can be managed at the account level and allocated across sleeves according to rules.

**Cash Management Across Sleeves:**

The PMS must define how cash is handled across sleeves:

- **Cash waterfall rules** — When a client deposits funds, which sleeves receive
  the cash and in what priority order?
- **Cash raise logic** — When a client requests a withdrawal, which sleeves are
  liquidated and in what order (typically selling the most overweight sleeve first
  or the sleeve with the most harvestable losses)?
- **Income allocation** — Dividends and interest generated within a sleeve may stay
  in that sleeve or flow to a central cash sleeve.

**UMA vs. SMA vs. Mutual Fund Wrap:**

| Feature | UMA | SMA | Mutual Fund Wrap |
|---|---|---|---|
| Number of strategies | Multiple | Single | Multiple (via funds) |
| Account structure | One account, multiple sleeves | One account, one strategy | One account, fund portfolio |
| Security ownership | Direct (individual securities) | Direct | Indirect (fund shares) |
| Tax management | Cross-sleeve optimization | Single-strategy only | Limited (fund-level) |
| Customization | High (per-sleeve and cross-sleeve) | Moderate (single strategy) | Low |
| Typical minimum | $250K-$1M+ | $100K-$250K | $25K-$100K |
| Manager access | Multiple managers, one account | One manager | Multiple managers via funds |

### 4. Drift Monitoring and Rebalancing

Portfolio drift is the divergence of actual portfolio weights from target model weights
caused by differential asset returns, cash flows, and corporate actions over time. The
PMS continuously monitors drift and generates rebalancing recommendations when
thresholds are breached.

**Measuring Drift:**

- **Absolute drift** — The simple difference between actual weight and target weight.
  If U.S. equity target is 40% and actual is 44%, absolute drift is +4 percentage
  points.
- **Relative drift** — The drift as a percentage of the target weight. Using the same
  example, relative drift is 4/40 = 10%.
- **Band-based monitoring** — Each asset class or security has an allowable range
  (band) around the target. Rebalancing triggers only when a holding breaches the
  band boundary. Example: target 40% with a +/-5% band means rebalancing triggers
  below 35% or above 45%.

**Drift Thresholds:**

Common threshold configurations in PMS platforms:

- Conservative: 3% absolute or 15% relative drift.
- Moderate: 5% absolute or 25% relative drift.
- Permissive: 7% absolute or 30% relative drift.

The appropriate threshold depends on tax sensitivity, turnover tolerance, trading costs,
and client preferences.

**Rebalancing Approaches:**

- **Calendar-based** — Rebalancing at fixed intervals (quarterly, semi-annually,
  annually) regardless of drift levels. Simple to implement but may miss significant
  interim drift or trigger unnecessary trades.
- **Threshold-based** — Rebalancing only when drift exceeds defined thresholds.
  More responsive than calendar-based and avoids unnecessary trading, but requires
  continuous monitoring.
- **Opportunistic (cash-flow-directed)** — Using client deposits, withdrawals,
  dividends, and other cash flows as opportunities to move toward targets without
  generating incremental trades. The most tax-efficient approach for accounts with
  regular cash flows.
- **Hybrid** — Combining threshold-based monitoring with opportunistic cash flow
  rebalancing. Thresholds serve as the outer guardrail while cash flows handle
  minor drift continuously.

**Tax-Aware Rebalancing:**

A sophisticated PMS rebalancing engine incorporates tax considerations:

- **Capital gains minimization** — When selling overweight positions, prefer lots
  with losses or long-term gains over short-term gains.
- **Loss harvesting** — Proactively selling positions with unrealized losses to
  generate tax deductions, then replacing with similar (but not substantially
  identical) securities.
- **Wash sale avoidance** — The PMS must track the 30-day wash sale window across
  all accounts for the same tax ID to prevent disallowed losses.
- **Gain budget** — Some firms set a maximum dollar amount of realized gains per
  account per year, and the rebalancing engine respects this constraint.

**Cash-Flow-Directed Rebalancing:**

When a client deposits $50,000 into a portfolio, the PMS calculates the optimal
allocation of that cash to move the portfolio closer to target weights. Rather than
investing proportionally to the current allocation, the deposit is directed to the
most underweight positions. Similarly, withdrawals are funded by selling the most
overweight positions first.

### 5. Held-Away Asset Aggregation

A complete picture of a client's financial situation requires visibility into all assets,
not just those managed by the advisory firm. Held-away assets include employer retirement
plans (401(k), 403(b)), stock options, restricted stock units (RSUs), bank accounts,
annuities, real estate, and accounts at other custodians.

**Data Sources for Held-Away Assets:**

- **Account aggregation services** — Technology platforms that connect to financial
  institutions via screen-scraping or API to retrieve account data. Major providers
  include Plaid, Yodlee (Envestnet), MX, and ByAllAccounts (Morningstar). These
  services pull positions, balances, and sometimes transactions on a scheduled basis.
- **Custodian data feeds** — Some custodians provide direct feeds for accounts
  held at their institution, enabling higher-quality data than aggregation services.
- **Manual entry** — For assets that cannot be electronically aggregated (real estate,
  private equity, collectibles), advisors or clients enter valuations manually. These
  require periodic updates to remain useful.
- **Employer plan integration** — Specialized feeds from retirement plan recordkeepers
  (Fidelity NetBenefits, Empower, Vanguard) that provide participant-level data.

**Challenges with Held-Away Data:**

- **Data freshness** — Aggregated data may be 1-3 days stale, and connections can
  break when institutions change login procedures or add multi-factor authentication.
- **Categorization accuracy** — Aggregation services may misclassify securities or
  asset types, requiring manual correction in the PMS.
- **Stale connections** — Clients must periodically re-authenticate their linked
  accounts. Stale connections produce outdated data that can lead to incorrect
  planning recommendations.
- **Incomplete data** — Some institutions block aggregation, and certain asset types
  (unvested RSUs, stock options) may not transmit full detail (exercise price,
  vesting schedule).

**Use in Financial Planning and Portfolio Management:**

Held-away assets directly affect advisory decisions:

- **Asset allocation assessment** — A client's managed account may appear well
  diversified, but when combined with a 401(k) heavily concentrated in employer
  stock, the total household allocation could be dangerously concentrated.
- **Planning recommendations** — Held-away 401(k) assets affect retirement
  projections, Roth conversion analysis, and Social Security claiming strategies.
- **Tax planning** — Knowing the asset location (tax-deferred, Roth, taxable) across
  all accounts enables better tax-efficient asset placement decisions.

**Reporting Views:**

The PMS should provide two distinct reporting perspectives:

- **Managed-only view** — Shows only assets under the firm's management, used for
  billing, performance reporting, and regulatory filings.
- **Total household view** — Includes held-away assets, used for financial planning
  discussions, asset allocation reviews, and comprehensive client presentations.

### 6. Portfolio Accounting and Reconciliation

Portfolio accounting is the systematic tracking of all investment positions, transactions,
cost basis, cash flows, and accrued income within the PMS. Accuracy in portfolio
accounting is the foundation for reliable performance reporting, tax management, and
client trust.

**PMS as Investment Book of Record (IBOR):**

The PMS maintains a complete transaction history and position ledger for every managed
account:

- **Positions** — Current holdings with quantity, market value, unrealized gain/loss.
- **Transactions** — Buys, sells, exchanges, transfers-in, transfers-out, dividends,
  interest, fees, corporate actions.
- **Cost basis** — Original purchase price and date for each tax lot, adjusted for
  corporate actions (splits, mergers, return of capital).
- **Cash balances** — Settled and pending cash, including accrued income not yet
  received.
- **Accrued income** — Interest accrued on fixed-income holdings between coupon
  payment dates.

**Daily Reconciliation Process:**

Reconciliation compares the PMS investment book of record against the custodian's
official book of record across three dimensions:

1. **Position reconciliation** — Compares shares/units held per security per account.
   Breaks typically result from unprocessed trades, missed corporate actions, or
   data-feed errors.
2. **Transaction reconciliation** — Compares trade activity for the day. Breaks may
   indicate trades executed at the custodian but not reflected in the PMS, or PMS
   trades that failed to execute.
3. **Cash reconciliation** — Compares cash balances accounting for settled and
   unsettled activity. Cash breaks often result from timing differences in
   dividend/interest posting or fee deductions.

**Break Identification and Resolution:**

A break is any discrepancy between PMS and custodian records. Break resolution follows
a standard workflow:

1. Identify break in the daily reconciliation report.
2. Classify the break type (position, transaction, cash, cost basis).
3. Determine root cause (missed corporate action, trade error, feed issue, timing).
4. Apply correction in the appropriate system (PMS adjustment, custodian inquiry).
5. Verify the break is resolved in the next reconciliation cycle.
6. Document the resolution for audit trail purposes.

**Corporate Actions Processing:**

Corporate actions are among the most common sources of reconciliation breaks:

- **Cash dividends** — Record income and increase cash balance.
- **Stock dividends** — Increase share count without cash impact.
- **Stock splits** — Adjust share count and cost basis per share.
- **Reverse splits** — Reduce share count and adjust cost basis.
- **Mergers/acquisitions** — Remove acquired security, add acquiring security,
  adjust cost basis for tax-free reorganizations.
- **Spin-offs** — Add new security, allocate cost basis from parent.
- **Tender offers** — Partial or full redemption at specified price.
- **Return of capital** — Reduce cost basis rather than record income.

**Cost Basis Methods:**

The PMS must support multiple cost basis methods, as the method affects realized
gains and losses:

- **Specific identification** — The investor (or PMS algorithm) selects which tax
  lots to sell, enabling optimal tax management. This is the most common method
  for advisory accounts.
- **FIFO (First In, First Out)** — Sells the oldest lots first. Simple but may
  result in larger gains in rising markets.
- **Average cost** — Uses the average cost of all shares. Permitted only for mutual
  fund shares and certain other securities.

**Tax Lot Management:**

Effective tax lot management enables gain/loss optimization:

- Maintain lot-level detail (purchase date, cost, quantity) for every position.
- Track holding period (short-term vs. long-term) to distinguish gain character.
- Support lot selection strategies (highest cost, lowest cost, loss harvesting,
  gain minimization).
- Track wash sale adjustments across accounts with the same tax ID.

### 7. Trading and Order Management Integration

The PMS generates trade proposals based on model changes, rebalancing triggers, cash
flow events, and ad-hoc advisor instructions. These proposals flow through a trading
workflow that includes compliance checks, order aggregation, and execution routing.

**PMS-Generated Trade Lists:**

Trade lists originate from several PMS functions:

- **Model-driven trades** — When a model allocation changes or a new security is
  substituted, the PMS generates trades for all accounts assigned to that model.
- **Rebalancing trades** — When drift monitoring detects threshold breaches, the
  PMS generates trades to restore target alignment.
- **Cash-flow trades** — When a client deposits or withdraws funds, the PMS
  generates invest or liquidation trades.
- **Ad-hoc trades** — Advisor-initiated trades for client-specific needs (e.g.,
  selling a concentrated stock position, gifting securities).

**Integration with Order Management:**

In larger firms, the PMS integrates with a separate Order Management System (OMS):

1. PMS proposes trades (trade blotter or trade list).
2. Advisor or portfolio manager reviews and approves.
3. Approved trades are sent to the OMS.
4. OMS applies pre-trade compliance checks.
5. OMS aggregates orders across accounts for block trading.
6. OMS routes orders to execution venues.
7. Execution confirmations flow back to the PMS to update positions.

In smaller firms, the PMS may handle steps 3-7 internally using a built-in trading
module (e.g., Orion Eclipse, Tamarac Trading).

**Block Trading from PMS:**

When the same trade needs to execute across dozens or hundreds of accounts, the PMS
or OMS aggregates individual account orders into block orders:

- Aggregate buy or sell orders for the same security across accounts.
- Execute the block as a single order for best execution.
- Allocate fills back to individual accounts pro-rata or according to a
  pre-defined allocation methodology.
- Ensure fair and equitable treatment across accounts (no account systematically
  receives better or worse fills).

**Pre-Trade Compliance Checks:**

Before trades execute, the PMS or OMS validates against compliance rules:

- **Restricted securities** — Securities on the firm's restricted list (due to
  insider information, investment banking relationships, or client instructions).
- **Concentration limits** — Maximum position size as a percentage of the account
  or portfolio (e.g., no single equity position exceeding 10%).
- **Client restrictions** — Individual client mandates such as ESG exclusions,
  sector prohibitions, or specific security restrictions.
- **Regulatory limits** — Position limits for certain securities or asset classes.
- **Cash minimums** — Ensuring sufficient cash remains after trading to cover
  anticipated withdrawals or fee debits.

**Trade Implementation Methods:**

- **Direct custodian trading** — The PMS sends trade instructions directly to the
  custodian's trading platform via API or file-based integration. Common for simple
  equity and ETF trades.
- **Third-party execution platforms** — Trades are routed to an execution management
  system (EMS) for best-execution routing across multiple venues. Used for fixed
  income, international, or complex orders.
- **Mutual fund trading** — Mutual fund orders typically execute through the
  custodian's fund trading platform (e.g., Schwab Mutual Fund OneSource, Fidelity
  FundsNetwork) at NAV.

### 8. Performance Calculation Engine

The PMS serves as the performance calculation engine for the advisory practice,
computing returns at multiple levels and across multiple methodologies.

**Time-Weighted Return (TWR):**

TWR measures the compound growth rate of a portfolio, eliminating the impact of
external cash flows (deposits and withdrawals). This method is the standard for
evaluating investment manager performance because it reflects only investment
decisions, not the timing of client cash flows.

TWR is calculated by:

1. Dividing the measurement period into sub-periods at each external cash flow.
2. Computing the holding-period return for each sub-period.
3. Geometrically linking the sub-period returns.

TWR is required for benchmark comparison and GIPS-compliant composites because it
enables fair comparison between portfolios with different cash flow patterns.

**Money-Weighted Return (MWR / IRR):**

MWR measures the actual return experienced by the investor, accounting for the
timing and size of cash flows. A client who adds significant funds just before a
market rally will see a higher MWR than TWR, while a client who withdraws before
a rally will see a lower MWR than TWR.

MWR is most relevant for:

- Client reporting (showing the personal investment experience).
- Evaluating the impact of cash flow timing decisions.
- Private equity and alternative investments where cash flow timing is integral
  to the investment.

**Daily vs. Monthly Performance:**

- **Daily performance** — Returns calculated every day using daily valuations.
  Provides the most precise TWR calculation and enables intra-month reporting.
  Requires daily position and pricing data from custodians.
- **Monthly performance** — Returns calculated at month-end using month-end
  valuations. Less precise for TWR (uses Modified Dietz or similar approximation
  for intra-month cash flows) but requires less infrastructure.

Most modern PMS platforms support daily performance calculation.

**Benchmark Assignment and Tracking:**

Each model, account, or composite is assigned one or more benchmarks:

- **Primary benchmark** — The market index most representative of the portfolio's
  investment strategy (e.g., 60% MSCI ACWI / 40% Bloomberg U.S. Aggregate for
  a 60/40 portfolio).
- **Blended benchmarks** — Weighted combinations of multiple indices matching
  the portfolio's asset allocation.
- **Custom benchmarks** — Firm-constructed benchmarks reflecting specific
  investment policies.

The PMS must track benchmark returns at the same frequency and over the same periods
as portfolio returns to enable meaningful comparison.

**Performance at Multiple Levels:**

A comprehensive PMS calculates performance at every level of the investment hierarchy:

- **Security level** — Return contribution of each holding.
- **Sleeve level** — Performance of each UMA sleeve or sub-strategy.
- **Account level** — Total account performance (TWR and MWR).
- **Household level** — Aggregated performance across all accounts for a client
  or household.
- **Model level** — Theoretical performance of the model itself (useful for
  evaluating model quality separately from implementation).
- **Composite level** — Aggregated performance of all accounts following a
  similar strategy, used for GIPS reporting and marketing.
- **Firm level** — Overall firm AUM-weighted performance.

### 9. Billing and Fee Calculation

The PMS fee engine automates the calculation, deduction, and tracking of advisory fees,
which are typically the primary revenue source for RIA firms.

**Fee Structures:**

- **AUM-based (flat rate)** — A single percentage applied to all managed assets
  (e.g., 1.00% annually on all AUM).
- **AUM-based (tiered/breakpoint)** — Declining fee rates at higher asset levels.
  Example: 1.25% on the first $500K, 1.00% on $500K-$1M, 0.75% on $1M-$5M,
  0.50% above $5M. Tiers may be applied per account or at the household level.
- **Flat/retainer fees** — Fixed dollar amounts for financial planning or advisory
  services, independent of AUM.
- **Performance fees** — Fees based on investment returns exceeding a benchmark or
  hurdle rate. Subject to SEC regulations (generally available only to qualified
  clients with $1.1M+ in AUM or $2.2M+ net worth under the Investment Advisers
  Act).
- **Blended fees** — Combinations of the above (e.g., reduced AUM fee plus
  financial planning retainer).

**Billing Frequency and Timing:**

- **Quarterly billing** — The most common frequency. Billed in advance (based on
  beginning-of-quarter AUM) or in arrears (based on end-of-quarter AUM or
  average daily AUM during the quarter).
- **Monthly billing** — Common for larger accounts or institutional mandates.
- **Annual billing** — Less common, used for flat-fee planning engagements.

Advance billing requires prorating for accounts opened or closed mid-quarter.
Arrears billing is more precise but delays revenue recognition.

**Billable AUM Calculation:**

Determining which assets are included in the billable base requires clear policies:

- **Included assets** — Typically all managed securities and cash held at the
  custodian. Some firms exclude cash above a threshold or assets in transit.
- **Excluded assets** — Held-away assets, assets under a separate fee arrangement,
  or specific asset types excluded by client agreement.
- **Household billing** — Aggregating AUM across all accounts for a household to
  determine the fee tier, then applying that tier to each account. This benefits
  clients with multiple smaller accounts who collectively reach higher breakpoints.
- **Billing date valuation** — The market value used for fee calculation. End-of-
  period, beginning-of-period, or average daily balance during the period.

**Fee Deduction Methods:**

- **Direct debit** — The advisory fee is deducted directly from the client's
  custodial account. Requires client authorization (typically in the investment
  advisory agreement). The custodian processes the deduction based on an invoice
  from the advisor. This is the most common method for RIAs.
- **Invoice/direct pay** — The firm sends an invoice and the client pays by check
  or ACH. Used for financial planning fees or when clients prefer not to have
  fees deducted from investment accounts.

**Revenue Tracking and Reporting:**

The PMS fee engine should provide:

- Revenue by client, advisor, model, strategy, and office.
- Fee trend analysis (quarter-over-quarter, year-over-year).
- Fee schedule compliance (verifying charged fees match contracted rates).
- Billing audit trail for regulatory examination support.

### 10. Custodian Integration and Data Feeds

Custodian integration is the data backbone of the PMS. The quality, completeness,
and timeliness of custodian data feeds directly determine the accuracy of portfolio
accounting, performance reporting, rebalancing, and billing.

**Data Flowing Between PMS and Custodians:**

| Data Type | Direction | Frequency | Purpose |
|---|---|---|---|
| Positions | Custodian to PMS | Daily (EOD) | Reconciliation, reporting |
| Transactions | Custodian to PMS | Daily (EOD) | Accounting, performance |
| Cash balances | Custodian to PMS | Daily (EOD) | Cash management, rebalancing |
| Cost basis | Custodian to PMS | Daily or on-demand | Tax reporting, gain/loss |
| Corporate actions | Custodian to PMS | As-occurs + EOD | Accounting adjustments |
| New accounts | Custodian to PMS | Daily or real-time | Account setup |
| Trade instructions | PMS to custodian | Real-time or batch | Order execution |
| Fee invoices | PMS to custodian | Quarterly/monthly | Fee deduction |

**Integration Methods:**

- **Custodian proprietary data feeds** — Major custodians provide standardized
  data files in proprietary or industry-standard formats. Examples: Schwab
  (Schwab Advisor Center data feeds), Fidelity (Wealthscape data feeds),
  Pershing (NetX360 data feeds). These are typically delivered as batch files
  (CSV, XML, or fixed-width) at end-of-day.
- **FIX protocol** — Financial Information eXchange protocol for real-time trade
  messaging. Used for order routing, execution reporting, and position updates.
  More common for institutional trading than advisory account management.
- **API-based integration** — RESTful APIs provided by custodians for real-time
  data access. Increasingly available but with varying levels of completeness.
  Schwab and Fidelity have expanded API offerings for RIAs.
- **Third-party data aggregators** — Services like Quovo (Plaid), ByAllAccounts
  (Morningstar), or Addepar's data infrastructure that normalize data from
  multiple custodians into a standard format for PMS consumption.

**Feed Timing:**

- **End-of-day (EOD) batch** — The most common feed timing. Custodian generates
  files after market close and settlement processing (typically available by
  early morning of the following business day). EOD feeds provide the settled
  view of positions and transactions.
- **Intraday updates** — Some custodians provide intraday position snapshots and
  real-time trade confirmations. Useful for same-day rebalancing and cash
  management but not universally available.
- **Real-time streaming** — Available for limited data types (trade confirmations,
  price updates) via FIX or websocket connections. Primarily used by firms with
  active trading or time-sensitive operations.

**Multi-Custodian Management:**

Many advisory firms custody client assets at two or more custodians (e.g., Schwab
and Fidelity). The PMS must:

- Ingest and normalize data feeds from each custodian into a unified data model.
- Present a consolidated view of positions, performance, and asset allocation
  across custodians.
- Generate trades appropriate for each custodian's trading platform and rules.
- Reconcile separately against each custodian's records.
- Handle custodian-specific differences in security identifiers, transaction
  types, corporate action processing, and settlement conventions.

**Custodian Transition Management:**

When a firm changes its primary custodian (e.g., transitioning from TD Ameritrade
to Schwab following the 2023-2024 acquisition), the PMS must support:

- Mapping accounts from the old custodian to the new.
- Ingesting the new custodian's data feeds and formats.
- Transferring historical data to maintain performance continuity.
- Managing the transition period when accounts may exist at both custodians
  simultaneously.
- Re-establishing automated trading and fee deduction with the new custodian.
- Communicating changes to clients and managing expectations around
  temporary data gaps.

## Worked Examples

### Example 1: PMS Migration for a Growing RIA

**Scenario:**

A $500M RIA with 800 client households has been managing portfolios using Excel
spreadsheets and the custodian's online platform. The firm operates 12 model
portfolios across two custodians (Schwab and Fidelity). As the firm grows, the
spreadsheet approach creates unacceptable operational risk: rebalancing is
inconsistent, performance reporting is delayed by weeks, and the firm recently
discovered it had been billing a client at the wrong fee rate for two quarters.
The firm decides to implement Orion as its portfolio management system.

**Design Considerations:**

**Platform selection criteria:**

- Multi-custodian support (Schwab and Fidelity integration required).
- Rebalancing engine capable of handling 12+ models across 800+ households.
- Tax-aware rebalancing with wash sale tracking.
- Automated billing with tiered fee schedule support.
- Performance reporting with composite construction for marketing materials.
- Integration with the firm's existing CRM (Salesforce).
- Client portal for on-demand performance access.

**Data migration planning:**

- Export current positions and cost basis from both custodians.
- Reconstruct historical transactions from custodian records (typically 3-5
  years for performance history, full history for cost basis).
- Map existing security positions to Orion's security master.
- Import client and account demographic data from CRM.
- Establish the 12 model portfolios in Orion with target allocations and
  security selections.

**Model setup and configuration:**

- Define each of the 12 models with target weights, drift bands, and
  rebalancing rules.
- Assign each client account to the appropriate model.
- Configure substitution rules for taxable vs. tax-deferred accounts.
- Set drift thresholds (the firm selects 5% absolute / 25% relative).
- Configure cash reserve rules (2% minimum cash per account).

**Custodian feed setup:**

- Establish Schwab data feeds: positions, transactions, cash balances,
  cost basis, corporate actions. Test file delivery and parsing.
- Establish Fidelity data feeds: same data categories. Test independently.
- Configure daily reconciliation jobs for both custodians.
- Validate initial reconciliation: resolve any breaks before go-live.

**Go-live workflow:**

- Run parallel operations for 30 days (maintain spreadsheets alongside Orion).
- Compare rebalancing recommendations from both systems.
- Validate performance calculations against custodian-reported returns.
- Validate billing calculations against historical invoices.
- Train advisors and operations staff on the new workflows.
- Decommission spreadsheet processes after successful parallel period.

**Analysis:**

The migration represents a significant operational transformation. The firm should
budget 3-6 months for full implementation, including 1-2 months for data migration
and setup, 1 month for parallel testing, and 1-2 months for staff training and
workflow refinement. Key risks include data quality issues during migration
(especially historical cost basis), disruption to client reporting during the
transition, and staff resistance to new workflows. The firm should designate a
dedicated project manager and plan for temporary increases in operations staffing
during the transition. Post-implementation, the firm should expect significant
efficiency gains: rebalancing that previously took two days per quarter should
complete in hours, billing errors should be eliminated by automated fee calculation,
and performance reports should be available daily rather than weeks after quarter-end.

### Example 2: UMA/Sleeve Implementation for HNW Clients

**Scenario:**

A wealth management firm serving high-net-worth clients ($1M+ investable assets)
currently manages client portfolios using 3-5 separate SMAs per client, each
following a different strategy. This creates operational burden (multiple account
statements, separate rebalancing for each SMA, inability to coordinate tax
management across accounts) and client confusion. The firm decides to transition
its HNW clients to a UMA/sleeve-based structure using its existing PMS (Tamarac).

**Design Considerations:**

**Sleeve structure design:**

The firm designs a five-sleeve UMA architecture:

| Sleeve | Allocation Range | Strategy | Management |
|---|---|---|---|
| Core U.S. Equity | 25-45% | Broad U.S. equity exposure | Firm proprietary model |
| International Equity | 10-25% | Developed and emerging markets | DFA model via Tamarac |
| Fixed Income | 15-35% | Investment-grade and municipal bonds | PIMCO model |
| Alternatives | 5-15% | Real assets, liquid alternatives | Third-party manager |
| Tactical Overlay | 0-10% | Short-term tactical tilts | CIO discretion |

Cash is managed at the total account level rather than within individual sleeves,
with a 2% minimum cash target.

**Model assignment rules:**

- Each client's Investment Policy Statement (IPS) dictates the overall allocation
  across sleeves based on their risk profile.
- Conservative clients: higher fixed income and lower alternatives allocation.
- Aggressive clients: higher equity and alternatives allocation.
- Sleeve-level models operate independently within their assigned allocation.
- The overlay manager (CIO) can make tactical adjustments within the overlay
  sleeve without affecting other sleeves.

**Cross-sleeve tax management:**

- The PMS overlay engine monitors unrealized gains and losses across all sleeves.
- When rebalancing triggers a sell in one sleeve, the overlay engine checks
  whether a loss can be harvested in another sleeve to offset the gain.
- Wash sale rules are monitored across sleeves: if the fixed income sleeve sells
  a bond fund at a loss, the equity sleeve cannot purchase a substantially
  identical fund within 30 days.
- Year-end tax management: the overlay engine runs a cross-sleeve analysis to
  identify harvesting opportunities before December 31.

**Reporting configuration:**

- **Client-facing reports** show total UMA performance alongside per-sleeve
  performance attribution, so clients understand how each strategy contributes.
- **Internal reports** track model-level performance (how well each model
  performed independent of client cash flows) and implementation efficiency
  (how closely client accounts track their assigned models).
- **Billing reports** calculate fees on total UMA AUM (not per-sleeve).
- **Household reports** aggregate across multiple UMAs and non-UMA accounts
  for clients with more than one account.

**Analysis:**

The UMA transition consolidates 3-5 accounts per client into a single account,
reducing custodian fees, simplifying client statements, and enabling cross-strategy
tax optimization that was previously impossible. The firm should expect a 2-3 month
transition per client cohort, as existing SMA positions must be transferred in-kind
to the new UMA account structure. Tax implications of the transition must be
carefully managed — the firm should avoid realizing gains during the restructuring
by transferring positions in-kind wherever possible. The ongoing operational benefit
is substantial: the overlay manager can rebalance all sleeves simultaneously,
dividends and income flow to a single cash pool, and withdrawals can be sourced
from the most tax-efficient sleeve. The firm should track client satisfaction
metrics before and after the transition, anticipating improvement in client
comprehension of their portfolio structure and investment strategy.

### Example 3: Reconciliation Break Investigation and Resolution

**Scenario:**

An advisory practice managing $350M across 600 accounts discovers during its
Monday morning reconciliation review that 48 accounts (8% of the total) show
position discrepancies between the PMS and the custodian (Schwab). The breaks
range from minor share-count differences to entirely missing positions. The
operations team needs to diagnose the causes, resolve the breaks, and implement
controls to prevent recurrence.

**Design Considerations:**

**Break classification and diagnosis:**

The operations team categorizes the 48 breaks into root-cause buckets:

| Category | Count | Typical Cause |
|---|---|---|
| Missed corporate action | 18 | A stock split processed at custodian but not reflected in PMS |
| Trade settlement timing | 12 | Friday trades settled at custodian over the weekend but PMS shows pending |
| Data feed failure | 8 | The Saturday custodian file failed to load due to a format change in one field |
| Dividend reinvestment | 6 | DRIP shares added at custodian but PMS not configured for auto-DRIP on these accounts |
| Genuine error | 4 | Trades executed at custodian but not initiated through PMS (advisor placed directly) |

**Resolution workflow:**

1. **Corporate action breaks (18 accounts):** The PMS operations team identifies
   that a widely-held equity (held in 18 accounts) underwent a 3:1 stock split
   on the prior Thursday. The custodian processed the split automatically, but
   the PMS corporate action module failed to pick it up from the data feed. The
   team manually applies the split in the PMS, adjusting share counts and cost
   basis for all 18 accounts.

2. **Settlement timing breaks (12 accounts):** These breaks are expected and
   will self-resolve when Monday's end-of-day reconciliation runs. The team marks
   them as "expected timing difference" and monitors for resolution.

3. **Data feed failure (8 accounts):** The Saturday batch file from Schwab
   contained a format change in the corporate action field that caused the PMS
   file parser to reject the entire file for 8 accounts. The team contacts the
   PMS vendor to update the parser, manually imports the affected data, and
   re-runs reconciliation for those accounts.

4. **DRIP configuration (6 accounts):** Six accounts are configured for dividend
   reinvestment at the custodian but the PMS does not reflect this setting. When
   dividends reinvest into fractional shares, the PMS records a cash dividend
   instead. The team updates the DRIP flag in the PMS for these accounts and
   adjusts positions to match the custodian.

5. **Unauthorized trades (4 accounts):** An advisor placed 4 trades directly
   through the custodian platform without going through the PMS. The team enters
   the trades into the PMS after the fact and counsels the advisor on the
   requirement to use the PMS for all trade activity.

**Controls to reduce future breaks:**

- **Automated corporate action processing:** Configure the PMS to automatically
  apply mandatory corporate actions (splits, mergers) from the custodian data
  feed, with alerts for actions requiring manual review (tenders, elections).
- **Feed monitoring:** Implement automated alerts when custodian data files
  fail to arrive, arrive with unexpected format changes, or contain fewer
  records than expected.
- **DRIP audit:** Run a quarterly audit comparing DRIP settings in the PMS
  against custodian DRIP elections for all accounts.
- **Trade workflow enforcement:** Configure custodian access so that advisors
  cannot place trades directly; all trades must originate from the PMS.
- **Daily break dashboard:** Implement a dashboard showing break counts by
  category, age, and resolution status, with escalation rules for breaks
  older than 3 business days.

**Analysis:**

An 8% break rate is above the industry target of under 2% for well-run operations.
The immediate resolution of the 48 breaks eliminates the risk of incorrect
performance reports or billing. However, the more important outcome is the
implementation of preventive controls. Automated corporate action processing alone
should eliminate the largest break category (37.5% of all breaks). Feed monitoring
prevents silent data-quality failures that can cascade into reporting and billing
errors. The trade workflow enforcement addresses a compliance concern: trades placed
outside the PMS bypass pre-trade compliance checks and block-trading allocations,
creating best-execution and fair-allocation risks. The firm should target a break
rate below 1% within 90 days of implementing these controls and track the metric
weekly in operations meetings.

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

- **asset-allocation** (Layer 4, wealth-management) — PMS implements the strategic
  and tactical asset allocation defined in the client's investment policy. Model
  portfolios in the PMS are the operational expression of asset allocation decisions.
- **rebalancing** (Layer 4, wealth-management) — The PMS rebalancing engine applies
  rebalancing theory (threshold-based, calendar-based, opportunistic) to live client
  portfolios. The rebalancing skill defines the theory; this skill covers the
  system implementation.
- **tax-efficiency** (Layer 5, wealth-management) — PMS tax-loss harvesting,
  wash sale monitoring, and tax-aware rebalancing apply the tax-efficiency
  principles defined in the tax-efficiency skill to operational workflows.
- **performance-metrics** (Layer 1a, wealth-management) — The PMS calculates the
  return metrics (TWR, MWR, alpha, Sharpe ratio) defined in the performance-metrics
  skill. That skill defines the math; this skill covers how the PMS implements the
  calculations.
- **performance-reporting** (Layer 8, wealth-management) — The PMS generates the
  underlying performance data that feeds client-facing performance reports. The
  reporting skill covers presentation and communication; this skill covers
  calculation and data infrastructure.
- **gips-compliance** (Layer 9, compliance) — PMS composite construction and
  performance calculation must satisfy GIPS requirements for firms that claim
  compliance. The GIPS skill defines the standards; this skill covers the PMS
  configuration needed to meet them.
- **order-management-advisor** (Layer 10, advisory-practice) — The OMS receives
  trade lists generated by the PMS. This skill covers trade list generation; the
  OMS skill covers order routing, execution, and allocation.
- **financial-planning-integration** (Layer 10, advisory-practice) — The PMS
  current portfolio (including held-away aggregation) feeds financial planning
  tools for projections and scenario analysis.
- **fee-billing** (Layer 10, advisory-practice) — The PMS fee engine handles
  billing calculations described here. The fee-billing skill covers the broader
  billing operations workflow including invoicing, collections, and revenue
  recognition.
- **client-reporting-delivery** (Layer 10, advisory-practice) — PMS performance
  data, portfolio holdings, and asset allocation feeds the client reporting and
  delivery workflow.
