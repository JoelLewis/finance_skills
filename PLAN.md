# Finance Skills — Implementation Plan

## Overview

27 skills across 9 layers (Layer 0–8), organized by dependency order. Each skill
consists of a **specification document** (markdown) and a **reference implementation**
(Python module with tests). Skills are built bottom-up: no skill is drafted until
its dependencies exist.

---

## Repository Structure

```
finance_skills/
├── PLAN.md                          # This file
├── LICENSE
├── pyproject.toml                   # Project config, dependencies
├── README.md                        # Generated after skills are complete
│
├── docs/                            # Skill specification documents
│   ├── layer0-foundations/
│   │   ├── return-calculations.md
│   │   ├── time-value-of-money.md
│   │   └── statistics-fundamentals.md
│   ├── layer1a-retrospective/
│   │   ├── historical-risk.md
│   │   └── performance-metrics.md
│   ├── layer1b-prospective/
│   │   ├── forward-risk.md
│   │   └── volatility-modeling.md
│   ├── layer2-asset-classes/
│   │   ├── equities.md
│   │   ├── fixed-income-sovereign.md
│   │   ├── fixed-income-municipal.md
│   │   ├── fixed-income-corporate.md
│   │   ├── fixed-income-structured.md
│   │   ├── commodities.md
│   │   ├── real-assets.md
│   │   ├── alternatives.md
│   │   ├── fund-vehicles.md
│   │   ├── currencies-and-fx.md
│   │   └── digital-assets.md
│   ├── layer3-valuation/
│   │   ├── quantitative-valuation.md
│   │   └── qualitative-valuation.md
│   ├── layer4-portfolio-construction/
│   │   ├── diversification.md
│   │   ├── asset-allocation.md
│   │   ├── bet-sizing.md
│   │   └── rebalancing.md
│   ├── layer5-investment-policy/
│   │   ├── investment-policy.md
│   │   ├── tax-efficiency.md
│   │   └── performance-attribution.md
│   ├── layer6-personal-finance/
│   │   ├── debt-management.md
│   │   ├── lending.md
│   │   ├── emergency-fund.md
│   │   ├── savings-goals.md
│   │   └── liquidity-management.md
│   ├── layer7-behavioral/
│   │   └── finance-psychology.md
│   └── layer8-reporting/
│       └── performance-reporting.md
│
├── src/
│   └── finance_skills/
│       ├── __init__.py
│       ├── layer0/
│       │   ├── __init__.py
│       │   ├── return_calculations.py
│       │   ├── time_value_of_money.py
│       │   └── statistics_fundamentals.py
│       ├── layer1a/
│       │   ├── __init__.py
│       │   ├── historical_risk.py
│       │   └── performance_metrics.py
│       ├── layer1b/
│       │   ├── __init__.py
│       │   ├── forward_risk.py
│       │   └── volatility_modeling.py
│       ├── layer2/
│       │   ├── __init__.py
│       │   ├── equities.py
│       │   ├── fixed_income_sovereign.py
│       │   ├── fixed_income_municipal.py
│       │   ├── fixed_income_corporate.py
│       │   ├── fixed_income_structured.py
│       │   ├── commodities.py
│       │   ├── real_assets.py
│       │   ├── alternatives.py
│       │   ├── fund_vehicles.py
│       │   ├── currencies_and_fx.py
│       │   └── digital_assets.py
│       ├── layer3/
│       │   ├── __init__.py
│       │   ├── quantitative_valuation.py
│       │   └── qualitative_valuation.py
│       ├── layer4/
│       │   ├── __init__.py
│       │   ├── diversification.py
│       │   ├── asset_allocation.py
│       │   ├── bet_sizing.py
│       │   └── rebalancing.py
│       ├── layer5/
│       │   ├── __init__.py
│       │   ├── investment_policy.py
│       │   ├── tax_efficiency.py
│       │   └── performance_attribution.py
│       ├── layer6/
│       │   ├── __init__.py
│       │   ├── debt_management.py
│       │   ├── lending.py
│       │   ├── emergency_fund.py
│       │   ├── savings_goals.py
│       │   └── liquidity_management.py
│       ├── layer7/
│       │   ├── __init__.py
│       │   └── finance_psychology.py
│       └── layer8/
│           ├── __init__.py
│           └── performance_reporting.py
│
└── tests/
    ├── __init__.py
    ├── layer0/
    │   ├── test_return_calculations.py
    │   ├── test_time_value_of_money.py
    │   └── test_statistics_fundamentals.py
    ├── layer1a/
    │   ├── test_historical_risk.py
    │   └── test_performance_metrics.py
    ├── layer1b/
    │   ├── test_forward_risk.py
    │   └── test_volatility_modeling.py
    ├── layer2/
    │   └── ...  (one test file per skill)
    ├── layer3/
    │   ├── test_quantitative_valuation.py
    │   └── test_qualitative_valuation.py
    ├── layer4/
    │   ├── test_diversification.py
    │   ├── test_asset_allocation.py
    │   ├── test_bet_sizing.py
    │   └── test_rebalancing.py
    ├── layer5/
    │   ├── test_investment_policy.py
    │   ├── test_tax_efficiency.py
    │   └── test_performance_attribution.py
    ├── layer6/
    │   ├── test_debt_management.py
    │   ├── test_lending.py
    │   ├── test_emergency_fund.py
    │   ├── test_savings_goals.py
    │   └── test_liquidity_management.py
    ├── layer7/
    │   └── test_finance_psychology.py
    └── layer8/
        └── test_performance_reporting.py
```

