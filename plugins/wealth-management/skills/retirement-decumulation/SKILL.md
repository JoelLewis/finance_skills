---
name: retirement-decumulation
description: "Turn a retirement portfolio into sustainable lifetime income: sequence-of-returns risk, the 4% rule and its assumptions, Guyton-Klinger-style guardrails, RMD calculation from the Uniform Lifetime Table, Social Security claiming math (early reduction, delayed credits, breakeven age, survivor benefits), gap-year bracket-filling with Roth conversions, bucket strategies vs total-return, and SPIA annuitization as longevity insurance. Use when the user asks about a 'safe withdrawal rate', 'when should I claim Social Security', a 'guardrails strategy', 'sequence of returns risk', or 'how much can I spend in retirement'. Also trigger on RMD amounts or missed-RMD penalties, Social Security breakeven analysis, '4% rule', 'bucket strategy', retirement paycheck design, drawdown or decumulation planning, and whether to buy an annuity. For accumulation-side savings math, see savings-goals; for asset location and tax mechanics, see tax-efficiency."
---

# Retirement Decumulation

## Core Concepts

### Sequence-of-Returns Risk
Two retirees earning identical average returns can finish with very different wealth if the returns arrive in a different order while money is being withdrawn. Without withdrawals, order is irrelevant — multiplication commutes. With withdrawals, dollars sold after a decline are gone permanently and never participate in the recovery, so poor early returns do disproportionate damage. The danger zone is roughly the five to ten years on either side of the retirement date. Mitigants: flexible spending rules (guardrails), a cash/short-bond buffer, reduced equity exposure near retirement (or a rising equity glide path), and part-time income that lowers the withdrawal rate in early years.

### Safe Withdrawal Rate (SWR) Framework
Bengen's 1994 study (extended by the 1998 Trinity study) found that an initial withdrawal of 4% of the portfolio, adjusted for inflation each year thereafter, survived every rolling 30-year US historical period with 50-75% stocks — the "4% rule." Its assumptions are also its criticisms: it relies on US historical returns (an unusually strong market), a fixed 30-year horizon, rigid inflation-adjusted spending with zero flexibility, and it ignores fees and taxes. Longer retirements, high starting valuations, or lower expected returns argue for 3-3.5% initial rates; dynamic rules (guardrails, amortization-based, RMD-style percent-of-balance) support higher initial rates because spending flexes with the portfolio.

### Guardrails (Guyton-Klinger-Style Decision Rules)
A concrete dynamic rule set:
- **Initial rate:** withdraw, e.g., 5.0% of the starting portfolio in year one.
- **Inflation rule:** each year, increase the prior dollar withdrawal by inflation.
- **Guardrails:** compute the current withdrawal rate = this year's withdrawal / current portfolio. Set guardrails at plus or minus 20% of the initial rate (for 5.0%: upper 6.0%, lower 4.0%).
- **Capital-preservation rule:** if the current rate rises above the upper guardrail, cut the withdrawal 10%.
- **Prosperity rule:** if the current rate falls below the lower guardrail, raise the withdrawal 10%.

The full Guyton-Klinger rule set also skips the inflation increase after a negative-return year. The trade-off: a higher starting income than the 4% rule, paid for with variable spending — the retiree must actually take the cuts when triggered.

### Required Minimum Distributions (RMDs)
RMDs from tax-deferred accounts begin at age 73 under SECURE 2.0, rising to 75 in 2033 for those born in 1960 or later. Mechanics:
- RMD = prior December 31 balance / distribution period (divisor) from the IRS Uniform Lifetime Table (use the Joint Life table instead if the sole beneficiary is a spouse more than 10 years younger).
- Uniform Lifetime Table excerpt (table effective 2022, current as of 2026): age 73 → 26.5, 75 → 24.6, 80 → 20.2, 85 → 16.0, 90 → 12.2.
- Missed-RMD penalty: 25% excise tax on the shortfall, reduced to 10% if corrected within the correction window (SECURE 2.0; previously 50%).
- The first RMD can be delayed until April 1 of the year after the first RMD year, but then two RMDs land in one tax year.
- Roth IRAs have no lifetime RMDs; since 2024, designated Roth 401(k) accounts are also exempt.
- An RMD is a distribution requirement, not a spending requirement — excess can be reinvested in taxable or given via qualified charitable distribution (QCD, available at age 70 1/2, limit indexed annually — verify the current figure).

### Social Security Claiming
Full retirement age (FRA) is 67 for those born in 1960 or later. The adjustment factors are statutory:
- **Early claiming:** benefit reduced 5/9 of 1% per month for the first 36 months before FRA, and 5/12 of 1% per month beyond 36. Claiming at 62 with FRA 67 (60 months early): 36 x 5/9% + 24 x 5/12% = 20% + 10% = 30% reduction — the retiree gets 70% of the Primary Insurance Amount (PIA).
- **Delayed retirement credits:** 2/3 of 1% per month (8% per year) for each month past FRA, up to age 70. Claiming at 70 with FRA 67: 36 x 2/3% = 24% increase — 124% of PIA.
- **Breakeven:** months after the later claim age = B_early x months_delayed / (B_late - B_early), ignoring COLAs and discounting (COLAs apply proportionally to both paths).
- **Survivor benefit:** the survivor keeps the larger of the two benefits, so delaying the higher earner's claim is longevity insurance on the second-to-die — breakeven for that decision should use joint life expectancy, which typically favors delay.
- Claiming before FRA while still working triggers the earnings test (threshold indexed annually — verify the current figure); withheld benefits are restored through recomputation at FRA.

