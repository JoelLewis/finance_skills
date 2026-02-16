---
name: next-best-action
description: "Next-best-action frameworks for advisor workflows: event-driven triggers, prioritization scoring, action queuing, advisor nudges, automated workflows, personalized recommendations."
allowed-tools: ["Bash", "Read", "Write", "Edit"]
---

# Next-Best-Action — Event-Driven Advisor Recommendations

## Purpose
Enable the design, evaluation, and implementation of next-best-action (NBA) systems for financial advisory practices. This skill covers the full NBA lifecycle — from event detection and trigger design through action identification, prioritization scoring, advisor delivery, workflow integration, and effectiveness measurement. It provides frameworks for building proactive, data-driven advisor productivity tools that surface the most valuable action an advisor should take for each client at any given time, replacing reactive and manual task management with intelligent, personalized recommendations.

## Layer
10 — Advisory Practice (Front Office)

## Direction
prospective

## When to Use
- Designing or evaluating an NBA engine for an RIA, broker-dealer, or wealth management platform
- Building event-driven triggers that detect portfolio, life, market, compliance, or practice events
- Defining an action library and recommendation logic for advisor outreach
- Designing prioritization and scoring models to rank competing actions
- Routing NBA actions to the appropriate team member (advisor, CSA, operations, compliance)
- Selecting delivery channels and designing advisor nudge formats
- Integrating NBA recommendations with CRM, portfolio management, financial planning, and trading systems
- Implementing compliance-driven NBA actions (annual reviews, disclosure delivery, suitability re-certification)
- Measuring NBA effectiveness (acceptance rate, time-to-action, revenue impact, compliance completion)
- Evaluating vendor NBA platforms or building custom NBA capabilities

## Core Concepts

### Next-Best-Action Framework
Next-best-action is an advisor productivity and client service methodology that analyzes client data across systems to surface the single most valuable action an advisor should take for each client at any given time. The concept originates in CRM and marketing automation — industries that have long used event-driven recommendation engines to guide customer-facing personnel toward high-value interactions — but its application in wealth management addresses a distinct set of challenges: advisors managing hundreds of client relationships cannot manually monitor every portfolio, life event, compliance deadline, and practice touchpoint across their entire book of business.

NBA differs fundamentally from traditional task management. Traditional task management is reactive and manual: advisors create their own to-do lists, respond to inbound client requests, and rely on memory or periodic reviews to identify outreach opportunities. NBA is proactive and data-driven: the system continuously monitors client data across custodial feeds, CRM records, financial plans, compliance calendars, and market data, automatically identifying situations that warrant advisor attention and recommending specific actions with supporting context.

The core components of an NBA system are:

- **Event detection** — Continuous monitoring of data sources to identify triggering events (portfolio drift, large cash movement, life milestone, compliance deadline, market dislocation).
- **Action identification** — Mapping detected events to a catalog of recommended actions (schedule review, propose rebalancing, discuss tax-loss harvesting, update beneficiaries).
- **Prioritization** — Scoring and ranking competing actions across all clients to ensure advisors focus on the highest-value activities given limited time.
- **Routing** — Directing each action to the appropriate person based on role, expertise, relationship, and availability.
- **Delivery** — Presenting recommendations through the channels advisors actually use (dashboard, mobile notification, email digest, CRM task).
- **Tracking** — Recording action outcomes (accepted, deferred, rejected, completed) to close the feedback loop and improve future recommendations.

### Event Detection and Trigger Types
The quality of an NBA system depends on the breadth and reliability of its event detection. Events fall into five categories, each requiring different data sources and detection logic.

**Portfolio events** are detected from custodial data feeds, portfolio management systems, and market data:

- Drift beyond threshold — A client's actual allocation has deviated from the target model beyond the firm's tolerance band (e.g., equity allocation at 72% vs. 65% target with a 5% tolerance). Requires real-time or daily position data and model assignment.
- Large cash deposit or withdrawal — A significant cash movement (typically defined by absolute amount or percentage of portfolio) has occurred. Detected from custodial transaction feeds. A $200,000 deposit into a $1 million account signals an investment opportunity; a $200,000 withdrawal from the same account may signal a liquidity event requiring plan reassessment.
- Concentrated position — A single holding has grown to exceed a concentration threshold (e.g., 10% or 15% of portfolio value), whether through appreciation, additional purchases, or stock compensation vesting. Detected from position-level holdings data.
- Tax-loss harvesting opportunity — Unrealized losses in taxable accounts exceed a significance threshold, particularly near year-end or after market declines. Requires lot-level cost basis data and market prices.
- Required minimum distribution (RMD) due — A client with a traditional IRA or inherited IRA is approaching or has reached an RMD deadline. Requires account type data and client date of birth. RMD deadlines are absolute (December 31 for most, April 1 of the following year for the year the owner turns 73).
- Margin call — A client's margin account has breached maintenance requirements. Requires margin balance and equity data from the custodian. Margin calls are time-sensitive and typically require same-day or next-day resolution.

**Life events** are detected from CRM data, client-reported information, and public records:

