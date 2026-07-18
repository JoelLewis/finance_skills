---
name: financial-planning-workflow
description: "Orchestrate the advisor workflow for assembling and delivering a comprehensive financial plan — data gathering, cash flow analysis, retirement modeling, Monte Carlo analysis, Roth conversion and withdrawal sequencing, Social Security claiming strategy, education and estate goals, scenario modeling, and prioritized recommendations. Use when the user asks about building a financial plan, structuring a planning engagement, retirement or Social Security modeling, Roth conversion strategy, scenario analysis, prioritizing competing recommendations, preparing a plan presentation, or deciding when a plan needs updating. Also trigger on 'comprehensive financial plan', 'discovery meeting', 'retirement modeling', 'Monte Carlo', 'Roth conversion', 'Social Security claiming', 'savings rate', or 'is my client on track'. For planning-tool data flows, capital market assumption governance, or connecting planning software to CRM/PMS, use financial-planning-integration instead."
---

# Financial Planning Workflow

## Core Concepts

### Client Profile and Data Gathering
The financial plan begins with a structured intake that captures the client's complete financial picture. Incomplete data leads to unreliable projections and missed planning opportunities. The advisor should collect the following categories systematically before any analysis begins:

**Household demographics** — ages, marital status, dependents (ages and expected years of financial support), health status and family longevity history, employment status and expected retirement dates, state of residence (for state tax modeling).

**Income and benefits** — gross salary, bonuses, commissions, self-employment income, rental income, pension details (defined benefit formula, COLA, survivor options), Social Security statements for both spouses, deferred compensation schedules, stock option or RSU vesting schedules.

**Expense analysis** — fixed obligations (mortgage, loan payments, insurance premiums, property taxes), discretionary spending (travel, dining, entertainment), irregular expenses (home maintenance, vehicle replacement, medical), and expected changes (mortgage payoff date, child-related expenses aging out, healthcare costs in retirement).

**Assets and accounts** — taxable brokerage accounts, traditional and Roth IRAs, 401(k)/403(b) balances and contribution rates, HSAs, 529 plans, real estate (primary residence and investment properties with basis information), business ownership interests, cash reserves, and any concentrated stock positions.

**Liabilities** — mortgage balance, rate, and remaining term; student loans; auto loans; credit card balances; HELOCs; any contingent liabilities (co-signed loans, pending legal obligations).

**Insurance** — life insurance (term and permanent, face amounts, premiums, cash values), disability coverage (employer-provided and individual, benefit amounts, elimination periods, own-occupation vs any-occupation), long-term care coverage, umbrella liability, and health insurance details.

**Estate documents** — wills, trusts, powers of attorney, healthcare directives, beneficiary designations on all accounts and insurance policies, any existing irrevocable trusts or family limited partnerships.

**Tax returns** — most recent two to three years of federal and state returns, revealing effective tax rates, deduction patterns, AMT exposure, capital gain/loss carryforwards, and charitable giving history.

### Cash Flow Analysis
Cash flow is the engine of the financial plan. Before projecting any future goals, the advisor must establish a reliable baseline of current income, spending, and savings. Key steps include:

1. **Categorize income sources** by stability (guaranteed vs variable), tax treatment (ordinary, qualified dividend, capital gain, tax-exempt), and expected duration (salary until retirement, pension for life, Social Security from age 62-70).
2. **Build the expense baseline** from actual spending data (bank and credit card statements), not estimates. Clients consistently underestimate discretionary spending. Apply a 10-15% buffer if only using estimates.
3. **Calculate the savings rate** as a percentage of gross income. A rate below 15% for clients more than 15 years from retirement is a yellow flag. Document where current savings flow (401k, IRA, taxable, 529).
4. **Project cash flow changes** over time: salary growth assumptions, expense step-downs (mortgage payoff, children finishing college), expense step-ups (healthcare in early retirement before Medicare, long-term care in later years), and inflation-adjusted lifestyle spending.
5. **Identify surplus or deficit** in the current year and in projected future years. A current surplus is the raw material for all goal funding. A current deficit means the plan must address spending reduction or income enhancement before layering on new goals.

