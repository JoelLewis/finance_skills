---
name: proposal-generation
description: "Investment proposal generation: risk profiling output, model portfolio recommendation, fee illustration, scenario projections, compliance review, and proposal delivery for advisory practices."
allowed-tools: ["Bash", "Read", "Write", "Edit"]
---

# Proposal Generation

## Purpose
Guide the end-to-end creation of investment proposals for wealth management and advisory firms. This skill covers the complete proposal workflow — from prospect data collection and risk profiling through model portfolio recommendation, fee illustration, performance projections, compliance review, and proposal delivery. It enables a user or agent to design, build, evaluate, or automate proposal generation systems that convert prospects into advisory clients while satisfying regulatory requirements for performance presentation, fee disclosure, and suitability documentation.

## Layer
10 — Advisory Practice (Front Office)

## Direction
prospective

## When to Use
- Generating an investment proposal for a new prospect or existing client considering additional assets
- Mapping a risk questionnaire score to a recommended model portfolio
- Building the asset allocation and holdings detail section of a proposal document
- Creating fee illustrations that show tiered advisory fees, fund-level expenses, and total cost of ownership
- Producing Monte Carlo projections or historical scenario analysis for a proposed portfolio
- Analyzing a prospect's current portfolio to quantify improvement opportunities (risk reduction, cost savings, tax efficiency, diversification)
- Reviewing a proposal for compliance with the SEC Marketing Rule, advertising rules, and suitability requirements
- Designing proposal templates and workflows for a multi-advisor firm
- Evaluating or selecting proposal generation technology (Orion, Black Diamond, Riskalyze/Nitrogen, MoneyGuidePro, RightCapital)
- Standardizing model portfolio lineups and ensuring consistent recommendation rationale across advisors
- Preparing transition analysis showing the cost and tax impact of moving from an existing portfolio to a recommended portfolio

## Core Concepts

### Proposal Workflow Architecture
The investment proposal is the centerpiece of the advisory sales process. It translates a prospect's financial situation and goals into a specific, actionable investment recommendation. The end-to-end workflow proceeds through defined stages:

1. **Discovery meeting** — the advisor meets with the prospect to understand their financial situation, goals, concerns, and expectations. The advisor collects current account statements, tax returns, and any existing financial plan. The discovery meeting establishes the advisory relationship's tone and sets expectations for the proposal.
2. **Data collection and organization** — the advisor or operations team enters prospect data into the proposal system: personal information, current holdings (manually or via account aggregation), financial goals, time horizons, income, expenses, tax situation, and any unique circumstances (concentrated positions, restricted stock, estate planning needs).
3. **Risk profiling** — the prospect completes a risk tolerance questionnaire. The system scores the responses and produces a risk profile that maps to a position on the firm's risk-return spectrum. The risk profile is the bridge between subjective client preferences and objective portfolio construction.
4. **Model portfolio selection** — the risk profile score maps to a specific model portfolio from the firm's lineup. The advisor reviews the mapping, considers any client-specific factors that might warrant adjustment (tax sensitivity, income needs, ESG preferences, concentrated positions), and confirms the recommended model.
5. **Current portfolio analysis** — if the prospect has existing investments, the system analyzes their current holdings: asset allocation, risk metrics, expense ratios, tax lots, concentrated positions, overlap, and style drift. This analysis quantifies the gap between the current portfolio and the recommended model.
6. **Proposal document generation** — the system assembles the proposal document from templates, populating it with client-specific data, the recommended portfolio, fee schedule, projections, and disclaimers. The proposal document is the deliverable that the prospect reviews and uses to make their decision.
7. **Compliance review** — before the proposal is presented, it undergoes supervisory review to verify suitability documentation, performance presentation compliance, fee disclosure adequacy, and proper disclaimers. For firms subject to the SEC Marketing Rule, proposals that include performance data require additional scrutiny.
8. **Presentation and discussion** — the advisor presents the proposal to the prospect, walks through the analysis and recommendation, answers questions, and addresses concerns. The presentation meeting is where the advisory value proposition is demonstrated.
9. **Revision and finalization** — based on the prospect's feedback, the advisor may revise the recommendation (different model, adjusted allocation, modified fee structure) and regenerate the proposal.
10. **Acceptance and onboarding** — the prospect accepts the proposal by signing the advisory agreement (IMA or similar). The proposal data flows into the onboarding process: account opening, funding, and initial investment in the recommended model.

The workflow is iterative, not strictly linear. Prospects may request multiple revisions, ask for comparisons between different models, or bring additional assets into scope after the initial proposal. The proposal system must support version tracking and efficient regeneration.

### Risk Profiling and Model Mapping
Risk profiling is the foundation of the proposal recommendation. The risk questionnaire produces a quantitative score that determines which model portfolio is appropriate for the prospect.

