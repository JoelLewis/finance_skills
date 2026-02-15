---
name: finance-psychology
description: Behavioral finance biases, nudges, decision frameworks, emotional discipline in investing.
allowed-tools: ["Bash", "Read", "Write", "Edit"]
---

# Finance Psychology — Behavioral Finance

## Purpose
Help users recognize and mitigate cognitive and emotional biases that impair investment decisions. This skill provides frameworks for identifying behavioral pitfalls, implementing nudges and choice architecture, and coaching investors toward disciplined, evidence-based decision-making.

## Layer
7 — Behavioral Finance

## Direction
both

## When to Use
- Helping users recognize cognitive biases affecting their financial decisions
- Making better financial decisions by applying debiasing techniques
- Understanding market psychology, sentiment extremes, and crowd behavior
- Behavioral coaching: building emotional discipline and rules-based investing habits
- Designing choice architecture (defaults, auto-enrollment, commitment devices)
- Evaluating whether a decision is driven by analysis or by emotion

## Core Concepts

### Loss Aversion
Losses hurt approximately 2x more than equivalent gains feel good (Kahneman & Tversky, Prospect Theory 1979).

**Impact:** Investors sell winners too early to "lock in" gains while holding losers too long hoping to break even. This is the *disposition effect* — it reverses the rational approach of cutting losses and letting winners run.

**Mitigation:**
- Pre-commit to stop-loss levels at the time of purchase, before emotions engage.
- Use rules-based rebalancing that forces trimming winners and adding to underperformers mechanically.
- Reframe: evaluate the holding as if you held cash — "would I buy this today at this price?"

### Overconfidence
Investors systematically overestimate their own skill, knowledge, and precision while underestimating uncertainty and the role of luck.

**Impact:** Excessive trading frequency (which erodes returns through costs and taxes), concentrated positions, under-diversification, and underestimation of tail risks.

**Mitigation:**
- Track prediction accuracy over time — most people discover their hit rate is far lower than they believe.
- Use base rates: "what fraction of active stock pickers beat the index over 10 years?" (historically ~10-15%).
- Size positions according to conviction *and* uncertainty; use Kelly-criterion-inspired frameworks.

### Anchoring
Over-relying on an initial reference point — often the purchase price, a 52-week high, or an analyst price target — when making decisions.

**Impact:** Holding a stock because "it was worth $X" even though fundamentals have changed. Refusing to sell below cost basis despite deteriorating prospects. Fixating on round numbers as support/resistance.

**Mitigation:**
- Evaluate current fundamentals and forward-looking value, not historical prices.
- Ask: "If I didn't own this, would I buy it today at this price with this information?"
- Use multiple independent valuation methods to avoid anchoring on a single estimate.

### Recency Bias
Overweighting recent events and extrapolating them into the future, while underweighting long-term historical base rates.

**Impact:** Chasing performance after strong recent returns, panic selling after drawdowns, extrapolating recent trends indefinitely (e.g., "stocks always go up" after a bull run, or "the market is broken" after a crash).

**Mitigation:**
- Provide long-term historical context: show 50+ year return distributions, not just recent quarters.
- Systematic rebalancing forces buying what has fallen and selling what has risen.
- Use dollar-cost averaging to remove timing decisions.

### Herding
Following the crowd, driven by fear of missing out (FOMO) or social proof. The impulse to buy when everyone is buying and sell when everyone is selling.

**Impact:** Buying at market tops when euphoria peaks, selling at bottoms when panic is greatest. This is the single most reliable way to destroy wealth over time.

**Mitigation:**
- Contrarian checklist: when you feel strongest urge to act with the crowd, pause and review your Investment Policy Statement (IPS).
- Pre-committed IPS with rebalancing bands removes the decision from the emotional moment.
- Warren Buffett's rule: "Be fearful when others are greedy, and greedy when others are fearful."

### Mental Accounting
Treating money differently based on its source, label, or intended use, rather than recognizing that money is fungible.

**Impact:** Taking more risk with "house money" (gains), keeping too much in low-yield savings earmarked for specific goals while carrying high-interest debt, evaluating each account in isolation rather than viewing the total portfolio holistically.

**Mitigation:**
- View total portfolio across all accounts as a single allocation.
- Recognize the fungibility of money: a dollar of gains is worth exactly the same as a dollar of salary.
- Use a unified financial plan that considers all assets and liabilities together.

### Status Quo Bias
Preference for the current state of affairs, inertia, and the tendency to avoid making changes even when changes are beneficial.

**Impact:** Not rebalancing portfolios that have drifted far from targets, staying in underperforming investments, remaining in high-fee funds, keeping legacy holdings for no analytical reason.

**Mitigation:**
- Automated rebalancing (calendar-based or threshold-based) removes the need for active decisions.
- Periodic portfolio review (quarterly or semi-annually) with a structured checklist.
- Apply the "clean slate" test: "if I were building this portfolio from scratch today, would I hold these same positions?"

### Confirmation Bias
Seeking, interpreting, and remembering information in a way that confirms pre-existing beliefs while ignoring or discounting disconfirming evidence.

**Impact:** Ignoring disconfirming evidence for a stock thesis, reading only bullish research on a long position, dismissing valid criticisms as "FUD" (fear, uncertainty, doubt).

