# Finance Skills — Implementation Plan

## Overview

A mono-repo of Claude Code skill plugins for financial services. Each plugin is a
self-contained domain of skills that can be installed independently into a project's
`.claude/skills/` directory. Plugins declare dependencies on other plugins and share
a common skill template.

All **81 skills** are implemented across seven plugins (`core`, `wealth-management`,
`compliance`, `advisory-practice`, `trading-operations`, `client-operations`,
`data-integration`).

---

## Plugin Architecture

### Design Principles
- **`core` is implicit** — always installed; every plugin depends on it
- **Plugins are independently installable** — a project pulls only the domains it needs
- **Cross-plugin references are allowed** — skills reference related skills in other plugins via cross-references section
- **Skills live in `.claude/skills/`** — installation symlinks a plugin's skills into the target project's skill directory
- **No Python scripts for guidance-only skills** — compliance/operations plugins are guidance-only; quantitative plugins may have `scripts/` subdirectories

### Plugin Dependency Graph

```
core (implicit — always installed)
  ├── wealth-management
  ├── compliance  ←── (recommended for all plugins)
  ├── advisory-practice  ←── depends on wealth-management
  ├── trading-operations
  ├── client-operations
  └── data-integration
```

### Installation Model

```bash
# Install a plugin into a target project
./install.sh --plugin wealth-management --target /path/to/project

# This symlinks:
#   plugins/core/skills/*           → /path/to/project/.claude/skills/
#   plugins/wealth-management/skills/* → /path/to/project/.claude/skills/
```

Each plugin directory contains:
```
plugins/<plugin-name>/
├── plugin.json          # Metadata: name, description, dependencies, skill list
└── skills/
    ├── <skill-name>/
    │   ├── SKILL.md
    │   └── scripts/     # (optional) Python reference implementations
    └── ...
```

---

## Plugins

### 1. `core` (Implicit Foundation) — 3 skills ✅

Mathematical and statistical foundations required by all other plugins.

| Skill | Description | Script |
|-------|-------------|--------|
| return-calculations | TWR, MWR/IRR, CAGR, annualization, sub-period linking | ✅ |
| time-value-of-money | PV, FV, NPV, IRR, annuities, amortization | ✅ |
| statistics-fundamentals | Distributions, covariance, regression, bootstrapping | ✅ |

### 2. `wealth-management` — 31 skills ✅

Investment knowledge for personal and institutional wealth management. Consumer/advisor-facing investment domain.

| Layer | Skills | Count |
|-------|--------|-------|
| 1a — Realized Risk | historical-risk, performance-metrics | 2 |
| 1b — Forward Risk | forward-risk, volatility-modeling | 2 |
| 2 — Asset Classes | equities, fixed-income-sovereign, fixed-income-municipal, fixed-income-corporate, fixed-income-structured, commodities, real-assets, alternatives, fund-vehicles, currencies-and-fx, digital-assets | 11 |
| 3 — Valuation | quantitative-valuation, qualitative-valuation | 2 |
| 4 — Portfolio Construction | diversification, asset-allocation, bet-sizing, rebalancing | 4 |
| 5 — Policy & Planning | investment-policy, tax-efficiency, performance-attribution | 3 |
| 6 — Personal Finance | debt-management, lending, emergency-fund, savings-goals, liquidity-management | 5 |
| 7 — Behavioral Finance | finance-psychology | 1 |
| 8 — Reporting | performance-reporting | 1 |

**Python scripts completed:** historical-risk, performance-metrics (Layer 1a). Remaining layers pending.

### 3. `compliance` — 16 skills ✅

Regulatory guidance for US securities law compliance. Guidance-only (no Python scripts). Skills flag problems to design around and share distilled takes from public compliance guides, enforcement actions, and industry practice.

