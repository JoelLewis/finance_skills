---
name: savings-goals
description: Goal-based savings: future value targeting, required savings rates, education funding (529), retirement accumulation.
allowed-tools: ["Bash", "Read", "Write", "Edit"]
---

# Savings Goals

## Purpose
Plan and track savings for specific financial goals — retirement, education, home purchase, and other targets. This skill computes required savings rates, projects future values under different scenarios, and helps prioritize competing goals.

## Layer
6 — Personal Finance

## Direction
Prospective

## When to Use
- Computing required monthly savings to reach a future goal
- Planning education funding (529 plans, cost projections)
- Retirement accumulation targets and savings rate analysis
- Down payment planning for home purchase
- Balancing and prioritizing multiple competing savings goals
- Evaluating whether current savings pace is on track

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
- **Current costs**: ~$25K/year (public in-state) to $60K+/year (private), growing ~5%/year
- **Front-loading**: maximize early contributions for compound growth
- **Superfunding**: 5-year gift tax averaging (contribute 5× annual exclusion at once)
- **Financial aid impact**: 529 owned by parent counted at ~5.6% in EFC

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
- PMT = $1,166.67 / [3.4787 - 1]
- PMT = $1,166.67 / 2.4787 = **$470.72/month**

### Example 2: Retirement Accumulation
**Given:** Age 30, $50,000 currently saved, wants $2,000,000 by age 65, expects 8% annual return
**Calculate:** Required monthly savings
**Solution:**
- FV of current savings: $50,000 × (1.08)^35 = $50,000 × 14.785 = $739,274
- Remaining needed: $2,000,000 - $739,274 = $1,260,726
- Monthly rate: r = 0.08/12 = 0.006667
- Months: n = 35 × 12 = 420
- PMT = $1,260,726 × 0.006667 / [(1.006667)^420 - 1]
- PMT = $8,404.84 / [16.367 - 1]
- PMT = $8,404.84 / 15.367 = **$547/month**
- With employer match of $200/mo: personal contribution = **$347/month**

## Common Pitfalls
- Not inflation-adjusting future goals (college in 18 years costs much more than today)
- Neglecting employer match — it's the highest guaranteed return available
- Too conservative allocation for long-horizon goals (20+ years can tolerate equity risk)
- Saving for college before adequately funding retirement (retirement has no financial aid)
- Not revisiting savings rate as income grows (lifestyle creep absorbs raises)
- Using average returns without considering sequence risk near goal date

## Cross-References
- **time-value-of-money** — FV/PV calculations, annuity formulas
- **emergency-fund** — must be funded before other goals
- **debt-management** — high-interest debt payoff competes with savings
- **tax-efficiency** — 529 tax benefits, Roth vs traditional, HSA
- **investment-policy** — goal-based allocation aligns with IPS constraints
- **asset-allocation** — glide paths for target-date retirement savings
- **finance-psychology** — mental accounting, present bias, commitment devices

## Reference Implementation
See `scripts/savings_goals.py` for computational helpers.