**Mitigation:**
- Actively seek opposing viewpoints: for every bull case, find the strongest bear case.
- Devil's advocate process: assign someone (or yourself) to argue the opposite side before making a decision.
- Pre-mortem analysis: "assume this investment loses 50% — what went wrong?"

### Framing Effects
Decisions change depending on how choices are presented, even when the underlying facts are identical.

- "90% survival rate" vs "10% mortality rate" feel very different despite being logically equivalent.
- "You could lose $10,000" vs "there is a small probability of a 5% drawdown" trigger different responses.
- Presenting returns in nominal vs real terms changes perceived attractiveness.

**Mitigation:** Always reframe important financial decisions in multiple ways before acting. Present both gains and losses, both probabilities and dollar amounts.

### Nudges and Choice Architecture
Designing the decision environment to guide better outcomes without restricting freedom of choice (Thaler & Sunstein).

**Key nudges in investing:**
- **Auto-enrollment** in 401(k) plans dramatically increases participation rates (from ~50% to ~90% in studies).
- **Auto-escalation** increases contribution rates automatically with raises, overcoming inertia.
- **Default to diversified portfolio** (target-date fund) prevents naive 1/N allocation across random options.
- **Commitment devices** such as pre-set rebalancing rules, automatic savings transfers, and written Investment Policy Statements.
- **Cooling-off periods** before executing large trades based on emotional reactions.

## Worked Examples

### Example 1: Disposition Effect — Holding a Loser
**Given:** An investor bought shares of XYZ Corp at $100 per share. The stock is now at $80. The company has reported two consecutive quarters of declining revenue, lost a major customer, and faces a new competitive threat. The investor says, "I can't sell now — I'd be locking in a loss. I'll wait until it gets back to $100."

**Analysis:**
1. **Identify the bias:** This is classic loss aversion manifesting as the disposition effect. The investor is anchored to the $100 purchase price and is holding to avoid the psychological pain of realizing a loss.
2. **Reframe the decision:** The purchase price is a sunk cost — it is irrelevant to the forward-looking decision. The correct question is: "If I had $80 in cash right now, would I buy XYZ Corp today given its deteriorating fundamentals?"
3. **Evaluate fundamentals objectively:** Two quarters of declining revenue, lost customer, new competition — the thesis that justified buying at $100 may be broken.
4. **Apply a framework:** If the original investment thesis is invalidated, the rational action is to sell regardless of the current price relative to cost basis. Tax-loss harvesting may even provide a tangible benefit from realizing the loss.
5. **Implement safeguards for the future:** Set stop-loss rules at time of purchase (e.g., "I will re-evaluate if the stock falls 15% or if the company misses revenue estimates for two consecutive quarters"). Write these rules down before buying.

### Example 2: Recency Bias — Panic After a Drawdown
**Given:** After a 25% market drawdown in 2022, an investor wants to move their entire portfolio to 100% cash. They say, "The market is clearly broken. I need to protect what I have left."

**Analysis:**
1. **Identify the bias:** Recency bias — the investor is extrapolating the recent drawdown into an expectation of continued decline. The emotional pain of recent losses is dominating their assessment of future probabilities.
2. **Provide historical context:**
   - The S&P 500 has experienced drawdowns of 20%+ roughly every 4-6 years on average.
   - After every previous bear market, the market recovered and reached new highs (median recovery time ~2 years).
   - Missing the 10 best days in the market (which often cluster near the worst days) dramatically reduces long-term returns.
3. **Quantify the cost of market timing:** Selling after a 25% drop and waiting for "clarity" means the investor has already absorbed the loss and now needs to correctly time the re-entry — getting two decisions right instead of zero.
4. **Behavioral coaching approach:**
   - Validate the emotion: "It is completely normal to feel anxious after a significant decline."
   - Reframe with data: show historical drawdown and recovery chart.
   - Revisit the financial plan: "Your retirement is 20 years away. Does a 25% drawdown in one year change the long-term math?"
   - Offer a compromise if needed: "If you must act, reduce equity by 5-10% rather than going to 100% cash. This satisfies the urge to do something while preserving most of the recovery upside."

## Common Pitfalls
- Biases are far easier to spot in others than in ourselves — self-awareness is necessary but not sufficient.
- Knowing about biases does not eliminate them; debiasing is genuinely hard and requires structural safeguards (rules, automation, accountability).
- Over-correcting: contrarianism for its own sake is also a bias (reactance). Being contrarian is only valuable when supported by independent analysis.
- One-size-fits-all behavioral advice ignores individual differences in risk tolerance, time horizon, financial literacy, and emotional temperament.
- Patronizing tone: recognize and name biases without being condescending. The goal is to empower the investor, not to demonstrate intellectual superiority.
- Assuming rationality is always optimal: some "irrational" behaviors (e.g., holding cash for sleep-at-night comfort) may be utility-maximizing for that individual even if not return-maximizing.

## Cross-References
- Layer 1: `statistics-fundamentals` — base rates, probability calibration
- Layer 2: `time-value-of-money` — framing decisions in present value terms
- Layer 4: `historical-risk` — long-term drawdown context for recency bias discussions
- Layer 5: `asset-allocation` — systematic rebalancing as a debiasing mechanism
- Layer 5: `diversification` — structural protection against overconfidence and concentration
- Layer 8: `performance-reporting` — framing effects in how returns are presented

## Reference Implementation
See `scripts/finance_psychology.py` for computational helpers.