- Birthday milestones — Age-based financial triggers: 59-1/2 (penalty-free IRA withdrawals), 62 (early Social Security eligibility), 65 (Medicare eligibility), 70-1/2 (qualified charitable distributions from IRAs), 73 (RMD beginning age under SECURE 2.0 for those born 1951-1959). Detected from client date of birth in CRM.
- Marriage, divorce, death of spouse — Major life transitions requiring comprehensive financial plan review, beneficiary updates, account re-titling, and potentially revised investment strategy. Typically detected through advisor-reported CRM updates or client-initiated contact.
- New child or grandchild — Triggers discussions about education savings (529 plans), life insurance review, estate plan updates, and beneficiary designation changes.
- Job change or retirement — Income changes, employer benefit transitions (401k rollover), stock option/RSU vesting acceleration, and potential shift in investment time horizon and risk profile.

**Market events** are detected from market data feeds, portfolio analytics, and research systems:

- Sector or asset class drawdown affecting client holdings — A significant decline in a sector or asset class in which the client has meaningful exposure. Requires mapping client holdings to sectors and monitoring sector-level returns.
- Interest rate change impacting fixed income allocation — Significant rate movements that affect the duration risk, yield, or relative value of a client's fixed income holdings. Particularly relevant for clients with large bond allocations or approaching income-distribution phase.
- New fund or product launch replacing a current holding — A lower-cost, better-performing, or more tax-efficient alternative to a fund currently held by clients. Detected through product research and comparison analytics.

**Compliance events** are detected from compliance calendars, CRM activity logs, and regulatory data:

- Annual review overdue — The client has not received a formal portfolio or suitability review within the firm's required interval (typically 12 months). Detected by comparing the last review date in CRM to the current date.
- Suitability or best-interest re-certification due — Client profile information is stale and requires re-confirmation. Particularly important under Reg BI, where the care obligation requires that recommendations reflect current client circumstances.
- Disclosure delivery required — New regulations or rule amendments require delivery of updated disclosures (Form CRS updates, Form ADV amendments, privacy notices) to existing clients.

**Practice events** are detected from CRM activity tracking and practice management data:

- Client contact gap — A client has not been contacted (by any channel) within the firm's service standard for that client's tier. For example, a Tier 1 client ($5M+ AUM) with a quarterly contact standard who has not been contacted in 100 days.
- Upcoming contract renewal — An advisory agreement renewal or fee schedule review is approaching.
- Referral opportunity — A client has recently had a positive experience (strong performance period, successful financial plan milestone, positive service interaction) that presents a natural referral conversation opportunity.

### Action Library and Recommendation Logic
The action library is the catalog of all actions the NBA system can recommend. Each action is a defined, repeatable unit of advisor work with associated templates, context requirements, and completion criteria.

**Action catalog design.** A well-designed action library typically includes 30 to 60 distinct actions organized by category. Examples:

- Schedule annual review meeting
- Propose portfolio rebalancing to target model
- Discuss tax-loss harvesting opportunity with estimated tax savings
- Recommend Roth IRA conversion analysis (relevant for clients in temporarily low tax brackets)
- Update beneficiary designations following life event
- Review life insurance coverage adequacy
- Discuss estate plan review (triggered by legislative change, asset growth, or family change)
- Contact client regarding large uninvested cash position
- Congratulate client on life milestone (birthday, retirement, grandchild)
- Offer financial planning engagement to investment-only client
- Present charitable giving strategy (donor-advised fund, qualified charitable distribution)
- Discuss Social Security claiming strategy (approaching eligibility age)
- Review held-away account for consolidation opportunity
- Deliver required compliance disclosure

**Action templates.** Each action in the library includes pre-built supporting materials that reduce the advisor's preparation time and increase the likelihood of action completion:

- Talking points — Key discussion topics tailored to the specific trigger and client context (e.g., "Your portfolio has drifted to 72% equities vs. your 65% target. I recommend we rebalance by trimming the overweight in large-cap growth and adding to international and fixed income. This trade would also harvest approximately $12,000 in losses to offset the gains we realized earlier this year.").
- Email drafts — Pre-composed outreach emails personalized with client name, specific trigger details, and proposed next steps. The advisor reviews and edits before sending.
- Meeting agendas — Structured agendas for review meetings, planning discussions, or specific topic conversations.
- Analysis summaries — Pre-generated quantitative analysis (drift report, tax-loss harvesting estimate, RMD calculation, fee comparison) attached to the recommendation.

**Recommendation logic.** NBA systems use two primary approaches to map triggers to actions:

- Rule-based logic — Deterministic IF-THEN rules that map specific triggers to specific actions. Example: IF client age reaches 72 AND has traditional IRA AND no RMD distribution recorded this year THEN recommend "Contact client re: RMD before December 31 deadline." Rule-based logic is transparent, auditable, and appropriate for compliance-driven and well-understood triggers.
- ML-enhanced logic — Machine learning models that learn from historical advisor behavior to improve recommendations. The model observes which recommended actions advisors accept or reject, which actions lead to positive outcomes (client retention, additional assets, completed plans), and which client characteristics predict action relevance. ML enhancement is layered on top of rule-based logic — rules ensure required actions are never missed, while ML improves the ranking and presentation of discretionary actions.

### Prioritization and Scoring
Not all actions are equal. An advisor with 200 clients might have 50 pending actions on any given day, but can realistically complete five to seven. Prioritization scoring determines which actions rise to the top of the queue.

**Scoring dimensions.** Effective prioritization considers multiple dimensions, each scored on a normalized scale:

