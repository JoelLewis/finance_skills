---
name: reference-data
description: "Financial reference data: security master, client master, account master, identifiers (CUSIP, ISIN, SEDOL, FIGI), pricing, and reference data governance."
allowed-tools: ["Bash", "Read", "Write", "Edit"]
---

# Reference Data

## Purpose

Guide the design and management of reference data systems for financial services. Covers security master data (instrument identification, classification, terms), client master data (identity, demographics, relationships), account master data (registration, configuration, features), pricing data management, identifier systems (CUSIP, ISIN, SEDOL, FIGI), and reference data governance. Enables building or evaluating reference data infrastructure that serves as a reliable foundation for all downstream systems.

## Layer

13 — Data Integration (Reference Data & Integration)

## Direction

both

## When to Use

- Designing or evaluating a security master database for an advisory firm or asset manager
- Mapping security identifiers across systems (CUSIP to ISIN, SEDOL to FIGI, internal IDs)
- Building or improving a client master data model for onboarding, CRM, or regulatory reporting
- Defining account master attributes and account-to-client relationships across custodians
- Implementing pricing data management with validation, exception handling, and vendor hierarchy
- Establishing reference data governance — ownership, stewardship, quality metrics, change management
- Distributing reference data to downstream systems (portfolio management, trading, reporting, billing)
- Evaluating or integrating data vendors (Bloomberg, Refinitiv, ICE, S&P, Moody's)
- Troubleshooting data quality issues traced to reference data (stale prices, missing identifiers, incorrect classifications)
- Handling identifier changes caused by corporate actions (mergers, spin-offs, ticker changes)
- Trigger phrases: "security master," "CUSIP," "ISIN," "SEDOL," "FIGI," "client master," "account master," "pricing data," "reference data," "golden source," "MDM," "master data," "identifier mapping," "data governance," "pricing validation"

## Core Concepts

### 1. Security Master

The security master is the authoritative repository of instrument-level reference data, serving as the foundation for portfolio management, trading, performance, reporting, and compliance systems.

**Core fields:** Identifiers (CUSIP, ISIN, SEDOL, FIGI, ticker, internal ID), classification (asset class, sub-class, GICS sector, country, currency), issuer information (name, LEI, ratings), terms and conditions (asset-class-specific contractual attributes), and pricing factors (multiplier, day count, settlement convention).

**Asset-class-specific attributes:** Equity (shares outstanding, market cap, sector, exchange, dividend frequency). Fixed income (coupon, maturity, call schedule, credit rating, seniority, day count). Funds (NAV, expense ratio, share class, distribution frequency, load structure). ETFs (NAV, indicative value, expense ratio, underlying index). Options (underlying, strike, expiration, type, multiplier, exercise style). Alternatives (strategy type, vintage year, commitment, capital call schedule, valuation frequency).

**Security lifecycle events:** IPO/listing (new record creation with all required fields), corporate actions (splits, mergers, spin-offs, name/ticker/exchange changes — the single largest source of security master data quality issues), and delisting/maturity (flag as inactive, retain historical record for performance and audit).

**Golden source designation:** The security master should be the firm's golden source for instrument reference data. All downstream systems retrieve security attributes from it rather than maintaining independent copies.

### 2. Identifier Systems

Financial instruments carry multiple overlapping identifiers. No single scheme is universally sufficient.

- **CUSIP** — 9-character (6 issuer + 2 issue + 1 check digit), US/Canada securities, administered by CUSIP Global Services (FactSet). Changes on fundamental term changes (mergers, reorganizations).
- **ISIN** — 12-character (2 country + 9 national ID + 1 check digit), ISO 6166, globally unique. Required for MiFID II, EMIR reporting. Wraps the national identifier (CUSIP in US, SEDOL in UK).
- **SEDOL** — 7-character, assigned by the London Stock Exchange for LSE and UK/Irish listings. A single security may have different SEDOLs per listing exchange.
- **FIGI** — 12-character, developed by Bloomberg under OMG standard. Open-source and freely available (unlike CUSIP/SEDOL). Distinguishes instrument-level, composite, and exchange-level identifiers.
- **Ticker symbols** — Exchange-assigned, not globally unique, change frequently. Never use as a primary identifier; use only for display or trading convenience.
- **Internal identifiers** — Firm-generated (UUID or sequential integer), immutable across the security's life. Serves as the stable key linking all external identifiers.

**Identifier mapping:** The security master must maintain a cross-reference table linking all identifiers per security. Challenges include one-to-many relationships (one ISIN to multiple SEDOLs), temporal changes from corporate actions (versioned mappings for point-in-time lookups), and vendor discrepancies requiring conflict resolution.

### 3. Client Master

The client master is the authoritative repository of client-level reference data supporting onboarding, account management, KYC/AML compliance, reporting, and relationship management.

**Data model:** Individuals (legal name, DOB, SSN/TIN, address, phone, email, citizenship, employment). Entities (legal name, EIN, formation state/country, entity type, formation date). Trusts (trust name, type, grantor, trustee, beneficiaries, governing law).

**Identity management:** Each client must have a single unique identifier regardless of how many accounts or roles they hold. Deduplication is critical for regulatory reporting, household billing, cross-account compliance (wash sales), and unified servicing.

**Household and relationships:** Household grouping links related clients for billing, reporting, and planning. Relationship types include spouse, parent/child, trustee/beneficiary, authorized signer, trusted contact. Advisor assignment (primary, secondary, service team) is tracked here.

**KYC/AML data:** Verification status, method, risk rating, PEP status, OFAC screening results, beneficial ownership (entities), source of funds/wealth, EDD flags.

**Client preferences:** Communication channel, statement delivery, language, investment preferences (ESG exclusions, sector restrictions), tax lot method preference.

**Golden source:** CRM is typically the golden source for relationship and advisory data; custodian is the golden source for regulatory identity data (legal name, SSN, address of record). The client master integrates both and enforces synchronization.

### 4. Account Master

The account master stores attributes and configuration of every client account, linking accounts to clients and driving trading, billing, reporting, and compliance.

**Attributes:** Registration (individual, joint, trust, IRA, Roth, SEP, 401(k), corporate, estate, UGMA/UTMA), account type (advisory, brokerage, wrap, retirement, education, charitable), tax status (taxable, tax-deferred, tax-exempt), custodian, advisor, model assignment, features (margin, options level, DRIP, cost basis method).

**Account-to-client relationships:** Owner, authorized party (POA, trading authorization), beneficiary, trustee, custodian (for UGMA/UTMA).

**Status management:** Active, restricted (regulatory hold, death notification, legal dispute), closed (retain historical data per books-and-records requirements), dormant (escheatment/unclaimed property exposure).

**Cross-system identification:** Custodian account number, PMS account ID, CRM account ID, and billing account ID may all differ. The account master maintains mappings and provides a canonical internal ID as the cross-system key.

### 5. Pricing Data

Pricing is the most time-sensitive reference data category. Incorrect prices propagate immediately into valuations, performance, billing, and compliance.

**End-of-day pricing:** Official exchange close (4:00 PM ET for US equities), mutual fund NAV (available 6:00-7:00 PM ET), evaluated pricing for infrequently traded fixed income (Bloomberg, ICE, Refinitiv models).

**Pricing hierarchy:** Define a preferred source per security type with automatic fallback. Example: US equities — exchange close, then Bloomberg, then Refinitiv. Corporate bonds — ICE evaluated, then Bloomberg BVAL, then Refinitiv. Alternatives — manager/GP valuation, then third-party appraisal, then internal model.

**Stale price detection:** Flag prices unchanged beyond expected thresholds (1 day for liquid equities, 3-5 days for bonds, 30 days for alternatives). Assess portfolio-level impact and resolve via vendor contact, broker quote, or fair value estimate.

**Fair value pricing:** Adjust international securities' closing prices for subsequent market, currency, and news developments when foreign exchanges close hours before the US close. Prevents stale-price arbitrage in mutual funds.

**Pricing validation:** Automated checks before loading — variance check (flag moves exceeding 10-15% for equities, 5% for bonds), zero-price detection, negative-price detection, cross-source comparison, currency verification, stale detection.

**Manual overrides:** Restricted to authorized users, documented with reason and source, logged in an audit trail, time-limited pending vendor correction.

### 6. Reference Data Governance

Governance establishes the structures, policies, and processes ensuring reference data is accurate, complete, timely, and consistent.

**Data ownership:** Each domain has a designated owner — security master (investment operations), client master (co-owned by compliance and advisory practice), account master (operations/client services), pricing (portfolio accounting/valuation). Owners are accountable for quality and authorize changes to definitions and sources.

**Data stewardship:** Stewards execute governance daily — monitoring quality dashboards, resolving exceptions, coordinating with vendors, approving overrides, maintaining data dictionaries.

**Data quality metrics:** Completeness (percentage of records with all required fields), accuracy (percentage matching the authoritative source), timeliness (percentage updated within the expected window), consistency (same value across all systems).

**MDM patterns:** Registry (links only, no conflict resolution), consolidation (read-only golden record aggregated from sources), coexistence (bidirectional sync between MDM and sources), transaction/hub (single system of entry for all reference data).

**Change management:** Impact analysis before changes, non-production testing, downstream notification, rollback procedures, post-change validation.

**Audit trail:** Log every change with old value, new value, timestamp, user/process, and reason. Required for regulatory examination, dispute resolution, and root-cause analysis.

### 7. Reference Data Distribution

Mastered reference data must be distributed reliably to all consuming systems.

**Publishing models:** Event-driven/push (message bus or event stream for near-real-time propagation), polling/pull (scheduled queries — simpler but introduces latency), bulk/files (CSV/XML/JSON via SFTP or S3 for EOD snapshots), API/on-demand (point-of-need retrieval — eliminates cache staleness but creates runtime dependency).

**Delta distribution:** Send only changed records since the last distribution. Requires change tracking, sequencing, and full-refresh fallback capability.

**Caching:** Local caching in consuming systems reduces latency but risks staleness. Mitigate with TTL policies, event-driven cache invalidation, and version numbers.

**Point-in-time retrieval:** Support queries for the state of any record as of a specific date. Required for historical performance, regulatory reporting, and audit. Implement via effective-date/expiration-date columns or full history tables.

### 8. Vendor Management

Data vendors are the primary external source for security reference data, pricing, ratings, and identifiers.

**Major vendors:** Bloomberg (broad coverage, FIGI, real-time pricing), Refinitiv/LSEG (global coverage, evaluated pricing), ICE Data Services (fixed income pricing, indices), S&P Global (ratings, CUSIP, fundamentals), Moody's (credit ratings, risk data), FactSet (multi-source aggregation, CUSIP Global Services), MSCI (ESG ratings, factor data, indices).

**Evaluation criteria:** Coverage (asset classes, geographies), quality (accuracy, completeness, error correction), timeliness (availability relative to processing deadlines), format/delivery (API, file, schema stability), licensing terms (redistribution rights, per-user fees), cost (total cost of ownership), support quality.

**Multi-vendor strategy:** Source critical data from at least two vendors — primary, backup, and arbitration rules for disagreements.

**Vendor monitoring:** Track file arrival times, monitor record counts for unexpected drops, compare against independent sources, maintain quarterly vendor scorecards, escalate persistent quality issues.

## Worked Examples

### Example 1: Designing a Security Master for a Multi-Custodian Advisory Firm

**Scenario:** An RIA manages $1.2B across 1,500 accounts at Schwab and Fidelity, trading US/international equities, ETFs, mutual funds, corporate bonds, and municipal bonds. Each custodian feed populates separate security tables — no unified security master exists. Recurring issues: the same mutual fund appears with different names per custodian, corporate bonds lack consistent credit ratings, and a stock split was processed for Schwab but missed for Fidelity because corporate actions were handled independently.

**Design considerations:** The firm defines a security master record with immutable internal UUID, all external identifiers (CUSIP, ISIN, SEDOL, FIGI, ticker, custodian-specific IDs), classification fields (asset class, GICS sector, credit tier), issuer data (name, LEI, country), asset-class-specific terms, pricing fields, and status. A cross-reference table links each internal ID to all external identifiers with effective dates for point-in-time lookups. Bloomberg is the primary vendor for reference data and pricing; ICE is secondary for fixed income; custodian feeds provide reconciliation checks; CUSIP Global Services provides identifier change notifications. All corporate actions are processed through the security master first, then propagated to both custodians — eliminating inconsistent processing. Data quality controls include daily completeness and pricing validation checks, weekly cross-vendor pricing comparison, and monthly classification audits.

**Analysis:** The centralized security master eliminates the root cause — disparate, unreconciled security data. The internal UUID survives corporate actions, identifier changes, and custodian transitions. The most significant ongoing cost is the corporate action workflow, requiring a dedicated data operations analyst as security master steward.

### Example 2: Implementing Pricing Data Management with Validation and Exception Handling

**Scenario:** An asset manager runs nightly valuations for 30 separate accounts and 5 commingled funds holding 2,000 securities (US/international equities, corporate/municipal bonds, MBS). Pricing comes from a single vendor (Refinitiv). Past incidents: a municipal bond valued at zero for three days unnoticed, an international equity stale for a week during a local holiday, a corporate bond evaluated price off by 15% due to vendor error.

**Design considerations:** The firm establishes a tiered pricing hierarchy per asset class with automatic fallback (e.g., corporate bonds: ICE evaluated, then Refinitiv, then Bloomberg BVAL). Automated validation runs before loading: variance check (15% equity, 5% bonds), zero-price check, stale-price check (2 days equities, 5 days bonds, adjusted for local holidays), cross-vendor comparison (flag >2% divergence for fixed income), currency verification, reasonableness bounds. Exceptions are severity-classified (critical/high/medium/low) and appear on a pricing dashboard. Critical exceptions trigger immediate alerts; the pricing analyst investigates, resolves (accept with documentation, substitute from backup vendor, or manual override), and logs all actions. Unresolved exceptions escalate after defined time windows. For international equities, a fair value model adjusts foreign closing prices using US market movement, currency changes, and sector ETF data.

**Analysis:** The framework transforms pricing from passive receipt to active quality control. Multi-vendor hierarchy eliminates single-vendor dependency. Automated validation catches all three prior incident types. A well-run pricing operation targets exception rates below 2% of the universe per day, with same-day resolution for critical and high-severity exceptions.

### Example 3: Building Client Master Data Governance for Regulatory Compliance

**Scenario:** A wealth management firm serving 3,000 households discovers poor client data quality: 12% incomplete addresses, 8% stale employment data (clients known to be retired still listed as employed), 5% of entity clients missing beneficial ownership documentation, and inconsistent household groupings causing billing errors (missing breakpoint discounts). Client data exists in three systems (Salesforce CRM, Schwab custodian, Orion PMS) with no designated golden source and divergent records. The firm must remediate and establish governance before FinCEN's 2026 investment adviser AML/CIP requirements.

**Design considerations:** Data owners are assigned by domain: client identity (CCO — regulatory significance), client relationships (Head of Client Services — servicing and billing), client financial profile (CIO — suitability). Golden sources: Schwab for legal identity data (verified through CIP, used for 1099s), Salesforce for relationship/advisory data, Orion as a consumer only (synchronized from the other two, not edited directly). Remediation: incomplete addresses resolved by cross-referencing CRM against custodian and contacting clients for gaps (target 100% in 90 days); stale employment flagged for clients 60+ not updated in two years, with automated triggers when systematic withdrawals begin; missing beneficial ownership collected using FinCEN forms, prioritized by account size (target 100% in 60 days); household groupings identified via shared addresses/phones/names, confirmed by advisors, with overbilling refunds issued. Ongoing governance: daily automated quality checks with exception dashboard, weekly steward review of trends, monthly metrics reporting to operations committee, quarterly governance review with data owners, annual comprehensive data refresh for inactive clients.

**Analysis:** The program addresses both immediate gaps and structural causes. Golden source designation eliminates cross-system ambiguity. The remediation requires significant advisor engagement, best positioned as a client service improvement. FinCEN's 2026 effective date creates additional urgency for complete, verified client identity data.

## Common Pitfalls

1. **Using ticker symbols as primary identifiers.** Tickers are not globally unique, change frequently, and are recycled. Systems keyed on tickers break during corporate actions.
2. **Maintaining separate security records per custodian.** The same instrument appears as multiple securities, causing duplicated positions and inconsistent corporate action processing.
3. **Treating pricing as passive data receipt.** Loading vendor prices without validation allows zero prices, stale prices, and vendor errors to propagate into valuations and billing.
4. **No designated golden source for client data.** Multiple systems maintaining client data without hierarchy causes drift, conflicts, and no authoritative record.
5. **Ignoring temporal versioning.** Overwriting current state without preserving history prevents point-in-time reporting, historical performance, and audit support.
6. **Underinvesting in corporate action processing.** Corporate actions are the primary source of security master failures — treating them as low-priority clerical work causes persistent reconciliation breaks.
7. **Single-vendor pricing dependency.** No backup source means manual pricing when the vendor is late, missing, or incorrect — which does not scale.
8. **Neglecting data quality metrics.** Without measuring completeness, accuracy, timeliness, and consistency, issues are invisible until they cause downstream failures.
9. **Point-to-point integrations instead of central reference data service.** Each consuming system connecting directly to vendors creates N redundant copies with independent quality issues.
10. **Failing to plan for identifier changes during corporate actions.** Systems that do not handle CUSIP/ISIN/ticker changes gracefully lose position history and break performance chains.

## Cross-References

- **market-data** (Layer 13, data-integration) — Market data covers real-time pricing and trade data; reference data provides the instrument master that market data references.
- **data-quality** (Layer 13, data-integration) — General data quality principles (profiling, validation, monitoring) applied here specifically to financial reference data.
- **integration-patterns** (Layer 13, data-integration) — Integration patterns (event-driven, batch, API) are the mechanisms for distributing reference data.
- **portfolio-management-systems** (Layer 10, advisory-practice) — The PMS is a primary consumer of security master, pricing, and account master data.
- **reconciliation** (Layer 13, data-integration) — Reference data mismatches (identifiers, stale prices) are a leading cause of reconciliation breaks.
- **corporate-actions** (Layer 13, data-integration) — Corporate actions drive security master changes; this skill covers the resulting reference data updates.
- **know-your-customer** (Layer 9, compliance) — KYC requirements define what client data must be collected; the client master stores and governs it.
- **books-and-records** (Layer 9, compliance) — Reference data records are books and records subject to retention and examination requirements.
