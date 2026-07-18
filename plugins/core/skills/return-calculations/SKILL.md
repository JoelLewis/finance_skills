---
name: return-calculations
description: "Compute and compare investment return metrics including TWR, MWR (dollar-weighted IRR on portfolio cash flows), CAGR, and annualized returns. Use when the user asks about portfolio performance calculation, comparing manager returns, linking sub-period returns, understanding why different return methods give different numbers, converting returns across time periods, or computing the IRR of an investor's own contributions and withdrawals. Also trigger when users mention 'how much did I make', 'annual return', 'compound growth', 'dollar-weighted vs time-weighted', 'what was my rate of return', 'geometric vs arithmetic mean', 'log returns', or ask about the effect of cash flows on reported returns. For project or loan IRR, NPV, and generic 'solve for the rate' problems, use time-value-of-money instead."
---

# Return Calculations

## Core Concepts

### Simple (Holding Period) Return

$$R = \frac{V_{end} - V_{begin} + D}{V_{begin}}$$

where `D` = distributions (dividends, interest) received during the period. If `V_end` already reflects reinvested distributions, do not add `D` again.

### Mean and Log Return Conventions

- **Arithmetic mean** `R_a = (1/n) * sum(R_i)` — unbiased estimate of the expected *single-period* return (use for forward-looking inputs, e.g., mean-variance optimization). Always >= geometric mean; overstates realized compound growth.
- **Geometric mean** `R_g = [prod(1 + R_i)]^(1/n) - 1` — the correct measure of realized multi-period compound growth. The gap below the arithmetic mean approximates `sigma^2 / 2` (volatility drag).
- **Log return** `r = ln(V_end / V_begin)` — time-additive (`r_total = r_1 + ... + r_n`), so preferred for statistical modeling and multi-period aggregation. Convert with `R_simple = e^r - 1` and `r = ln(1 + R_simple)`. Log returns are additive across time but NOT across assets.

### CAGR (Compound Annual Growth Rate)

$$CAGR = \left(\frac{V_{end}}{V_{begin}}\right)^{1/n} - 1$$

where `n` is measured in years. The annualized geometric growth rate between two valuations with no intermediate cash flows.

### Time-Weighted Return (TWR)
Chain-links sub-period returns calculated between each external cash flow, removing the effect of cash flow timing. TWR measures the manager's investment skill independent of investor deposit/withdrawal decisions, and is the GIPS standard for manager performance.

$$1 + R_{TWR} = \prod_{i=1}^{n}(1 + R_i), \qquad R_i = \frac{V_{end,i}}{V_{begin,i} + CF_i} - 1$$

Exact TWR requires a portfolio valuation on every cash flow date.

### Modified Dietz Return
When valuations on each cash flow date are unavailable, Modified Dietz approximates the period return by day-weighting each external cash flow within the period:

$$R_{MD} = \frac{V_{end} - V_{begin} - CF_{net}}{V_{begin} + \sum_i CF_i \times w_i}, \qquad w_i = \frac{CD - D_i}{CD}$$

where `CF_net` = sum of external cash flows, `CD` = calendar days in the period, and `D_i` = day of flow `i` (so `w_i` is the fraction of the period the flow was invested). It is a money-weighted approximation; chain-linking Modified Dietz sub-period returns approximates TWR. Accuracy degrades when flows are large relative to portfolio value or markets are volatile within the period — revalue on large-flow dates instead.

### Money-Weighted Return (MWR / IRR)
The internal rate of return that sets the NPV of all investor cash flows (contributions, withdrawals, and terminal value) to zero:

$$0 = \sum_{t=0}^{T} \frac{CF_t}{(1 + r)^t}$$

MWR reflects the actual investor experience because it is sensitive to the timing and magnitude of cash flows. Solved numerically (Newton-Raphson or bisection).

### Annualization

$$R_{annual} = (1 + R_{period})^{periods\_per\_year} - 1$$

For example, a 2% quarterly return annualizes to `(1.02)^4 - 1 = 8.24%`.

### Sub-Period Linking

$$(1 + R_{total}) = \prod_{i=1}^{n}(1 + R_i)$$

The foundational identity behind TWR and CAGR.

## Worked Examples

### Example 1: Computing CAGR from a 5-Year Investment
**Given:** An investment of $10,000 grows to $16,105.10 over exactly 5 years with no intermediate cash flows.

**Calculate:** The compound annual growth rate (CAGR).

**Solution:**

