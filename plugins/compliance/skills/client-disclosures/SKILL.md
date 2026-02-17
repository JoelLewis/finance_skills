---
name: client-disclosures
description: "Client disclosure documents: Form ADV, Form CRS, prospectus delivery, Reg S-P privacy, trade confirmations, account statements, delivery timing."
allowed-tools: ["Bash", "Read", "Write", "Edit"]
---

# Client Disclosures

## Purpose
Guide the understanding of disclosure document requirements — what documents must exist, what they must contain, and when they must be delivered. This skill covers Form ADV, Form CRS, prospectus obligations, privacy notices, trade confirmations, account statements, and delivery methods — enabling a user or agent to design compliant disclosure workflows.

## Layer
9 — Compliance & Regulatory Guidance

## Direction
prospective

## When to Use
- Designing client onboarding workflows that include required document delivery
- Reviewing Form ADV Part 2A content for completeness
- Implementing Form CRS delivery and filing requirements
- Building prospectus delivery tracking systems
- Establishing privacy notice delivery and opt-out processes
- Ensuring timely trade confirmation delivery
- Designing account statement generation and distribution
- Evaluating electronic vs paper delivery compliance
- Establishing document retention and delivery audit trails

## Core Concepts

### Form ADV Part 1
Filed electronically via IARD (Investment Adviser Registration Depository). Contains:
- Registration information (SEC, states)
- Form of organization, control persons, and ownership
- Disciplinary history (criminal, regulatory, civil)
- Other business activities and financial industry affiliations
- Custody of client assets
- Participation in client transactions
- AUM and number of clients

Part 1 is publicly available through the SEC's Investment Adviser Public Disclosure (IAPD) website. It is not delivered to clients but is a regulatory filing that must be kept current (annual updating amendment within 90 days of fiscal year end, interim amendments for material changes).

### Form ADV Part 2A (Firm Brochure)
The primary disclosure document for RIAs. Must contain 18 items:
1. Cover page
2. Material changes summary (annual update)
3. Table of contents
4. Advisory business description
5. **Fees and compensation** (see fee-disclosure skill)
6. Performance-based fees (if applicable)
7. Types of clients
8. Methods of analysis, investment strategies, and risk of loss
9. Disciplinary information
10. Other financial industry activities and affiliations
11. Code of ethics, participation in client transactions, personal trading
12. Brokerage practices (best execution, soft dollars, directed brokerage)
13. Review of accounts (frequency, triggers, reviewer qualifications)
14. Client referrals and other compensation
15. Custody
16. Investment discretion
17. Voting client securities (proxy voting)
18. Financial information (balance sheet if prepaid fees or custody)

**Delivery requirements:** Initial delivery to prospective clients before or at the time of entering the advisory contract. Annual offer to deliver updated brochure (or delivery of a summary of material changes with an offer to provide the full brochure) within 120 days of fiscal year end. Interim delivery required for material changes that clients should know about.

### Form ADV Part 2B (Brochure Supplement)
Provides information about specific supervised persons who provide investment advice:
- Educational background and business experience
- Disciplinary information
- Other business activities
- Additional compensation (from non-clients)
- Supervision structure

Delivered to clients before or at the time the supervised person begins providing advice. Updated for material changes.

### Form CRS (Client Relationship Summary)
Required for both RIAs and BDs. Maximum 2 pages (4 for dual registrants). Must follow SEC-prescribed format with specific headings and conversation starters:

**Required sections:**
1. **Introduction** — firm name, registration status (IA, BD, or both), statement that brokerage and advisory services differ
2. **Relationships and Services** — description of principal services, monitoring, investment authority, limited product offerings, account minimums
3. **Fees, Costs, Conflicts, and Standard of Conduct** — principal fees, other costs, conflicts, applicable standard of conduct (Reg BI for BDs, fiduciary for IAs)
4. **Disciplinary History** — yes/no question with link to Investor.gov
5. **Additional Information** — how to find more information, who to contact

**Delivery timing:**
- Before or at the earliest of: (a) entering an advisory or brokerage agreement, (b) opening an account, or (c) making a recommendation of account type, security, or investment strategy
- When opening a new account that is different from existing accounts
- When recommending a rollover from a retirement account
- Upon request
- File with SEC via IARD/CRD