| Skill | Primary Sources |
|-------|----------------|
| investment-suitability | FINRA Rules 2111, 2090; Regulatory Notices |
| know-your-customer | FINRA Rule 2090; CDD Rule (31 CFR 1010.230); USA PATRIOT Act §326 |
| anti-money-laundering | BSA; FinCEN; FINRA Rule 3310; OFAC |
| reg-bi | SEC Reg BI (17 CFR 240.15l-1); SEC Staff Bulletins |
| fiduciary-standards | IA Act §206; SEC 2019 Interpretation; ERISA §404; DOL rules |
| fee-disclosure | ADV Part 2A Item 5; SEC prospectus rules; Reg BI disclosure |
| advice-standards | IA Act §202(a)(11); SEC releases; Reg BI "recommendation" definition |
| sales-practices | FINRA Rules 2010, 2020, 3110, 3270, 3280; enforcement actions |
| advertising-compliance | SEC Marketing Rule (206(4)-1); FINRA Rule 2210 |
| client-disclosures | Form ADV; Form CRS; Reg S-P; prospectus delivery rules |
| conflicts-of-interest | Reg BI COI obligation; IA Act fiduciary duty; FINRA compensation rules |
| books-and-records | SEC 17a-3/17a-4 (BDs), Rule 204-2 (IAs), FINRA retention, WORM, e-comms archiving |
| regulatory-reporting | Form PF, 13F/13H, Form ADV amendments, FOCUS reports, blue sheets, CAT reporting |
| gips-compliance | CFA Institute GIPS standards, composite construction, performance presentation, verification |
| privacy-data-security | Reg S-P, Reg S-ID, SEC cybersecurity rules (2023), state privacy law intersections |
| examination-readiness | SEC/FINRA exam process, document production, deficiency findings, mock exam frameworks |

### 4. `advisory-practice` (Front Office) — 10 skills ✅

Advisor-facing systems and workflows. Teaches Claude how advisor platforms work so it can help design, evaluate, or integrate with them.

| Skill | Coverage |
|-------|----------|
| client-onboarding | Digital onboarding flows, document collection, KYC integration, account opening forms, e-signature |
| crm-client-lifecycle | Client segmentation, household management, service tiers, review scheduling, retention |
| portfolio-management-systems | Model portfolios, sleeve-based management, UMA/SMA, drift monitoring, held-away aggregation |
| order-management-advisor | Advisor order entry, block trading, allocation, order types, pre-trade compliance |
| financial-planning-integration | Planning tool data flows, goal-based plans, Monte Carlo, plan-to-portfolio linkage |
| proposal-generation | Investment proposals, risk profiling output, model recommendation, fee illustration |
| advisor-dashboards | Practice analytics (AUM, revenue, flows), client dashboards, exception/alert dashboards |
| next-best-action | Event-driven triggers (rebalance, large cash, life event), prioritization, action queuing |
| fee-billing | Fee calculation (tiered, flat, breakpoint), billing cycles, collection methods, revenue recognition |
| client-reporting-delivery | Report generation, customization, delivery channels, frequency management |

### 5. `trading-operations` (Order Lifecycle & Execution) — 9 skills ✅

Order lifecycle from entry through settlement, plus operational risk. Serves multiple front-ends (advisor, algorithmic, client-direct).

| Skill | Coverage |
|-------|----------|
| order-lifecycle | Order states, FIX protocol basics, order types, time-in-force, cancel/replace workflows |
| trade-execution | Best execution, venues (exchanges, ATS, market makers), smart order routing, TCA |
| pre-trade-compliance | Automated rule checks, concentration limits, restricted lists, hard/soft blocks |
| post-trade-compliance | Trade surveillance, pattern detection, best execution review, allocation fairness |
| settlement-clearing | T+1, DTC/NSCC, fails management, corporate actions on settlement, DVP/RVP |
| exchange-connectivity | Venue connectivity, market data feeds, FIX sessions, trading halts, circuit breakers |
| margin-operations | Reg T, maintenance margin, portfolio margin, margin calls, liquidation waterfall, SBLOC |
| operational-risk | Trade breaks, settlement fails, error handling, loss event taxonomy, key risk indicators |
| counterparty-risk | Counterparty exposure, credit risk monitoring, netting, collateral management |

### 6. `client-operations` (Account Lifecycle & Servicing) — 8 skills ✅

Back-office account operations and servicing workflows.

| Skill | Coverage |
|-------|----------|
| account-opening-workflow | Account types, required docs, approval workflows, NIGO management, regulatory holds |
| account-opening-compliance | CIP/KYC integration, suitability checks, OFAC screening, beneficial ownership |
| account-maintenance | Address changes, beneficiary updates, re-registration, cost basis, restrictions |
| account-transfers | ACAT, non-ACAT, partial transfers, journal entries, rollovers, estate transfers |
| reconciliation | Position/cash/transaction recon, break identification, three-way reconciliation |
| corporate-actions | Mandatory/voluntary actions, dividends, splits, M&A, tender offers, record dates |
| stp-automation | STP design, exception-based workflow, STP rate metrics, integration patterns |
| workflow-automation | BPM concepts, task routing, approval chains, escalation, SLA monitoring, case management |