```
CAGR = (V_end / V_begin)^(1/n) - 1
CAGR = (16,105.10 / 10,000)^(1/5) - 1
CAGR = (1.610510)^(0.2) - 1
CAGR = 1.10 - 1
CAGR = 0.10 = 10%
```

The investment grew at a compound annual rate of **10%** per year.

Verification: `$10,000 * (1.10)^5 = $10,000 * 1.61051 = $16,105.10`

### Example 2: TWR vs MWR Divergence with Poorly Timed Cash Flow
**Given:** A fund has the following history:
- Start of Year 1: Portfolio value = $100,000
- End of Year 1: Portfolio value = $120,000 (return = +20%)
- Start of Year 2: Investor deposits $100,000, bringing portfolio to $220,000
- End of Year 2: Portfolio value = $198,000 (return = -10%)

**Calculate:** Both TWR and MWR, and explain the divergence.

**Solution:**

**Time-Weighted Return (TWR):**
```
Sub-period 1 return: R_1 = (120,000 - 100,000) / 100,000 = +20%
Sub-period 2 return: R_2 = (198,000 - 220,000) / 220,000 = -10%

TWR (cumulative) = (1 + 0.20) * (1 + (-0.10)) - 1
                  = 1.20 * 0.90 - 1
                  = 1.08 - 1
                  = +8.0%

TWR (annualized) = (1.08)^(1/2) - 1 = 3.92%
```

**Money-Weighted Return (MWR / IRR):**
Cash flows from the investor's perspective:
- t=0: -$100,000 (initial investment)
- t=1: -$100,000 (additional deposit)
- t=2: +$198,000 (terminal value)

Solve: `-100,000 + (-100,000)/(1+r) + 198,000/(1+r)^2 = 0`

This is quadratic in `x = 1/(1+r)`; the positive root gives r = -0.66815% (verifiable with the bundled script or any IRR solver).

NPV check at r = -0.0066815:
```
-100,000 + (-100,000)/0.9933185 + 198,000/0.9933185^2
= -100,000 - 100,672.65 + 200,672.65
= 0.00  (exact)
```

The MWR is approximately **-0.67% annualized**.

**Interpretation:** The TWR of +3.92% annualized reflects the manager's skill: the fund gained 20% then lost 10%, netting +8% over two years. The MWR of approximately -0.67% reflects the investor's experience: more money was at risk during the losing year (Year 2) because of the large deposit, so the investor's dollar-weighted outcome was slightly negative. This divergence highlights why TWR is preferred for evaluating manager performance, while MWR better describes the specific investor's realized result.

## Common Pitfalls
- Confusing arithmetic and geometric means: the arithmetic mean is always greater than or equal to the geometric mean (AM-GM inequality). Using arithmetic mean to project compounded growth overstates terminal wealth.
- Using arithmetic mean for multi-period compounding: always use geometric mean or CAGR when describing compound growth over multiple periods.
- Annualizing returns from very short periods: annualizing a 2% weekly return yields `(1.02)^52 - 1 = 180%`, which amplifies noise and is misleading. Annualization is most meaningful for periods of at least one year.
- Ignoring cash flow timing when TWR is appropriate: MWR conflates manager skill with investor timing decisions. Use TWR for manager evaluation.
- Double-counting dividends: if the ending value `V_end` already includes reinvested dividends, do not add `D` separately in the holding period return formula.
- Trusting Modified Dietz with large intra-period flows: when a single flow exceeds roughly 10% of portfolio value, revalue the portfolio on the flow date rather than day-weighting.

## Running the Script
`scripts/return_calculations.py` provides a `Returns` class with static methods for every formula above (holding period return, TWR, MWR/IRR via Newton's method, Modified Dietz is straightforward to compose from these, CAGR, annualization, linking, arithmetic/geometric means, log-return conversions).

- Run: `uv run scripts/return_calculations.py` (PEP 723 inline metadata resolves numpy automatically), or `python3 scripts/return_calculations.py` with numpy installed.
- Bare invocation (or `--verify`) prints a demo of all functions **and** asserts the worked-example values above (Example 1 CAGR = 10%, Example 2 TWR = +8.0% cumulative / 3.92% annualized, MWR = -0.6682%), exiting nonzero on any mismatch.
- `--help` lists the available functions and import usage.
- For programmatic use, import rather than run: `from return_calculations import Returns`.

## Cross-References
- **time-value-of-money** (core plugin): NPV, IRR, and discounting concepts overlap with MWR calculations; owns project/loan IRR
- **statistics-fundamentals** (core plugin): Arithmetic and geometric means, return distribution analysis