### Retirement Modeling
Retirement is typically the largest and most complex goal in the plan. The analysis has two phases: accumulation (saving and investing toward retirement) and distribution (drawing down assets to fund retirement spending).

**Accumulation phase** — project account balances forward using current savings rates, employer matches, expected returns by asset class, and tax-deferred growth. Model the impact of increasing savings rates (e.g., saving all future raises). Account for expected lump-sum events (inheritance, home downsizing, stock option exercises).

**Social Security optimization** — model claiming at 62, full retirement age, and 70 for both spouses. The optimal strategy depends on relative earnings, age difference, health, and other income sources. Delayed claiming increases the inflation-adjusted guaranteed income floor. For married couples, evaluate the restricted application and survivor benefit interaction.

**Pension integration** — if the client has a defined benefit pension, model the lump-sum vs annuity decision, survivor benefit election (joint-and-survivor percentages), and COLA provisions. The pension's guaranteed income reduces the withdrawal burden on the investment portfolio.

**Sustainable withdrawal strategy** — establish the initial withdrawal rate (commonly benchmarked against 4% but adjusted for plan duration, asset allocation, and flexibility). Model withdrawal sequencing across account types: draw from taxable first to allow tax-deferred accounts to compound, but consider Roth conversion opportunities in low-income years between retirement and Social Security/RMD onset.

**Monte Carlo simulation** — run probability-of-success analysis using 1,000+ randomized return sequences to stress-test the plan against sequence-of-returns risk. A plan with 80-90% success probability is generally considered funded. Below 70% requires material adjustment. Present results as a confidence range rather than a single deterministic projection.

**Longevity risk** — plan to age 90-95 for at least one spouse. Use mortality tables adjusted for client health and family history. Discuss the asymmetry: running out of money is catastrophic, while dying with a surplus is merely suboptimal.

### Education Funding
For clients with children or grandchildren, education funding is modeled as a specific goal with its own timeline and inflation rate:

- **Estimate total cost** using current tuition for target institution types (public in-state, public out-of-state, private) inflated at the education inflation rate (historically 5-6% annually, higher than general CPI).
- **Assess current 529 balances** and ongoing contribution capacity. Model the investment glide path within the 529 (aggressive early, conservative as enrollment approaches).
- **Analyze the funding gap** between projected 529 balances and total cost. Determine how much must come from current cash flow at the time of enrollment.
- **Consider financial aid interaction** — 529 assets owned by the parent count as parental assets on the FAFSA (assessed at up to 5.64% vs 20% for student assets). The simplified FAFSA replaced the Expected Family Contribution with the Student Aid Index (SAI), and under SAI rules distributions from grandparent-owned 529s no longer count as student income. Verify current FAFSA treatment when modeling aid eligibility.
- **Evaluate trade-offs** between fully funding education and other goals. Retirement should generally take priority because education can be funded with loans while retirement cannot.

### Estate Planning Integration
The financial plan must address wealth transfer, even for clients who do not consider themselves wealthy. Key elements:

- **Estate tax exposure** — calculate the gross estate (all assets including life insurance death benefits, retirement accounts, and real estate) against the current federal exemption. The scheduled TCJA sunset never took effect: the One Big Beautiful Bill Act (2025) set the exemption at $15 million per person (about $30 million per married couple) for 2026, made it permanent, and indexed it for inflation beginning in 2027. Verify current-year exemption values before modeling. For clients near or above the exemption, model lifetime gifting and trust strategies that use the exemption.
- **Trust structures** — identify whether existing or new trusts serve the client's goals: revocable living trusts for probate avoidance, irrevocable life insurance trusts (ILITs) for removing life insurance from the estate, generation-skipping trusts, and special needs trusts for dependents with disabilities.
- **Beneficiary designation audit** — verify that beneficiary designations on retirement accounts, insurance policies, and TOD/POD accounts are current and consistent with the estate plan. Beneficiary designations override wills.
- **Charitable giving strategy** — for charitably inclined clients, evaluate donor-advised funds, qualified charitable distributions (QCDs) from IRAs after age 70.5, charitable remainder trusts, and bunching strategies for itemized deductions.
- **Business succession** — for business owners, integrate the succession or sale timeline with the retirement plan. Model the after-tax proceeds from a business sale and the transition of income from active business earnings to investment portfolio withdrawals.

