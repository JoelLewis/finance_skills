# Finance Skills

A mono-repo of Claude Code skill plugins for financial services. Each plugin is a
self-contained domain of skills that can be installed independently into any project's
`.claude/skills/` directory, giving Claude deep expertise in that financial domain.

## What Are Plugins?

Each plugin is a collection of SKILL.md files (and optional Python reference scripts)
that teach Claude domain knowledge. When installed, Claude can:

- Answer domain-specific questions with regulatory citations and worked examples
- Flag compliance concerns during design discussions
- Generate and explain financial computations
- Assist with building, evaluating, or integrating with financial systems

Plugins are independently installable — pull only the domains your project needs. The
`core` plugin is implicit and always included.

---

## Plugins

### `core` — Mathematical Foundations

Always installed. Provides the math that every other plugin builds on.

| Skill | What Claude can do |
|-------|-------------------|
| `return-calculations` | Compute TWR, MWR/IRR, CAGR, sub-period linking, annualization |
| `time-value-of-money` | PV, FV, NPV, IRR, annuities, amortization schedules |
| `statistics-fundamentals` | Distributions, covariance matrices, regression, bootstrapping |

Python reference scripts included for all three skills.

---

### `wealth-management` — Investment Knowledge

Investment knowledge for personal and institutional wealth management. Covers the full
investment lifecycle from risk measurement through reporting.

**Risk measurement:** Historical volatility estimators, drawdown analysis, historical
VaR, parametric VaR, Monte Carlo VaR, CVaR/Expected Shortfall, GARCH, implied
volatility surfaces.

**Asset classes:** Equities (factors, index construction, earnings), fixed income
(sovereign, municipal, corporate, structured), commodities, real assets, alternatives,
fund vehicles, currencies and FX, digital assets.

**Valuation:** Quantitative models (DCF, DDM, comparables, residual income) and
qualitative assessment (moats, management quality, ESG).

**Portfolio construction:** Diversification theory, mean-variance optimization,
Black-Litterman, risk parity, Kelly criterion, position sizing, calendar- and
threshold-based rebalancing.

**Policy and planning:** IPS construction, tax-aware investing, asset location,
tax-loss harvesting, performance attribution (Brinson, factor-based).

**Personal finance:** Debt prioritization, mortgage and loan analysis, emergency fund
sizing, savings goals, liquidity management.

**Behavioral finance:** Cognitive biases, nudges, emotional discipline.

**Reporting:** Risk-adjusted performance ratios, performance reports, benchmark
comparison, goal progress tracking.

31 skills. Python scripts for quantitative skills (risk, performance metrics, and core
math).

---

### `compliance` — US Securities Regulatory Guidance

Guidance-only (no Python scripts). Skills teach Claude how to flag problems and share
distilled knowledge from public compliance guides, SEC/FINRA enforcement actions, and
industry practice. All skills cite specific rule numbers and act sections.

| Skill | Coverage |
|-------|----------|
| `investment-suitability` | FINRA Rules 2111/2090, reasonable-basis/customer-specific/quantitative suitability |
| `know-your-customer` | CIP, CDD, beneficial ownership, customer profiling, EDD |
| `anti-money-laundering` | BSA/AML, CTRs, SARs, OFAC screening, structuring detection |
| `reg-bi` | SEC Reg BI disclosure, care, conflict of interest, and compliance obligations |
| `fiduciary-standards` | IA Act §206, SEC 2019 Interpretation, ERISA §404, DOL rules |
| `fee-disclosure` | ADV Part 2A Item 5, Reg BI cost disclosure, 12b-1, wrap fees, ERISA 408(b)(2) |
| `advice-standards` | IA Act §202(a)(11), the investment advice vs. education bright line |
| `sales-practices` | Churning, breakpoint abuse, selling away, unauthorized trading, supervision |
| `advertising-compliance` | SEC Marketing Rule (206(4)-1), FINRA Rule 2210, performance advertising |
| `client-disclosures` | Form ADV, Form CRS, Reg S-P, trade confirmations, delivery timing |
| `conflicts-of-interest` | Reg BI COI obligation, fiduciary duty, FINRA compensation rules |
| `books-and-records` | SEC 17a-3/17a-4, Rule 204-2, WORM storage, electronic communications archiving |
| `regulatory-reporting` | Form PF, 13F/13H, Form ADV amendments, FOCUS reports, CAT reporting |
| `gips-compliance` | CFA Institute GIPS: composites, performance presentation, verification |
| `privacy-data-security` | Reg S-P, Reg S-ID, SEC cybersecurity rules (2023), state privacy law |
| `examination-readiness` | SEC/FINRA exam process, document production, deficiency findings, mock exam frameworks |

