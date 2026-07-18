---
name: equity-compensation
description: "Guides equity compensation planning for wealth management clients: RSU vesting and the supplemental-withholding gap, NSO and ISO exercise taxation, AMT on ISO spreads and the AMT credit, qualifying vs disqualifying dispositions, 83(b) elections for restricted stock, qualified Section 423 ESPPs, and managing concentrated employer stock (staged diversification, exchange funds, protective collars, charitable strategies, Rule 10b5-1 trading plans, Section 16 insider constraints). Use when the user asks about stock options, RSUs, ESPP purchases, or trading windows — e.g. 'my RSUs vested', 'should I exercise my ISOs', 'will I get an AMT hit', 'file an 83(b) election', 'disqualifying disposition', 'set up a 10b5-1 plan', 'I have too much company stock', or questions about selling employer shares as an executive or insider."
---

# Equity Compensation

## Core Concepts

### Restricted Stock Units (RSUs)
RSUs are a promise of shares delivered at vesting. There is no election to make and no exercise decision:

- **Taxation:** Full FMV of shares at vest is ordinary income (W-2 wages), subject to income tax, Social Security (up to the wage base), and Medicare. Cost basis = FMV at vest; holding period starts at vest.
- **Withholding shortfall trap:** Employers withhold federal tax on RSU income at the flat supplemental wage rate — 22% on supplemental wages up to $1 million cumulative for the year, with a mandatory 37% rate on the excess above $1 million (rates as of 2026, tied to statutory brackets — verify current). A client whose actual marginal rate is 32-37% is systematically under-withheld and can face a large April balance due plus underpayment penalties. Plan estimated payments or extra withholding in vest years.
- **Post-vest decision:** Holding vested RSU shares is economically identical to buying employer stock with a cash bonus. The default recommendation is sell-at-vest unless there is a deliberate concentration thesis; there is no tax benefit to holding beyond starting the capital gains clock.

### Nonqualified Stock Options (NSOs)
- **At exercise:** Spread (FMV − strike) × shares is ordinary income (W-2 for employees), with payroll tax and withholding. Basis = FMV at exercise; subsequent gain/loss is capital.
- **No AMT preference** — NSO taxation is entirely in the regular system.
- Exercise timing is a bet on rate arbitrage and appreciation: early exercise moves future appreciation from ordinary income to capital gains but accelerates tax and concentrates risk.

### Incentive Stock Options (ISOs)
- **At exercise:** No regular-tax income. The spread (FMV − strike) × shares is an AMT preference item in the exercise year (unless the shares are sold in a disqualifying disposition in that same calendar year, which eliminates the AMT adjustment).
- **Qualifying disposition:** Sale more than 2 years from grant AND more than 1 year from exercise. Entire gain over strike is long-term capital gain.
- **Disqualifying disposition:** Either holding test fails. Spread at exercise (capped at actual gain if the stock declined) becomes ordinary income in the year of sale; any gain above FMV-at-exercise is capital gain (short- or long-term by holding period from exercise). No payroll tax on the ordinary portion.
- **$100,000 ISO limit:** Aggregate grant-date FMV of ISOs first exercisable in any calendar year cannot exceed $100,000 (IRC 422(d)). This is a statutory figure and is NOT inflation-indexed. The excess is treated as NSOs.
- ISOs must be exercised within 3 months of termination (12 months for disability) to retain ISO status.

### The AMT Mechanism and AMT Credit
The alternative minimum tax is a parallel tax computation. Simplified flow:

1. Start with regular taxable income, add back preference/adjustment items (the ISO spread is the dominant one for equity-comp clients) to get AMTI.
2. Subtract the AMT exemption — an inflation-indexed amount (in the low-to-mid $130,000s for MFJ as of recent years — verify the current figure) that phases out above a high AMTI threshold (thresholds and phaseout rate were changed by 2025 tax legislation effective 2026 — verify current parameters before advising).
3. Apply the two AMT rates: 26% up to an indexed breakpoint (roughly the low $200,000s of AMT base — verify current) and 28% above it, giving the tentative minimum tax (TMT).
4. AMT due = max(0, TMT − regular tax). The client pays the higher of the two systems.