---

## Skill Document Template

Each `docs/<layer>/<skill-name>.md` follows this structure:

```markdown
# <Skill Name>

> Layer N — <Layer Name>
> Dependencies: [list of prerequisite skills]

## Purpose

One-paragraph statement of what this skill covers and what questions it answers.

## Direction

Whether this skill is **retrospective** (backward-looking), **prospective**
(forward-looking), or **both**. What assumptions are required when using
backward-looking outputs as forward-looking inputs.

## Core Concepts

### <Concept 1>
Definition, intuition, formulas (LaTeX where helpful).

### <Concept 2>
...

## Key Formulas

Enumerated with derivation sketches and variable definitions.

## When to Use / When Not to Use

Applicability boundaries, failure modes, common misapplications.

## Cross-References

Links to related skills, especially cross-layer connections.

## Reference Implementation

Brief description of the classes/functions provided in `src/`, their
interfaces, and design rationale.

## Sources & Further Reading

Textbook chapters, papers, canonical references.
```

---

## Implementation Phases

Work proceeds layer by layer, bottom-up. Within each phase, skills with no
intra-layer dependencies can be drafted in parallel.

### Phase 1 — Layer 0: Mathematical Foundations (3 skills)

No dependencies. These are the true foundation.

| # | Skill | Key classes/functions | Notes |
|---|-------|----------------------|-------|
| 1 | **return-calculations** | `Returns` class — TWR, MWR/IRR, CAGR, annualization, sub-period linking, arithmetic vs. geometric vs. log returns | Start here. Everything else imports return math. |
| 2 | **time-value-of-money** | PV/FV/NPV/IRR solvers, `AmortizationSchedule`, annuity functions, compounding conventions | Shared by debt-management and lending (Layer 6). |
| 3 | **statistics-fundamentals** | Distribution fitting, covariance matrix estimation (sample, Ledoit-Wolf shrinkage), rolling regression, bootstrap | Shared by all risk and portfolio skills. |

All three can be drafted in parallel since they have no inter-dependencies.

---

### Phase 2 — Layer 1a: Retrospective Measurement (2 skills)

Depends on: Layer 0.

| # | Skill | Key classes/functions | Notes |
|---|-------|----------------------|-------|
| 4 | **historical-risk** | `HistoricalRiskAnalyzer` — realized vol (close-to-close, Parkinson, Garman-Klass), realized correlation, max drawdown (depth/duration/recovery), historical VaR, downside deviation, tracking error | No distributional assumptions. Pure observed-data analysis. |
| 5 | **performance-metrics** | `PerformanceScorecard` — Sharpe, Sortino, Information Ratio, Calmar, Treynor, Omega, Sterling, capture ratios, batting average, win/loss | Backward-looking summaries. Document sensitivity to period, benchmark, survivorship. |