**Risk questionnaire design:**
- Questionnaires typically contain 10-25 questions assessing both willingness (behavioral/emotional tolerance for loss) and capacity (financial ability to absorb losses without jeopardizing goals).
- Common question formats include: scenario-based loss tolerance ("If your portfolio lost 20% in a month, would you sell, hold, or buy more?"), time horizon assessment, income stability evaluation, and investment experience self-assessment.
- Scoring produces a numerical result (e.g., 1-100) or a categorical classification (Conservative, Moderately Conservative, Moderate, Moderately Aggressive, Aggressive).
- Third-party risk profiling tools (Riskalyze/Nitrogen, Tolerisk, FinaMetrica) provide validated, statistically tested questionnaires with defensible scoring methodologies. These are preferred over home-built questionnaires because they have undergone psychometric validation and are widely accepted by regulators.

**Model portfolio lineup design:**
A typical advisory firm maintains 5-10 model portfolios spanning the risk-return spectrum:

| Risk Score Range | Model Name | Equity/Fixed Income | Expected Return Range | Expected Max Drawdown |
|-----------------|------------|--------------------|-----------------------|----------------------|
| 1-20 | Conservative Income | 20/80 | 3-5% | -8 to -12% |
| 21-35 | Moderate Conservative | 35/65 | 4-6% | -12 to -18% |
| 36-50 | Moderate | 50/50 | 5-7% | -18 to -25% |
| 51-65 | Moderate Growth | 65/35 | 6-8% | -25 to -32% |
| 66-80 | Growth | 80/20 | 7-9% | -32 to -40% |
| 81-100 | Aggressive Growth | 95/5 | 8-11% | -40 to -50% |

Each model is defined by a strategic asset allocation with target weights and permissible ranges for each asset class, along with specific fund or ETF selections that implement the allocation. Models should be reviewed and rebalanced on a defined schedule (typically quarterly or semi-annually).

**Suitability alignment:**
The risk profile alone does not determine the recommendation. The advisor must also consider:
- **Time horizon** — a young investor with a long horizon may be profiled as moderate but could reasonably be placed in a growth model, while a retiree with the same risk score needs more conservative positioning due to sequence-of-returns risk.
- **Income needs** — a prospect requiring portfolio income may need a model tilted toward income-producing assets, regardless of risk score.
- **Tax sensitivity** — a taxable account may warrant a tax-managed version of the model (municipal bonds, tax-loss harvesting overlay, low-turnover equity strategies).
- **Concentrated positions** — a prospect with a large single-stock position may need a transition strategy rather than an immediate full model assignment.
- **ESG preferences** — if the prospect has environmental, social, or governance preferences, the firm may offer ESG-screened variants of its standard models.

**Documenting the recommendation rationale:**
The proposal must articulate why this specific model is appropriate for this prospect. The rationale should reference the risk profile score, the model's risk-return characteristics, and how the recommendation aligns with the prospect's stated objectives, time horizon, and constraints. This documentation serves both as a client communication tool and as a suitability record for compliance purposes.

### Proposal Document Components
A complete investment proposal typically includes the following sections:

**Executive summary** — a one-page overview of the recommendation: who the client is, what is being recommended, why it is appropriate, and the expected outcome. The executive summary is often the only page some decision-makers read in detail; it must be clear and compelling.

**Client profile recap** — a summary of the prospect's financial situation as understood by the advisor: personal information, financial goals, time horizon, risk profile score and interpretation, income and expense summary, tax situation, and any special circumstances. This section demonstrates that the advisor listened during discovery and correctly understands the prospect's needs.

**Current portfolio analysis (if applicable)** — for prospects with existing investments, this section provides:
- Holdings list with current market values
- Asset allocation breakdown (pie chart and table) compared to the recommended allocation
- Risk metrics: portfolio standard deviation, beta, Sharpe ratio, maximum drawdown estimate
- Expense analysis: weighted average expense ratio, total annual cost in dollars
- Concentrated position identification: any single holding exceeding 5-10% of the portfolio
- Style analysis: Morningstar style box mapping, factor exposures
- Income analysis: current yield, income projection
- Tax lot summary: unrealized gains and losses, short-term vs long-term, estimated tax impact of liquidation

**Recommended portfolio** — the core of the proposal:
- Asset allocation targets with visual representation (pie chart, bar chart)
- Holdings list: each fund or ETF, its asset class role, expense ratio, target weight, and dollar amount
- Risk-return profile of the recommended portfolio: expected return, standard deviation, Sharpe ratio, maximum drawdown estimate
- Comparison table: current portfolio vs recommended portfolio on key metrics
- Income projection: expected yield and annual income from the recommended portfolio

**Fee schedule** — a complete disclosure of all costs the client will bear (see Fee Illustration section below).

**Historical performance context** — how the recommended model or a similar allocation has performed historically. This section requires careful attention to compliance (see Performance Projections and Disclaimers section below). Common presentations include:
- Historical returns of the model portfolio (if a track record exists) or a blended benchmark representing the target allocation
- Calendar-year returns showing both up and down years
- Growth of $1 million chart over a trailing period (e.g., 10 or 20 years)
- Performance during specific market events (2008-2009 crisis, 2020 COVID drawdown, 2022 rate shock)