- **Urgency** — How time-sensitive is the action? An RMD deadline in December is more urgent in November than in March. A margin call is urgent immediately. A referral opportunity is low urgency. Urgency scoring should incorporate hard deadlines (compliance dates, regulatory deadlines) and soft deadlines (optimal timing windows that pass but do not create violations).
- **Impact** — What is the potential benefit of completing the action? Impact can be measured along several sub-dimensions: revenue potential (will the action lead to new assets, a planning engagement, or retained AUM?), retention risk (is the client at risk of leaving if this issue is not addressed?), compliance requirement (is the action mandated by regulation or firm policy?), client satisfaction (will the action strengthen the relationship?).
- **Effort** — How much advisor time and preparation does the action require? A quick congratulatory call requires five minutes; a comprehensive financial plan review requires several hours of preparation and a 90-minute meeting. Effort scoring ensures that the queue includes a realistic mix of quick wins and substantial engagements.
- **Client importance** — What is the client's tier, AUM, relationship depth, and strategic value? Most firms weight actions for higher-tier clients more heavily, reflecting the disproportionate business impact of retaining and deepening large relationships. However, this weighting should not result in lower-tier clients being systematically neglected — compliance-driven and risk-driven actions should override tier-based scoring.

**Composite scoring.** The overall priority score is a weighted combination of dimension scores:

Priority = (W_urgency x Urgency) + (W_impact x Impact) - (W_effort x Effort) + (W_client x ClientImportance)

Weights are calibrated to the firm's strategic priorities. A firm focused on growth may weight impact and client importance heavily. A firm under regulatory scrutiny may weight urgency and compliance-driven impact heavily. Weights should be reviewed and adjusted periodically based on business outcomes.

**Priority queue management.** Queue design prevents action fatigue — the phenomenon where advisors ignore recommendations because the system generates too many:

- Cap the daily queue at five to seven actions per advisor, based on empirical research showing that beyond this threshold, completion rates drop sharply.
- Ensure the queue includes a mix of action types — not exclusively compliance items or exclusively revenue-driven items.
- Allow advisors to defer actions (with a snooze period) without permanently dismissing them. Deferred actions return to the queue after the snooze period with an adjusted priority score.
- Compliance-driven actions with approaching deadlines should be flagged as non-deferrable once they enter a critical window (e.g., within 15 days of the deadline).

**Advisor capacity consideration.** The NBA system should account for advisor availability when generating queues. An advisor returning from vacation faces a backlog; an advisor with a light meeting day has capacity for a complex action. Integration with the advisor's calendar and CRM activity log enables capacity-aware queue generation.

### Action Routing and Assignment
Not every action requires the advisor's personal attention. Effective routing directs each action to the right person based on the nature of the work, the relationship requirement, and the team structure.

**Role-based routing rules:**

- **Advisor** — Relationship decisions, complex discussions, high-value client interactions, investment strategy conversations, financial planning reviews. The advisor handles actions where the personal relationship and professional judgment are essential.
- **Client service associate (CSA)** — Scheduling meetings, document collection, routine follow-up calls, account maintenance requests, birthday and milestone acknowledgments (if the firm delegates these). CSAs handle actions that are important but do not require the advisor's expertise.
- **Operations team** — Account transfers, beneficiary designation processing, cost basis corrections, distribution processing, account opening paperwork. Operations handles actions that involve back-office execution.
- **Compliance team** — Regulatory disclosure delivery, suitability re-certification review, advertising review items, compliance-exception resolution. Compliance handles actions that require regulatory expertise or supervisory approval.

**Escalation rules.** Actions that are not completed within their service-level agreement (SLA) should escalate automatically:

- Level 1 (approaching SLA) — Visual indicator in the dashboard (color change from green to yellow).
- Level 2 (at SLA) — Push notification to the assigned individual and their supervisor.
- Level 3 (past SLA) — Escalation to the practice manager or branch manager, with the overdue action flagged in management reports.
- Level 4 (compliance actions past SLA) — Escalation to the Chief Compliance Officer, with the overdue action logged as a compliance exception.

**Team-based routing.** In team-based advisory practices, routing rules should consider advisor specialization (tax planning, estate planning, retirement income), current workload, and client assignment. If the primary advisor is unavailable, the system should route time-sensitive actions to a designated backup advisor rather than allowing them to age in the queue.

### Delivery Channels and Nudges
The most carefully prioritized recommendation is worthless if the advisor never sees it. Delivery channel design and nudge formatting directly affect adoption rates.

**Delivery channels:**

- **Dashboard widget (morning briefing)** — A dedicated section of the advisor's home screen displaying the day's priority queue. The morning briefing is the primary delivery channel for most NBA implementations, designed to be the first thing the advisor reviews each day. Effective morning briefings display the top five to seven actions ranked by priority, with a one-line summary and the client name for each.
- **Push notifications (mobile and desktop)** — Real-time alerts for urgent, time-sensitive actions (margin call, large cash deposit, compliance deadline within 48 hours). Push notifications should be reserved for genuinely urgent items to avoid notification fatigue.
- **Email digest (daily or weekly)** — A summary email listing pending actions, upcoming deadlines, and completed actions from the prior period. The email digest serves as a secondary channel and a record that the advisor can reference outside the dashboard. Weekly digests work well for practice-level summaries; daily digests suit high-volume practices.
- **CRM task creation** — NBA recommendations automatically create tasks in the firm's CRM system, ensuring that actions are tracked in the advisor's existing workflow tool. CRM integration is critical for adoption — if advisors must check a separate system for NBA recommendations, adoption will be low.
- **Calendar integration** — For actions involving client meetings, the system can auto-suggest or auto-block calendar time based on the client's preferred meeting times and the advisor's availability. This reduces the friction between "I should schedule a review with this client" and actually scheduling it.

