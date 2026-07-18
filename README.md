# Finance Skills for Claude Code

A collection of Claude Code skill plugins for financial services. 91 skills across
7 domain plugins teach Claude investment management, regulatory compliance, advisory
workflows, trading operations, and more — so it can assist with finance questions,
build financial tools, and flag compliance concerns.

Built by [Joel Lewis](https://joelelewis.com?ref=finance_skills).

**Contributions welcome!** Found a way to improve a skill or have a new one to add?
See [CONTRIBUTING.md](CONTRIBUTING.md).

> **Disclaimer:** These skills are provided as-is for educational and informational
> purposes only. The authors make no representations or warranties regarding the
> accuracy, completeness, or currentness of this content. Nothing in these skills
> constitutes financial, legal, tax, or investment advice. Users should independently
> verify any information before relying on it in a professional or personal context.
> See [LICENSE](LICENSE) for full terms.

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

**Valuation:** Quantitative models (DCF, DDM, comparables, residual income),
qualitative assessment (moats, management quality, ESG), and financial-statement
analysis (FCF/EBITDA derivation, ROIC, DuPont, earnings quality).

**Portfolio construction:** Diversification theory, mean-variance optimization,
Black-Litterman, risk parity, Kelly criterion, position sizing, calendar- and
threshold-based rebalancing, factor investing (Fama-French regressions, smart-beta
evaluation).

**Policy and planning:** IPS construction, tax-aware investing, asset location,
tax-loss harvesting (dedicated workflow skill), performance attribution (Brinson,
factor-based).

**Personal finance:** Debt prioritization, mortgage and loan analysis, emergency fund
sizing, savings goals, liquidity management, equity compensation (RSU/ISO/NSO, AMT,
concentrated stock), retirement decumulation (withdrawal rates, RMDs, Social Security
claiming), insurance planning, and estate & gifting.

**Behavioral finance:** Cognitive biases, nudges, emotional discipline.

**Reporting:** Risk-adjusted performance ratios, performance reports, benchmark
comparison, goal progress tracking.

38 skills. Python scripts for quantitative skills (risk, performance metrics, and core
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
| `private-placements` | Reg D 506(b)/(c), accredited investor and qualified purchaser tests, Form D, FINRA 5122/5123 |

17 skills.

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
| `client-review-prep` | Pre-meeting review preparation, performance summary, drift analysis, talking points |
| `financial-planning-workflow` | End-to-end financial plan assembly, retirement modeling, scenario analysis |

12 skills.

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

## Installation

### Option 1: Claude Code Marketplace (Recommended)

Install via Claude Code's built-in plugin system:

```bash
/install JoelLewis/finance_skills
```

### Option 2: npx skills

Use [npx skills](https://github.com/anthropics/skills) to install skills directly:

```bash
# Install all skills
npx skills add JoelLewis/finance_skills

# Install specific plugins
npx skills add JoelLewis/finance_skills --plugin wealth-management

# List available plugins
npx skills add JoelLewis/finance_skills --list
```

### Option 3: install.sh (Symlink)

Clone the repo and use the included installer, which symlinks skills into your
project so updates are reflected immediately:

```bash
git clone https://github.com/JoelLewis/finance_skills.git
cd finance_skills

# Install a single plugin
./install.sh --plugin wealth-management --target /path/to/your/project

# Install all plugins
./install.sh --plugin all --target /path/to/your/project

# List available plugins
./install.sh --list
```

The installer always installs `core` first (implicit dependency), then any declared
plugin dependencies, then symlinks each skill into `<target>/.claude/skills/`.

### Option 4: Clone and Copy

Copy skills directly without symlinks:

```bash
git clone https://github.com/JoelLewis/finance_skills.git
mkdir -p /path/to/your/project/.claude/skills

# Copy a single plugin
cp -r finance_skills/plugins/core/skills/* /path/to/your/project/.claude/skills/
cp -r finance_skills/plugins/wealth-management/skills/* /path/to/your/project/.claude/skills/

# Or copy everything
for plugin in finance_skills/plugins/*/; do
  cp -r "$plugin"skills/* /path/to/your/project/.claude/skills/
done
```

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

After installing, Claude will automatically pick up the skills. Verify with:

```bash
ls /path/to/your/project/.claude/skills/
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
├── CLAUDE.md                  # Claude Code project instructions
├── .claude-plugin/
│   └── marketplace.json       # Plugin catalog (catalog of record)
├── install.sh                 # Plugin installer (--list, --check)
└── plugins/
    ├── core/
    │   ├── .claude-plugin/
    │   │   └── plugin.json    # Plugin manifest (deps, keywords, scripts flag)
    │   └── skills/
    │       ├── return-calculations/
    │       ├── time-value-of-money/
    │       └── statistics-fundamentals/
    ├── wealth-management/
    │   ├── .claude-plugin/plugin.json
    │   └── skills/            # ... (38 skills)
    ├── compliance/
    │   ├── .claude-plugin/plugin.json
    │   └── skills/            # ... (17 skills)
    ├── advisory-practice/
    │   ├── .claude-plugin/plugin.json
    │   └── skills/            # ... (12 skills)
    ├── trading-operations/
    │   ├── .claude-plugin/plugin.json
    │   └── skills/            # ... (9 skills)
    ├── client-operations/
    │   ├── .claude-plugin/plugin.json
    │   └── skills/            # ... (8 skills)
    └── data-integration/
        ├── .claude-plugin/plugin.json
        └── skills/            # ... (4 skills)
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

## What Are Plugins?

Each plugin is a collection of SKILL.md files (and optional Python reference scripts)
that teach Claude domain knowledge. When installed, Claude can:

- Answer domain-specific questions with regulatory citations and worked examples
- Flag compliance concerns during design discussions
- Generate and explain financial computations
- Assist with building, evaluating, or integrating with financial systems

Plugins are independently installable — pull only the domains your project needs. The
`core` plugin is implicit and always included.

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
| Review prep workflow | client-review-prep → performance-reporting, performance-attribution, rebalancing, tax-efficiency, investment-policy | Meeting preparation assembles data from multiple knowledge skills |
| Financial plan orchestration | financial-planning-workflow → savings-goals, debt-management, emergency-fund, liquidity-management, tax-efficiency, investment-policy | Planning workflow references underlying knowledge skills |
| TLH workflow depth | tax-loss-harvesting ↔ tax-efficiency, rebalancing | Dedicated TLH workflow extends broader tax-efficiency coverage and coordinates with rebalancing |
| Plan to review cycle | financial-planning-workflow ↔ client-review-prep | Plan progress is reviewed in client meetings; reviews may trigger plan updates |

---