### Withdrawal Sequencing and Gap-Year Bracket-Filling
The conventional order — taxable first, then tax-deferred, then Roth — preserves tax-free growth longest (see tax-efficiency for the tax mechanics and asset-location foundations). The decumulation refinement is the **gap years**: after retiring but before Social Security and RMDs begin, taxable-only withdrawals can leave the ordinary brackets nearly empty. Filling low brackets with partial Roth conversions (or tax-deferred withdrawals) in those years shrinks future RMDs, reduces the survivor's single-filer bracket exposure, and smooths lifetime tax rates — while watching Medicare IRMAA surcharge thresholds (indexed annually) that behave as cliffs. Delaying Social Security to 70 both earns delayed credits and widens the conversion window.

### Bucket Strategies vs Total-Return
A bucket strategy holds 1-2 years of spending in cash, several more years in bonds, and the remainder in equities; spending comes from cash, refilled from the growth buckets opportunistically. A total-return approach holds one target allocation and funds withdrawals by rebalancing. Mathematically a maintained bucket structure is close to a fixed allocation with rebalancing discipline; its real value is behavioral — retirees tolerate equity drawdowns better knowing near-term spending is secured. The main failure mode is leaving the refill rules undefined.

### Annuitization as Longevity Insurance
A single premium immediate annuity (SPIA) converts an irrevocable premium into lifetime income. Because payments pool longevity risk across annuitants, mortality credits let a SPIA sustain a higher payout rate than a self-insured portfolio at the same confidence level — insurance, not an investment to benchmark against market returns. A floor-and-upside design annuitizes enough (with Social Security) to cover essential expenses and invests the rest for growth. Trade-offs: nominal SPIAs carry inflation risk, liquidity and bequest are surrendered, and payments depend on insurer solvency (state guaranty association limits vary). Deferred income annuities and QLACs push income to advanced ages as a tail-longevity hedge (QLAC premium cap: $200,000 statutory base under SECURE 2.0, indexed annually — verify the current limit).

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| Balance recursion (start-of-year withdrawal) | B_t = (B_{t-1} - W_t) x (1 + r_t) | Simulate a withdrawal plan / sequence risk |
| Inflation-adjusted withdrawal | W_t = W_1 x (1 + i)^(t-1) | Fixed-real spending path |
| Current withdrawal rate | CWR = W / B | Guardrail test each year |
| Guardrail bands | upper = r_0 x 1.20; lower = r_0 x 0.80 | Trigger thresholds |
| Guardrail adjustment | W' = W x 0.90 (cut) or W x 1.10 (raise) | Capital-preservation / prosperity rules |
| RMD | RMD = balance_Dec31 / divisor | Required minimum distribution |
| SS early reduction | factor = 1 - [min(m,36) x 5/9 + max(m-36,0) x 5/12]/100 | Benefit if claimed m months before FRA |
| SS delayed credit | factor = 1 + m x (2/3)/100 | Benefit if claimed m months after FRA (to 70) |
| SS breakeven | months after late claim = B_e x Δm / (B_l - B_e) | Age where delaying pulls ahead |

## Worked Examples

### Example 1: Sequence-of-returns risk
**Given:** $1,000,000 portfolio, $50,000 withdrawn at the start of each year (no inflation adjustment for clarity). Sequence A returns: -20%, +10%, +25%. Sequence B: the same returns reversed (+25%, +10%, -20%).
**Calculate:** Ending balances.
**Solution:**
- **No withdrawals:** both orderings end at $1,000,000 x 0.80 x 1.10 x 1.25 = **$1,100,000** — order is irrelevant.
- **Sequence A (crash first):** Y1: (1,000,000 - 50,000) x 0.80 = 760,000. Y2: (760,000 - 50,000) x 1.10 = 781,000. Y3: (781,000 - 50,000) x 1.25 = **$913,750**.
- **Sequence B (crash last):** Y1: 950,000 x 1.25 = 1,187,500. Y2: 1,137,500 x 1.10 = 1,251,250. Y3: 1,201,250 x 0.80 = **$961,000**.
- Identical returns, identical withdrawals — the early-crash retiree ends **$47,250 poorer**. Over a 30-year retirement the same effect determines success or failure.