Both can be drafted in parallel.

---

### Phase 3 — Layer 1b: Prospective Measurement (2 skills)

Depends on: Layer 0. Can run in parallel with Phase 2.

| # | Skill | Key classes/functions | Notes |
|---|-------|----------------------|-------|
| 6 | **forward-risk** | `RiskForecaster` — parametric VaR, Monte Carlo VaR, CVaR/ES, scenario analysis, stress testing, factor-based risk decomposition, regime-switching models | Explicit assumption documentation required. |
| 7 | **volatility-modeling** | `VolatilityModeler` — EWMA, GARCH(1,1), EGARCH, implied vol extraction, vol term structure/surface, variance risk premium | Bridge between retrospective (realized) and prospective (implied, GARCH forecasts). |

Both can be drafted in parallel. Phase 2 and Phase 3 can also run in parallel.

---

### Phase 4 — Layer 2: Asset Classes & Instruments (11 skills)

Depends on: Layers 0–1. Largest phase. Group into sub-batches.

**Batch 4a — Equities & Fixed Income Core (4 skills, parallel)**

| # | Skill | Key classes/functions | Notes |
|---|-------|----------------------|-------|
| 8 | **equities** | Factor exposure analyzer, style box classifier | Equity market structure, factors, index construction. |
| 9 | **fixed-income-sovereign** | `BondPricer`, yield curve bootstrapper, duration/convexity analytics | Treasury mechanics, yield curve math. |
| 10 | **fixed-income-municipal** | Tax-equivalent yield calculator across federal/state/local/AMT | Muni-specific credit analysis, tax treatment. |
| 11 | **fixed-income-corporate** | `CreditAnalyzer` — OAS, spread duration, credit migration matrices | IG vs. HY, credit spreads, private credit. |

**Batch 4b — Structured & Alternatives (4 skills, parallel)**

| # | Skill | Key classes/functions | Notes |
|---|-------|----------------------|-------|
| 12 | **fixed-income-structured** | Prepayment model (PSA/CPR), CMO waterfall simulator | MBS, ABS, CLOs, securitization mechanics. |
| 13 | **commodities** | Roll yield calculator, futures curve analyzer | Contango/backwardation, commodity index construction. |
| 14 | **real-assets** | Property valuation model (cap rate, DCF, comps), REIT NAV analyzer | REITs, farmland, timber, infrastructure. |
| 15 | **alternatives** | PE cash flow modeler, J-curve simulator, PME calculator | PE, VC, hedge funds, fee structures. |

**Batch 4c — Vehicles & Other Asset Types (3 skills, parallel)**

| # | Skill | Key classes/functions | Notes |
|---|-------|----------------------|-------|
| 16 | **fund-vehicles** | Total cost comparison engine (including tax drag estimation) | Mutual funds vs. ETFs vs. CEFs, creation/redemption, share classes. |
| 17 | **currencies-and-fx** | FX hedging cost calculator, carry trade backtester | Interest rate parity, currency hedging, PPP. |
| 18 | **digital-assets** | Network value metrics calculator | Bitcoin/Ethereum frameworks, custody risk, correlation properties. |

---

### Phase 5 — Layer 3: Valuation (2 skills)

Depends on: Layers 0–2.

| # | Skill | Key classes/functions | Notes |
|---|-------|----------------------|-------|
| 19 | **quantitative-valuation** | `DCFModel` (multi-stage), `ComparablesEngine`, `BondValuation` | DCF, DDM, residual income, multiples, LBO floor. |
| 20 | **qualitative-valuation** | `MoatScorecard`, `RegimeIdentifier`, `ReflexivityTracker` | Reflexivity, narrative economics, moat analysis. Cross-references finance-psychology. |

Both can be drafted in parallel.

---

### Phase 6 — Layer 4: Diversification & Portfolio Construction (4 skills)

