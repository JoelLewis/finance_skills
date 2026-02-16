# Finance Skills — Implementation Plan

## Overview

45 Claude Code skills across 10 layers (Layer 0–9), organized by dependency order.
Each skill lives in `.claude/skills/<skill-name>/` and consists of:

- **SKILL.md** — The skill specification: purpose, concepts, formulas, worked examples, pitfalls
- **scripts/<name>.py** — Reference implementation (Python computational helpers; not all skills have scripts yet)

Skills are designed to be loaded by Claude Code when a user asks a finance question.
The SKILL.md teaches Claude the domain knowledge; the scripts provide runnable
computational tools.

---

## Repository Structure

```
finance_skills/
├── PLAN.md                              # This file
├── LICENSE
│
└── .claude/skills/
    ├── return-calculations/             # Layer 0 — Mathematical Foundations
    │   ├── SKILL.md
    │   └── scripts/
    │       └── return_calculations.py   ✅
    ├── time-value-of-money/
    │   ├── SKILL.md
    │   └── scripts/
    │       └── time_value_of_money.py   ✅
    ├── statistics-fundamentals/
    │   ├── SKILL.md
    │   └── scripts/
    │       └── statistics_fundamentals.py ✅
    │
    ├── historical-risk/                 # Layer 1a — Realized Risk & Performance
    │   ├── SKILL.md
    │   └── scripts/
    │       └── historical_risk.py       ✅
    ├── performance-metrics/
    │   ├── SKILL.md
    │   └── scripts/
    │       └── performance_metrics.py   ✅
    │
    ├── forward-risk/                    # Layer 1b — Forward-Looking Risk
    │   └── SKILL.md
    ├── volatility-modeling/
    │   └── SKILL.md
    │
    ├── equities/                        # Layer 2 — Asset Classes
    │   └── SKILL.md
    ├── fixed-income-sovereign/
    │   └── SKILL.md
    ├── fixed-income-municipal/
    │   └── SKILL.md
    ├── fixed-income-corporate/
    │   └── SKILL.md
    ├── fixed-income-structured/
    │   └── SKILL.md
    ├── commodities/
    │   └── SKILL.md
    ├── real-assets/
    │   └── SKILL.md
    ├── alternatives/
    │   └── SKILL.md
    ├── fund-vehicles/
    │   └── SKILL.md
    ├── currencies-and-fx/
    │   └── SKILL.md
    ├── digital-assets/
    │   └── SKILL.md
    │
    ├── quantitative-valuation/          # Layer 3 — Valuation
    │   └── SKILL.md
    ├── qualitative-valuation/
    │   └── SKILL.md
    │
    ├── diversification/                 # Layer 4 — Portfolio Construction
    │   └── SKILL.md
    ├── asset-allocation/
    │   └── SKILL.md
    ├── bet-sizing/
    │   └── SKILL.md
    ├── rebalancing/
    │   └── SKILL.md
    │
    ├── investment-policy/               # Layer 5 — Policy & Planning
    │   └── SKILL.md
    ├── tax-efficiency/
    │   └── SKILL.md
    ├── performance-attribution/
    │   └── SKILL.md
    │
    ├── debt-management/                 # Layer 6 — Personal Finance
    │   └── SKILL.md
    ├── lending/
    │   └── SKILL.md
    ├── emergency-fund/
    │   └── SKILL.md
    ├── savings-goals/
    │   └── SKILL.md
    ├── liquidity-management/
    │   └── SKILL.md
    │
    ├── finance-psychology/              # Layer 7 — Behavioral Finance
    │   └── SKILL.md
    │
    ├── performance-reporting/           # Layer 8 — Reporting
    │   └── SKILL.md
    │
    ├── investment-suitability/          # Layer 9 — Compliance & Regulatory Guidance
    │   └── SKILL.md
    ├── know-your-customer/
    │   └── SKILL.md
    ├── anti-money-laundering/
    │   └── SKILL.md
    ├── reg-bi/
    │   └── SKILL.md
    ├── fiduciary-standards/
    │   └── SKILL.md
    ├── fee-disclosure/
    │   └── SKILL.md
    ├── advice-standards/
    │   └── SKILL.md
    ├── sales-practices/
    │   └── SKILL.md
    ├── advertising-compliance/
    │   └── SKILL.md
    ├── client-disclosures/
    │   └── SKILL.md
    └── conflicts-of-interest/
        └── SKILL.md
```