### Risk Management Review
Assess whether the client's insurance coverage matches the risks identified in the plan:

- **Life insurance gap** — calculate the capital needed to replace the insured's income contribution, fund remaining goals (education, mortgage payoff), and provide for surviving dependents. Subtract existing coverage and assets. The gap determines additional coverage needed.
- **Disability coverage** — verify that combined employer and individual coverage replaces at least 60% of gross income. Check elimination periods, benefit duration, own-occupation definitions, and coordination with other income sources.
- **Long-term care** — for clients over age 50, model the potential cost of extended care (in-home, assisted living, skilled nursing) and evaluate traditional LTC insurance, hybrid life/LTC products, or self-insurance strategies based on asset levels.
- **Liability coverage** — ensure umbrella liability coverage is adequate relative to net worth. Minimum recommended coverage is typically equal to net worth or $1 million, whichever is greater.

### Scenario Modeling
A single deterministic projection creates false precision. The plan should present at least three scenarios to frame the range of outcomes:

1. **Base case** — reasonable assumptions for returns, inflation, income growth, and spending. This is the plan the client tracks against.
2. **Optimistic case** — higher returns, earlier-than-expected inheritance, lower healthcare costs, or ability to work part-time in early retirement. Shows upside potential and what becomes possible.
3. **Pessimistic case** — lower returns, job loss at age 55, major health event, market crash in early retirement years (sequence-of-returns stress test), or need to support aging parents. Shows downside risk and what breaks.

Additionally, model specific what-if questions the client raises: "What if I retire at 58 instead of 62?" "What if we move to a no-income-tax state?" "What if we pay for private school?" Each what-if should show the impact on retirement success probability and the trade-off with other goals.

### Prioritized Recommendations
The output of the planning process is a ranked list of action items. Prioritization follows this framework:

1. **Foundation items first** — emergency fund adequacy, appropriate insurance coverage, estate document completion. These protect against catastrophic risk and cost relatively little.
2. **Employer match capture** — maximize 401(k) contributions to the employer match. This is an immediate 50-100% return.
3. **High-interest debt elimination** — pay down debt with interest rates above the expected portfolio return (typically any debt above 6-7%).
4. **Tax-advantaged account maximization** — fill remaining 401(k)/403(b) space, fund Roth IRAs (or backdoor Roth), HSA contributions.
5. **Goal-specific funding** — direct remaining surplus to prioritized goals (retirement shortfall, education funding, home purchase).
6. **Tax optimization moves** — Roth conversions in low-income years, tax-loss harvesting, asset location optimization, charitable giving strategies.
7. **Estate planning actions** — trust creation, beneficiary updates, gifting strategies.

Each recommendation should include a specific action, responsible party, target completion date, and the quantified impact on the plan (e.g., "Increasing 401k contribution from 6% to 10% improves retirement success probability from 72% to 84%").

### Plan Presentation and Delivery
The plan presentation meeting converts analysis into client commitment. Effective delivery requires:

- **Lead with goals, not numbers** — begin by restating the client's goals and concerns as expressed in the discovery meeting. This demonstrates that the plan is personalized, not generic.
- **Present the base case first** — show that the plan works under reasonable assumptions before introducing stress scenarios. Clients anchor on the first number they see.
- **Use plain language** — translate Monte Carlo success rates into concrete terms: "In 85 out of 100 simulated market environments, your portfolio sustains your spending through age 95."
- **Discuss trade-offs explicitly** — when goals compete for limited resources, present the trade-off clearly: "Fully funding both children's education at private universities reduces your retirement success probability from 88% to 71%. Here are three alternatives that balance both goals."
- **Document agreed-upon actions** — end the meeting with a written list of next steps, owners, and deadlines. This becomes the implementation checklist that the advisory team tracks.