Depends on: Layers 0–3.

| # | Skill | Key classes/functions | Notes |
|---|-------|----------------------|-------|
| 21 | **diversification** | `DiversificationAnalyzer` — marginal contribution, factor overlap detection | Math of diversification, concentration metrics, tail dependence. |
| 22 | **asset-allocation** | `Optimizer` — MVO, risk parity, Black-Litterman, constraint handling | Strategic vs. tactical, glide paths, goal-based. |
| 23 | **bet-sizing** | Kelly calculator (single + multi-asset), risk budget allocator | Kelly criterion, fractional Kelly, when Kelly fails. |
| 24 | **rebalancing** | `RebalanceEngine` — optimal trade lists given weights, tax lots, costs | Calendar vs. threshold, tax-aware, rebalancing bonus. |

All four can be drafted in parallel. `diversification` and `asset-allocation`
have the strongest logical connection but no code dependency at draft time.

---

### Phase 7 — Layer 5: Investment Guidance & Policy (3 skills)

Depends on: Layers 0–4.

| # | Skill | Key classes/functions | Notes |
|---|-------|----------------------|-------|
| 25 | **investment-policy** | `IPSBuilder` — constraint framework → allocation parameters | IPS construction, risk tolerance, time horizon, liquidity needs. |
| 26 | **tax-efficiency** | `TaxLossHarvester`, `RothConversionAnalyzer` | TLH, asset location, gain/loss budgeting, charitable strategies. |
| 27 | **performance-attribution** | Brinson-Fachler attribution engine | Allocation/selection/interaction effects. Clearly retrospective. |

All three can be drafted in parallel.

---

### Phase 8 — Layer 6: Personal Finance Operations (5 skills)

Depends on: Layers 0, 5.

| # | Skill | Key classes/functions | Notes |
|---|-------|----------------------|-------|
| 28 | **debt-management** | `DebtOptimizer` — snowball, avalanche, NPV-optimal, hybrid payoff schedules | Imports TVM for amortization. Refinancing analysis. |
| 29 | **lending** | `LeverageAnalyzer`, margin call simulator, credit card payoff optimizer | SBLOCs, portfolio margin, strategic leverage. Links to liquidity-management. |
| 30 | **emergency-fund** | `EmergencyFundCalculator` — tiered sizing based on household factors | Income volatility, tiered liquidity, opportunity cost. |
| 31 | **savings-goals** | `GoalPlanner` — savings schedules with Monte Carlo funding probability | Goal-based planning, competing goals, mental accounting. |
| 32 | **liquidity-management** | `CashFlowForecaster` — forward calendar with shortfall detection | Capital call pacing, margin scenarios, sweep optimization. |

All five can be drafted in parallel. Key cross-references:
- `lending` ↔ `liquidity-management` (margin calls create liquidity events)
- `lending` ↔ `debt-management` (borrowing vs. repayment)
- `time-value-of-money` → both `lending` and `debt-management`

---

### Phase 9 — Layer 7: Behavioral Finance (1 skill)

Depends conceptually on all layers.

| # | Skill | Key classes/functions | Notes |
|---|-------|----------------------|-------|
| 33 | **finance-psychology** | `BiasAssessment` questionnaire, `CoupleAlignmentWorksheet` | Three sub-domains: individual biases, couple dynamics, family governance. Cross-references qualitative-valuation. |

---

### Phase 10 — Layer 8: Reporting & Synthesis (1 skill)

Depends on all layers.

| # | Skill | Key classes/functions | Notes |
|---|-------|----------------------|-------|
| 34 | **performance-reporting** | `ReportGenerator` — formatted reports from portfolio data, benchmarks, attribution | GIPS-aware concepts, explicit retrospective/prospective labeling. |

---

## Cross-Layer Connection Registry

These connections must be documented in the cross-references section of each
relevant skill and tested with integration tests:

| Connection | Skills Involved | Nature |
|-----------|----------------|--------|
| Amortization math sharing | `time-value-of-money` → `lending`, `debt-management` | Code import |
| Margin/SBLOC liquidity | `lending` ↔ `liquidity-management` | Cross-reference |
| Borrowing vs. repayment | `lending` ↔ `debt-management` | Cross-reference |
| Behavioral valuation | `qualitative-valuation` ↔ `finance-psychology` | Cross-reference |
| Retro/prospective propagation | `performance-metrics` → `performance-attribution` → `performance-reporting` | Labeling discipline |
| Prospective → allocation | `forward-risk`, `volatility-modeling` → `asset-allocation` | Code import |
| Covariance matrix flow | `statistics-fundamentals` → `historical-risk`, `forward-risk`, `diversification`, `asset-allocation` | Code import |
| Return math flow | `return-calculations` → nearly every skill | Code import |

---

## Drafting Order Summary

```
Phase 1:  [1] return-calculations     ─┐
          [2] time-value-of-money      ├─ all parallel (Layer 0)
          [3] statistics-fundamentals  ─┘

Phase 2:  [4] historical-risk         ─┐ parallel (Layer 1a)
          [5] performance-metrics      ─┘

Phase 3:  [6] forward-risk            ─┐ parallel (Layer 1b)
          [7] volatility-modeling      ─┘
          (Phases 2 & 3 can run in parallel)

Phase 4a: [8]  equities                ─┐
          [9]  fixed-income-sovereign   │ parallel
          [10] fixed-income-municipal   │
          [11] fixed-income-corporate   ─┘

Phase 4b: [12] fixed-income-structured ─┐
          [13] commodities              │ parallel
          [14] real-assets              │
          [15] alternatives             ─┘

Phase 4c: [16] fund-vehicles           ─┐
          [17] currencies-and-fx        │ parallel
          [18] digital-assets           ─┘
          (Batches 4a, 4b, 4c can run in parallel)

Phase 5:  [19] quantitative-valuation  ─┐ parallel (Layer 3)
          [20] qualitative-valuation    ─┘

Phase 6:  [21] diversification         ─┐
          [22] asset-allocation         │ parallel (Layer 4)
          [23] bet-sizing               │
          [24] rebalancing              ─┘

Phase 7:  [25] investment-policy        ─┐
          [26] tax-efficiency            │ parallel (Layer 5)
          [27] performance-attribution   ─┘

Phase 8:  [28] debt-management          ─┐
          [29] lending                   │
          [30] emergency-fund            │ parallel (Layer 6)
          [31] savings-goals             │
          [32] liquidity-management      ─┘

Phase 9:  [33] finance-psychology       (Layer 7)

Phase 10: [34] performance-reporting    (Layer 8)
```

Total: **27 skills** (numbered 1–34 in drafting order, with gaps for the
batched sub-phases within Layer 2).

**Corrected count**: Skills 1–27 map to the 27 unique skills. The numbering
above uses 1–34 only to show sub-batch ordering within Phase 4; the actual
skill count is 27.

---

## Per-Skill Drafting Checklist

For each skill, the drafter must:

- [ ] Write the spec document (`docs/<layer>/<skill-name>.md`) following the template
- [ ] Create the Python module (`src/finance_skills/<layer>/<skill_module>.py`)
  - [ ] Define public classes/functions with full type annotations
  - [ ] Include docstrings mapping to spec sections
  - [ ] Import from dependency layers only (no circular imports)
- [ ] Write tests (`tests/<layer>/test_<skill_module>.py`)
  - [ ] At least one test per public function/method
  - [ ] Edge cases documented in the spec's "When Not to Use" section
  - [ ] Numerical tests with known-answer values from textbooks
- [ ] Verify cross-references are bidirectional
- [ ] Tag direction (retrospective / prospective / both) in both doc and code

---

## Conventions

- **Python version**: 3.11+
- **Dependencies**: numpy, scipy, pandas. No other runtime deps unless justified.
- **Naming**: snake_case for modules and functions, PascalCase for classes
- **Formulas in docs**: LaTeX notation inside `$...$` blocks
- **Test runner**: pytest
- **No premature optimization**: clarity over performance in reference implementations