**AMT credit:** AMT paid on *deferral* items (like the ISO spread) generates a minimum tax credit carried forward indefinitely, usable in future years when regular tax exceeds TMT. The ISO AMT is largely a prepayment, not a permanent cost — but the credit can take many years to recover. Shares exercised also get a higher AMT basis (FMV at exercise), so a later qualifying sale produces a smaller AMT gain, helping unlock the credit.

**Planning levers:** Exercise early in the year (option to disqualify before Dec 31 if the stock collapses — the classic dot-com trap was owing AMT on vanished paper gains); exercise only up to the "AMT crossover" amount where TMT just equals regular tax; spread exercises across years.

### 83(b) Elections (Restricted Stock, Not RSUs)
For restricted *stock* (including early-exercised options), Section 83(b) lets the holder elect to be taxed at grant/early-exercise on (FMV − price paid) rather than at vesting:

- **30-day deadline from the transfer date — statutory, no extensions.** File with the IRS and give a copy to the employer.
- Converts all post-grant appreciation to capital gain and starts the holding period immediately. Most valuable when current spread is near zero (founder stock, early exercise at strike = FMV).
- **Risk:** Tax paid is not refundable if the shares are later forfeited; no deduction for the forfeited income (only a capital loss for actual amounts paid).
- RSUs are not eligible — there is no property transferred at grant.

### Employee Stock Purchase Plans (ESPP, Section 423)
- Qualified plans allow purchase at up to a 15% discount, often with a lookback applying the discount to the lower of the offering-date or purchase-date price. Statutory cap: $25,000 per year of stock (valued at offering-date FMV) — IRC 423(b)(8), not indexed.
- **Qualifying disposition** (>2 years from offering date and >1 year from purchase): ordinary income = the lesser of (a) actual gain and (b) the discount computed on the offering-date price; the rest is long-term capital gain. With a lookback and an appreciated stock, this often converts most of the gain to LTCG.
- **Disqualifying disposition:** ordinary income = FMV at purchase − purchase price (the full bargain element, even if later sold at a loss); remainder is capital gain/loss.
- A 15% discount with a 6-month purchase period is roughly a 15/85 ≈ 17.6% return over ≤6 months even selling immediately — max participation with immediate sale is the low-risk baseline recommendation; holding for qualifying treatment adds concentration risk for a modest tax benefit.

### Concentrated Stock Management
A single position above roughly 10% of net worth warrants a plan. Tools, in rough order of simplicity:

- **Staged diversification:** Preset sell schedule (e.g., equal tranches quarterly over 1-3 years) removes timing regret and market-timing behavior; coordinate lots (highest basis first) and gain budgets with the tax plan; insiders execute via a 10b5-1 plan.
- **Charitable strategies:** Donate long-term appreciated shares directly (or to a donor-advised fund) — full FMV deduction and the embedded gain is never taxed. Charitable remainder trusts (CRTs) allow diversification inside the trust with tax deferral and an income stream.
- **Exchange funds:** Contribute the concentrated position to a partnership pooling many investors' stocks; receive diversified units without a current sale. Requires a 7-year holding period for tax-deferred treatment (redemption in kind carries over basis); funds must hold at least 20% in qualifying illiquid assets; expect fees, lockup, limited control, and accreditation requirements.
- **Protective collars:** Buy a put, sell a call (often zero-premium). Caps downside without a sale. Watch: a collar that is too tight risks constructive-sale treatment under IRC 1259 (no bright line; meaningful band retained in practice); straddle rules can suspend the holding period and defer losses; a protective put on stock not yet held long-term restarts/suspends the LTCG clock. Collared stock supports high loan-to-value margin borrowing for diversification or liquidity ("collar and loan").
- **Completion strategies:** Build the rest of the portfolio to underweight the employer's sector so total exposure is closer to market weight.