**Nudge design.** A nudge is the atomic unit of NBA delivery — the brief, actionable message that presents the recommendation to the advisor. Effective nudges share several characteristics:

- Brief — Two to three sentences maximum for the initial display. The advisor should be able to read the nudge in under 10 seconds and decide whether to act.
- Contextual — The nudge includes enough client-specific information that the advisor understands why the action matters without opening the full client record. Include the trigger event, the relevant data point, and the recommended action.
- Actionable — The nudge includes a clear call to action and a direct link to execute it. "John Smith deposited $150K yesterday. His portfolio is now 12% cash vs. 3% target -- recommend investing per his growth model. [View Account] [Create Proposal]."
- Prioritized — Visual cues (color coding, icons, position in the queue) communicate the action's priority relative to other items.

**Timing.** When nudges are delivered affects adoption:

- Morning delivery (7:00-8:00 AM) for the daily priority queue, so advisors start the day with a clear action plan.
- Real-time delivery for urgent items (margin calls, same-day compliance deadlines, large cash movements).
- Post-market-close delivery for performance-related triggers (drawdown alerts, drift notifications) that should not interrupt the trading day.
- End-of-week delivery for practice-level summaries and the following week's preview.

### Client Context and Personalization
Effective NBA recommendations require deep client context. A generic "call this client" recommendation is far less actionable than a recommendation that explains why the call matters and provides client-specific talking points.

**Context assembly.** When an event triggers an NBA recommendation, the system should assemble a context package that includes:

- **Investment profile** — Current allocation, target model, risk profile, investment objectives, account types, tax status, cost basis summary.
- **Financial plan status** — Current plan (if any), funded status of goals, Monte Carlo probability, key assumptions, upcoming milestones. A client whose retirement plan is 95% funded requires a different conversation than one at 60%.
- **Recent interactions** — Last contact date, last meeting date, topics discussed, outstanding action items from prior meetings, recent service requests. The advisor should not call a client unaware that the client called the service desk with a complaint yesterday.
- **Communication preferences** — Preferred contact method (phone, email, video), preferred meeting time, preferred frequency. Respecting preferences increases engagement and demonstrates attentiveness.
- **Life stage and upcoming events** — Current life stage (accumulation, pre-retirement, distribution, legacy), upcoming milestones (age-based, contract-based), recent life events.
- **Household context** — Spouse/partner information, dependent children, other family members who are also clients, household-level asset aggregation, estate plan status.

**Personalization.** The recommended action and its supporting materials should reflect the specific client's situation:

- Talking points should reference the client's specific holdings, goals, and circumstances — not generic advice.
- Analysis summaries should use the client's actual data (actual drift amount, actual tax-loss estimate, actual RMD calculation).
- Email drafts should reflect the client's communication style and relationship tone (formal vs. informal, detail-oriented vs. summary-focused).

**Historical context.** The system should track the history of NBA recommendations for each client:

- What actions were previously recommended? Did the advisor accept, defer, or reject them?
- Were deferred actions eventually completed?
- What was the client's response to prior outreach driven by NBA recommendations?

This history prevents repetitive recommendations (do not recommend the same action that was rejected last week) and enables trend analysis (a client who consistently defers review meetings may need a different engagement approach).

### Workflow Integration
NBA delivers maximum value when the recommendation connects seamlessly to the execution workflow. Clicking "Propose Rebalancing" should not just remind the advisor to rebalance — it should open the rebalancing tool with the client's accounts pre-loaded, the current drift analysis displayed, and the proposed trades ready for review.

**Execution workflow connections:**

- "Propose Rebalancing" opens the portfolio management system with the client's account, current vs. target allocation, and proposed trades pre-populated.
- "Schedule Review" opens the calendar with the client's preferred meeting times highlighted, a pre-built agenda template attached, and a draft invitation email ready to send.
- "Send Tax-Loss Report" generates the tax-loss harvesting analysis from the portfolio system, formats it into the firm's reporting template, and queues it for delivery through the client's preferred channel.
- "Update Beneficiaries" opens the account maintenance workflow with the client's current beneficiary designations displayed and a form pre-populated with the client's information.
- "Deliver Disclosure" queues the required document for delivery through the firm's document delivery system, with tracking confirmation.

**CRM activity logging.** When an advisor completes an NBA-recommended action, the system should automatically log the activity in the CRM:

- Record the trigger event, recommended action, advisor action (accepted/deferred/rejected), completion timestamp, and outcome.
- Link the activity to the client record and the advisor record.
- If the action involved a client interaction, log the interaction details (date, method, duration, topics, next steps).

Automatic logging eliminates the manual data entry that advisors routinely skip, ensuring that the CRM reflects actual practice activity and providing the data foundation for relationship tracking, compliance documentation, and practice analytics.

**Feedback loop.** Advisor acceptance and rejection of NBA recommendations should feed back into the system to improve future recommendations:

- Track acceptance rates by action type, trigger type, advisor, and client segment.
- Identify actions that are consistently rejected and investigate whether the trigger logic, prioritization, or action template needs refinement.
- Identify advisors with low acceptance rates and determine whether the issue is action quality, delivery timing, or advisor engagement.
- Use acceptance/rejection data to train ML models that improve action ranking and personalization over time.

