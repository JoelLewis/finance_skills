---
name: financial-planning-integration
description: "Integrate financial planning engines with the advisor technology stack — data flows between planning tools, CRM, PMS, custodians, and aggregation platforms; capital market assumption (CMA) governance and synchronization; plan-to-IPS-to-model linkage; and governed tax reference parameters in planning tools. Use when the user asks about connecting eMoney, MoneyGuidePro, or RightCapital to CRM or portfolio systems, eliminating manual re-entry between systems, keeping plan and portfolio assumptions consistent, mapping plan outputs (required return, risk capacity, withdrawal schedule) into the IPS and model assignment, or establishing plan update cadence and data-freshness rules. Also trigger on 'plan-to-IPS linkage', 'assumption synchronization', 'CMA governance', or 'planning tool integration'. For planning methodology itself — Monte Carlo modeling, Roth conversion strategy, Social Security claiming, retirement projections — use financial-planning-workflow instead."
---

# Financial Planning Integration

## Core Concepts

### Financial Planning System Architecture
The financial planning engine is the analytical hub of the advisor technology stack. It ingests client data from multiple systems, models the client's financial future, and produces outputs that drive portfolio construction, cash management, and ongoing advisory recommendations. (For the planning methodology those engines implement, see financial-planning-workflow.)

**Relationship to other systems in the advisor technology stack:**
- **CRM (client relationship management):** Source of client demographic data, household composition, employment status, life events, and planning review triggers. The CRM is the system of record for client facts; the planning tool consumes these facts as inputs.
- **PMS (portfolio management system):** Source of current portfolio holdings, asset allocation, and account types. The plan produces a required return target and risk capacity that feed back to the PMS as constraints for portfolio construction.
- **Custodian:** Source of account balances, positions, and transaction history. Custodial data feeds ensure the plan reflects actual account values rather than stale estimates.
- **Aggregation platform:** Source of held-away assets — accounts at other custodians, employer retirement plans, bank accounts, real estate equity estimates, stock options. Aggregation fills the gap between what the advisor custodies and what the client actually owns, which is essential for a complete financial picture.

**Common financial planning platforms (as of 2026; verify current vendor lineups):** eMoney Advisor, MoneyGuidePro (Envestnet), RightCapital, Naviplan (InvestCloud), and planning modules embedded within all-in-one platforms (e.g., Orion Planning, Advyzon). Platform selection depends on firm size, integration requirements, planning complexity, and client-facing presentation needs. Some platforms emphasize interactive client portals (eMoney, RightCapital); others emphasize advisor-facing analytical depth (MoneyGuidePro, Naviplan).

### Goal Data Model and Status Tracking
Goals are the structured records that flow between the planning tool, CRM, and client portal. Each goal carries a defined set of attributes that downstream systems consume:

- **Target amount:** The dollar amount needed, in today's or future dollars
- **Target date:** When the funds are needed (single date or range for ongoing goals like retirement income)
- **Priority:** Essential, important, or aspirational
- **Funding source:** Which accounts and income streams fund the goal — this account linkage is what connects the plan to the PMS
- **Inflation assumption:** The category-specific inflation rate applied (general CPI, education, healthcare)

Each goal carries a status derived from its current probability of success, and status updates flow out to the CRM and client portal:

- **On track:** Probability at or above the target threshold (commonly 80-90%)
- **Needs attention:** 60-80%, where modest adjustments could restore on-track status
- **At risk:** 40-60%, requiring significant plan changes
- **Unlikely:** Below 40%, where the goal may need restructuring or deprioritization

These status indicators must update dynamically as portfolio feeds refresh plan inputs. How to set goals, prioritize among them, and model trade-offs is methodology — see financial-planning-workflow.

### Capital Market Assumptions as Governed Inputs
The expected return, volatility, and correlation assumptions behind plan projections are the most consequential — and most frequently desynchronized — data elements in the planning stack.

- Small changes are high-leverage: reducing an expected equity return from 8% to 7% can shift a plan's probability of success by 10-15 percentage points. A single probability number presented without assumption context creates false precision.
- The firm should maintain a single authoritative capital market assumptions (CMA) document — owned by the investment committee, reviewed on a defined cadence (quarterly or annually) — that every system (planning tool, PMS, proposal engine) references. Assumptions set independently in each system will drift apart.
- When CMAs change, all systems must update simultaneously and all client plans should be re-run, with material probability changes flagged for advisor review.
- Distribution choices (normal vs. log-normal, historical bootstrapping, regime-switching) are also assumptions that should be documented in the CMA governance record, since different planning tools default to different methods.