### 7. `data-integration` (Reference Data & Integration) — 4 skills ✅

Data foundations that every system depends on.

| Skill | Coverage |
|-------|----------|
| reference-data | Security master, client master, account master, identifiers (CUSIP/ISIN/SEDOL), pricing |
| market-data | Real-time vs delayed, Level 1/2/3, data vendors, consolidated tape, licensing |
| integration-patterns | API design for financial systems, FIX, ISO 20022, file-based, event-driven, idempotency |
| data-quality | Golden source, data lineage, validation rules, exception management, governance |

---

## Skill Count Summary

| Plugin | Skills | Status |
|--------|--------|--------|
| core | 3 | ✅ |
| wealth-management | 31 | ✅ |
| compliance | 16 | ✅ |
| advisory-practice | 10 | ✅ |
| trading-operations | 9 | ✅ |
| client-operations | 8 | ✅ |
| data-integration | 4 | ✅ |
| **Total** | **81** | |

---

## Future Scope (Not Currently Planned)

| Domain | Priority | Notes |
|--------|----------|-------|
| Banking operations (deposits, payments, lending origination) | **High** | Revisit as a future plugin |
| Fund administration / transfer agency | Low | Separate industry vertical |
| Insurance product operations | Low | Separate regulatory regime |
| Institutional trading (dark pools, swaps, prime brokerage) | Low | Consider if demand arises |

---

## Repository Structure

Skills live in `plugins/<plugin-name>/skills/`. The `install.sh` script symlinks
them into a target project's `.claude/skills/` directory.

```
finance_skills/
├── README.md                            # Usage and plugin overview
├── PLAN.md                              # This file
├── CLAUDE.md                            # Project-level Claude instructions
├── LICENSE
├── install.sh                           # Plugin installer
│
└── plugins/
    ├── core/
    │   ├── plugin.json
    │   └── skills/
    │       ├── return-calculations/
    │       │   ├── SKILL.md
    │       │   └── scripts/return_calculations.py ✅
    │       ├── time-value-of-money/
    │       │   ├── SKILL.md
    │       │   └── scripts/time_value_of_money.py ✅
    │       └── statistics-fundamentals/
    │           ├── SKILL.md
    │           └── scripts/statistics_fundamentals.py ✅
    ├── wealth-management/
    │   ├── plugin.json
    │   └── skills/                      # 31 skills
    │       ├── historical-risk/         # scripts/historical_risk.py ✅
    │       ├── performance-metrics/     # scripts/performance_metrics.py ✅
    │       └── ... (29 more)
    ├── compliance/
    │   ├── plugin.json
    │   └── skills/                      # 16 skills, guidance-only
    ├── advisory-practice/
    │   ├── plugin.json
    │   └── skills/                      # 10 skills (8 implemented)
    ├── trading-operations/
    │   ├── plugin.json
    │   └── skills/                      # 9 skills
    ├── client-operations/
    │   ├── plugin.json
    │   └── skills/                      # 8 skills (7 implemented)
    └── data-integration/
        ├── plugin.json
        └── skills/                      # 4 skills (2 implemented)
```

---

## SKILL.md Template

Each skill follows this structure:

```markdown
---
name: <skill-name>
description: <one-line description used for skill matching>
allowed-tools: ["Bash", "Read", "Write", "Edit"]
---

# <Skill Title>

## Purpose
What this skill enables Claude to do.

## Layer
N — Layer Name

## Direction
retrospective | prospective | both

## When to Use
- Trigger phrases and situations

## Core Concepts
### <Concept>
Explanation with formulas.

## Key Formulas (optional — omit for non-quantitative skills)
| Formula | Expression | Use Case |

## Worked Examples
### Example 1: <title>
**Given:** ... **Calculate:** ... **Solution:** ...
(Compliance/operations skills use scenario-based examples:
**Scenario:** ... **Compliance Issues:** ... **Analysis:** ...)

## Common Pitfalls
- Things to watch out for

## Cross-References
- Related skills

## Reference Implementation (optional — omit for guidance-only skills)
See `scripts/<name>.py` for computational helpers.
```

---