### Compliance-Driven Actions
NBA systems serve a dual purpose: enhancing advisor productivity and ensuring compliance-mandated actions are completed on time. Compliance-driven NBA actions differ from discretionary actions in several important ways.

**Examples of compliance-driven NBA actions:**

- Annual suitability review or best-interest review due for a client whose last review was 11 months ago.
- Form CRS delivery required because the firm filed an amended Form CRS and must deliver the updated version to existing clients.
- Best-interest documentation needed for a recent recommendation that lacks the required documentation under Reg BI.
- Account restriction review required — a restricted account (e.g., deceased account holder, legal dispute, regulatory freeze) requires periodic review and cannot be traded until the restriction is resolved.
- Annual privacy notice delivery due under Reg S-P.
- Client identity verification incomplete — CIP documentation gap identified during periodic review.

**Non-dismissible actions.** Unlike discretionary actions (where an advisor can reasonably decide that a referral conversation is not appropriate this week), compliance-driven actions cannot be ignored or permanently dismissed without supervisory override. The system should enforce this:

- Compliance actions cannot be snoozed beyond their regulatory deadline.
- Dismissal of a compliance action requires entry of a reason and supervisor approval.
- Overdue compliance actions are automatically escalated per the escalation rules.

**Audit trail.** All compliance-driven NBA actions must maintain a comprehensive audit trail:

- Timestamp of trigger detection (when the system identified the compliance event).
- Timestamp of action creation (when the recommendation was generated).
- Timestamp of advisor notification (when the recommendation was delivered).
- Advisor response (accepted, deferred with date, escalated).
- Completion timestamp and evidence (meeting notes, signed documents, delivery confirmation).
- Responsible party (the individual who completed the action).
- Supervisor acknowledgment (for escalated or overdue items).

This audit trail serves as evidence of supervisory oversight during regulatory examinations. When an SEC or FINRA examiner asks, "How do you ensure that all clients receive annual reviews?" the firm can produce the NBA compliance log showing trigger dates, notification dates, completion dates, and escalation records for every client.

### Measurement and Optimization
An NBA system that cannot measure its own effectiveness cannot improve. Measurement frameworks should track both operational metrics (is the system working?) and outcome metrics (is the system creating value?).

**Operational metrics:**

- **Action acceptance rate** — What percentage of recommended actions do advisors accept and complete? Benchmark: mature NBA implementations achieve 60-75% acceptance rates. Below 40% suggests the recommendations are not relevant or the delivery is not effective.
- **Time-to-action** — How quickly are accepted actions completed after recommendation? Measure the distribution, not just the average. A median of two days with a long tail of 30+ day completions indicates a queue management problem.
- **Queue utilization** — What percentage of the daily queue capacity (five to seven actions) is being used? Persistent under-utilization suggests insufficient triggers or overly conservative scoring. Persistent over-utilization (advisors consistently receiving more actions than they can complete) suggests the cap needs adjustment or the practice needs additional staff.
- **Trigger accuracy** — What percentage of detected events actually warrant an action? False positive triggers (e.g., flagging a cash deposit that the client has already discussed with the advisor) reduce trust in the system.
- **Compliance completion rate** — What percentage of compliance-driven actions are completed before their deadline? Target: 100% for hard regulatory deadlines, 95%+ for firm-imposed deadlines.

**Outcome metrics:**

- **Revenue impact** — Do clients who receive NBA-driven outreach produce more revenue (through additional assets, planning engagements, or product adoption) than comparable clients who do not? This requires careful measurement with appropriate controls, as NBA-targeted clients may differ systematically from non-targeted clients.
- **Retention impact** — Is the client retention rate higher for clients who receive regular NBA-driven advisor contact? Retention is a lagging indicator, so firms should also track leading indicators like client satisfaction scores and engagement frequency.
- **Advisor productivity** — Are advisors completing more client-facing activities per day/week after NBA implementation? Measure both quantity (number of client interactions) and quality (actions that lead to outcomes vs. check-the-box contacts).

**Continuous improvement:**

- A/B testing — Compare different action templates, delivery times, and nudge formats to identify what drives higher acceptance and completion rates. Run tests within advisor cohorts to control for individual differences.
- Advisor feedback — Collect qualitative input from advisors on action quality, relevance, and timing through periodic surveys and advisory councils. Advisors who feel the system works for them become champions; advisors who feel it works against them become resisters.
- Trigger refinement — Periodically review trigger thresholds and logic. If 80% of drift-triggered rebalancing actions are deferred because the drift is near the threshold but not compelling, the threshold may be too tight. If large-cash-deposit actions are consistently accepted, the system is working well for that trigger type.
- Template refresh — Update action templates (talking points, email drafts, analysis summaries) based on advisor feedback and changing market conditions. Templates that reference outdated market themes or stale data points undermine credibility.

## Worked Examples

### Example 1: Building an NBA engine for a 15-advisor RIA

**Scenario:** A registered investment adviser with 15 advisors collectively managing 1,200 client households ($3.2 billion AUM) is designing its first NBA engine. The firm uses a leading CRM platform, a third-party portfolio management system with custodial data feeds from two custodians, and a financial planning tool. Advisors currently manage their own task lists and rely on periodic (semi-annual or annual) review cycles to identify client needs. The firm wants to shift to a proactive, event-driven engagement model that ensures no high-value action is missed and no compliance deadline is breached.

**Design Considerations:**