**Scenario projections** — forward-looking analysis showing potential outcomes:
- Monte Carlo simulation results: probability of meeting the client's goal, median outcome, 10th percentile (bad case), 90th percentile (good case)
- Straight-line projections at expected return (with explicit disclaimer that this is illustrative only)
- Stress test scenarios: how the portfolio would perform in a repeat of historical crises

**Disclaimers and disclosures** — required legal language (see Compliance Review section below).

**Next steps** — a clear call to action: sign the advisory agreement, fund the account, and begin investing. Include a timeline for implementation.

### Fee Illustration
The fee illustration section of the proposal must present costs clearly, completely, and in compliance with fee disclosure requirements. Prospects make decisions based on fees; incomplete or misleading fee disclosure undermines trust and creates regulatory risk.

**Advisory fee presentation:**
- Present the firm's fee schedule with all tiers and breakpoints. For a tiered schedule, show both the marginal rate at each tier and the blended (effective) rate for the prospect's specific asset level.
- Example tiered fee schedule illustration for a $2M portfolio:

| Tier | Rate | Assets in Tier | Fee for Tier |
|------|------|---------------|-------------|
| First $500K | 1.00% | $500,000 | $5,000 |
| Next $500K | 0.85% | $500,000 | $4,250 |
| Next $1M | 0.75% | $1,000,000 | $7,500 |
| **Total** | **Blended: 0.8375%** | **$2,000,000** | **$16,750/year** |

- Show the fee in both percentage and dollar terms. Dollar amounts are more tangible to prospects and required under Reg BI.
- Specify billing frequency (quarterly in advance or arrears) and the per-quarter dollar amount.

**Fund-level expense disclosure (fee-on-fee):**
- Disclose the weighted average expense ratio of the funds in the recommended portfolio.
- Show the total annual cost combining advisory fees and fund expenses.
- Example: Advisory fee 0.84% + weighted average fund expense ratio 0.12% = total annual cost 0.96%, or $19,200 on a $2M portfolio.
- For proposals recommending funds-of-funds or wrap programs with underlying fund costs, the layered fee structure must be made transparent.

**Total cost of ownership:**
- Beyond advisory fees and fund expenses, disclose any other costs: custodian fees, transaction costs (if applicable), account maintenance fees, wire fees, and any other charges.
- Present a single "all-in" annual cost figure and percentage so the prospect can compare to alternatives.

**Breakpoint analysis:**
- If the prospect's assets are near a fee tier breakpoint, show the impact of consolidating additional assets to reach the next lower rate.
- Example: "At your current $475,000, your blended rate is 1.00%. By consolidating an additional $25,000, your blended rate drops to 0.985%, saving approximately $75 per year. At $1,000,000, your blended rate is 0.925%."

**Fee comparison vs alternatives:**
- Prospects often compare advisory fees to robo-advisors, self-directed brokerage, or other advisory firms. The proposal may include a comparison showing the additional services provided for the advisory fee (financial planning, tax management, behavioral coaching, rebalancing).
- Be factual and avoid disparaging competitors. Focus on value delivered rather than competitor shortcomings.

**Reg BI cost disclosure requirements:**
- For broker-dealers making recommendations, Reg BI requires that the cost disclosure be specific to the recommendation, not generic. The prospect must be able to understand the total cost of the specific securities and account type being recommended.
- The Disclosure Obligation under Reg BI requires written disclosure of all material fees and costs, including indirect compensation (12b-1 fees, revenue sharing).

### Performance Projections and Disclaimers
Performance presentation in proposals is one of the most compliance-sensitive areas of the advisory business. The SEC Marketing Rule (Rule 206(4)-1 under the Advisers Act, effective November 2022) substantially governs how investment advisers present performance.

**Is a proposal "advertising"?**
Under the Marketing Rule, "advertisement" includes any communication to more than one person (or designed for such use) that offers or promotes advisory services. A one-on-one proposal to a specific prospect is generally not an advertisement if it is truly tailored to that individual. However, if the firm uses a standardized proposal template that is distributed broadly with only minor customization, regulators may view it as advertising. Best practice: treat all performance presentations in proposals as if the Marketing Rule applies, even for one-on-one presentations.

**Historical performance presentation:**
- If presenting actual model portfolio track records, the Marketing Rule requires: gross and net-of-fee performance shown with equal prominence, a disclosure of whether the performance reflects actual client accounts or a model/hypothetical, the time period covered, and material conditions or assumptions.
- If presenting index or benchmark returns as a proxy for the recommended allocation, clearly label them as benchmark returns, not the firm's performance. Disclose that the benchmark is not directly investable and does not reflect fees, trading costs, or taxes.

**Hypothetical performance:**
- The Marketing Rule permits hypothetical performance (including backtested model portfolios) in one-on-one presentations, provided the adviser adopts policies and procedures reasonably designed to ensure the performance is relevant to the recipient's financial situation and investment objectives, and the adviser provides sufficient information for the recipient to understand the assumptions and limitations.
- Required disclosures for hypothetical performance: the results do not represent actual trading, the results were achieved by retroactive application of a model, actual results may differ materially, and the specific methodology and assumptions used.
- Backtested performance must disclose the material assumptions (rebalancing frequency, dividend reinvestment, fund selection dates, any survivorship bias corrections).