### Ongoing Monitoring
A financial plan is a living document. Establish triggers for plan updates:

- **Scheduled reviews** — full plan update annually, brief progress check at semi-annual or quarterly client reviews.
- **Life event triggers** — marriage, divorce, birth of a child, job change, inheritance, health diagnosis, home purchase or sale, retirement date change, death of a spouse.
- **Market-driven triggers** — portfolio value deviates more than 20% from the plan projection, interest rate environment changes materially (affecting bond allocation and mortgage decisions), or tax law changes affect planning assumptions.
- **Goal completion** — when a goal is achieved (mortgage paid off, child graduates, insurance need expires), reallocate the freed cash flow to remaining or new goals.

At each update, re-run the probability-of-success analysis and compare to the prior review. Track whether the plan is improving, stable, or deteriorating, and adjust recommendations accordingly.

## Worked Examples

### Example 1: Dual-Income Couple with Retirement and Education Goals
**Scenario:** Michael (44) and Sarah (42) are married with two children (ages 10 and 7). Combined gross income is $285,000. They have $620,000 in retirement accounts (mix of 401k and Roth IRA), $85,000 in 529 plans, a $480,000 mortgage at 3.25% with 22 years remaining, and $45,000 in taxable savings. Both have employer-sponsored health and disability insurance. They have basic term life policies ($500,000 each) and outdated wills drafted before their second child was born. They want to retire at 62, send both children to four-year public universities, and pay off the mortgage before retirement.

**Planning Elements:**
- Cash flow analysis reveals a $2,800/month surplus after all current obligations and savings. Current savings rate is 18% of gross income (strong).
- Retirement modeling projects $2.1M in retirement assets at age 62 assuming 6.5% nominal returns, current contribution rates, and employer matches. Estimated retirement spending is $9,500/month in today's dollars. Social Security at full retirement age (67) provides combined $5,200/month. Monte Carlo simulation shows 79% success probability at current trajectory — below the 85% target.
- Education funding gap: projected four-year public university cost is $140,000 per child (in future dollars). Current 529 balances plus ongoing contributions cover approximately 65% of costs. Remaining $98,000 gap across both children.
- Mortgage payoff by 62 requires $1,400/month in additional principal payments starting now, which consumes half the current surplus.
- Life insurance gap analysis shows $500,000 per spouse is insufficient — Michael's income supports the mortgage and retirement savings; Sarah's supports education funding and lifestyle. Recommended coverage: $1.2M on Michael, $800,000 on Sarah.
- Estate documents need updating: add second child as beneficiary, establish guardianship designations, update healthcare directives.

**Analysis:** The plan reveals competing demands on a finite surplus. Prioritized recommendations: (1) Update wills and beneficiary designations immediately — no cost, high risk reduction. (2) Increase term life coverage to recommended levels — adds approximately $120/month. (3) Increase 401(k) contributions by 2% of salary each ($475/month combined) to close the retirement gap — improves Monte Carlo success to 86%. (4) Maintain current 529 contributions but do not accelerate — the education gap can be bridged with cash flow from reduced expenses as children age and from the surplus freed when the mortgage reaches its natural payoff date (age 66). (5) Do not accelerate mortgage payoff — the 3.25% rate is below expected portfolio returns, and the capital is more productive in retirement accounts. The mortgage payoff falls after the target retirement date, but the remaining balance ($68,000) is manageable from retirement assets. Present this trade-off explicitly so the client can make an informed decision about the emotional value of entering retirement debt-free versus the financial efficiency of maintaining the mortgage.

### Example 2: Near-Retirement Single Professional
**Scenario:** Patricia (58) is a single corporate attorney earning $210,000 annually. She has $1.4M in her 401(k), $180,000 in a Roth IRA, $95,000 in a taxable brokerage account, and owns her home outright (valued at $550,000). She wants to retire at 62 but is concerned about healthcare costs before Medicare eligibility at 65. Her Social Security benefit at 62 is $2,100/month; at 67 it is $3,100/month; at 70 it is $3,850/month. She has no pension, no dependents, and her estate plan leaves everything to a sibling and two nieces. She has employer-provided life and disability insurance that terminates at retirement.