### Rule 10b5-1 Plans and Section 16 (High Level)
- A Rule 10b5-1 plan is a written trading plan adopted while not in possession of MNPI, giving an affirmative defense to insider-trading liability for trades executed later under its formula.
- **2022 SEC amendments (effective February 2023):** Mandatory cooling-off periods before the first trade — for directors and officers, the later of 90 days after adoption/modification or 2 business days after filing the 10-Q/10-K covering the adoption quarter, capped at 120 days; for other insiders, 30 days. Also: good-faith condition, director/officer certification, a general bar on overlapping plans, one single-trade plan per 12 months, and quarterly issuer disclosure of plan adoptions/terminations.
- **Section 16** (directors, officers, >10% holders): Form 4 within 2 business days of transactions; short-swing profit recapture under 16(b) on matched purchases and sales within 6 months (this can trap ESPP/option activity paired with open-market sales). Affiliates selling in the open market are also subject to Rule 144 volume limits and Form 144 filings. Coordinate every diversification plan with company counsel and the insider-trading policy's window periods.

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| RSU income at vest | shares × FMV_vest | Ordinary W-2 income |
| RSU withholding gap | income × (t_marginal − t_supplemental) | Estimated additional tax due in April |
| NSO ordinary income | shares × (FMV_exercise − strike) | Taxed at exercise, ordinary rates |
| ISO AMT preference | shares × (FMV_exercise − strike) | Added to AMTI in exercise year |
| Tentative minimum tax | 26% × base up to breakpoint + 28% × excess, base = AMTI − exemption | Parallel AMT computation |
| AMT due / credit | max(0, TMT − regular tax) | Incremental tax; credit carryforward for deferral items |
| Disqualifying ISO ordinary income | min(FMV_exercise, sale price) − strike, floored at 0 | Ordinary portion when holding test fails |
| ESPP qualifying ordinary income | min(actual gain, discount% × offer-date FMV) | Ordinary portion; remainder LTCG |

## Worked Examples

### Example 1: RSU withholding gap
**Given:** 10,000 RSUs vest at $40/share. Employer withholds federal tax at the 22% supplemental rate (net-share settlement). Client's actual federal marginal rate: 35%.
**Solution:**
1. Ordinary income at vest: 10,000 × $40 = **$400,000** (W-2).
2. Federal withholding: $400,000 × 22% = $88,000 → 2,200 shares withheld; client receives **7,800 net shares**.
3. Actual federal tax on the vest income: $400,000 × 35% = $140,000.
4. **Shortfall: $140,000 − $88,000 = $52,000** owed at filing — before state tax and any Medicare surtax. The client should make an estimated payment in the vest quarter to avoid underpayment penalties.

### Example 2: ISO exercise AMT computation
**Given:** Exercise 5,000 ISOs, strike $10, FMV at exercise $50, and hold the shares. Other AMTI (income after regular deductions, before the spread): $250,000 MFJ. Regular tax: $60,000. Illustrative AMT parameters: exemption $137,000 with no phaseout at this income level, 28% rate above $220,000 of AMT base (both figures indexed — verify current year).
**Solution:**
1. AMT preference (spread): 5,000 × ($50 − $10) = **$200,000**. No regular-tax income.
2. AMTI: $250,000 + $200,000 = $450,000.
3. AMT base: $450,000 − $137,000 = $313,000.
4. TMT: 26% × $220,000 + 28% × ($313,000 − $220,000) = $57,200 + $26,040 = **$83,240**.
5. AMT due: $83,240 − $60,000 = **$23,240** on top of regular tax — an effective 11.6% prepayment on the $200,000 spread, carried forward as a minimum tax credit for future years when regular tax exceeds TMT.
6. AMT basis in the shares becomes $50 (vs $10 regular basis), shrinking the AMT gain on a later qualifying sale and helping recover the credit.