### Example 2: Guardrails adjustment
**Given:** Retiree starts with $1,000,000 and a 5.0% initial rate ($50,000). Guardrails at plus or minus 20% of 5.0%: upper 6.0%, lower 4.0%. Adjustments are 10%.
**Calculate:** The required action in a bad-market year and a strong-market year.
**Solution:**
- **Capital preservation:** after a bad year the portfolio is $780,000; the inflation-adjusted plan (3% inflation) calls for $50,000 x 1.03 = $51,500. Current rate = 51,500 / 780,000 = **6.60%** > 6.0% upper guardrail → cut 10%: new withdrawal = 51,500 x 0.90 = **$46,350** (rate 5.94%, back inside the bands).
- **Prosperity:** later the portfolio reaches $1,400,000 with a planned $52,000 withdrawal. Current rate = 52,000 / 1,400,000 = **3.71%** < 4.0% lower guardrail → raise 10%: new withdrawal = 52,000 x 1.10 = **$57,200** (rate 4.09%).

### Example 3: RMD at age 73
**Given:** Retiree turns 73 in 2026; the Traditional IRA balance on December 31 of the prior year was $850,000. Uniform Lifetime Table divisor at 73 = 26.5.
**Calculate:** The RMD and the penalty if entirely missed.
**Solution:**
- RMD = 850,000 / 26.5 = **$32,075.47** (about 3.77% of the balance).
- If entirely missed: 25% excise tax = 32,075.47 x 0.25 = **$8,018.87**; if corrected within the correction window, 10% = **$3,207.55**.

### Example 4: Social Security claiming breakeven
**Given:** PIA = $2,000/month at FRA 67 (born 1960 or later).
**Calculate:** Benefits at 62 and 70, and the breakeven ages (ignoring COLA and discounting).
**Solution:**
- **Claim at 62** (60 months early): reduction = 36 x 5/9% + 24 x 5/12% = 30% → **$1,400/month**.
- **Claim at 70** (36 months delayed): credit = 36 x 2/3% = 24% → **$2,480/month**.
- **62 vs 67:** head start = 60 x 1,400 = $84,000; monthly gain from waiting = $600. Breakeven = 84,000 / 600 = 140 months after 67 → age **78.7**.
- **67 vs 70:** head start = 36 x 2,000 = $72,000; monthly gain = $480. Breakeven = 72,000 / 480 = 150 months after 70 → age **82.5**.
- A single claimant expecting to live past roughly 80-82 gains from delaying; for couples, the higher earner's delay is evaluated on joint life expectancy because of the survivor benefit.

## Common Pitfalls
- Treating the 4% rule as a guarantee rather than a historical US backtest with rigid assumptions — and applying it to 40-year early retirements or high-fee portfolios unadjusted
- Planning with average returns and ignoring sequence: a Monte Carlo mean hides the early-crash paths that deplete portfolios
- Adopting guardrails but refusing the spending cut when the capital-preservation rule triggers — the higher initial rate is only safe because of the cuts
- Treating the RMD as a spending rule: it forces a taxable distribution, not consumption, and it is a floor, not a plan
- Missing the two-RMDs-in-one-year trap when delaying the first RMD to April 1
- Claiming Social Security at 62 by default, ignoring the survivor benefit — the higher earner's early claim permanently reduces the widow(er)'s income
- Running Roth conversions that trip IRMAA surcharge cliffs or push conversion income into the next bracket
- Leaving bucket refill rules undefined, so the strategy silently drifts to an ad hoc allocation
- Judging a SPIA as an investment by implied return instead of as longevity insurance priced with mortality credits — or annuitizing so much that liquidity and bequest goals fail

## Cross-References
- **savings-goals** (wealth-management plugin): the accumulation-side counterpart — the safe withdrawal rate sizes the nest egg target that savings plans aim for
- **tax-efficiency** (wealth-management plugin): asset location, Roth conversion breakeven, and the tax mechanics behind withdrawal sequencing and RMDs
- **asset-allocation** (wealth-management plugin): glide paths and the equity/bond mix that governs sequence-risk exposure in decumulation
- **historical-risk** (wealth-management plugin): drawdown and volatility measures that quantify the return sequences retirees must survive
- **emergency-fund** (wealth-management plugin): the cash-reserve discipline that becomes bucket one of a retirement bucket strategy
- **investment-policy** (wealth-management plugin): the IPS documents the spending policy, guardrail rules, and rebalancing discipline for decumulation
- **financial-planning-workflow** (advisory-practice plugin): decumulation strategy is a core deliverable of the retirement-income phase of a comprehensive plan

## Running the script
Run the reference implementation directly:

```
uv run scripts/retirement_decumulation.py      # PEP 723 header resolves dependencies automatically
python3 scripts/retirement_decumulation.py     # standard library only — no installs needed
```

A bare run prints a demo covering sequence-of-returns comparison, guardrails adjustments, RMD calculation and penalties, Social Security claiming factors, and breakeven ages. Use `--verify` to recompute the demo figures and assert they match this skill's worked examples (prints PASS/FAIL, exits nonzero on mismatch), and `--help` to list the available classes and functions. The file is primarily meant to be imported as a module (`from retirement_decumulation import RetirementDecumulation`) rather than run standalone.
