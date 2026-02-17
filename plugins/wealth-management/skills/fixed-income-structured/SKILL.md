---
name: fixed-income-structured
description: Structured products: MBS (agency/non-agency), ABS, CLOs, prepayment risk, tranching, waterfall structures.
allowed-tools: ["Bash", "Read", "Write", "Edit"]
---

# Fixed Income — Structured Products

## Purpose
Analyze structured fixed income products including mortgage-backed securities (MBS), asset-backed securities (ABS), and collateralized loan obligations (CLOs). This skill covers prepayment modeling, tranching mechanics, waterfall structures, and the unique risk characteristics of securitized products.

## Layer
2 — Asset Classes

## Direction
both

## When to Use
- User asks about mortgage-backed securities (MBS), agency or non-agency
- User asks about asset-backed securities (ABS) — auto loans, credit cards, student loans
- User asks about CLOs (Collateralized Loan Obligations) or CDOs
- User asks about prepayment risk, extension risk, or contraction risk
- User asks about tranching, waterfall structures, or subordination
- User asks about PSA prepayment models, CPR, or SMM
- User asks about weighted average life (WAL) vs maturity
- User asks about negative convexity in MBS

## Core Concepts

### MBS Pass-Throughs
A pool of mortgages whose cash flows (principal, interest, prepayments) are passed through to investors on a pro-rata basis. Agency MBS (Ginnie Mae, Fannie Mae, Freddie Mac) carry a government or GSE guarantee against credit losses, isolating prepayment risk as the primary concern. Non-agency MBS lack this guarantee and carry both credit and prepayment risk.

### Prepayment Risk
Borrowers can refinance when rates drop, returning principal early. This creates negative convexity — when rates fall, MBS prices rise less than comparable Treasuries because prepayments accelerate and shorten the bond's effective life. Prepayment risk has two faces:

**Contraction risk:** Rates fall, prepayments accelerate, duration shortens. Investors receive principal back when reinvestment rates are lower.

**Extension risk:** Rates rise, prepayments slow, duration extends. Investors are locked into below-market coupons for longer than expected.

### PSA Prepayment Model
The Public Securities Association model provides a benchmark prepayment speed:

100% PSA = ramp from 0% CPR to 6% CPR linearly over the first 30 months, then constant at 6% CPR thereafter.

At 150% PSA, all speeds are multiplied by 1.5 (e.g., the plateau is 9% CPR). At 200% PSA, the plateau is 12% CPR.

### CPR and SMM
**CPR (Conditional Prepayment Rate):** Annualized prepayment rate as a percentage of the remaining pool balance.

**SMM (Single Monthly Mortality):** Monthly prepayment rate.

SMM = 1 - (1 - CPR)^(1/12)

### Weighted Average Life (WAL)
WAL = sum(t × Principal_t) / Total Principal. Unlike maturity, WAL accounts for the timing of principal repayments (both scheduled and prepayments). WAL is shorter than maturity for amortizing securities and is sensitive to prepayment assumptions.

### CMO Tranches
Collateralized Mortgage Obligations redistribute MBS cash flows into tranches with different risk profiles:

**Sequential pay:** Principal flows to the first tranche until retired, then the second, etc. Earlier tranches have shorter duration, later tranches have longer duration.

**PAC (Planned Amortization Class):** Provides a predictable principal schedule within a band of prepayment speeds (e.g., 100-250% PSA). Stability comes at the expense of companion/support tranches that absorb prepayment variability.

**Support/Companion tranches:** Absorb excess or deficit prepayments to protect PAC tranches. Highly volatile duration.

### ABS (Asset-Backed Securities)
Securitized pools of non-mortgage assets:
- Auto loans: amortizing, relatively predictable cash flows
- Credit cards: revolving, with a revolving period followed by a controlled amortization period
- Student loans: longer duration, income-driven repayment creates uncertainty

### CLOs (Collateralized Loan Obligations)
Tranched portfolios of leveraged loans (typically 150-250 loans). AAA tranches benefit from significant subordination (30-40% of the structure below them). Equity tranches receive residual cash flows after all senior tranches are paid. Waterfall tests (overcollateralization and interest coverage tests) redirect cash flows to protect senior tranches when the portfolio deteriorates.

### Waterfall Structure
Cash flows are distributed by seniority: senior tranches receive interest and principal first, mezzanine next, equity last. If pool performance deteriorates, lower tranches absorb losses first (subordination protects senior tranches). Overcollateralization (OC) tests and interest coverage (IC) tests trigger cash flow diversions when breached.

### OAS for Structured Products
OAS is essential for MBS because it captures prepayment optionality. Standard modified duration is inappropriate for MBS — use effective duration (computed via OAS models) or empirical duration. Monte Carlo simulation of interest rate paths and corresponding prepayment responses is the standard valuation approach for MBS.

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| SMM from CPR | SMM = 1 - (1-CPR)^(1/12) | Monthly prepayment rate |
| CPR from SMM | CPR = 1 - (1-SMM)^12 | Annualize monthly rate |
| PSA CPR (month t, t<=30) | CPR = 6% × (t/30) × PSA/100 | Ramping prepayment model |
| PSA CPR (month t, t>30) | CPR = 6% × PSA/100 | Plateau prepayment model |
| WAL | sum(t × Principal_t) / Total Principal | Average principal timing |
| OAS Price | P = E[sum CF_t(path) / (1+s_t+OAS)^t] | MBS valuation |

## Worked Examples

### Example 1: Convert PSA to CPR
**Given:** 150% PSA, month 20
**Calculate:** CPR and SMM in month 20
**Solution:**
At 100% PSA, month 20: CPR = 6% × (20/30) = 4.0%
At 150% PSA: CPR = 4.0% × 1.5 = 6.0%
SMM = 1 - (1 - 0.06)^(1/12) = 1 - (0.94)^(0.0833) = 1 - 0.99486 = 0.00514 = 0.514%

In month 20 at 150% PSA, approximately 0.514% of the remaining pool balance prepays each month, equivalent to 6.0% annualized.

### Example 2: CLO Tranche Analysis
**Given:** A CLO with $500M total assets. AAA tranche = $325M (65%), AA = $50M (10%), A = $37.5M (7.5%), BBB = $25M (5%), BB = $12.5M (2.5%), Equity = $50M (10%).
**Calculate:** Subordination level for the AAA tranche
**Solution:**
Subordination below AAA = AA + A + BBB + BB + Equity
= $50M + $37.5M + $25M + $12.5M + $50M = $175M
Subordination % = $175M / $500M = 35%

The AAA tranche has 35% subordination — the portfolio would need to lose more than 35% of its value before AAA investors suffer any principal loss. This substantial credit enhancement is why CLO AAA tranches have historically experienced zero defaults.

## Common Pitfalls
- Ignoring negative convexity of MBS — MBS underperform Treasuries in both rallies (contraction) and selloffs (extension)
- Using modified duration for MBS — use effective/OAS duration instead, as cash flows change with rates
- Assuming constant prepayment speeds — speeds vary with rates, seasonality, borrower demographics, and housing turnover
- Not understanding that waterfall mechanics affect tranche risk differently — senior and subordinate tranches of the same deal have very different risk profiles

## Cross-References
- Layer 2: `fixed-income-sovereign` for the Treasury curve and duration/convexity concepts
- Layer 2: `fixed-income-corporate` for credit spread concepts applied to non-agency MBS and CLOs
- Layer 2: `real-assets` for real estate market fundamentals underlying MBS
- Layer 3: `portfolio-construction` for structured products in multi-asset portfolios

## Reference Implementation
See `scripts/fixed_income_structured.py` for computational helpers.
