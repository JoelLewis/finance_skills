---
name: savings-goals
description: "Plan and track savings for specific financial goals including retirement, education, and home purchase. Use when the user asks about required savings rates, 529 plans, retirement accumulation targets, down payment planning, or goal prioritization. Also trigger when users mention 'how much do I need to save each month', 'am I on track for retirement', 'college savings', 'safe withdrawal rate', '4% rule', 'FIRE savings rate', 'catch-up contributions', 'employer match', or ask how to balance competing savings goals."
---

# Savings Goals

## Core Concepts

### Required Monthly Savings
To accumulate a future value FV in n periods at rate r per period:

PMT = FV × r / [(1+r)^n - 1]

This is the sinking fund formula (future value of annuity solved for PMT).

### Inflation-Adjusted Targets
Always compute goals in future (nominal) dollars:

FV_nominal = FV_today × (1 + inflation)^years

Then solve for the required savings using the nominal return, or use the real return with today's dollars.

### Education Funding
- **529 plans**: tax-free growth for qualified education expenses, state tax deductions in many states
- **Current costs** (2025-26, total cost of attendance, College Board Trends in College Pricing): ~$30K/year (public four-year in-state) to ~$65K/year (private nonprofit), growing ~5%/year
- **Front-loading**: maximize early contributions for compound growth
- **Superfunding**: 5-year gift tax averaging (contribute 5× annual exclusion at once)
- **Financial aid impact**: parent-owned 529 assets are assessed at a maximum of 5.64% in the federal Student Aid Index (SAI) formula — FAFSA has used the SAI in place of the Expected Family Contribution (EFC) since the 2024-25 award year

### Retirement Accumulation
- **Target nest egg**: annual spending need / safe withdrawal rate
  - Example: $80K/year spending / 0.04 = $2,000,000
- **Safe withdrawal rate**: traditionally 4% (Bengen rule), adjusted for fees, taxes, longevity
- **Required savings rate**: depends on starting age, current savings, expected returns
- **Employer match**: always capture full match — it's an immediate 50-100% return
- **Catch-up contributions**: additional 401(k)/IRA contributions allowed after age 50

### Down Payment Saving
- Typical target: 20% of home price (avoids PMI)
- Timeline: typically 2-7 years → conservative allocation (HYSA, short-term bonds)
- Include closing costs (2-5% of purchase price) in savings target

### Goal Priority Framework
Recommended priority order:
1. Emergency fund (3-6 months expenses)
2. Employer 401(k) match (free money)
3. High-interest debt payoff (>6-8% rate)
4. HSA (triple tax advantage if eligible)
5. Max retirement accounts (401k, IRA, Roth)
6. Education funding (529)
7. Other goals (home, vacation, etc.)

### Multiple Goal Balancing
- Allocate savings across goals based on priority, timeline, and flexibility
- Non-negotiable goals (retirement) take precedence over flexible goals
- Shorter timelines need more conservative investment allocation
- Use goal-based investing: separate sub-portfolios per goal with appropriate risk

### Savings Rate Benchmarks
- Minimum: 15% of gross income for retirement (including employer match)
- Aggressive: 25-50%+ for early retirement / FIRE
- Savings rate = total savings / gross income

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| Required savings (PMT) | PMT = FV × r / [(1+r)^n - 1] | Monthly savings for a goal |
| Future value with savings | FV = PV(1+r)^n + PMT×[(1+r)^n - 1]/r | Project goal balance |
| Inflation adjustment | FV_real = FV_today × (1+π)^t | Convert today's dollars to future |
| Retirement target | Nest egg = annual spend / SWR | Size the retirement goal |
| Years to goal | n = ln(FV×r/PMT + 1) / ln(1+r) | How long until goal is funded |
| Savings rate | SR = total savings / gross income | Track savings discipline |

## Worked Examples

### Example 1: College Savings (529)
**Given:** Need $200,000 in 18 years, expect 7% annual return, starting from $0
**Calculate:** Required monthly savings
**Solution:**
- Monthly rate: r = 0.07/12 = 0.005833
- Months: n = 18 × 12 = 216
- PMT = $200,000 × 0.005833 / [(1.005833)^216 - 1]
- PMT = $1,166.67 / [3.5125 - 1]
- PMT = $1,166.67 / 2.5125 = **$464.34/month**

### Example 2: Retirement Accumulation
**Given:** Age 30, $50,000 currently saved, wants $2,000,000 by age 65, expects 8% annual return
**Calculate:** Required monthly savings
**Solution:**
- Monthly rate: r = 0.08/12 = 0.006667; months: n = 35 × 12 = 420
- FV of current savings (monthly compounding): $50,000 × (1.006667)^420 = $50,000 × 16.2925 = $814,627
- Remaining needed: $2,000,000 - $814,627 = $1,185,373
- PMT = $1,185,373 × 0.006667 / [(1.006667)^420 - 1]
- PMT = $7,902.49 / [16.2925 - 1]
- PMT = $7,902.49 / 15.2925 = **$517/month**
- With employer match of $200/mo: personal contribution = **$317/month**

## Common Pitfalls
- Not inflation-adjusting future goals (college in 18 years costs much more than today)
- Neglecting employer match — it's the highest guaranteed return available
- Too conservative allocation for long-horizon goals (20+ years can tolerate equity risk)
- Saving for college before adequately funding retirement (retirement has no financial aid)
- Not revisiting savings rate as income grows (lifestyle creep absorbs raises)
- Using average returns without considering sequence risk near goal date

## Cross-References
- **time-value-of-money** (core plugin): FV/PV calculations, annuity formulas
- **emergency-fund** (wealth-management plugin): must be funded before other goals
- **debt-management** (wealth-management plugin): high-interest debt payoff competes with savings
- **tax-efficiency** (wealth-management plugin): 529 tax benefits, Roth vs traditional, HSA
- **investment-policy** (wealth-management plugin): goal-based allocation aligns with IPS constraints
- **asset-allocation** (wealth-management plugin): glide paths for target-date retirement savings
- **finance-psychology** (wealth-management plugin): mental accounting, present bias, commitment devices
- **financial-planning-workflow** (advisory-practice plugin): savings goals are key inputs to the comprehensive financial planning process
- **insurance-planning** (wealth-management plugin): education and survivor-income goals feed the capital-needs calculation for life insurance sizing
- **estate-gifting** (wealth-management plugin): 529 superfunding (5-year gift-tax election) lets grandparents front-load education goals within annual exclusions
- **retirement-decumulation** (wealth-management plugin): the drawdown-side counterpart — safe withdrawal rates and spending rules for the nest egg accumulated here
## Running the script
Run the reference implementation directly:

```
uv run scripts/savings_goals.py      # PEP 723 header resolves dependencies automatically
python3 scripts/savings_goals.py     # standard library only — no installs needed
```

A bare run prints a demo covering required monthly savings, retirement accumulation, time-to-goal, inflation adjustment, shortfall analysis, education funding, savings rate, and real returns. Use `--verify` to recompute the demo figures and assert they match this skill's worked examples (prints PASS/FAIL, exits nonzero on mismatch), and `--help` to list the available classes and functions. The file is primarily meant to be imported as a module (`from savings_goals import SavingsGoals`) rather than run standalone.