Monte Carlo mechanics and how to interpret probability-of-success results are covered in financial-planning-workflow.

### Tax Reference Parameters as Governed Inputs
Planning-tool tax projections depend on annually updated reference data: federal and state bracket thresholds, standard deduction amounts, IRMAA (Medicare income-related monthly adjustment amount) thresholds, contribution limits, and RMD ages. These parameters are data-governance concerns, not just planning inputs:

- Most planning vendors push annual tax-table updates, but firms must verify the update landed before running year-end conversion or withdrawal analyses. A plan computed on last year's brackets silently misstates bracket-fill room and IRMAA exposure.
- Anchor every figure to a tax year in client-facing output. For reference, 2026 values: standard deduction $32,200 (married filing jointly); 22% bracket tops out at $211,400 of MFJ taxable income; first IRMAA threshold $218,000 MFJ (based on MAGI from two years prior). Always verify current-year values — these adjust annually.
- Custom overrides (e.g., a state tax assumption entered manually) should be inventoried and re-validated each year, since they do not refresh with vendor updates.

### Plan-to-Portfolio Linkage
The financial plan and the investment portfolio are two sides of the same coin. The plan determines what the portfolio must deliver (required return, risk budget, withdrawal schedule), and the portfolio must be constructed to meet those requirements. When the plan and portfolio are disconnected, the client receives inconsistent advice.

**From plan to portfolio — the forward link:**
- The plan produces a required rate of return: the return the portfolio must achieve for the plan to succeed at the target probability.
- The plan identifies the client's risk capacity: the maximum tolerable drawdown or volatility before the plan fails. Risk capacity is derived from the plan — a client with a well-funded plan and flexible spending has high risk capacity; a client on the edge of plan failure has low risk capacity.
- These outputs feed the Investment Policy Statement (IPS), which translates planning assumptions into portfolio constraints: target allocation, allowable ranges, rebalancing triggers, withdrawal rules.