---

## Skill Layers

| Layer | Name | Skills | Direction |
|-------|------|--------|-----------|
| 0 | Mathematical Foundations | return-calculations, time-value-of-money, statistics-fundamentals | both |
| 1a | Realized Risk & Performance | historical-risk, performance-metrics | retrospective |
| 1b | Forward-Looking Risk | forward-risk, volatility-modeling | prospective |
| 2 | Asset Classes | equities, fixed-income-×4, commodities, real-assets, alternatives, fund-vehicles, currencies-and-fx, digital-assets | both |
| 3 | Valuation | quantitative-valuation, qualitative-valuation | prospective / both |
| 4 | Portfolio Construction | diversification, asset-allocation, bet-sizing, rebalancing | both |
| 5 | Policy & Planning | investment-policy, tax-efficiency, performance-attribution | both / retrospective |
| 6 | Personal Finance | debt-management, lending, emergency-fund, savings-goals, liquidity-management | both |
| 7 | Behavioral Finance | finance-psychology | both |
| 8 | Reporting | performance-reporting | retrospective |
| 9 | Compliance & Regulatory Guidance | investment-suitability, know-your-customer, anti-money-laundering, reg-bi, fiduciary-standards, fee-disclosure, advice-standards, sales-practices, advertising-compliance, client-disclosures, conflicts-of-interest | prospective |

**Total: 45 skills**

---

## SKILL.md Template

Each `.claude/skills/<skill-name>/SKILL.md` follows this structure:

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
(Layer 9 compliance skills use scenario-based examples:
**Scenario:** ... **Compliance Issues:** ... **Analysis:** ...)

## Common Pitfalls
- Things to watch out for

## Cross-References
- Related skills

## Reference Implementation (optional — omit for guidance-only skills)
See `scripts/<name>.py` for computational helpers.
```

---

## Cross-Layer Connection Registry

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

---

## Implementation Status

### Phase 1: SKILL.md Files (Current)
- [x] Layer 0 — Mathematical Foundations (3 skills)
- [x] Layer 1a/1b — Risk & Performance (4 skills)
- [x] Layer 2 — Asset Classes (11 skills)
- [x] Layer 3 — Valuation (2 skills)
- [x] Layer 4 — Portfolio Construction (4 skills)
- [x] Layer 5 — Policy & Planning (3 skills)
- [x] Layer 6 — Personal Finance (5 skills)
- [x] Layer 7 — Behavioral Finance (1 skill)
- [x] Layer 8 — Reporting (1 skill)
- [ ] Layer 9 — Compliance & Regulatory Guidance (11 skills)

### Phase 2: Python Reference Implementations
- [x] Layer 0 scripts (return-calculations, time-value-of-money, statistics-fundamentals)
- [x] Layer 1a scripts (historical-risk, performance-metrics)
- [ ] Layer 1b scripts
- [ ] Layer 2 scripts
- [ ] Layer 3 scripts
- [ ] Layer 4 scripts
- [ ] Layer 5 scripts
- [ ] Layer 6 scripts
- [ ] Layer 7 scripts
- [ ] Layer 8 scripts

---

## Conventions

- **Python version**: 3.11+ (scripts are standalone helpers, no package install needed)
- **Dependencies**: numpy, scipy, pandas only (stdlib preferred where possible)
- **Scripts**: Each skill's `scripts/` dir contains runnable Python with clear functions
- **Formulas in SKILL.md**: LaTeX-style notation for clarity
- **Direction labeling**: Every concept tagged as retrospective or prospective
- **Layer 9 conventions**: Compliance skills are guidance-only (no Python scripts). Worked examples use scenario-based format (**Scenario / Compliance Issues / Analysis**) rather than numerical calculations. Primary sources cited inline (rule numbers, act sections, form references).