### Prospectus and SAI Delivery
**Mutual funds:** Summary prospectus must be delivered at or before the time of sale (point of sale delivery). The summary prospectus must provide access to the full statutory prospectus and SAI (online or upon request).

**ETFs:** No point-of-sale prospectus delivery is required for exchange-traded transactions (SEC Rule 498). However, the prospectus must be available online, and a paper copy must be delivered upon request within 3 business days.

**New issues (IPOs):** Prospectus must be delivered before or with the confirmation of sale.

**Statement of Additional Information (SAI):** Not routinely delivered but must be available upon request. Contains additional detail on investment policies, portfolio turnover, taxation, financial statements, and fund governance.

### Regulation S-P (Privacy Notices)
Regulation S-P (17 CFR Part 248) requires financial institutions to protect customer nonpublic personal information (NPI):

- **Initial privacy notice** — delivered at account opening; describes information collected, information shared, opt-out rights, and security practices
- **Annual privacy notice** — historically required annually; the FAST Act (2015) created an exception: firms with unchanged privacy practices that do not share NPI (other than with permitted exceptions) may post privacy notices online instead of mailing them annually
- **Opt-out notice** — if the firm shares NPI with nonaffiliated third parties (beyond permitted exceptions), customers must be given a reasonable opportunity to opt out before sharing
- **Safeguards rule** — requires written policies and procedures to protect customer information, including administrative, technical, and physical safeguards

### Trade Confirmations
SEC Rule 10b-10 requires broker-dealers to send trade confirmations to customers at or before completion of each transaction:

**Required content:**
- Date of transaction
- Identity, price, and number of shares or units
- Whether the firm acted as principal or agent
- If agent: commission and source of commission
- If principal: markup/markdown (for certain transactions)
- Market where the transaction was effected
- Accrued interest (for fixed income)
- Settlement date

**Timing:** At or before the completion of the transaction. For most equity transactions, this means at or before T+1 settlement.

### Account Statements
FINRA Rule 2231 governs customer account statements:
- **Frequency:** At least quarterly for accounts with activity or positions; at least annually for accounts with positions but no activity in the quarter
- **Content:** Account positions, market values, account activity during the period, balances
- **Valuations:** Securities must be valued at current market prices or, if unavailable, at estimated fair value with appropriate disclaimers
- **Direct mailing:** Must be sent directly to the customer address of record (or electronic delivery address); may not be routed through the registered representative

### Proxy Voting Disclosure
SEC Rule 206(4)-6 requires registered investment advisers that exercise proxy voting authority to:
- Adopt written proxy voting policies and procedures
- Disclose to clients how they can obtain information about proxy voting policies and how votes were cast
- Maintain records of proxy voting (at least 5 years from the end of the fiscal year in which the record was created)

### Electronic Delivery
SEC guidance permits electronic delivery of disclosure documents if:
- **Consent:** The customer affirmatively consents to electronic delivery (for certain documents) or the firm ensures actual receipt (e.g., via email with access confirmation)
- **Access equals delivery:** For prospectuses and certain other documents, making the document available on a website with notice to the customer may satisfy delivery requirements
- **Format:** Documents must be delivered in a format the customer can access, read, and retain
- **Paper backup:** Customers must retain the right to request paper delivery at any time

Firms must maintain records of electronic delivery consent and have systems to track document access.

### Delivery Timing Summary

| Document | Trigger | Timing |
|----------|---------|--------|
| Form ADV Part 2A | New advisory relationship | Before or at entering advisory contract |
| Form ADV Part 2A (annual) | Fiscal year end | Within 120 days |
| Form ADV Part 2B | New supervised person | Before advice begins |
| Form CRS | New relationship / recommendation | Before or at earliest trigger event |
| Prospectus (mutual fund) | Purchase | At or before point of sale |
| Prospectus (ETF) | Request | Within 3 business days of request |
| Privacy notice (initial) | Account opening | At account opening |
| Privacy notice (annual) | Annual cycle | Once per 12-month period (if required) |
| Trade confirmation | Trade execution | At or before completion of transaction |
| Account statement | Quarterly / annually | Per FINRA Rule 2231 schedule |

## Worked Examples

