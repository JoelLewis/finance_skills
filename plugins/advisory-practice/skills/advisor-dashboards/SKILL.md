---
name: advisor-dashboards
description: "Design, build, and optimize dashboards for RIA practice management with AUM tracking, revenue analytics, and KPI frameworks. Use when the user asks about tracking firm-level metrics, monitoring advisor productivity, measuring organic growth rate, analyzing client retention and attrition, building executive or branch manager views, setting up exception alerts for NIGO or rebalancing drift, benchmarking against industry peers, or designing role-based dashboard access. Also trigger when users mention 'how is the practice doing', 'revenue per advisor', 'client attrition', 'net new assets', 'effective fee rate', 'practice benchmarking', 'AUM growth decomposition', 'advisor capacity', or 'referral tracking'."
---

# Advisor Dashboards

## Purpose

Guide the design, build, and optimization of dashboards for RIA practice management — covering KPI selection, role-based views, exception monitoring, and benchmarking.

## Layer

10 — Advisory Practice (Front Office)

## Direction

both

## When to Use

- Designing or evaluating dashboards for RIA management, advisors, compliance, or operations
- Defining practice-level KPIs and metric hierarchies
- Tracking AUM growth, revenue trends, client flows, or advisor productivity
- Building exception and alert dashboards for operations or compliance
- Establishing benchmarking frameworks or goal-tracking views

## Core Concepts

### 1. Practice-Level KPI Framework

When advising on KPI selection, recommend metrics from this framework organized by firm health dimension:

| Category | Key Metrics | Benchmark Targets |
|----------|------------|-------------------|
| **Growth** | Total AUM, organic growth rate, net new assets, net flows | 5-10% annual organic growth |
| **Revenue** | Total revenue, effective fee rate (revenue / avg AUM), revenue per client | Effective fee rate trend stable or rising |
| **Clients** | Household count, retention rate, referral rate | 95%+ retention rate |
| **Productivity** | Clients per advisor, revenue per advisor, meeting volume | 75-125 households per advisor |
| **Profitability** | Operating margin, revenue per employee, comp-to-revenue ratio | 25-35% operating margin, 55-70% comp ratio |

**Critical decomposition:** Always recommend separating AUM growth into market appreciation vs. net new assets. A firm growing AUM 12% in a 10% market achieved only 2% organic growth.

**Track each metric at multiple levels:** firm > team > advisor > client segment > account type.

### 2. AUM and Revenue Dashboard Design

Recommend these core panels for financial dashboards:

- **AUM hierarchy view** — Drill from firm total down to team/advisor/household. Flag concentration risk (single advisor managing disproportionate share)
- **Revenue breakdown** — By fee type (AUM-based, planning, hourly), by advisor, by segment. Track effective fee rate trend over 8+ quarters
- **Flow tracking** — Gross inflows (new + existing client), gross outflows (distributions + attrition), net flows on rolling 12-month trend
- **AUM growth waterfall** — Beginning AUM + market return + net new assets = ending AUM. Display as waterfall chart
- **Pipeline** — CRM-sourced prospects with estimated AUM, probability, expected funding date, assigned advisor

### 3. Client Flow Analytics

Advise on these flow analysis components:

- **Acquisition funnel:** Lead > meeting > proposal > signed > funded. Track conversion rates at each stage and average time-to-fund. Segment by advisor to identify bottlenecks
- **Attrition tracking:** Departures by reason (fee sensitivity, service, competitor, death, relocation), by advisor, by tenure. Flag early-tenure attrition (<2 years) as onboarding issue; long-tenure (10+ years) as generational risk
- **Money-in-motion signals:** Large external deposits (consolidation opportunity), systematic outflows exceeding income needs (departure risk), reduced engagement, beneficiary changes. Flag for proactive advisor follow-up
- **Asset consolidation:** Gap between total household assets (via aggregation) and managed assets. Rank opportunities by dollar value
- **Competitive losses:** Capture destination and reason for departures to inform pricing and value proposition
- **Generational transfer risk:** Flag accounts with primary holder age 75+; track whether next-generation relationship exists and outcomes of recent inheritance events

### 4. Exception and Alert Dashboard Design

Structure exception dashboards by category with count badges, sortable detail lists, and aging statistics:

| Exception Type | Key Fields to Display | SLA Target |
|---------------|----------------------|------------|
| **Compliance alerts** | Responsible party, deadline, days overdue, escalation status | Per regulatory deadline |
| **Reconciliation breaks** | Account, PMS vs. custodian value, magnitude, age | Resolved within 3 business days |
| **NIGO items** | Deficiency reason, age, assigned CSA, resolution status | Resubmitted within 2 business days |
| **Transfer tracking** | Custodian, estimated value, submission date, current status | Escalate if >10 business days |
| **Billing exceptions** | Fee deviation %, zero-dollar fees, schedule mismatches | Resolved before billing approval |
| **Rebalancing drift** | Current vs. target allocation, drift magnitude, days since breach | Per firm drift policy |

