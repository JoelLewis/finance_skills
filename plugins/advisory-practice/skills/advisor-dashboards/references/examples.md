# Worked Examples — Advisor Dashboards

## Table of Contents

1. [Building an Executive Dashboard for an RIA's Management Team](#example-1-building-an-executive-dashboard-for-an-rias-management-team) — four-quadrant management-committee view, data integration layer, freshness alignment
2. [Designing an Advisor-Facing Daily Dashboard](#example-2-designing-an-advisor-facing-daily-dashboard) — action queue design, integration depth, adoption measurement
3. [Creating an Exception Monitoring Dashboard for Operations](#example-3-creating-an-exception-monitoring-dashboard-for-operations) — exception categories, SLA-based aging, trend analysis

## Example 1: Building an Executive Dashboard for an RIA's Management Team

**Scenario:** A $1.8 billion RIA with 22 advisors, 1,400 client households, and two offices needs an executive dashboard for the three-member management committee (CEO, COO, CCO). The firm has a portfolio management system (Orion), a CRM (Salesforce), and a standalone billing system. The management committee meets weekly and wants a single-page view that answers: Are we growing? Are we profitable? Are we compliant? Where do we need to act?

**Design Considerations:**

The executive dashboard must synthesize data from three separate systems into a unified view without requiring the management committee to log into multiple platforms. The data integration layer should pull AUM and performance data from Orion nightly, client and pipeline data from Salesforce via API, and revenue and billing data from the billing system after each quarterly billing run (with interim accrual estimates during the quarter). All data should land in a lightweight data warehouse that powers the dashboard, ensuring that metric calculations are consistent and auditable.

The layout should be organized into four quadrants aligned with the management committee's four key questions.

**Growth quadrant:**

- Total firm AUM with quarter-over-quarter and year-over-year change
- AUM growth decomposition waterfall (market vs. net new assets)
- Organic growth rate (annualized) benchmarked against the 5-10% industry target
- Net flows for the current quarter with a rolling 12-month trend
- New client pipeline with estimated AUM and probability-weighted forecast

**Revenue quadrant:**

- Total quarterly revenue with prior-quarter and prior-year comparison
- Effective fee rate trend (trailing 8 quarters)
- Revenue by advisor, ranked by contribution
- Revenue concentration: percentage of revenue from the top 10 clients, flagged if any single household exceeds 5%
- Revenue forecast for the next quarter based on current AUM and effective fee rates

**Compliance quadrant:**

- Annual review completion rate (percentage of clients current; target 100%)
- Overdue compliance items count with aging breakdown
- Disclosure delivery status for any pending regulatory updates
- Trade surveillance exception count

**People/Productivity quadrant:**

- AUM per advisor and revenue per advisor benchmarked against current industry-study medians
- Clients per advisor with capacity indicators
- Advisor retention (departures or signaled intent to leave)
- Staff-to-advisor ratio compared to industry benchmarks

**Analysis:**

The key design challenge is data freshness alignment. AUM data refreshes nightly from custodian feeds through Orion, but revenue data updates quarterly (with monthly accrual estimates providing interim visibility). Pipeline data in Salesforce depends on advisor diligence in updating opportunity records — stale pipeline data is worse than no pipeline data because it creates false confidence. The management committee should be trained to understand the refresh cadence of each metric, and the dashboard should display "as of" timestamps on every panel.

The most actionable items for the weekly meeting are: the organic growth rate (is the firm gathering assets or just riding the market?), the compliance completion rate (are we on track for 100% before year-end?), and advisor capacity indicators (do we need to hire before capacity constrains growth?). Revenue concentration deserves special attention — if the firm discovers that its top 10 households generate 25% of total revenue, that concentration risk should trigger a strategic discussion about diversification through new client acquisition and service-tier expansion.

Over time, the trailing trend data will prove more valuable than any single week's snapshot, enabling the management committee to detect gradual shifts — fee compression, rising attrition, declining organic growth — before they become critical. The firm should establish a quarterly dashboard review cadence to assess whether the displayed metrics are still driving decisions and whether any new strategic priorities require additional panels.

## Example 2: Designing an Advisor-Facing Daily Dashboard

**Scenario:** A 10-advisor RIA wants to replace its current practice of advisors checking multiple systems each morning (CRM for tasks, PMS for drift alerts, email for custodian notifications, spreadsheet for client birthdays) with a single daily dashboard that serves as the advisor's operational home screen. Each advisor manages approximately 100 client households. The firm uses Tamarac for portfolio management, Redtail for CRM, and Schwab as its primary custodian.

**Design Considerations:**

The daily dashboard must be the first screen the advisor sees each morning and should answer: What requires my attention today? The design should prioritize actionability over comprehensiveness — every item on the screen should have a clear next step, and the advisor should be able to act directly from the dashboard without navigating to another system.

The top section is a personal scorecard showing: the advisor's total AUM with daily change (from Tamarac), year-to-date net new assets versus annual goal, number of active client households, and upcoming milestone (next goal checkpoint). This section is compact — one line of key metrics providing context for the day.

The primary section is the action queue, displaying the top five to seven prioritized items drawn from multiple sources. Portfolio drift alerts from Tamarac (accounts exceeding the firm's 5% absolute drift threshold, showing client name, magnitude of drift, and a link to the rebalancing tool). CRM tasks due today from Redtail (follow-up calls, document collection, meeting preparation). Compliance deadlines approaching within 30 days (annual reviews, disclosure deliveries, profile updates). Client milestones from Redtail (birthdays this week, anniversaries, age-based triggers). Large cash movements detected from Schwab's transaction feed (deposits or withdrawals exceeding $25,000 in the prior business day). Each queue item includes the client name, a one-line description of why it matters, and direct-action buttons (call, email, schedule, view account, create proposal).

The secondary section provides awareness without demanding action: a market summary (major index performance for context during client conversations), the advisor's meeting schedule for the day (pulled from calendar integration), and a client communication log showing the last five outbound contacts with days-since-contact for the advisor's top-tier clients.

**Analysis:**

The critical success factor is integration depth. If the dashboard simply links to Tamarac, Redtail, and Schwab without pulling data into a unified view, it is merely a bookmark page and will not change advisor behavior. True integration means that clicking a drift alert opens Tamarac's rebalancing screen with the client's account pre-loaded, clicking a CRM task opens the Redtail activity record, and clicking a cash movement alert shows the client's full account detail from Schwab with the recent transaction highlighted.

The data refresh cadence should be: market data updates continuously during market hours, portfolio drift and cash movements refresh overnight from custodian EOD feeds, CRM tasks refresh in real-time via API, and compliance deadlines update daily from the compliance calendar. Mobile responsiveness is essential — when an advisor is at a client lunch and receives a push notification about a large deposit, they should be able to view the alert and make a note on their phone without returning to the office.

Adoption measurement is critical for the first 90 days. Track how many advisors log in to the dashboard daily, how many action items are completed through the dashboard versus through the underlying systems directly, and whether advisors report reduced time spent checking multiple systems. If adoption is low, conduct advisor interviews to identify friction points — the most common barriers are slow load times, stale data, and actions that require too many clicks to execute.

## Example 3: Creating an Exception Monitoring Dashboard for Operations

**Scenario:** A $3.5 billion RIA with a five-person operations team processes approximately 200 account-level events per day across two custodians (Schwab and Fidelity). The operations manager wants an exception dashboard that centralizes all items requiring human intervention, replaces the current process of checking multiple custodian portals and email inboxes, and provides aging and escalation visibility to ensure nothing falls through the cracks.

**Design Considerations:**

The exception dashboard should be organized by exception category, with each category displaying a count badge, a sortable detail list, and aging statistics. The categories are:

Reconciliation breaks: position, transaction, and cash discrepancies between the PMS and each custodian, sourced from the daily reconciliation job in Orion. Display break type, account, security (if applicable), PMS value versus custodian value, magnitude of the discrepancy, age in business days, and assigned operations staff member. Flag breaks older than 3 business days in yellow and older than 5 in red. The target is fewer than 10 open breaks at any time and zero breaks older than 5 business days.

Transfer tracking (ACAT and non-ACAT): all pending asset transfers, showing originating and receiving custodian, client name, estimated asset value, submission date, expected completion date, current status, and any NIGO or rejection notices. Transfers taking longer than 10 business days should escalate to the operations manager. Track NIGO rate (percentage of transfers returned as not in good order) and average transfer completion time as process health metrics.

Account opening status: new accounts in various stages of setup at each custodian, showing client name, account type, submission date, current status, and any outstanding documentation requirements. NIGO items should be flagged with the specific deficiency (missing signature, wrong form version, incomplete beneficiary designation) so the assigned CSA can resolve them efficiently.

Billing exceptions: sourced from the billing system's exception report after each billing preview. Display accounts with fees that deviate more than 10% from the prior period, zero-dollar fees, accounts missing from the billing run, and fee-schedule mismatches. Billing exceptions must be resolved before the billing run is approved and custodian debit instructions are submitted.

Custodian communication queue: items requiring follow-up with the custodian — rejected trades, failed fee debits, account restriction inquiries, cost basis disputes, and general service requests. Track submission date, custodian case number (if applicable), and days open.

**Analysis:**

The operations manager should configure a summary banner at the top of the dashboard showing total open exceptions by category, total exceptions opened today, total resolved today, and the current oldest unresolved item. This banner provides instant visibility into whether the team is keeping pace or falling behind.

Weekly trend charts showing exception volume by category help identify systemic issues: a rising reconciliation break count may indicate a custodian feed problem or a PMS configuration issue, while a rising NIGO rate may indicate that the firm's account opening forms need updating or that CSA training is required. Seasonal patterns also emerge from trend data — transfer volumes spike in January (new year rollovers) and April (tax-related movements), and the operations team can prepare by adjusting staffing or pre-staging common documentation.

The dashboard should also generate a daily email digest to the operations manager at end of day, summarizing open items, items resolved, and items approaching their SLA — ensuring that the manager has a complete picture even on days they cannot monitor the dashboard in real-time. SLA targets for each exception category should be prominently displayed: reconciliation breaks resolved within 3 business days, NIGO items resubmitted within 2 business days, transfers escalated if not completed within 10 business days, and billing exceptions resolved before the billing approval deadline. These SLAs provide both team accountability and the basis for process improvement when targets are consistently missed.