### Example 1: RIA failing to deliver Form CRS at the right time
**Scenario:** A newly registered RIA firm begins taking on clients. The firm delivers Form ADV Part 2A during onboarding but does not file or deliver Form CRS, believing it is only required for broker-dealers. The firm signs advisory agreements with 50 clients over six months before discovering the oversight.
**Compliance Issues:** Form CRS is required for both RIAs and BDs. The firm has violated the delivery requirement for all 50 clients and has also failed to file the form with the SEC via IARD. This is a material compliance deficiency that would likely be identified in an SEC examination.
**Analysis:** The firm must immediately: (1) draft a Form CRS compliant with SEC format requirements, (2) file it with the SEC via IARD, (3) deliver it to all existing clients, and (4) implement procedures to ensure delivery at the required trigger points going forward. The firm should consider disclosing the lapse to its CCO and potentially to the SEC if the deficiency is material. The 50 advisory agreements remain valid but the disclosure deficiency exposes the firm to regulatory action.

### Example 2: Relying on annual ADV delivery exception incorrectly
**Scenario:** An RIA updated its fee schedule mid-year, increasing advisory fees by 25 basis points for new clients. The firm also began offering a new service (financial planning) and added two new supervised persons. The firm does not distribute an updated brochure or summary of material changes, planning to address all changes in the next annual ADV delivery.
**Compliance Issues:** Material changes require interim delivery, not just annual updates. A 25 bps fee increase, addition of a new service, and new supervised persons providing advice are all material changes. Waiting until the annual update cycle delays required disclosure.
**Analysis:** The firm must: (1) file an amended Form ADV promptly with the SEC, (2) deliver a summary of material changes or an updated brochure to existing clients who are affected, (3) deliver Part 2B supplements for the new supervised persons to clients they advise, and (4) ensure new clients receive the updated documents before entering into advisory agreements. The annual delivery obligation supplements — but does not replace — the interim delivery requirement for material changes.

### Example 3: BD not providing timely trade confirmations for fixed income
**Scenario:** A broker-dealer's back-office system delays trade confirmations for fixed-income transactions by 5-7 business days after settlement due to a systems processing bottleneck. Equity confirmations are sent on trade date. The delay affects approximately 2,000 fixed-income transactions per quarter.
**Compliance Issues:** SEC Rule 10b-10 requires confirmations at or before completion of the transaction. A 5-7 day delay after settlement is a clear violation. Fixed-income confirmations must include accrued interest calculations, which may explain the processing delay, but the regulatory requirement does not accommodate systems limitations.
**Analysis:** The firm must: (1) remediate the systems bottleneck to ensure timely confirmation delivery, (2) review the scope of the issue (how many clients affected, over what period), (3) consider filing a FINRA rule violation with compliance, (4) assess whether the delay caused client harm (e.g., inability to identify errors or unauthorized trades in a timely manner), and (5) implement monitoring to prevent recurrence. Firms should prioritize confirmation delivery systems for all asset classes, not just equities.

## Common Pitfalls
- Delivering Form ADV but forgetting Form CRS (or vice versa)
- Not filing Form CRS with the SEC — it must be both filed and delivered
- Treating annual ADV delivery as a substitute for interim material change delivery
- Failing to deliver Part 2B supplements when a new supervised person begins advising existing clients
- Assuming all electronic delivery is permissible without proper consent or access verification
- Not maintaining records of document delivery (dates, methods, versions delivered)
- Providing privacy notices that satisfy the letter of Reg S-P but do not actually explain the firm's information sharing practices clearly
- Delaying trade confirmations due to systems issues without recognizing the regulatory requirement for timely delivery
- Not updating delivery procedures when regulations change (e.g., Form CRS rollover delivery requirement)
- Sending account statements through the registered representative rather than directly to the customer

## Cross-References
- **fee-disclosure** (Layer 9): Form ADV Item 5 and Form CRS fee section are key fee disclosure vehicles
- **reg-bi** (Layer 9): Reg BI Disclosure Obligation drives much of the BD disclosure framework
- **fiduciary-standards** (Layer 9): Full and fair disclosure is a core fiduciary obligation; Form ADV is the primary vehicle
- **conflicts-of-interest** (Layer 9): Conflict disclosure is embedded throughout Form ADV, Form CRS, and Reg BI disclosures
- **advertising-compliance** (Layer 9): Marketing materials must be consistent with disclosure documents