The trigger catalog should cover all five event categories, calibrated to the firm's specific thresholds and data availability.

Portfolio triggers: drift beyond 5% absolute deviation from the target model (available daily from the portfolio management system); cash position exceeding 5% of portfolio value for more than 10 business days (from custodial cash balance data); single-position concentration exceeding 12% of portfolio value (from position-level holdings); unrealized tax losses exceeding $5,000 in taxable accounts (from lot-level cost basis data, available from the custodian); RMD due within 90 days (from account type and client date of birth in CRM, cross-referenced with distribution history).

Life event triggers: age milestones at 59.5, 62, 65, 70.5, and 73 (from CRM date of birth, triggered 60 days before the milestone); marriage, divorce, death of spouse, new child (from CRM life event fields, entered by advisors or CSAs during client interactions); retirement or job change (from CRM, typically advisor-reported).

Compliance triggers: annual review overdue (last review date + 365 days, from CRM activity records); client profile update due (last suitability update + 365 days, from CRM); Form ADV delivery required (triggered by firm-level compliance calendar when amendments are filed).

Practice triggers: no client contact in 90 days for Tier 1 clients, 180 days for Tier 2, 365 days for Tier 3 (from CRM activity timestamps); advisory agreement renewal within 60 days (from contract dates in CRM).

Market triggers: sector drawdown exceeding 10% in a 30-day period where the client has more than 15% exposure to the affected sector (from portfolio holdings mapped to sector classifications and market data).

The prioritization scoring model should use four dimensions with firm-specific weights. For this firm — which is growth-oriented but has had compliance findings in the past — suggested weights are: urgency 30%, impact 30%, client importance 25%, effort adjustment -15%. Urgency receives a score of 1-10 based on time sensitivity (10 for same-day compliance deadlines, 1 for opportunities with no expiration). Impact receives a score of 1-10 based on revenue potential, retention risk, and compliance requirement (compliance-mandated actions receive a floor score of 7). Client importance receives a score of 1-10 based on household AUM tier (Tier 1 above $5M = 10, Tier 2 $1-5M = 7, Tier 3 below $1M = 4). Effort receives a negative adjustment of 1-5 reflecting the time required (quick call = -1, comprehensive review = -5), ensuring that the queue does not fill with only time-intensive items.

The daily action queue is capped at six actions per advisor. The system generates the queue at 6:00 AM each morning, drawing from the scored action pool. Queue composition rules ensure variety: no more than two compliance-only items (unless hard deadlines require it), at least one quick-win action (effort score of -1 or -2) to provide a sense of accomplishment, and compliance actions with deadlines within 15 days are always included regardless of other scoring.

A sample morning queue for one advisor managing 85 client households might display:

1. Priority 9.2 — "Margaret Chen (Tier 1, $6.8M): RMD of $48,200 due by Dec 31. No distribution recorded. Contact to confirm distribution method and timing. [View RMD Calculator] [Draft Email]"
2. Priority 8.5 — "David and Susan Park (Tier 1, $5.1M): Portfolio drifted to 74% equity vs. 65% target after tech rally. Propose rebalancing with $18K tax-loss harvest in international fund. [View Drift Report] [Create Proposal]"
3. Priority 7.8 — "Robert Hartley (Tier 2, $2.3M): Turned 65 last week. Discuss Medicare enrollment, supplemental insurance review, and potential retirement income plan update. [View Financial Plan] [Schedule Meeting]"
4. Priority 7.1 — "Compliance: Patricia Alvarez (Tier 2, $1.8M): Annual review overdue by 22 days. Schedule and complete review within 15 days. [Schedule Meeting] [Generate Review Package]"
5. Priority 6.5 — "James O'Brien (Tier 3, $620K): Deposited $85K eight days ago. Cash now 18% of portfolio. Recommend investing per balanced model. [View Account] [Create Proposal]"
6. Priority 5.8 — "Lisa Yamamoto (Tier 2, $3.1M): No contact in 95 days (Tier 2 standard: 90 days). Quick check-in call recommended. [View Recent Activity] [Log Call]"

Delivery is through a dedicated dashboard widget displayed as the advisor's home screen in the CRM, with push notifications reserved for items reaching Priority 9.0+ or compliance deadlines within 48 hours.

The measurement framework tracks: weekly acceptance rate by advisor (target above 65%), average time-to-action (target under 3 business days), compliance action completion rate (target 100% before deadline), and quarterly revenue attribution (comparing AUM growth and planning engagement rates between NBA-active and pre-NBA periods).

### Example 2: Large cash deposit triggers end-to-end NBA workflow

**Scenario:** At 9:15 AM on a Tuesday, the custodial data feed reports that client Thomas Brennan deposited $200,000 into his taxable brokerage account via wire transfer. Thomas is a Tier 1 client ($4.2M total relationship) assigned to advisor Sarah Kim. His investment profile indicates a growth objective with moderate-to-aggressive risk tolerance. His current allocation is 68% equity, 22% fixed income, 10% alternatives — closely aligned with his target model of 70/20/10. The $200K deposit shifts his effective allocation to approximately 60% equity, 19% fixed income, 9% alternatives, and 12% cash.

**Design Considerations:**

The event detection layer should process custodial transaction feeds at least daily (ideally intraday for large-cash triggers). The large-cash-deposit trigger fires when: (a) a cash deposit exceeds $50,000 or 5% of the account value, AND (b) the resulting cash position exceeds the target cash allocation by more than 3 percentage points. In this case, both conditions are met: the $200K deposit exceeds $50,000, and the resulting 12% cash allocation exceeds the 0% target cash position by 12 percentage points.