16 skills.

---

### `advisory-practice` — Front Office Systems

Teaches Claude how advisor platforms work so it can help design, evaluate, or integrate
with them. Covers the full advisor workflow from client onboarding through reporting.

| Skill | Coverage |
|-------|----------|
| `client-onboarding` | Digital onboarding, document collection, KYC integration, e-signature, NIGO handling |
| `crm-client-lifecycle` | Client segmentation, household management, service tiers, review scheduling |
| `portfolio-management-systems` | Model portfolios, sleeve/UMA/SMA management, drift monitoring, held-away aggregation |
| `order-management-advisor` | Advisor order entry, block trading, allocation, pre-trade compliance |
| `financial-planning-integration` | Planning tool data flows, goal-based plans, Monte Carlo, plan-to-portfolio linkage |
| `proposal-generation` | Risk profiling output, model recommendation, fee illustration, compliance review |
| `advisor-dashboards` | Practice analytics, AUM/revenue/flows, exception and alert dashboards |
| `next-best-action` | Event-driven triggers, prioritization scoring, advisor nudges, automated workflows |
| `fee-billing` | Fee calculation (tiered, flat, breakpoint), billing cycles, revenue recognition |
| `client-reporting-delivery` | Report generation, delivery channels, frequency management, compliance review |

10 skills.

---

### `trading-operations` — Order Lifecycle and Execution

Order lifecycle from entry through settlement. Serves advisor, algorithmic, and
client-direct trading contexts.

| Skill | Coverage |
|-------|----------|
| `order-lifecycle` | Order states, FIX protocol basics, order types, time-in-force, cancel/replace |
| `trade-execution` | Best execution, venues, smart order routing, TCA |
| `pre-trade-compliance` | Rule engines, concentration limits, restricted lists, hard/soft blocks |
| `post-trade-compliance` | Trade surveillance, pattern detection, best execution review, allocation fairness |
| `settlement-clearing` | T+1, DTC/NSCC, fails management, corporate actions on settlement, DVP/RVP |
| `exchange-connectivity` | Venue connectivity, market data feeds, FIX sessions, trading halts, circuit breakers |
| `margin-operations` | Reg T, maintenance margin, portfolio margin, margin calls, liquidation waterfall |
| `operational-risk` | Trade breaks, settlement fails, error handling, loss event taxonomy, KRIs |
| `counterparty-risk` | Counterparty exposure, credit risk monitoring, netting, collateral management |

9 skills.

---

### `client-operations` — Account Lifecycle and Servicing

Back-office account operations and servicing workflows.

| Skill | Coverage |
|-------|----------|
| `account-opening-workflow` | Account types, required docs, approval workflows, NIGO management, regulatory holds |
| `account-opening-compliance` | CIP/KYC integration, suitability checks, OFAC screening, beneficial ownership |
| `account-maintenance` | Address changes, beneficiary updates, re-registration, cost basis, restrictions |
| `account-transfers` | ACAT, non-ACAT, partial transfers, journal entries, rollovers, estate transfers |
| `reconciliation` | Position/cash/transaction recon, break identification, three-way reconciliation |
| `corporate-actions` | Mandatory/voluntary actions, dividends, splits, M&A, tender offers, record dates |
| `stp-automation` | STP design, exception-based workflow, STP rate metrics, integration patterns |
| `workflow-automation` | BPM concepts, task routing, approval chains, escalation, SLA monitoring |

8 skills.

---

### `data-integration` — Reference Data and Integration

Data foundations that every financial system depends on.

| Skill | Coverage |
|-------|----------|
| `reference-data` | Security master, client master, account master, CUSIP/ISIN/SEDOL/FIGI, pricing |
| `market-data` | Real-time vs delayed, Level 1/2/3, data vendors, consolidated tape, licensing |
| `integration-patterns` | API design for financial systems, FIX, ISO 20022, event-driven, idempotency |
| `data-quality` | Golden source, data lineage, validation rules, exception management, governance |

