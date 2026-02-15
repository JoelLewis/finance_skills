---
name: finance-psychology
description: Behavioral finance biases, nudges, decision frameworks, emotional discipline in investing.
allowed-tools: ["Bash", "Read", "Write", "Edit"]
---

# Behavioral Finance & Investor Psychology

## Purpose
Identify and mitigate cognitive and emotional biases that impair investment
decision-making. Provide evidence-based frameworks, nudges, and choice
architecture so users can make more rational financial decisions and maintain
emotional discipline through market cycles.

## Layer
7 — Behavioral Finance

## Direction
both

## When to Use
- Helping users recognize cognitive biases affecting their investment decisions
- Making better financial decisions under uncertainty
- Understanding market psychology and crowd behavior
- Behavioral coaching during periods of market stress or euphoria
- Designing choice architecture (defaults, auto-enrollment, auto-escalation)
- Evaluating whether an investment thesis is driven by evidence or by bias

## Core Concepts

### Loss Aversion
Losses hurt roughly 2x more than equivalent gains feel good (Kahneman &
Tversky, 1979 — Prospect Theory).

**Impact:** Investors sell winners too early to "lock in" gains and hold losers
too long hoping to break even. This is the *disposition effect* — one of the
most reliably documented patterns in individual investor behavior.

**Mitigation:**
- Pre-commit to stop-loss levels before entering a position.
- Use rules-based rebalancing that forces sells mechanically.
- Frame decisions in terms of total portfolio value, not individual positions.

### Overconfidence
Investors systematically overestimate their own skill and underestimate
uncertainty. Calibration studies show people who say they are "99% sure" are
correct only about 80% of the time.

**Impact:** Excessive trading (Barber & Odean found overconfident investors
trade more and earn less), concentrated positions, and under-diversification.

**Mitigation:**
- Track prediction accuracy over time — keep a decision journal.
- Use base rates: "What is the historical success rate of stock-pickers?"
- Size positions to survive being wrong.

### Anchoring
Over-relying on an initial reference point — often the purchase price, a
52-week high, or an analyst price target — when making subsequent judgments.

**Impact:** Holding a losing position because "it was worth $X" or refusing to
buy because a stock is "too far above" an arbitrary anchor, even when
fundamentals have changed.

**Mitigation:**
- Evaluate current fundamentals and forward expectations, not historical prices.
- Ask: "If I did not own this, would I buy it today at this price?"
- Use valuation models that are anchored to cash flows, not past prices.

### Recency Bias
Overweighting recent events when forming expectations about the future. After a
strong bull market, investors expect further gains; after a drawdown, they
expect further losses.

**Impact:** Chasing performance (buying what has gone up), panic selling after
drawdowns, and extrapolating short-term trends into long-term forecasts.

**Mitigation:**
- Provide long-term historical context (e.g., average recovery time after a
  20%+ drawdown).
- Systematic rebalancing forces a "buy low, sell high" discipline.
- Use base rates: "How often do drawdowns of this size lead to permanent loss?"

### Herding
Following the crowd — driven by FOMO (fear of missing out), social proof, or
the assumption that others have superior information.

**Impact:** Buying at market tops when enthusiasm is highest, selling at bottoms
when fear is greatest. Herding amplifies bubbles and crashes.

**Mitigation:**
- Contrarian checklist: "Am I buying because of analysis or because everyone
  else is?"
- Pre-committed Investment Policy Statement (IPS) that specifies allocation
  targets independent of market sentiment.
- Waiting periods before acting on "hot tips."

### Mental Accounting
Treating money differently depending on its source, intended use, or label —
even though money is fungible.

**Impact:** Taking excessive risk with "house money" (gains from previous
wins), maintaining separate "buckets" that prevent holistic portfolio
optimization, and ignoring the opportunity cost of idle cash in a savings
account while carrying high-interest debt.

**Mitigation:**
- View the total portfolio as a single entity with a unified risk-return
  profile.
- Recognize that a dollar is a dollar regardless of its source.
- Use goals-based investing deliberately, but optimize across goals.

### Status Quo Bias
Preferring the current state of affairs and resisting change, even when change
would be beneficial. Inertia is the default human behavior.

**Impact:** Not rebalancing drifted portfolios, staying in underperforming
funds due to inertia, failing to roll over old 401(k) accounts, and keeping
legacy positions out of habit.

**Mitigation:**
- Automated rebalancing (calendar or threshold-based).
- Periodic portfolio reviews with explicit "keep or sell" decisions.
- Default options that work in the investor's favor (see Nudges below).

### Confirmation Bias
Seeking, interpreting, and remembering information that confirms existing
beliefs while ignoring or dismissing disconfirming evidence.

**Impact:** An investor with a bullish thesis on a stock reads only positive
analysis, ignores warning signs, and interprets ambiguous news as supportive.

**Mitigation:**
- Actively seek opposing viewpoints — read the bear case.
- Devil's advocate process: before any major decision, articulate the three
  strongest reasons the thesis is wrong.