**Planning Elements:**
- Cash flow analysis shows current spending of $7,800/month. In retirement, work-related expenses drop but healthcare costs add approximately $1,200/month for ACA marketplace coverage (ages 62-65). Net retirement spending estimate: $7,200/month in today's dollars.
- Retirement modeling: at age 62, projected portfolio is $1.72M across all accounts. Required annual withdrawal is approximately $86,400 (before Social Security). If she claims Social Security at 62 ($25,200/year), portfolio withdrawal drops to $61,200/year — a 3.6% withdrawal rate on the portfolio. Monte Carlo simulation shows 83% success probability.
- Delaying Social Security to 67 increases the annual benefit by $12,000/year (guaranteed, inflation-adjusted) but requires higher portfolio withdrawals for five additional years. Net present value analysis favors delay if Patricia lives past age 80. Delaying to 70 improves success probability to 91% but requires $86,400/year from the portfolio for eight years.
- Roth conversion opportunity: between ages 62 and 67, Patricia's income drops from $210,000 to near zero (only taxable portfolio withdrawals). This creates a five-year window to convert 401(k) assets to Roth at lower tax brackets, reducing future RMD tax burden and providing tax-free income flexibility in later years.
- Healthcare bridge: ACA marketplace premiums are income-sensitive (premium tax credits phase in below 400% FPL). Managing taxable income through strategic Roth conversions and withdrawal sequencing can optimize premium subsidies during the 62-65 gap.
- No dependents means life insurance is unnecessary post-retirement. Disability insurance is no longer needed once she stops working.

**Analysis:** Prioritized recommendations: (1) Build a two-year cash reserve ($175,000) in the taxable account before retirement to fund the first two years of expenses without forced portfolio withdrawals in a potential down market — begin redirecting current savings surplus now. (2) Retire at 62 as planned — the numbers support it. (3) Delay Social Security to age 70 — the guaranteed income increase is the most efficient longevity insurance available, and her portfolio can sustain the interim withdrawals. (4) Execute systematic Roth conversions of $80,000-$100,000 annually from ages 62-67, filling the 22% and 24% tax brackets. This front-loads tax liability but reduces lifetime taxes and eliminates RMD pressure. (5) Manage ACA income carefully — keep MAGI below the subsidy cliff during ages 62-65 by coordinating Roth conversion amounts with healthcare premium optimization. (6) Simplify the estate plan — current documents are adequate, but consider adding a revocable living trust to avoid probate on the real estate and ensure seamless transfer to the sibling and nieces.

### Example 3: Post-Divorce Financial Reset
**Scenario:** David (47) recently finalized a divorce. He received $310,000 from the division of retirement accounts (rolled into an IRA), $120,000 in a taxable account, and retains the family home (valued at $425,000 with a $280,000 mortgage at 4.75%). He has primary custody of two children (ages 12 and 14) and receives $2,400/month in child support until each child turns 18. His salary is $135,000. He has a $250,000 term life policy from his employer but no individual coverage. His previous financial plan was built around dual incomes and is now obsolete. He has no updated will or estate documents.

**Planning Elements:**
- Cash flow analysis reveals a tight budget: after mortgage ($1,850/month), child-related expenses, and basic living costs, the monthly surplus is only $400. Child support of $2,400/month expires in 4 years (older child) and 6 years (younger child). Current savings rate is under 4% of gross income — a critical concern.
- Retirement modeling: $310,000 in the IRA at age 47 with minimal ongoing contributions projects to approximately $740,000 by age 67 at 6.5% returns. Combined with Social Security (estimated $2,600/month at 67), this supports only $5,200/month in retirement — well below his current $7,800/month spending. Monte Carlo success probability: 52%. The plan is significantly underfunded.
- Housing decision: the mortgage at 4.75% on a home sized for a family may not be optimal for a single parent whose children will leave in 4-6 years. Selling the home, capturing approximately $145,000 in equity, moving to a less expensive property, and redirecting the savings could materially improve the retirement outlook. However, this must be weighed against stability for the children during the post-divorce transition.
- Insurance gaps: the $250,000 employer term policy is insufficient. If David dies, the children lose his income ($135,000/year) and child support ends. They need a guardian with resources to fund their care and education. Recommended coverage: $750,000-$1,000,000 of individual term life, decreasing as the children age out.
- Estate documents are urgent: the former spouse is likely still named as beneficiary on retirement accounts, insurance policies, and possibly the will. These must be updated immediately. A new will must name a guardian for the minor children.
- Education funding: no 529 accounts exist. With the tight budget, starting 529 contributions is unrealistic until child support expenses end and the surplus increases.

