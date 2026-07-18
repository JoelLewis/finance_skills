---
name: asset-allocation
description: "Determine how to distribute capital across asset classes using strategic and tactical allocation frameworks. Use when the user asks about portfolio allocation, mean-variance optimization, Black-Litterman, risk parity, glide paths, or target-date strategies. Also trigger when users mention 'how much in stocks vs bonds', '60/40 portfolio', 'policy portfolio', 'core-satellite', 'liability-driven investing', 'asset-liability matching', or ask how to split their money across investments."
---

# Asset Allocation

## Core Concepts

### Strategic Asset Allocation (SAA)
The long-term policy portfolio based on an investor's risk tolerance, return objectives, time horizon, and constraints. SAA determines the baseline target weights (e.g., 60% equity / 30% bonds / 10% alternatives) and is the dominant driver of long-term portfolio returns. SAA should be revisited when investor circumstances change, not in response to market movements.

### Tactical Asset Allocation (TAA)
Short-to-medium-term deviations from the SAA based on market views, valuations, or momentum signals. TAA requires a disciplined process to avoid becoming ad hoc market timing. Key considerations:
- Define allowable deviation bands (e.g., +/- 10% from SAA)
- Have a clear signal framework (valuation, momentum, macro)
- Set reversion rules: when to return to SAA weights

### Mean-Variance Optimization (MVO)
Markowitz's framework for finding optimal portfolio weights that maximize risk-adjusted return:

max w'*mu - (lambda/2) * w'*Sigma*w

subject to: sum(w_i) = 1, w_i >= 0 (if long-only), and any additional constraints.

Where:
- w = weight vector
- mu = expected return vector
- Sigma = covariance matrix
- lambda = risk aversion parameter

MVO requires three inputs: expected returns, the covariance matrix, and risk aversion. The solution is highly sensitive to expected return inputs.

### Black-Litterman Model
Combines market equilibrium returns with investor views to produce more stable, intuitive portfolio weights. Two-step process:

**Step 1 — Implied Equilibrium Returns:**
Pi = lambda * Sigma * w_mkt

where w_mkt is the market-capitalization weight vector, lambda is the risk aversion parameter, and Sigma is the covariance matrix. These are the returns the market implicitly expects given current prices.

**Step 2 — Blending with Views:**
E(R) = [(tau*Sigma)^(-1) + P'*Omega^(-1)*P]^(-1) * [(tau*Sigma)^(-1)*Pi + P'*Omega^(-1)*Q]

where:
- tau = scalar (uncertainty of equilibrium, typically 0.025-0.05)
- P = pick matrix (identifies assets in each view)
- Q = view vector (expected returns from views)
- Omega = diagonal matrix of view uncertainties

The result is a posterior expected return vector that tilts away from equilibrium toward the investor's views, proportional to confidence.

### Risk Parity
Equalizes the risk contribution from each asset (or factor) rather than equalizing capital allocation:

RC_i = w_i * (Sigma*w)_i / sigma_p

Set RC_i = RC_j for all i, j.

In a simple two-asset case with no correlation:
w_i is proportional to 1/sigma_i

Risk parity portfolios allocate more capital to lower-volatility assets (typically bonds) and often require leverage to achieve competitive return targets.

### Glide Path
An age-based or time-based allocation that systematically shifts from growth assets to defensive assets as the investor ages or the target date approaches:

Common rule of thumb: Equity % = 110 - Age

Target-date fund glide paths typically:
- Start at 90% equity for young investors
- Decrease by ~1-2% per year
- Reach 30-40% equity at retirement
- Continue to "through" allocation post-retirement

### Core-Satellite
A hybrid approach combining:
- **Core (60-80%):** Low-cost, broadly diversified index funds or ETFs
- **Satellites (20-40%):** Active strategies, factor tilts, alternatives, or concentrated positions

This structure captures the market return efficiently (core) while allowing alpha generation or specific exposures (satellites).

### Asset-Liability Matching
For investors with defined liabilities (pensions, insurance, endowments with spending rules):
- Match asset duration and cash flows to liability duration and timing
- Surplus optimization: optimize the portfolio relative to liabilities, not absolute return
- Liability-driven investing (LDI): hedge liability risk with duration-matched bonds, invest surplus in return-seeking assets

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| MVO Objective | max w'*mu - (lambda/2)*w'*Sigma*w | Optimal portfolio weights |
| Equilibrium Returns | Pi = lambda * Sigma * w_mkt | Black-Litterman starting point |
| BL Posterior | E(R) = [(tau*Sigma)^(-1) + P'*Omega^(-1)*P]^(-1) * [(tau*Sigma)^(-1)*Pi + P'*Omega^(-1)*Q] | Blended expected returns |
| Risk Contribution | RC_i = w_i * (Sigma*w)_i / sigma_p | Risk parity target |
| Risk Parity Condition | RC_i = RC_j for all i, j | Equal risk contribution |
| Glide Path Rule | Equity % = 110 - Age | Age-based allocation |

## Worked Examples

