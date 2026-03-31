---
name: bet-sizing
description: "Determine how much capital to allocate to individual positions within a portfolio. Use when the user asks about position sizing, the Kelly criterion, fractional Kelly, risk budgeting, or conviction weighting. Also trigger when users mention 'how much to put in one stock', 'maximum position size', 'how concentrated should my portfolio be', 'number of holdings', 'VaR budget per position', 'how big a bet', or ask about scaling position sizes with volatility."
---

# Bet Sizing

## Purpose
Frameworks for determining how much capital to allocate to individual positions. Even a portfolio of good ideas can fail with poor sizing.

## Layer
4 — Portfolio Construction

## Direction
prospective

## When to Use
- Sizing a new position or adjusting an existing one
- Applying Kelly criterion to a bet or investment with estimable odds
- Allocating a risk budget across active positions
- Setting maximum position sizes (liquidity, risk, or regulatory limits)
- Scaling position sizes with volatility changes

## Core Concepts

### Sizing Method Decision Framework

Use this to select the appropriate method:

| Situation | Method | Key Input |
|-----------|--------|-----------|
| Binary bet with known odds | Kelly (Discrete) | win prob p, payoff odds b |
| Investment with return/vol estimates | Kelly (Continuous) | excess return mu-r_f, volatility sigma |
| Parameter uncertainty is high | Fractional Kelly | Kelly fraction (1/2, 1/3, 1/4) |
| Portfolio-level risk constraint | Risk Budgeting | total VaR or tracking error budget |
| Hard caps required (regulatory, liquidity) | Max Position Limits | ADV, mandate rules |
| Qualitative edge, no precise probabilities | Conviction Weighting | edge score x certainty score |
| Volatility regime is shifting | Volatility Scaling | target risk / current vol |

### Sizing Workflow

1. **Determine edge**: Estimate expected return, win probability, or conviction score
2. **Select method** from the table above based on available inputs
3. **Calculate raw size** using the appropriate formula (see Key Formulas)
4. **Apply fractional Kelly** if using Kelly — default to half Kelly unless parameter confidence is high
5. **Check constraints**: liquidity limit (position < 10-25% of ADV), risk limit (position risk < 10% of portfolio risk), regulatory caps
6. **Final size** = min(calculated size, all binding constraints)

### Kelly Criterion

**Discrete** (binary bet): f* = (b*p - q) / b where b = payoff odds, p = win prob, q = 1-p. Bet only when b*p > q (positive edge).

**Continuous** (investment): f* = (mu - r_f) / sigma^2. Often implies leverage — an asset with 8% excess return and 20% vol gives f* = 200%.

### Fractional Kelly

Full Kelly maximizes geometric growth but assumes perfect parameter knowledge. Use a fraction to trade small growth reduction for large risk reduction:

| Fraction | Growth Retained | When to Use |
|----------|----------------|-------------|
| Half (f*/2) | ~75% | Default practical choice |
| Third (f*/3) | ~56% | High parameter uncertainty |
| Quarter (f*/4) | ~44% | Very uncertain estimates |

### Risk Budgeting

Allocate risk (not capital) across positions against a total budget (e.g., portfolio VaR or tracking error).

- **VaR-based**: Position VaR_i = w_i * sigma_i * z_alpha * V; sum of position VaRs <= total VaR budget
- **Tracking error**: Size active positions so risk contributions sum to active risk budget

### Maximum Position Limits

- **Liquidity**: Position < 10-25% of ADV (exit within 5-10 trading days)
- **Risk**: Single position risk contribution < 10% of portfolio risk; weight < 5% (diversified) or 10% (concentrated)
- **Regulatory**: Diversified mutual fund max 5% per name; non-diversified max 25%

### Conviction Weighting

Score each position: edge strength (1-5) x certainty (1-5). Size proportional to the product. Use when precise probabilities are unavailable but qualitative assessment of edge exists.

### Volatility Scaling

Adjusted size = Target risk / Current volatility. When vol doubles, size halves, keeping dollar risk constant. Core principle in managed futures and risk-targeting strategies.

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| Kelly (Discrete) | f* = (b*p - q) / b | Binary bet sizing |
| Kelly (Continuous) | f* = (mu - r_f) / sigma^2 | Investment position sizing |
| Half Kelly | f = f* / 2 | Practical conservative sizing |
| Growth Rate at Kelly | g* = (mu - r_f)^2 / (2*sigma^2) | Maximum geometric growth |
| Growth Rate at f | g(f) = f*(mu - r_f) - f^2*sigma^2/2 | Growth rate for any fraction |
| Volatility-Scaled Size | w = target_risk / sigma_i | Constant risk per position |
| Position VaR | VaR_i = w_i * sigma_i * z_alpha * V | Position-level risk |

## Worked Examples

### Example 1: Discrete Kelly with Fractional Adjustment
**Given:** p = 55%, q = 45%, b = 1 (even-money bet)

f* = (1 * 0.55 - 0.45) / 1 = **10%** of wealth per bet

Half Kelly: 10% / 2 = **5%** — retains 75% of growth rate, substantially lower drawdown.

### Example 2: Continuous Kelly for an Investment
**Given:** Excess return (mu - r_f) = 8%, volatility (sigma) = 20%

f* = 0.08 / 0.04 = **200%** (implies 2x leverage)

Apply fractional Kelly given parameter uncertainty:

| Fraction | Allocation | Growth Rate |
|----------|-----------|-------------|
| Full Kelly | 200% | g* = 0.08^2 / (2 * 0.04) = 8.0% p.a. |
| Half Kelly | 100% | g = 1.0 * 0.08 - 1.0^2 * 0.04/2 = 6.0% p.a. (75%) |
| Quarter Kelly | 50% | g = 0.5 * 0.08 - 0.25 * 0.04/2 = 3.5% p.a. (44%) |

Half Kelly (100% allocation, no leverage) is prudent given estimation uncertainty.

## Common Pitfalls
- Never use full Kelly in practice — parameter estimation error turns optimal into catastrophic; default to half Kelly or less
- Kelly maximizes log wealth, which may not match the investor's utility function or risk tolerance
- Kelly-optimal size may exceed market liquidity — always check against ADV constraints
- Single-asset Kelly ignores correlations; correlated positions collectively require smaller sizing
- Historical win rates overstate future edge (survivorship bias) — discount estimates before sizing
- Edge and volatility are time-varying — re-evaluate sizing as regimes shift

## Cross-References
- **historical-risk** (wealth-management plugin, Layer 1a): realized volatility as a key input to Kelly sizing
- **forward-risk** (wealth-management plugin, Layer 1b): expected return forecasts as inputs to Kelly criterion
- **diversification** (wealth-management plugin, Layer 4): tension between concentration (large bets) and diversification (many small bets)
- **asset-allocation** (wealth-management plugin, Layer 4): bet sizing operates within the asset allocation framework
- **rebalancing** (wealth-management plugin, Layer 4): positions drift from target sizes and require rebalancing
- **quantitative-valuation** (wealth-management plugin, Layer 3): valuation-based edge estimates feed into conviction weighting

## Reference Implementation
See `scripts/bet_sizing.py` for computational helpers.