**Analysis:** This plan requires honest conversation about trade-offs and a phased approach. Prioritized recommendations: (1) Update all beneficiary designations and estate documents within 30 days — this is the highest-urgency item. Name a guardian for the children. Remove the former spouse from all accounts. (2) Obtain individual term life insurance ($750,000, 15-year term) immediately while David is healthy — estimated cost $65/month. (3) Increase 401(k) contribution to capture the full employer match if not already doing so. (4) Build a three-month emergency fund ($18,000) in a high-yield savings account — currently has no dedicated emergency reserve. (5) When child support for the older child ends (in 4 years), redirect $1,200/month to retirement savings — this single change improves Monte Carlo success to 68%. When the second child's support ends, redirect another $1,200/month — success probability reaches 79%. (6) Evaluate the housing decision at the 4-year mark when the older child leaves for college. At that point, downsizing becomes practical and can unlock equity for retirement savings. (7) Education funding is deferred — David should discuss expectations honestly with the children. Community college for two years followed by university transfer, merit scholarships, and modest student loans are realistic alternatives to full four-year residential funding. Retirement must take priority because it cannot be financed with debt. Present the full timeline showing how the plan improves materially as child-related expenses roll off over the next six years.

## Common Pitfalls
- Treating the financial plan as a one-time deliverable rather than a living document that requires regular updates and course corrections
- Starting analysis before completing data gathering, leading to inaccurate projections and missed planning opportunities
- Using a single deterministic projection instead of scenario modeling, which creates false confidence in a specific outcome
- Failing to model the interaction between goals — funding one goal aggressively may starve another
- Allowing the client's emotional preference (e.g., paying off a low-rate mortgage) to override financial efficiency without at least quantifying the trade-off
- Ignoring the healthcare cost bridge between early retirement and Medicare eligibility at 65
- Neglecting to audit beneficiary designations, which override wills and can direct assets to former spouses or deceased individuals
- Modeling retirement spending as a flat inflation-adjusted number when spending patterns actually change (higher early in retirement during active years, lower in middle years, higher again if long-term care is needed)
- Prioritizing education funding over retirement — clients can borrow for education but cannot borrow for retirement
- Presenting too many recommendations at once without clear prioritization, leading to client overwhelm and inaction

## Cross-References
- **savings-goals** (wealth-management plugin): provides goal-based savings calculations referenced during retirement and education analysis
- **debt-management** (wealth-management plugin): debt payoff strategies are evaluated during cash flow and recommendation phases
- **emergency-fund** (wealth-management plugin): emergency fund adequacy is assessed early in the planning process
- **liquidity-management** (wealth-management plugin): cash flow tier structure informs the plan's liquidity analysis
- **tax-efficiency** (wealth-management plugin): tax-aware strategies (Roth conversions, asset location) are core plan recommendations
- **investment-policy** (wealth-management plugin): the financial plan informs and is codified in the investment policy statement
- **time-value-of-money** (core plugin): PV/FV/annuity calculations underpin all projection modeling
- **client-review-prep** (advisory-practice plugin): plan progress review is integrated into the periodic client review workflow
- **financial-planning-integration** (advisory-practice plugin): covers the software and system integration for planning tools
- **proposal-generation** (advisory-practice plugin): the financial plan often leads to an investment proposal for implementation
- **tax-loss-harvesting** (wealth-management plugin): TLH is a specific tax recommendation that may emerge from the plan