Context assembly begins immediately after the trigger fires. The system gathers: (1) Thomas's investment profile from CRM — growth objective, moderate-to-aggressive risk, 15+ year time horizon, high marginal tax bracket (37% federal); (2) current portfolio composition from the portfolio management system — position-level holdings, model assignment, drift analysis showing the portfolio is now 10 percentage points underweight equity due to cash dilution; (3) financial plan status from the planning tool — retirement plan is 88% funded with current contributions, and investing the $200K would increase the funded status to approximately 93%; (4) tax situation — the taxable account has $14,000 in unrealized short-term losses in an international equity ETF and $32,000 in unrealized long-term gains in a large-cap growth fund, suggesting tax-lot-level attention during investment; (5) recent interactions from CRM — Sarah spoke with Thomas 12 days ago about a general portfolio check-in, no mention of an incoming deposit, suggesting this may be an inheritance, bonus, real estate proceeds, or other liquidity event that Sarah should understand before investing.

Action recommendation: the system recommends "Invest Large Cash Position Per Growth Model with Tax-Lot Optimization." The action template includes: talking points for Sarah's call to Thomas (congratulate/inquire about the source of funds, recommend investing per his growth model to bring allocation back to target, note the opportunity to harvest the $14K international equity loss while redeploying, explain that the investment will improve his retirement plan funded status from 88% to approximately 93%); a pre-generated trade proposal showing the specific purchases needed to restore target allocation (approximately $140K to equities across three funds, $40K to fixed income, $20K to alternatives, with tax-lot selection optimized to harvest losses); and a draft email for Thomas summarizing the recommendation.

Advisor notification: Sarah receives a push notification at 9:45 AM (within 30 minutes of the trigger event, reflecting the high priority of a large cash deposit): "Thomas Brennan deposited $200K. Portfolio now 12% cash vs. 0% target. Recommend investing per growth model. Est. tax-loss harvest: $14K. [View Proposal] [Call Thomas]." The action also appears as the top item in Sarah's morning dashboard queue with a Priority score of 8.9 (high urgency due to uninvested cash, high impact due to Tier 1 client and plan improvement, moderate effort for the call and trade execution).

Execution workflow: Sarah taps "Call Thomas" to initiate the call. During the conversation, she learns the $200K is the proceeds from selling a rental property — useful context for tax planning (Thomas may have capital gains from the property sale that the international equity losses could offset). Sarah then taps "View Proposal" to review the pre-generated trade proposal, makes a minor adjustment (increasing the international equity allocation slightly to improve diversification), and submits the trades through the order management system with the tax-lot selection preserving the loss-harvesting opportunity.

Action completion logging: when the trades are executed, the system automatically logs the completed action in CRM: trigger event (large cash deposit, $200K, detected 9:15 AM), advisor notification (9:45 AM), advisor action (accepted, called client at 10:20 AM, 18-minute call), trades submitted (10:45 AM), trades executed (11:02 AM), outcome (portfolio restored to target allocation, $14K tax loss harvested, client expressed satisfaction). The entire workflow — from cash deposit to invested portfolio — completed in under two hours.

### Example 3: Compliance-driven NBA for annual review completion

**Scenario:** A wealth management firm with 400 client households has a compliance policy requiring that every client receive a documented annual review. The firm's last FINRA examination cited a deficiency: 23% of clients had not received an annual review within the required 12-month window. The CCO is implementing a compliance-driven NBA workflow to ensure 100% annual review completion and provide auditable evidence of supervisory oversight.

**Design Considerations:**

The trigger logic uses a simple but reliable date calculation: for each client, the system compares the date of the last documented annual review (stored in CRM as a completed activity of type "Annual Review") to the current date. The trigger fires at three escalation points:

- 60-day advance notice: when (current date + 60 days) exceeds (last review date + 365 days), the system generates a "Schedule Annual Review" action. This gives the advisor two months to schedule and complete the review before the deadline. Priority score: 5.0 (moderate urgency, mandatory compliance item, standard effort).
- 30-day warning: when (current date + 30 days) exceeds (last review date + 365 days) and no review has been scheduled, the system escalates the action. The priority score increases to 7.5, the dashboard displays the item in amber, and the advisor receives a direct notification: "Annual review for [Client Name] due in 30 days. Schedule immediately. [Schedule Meeting] [Generate Review Package]."
- 15-day alert: when (current date + 15 days) exceeds (last review date + 365 days) and no review has been scheduled or conducted, the system escalates further. Priority score increases to 9.0, the dashboard displays the item in red, the advisor and the advisor's supervisor both receive notifications, and the action becomes non-deferrable. The notification to the supervisor reads: "[Advisor Name] has an annual review for [Client Name] due in 15 days — not yet scheduled. Supervisor action required."
- Overdue escalation: when the current date exceeds (last review date + 365 days) and no review has been completed, the system logs a compliance exception and notifies the Chief Compliance Officer. The CCO notification includes: client name, advisor name, original deadline, days overdue, and all prior escalation timestamps. The CCO can assign the review to another advisor, require a written explanation from the responsible advisor, or take other supervisory action.