## Cross-Plugin Connection Registry

| Connection | Skills Involved | Nature |
|-----------|----------------|--------|
| Amortization math | time-value-of-money → lending, debt-management | Shared formulas |
| Margin/SBLOC liquidity | lending ↔ liquidity-management | Cross-reference |
| Borrowing vs repayment | lending ↔ debt-management | Cross-reference |
| Behavioral valuation | qualitative-valuation ↔ finance-psychology | Cross-reference |
| Retro/prospective chain | performance-metrics → performance-attribution → performance-reporting | Data flow |
| Prospective → allocation | forward-risk, volatility-modeling → asset-allocation | Input/output |
| Covariance matrix flow | statistics-fundamentals → historical-risk, forward-risk, diversification, asset-allocation | Shared computation |
| Return math flow | return-calculations → nearly every skill | Foundation |
| Suitability → policy | investment-suitability → investment-policy | Suitability obligations inform IPS constraints |
| KYC → suitability | know-your-customer → investment-suitability, reg-bi | Customer profile feeds suitability/BI analysis |
| KYC → AML | know-your-customer → anti-money-laundering | CDD/CIP feeds AML monitoring |
| Fiduciary vs Reg BI | fiduciary-standards ↔ reg-bi | Parallel standards for IAs vs BDs |
| Advice line | advice-standards → fiduciary-standards, reg-bi | Determines which standard applies |
| Fee transparency | fee-disclosure → fund-vehicles, investment-policy | Fee rules constrain product/policy design |
| Sales oversight | sales-practices → investment-suitability, reg-bi | Supervision enforces suitability/BI |
| Marketing rules | advertising-compliance → performance-reporting, performance-metrics | Constrains how performance can be presented |
| Disclosure docs | client-disclosures → fee-disclosure, conflicts-of-interest | Delivery vehicles for fee and COI disclosures |
| COI across layer | conflicts-of-interest → reg-bi, fiduciary-standards, sales-practices | COI obligation embedded in multiple standards |
| Records foundation | books-and-records → client-disclosures, sales-practices, anti-money-laundering | Retention rules underpin all compliance recordkeeping |
| Reporting mechanics | regulatory-reporting → anti-money-laundering, client-disclosures, know-your-customer | Filing obligations tie to KYC, AML, and disclosure data |
| GIPS performance chain | gips-compliance → performance-metrics, performance-attribution, performance-reporting | GIPS constrains calculation, attribution, and presentation |
| Privacy data flows | privacy-data-security → client-disclosures, know-your-customer, books-and-records | NPI protection overlays disclosure, KYC, and retention |
| Exam readiness umbrella | examination-readiness → all compliance skills | Exam preparation draws on every compliance domain |

---

## Implementation Status

### Phase 1: SKILL.md Files
- [x] core (3 skills)
- [x] wealth-management (31 skills)
- [x] compliance (16 skills)
- [x] advisory-practice (10 skills)
- [x] trading-operations (9 skills)
- [x] client-operations (8 skills)
- [x] data-integration (4 skills)

### Phase 2: Python Reference Implementations (quantitative plugins only)
- [x] core scripts (return-calculations, time-value-of-money, statistics-fundamentals)
- [x] wealth-management Layer 1a scripts (historical-risk, performance-metrics)
- [ ] wealth-management remaining scripts
- [ ] trading-operations scripts (where applicable)

### Phase 3: Plugin Reorganization
- [x] Create `plugins/` directory structure
- [x] Move existing skills into plugin subdirectories
- [x] Create `plugin.json` manifests for each plugin
- [x] Build `install.sh` installer script
- [ ] Update skill cross-references for plugin-relative paths

---

## Conventions

- **Python version**: 3.11+ (scripts are standalone helpers, no package install needed)
- **Dependencies**: numpy, scipy, pandas only (stdlib preferred where possible)
- **Scripts**: Each skill's `scripts/` dir contains runnable Python with clear functions
- **Formulas in SKILL.md**: LaTeX-style notation for clarity
- **Direction labeling**: Every concept tagged as retrospective or prospective
- **Compliance/operations conventions**: Guidance-only skills (no Python scripts). Worked examples use scenario-based format (**Scenario / Compliance Issues / Analysis**). Primary sources cited inline (rule numbers, act sections, form references).
- **Naming**: Skill directories use `lowercase-hyphenated`; Python files use `lowercase_underscore`