**Monte Carlo projections:**
- Monte Carlo simulations generate a distribution of potential outcomes by running thousands of randomized return scenarios based on the portfolio's expected return, standard deviation, and correlation assumptions.
- Key outputs: probability of achieving the client's goal (e.g., "85% probability of maintaining your income through age 95"), median projected portfolio value at target date, range of outcomes (10th to 90th percentile fan chart).
- Required disclosures: Monte Carlo simulations are hypothetical, based on assumptions that may not reflect future market conditions, do not guarantee results, and are sensitive to the input assumptions (small changes in expected return or volatility can significantly alter the output).
- Do not present Monte Carlo results as predictions. Use language like "based on the assumptions described, the analysis suggests..." rather than "your portfolio will grow to..."

**Expected return ranges:**
- When presenting expected returns for a recommended portfolio, always present a range rather than a single point estimate. A single expected return figure implies false precision.
- Disclose the methodology: are expected returns based on capital market assumptions from a third-party provider (e.g., BlackRock, J.P. Morgan, Vanguard), the firm's internal research, or historical averages? Each approach has limitations that must be acknowledged.

**Required disclaimers (at minimum):**
- "Past performance is not indicative of future results."
- "Investing involves risk, including the potential loss of principal."
- "Hypothetical performance results have many inherent limitations. No representation is being made that any account will or is likely to achieve profits or losses similar to those shown."
- "The projections or other information regarding the likelihood of various investment outcomes are hypothetical in nature, do not reflect actual investment results, and are not guarantees of future results."
- For tax-related projections: "This analysis is not tax advice. Consult a qualified tax professional regarding your specific situation."

### Current Portfolio Analysis
When a prospect has an existing portfolio at another firm, the current portfolio analysis is one of the most persuasive sections of the proposal. It quantifies the specific improvements the prospect will experience by moving to the recommended portfolio.

**Holdings review:**
- Import the prospect's current holdings from account statements, a CSV export, or an account aggregation tool (ByAllAccounts, Quovo/Plaid, Yodlee).
- Classify each holding by asset class, sub-asset class, and style to build a complete picture of the current allocation.
- Identify any holdings that are not transferable in-kind (proprietary funds, annuities with surrender charges, illiquid alternatives).

**Risk assessment:**
- Calculate the current portfolio's risk metrics: annualized standard deviation, beta relative to a blended benchmark, maximum drawdown over the historical period, Value at Risk (VaR) at 95% confidence.
- Compare these metrics side-by-side with the recommended portfolio. If the current portfolio has higher risk for the same or lower expected return, this is a compelling argument for transition.
- Use risk visualization tools (Riskalyze/Nitrogen Risk Number, Morningstar risk/return scatterplot) to make the comparison accessible to non-technical prospects.

**Tax lot analysis:**
- For taxable accounts, identify unrealized gains and losses by holding and by tax lot.
- Classify gains and losses as short-term or long-term, as the tax impact differs substantially (short-term gains taxed as ordinary income vs long-term gains at preferential capital gains rates).
- Calculate the estimated tax cost of full liquidation vs a phased transition.
- Identify holdings with large embedded gains that may be candidates for retention or gradual disposition.

**Transition cost estimation:**
- The transition from current portfolio to recommended portfolio involves costs: capital gains taxes (for taxable accounts), transaction costs (commissions or spreads), and potential market impact for large or illiquid positions.
- Present a transition cost analysis: estimated tax liability, estimated transaction costs, and the net benefit of transitioning (reduced ongoing fees, improved risk-adjusted returns, better diversification) vs the one-time transition cost.
- For large embedded gains, propose a phased transition plan: sell short-term lots and loss positions immediately, transition long-term gain positions over 12-24 months, retain specific holdings that fit within the recommended allocation.

**Concentrated position identification:**
- Flag any single security representing more than 5% of the portfolio (or a lower threshold per firm policy).
- For each concentrated position, disclose the specific risk: single-stock risk (company-specific, sector-specific), lack of diversification, potential regulatory or insider trading restrictions.
- Propose strategies for managing the concentration: direct sale (with tax analysis), exchange funds, charitable remainder trusts, protective put options, systematic diversification over time.

**Improvement quantification:**
The proposal should clearly quantify the improvements the prospect will experience:
- Fee savings: current total cost vs proposed total cost, in dollars per year
- Risk reduction: current portfolio risk metrics vs proposed, expressed in terms the prospect understands ("Your current portfolio could lose up to $X in a severe downturn; the proposed portfolio limits that to approximately $Y")
- Diversification improvement: number of holdings, asset class coverage, geographic diversification, sector concentration reduction
- Income improvement: current yield vs proposed yield, annual income difference

### Compliance Review of Proposals
Every proposal must undergo compliance review before presentation to the prospect. The review ensures suitability documentation, performance presentation, fee disclosure, and disclaimers meet regulatory requirements.