**The IPS as the bridge document:**
- The IPS connects the financial plan to the portfolio. It specifies the return objective (from the plan), the risk tolerance (ability from the plan, willingness from client assessment), and the constraints (liquidity needs from the plan's withdrawal schedule, time horizon from the plan's goal dates, tax considerations from the plan's tax projection).
- When the plan changes, the IPS should be reviewed and updated. When the IPS changes, the portfolio should be adjusted accordingly.

**From portfolio to plan — the feedback loop:**
- Portfolio performance (actual returns, contributions, withdrawals) feeds back to update the plan. If the portfolio outperforms, the plan's probability of success improves. If the portfolio underperforms, the plan may need adjustment.
- Account-level activity (Roth conversions executed, RMDs taken, tax-loss harvesting realized) affects the plan's tax projection and should be reflected in the next plan update.

**Closed-loop planning:** Changes in the portfolio feed back to update the plan; changes in the plan feed forward to update the portfolio. This two-way connection is the hallmark of integrated advisory practice. Without it, the plan and portfolio drift apart over time, and the client receives conflicting messages about their financial situation.

**Mapping goals to accounts and time horizons:**
- Short-term goals (1-3 years) map to low-risk allocations: cash, short-term bonds, money market funds.
- Medium-term goals (3-10 years) map to moderate allocations: intermediate-term bonds, balanced strategies.
- Long-term goals (10+ years) map to growth allocations: equities, real assets, alternatives.
- This goal-to-account mapping ("bucketing" or "time segmentation") is the data linkage that lets clients see why different parts of the portfolio are invested differently — and it only works if the planning tool's goal records are linked to specific PMS accounts.

### Data Flows and Integration Patterns
The financial plan is only as good as the data that flows into it and the degree to which its outputs are acted upon.

**Data flowing into the financial plan:**
- **Client demographics** (from CRM): names, dates of birth, marital status, dependents, employment status, expected retirement date, health status, state of residence.
- **Current portfolio** (from PMS/custodian): account types, balances, holdings, asset allocation, cost basis, unrealized gains/losses.
- **Held-away assets** (from aggregation): 401(k) plans at current or former employers, spouse's accounts, bank accounts, real estate equity, stock options, restricted stock units, deferred compensation.
- **Insurance policies** (from client interview or document upload): life, disability, long-term care, annuity contracts.
- **Real estate** (from client interview or third-party valuation): primary residence value, mortgage balance, rental and vacation properties.
- **Income and expense data** (from client interview, tax returns, or budgeting tools): salary, bonus, rental and investment income, Social Security estimates (from SSA statements), pension details, itemized expenses or estimated spending rates.

**Data flowing out of the financial plan:**
- **Required return target** (to PMS/IPS): drives asset allocation decisions.
- **Risk capacity** (to PMS/IPS): the maximum risk the plan can tolerate before probability of success drops below the acceptable threshold.
- **Recommended savings rate** (to advisor/client): the annual savings needed to keep the plan on track.
- **Withdrawal schedule** (to PMS for cash management): timing and amount of withdrawals from each account, accounting for tax optimization and RMD requirements.
- **Roth conversion schedule** (to PMS for execution): recommended conversion amounts by year.
- **Goal status updates** (to CRM/client portal): on-track, needs attention, at risk, unlikely — for each goal.

**Integration challenges:**
- **Manual re-entry:** Many advisory firms still manually re-enter data between systems (e.g., typing client data from the CRM into the planning tool, or manually updating the plan when portfolio values change). This introduces errors, consumes advisor time, and causes data staleness.
- **Data freshness:** If the plan uses a portfolio snapshot from three months ago, the plan's outputs may not reflect current reality. Automated data feeds (via APIs or custodial data feeds) keep the plan current.
- **Assumption synchronization:** The financial plan and the PMS must use consistent return assumptions. If the plan assumes a 7% return for equities but the PMS uses 8%, the plan and portfolio will produce conflicting messages. Assumption synchronization requires a documented process: assumptions are set once (typically in the CMA document), and all downstream systems reference the same source.
- **Bidirectional updates:** Changes in the portfolio (performance, deposits, withdrawals, Roth conversions) should flow back to update the plan automatically. Changes in the plan (new goals, revised assumptions, updated claiming strategy) should flow forward to trigger portfolio review. Most current platforms support one direction reasonably well but not both.

### Plan Outputs, Update Cadence, and Documentation
**Standard visual outputs from planning tools** (useful when specifying portal or report integrations): probability gauge (overall probability of success), goal funding chart (per-goal probability), cash flow waterfall (income sources stacked against expenses by year), net worth projection (base case plus scenario lines), and Monte Carlo fan chart (median and percentile bands). Modern tools also support real-time scenario recalculation during client meetings, which requires live data connections rather than stale imports.

**Plan update cadence and triggers:**
- **Annual review:** At minimum, the plan is updated once per year with current portfolio values, revised income/expense assumptions, and any goal changes.
- **Event-driven updates:** Major life events recorded in the CRM (job change, retirement, inheritance, divorce, death of a spouse, birth of a child, home purchase or sale) should trigger a plan update automatically.
- **Continuous monitoring:** Some platforms provide daily plan updates from live portfolio feeds, alerting the advisor when probability of success drops below a threshold. Batch re-runs after major market dislocations (e.g., a drawdown exceeding 15%) identify clients whose plans need attention.

**Plan acceptance and documentation:** After presenting the plan, document the client's acknowledgment of the assumptions used, the recommendations made, and the client's decisions (accepted, deferred, declined). This supports compliance requirements and ensures the planning tool, CRM, and IPS all reflect the same agreed state.

## Worked Examples

### Example 1: Closing the Loop Between Financial Planning and Portfolio Management

**Scenario:** A mid-size RIA with $800M in assets under management uses separate systems for financial planning (eMoney) and portfolio management (Orion). The firm discovers that the planning tool assumes a 6.5% return for a balanced portfolio while the PMS assumes 7.5% for the same allocation. This 100-basis-point discrepancy means the plans are more conservative than the portfolios imply, leading to inconsistent client communications: the plan says "you need to save more" while the portfolio projection says "you are ahead of schedule." The firm wants to close the loop.

**Design Considerations:**
1. **Assumption synchronization.** The root cause is that assumptions are set independently in each system. The fix requires a single authoritative source for capital market assumptions (CMAs). Establish a formal CMA document — reviewed and approved quarterly or annually by the firm's investment committee — that specifies expected return, standard deviation, and correlation for each asset class. Both the planning tool and the PMS must reference this document. When CMAs change, both systems must be updated simultaneously.

2. **Plan-to-IPS-to-model mapping.** Define a clear chain: the financial plan produces a required return and risk capacity for each client. These flow into the client's IPS, which specifies a target allocation and model portfolio. The model portfolio is implemented in the PMS. The mapping should be explicit and documented:
   - Plan output: "This client needs a 5.2% real return with a maximum drawdown tolerance of -25%."
   - IPS translation: "Target allocation: 65% equity / 30% fixed income / 5% alternatives. Benchmark: 65% MSCI ACWI / 30% Bloomberg Aggregate / 5% HFRI Fund Weighted."
   - PMS implementation: "Assign to Balanced Growth Model (Model BG-65)."

3. **Integration architecture.** Map the data flows between systems:
   - CRM to planning tool: client demographics, household data, life events (automated via API or manual entry).
   - Custodian to PMS: account balances, positions, transactions (automated via custodial data feed — daily).
   - PMS to planning tool: current portfolio value, allocation, account types (automated via API, or manual export/import if no API exists). This feed should refresh at least monthly, preferably daily.
   - Planning tool to PMS: required return target, withdrawal schedule, Roth conversion schedule (typically manual — the advisor interprets plan outputs and implements in the PMS, but the firm should document this handoff).
   - Planning tool to CRM: goal status, plan review date, plan probability of success (for advisor dashboard and client portal display).

4. **Ongoing update workflow.** Define the cadence and triggers:
   - **Quarterly:** PMS pushes updated portfolio values to the planning tool. The plan recalculates probability of success. If the probability changes by more than 5 percentage points, the advisor reviews the plan and considers whether action is needed.
   - **Annually:** The investment committee reviews and publishes updated CMAs. Both the planning tool and PMS are updated simultaneously. All client plans are re-run with the new assumptions. Material changes in probability are flagged for advisor review.
   - **Event-driven:** Major client life events (recorded in CRM) trigger a plan review. Major market events (a drawdown exceeding 15%) trigger a batch re-run of all plans to identify clients whose probability has dropped below the threshold.

**Analysis:**
The assumption mismatch is a governance failure, not a technology failure. The technology fix (syncing assumptions) is straightforward; the governance fix (establishing a single source of truth for CMAs, with a documented review and update process) is what prevents the problem from recurring.

Implementation steps:
1. The investment committee publishes a formal CMA document with expected returns, standard deviations, and correlations for all asset classes used in the firm's models. Include both nominal and real return expectations.
2. Update the planning tool to use the published CMAs. Most planning tools allow custom asset class assumptions — enter the exact figures from the CMA document.
3. Update the PMS to use the same CMAs for portfolio projections and performance expectations.
4. Verify consistency: run a test case through both systems. A client with a 60/40 portfolio should see the same expected return in the plan and the PMS projection. Document the verification.
5. Establish the quarterly/annual review cadence and assign ownership (the investment committee owns CMAs; the planning team owns the plan-side update; the portfolio operations team owns the PMS-side update).
6. Build a reconciliation check: quarterly, compare the expected return assumptions in the planning tool and PMS for a sample of clients. Flag any discrepancies.
7. Document the plan-to-IPS-to-model mapping for each client tier or model portfolio. When a new client plan is completed, the advisor uses the mapping to assign the appropriate model in the PMS.

The closed-loop workflow ensures that the plan drives the portfolio (forward link) and the portfolio updates the plan (feedback loop), with consistent assumptions at every step. The client hears one coherent story, not conflicting messages from disconnected systems.

### Example 2: Governing the Tax Parameters Behind a Roth Conversion Schedule

**Scenario:** An advisor uses the planning tool to model a multi-year Roth conversion ladder for a recently retired client, filling lower tax brackets each year while staying under IRMAA thresholds. (The conversion methodology itself — bracket-fill logic, conversion sizing, paying conversion tax from taxable assets — is covered in financial-planning-workflow.) The integration question: the conversion schedule's correctness depends entirely on the tax reference parameters loaded in the planning tool, and on the schedule flowing accurately to the PMS for execution.

**Design Considerations:**
1. **Tax parameter currency.** The bracket-fill calculation hinges on three annually updated figures, each of which must reflect the correct tax year in the planning tool. For tax year 2026 (verify current-year values): the MFJ standard deduction is $32,200; the 22% bracket tops out at $211,400 of taxable income; and the first IRMAA surcharge threshold is $218,000 of MAGI (MFJ), applied with a two-year lookback. If the tool still carries prior-year tables, every year of the conversion schedule is mis-sized — the plan will either leave bracket room unused or push conversions over an IRMAA threshold, where the surcharge can add several thousand dollars per person per year in Medicare costs.
2. **Parameter audit before year-end runs.** Add a checklist item to the firm's planning operations calendar: confirm the vendor's annual tax-table update has been applied, and re-validate any manually entered overrides (state tax rates, custom deduction assumptions) before running year-end conversion analyses.
3. **Schedule handoff to the PMS.** The plan's output — the recommended conversion amount by year — must reach the team executing conversions in the PMS/custodian. Document this handoff: who transcribes the schedule, where it lives in the PMS, and how mid-year income changes (which alter remaining bracket room) trigger a recalculation in the planning tool before the conversion is executed.
4. **Feedback loop.** Executed conversions must flow back into the plan (via the custodial feed or manual update) so the next year's bracket-fill calculation starts from the actual remaining traditional IRA balance, not the projected one.

**Analysis:**
The recurring failure mode is not bad planning logic but stale or unsynchronized data: prior-year tax tables, a conversion schedule executed from an outdated plan version, or executed conversions never reflected back into the plan. Treat tax parameters like CMAs — versioned, owned, and verified on a calendar — and treat the conversion schedule like any other plan-to-PMS data flow, with a documented handoff and a return feed. Because IRMAA uses a two-year MAGI lookback, the plan must also retain prior-year income data accurately; a planning tool that only models the current year forward will miss surcharges triggered by income already realized.

## Common Pitfalls
- Using different capital market assumptions in the financial planning tool and the portfolio management system, leading to conflicting client communications about whether the plan is on track.
- Manual re-entry of data between planning and portfolio systems, introducing errors and data staleness that undermine plan accuracy.
- Treating assumption updates as ad hoc rather than governed — without a single CMA source of truth with assigned ownership and review cadence, systems drift apart again after every fix.
- Presenting a single Monte Carlo probability number without acknowledging assumption sensitivity — a 1-2% change in expected return can move the probability by 10-15 percentage points, so assumption governance is inseparable from honest plan communication.
- Running year-end tax analyses (Roth conversions, gain harvesting) on stale tax reference parameters — bracket thresholds, standard deductions, and IRMAA thresholds change every year and must be verified in the tool.
- Supporting only one direction of synchronization — portfolio changes that never update the plan, or plan changes that never trigger portfolio review, break the closed loop.
- Not linking goals to specific accounts and time horizons — without this linkage, the portfolio allocation has no data connection to the plan's requirements, and goal status cannot be computed from live account values.
- Not documenting the client's acknowledgment of planning assumptions and recommendations — this creates compliance risk and makes it difficult to demonstrate the advisor's reasoning at future review meetings.

## Cross-References
- **financial-planning-workflow** (advisory-practice plugin): The single home for planning methodology — data gathering, retirement modeling, Monte Carlo interpretation, Roth conversion and Social Security strategy, scenario modeling, and plan presentation. This skill covers how that methodology connects to the rest of the technology stack.
- **investment-policy** (wealth-management plugin): The financial plan drives IPS construction by providing the required return, risk capacity, time horizon, and constraint inputs that the IPS formalizes into portfolio governance.
- **asset-allocation** (wealth-management plugin): The plan's required return and risk capacity set the boundaries for strategic asset allocation; plan goals map to time-horizon-based allocation buckets.
- **portfolio-management-systems** (advisory-practice plugin): The PMS implements the portfolio derived from the financial plan's outputs; data flows between the planning tool and PMS must be bidirectional and assumption-consistent.
- **client-reporting-delivery** (advisory-practice plugin): Plan progress reporting — goal status, probability of success, milestone tracking — is a core component of the client report package.
- **proposal-generation** (advisory-practice plugin): Financial plan outputs (required return, recommended allocation, account types) feed directly into the investment proposal presented to new and existing clients.
- **crm-client-lifecycle** (advisory-practice plugin): The CRM stores planning data (goals, assumptions, plan review dates), triggers event-driven plan updates based on life events, and displays plan status on the advisor dashboard.
- **tax-efficiency** (wealth-management plugin): Defines the asset location, Roth conversion, withdrawal sequencing, and harvesting principles whose outputs flow through the integrations described here.
