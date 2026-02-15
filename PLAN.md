# Finance Skills — Implementation Plan

## Overview

27 Claude Code skills across 9 layers (Layer 0–8), organized by dependency order.
Each skill lives in `.claude/skills/<skill-name>/` and consists of:

- **SKILL.md** — The skill specification: purpose, concepts, formulas, worked examples, pitfalls
- **scripts/<name>.py** — Reference implementation (Python computational helpers)

Skills are designed to be loaded by Claude Code when a user asks a finance question.
The SKILL.md teaches Claude the domain knowledge; the scripts provide runnable
computational tools.

---

## Repository Structure

```
finance_skills/
├── PLAN.md                              # This file
├── LICENSE
├── CLAUDE.md                            # Project-level Claude instructions
│
└── .claude/skills/
    ├── return-calculations/             # Layer 0 — Mathematical Foundations
    │   ├── SKILL.md
    │   └── scripts/
    │       └── return_calculations.py
    ├── time-value-of-money/
    │   ├── SKILL.md
    │   └── scripts/
    │       └── time_value_of_money.py
    ├── statistics-fundamentals/
    │   ├── SKILL.md
    │   └── scripts/
    │       └── statistics_fundamentals.py
    │
    ├── historical-risk/                 # Layer 1a — Realized Risk & Performance
    │   ├── SKILL.md
    │   └── scripts/
    │       └── historical_risk.py
    ├── performance-metrics/
    │   ├── SKILL.md
    │   └── scripts/
    │       └── performance_metrics.py
    │
    ├── forward-risk/                    # Layer 1b — Forward-Looking Risk
    │   ├── SKILL.md
    │   └── scripts/
    │       └── forward_risk.py
    ├── volatility-modeling/
    │   ├── SKILL.md
    │   └── scripts/
    │       └── volatility_modeling.py
    │
    ├── equities/                        # Layer 2 — Asset Classes
    │   ├── SKILL.md
    │   └── scripts/
    │       └── equities.py
    ├── fixed-income-sovereign/
    │   ├── SKILL.md
    │   └── scripts/
    │       └── fixed_income_sovereign.py
    ├── fixed-income-municipal/
    │   ├── SKILL.md
    │   └── scripts/
    │       └── fixed_income_municipal.py
    ├── fixed-income-corporate/
    │   ├── SKILL.md
    │   └── scripts/
    │       └── fixed_income_corporate.py
    ├── fixed-income-structured/
    │   ├── SKILL.md
    │   └── scripts/
    │       └── fixed_income_structured.py
    ├── commodities/
    │   ├── SKILL.md
    │   └── scripts/
    │       └── commodities.py
    ├── real-assets/
    │   ├── SKILL.md
    │   └── scripts/
    │       └── real_assets.py
    ├── alternatives/
    │   ├── SKILL.md
    │   └── scripts/
    │       └── alternatives.py
    ├── fund-vehicles/
    │   ├── SKILL.md
    │   └── scripts/
    │       └── fund_vehicles.py
    ├── currencies-and-fx/
    │   ├── SKILL.md
    │   └── scripts/
    │       └── currencies_and_fx.py
    ├── digital-assets/
    │   ├── SKILL.md
    │   └── scripts/
    │       └── digital_assets.py
    │
    ├── quantitative-valuation/          # Layer 3 — Valuation
    │   ├── SKILL.md
    │   └── scripts/
    │       └── quantitative_valuation.py
    ├── qualitative-valuation/
    │   ├── SKILL.md
    │   └── scripts/
    │       └── qualitative_valuation.py
    │
    ├── diversification/                 # Layer 4 — Portfolio Construction
    │   ├── SKILL.md
    │   └── scripts/
    │       └── diversification.py
    ├── asset-allocation/
    │   ├── SKILL.md
    │   └── scripts/
    │       └── asset_allocation.py
    ├── bet-sizing/
    │   ├── SKILL.md
    │   └── scripts/
    │       └── bet_sizing.py
    ├── rebalancing/
    │   ├── SKILL.md
    │   └── scripts/
    │       └── rebalancing.py
    │
    ├── investment-policy/               # Layer 5 — Policy & Planning
    │   ├── SKILL.md
    │   └── scripts/
    │       └── investment_policy.py
    ├── tax-efficiency/
    │   ├── SKILL.md
    │   └── scripts/
    │       └── tax_efficiency.py
    ├── performance-attribution/
    │   ├── SKILL.md
    │   └── scripts/
    │       └── performance_attribution.py
    │
    ├── debt-management/                 # Layer 6 — Personal Finance
    │   ├── SKILL.md
    │   └── scripts/
    │       └── debt_management.py
    ├── lending/
    │   ├── SKILL.md
    │   └── scripts/
    │       └── lending.py
    ├── emergency-fund/
    │   ├── SKILL.md
    │   └── scripts/
    │       └── emergency_fund.py
    ├── savings-goals/
    │   ├── SKILL.md
    │   └── scripts/
    │       └── savings_goals.py
    ├── liquidity-management/
    │   ├── SKILL.md
    │   └── scripts/
    │       └── liquidity_management.py
    │
    ├── finance-psychology/              # Layer 7 — Behavioral Finance
    │   ├── SKILL.md
    │   └── scripts/
    │       └── finance_psychology.py
    │
    └── performance-reporting/           # Layer 8 — Reporting
        ├── SKILL.md
        └── scripts/
            └── performance_reporting.py
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

**Total: 27 skills**

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

## Key Formulas
| Formula | Expression | Use Case |

## Worked Examples
### Example 1: <title>
**Given:** ... **Calculate:** ... **Solution:** ...

## Common Pitfalls
- Things to watch out for

## Cross-References
- Related skills

## Reference Implementation
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

### Phase 2: Python Reference Implementations
- [ ] Layer 0 scripts
- [ ] Layer 1 scripts
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