### Example 3: Disqualifying vs qualifying ISO disposition
**Given:** 2,000 ISOs, strike $15, exercised at FMV $35, later sold at $60. Ordinary/STCG rate 35%, LTCG rate 15%.
**Qualifying (>2 yrs from grant, >1 yr from exercise):**
1. Entire gain is LTCG: 2,000 × ($60 − $15) = $90,000. Tax: $90,000 × 15% = **$13,500**. (The $40,000 spread was an AMT preference in the exercise year — see Example 2 mechanics.)
**Disqualifying (sold 8 months after exercise):**
2. Ordinary income = spread at exercise: 2,000 × ($35 − $15) = $40,000 → tax $14,000.
3. Remaining gain is STCG: 2,000 × ($60 − $35) = $50,000 → tax $17,500.
4. Total: **$31,500** — **$18,000 more** than the qualifying path. If the sale had occurred in the same calendar year as exercise, the AMT preference on the spread would be eliminated, which can make deliberate same-year disqualification rational when the stock has fallen.

## Common Pitfalls
- Assuming the RSU shares withheld at vest cover the full tax bill — the 22% supplemental rate (as of 2026 — verify current) under-withholds for anyone in the 32%+ brackets
- Exercising ISOs late in the year and holding: if the stock collapses the next year, AMT is still owed on the vanished exercise-date spread; exercising early in the year preserves the same-year disqualification escape hatch
- Missing the 83(b) 30-day deadline (statutory, no relief) or filing one for RSUs, which are ineligible
- Treating the AMT on ISO exercise as a permanent cost — it is mostly a prepayment recoverable via the minimum tax credit, but model the recovery timeline
- Breaking the ISO $100,000 first-exercisable-per-year limit (statutory, NOT indexed) with a large grant and assuming everything is ISO — the excess is NSO
- Selling ESPP shares one day short of the offering-date or purchase-date holding tests, converting favorable qualifying treatment into full bargain-element ordinary income
- Forgetting that a disqualifying ESPP or ISO disposition creates ordinary income even when the position is sold at an overall loss relative to the purchase-date FMV
- Letting an insider sell without a 10b5-1 plan, or trading before the cooling-off period ends (directors/officers: up to 120 days under the 2022 amendments, effective February 2023)
- Matching an open-market sale against any purchase (including ESPP) within 6 months as a Section 16 insider — short-swing profit recapture applies mechanically
- Writing a collar so tight it risks constructive-sale treatment, or ignoring straddle rules that suspend the holding period on unhedged appreciation
- Ignoring wash-sale interactions: recurring RSU vests and ESPP purchases can wash out losses harvested on employer stock in the surrounding 61-day window
- Anchoring on the grant-date or peak price ("I'll diversify when it gets back to $X") instead of treating vested equity as cash compensation to be invested per the plan

## Cross-References
- **tax-efficiency** (wealth-management plugin): bracket management around vest and exercise years, lot selection when diversifying, and charitable giving with appreciated employer stock
- **diversification** (wealth-management plugin): concentrated single-stock exposure from equity compensation is the classic case for staged diversification and completion portfolios
- **equities** (wealth-management plugin): valuation and risk characteristics of the underlying employer shares inform hold/sell and exercise decisions
- **liquidity-management** (wealth-management plugin): funding exercise costs, AMT bills, and withholding shortfalls without forced sales requires planned liquidity
- **tax-loss-harvesting** (wealth-management plugin): harvested losses offset gains realized while diversifying; recurring vests and ESPP purchases create wash-sale exposure on employer stock
- **investment-suitability** (compliance plugin): concentration levels and insider status are suitability considerations for hedging, lending, and diversification recommendations

## Running the script
Run with `uv run scripts/equity_compensation.py` (the PEP 723 header resolves dependencies automatically) or directly with `python3 scripts/equity_compensation.py` (standard library only). The bare run prints a demo covering RSU vest withholding and the withholding gap, an NSO exercise, the simplified ISO/AMT computation, qualifying vs disqualifying ISO dispositions, and ESPP purchase/disposition taxation. Pass `--verify` to assert the outputs match this skill's worked examples (prints PASS/FAIL and exits nonzero on mismatch), or `--help` for an overview of the available methods. The file is primarily meant to be imported as a module (e.g., `from equity_compensation import EquityCompensation`).