**Supervisory review requirements:**
- FINRA Rule 3110 (broker-dealers) and SEC guidance for RIAs require supervisory review of communications with the public. While a one-on-one proposal may not technically be "correspondence" or "advertising" under FINRA's definitions, most firm compliance manuals require supervisory sign-off on proposals, particularly those containing performance data or projections.
- The supervisor's review should verify: (1) the recommendation is suitable given the documented client profile, (2) performance data is presented in compliance with the Marketing Rule or FINRA advertising rules, (3) fee disclosure is complete and accurate, (4) all required disclaimers are present, and (5) any claims about the firm or its services are substantiated.

**Advertising rule applicability:**
- Under the SEC Marketing Rule, a one-on-one proposal to a specific prospect is generally not an advertisement. However, the proposal becomes advertising if it is used with more than one person or is designed for broad distribution. Template proposals with standardized performance and marketing language should be treated as advertisements.
- FINRA Rule 2210 classifies communications as institutional, retail, or correspondence. A proposal to a retail prospect is typically retail communication, requiring principal pre-approval if it makes performance claims or recommendations.

**Performance presentation rules:**
- If the proposal includes actual performance of the firm's models or composites, the Marketing Rule requires gross and net performance with equal prominence, the period covered, and material assumptions.
- If the proposal includes hypothetical or backtested performance, it must include disclosures about the limitations of hypothetical results and the methodology used.
- GIPS-compliant firms must present performance consistent with GIPS standards if they claim GIPS compliance; mixing GIPS and non-GIPS presentations creates confusion and potential violations.

**Fee disclosure adequacy:**
- Verify that the fee illustration includes all layers of cost: advisory fees, fund expenses, transaction costs, custodian fees, and any other charges.
- Confirm that fee tier calculations are accurate for the prospect's specific asset level.
- Ensure that any fee comparison to alternatives is fair and not misleading.

**Suitability documentation:**
- The compliance reviewer should verify that the prospect's risk profile, investment objectives, time horizon, and financial situation are documented and that the recommendation is consistent with this profile.
- If the recommendation deviates from the standard model mapping (e.g., the risk score maps to Moderate but the advisor recommends Moderate Growth), the rationale for the deviation must be documented and approved.

### Proposal Technology and Automation
Modern proposal generation relies on technology platforms that integrate data, automate document assembly, and streamline the workflow from discovery to delivery.

**Major proposal generation platforms:**

- **Orion Portfolio Solutions** — provides proposal generation integrated with its portfolio management and reporting platform. Features include model portfolio comparison, fee illustration, risk analysis, and automated document assembly. Strong integration with Orion's trading and reporting ecosystem.
- **Black Diamond (SS&C Advent)** — offers proposal tools as part of its wealth platform, including prospect pipeline tracking, proposal document generation, performance comparison, and integration with its reporting and billing systems.
- **Riskalyze/Nitrogen** — specializes in risk profiling and risk-aligned proposals. The Risk Number system provides an intuitive way to show prospects their current portfolio risk vs the proposed portfolio risk. Proposals include the "95% Historical Range" visualization that resonates with prospects. Nitrogen has expanded from risk assessment into a broader proposal and financial planning workflow.
- **MoneyGuidePro (Envestnet)** — primarily a financial planning tool, but its proposal capabilities include goal-based projections, Monte Carlo analysis, and integration with Envestnet's managed account platform. Proposals frame the investment recommendation within the context of the client's overall financial plan.
- **RightCapital** — financial planning platform with proposal generation that includes tax-aware projections, estate planning visualizations, and a modern client-facing interface. Strong with younger advisory firms and RIAs focused on comprehensive planning.
- **Hidden Levers** — stress testing and scenario analysis platform that generates proposal-ready reports showing how current and proposed portfolios would perform under various economic scenarios.
- **Advyzon** — all-in-one platform combining CRM, portfolio management, reporting, billing, and client portal with proposal generation capabilities.

**Template management:**
- Firms should maintain a library of approved proposal templates covering common scenarios: new prospect with no current portfolio, prospect with existing brokerage account, prospect with employer retirement plan rollover, institutional prospect, and trust/entity prospect.
- Templates should be version-controlled and require compliance approval before deployment. When performance data or model portfolio holdings change, all affected templates must be updated.
- Template customization should be limited to client-specific data fields; the narrative sections, disclaimers, and compliance language should be locked to prevent advisors from inadvertently making non-compliant modifications.

**Data integration:**
- Proposal systems should pull data from multiple sources: CRM (prospect information), risk profiling tool (risk score), portfolio management system (model portfolio details), market data provider (current prices, historical returns), and custodian (existing account data for current portfolio analysis).
- Account aggregation tools (Plaid, Yodlee, ByAllAccounts) can import the prospect's held-away account data for current portfolio analysis, eliminating manual data entry from account statements.

**Digital delivery:**
- Proposals should be deliverable digitally through a secure client portal or encrypted email, in addition to printed copies for in-person presentations.
- Interactive digital proposals allow the prospect to explore different scenarios, adjust assumptions, and compare models — increasing engagement and reducing the number of revision cycles.
- Digital delivery creates an audit trail: when the prospect received the proposal, how long they viewed it, and which sections they engaged with. This data helps advisors prepare for the presentation meeting.