**Design checklist for exception dashboards:**
- [ ] Summary banner: total open, opened today, resolved today, oldest unresolved
- [ ] Color coding: green/yellow/red by SLA status
- [ ] Aging analysis by category to identify process bottlenecks
- [ ] Daily email digest for managers
- [ ] Weekly trend charts to surface systemic issues

### 5. Advisor Productivity Metrics

Recommend tracking these productivity indicators:

- **Clients per advisor** — Capacity indicator (75-125 household range). Flag advisors near capacity for support staffing or client transition planning
- **Revenue per advisor** — Benchmark against Schwab RIA Benchmarking, InvestmentNews, FA Insight studies
- **Meeting volume** — Leading indicator of relationship health; declining counts signal disengagement
- **Proposal-to-close ratio** — Low ratios suggest pricing, proposal quality, or value proposition issues
- **Onboarding pipeline** — Track average time by stage (signed > opened > transferred > invested > first review). Identify delay bottlenecks
- **Capacity forecast** — Project when each advisor reaches capacity based on current growth trajectory. Inform hiring 12+ months ahead

### 6. Dashboard Design Principles

**Role-based view checklist — recommend the appropriate view based on the user's audience:**

| Role | Focus | Key Question |
|------|-------|-------------|
| **Advisor** | Personal book: NBA queue, drift alerts, tasks, personal KPIs, client milestones | "What should I do today?" |
| **Manager** | Team aggregation: advisor comparison, team pipeline/flows, exceptions, capacity | "Who needs support?" |
| **Compliance** | Firm-wide: overdue reviews, surveillance alerts, filing deadlines, exception aging | "Are supervisory obligations met?" |
| **Executive** | Firm financials: AUM, revenue, growth decomposition, profitability, benchmarks | "Where should we invest or act?" |

**Design principles to always recommend:**
- **Drill-down:** Every summary metric clickable from firm > team > advisor > client > account
- **Data freshness labels:** Timestamp every panel (AUM = nightly, exceptions = intraday, pipeline = last CRM update)
- **Mobile-first:** Top 3-5 metrics on mobile; push notifications for critical alerts
- **Data integration layer:** Normalize PMS, CRM, billing, custodian, planning, and compliance data into a single warehouse or ETL pipeline

### 7. Benchmarking and Goal Tracking

**Recommend these benchmarking layers for every KPI dashboard:**

- **Firm targets:** Actual/target/variance with green/yellow/red status based on year-to-date run rate
- **Advisor goals:** Individual targets for net new AUM, new households, revenue, meetings. Visible to advisor (self-management) and manager (coaching)
- **Industry benchmarks:** Source from Schwab RIA Benchmarking, Fidelity, InvestmentNews, FA Insight. Filter by firm size, geography, and service model for valid comparison
- **Trend analysis:** Display 8-12 quarters of history with 3-4 quarter moving averages. Trends reveal fee compression, seasonal flow patterns, and capacity saturation that snapshots miss

## Worked Examples

### Example 1: Executive Dashboard for an RIA Management Team

**Scenario:** A $1.8B RIA (22 advisors, 1,400 households, two offices) needs a weekly management committee dashboard fed by Orion (PMS), Salesforce (CRM), and a standalone billing system.

**Design Considerations:**

Recommend a four-quadrant layout aligned with the committee's core questions:

1. **Growth quadrant:** Total AUM (QoQ, YoY change), AUM growth waterfall, organic growth rate vs. 5-10% target, net flows (rolling 12-month), pipeline (probability-weighted forecast)
2. **Revenue quadrant:** Quarterly revenue (vs. prior quarter/year), effective fee rate trend (8 quarters), revenue by advisor, concentration risk (flag if top 10 households exceed 25% of revenue), next-quarter forecast
3. **Compliance quadrant:** Annual review completion rate (target 100%), overdue items with aging, disclosure delivery status, surveillance exception count
4. **People quadrant:** AUM and revenue per advisor vs. Schwab benchmarks, clients per advisor with capacity flags, staff-to-advisor ratio

**Integration approach:** Nightly Orion feed for AUM, Salesforce API for pipeline/clients, quarterly billing import with monthly accrual estimates. Land in a lightweight data warehouse.

**Analysis:**

The primary design challenge is data freshness alignment — label each panel with "as of" timestamps. Pipeline data quality depends on advisor CRM discipline; flag stale opportunities. The most actionable weekly items: organic growth rate, compliance completion trajectory, and advisor capacity indicators approaching saturation.

### Example 2: Advisor-Facing Daily Dashboard

**Scenario:** A 10-advisor RIA wants a single morning dashboard replacing separate logins to Tamarac (PMS), Redtail (CRM), and Schwab (custodian). Each advisor manages approximately 100 households.

**Design Considerations:**

Structure in three tiers:

1. **Personal scorecard (top bar):** AUM with daily change, YTD net new assets vs. goal, household count, next milestone
2. **Action queue (primary):** Top 5-7 prioritized items from all sources:
   - Drift alerts (accounts exceeding 5% threshold) with rebalancing link
   - CRM tasks due today
   - Compliance deadlines within 30 days
   - Client milestones (birthdays, anniversaries, age triggers)
   - Large cash movements (>$25K prior business day)
   - Each item: client name, one-line reason, direct-action buttons (call, email, schedule, view)
3. **Awareness panel (secondary):** Market summary, today's meeting schedule, last 5 outbound contacts with days-since for top-tier clients

**Analysis:**

Deep integration is the critical success factor — clicking a drift alert must open Tamarac's rebalancing screen pre-loaded, not just link to the login page. Refresh cadence: market data continuous, portfolio/cash overnight, CRM real-time, compliance daily. Track adoption for 90 days: daily login rate, actions completed via dashboard vs. directly, advisor-reported time savings. Common adoption barriers: slow load times, stale data, too many clicks to act.

### Example 3: Operations Exception Dashboard

**Scenario:** A $3.5B RIA (5-person ops team, 200 daily account events, dual custodian Schwab/Fidelity) needs a centralized exception dashboard replacing multiple portal and email checks.

**Design Considerations:**

Organize by exception category, each with count badge, sortable list, and aging stats:

- **Reconciliation breaks:** PMS vs. custodian discrepancies. Yellow at 3 days, red at 5. Target: <10 open, zero over 5 days
- **Transfers (ACAT/non-ACAT):** Status, NIGO/rejection notices. Escalate at 10 business days. Track NIGO rate and average completion time
- **Account opening:** Status by custodian, outstanding documentation, specific NIGO deficiency for CSA resolution
- **Billing exceptions:** Fee deviations >10%, zero-dollar fees, missing accounts, schedule mismatches. Resolve before billing approval
- **Custodian queue:** Rejected trades, failed debits, restriction inquiries. Track case numbers and days open

**Analysis:**

Top-of-dashboard summary banner: total open by category, opened today, resolved today, oldest item. Weekly trend charts surface systemic issues (rising recon breaks signal feed problems; rising NIGO rate signals form or training issues). Seasonal patterns (January rollovers, April tax movements) inform staffing. Daily EOD email digest ensures manager visibility. Display SLA targets prominently for team accountability.

## Common Pitfalls

- **Metric overload** — Limit each view to 5-7 primary metrics with drill-down for detail
- **Undifferentiated AUM growth** — Always decompose into market return vs. net new assets
- **Inconsistent metric definitions** — Establish a firm-wide data dictionary; enforce across all dashboards
- **Missing data freshness labels** — Timestamp every panel to prevent users mixing stale and current data
- **No drill-down capability** — Every aggregate must be clickable through to underlying detail
- **Desktop-only design** — Design for mobile first; push critical alerts to phone
- **Flat exception lists** — Implement severity levels, SLA-based aging, and escalation rules
- **Annual-only goal reviews** — Display goal progress continuously for real-time self-correction and coaching
- **Manual data entry** — Automate meeting counts, contact frequency, and task completion via calendar/CRM integration
- **Mismatched benchmarks** — Filter industry comparisons by firm size, geography, and service model
- **Dashboard without behavioral change** — Embed in operational rhythms: weekly meetings, compensation ties, exception assignment queues
- **Static dashboard design** — Review relevance annually; retire metrics that no longer drive decisions

## Cross-References

- **crm-client-lifecycle** (Layer 10, advisory-practice) — CRM data (client segments, activity logs, pipeline, lifecycle stage) is a primary data source for dashboard metrics including client count, attrition, meeting volume, and acquisition funnel analytics.
- **fee-billing** (Layer 10, advisory-practice) — Billing system data feeds revenue metrics, effective fee rates, billing exception counts, and fee-schedule compliance indicators displayed on revenue and exception dashboards.
- **performance-reporting** (Layer 7, wealth-management) — Performance calculation outputs (TWR, MWR, benchmark comparisons) feed dashboard panels showing portfolio-level and firm-level investment results, and performance dispersion across accounts.
- **client-reporting-delivery** (Layer 10, advisory-practice) — Client reporting workflows generate data on report delivery status, portal engagement, and communication frequency that inform advisor productivity and client engagement dashboard sections.
- **portfolio-management-systems** (Layer 10, advisory-practice) — The PMS provides AUM data, position-level holdings, drift analysis, and reconciliation status that power AUM dashboards, drift alert panels, and reconciliation exception views.
- **next-best-action** (Layer 10, advisory-practice) — NBA systems generate the prioritized action queue displayed on the advisor daily dashboard; dashboard adoption metrics (acceptance rate, completion rate) feed NBA effectiveness measurement.
- **operational-risk** (Layer 11, trading-operations) — Operational risk event data (trade errors, settlement failures, process breakdowns) feeds exception dashboards and provides the risk metrics displayed on management and compliance views.