Scheduling automation: when the advisor clicks "Schedule Meeting" from the NBA recommendation, the system should: (1) display the client's preferred meeting times and communication method from CRM; (2) cross-reference the advisor's calendar to identify available slots within the next 14 days; (3) generate a meeting invitation with a pre-built annual review agenda template; (4) upon client confirmation, automatically update the CRM with the scheduled review date and change the NBA action status to "Scheduled — Awaiting Completion."

Review preparation package generation: when a review meeting is scheduled, the system automatically generates a preparation package that includes: (a) a portfolio summary report showing current allocation, performance since last review, benchmark comparison, and drift analysis; (b) a financial plan update showing current funded status, progress toward goals, and any assumption changes needed; (c) a client profile summary showing demographic information, investment profile, risk tolerance, and any profile changes since the last review; (d) a compliance checklist covering suitability confirmation, beneficiary verification, contact information update, disclosure delivery status, and any outstanding action items from the prior review; (e) a list of all NBA-recommended actions taken for this client since the last annual review, demonstrating the ongoing service provided between reviews.

Completion tracking and compliance reporting: the review is not marked as complete until the advisor records the review activity in CRM with required fields: meeting date, attendees, topics discussed, any changes to the client profile or investment strategy, next steps, and confirmation that the suitability/best-interest review was conducted. The system validates that all required fields are populated before closing the action.

The compliance reporting dashboard provides the CCO with real-time visibility into: total clients with current annual reviews (target: 100%), clients with reviews due within 30 days (action required), clients with overdue reviews (compliance exceptions), completion rate by advisor (identifying advisors who consistently lag), and a historical trend chart showing the firm's review completion rate month-over-month.

For the FINRA examination response, the firm can produce: a system-generated report showing the trigger date, all escalation timestamps, scheduling date, completion date, and review documentation for every client — demonstrating that the firm has implemented a systematic, automated supervisory process that ensures annual review completion. This directly addresses the prior deficiency finding and demonstrates the "reasonably designed" supervisory system that FINRA expects under Rule 3110.

## Common Pitfalls
- Generating too many actions per advisor per day, causing action fatigue and system abandonment — cap daily queues at five to seven items and invest in prioritization quality over trigger quantity.
- Implementing NBA as a standalone system disconnected from the CRM, portfolio management, and financial planning tools — if advisors must check a separate system, adoption will fail; NBA must integrate into existing workflows.
- Relying entirely on rule-based logic without incorporating advisor feedback — rules that generate irrelevant or poorly timed recommendations erode trust; build feedback mechanisms from day one.
- Treating all actions as equal priority — without a robust scoring model, compliance deadlines, revenue opportunities, and routine touchpoints compete for the same queue positions, and important items get buried.
- Designing nudges that lack client-specific context — a generic "Contact this client" recommendation provides no value; nudges must include the trigger reason, relevant data, and a specific recommended action.
- Failing to connect NBA recommendations to execution workflows — if clicking "Propose Rebalancing" merely creates a reminder rather than opening the rebalancing tool with the client's data pre-loaded, the system adds overhead instead of reducing it.
- Making compliance-driven actions dismissible without supervisory oversight — compliance items must be non-deferrable past their regulatory deadline, with escalation to supervisors and the CCO.
- Not tracking action outcomes (acceptance, completion, client response) — without outcome data, the system cannot improve, and the firm cannot measure the return on its NBA investment.
- Ignoring advisor capacity when generating queues — recommending seven complex actions on a day when the advisor has six hours of meetings is counterproductive.
- Deploying the system without advisor input on trigger thresholds, action templates, and delivery preferences — top-down implementation without advisor buy-in consistently produces low adoption rates.
- Omitting the audit trail for compliance-driven actions — the entire compliance value of NBA depends on the ability to produce timestamped, complete records during regulatory examinations.
- Allowing the action library to become stale — talking points referencing outdated market conditions, email templates with old branding, or analysis summaries using last year's data undermine the system's credibility.

## Cross-References
- **crm-client-lifecycle** (Layer 10, advisory-practice) — CRM activity records, client segmentation, and lifecycle data are primary inputs for NBA triggers; every NBA action updates the CRM.
- **portfolio-management-systems** (Layer 10, advisory-practice) — Portfolio events (drift, cash position, concentrated holdings, performance) are a primary category of NBA triggers; the portfolio management system provides the data feeds and execution tools.
- **advisor-dashboards** (Layer 10, advisory-practice) — The advisor dashboard is the primary delivery channel for NBA recommendations; the morning briefing widget displays the prioritized action queue.
- **financial-planning-integration** (Layer 10, advisory-practice) — Financial plan status changes (goal progress, funded status, assumption changes) trigger planning-related NBA actions; plan data enriches action context.
- **rebalancing** (Layer 4, wealth-management) — Portfolio drift and rebalancing triggers are a key category of NBA events; the NBA recommendation links directly to the rebalancing workflow.
- **tax-efficiency** (Layer 5, wealth-management) — Tax-loss harvesting opportunities detected from cost basis data trigger NBA recommendations; tax context (gain/loss position, holding periods) enriches rebalancing and investment actions.
- **investment-suitability** (Layer 9, compliance) — Annual suitability reviews and profile re-certifications are compliance-driven NBA actions; suitability data informs the client context assembled for all NBA recommendations.
- **examination-readiness** (Layer 9, compliance) — NBA compliance action logs (trigger timestamps, escalation records, completion evidence) serve as auditable proof of supervisory oversight during SEC and FINRA examinations.