**E-signature for advisory agreements:**
- When the prospect accepts the proposal, the advisory agreement (Investment Management Agreement or similar) should be available for immediate electronic signature within the proposal platform or via integration with an e-signature provider (DocuSign, Adobe Sign).
- The signed advisory agreement triggers the onboarding workflow: account opening, funding, and initial investment in the recommended model.
- Capturing acceptance digitally reduces the time between proposal acceptance and first investment, which is critical because prospect commitment can wane with delay.

## Worked Examples

### Example 1: Generating a proposal for a new prospect with a $2M rollover from a 401(k)
**Scenario:** A 58-year-old prospect recently left her employer and has $2M in a 401(k) plan invested in a mix of target-date funds and company stock. She is considering rolling the assets to an IRA managed by an advisory firm. She has no other significant investable assets outside her home. She plans to retire at 63 and needs the portfolio to generate $80,000/year (in today's dollars) in retirement income starting at age 63. She completed the firm's risk questionnaire and scored 42 out of 100 (Moderate).

**Design Considerations:**
- The rollover is from a 401(k) to a Traditional IRA, which is a tax-free direct rollover if handled properly. The proposal should explicitly note that this is a direct (trustee-to-trustee) rollover, not a distribution, to avoid a taxable event.
- The 5-year time horizon to retirement combined with a Moderate risk score suggests a portfolio in the Moderate to Moderate Conservative range. While the risk score maps to Moderate (50/50 equity/fixed income), the relatively short time horizon and high dependence on this single portfolio for retirement income argue for a more conservative positioning. The advisor should consider recommending the Moderate Conservative model (35/65) or a custom blend, and document the rationale for any deviation from the standard risk mapping.
- Retirement income analysis: $80,000/year starting at 63, adjusted for 2.5% inflation, funded by a $2M portfolio over a 30+ year retirement (to age 95). The proposal should include Monte Carlo analysis showing the probability of sustaining this income. At a 4% initial withdrawal rate ($80,000/$2,000,000), the prospect is at the widely cited sustainable withdrawal threshold — the analysis should show the sensitivity of success probability to different return scenarios.
- The current 401(k) holdings include company stock, which may have Net Unrealized Appreciation (NUA) tax benefits. The proposal should address whether the NUA strategy is advantageous: if the cost basis of the company stock is low, distributing the shares in-kind to a taxable account (not rolling them to the IRA) allows the NUA to be taxed at long-term capital gains rates rather than ordinary income rates upon distribution from the IRA. This requires careful tax analysis and should be presented as a consideration, not as tax advice.
- Fee illustration: show the firm's tiered fee schedule applied to $2M, the weighted average expense ratio of the recommended funds, and the total cost. Compare this to the prospect's current 401(k) plan expenses (typically 0.50-1.50% all-in for employer plans, depending on plan size and investment options).

**Analysis:** The proposal document should include: (1) Executive summary framing the recommendation as a retirement transition strategy, not just a portfolio change. (2) Client profile recap emphasizing the 5-year accumulation phase followed by a 30+ year distribution phase. (3) Current portfolio analysis showing the 401(k) allocation — likely over-concentrated in company stock and potentially misallocated in the target-date fund (which may be targeting a different retirement date or risk level than appropriate). Quantify the single-stock concentration risk. (4) Recommended portfolio: Moderate Conservative model with 35% equity, 55% investment-grade fixed income, and 10% alternatives/real assets for inflation protection. Include a holdings detail table with specific funds, expense ratios, and target weights. (5) Retirement income projection using Monte Carlo showing 85-90% probability of sustaining $80,000/year (inflation-adjusted) through age 95 — if the probability is lower, discuss options (delaying retirement, reducing spending, part-time work). (6) Fee illustration showing the blended advisory fee of 0.8375% on $2M ($16,750/year) plus fund expenses of approximately 0.12% ($2,400/year) for a total of $19,150/year, compared to the estimated 401(k) plan cost. (7) NUA analysis as a supplementary section, clearly labeled as requiring tax professional review. (8) Transition plan: direct rollover of all non-company-stock assets; separate analysis for company stock disposition. (9) All required disclaimers regarding projections, past performance, and tax information.

### Example 2: Creating a proposal that compares current broker-dealer portfolio vs proposed advisory portfolio
**Scenario:** A prospect with $1.5M at a full-service broker-dealer is unhappy with performance and fees. The current portfolio consists of 18 individual stocks, 6 actively managed mutual funds (A-shares with front loads previously paid), and a fixed annuity. The prospect is 52 years old, risk score 65 (Moderate Growth), retired military with a pension covering basic expenses, and views the investment portfolio as growth capital with a 20+ year horizon. The advisor wants to demonstrate the advantages of the proposed advisory model vs the current BD portfolio.

**Design Considerations:**
- The current portfolio analysis is the most important section of this proposal. The prospect is motivated by dissatisfaction, so the analysis must honestly and accurately quantify the issues with the current portfolio while complying with rules against misleading comparisons.
- Current portfolio issues to analyze: (a) 18 individual stocks likely create concentration risk — measure diversification vs the recommended model; (b) actively managed A-share mutual funds have higher expense ratios (often 0.75-1.25%) than the ETFs or institutional share class funds in the proposed model (often 0.05-0.25%); (c) the prospect may be paying ongoing 12b-1 fees (0.25%) within the A-shares; (d) the fixed annuity may have surrender charges if liquidated before the surrender period expires — this is a critical transition cost to disclose; (e) calculate the total current cost: any ongoing BD advisory or account fees + fund expense ratios + 12b-1 fees.
- The comparison must be fair and not misleading. Do not compare the BD portfolio's worst year to the advisory portfolio's best year. Compare on risk-adjusted metrics (Sharpe ratio, Sortino ratio) over the same time periods. If comparing performance, ensure the comparison uses consistent time periods and accounts for survivorship bias in the current holdings.
- The fixed annuity requires careful handling: if it has a remaining surrender period, disclose the surrender charge and analyze whether the benefit of transition outweighs the surrender cost. If the annuity has favorable guaranteed rates, it may be appropriate to retain it.
- Transition tax analysis: the 18 individual stocks and mutual funds in a taxable account have embedded gains and losses. The proposal must include a tax lot analysis showing the estimated tax cost of liquidation. A phased transition may be more tax-efficient than an immediate full liquidation.

**Analysis:** The proposal should present a structured comparison: (1) Side-by-side asset allocation: current portfolio (likely equity-heavy given 18 stocks plus equity funds, possibly 85-90% equity) vs recommended Moderate Growth model (65/35). The current portfolio may actually carry more risk than the prospect's score supports — this is a powerful finding. (2) Cost comparison: Current all-in cost (estimate BD advisory fee at 1.0-1.5% + fund expenses at 0.90% average + 12b-1 fees at 0.25% on applicable funds) vs proposed (advisory fee of approximately 0.90% blended on $1.5M + fund expenses at 0.12%) — expected annual savings of $8,000-15,000 depending on current BD fee structure. Present this as a 10-year and 20-year cumulative savings. (3) Risk comparison: current portfolio standard deviation and max drawdown estimate vs recommended model. If the current portfolio is carrying 85-90% equity risk, the max drawdown in a 2008-type event would have been approximately -45 to -50%, vs -32% for the recommended model. (4) Diversification comparison: current 18-stock portfolio may have 40-50% in 3-4 sectors vs broad market diversification in the recommended model. (5) Transition plan: retain the fixed annuity if surrender charges apply, harvest tax losses in current holdings to offset gains, transition individual stocks with large embedded gains over 12-18 months, immediately transition mutual fund positions (A-share loads are sunk costs and should not factor into the decision to stay or leave). (6) Disclaimers: the comparison uses historical data and assumptions; actual future performance of either portfolio cannot be predicted; the comparison does not account for all factors that may affect performance; the prospect should consider the tax implications with a qualified professional.

### Example 3: Building a proposal template system for a multi-advisor firm with standardized models
**Scenario:** A growing RIA with 25 advisors and $4B AUM is transitioning from an ad-hoc proposal process (each advisor creates their own proposals using PowerPoint and Excel) to a standardized, automated proposal generation system. The firm has 7 model portfolios, a uniform fee schedule, and uses Schwab as its custodian, Orion for portfolio management, and Salesforce for CRM. The chief compliance officer wants every proposal to pass through a compliance workflow before delivery.

**Design Considerations:**
- The primary challenge is balancing standardization (for compliance, efficiency, and brand consistency) with advisor flexibility (each advisor has their own style, client base, and value proposition). The system should lock compliance-critical elements (disclaimers, performance presentation, fee disclosure) while allowing advisors to customize narrative sections (personal letter, firm value proposition, service description).
- Template architecture should include: (a) a master template with locked compliance sections, (b) modular components that advisors can include or exclude (current portfolio analysis module, retirement income module, tax transition module, estate planning integration module), (c) advisor-specific elements (advisor bio, contact information, personal branding within firm guidelines), and (d) model-specific content (each of the 7 models has a pre-written description, historical context, and risk-return profile).
- Data integration requirements: Salesforce provides prospect data (name, contact, financial information collected during discovery); the risk profiling tool provides the risk score and model mapping; Orion provides model portfolio details (holdings, allocation, historical performance); Schwab provides account data for current portfolio analysis (via account aggregation or statement import); the proposal system assembles all data into the selected template.
- Compliance workflow: after the advisor generates a proposal, it enters a compliance review queue. The compliance reviewer checks suitability alignment, performance data accuracy, fee calculation correctness, and disclaimer completeness. The system should flag proposals that deviate from standard model mappings or contain customized language that has not been pre-approved. Approved proposals are released for delivery; rejected proposals return to the advisor with specific correction requirements.
- Version control: when model portfolios are updated (quarterly rebalance, fund substitution), all templates must be refreshed. Proposals generated before the update should be flagged if they are still pending delivery, as they contain stale data. The system should prevent delivery of proposals with outdated model information.

**Analysis:** The recommended implementation plan: (1) Phase 1 — Template design (weeks 1-4): Work with the compliance team to define the locked compliance sections: disclaimers, performance presentation format, fee disclosure format, and required disclosures. Create the 7 model-specific content blocks with CCO approval. Design the modular components. Build the master template in the proposal platform with content controls that prevent unauthorized editing of locked sections. (2) Phase 2 — Integration (weeks 3-8): Connect Salesforce (prospect data), the risk profiling tool (risk score and model mapping), and Orion (model details and current portfolio data) to the proposal platform via API. Implement the compliance review workflow with status tracking, reviewer assignment, and approval/rejection routing. (3) Phase 3 — Pilot (weeks 8-10): Deploy to 3-5 advisors for testing. Gather feedback on usability, template quality, data accuracy, and compliance workflow efficiency. Identify edge cases that the templates do not handle well (complex trusts, institutional prospects, prospects with annuities). (4) Phase 4 — Rollout (weeks 10-14): Train all 25 advisors. Provide proposal generation guides and best practices. Establish metrics: proposals generated per advisor per month, compliance review turnaround time, revision rate (percentage of proposals requiring revisions), and time from proposal generation to client acceptance. (5) Ongoing governance: Quarterly template review aligned with model portfolio rebalancing. Annual compliance review of all template content. Advisor feedback loop for template improvements. Dashboard monitoring proposal pipeline, compliance review backlog, and conversion rates. The expected outcome is a reduction in proposal generation time from 3-5 hours (ad-hoc PowerPoint/Excel) to 30-60 minutes (templated, data-integrated), a near-elimination of compliance errors in delivered proposals, and consistent brand and message quality across all 25 advisors.

## Common Pitfalls
- Presenting hypothetical or backtested performance without the required disclosures about limitations, methodology, and the fact that results do not represent actual trading
- Showing only gross-of-fee performance without equal-prominence net-of-fee returns, violating the SEC Marketing Rule
- Using Monte Carlo projections without disclosing the input assumptions (expected return, standard deviation, correlation matrix) or the limitations of the simulation
- Mapping risk scores to models mechanically without considering time horizon, income needs, and other suitability factors that may warrant a different recommendation
- Omitting fund-level expenses from the fee illustration, presenting only the advisory fee as the total cost
- Failing to disclose surrender charges, tax consequences, or other transition costs when recommending a move from an existing portfolio
- Generating proposals with stale model portfolio data (holdings or allocations that have changed since the last rebalance)
- Allowing advisors to customize disclaimer language or remove required disclosures from proposal templates
- Presenting a current portfolio analysis that cherry-picks unfavorable metrics to make the current portfolio look worse than it is — comparisons must be fair and balanced
- Not documenting the rationale for recommending a model that deviates from the standard risk profile mapping
- Treating the proposal as a one-time document rather than versioning it — when assumptions change or the prospect requests modifications, the firm must track which version was presented and accepted
- Neglecting to address the prospect's existing concentrated positions, restricted stock, or illiquid holdings in the transition plan
- Using projected returns without clearly labeling them as hypothetical and subject to the Marketing Rule's requirements for hypothetical performance

## Cross-References
- **asset-allocation** (Layer 5): Strategic and tactical asset allocation frameworks that underpin model portfolio construction and the recommended allocation in proposals
- **investment-policy** (Layer 5): IPS construction defines the policy framework that the proposal recommendation must satisfy; the proposal is often the precursor to a formal IPS
- **performance-reporting** (Layer 7): Ongoing performance reporting follows the same presentation standards established in the proposal; consistency between proposal projections and actual reporting builds credibility
- **performance-metrics** (Layer 7): Risk-return metrics (Sharpe ratio, standard deviation, max drawdown) used in proposals to compare current vs recommended portfolios
- **fee-disclosure** (Layer 9): Regulatory requirements for fee presentation that the proposal's fee illustration section must satisfy
- **reg-bi** (Layer 9): Regulation Best Interest's Care and Disclosure Obligations govern how broker-dealers present recommendations and costs in proposals
- **client-disclosures** (Layer 9): Form ADV, Form CRS, and other required disclosures that must accompany or be delivered alongside the proposal
- **investment-suitability** (Layer 9): Suitability standards that the proposal recommendation must satisfy; the risk profile and model mapping must align with documented suitability requirements
- **advertising-compliance** (Layer 9): SEC Marketing Rule and FINRA advertising rules that govern performance presentation, testimonials, and promotional claims in proposals
- **financial-planning-integration** (Layer 10): Proposals increasingly embed financial planning elements (retirement projections, goal funding analysis); the planning integration skill covers how to connect proposals to comprehensive financial plans
- **quantitative-valuation** (Layer 4): Valuation frameworks relevant when proposals include analysis of individual securities in the prospect's current portfolio
- **diversification** (Layer 5): Diversification principles used to evaluate current portfolio concentration and demonstrate the improvement offered by the recommended model