- Pre-mortem analysis: "Assume this investment failed — why did it fail?"

### Framing Effects
Decisions change depending on how choices are presented, even when the
underlying economics are identical.

- "90% survival rate" vs "10% mortality rate" feel very different.
- "You will lose $500/year in fees" vs "Your fee is 0.5%" triggers different
  reactions.
- Presenting returns as nominal vs real (inflation-adjusted) changes
  risk perception.

**Application:** Be deliberate about framing when presenting information.
Show both frames when the choice of frame could influence the decision.

### Nudges and Choice Architecture
Small design choices in how options are presented can dramatically shift
behavior without restricting freedom of choice (Thaler & Sunstein).

**Key nudges in investing:**
- **Auto-enrollment in 401(k):** Increases participation from ~60% to ~90%.
- **Auto-escalation:** Automatically increase contribution rate with raises
  (Save More Tomorrow program).
- **Default to diversified portfolio:** Target-date fund as the default
  removes the paralysis of choice.
- **Simplification:** Reducing the number of fund options increases
  participation and improves diversification.

## Worked Examples

### Example 1: Disposition Effect — Holding a Loser
**Given:** An investor bought shares at $100. The stock is now at $80 with
deteriorating fundamentals (declining revenue, rising debt, lowered guidance).
The investor resists selling, saying "I'll sell when it gets back to $100."

**Analysis:**
1. **Identify the bias:** This is classic loss aversion manifesting as the
   disposition effect. The $100 purchase price is an anchor, and selling at $80
   would crystallize a loss that feels painful.
2. **Reframe the decision:** "Forget the purchase price. You have $80 per
   share today. Would you buy this stock at $80 given current fundamentals?"
   If the answer is no, holding is equivalent to buying — you are choosing to
   allocate capital here every day you hold.
3. **Evaluate objectively:** Review the current thesis — revenue declining,
   debt rising, guidance lowered. The fundamentals that justified the original
   purchase no longer hold.
4. **Consider tax consequences:** If in a taxable account, the $20/share loss
   can be harvested for tax benefit — turning the bias on its head.
5. **Pre-commit going forward:** Establish rules: "I will sell any position
   that drops 15% below my intrinsic value estimate, regardless of purchase
   price." Write it in your IPS.

### Example 2: Recency Bias — Panic After a Drawdown
**Given:** After a 25% market drawdown in 2022, an investor wants to move
their entire portfolio to cash, saying "The market is going to keep falling."

**Analysis:**
1. **Identify the bias:** Recency bias — the investor is extrapolating the
   recent drawdown into an expectation of continued decline.
2. **Provide historical context:**
   - Since 1950, the S&P 500 has experienced 20%+ drawdowns roughly every
     5-7 years.
   - Average time to recover from a 20-30% drawdown: ~14 months.
   - An investor who went to cash after the 2008 crash and waited for
     "safety" missed the 68% rally in 2009-2010.
3. **Quantify the cost of market timing:** Missing the 10 best days over a
   20-year period cuts total return roughly in half. Most of those best days
   occur within two weeks of the worst days.
4. **Reframe:** "You are not predicting the market — you are reacting to pain.
   The decision to go to cash is a market-timing bet that requires being right
   twice: when to get out and when to get back in."
5. **Constructive action:** If the investor's risk tolerance has genuinely
   changed, adjust the asset allocation modestly and systematically — do not
   make an all-or-nothing move driven by fear.

## Common Pitfalls
- **Biases are easier to spot in others than in ourselves.** Self-awareness is
  necessary but not sufficient — use processes and rules to compensate.
- **Knowing about biases does not eliminate them.** Debiasing is hard.
  Education alone reduces bias only marginally; structural interventions
  (automation, checklists, rules) are more effective.
- **Over-correcting is also a bias.** Contrarianism for its own sake is not
  rational — sometimes the crowd is right.
- **One-size-fits-all behavioral advice ignores individual differences.** Risk
  tolerance, time horizon, financial literacy, and personality all affect which
  biases are most relevant for a given person.
- **Being patronizing or condescending.** Recognize biases respectfully —
  these are universal human tendencies, not signs of ignorance or stupidity.

## Cross-References
- **Layer 2 — Statistics Fundamentals** (`statistics-fundamentals`): base rates
  and probability concepts that support debiasing.
- **Layer 3 — Asset Allocation** (`asset-allocation`): rules-based rebalancing
  as a structural mitigation for behavioral biases.
- **Layer 3 — Diversification** (`diversification`): diversification reduces
  the impact of overconfident concentrated bets.
- **Layer 5 — Historical Risk** (`historical-risk`): historical drawdown data
  provides context to counter recency bias.
- **Layer 8 — Performance Reporting** (`performance-reporting`): framing
  effects in how returns and risk are presented to clients.

## Reference Implementation
See `scripts/finance_psychology.py` for computational helpers.