4 skills.

---

## Marketplace Config

`marketplace.json` is a machine-readable catalog of every plugin in this repo. It
aggregates each plugin's name, description, version, dependencies, skill list, and
tags into a single document for use by tooling, CI, and the `install.sh --list`
command.

```bash
# Inspect the full catalog
cat marketplace.json | python3 -m json.tool
```

Each entry mirrors the corresponding `plugin.json` but is consolidated at the repo
level, making it the authoritative source for plugin discovery without requiring
directory traversal.

---

## Installation

### Prerequisites

- A project with a `.claude/` directory (Claude Code project)
- Bash shell (macOS, Linux, or WSL)

### Install a Plugin

```bash
# Clone this repo
git clone <repo-url> finance_skills
cd finance_skills

# Install a single plugin into your project
./install.sh --plugin wealth-management --target /path/to/your/project

# Install multiple plugins
./install.sh --plugin compliance --target /path/to/your/project
./install.sh --plugin advisory-practice --target /path/to/your/project

# Install all plugins
./install.sh --plugin all --target /path/to/your/project
```

The installer:
1. Always installs `core` (implicit dependency of every plugin)
2. Installs any declared plugin dependencies first
3. Symlinks each skill directory into `<target>/.claude/skills/`

### What Gets Installed

```
your-project/
└── .claude/
    └── skills/
        ├── return-calculations/    # from core
        ├── time-value-of-money/    # from core
        ├── statistics-fundamentals/ # from core
        ├── historical-risk/        # from wealth-management
        └── ...
```

Skills are symlinked (not copied), so updates to this repo are reflected immediately.

### Verify Installation

After installing, Claude will automatically pick up the skills. You can verify by
checking the symlinks:

```bash
ls -la /path/to/your/project/.claude/skills/
```

---

## Plugin Dependency Graph

```
core (implicit — always installed)
  ├── wealth-management
  ├── compliance  ←── (recommended for all plugins)
  ├── advisory-practice  ←── depends on wealth-management
  ├── trading-operations
  ├── client-operations
  └── data-integration
```

Installing `advisory-practice` automatically installs `core` and `wealth-management`.
Installing any plugin automatically installs `core`.

---

## Repository Structure

```
finance_skills/
├── README.md
├── PLAN.md                    # Architecture and implementation roadmap
├── CLAUDE.md                  # Claude Code project instructions
├── marketplace.json           # Machine-readable catalog of all plugins
├── install.sh                 # Plugin installer
└── plugins/
    ├── core/
    │   ├── plugin.json
    │   └── skills/
    │       ├── return-calculations/
    │       ├── time-value-of-money/
    │       └── statistics-fundamentals/
    ├── wealth-management/
    │   ├── plugin.json
    │   └── skills/
    │       └── ... (31 skills)
    ├── compliance/
    │   ├── plugin.json
    │   └── skills/
    │       └── ... (16 skills)
    ├── advisory-practice/
    │   ├── plugin.json
    │   └── skills/
    │       └── ... (10 skills)
    ├── trading-operations/
    │   ├── plugin.json
    │   └── skills/
    │       └── ... (9 skills)
    ├── client-operations/
    │   ├── plugin.json
    │   └── skills/
    │       └── ... (8 skills)
    └── data-integration/
        ├── plugin.json
        └── skills/
            └── ... (4 skills)
```

---

## Skill Template

Each SKILL.md follows a consistent structure:

- **Purpose** — what the skill enables Claude to do
- **When to Use** — trigger phrases and situations
- **Core Concepts** — the domain knowledge, with formulas where applicable
- **Key Formulas** — reference table (quantitative skills only)
- **Worked Examples** — concrete scenarios with step-by-step analysis
- **Common Pitfalls** — mistakes to watch for
- **Cross-References** — links to related skills in other plugins
- **Reference Implementation** — pointer to Python script (quantitative skills only)

Compliance and operations skills use scenario-based examples
(**Scenario / Compliance Issues / Analysis**) and cite specific rule numbers inline.
Quantitative skills include worked numerical examples and runnable Python scripts.