### Example 1: Three-Asset Mean-Variance Optimization
**Given:**
- Assets: US Equity (mu=8%, sigma=16%), Int'l Equity (mu=7%, sigma=18%), US Bonds (mu=3%, sigma=4%)
- Correlations: US/Intl Equity = 0.75, US Equity/Bonds = 0.10, Intl Equity/Bonds = 0.05
- Risk aversion: lambda = 4
- Constraints: long-only, fully invested

**Calculate:** Optimal weights

**Solution:**

Covariance matrix:
- Cov(US,US) = 0.16^2 = 0.0256
- Cov(Intl,Intl) = 0.18^2 = 0.0324
- Cov(Bond,Bond) = 0.04^2 = 0.0016
- Cov(US,Intl) = 0.75 * 0.16 * 0.18 = 0.0216
- Cov(US,Bond) = 0.10 * 0.16 * 0.04 = 0.00064
- Cov(Intl,Bond) = 0.05 * 0.18 * 0.04 = 0.00036

MVO with lambda=4 (solving numerically or via quadratic programming):

Optimal weights (long-only):
- US Equity: 51.9%
- Int'l Equity: 0%
- US Bonds: 48.1%

Portfolio: expected return = 5.60%, volatility = 8.71%

Note: International equity is driven to zero — it is highly correlated with US equity (0.75) but has a lower expected return, so the optimizer sees no reason to hold it. This is classic MVO behavior: small input differences produce corner solutions. Adding a maximum-weight or minimum-allocation constraint would force diversification. The high bond allocation reflects the heavy variance penalty (lambda=4); reducing lambda shifts toward equities.

### Example 2: Black-Litterman with a Relative View
**Given:** The same three assets and covariance matrix as Example 1.
- Market-cap weights: US Equity 55%, Int'l Equity 30%, US Bonds 15%
- Risk aversion lambda = 2.5, tau = 0.05
- Investor view: Int'l Equity will outperform US Bonds by 3% (view uncertainty Omega = [0.001]; lower = higher confidence)

**Calculate:** Equilibrium and posterior expected returns

**Solution:**

Step 1 — Equilibrium returns, Pi = lambda × Sigma × w_mkt:
- US Equity: 5.16%
- Int'l Equity: 5.41%
- US Bonds: 0.18%

Step 2 — View specification: P = [0, 1, -1], Q = [3%].

The equilibrium already implies Int'l beats Bonds by 5.23%, so a 3% view is *bearish* relative to equilibrium. Applying the Black-Litterman posterior formula:
- US Equity: 4.28% (pulled down via its 0.75 correlation with Int'l)
- Int'l Equity: 4.07% (down from 5.41%)
- US Bonds: 0.23% (up slightly)

The posterior tilts returns toward the view in proportion to confidence. Fed into MVO, these returns shift weights away from equities and toward bonds relative to market-cap weights — moderately, avoiding the extreme corner solutions that raw MVO produces (compare Example 1). Note that views are always evaluated relative to what equilibrium already implies, not in isolation.

## Common Pitfalls
- MVO is highly sensitive to expected return inputs and has been called an "error maximizer" — small changes in returns produce large changes in weights
- Unconstrained MVO often produces extreme, concentrated positions — always add constraints (long-only, max weight, turnover limits)
- Black-Litterman requires the analyst to specify confidence in views (Omega), which is itself uncertain
- Risk parity portfolios require leverage to achieve equity-like returns, introducing borrowing costs and leverage risk
- Ignoring implementation costs: transaction costs, bid-ask spreads, and taxes can significantly erode theoretical optimal returns
- Ignoring liquidity constraints: some asset classes (private equity, real estate) cannot be rebalanced quickly
- Glide paths assume a generic investor — individual circumstances may require customization
- Over-reliance on historical covariance matrices that may not reflect future relationships

## Cross-References
- **historical-risk** (wealth-management plugin): volatility and correlation inputs for mean-variance optimization
- **forward-risk** (wealth-management plugin): expected return forecasts and scenario analysis for portfolio optimization
- **diversification** (wealth-management plugin): diversification principles underpin all allocation frameworks
- **bet-sizing** (wealth-management plugin): position sizing within the allocated asset classes
- **rebalancing** (wealth-management plugin): maintaining allocation targets over time
- **quantitative-valuation** (wealth-management plugin): valuation signals can inform TAA decisions
- **retirement-decumulation** (wealth-management plugin): decumulation-phase glide paths and the sequence-of-returns risk that allocation choices must manage
- **factor-investing** (wealth-management plugin): sizing factor tilts as deliberate, survivable deviations from the policy portfolio
## Running the Script

```bash
uv run scripts/asset_allocation.py            # run the demo (uses PEP 723 inline deps)
uv run scripts/asset_allocation.py --verify   # check demo outputs against the worked examples (exit 1 on mismatch)
python3 scripts/asset_allocation.py            # alternative (requires: pip install numpy scipy)
```

The demo prints the calculations covered above; its values match the worked examples in this skill. Run `--help` for a list of the classes and functions. For programmatic use, import the module rather than running it — the demo only executes under `python asset_allocation.py`.
