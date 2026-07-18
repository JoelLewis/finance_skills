---
name: account-opening-workflow
description: "Design and operate back-office account opening pipelines from application intake through custodian submission and activation. Use when building account opening automation, reducing NIGO rejection rates from custodians or clearing firms, defining document requirements for trusts, entities, IRAs, or estate accounts, setting up multi-custodian account opening across Schwab, Fidelity, or Pershing, troubleshooting account opening failures or processing delays, or benchmarking cycle times and first-submission acceptance rates. For risk-based approval tiers and compliance screening requirements, see account-opening-compliance."
---

# Account Opening Workflow

## Core Concepts

### Account Type Determination and Registration
Account type determination is the foundational decision in the account opening workflow. The registration type dictates the document requirements, approval gates, tax treatment, titling rules, and custodian submission path. Operations teams must maintain a comprehensive account type matrix that maps each registration type to its downstream processing requirements.

**Individual and joint registration types:**
- **Individual** — single natural person as owner; titled in the individual's legal name; SSN as TIN; simplest registration and the baseline for all account opening processes
- **Joint Tenants with Right of Survivorship (JTWROS)** — two or more co-owners with equal, undivided interest; on death of one owner, the surviving owner(s) automatically inherit the deceased owner's share without probate; all owners must sign account opening documents; titled as "John Smith and Jane Smith JTWROS"
- **Tenants in Common (TIC)** — two or more co-owners with specified ownership percentages (need not be equal); on death, the deceased owner's share passes to their estate, not to the surviving co-owner(s); ownership percentages must be recorded and may affect tax reporting; titled as "John Smith and Jane Smith TIC"
- **Community Property** — available only in community property states (Arizona, California, Idaho, Louisiana, Nevada, New Mexico, Texas, Washington, Wisconsin); assets acquired during marriage are jointly owned; specific titling and tax implications vary by state; some custodians treat community property accounts differently from other joint account types
- **Community Property with Right of Survivorship** — a hybrid available in some community property states that combines community property tax treatment with automatic survivorship; not all custodians support this registration type

**Trust registration types:**
- **Revocable (living) trust** — grantor retains control and can modify or revoke the trust; typically titled as "John Smith, Trustee of the Smith Family Trust dated 01/15/2020"; grantor's SSN is often used as TIN; account opening requires trust certification or relevant pages of the trust agreement showing trust name, date, trustees, and investment powers
- **Irrevocable trust** — grantor has permanently relinquished control; separate tax entity requiring its own EIN; beneficial ownership certification required under FinCEN CDD Rule; titled in the trust's legal name with trustee designation; requires more extensive documentation including the full trust agreement or comprehensive trust certification
- **Testamentary trust** — created by a will and comes into existence upon the grantor's death; requires letters testamentary, death certificate, and court-certified copy of the will provisions creating the trust; account opening is typically manual due to the complexity and variation in court documentation

**Entity registration types:**
- **LLC (Limited Liability Company)** — requires articles of organization, operating agreement (or certificate of formation in some states), EIN, beneficial ownership certification; titled in the LLC's legal name; operating agreement must authorize the opening of investment accounts and identify authorized signers
- **Corporation (C-Corp and S-Corp)** — requires articles of incorporation, bylaws, corporate resolution authorizing the account and designating authorized signers, EIN, beneficial ownership certification; S-Corp election (IRS Form 2553) may be relevant for tax reporting but does not change account opening requirements
- **Partnership (General Partnership, Limited Partnership, LLP)** — requires partnership agreement, EIN, identification of general partner(s) who have authority to act on behalf of the partnership; limited partners typically do not have signing authority unless specified in the partnership agreement
- **Sole Proprietorship** — may use the individual's SSN or a separate EIN; requires DBA documentation if operating under a trade name; some custodians treat sole proprietorship accounts as individual accounts with a DBA designation

**Retirement account types:**
- **Traditional IRA** — tax-deductible contributions (subject to income limits if the owner participates in an employer plan), tax-deferred growth, required minimum distributions beginning at age 73 (SECURE 2.0; rises to 75 in 2033); requires IRA adoption agreement, beneficiary designation, and IRA disclosure statement
- **Roth IRA** — after-tax contributions, tax-free qualified distributions, no RMDs during the owner's lifetime; same documentation requirements as Traditional IRA plus verification of Roth eligibility (income limits)
- **SEP IRA** — employer-funded; contributions up to 25% of compensation or the annual dollar limit; requires SEP plan document (IRS Form 5305-SEP or prototype plan) and IRA adoption agreement; employer must execute the plan document before the account can be opened
- **SIMPLE IRA** — salary deferral plus employer match or non-elective contribution; requires SIMPLE plan document (IRS Form 5304-SIMPLE or 5305-SIMPLE) and SIMPLE IRA adoption agreement; must be established between January 1 and October 1 of the plan year
- **Inherited IRA** — beneficiary account established upon the death of the original IRA owner; subject to the 10-year distribution rule for most non-spouse beneficiaries under the SECURE Act; requires death certificate, beneficiary verification, and custodian-specific inherited IRA application; titled as "Jane Smith, Beneficiary of John Smith, Deceased"
- **Rollover IRA** — receives funds from an employer-sponsored plan (401(k), 403(b), 457); may be direct rollover (trustee-to-trustee) or indirect rollover (60-day); requires rollover paperwork and often a letter of acceptance from the receiving custodian

**Custodial and estate accounts:**
- **UTMA/UGMA** — custodian (typically a parent or grandparent) manages assets for a minor until the age of majority (18 or 21 depending on state and UTMA vs UGMA); the minor is the beneficial owner and the account is titled in the minor's SSN; titled as "John Smith, Custodian for Jane Smith under the [State] UTMA"
- **Estate** — opened to manage assets of a deceased person during probate; requires letters testamentary (if there is a will) or letters of administration (if intestate), death certificate, and EIN for the estate; titled as "Estate of John Smith, Deceased"; personal representative or executor is the authorized signer

**Account numbering and classification:**
- Account numbers are assigned by the custodian or clearing firm upon successful account creation; the firm's internal systems may maintain a separate internal account identifier that maps to the custodian account number
- Account classification codes are used for regulatory reporting (Form 13F, FOCUS reports, customer protection rule computations); classification must accurately reflect the account type, tax status, and beneficial ownership
- Multi-custodian firms must maintain a cross-reference between internal account identifiers and custodian-specific account numbers
- Account numbering schemes at custodians typically encode the account type, branch, or registration category within the number structure; operations teams should understand each custodian's numbering conventions for troubleshooting and reconciliation

### Document Requirements Matrix
The document requirements matrix is the operational backbone of account opening. It defines exactly which documents are required for each combination of account type, account features, and custodian. A well-maintained matrix prevents NIGO rejections, ensures regulatory compliance, and enables automation.

**Universal documents (required for all account types):**
- New account application form (custodian-specific; each custodian has its own form with different fields and formatting)
- W-9 (Request for Taxpayer Identification Number) for US persons, or W-8BEN (individuals) / W-8BEN-E (entities) for non-US persons
- Advisory agreement (for advisory accounts) or brokerage agreement (for brokerage accounts)
- Form CRS (Client Relationship Summary) — delivery acknowledgment
- Privacy notice (Regulation S-P) — delivery acknowledgment
- Trusted contact person designation (FINRA Rule 4512)

**Type-specific documents:**
- Joint accounts: joint account agreement specifying the ownership type (JTWROS, TIC, community property); signatures of all account holders
- Trust accounts: trust certification (or relevant pages of the trust agreement) showing trust name, date of formation, trustee names and powers, successor trustee provisions, and investment authority; trust EIN (irrevocable trusts); beneficial ownership certification (irrevocable trusts and certain revocable trusts depending on the custodian)
- Entity accounts: formation documents (articles of incorporation/organization, partnership agreement), governing documents (bylaws, operating agreement), authorizing resolution (corporate resolution, LLC member resolution, or partner authorization designating authorized signers and authorizing the account), EIN assignment letter, beneficial ownership certification form (FinCEN)
- IRA accounts: IRA adoption agreement, beneficiary designation form (primary and contingent beneficiaries), IRA disclosure statement, transfer/rollover forms (if funding from another retirement account or employer plan)
- Estate accounts: letters testamentary or letters of administration (court-certified), death certificate, EIN assignment letter for the estate, court order appointing the personal representative or executor
- Custodial accounts (UTMA/UGMA): custodial account agreement, minor's SSN, custodian's identification

**Feature-specific documents:**
- Margin: margin agreement, margin risk disclosure document; some custodians require a separate margin application
- Options: options agreement, OCC Characteristics and Risks of Standardized Options document acknowledgment; options approval level must be specified and may require additional documentation for higher levels
- Check writing and debit card: separate application for cash management features
- Discretionary authority: limited power of attorney or discretionary trading authorization signed by the client; investment advisory agreement with discretionary language

**Custodian-specific variations:**
Each custodian maintains its own form library, field requirements, and validation rules. The operations team must maintain custodian-specific document matrices and update them when custodians revise their requirements. Common variations include: different account application forms, different signature requirements (e.g., one custodian requires a separate signature page while another accepts signatures on the application), different beneficial ownership forms, and different trust certification formats. Failure to track custodian-specific variations is a major source of NIGO rejections.

### Application Processing Workflow
The application processing workflow is the sequence of steps from initial receipt of account opening request through account number assignment and confirmation. A well-designed workflow manages state transitions, enforces required gates, and provides visibility to all stakeholders.

**Workflow stages:**

1. **Receipt and intake** — the account opening request arrives from the advisor (via onboarding platform, CRM, email, or paper). The operations team logs the request, assigns it a tracking number, and records the timestamp. For firms with service-level agreements, the clock starts here.

2. **Initial review and triage** — an operations analyst reviews the request for completeness at a high level: is the account type clear, are the basic client details present, are the required documents attached. Requests are triaged by complexity: standard accounts (individual, joint, IRA) go to the automated or streamlined path; complex accounts (trusts, entities, estates) go to a specialized review queue.

3. **Data entry or import** — client data is entered into the firm's account opening system or imported from the onboarding platform. For API-integrated onboarding, this step is automated. For manual submissions, operations staff key in client information from the application forms. Data entry is a significant source of errors; validation rules should flag inconsistencies in real time.

4. **Document completeness check** — the operations analyst verifies that all required documents are present based on the document requirements matrix. This is a systematic, checklist-driven review: for the given account type plus features plus custodian, are all required documents attached, signed, and complete. Missing or incomplete documents trigger a NIGO hold and a request back to the advisor or client.

5. **Data validation** — automated and manual checks verify data consistency across all documents: name matches between application, W-9, and advisory agreement; SSN/EIN matches across forms; account type coding is consistent; address is complete and formatted correctly; beneficiary designations are complete for retirement accounts. Validation rules should be codified and automated wherever possible.

6. **Supervisory review** — certain account types and configurations require supervisory or compliance review before custodian submission. Triggers include: discretionary accounts, options trading approval, margin requests, accounts for senior investors (age 65+), PEP or EDD-flagged clients, high-net-worth thresholds, accounts with complex ownership structures. The supervisor reviews the application package, suitability documentation, and any compliance flags, then approves, rejects, or requests additional information.

7. **Custodian submission** — the validated and approved application package is submitted to the custodian via API, custodian portal, or manual upload. API submission is the target for standard account types; complex accounts often require portal or manual submission. The operations team records the submission timestamp and method.

8. **Custodian processing and account number assignment** — the custodian reviews the submission, runs its own validation, and either creates the account (returning an account number) or rejects it (NIGO). Processing time varies: API submissions for standard accounts may return an account number within minutes; manual submissions for complex accounts may take days to weeks. The operations team monitors submission status and follows up on aging submissions.

9. **Confirmation and notification** — upon receiving the account number, the operations team updates internal systems (CRM, PMS, billing), notifies the advisor and client, and triggers post-opening activities (funding, model assignment, welcome kit). The confirmation should include the account number, registration details, and any next steps required from the advisor or client.

**Workflow state management:**
Each account opening request should have a defined state at all times: received, in-review, pending-documents, pending-supervisory-review, pending-compliance, submitted-to-custodian, NIGO-hold, approved, activated, or closed/withdrawn. State transitions should be logged with timestamps, responsible party, and any notes. A dashboard showing the distribution of requests across states enables operations management to identify bottlenecks, aging items, and capacity issues.

### NIGO Management
NIGO (Not In Good Order) rejections are the single largest source of delay, cost, and client dissatisfaction in account opening operations. A systematic approach to NIGO management includes prevention, categorization, remediation, tracking, and root cause analysis.

**Common NIGO causes and prevention strategies:**
- **Missing signatures** (typically 20-30% of NIGOs) — prevented by automated signature detection in document review, e-signature platforms that enforce all signature blocks before completion, and pre-submission validation that checks for blank signature fields
- **Data inconsistencies** (15-25%) — name on W-9 does not match account application; address differs between forms; SSN/EIN mismatch. Prevented by single-entry data collection that propagates to all forms, and cross-document validation rules
- **Missing documents** (15-20%) — trust certification not included for trust account; beneficial ownership form missing for entity; beneficiary designation missing for IRA. Prevented by the document requirements matrix with automated checklists that block submission until all required documents are present
- **Incorrect account type coding** (10-15%) — the account type on the application does not match the registration details or the custodian's account type codes. Prevented by mapping tables between the firm's account types and each custodian's type codes, with validation at submission
- **Incomplete beneficiary designations** (5-10%) — missing contingent beneficiaries, percentages that do not sum to 100%, missing beneficiary SSNs for retirement accounts. Prevented by beneficiary form validation rules
- **Expired or invalid identity documents** (5-10%) — government ID has expired, W-8BEN has passed its three-year validity period. Prevented by document expiration tracking and pre-submission date validation
- **Missing beneficial ownership** (5-10%) — entity accounts submitted without the FinCEN beneficial ownership certification. Prevented by requiring the form as a mandatory document for all entity account types

**NIGO categorization:**
NIGOs should be categorized by: (1) custodian — to identify custodian-specific patterns, (2) rejection reason — using a standardized taxonomy of NIGO codes, (3) account type — to identify which account types have the highest rejection rates, (4) originating advisor or office — to identify training needs, (5) severity — distinguishing between minor corrections (e.g., missing initials) and substantive deficiencies (e.g., missing trust agreement). This categorization enables targeted remediation and process improvement.

**Remediation workflows:**
When a NIGO is received: (1) the operations team logs the rejection, categorizes it, and assigns it to an analyst; (2) the analyst determines the specific corrective action required; (3) if the correction can be made by operations (e.g., re-keying a data field), it is corrected and resubmitted; (4) if the correction requires the advisor or client (e.g., a missing signature, an additional document), the analyst contacts the advisor with a clear, specific request describing exactly what is needed; (5) a follow-up schedule is established (e.g., 2-day follow-up, 5-day escalation to the advisor's manager, 10-day escalation to operations management); (6) once the correction is received, the application is revalidated and resubmitted; (7) the NIGO is closed and the resolution is recorded.

**NIGO tracking and reporting:**
- **NIGO rate** — total NIGO rejections divided by total submissions, measured weekly and monthly; segmented by custodian, account type, and advisor/office
- **NIGO aging** — average time from NIGO receipt to resolution; distribution of open NIGOs by age (0-2 days, 3-5 days, 6-10 days, 10+ days)
- **First-submission acceptance rate** — the inverse of the NIGO rate; the percentage of applications accepted on first submission
- **Root cause distribution** — the percentage of NIGOs attributable to each cause category, tracked over time to measure the effectiveness of prevention initiatives
- **NIGO rate benchmarking** — industry benchmarks: best-in-class firms achieve NIGO rates below 5%; average firms operate at 10-20%; firms without automated validation often exceed 25%

### Regulatory Holds and Approval Gates
Regulatory holds and approval gates are control points in the account opening workflow where processing pauses until a specific review or approval is completed. These gates enforce compliance requirements, manage risk, and ensure appropriate oversight of complex or high-risk account openings.

**Supervisory approval requirements:**
- **Discretionary accounts** — accounts where the advisor has discretionary trading authority require supervisory review and approval before activation. The supervisor verifies that the client has granted discretionary authority in writing, that the investment strategy is suitable, and that the advisor is authorized by the firm to exercise discretion. FINRA Rule 3110 requires firms to designate a supervisor for discretionary account activity.
- **Options trading approval** — options approval requires assessment of the client's knowledge, experience, financial situation, and investment objectives. Most custodians use a tiered approval system (e.g., levels 0-4) with increasing levels requiring greater client sophistication and financial capacity. The registered options principal (ROP) or designated supervisor must approve the options level. Higher levels (e.g., uncovered options writing) require enhanced review.
- **Margin accounts** — margin trading requires disclosure delivery, client acknowledgment of margin risks, and supervisory approval. The supervisor reviews suitability of margin for the client's financial situation and investment objectives. Regulation T, FINRA Rules 4210 and 2264 govern margin requirements and disclosures.

**Compliance review triggers:**
- **Politically exposed persons (PEPs)** — clients identified as PEPs through screening trigger enhanced due diligence review before account opening. Compliance reviews source of wealth, source of funds, and the purpose of the account. Senior management approval is typically required.
- **Enhanced due diligence (EDD) clients** — clients from high-risk jurisdictions, with complex ownership structures, or with adverse media hits trigger EDD review. The compliance team conducts a deeper investigation before the account can be opened.
- **Senior investors** — clients age 65 and older trigger age-based review; the senior investor protection requirements (FINRA Rules 2165 and 4512, trusted contact procedures) are covered in account-opening-compliance.
- **High-net-worth thresholds** — firms require elevated review for accounts above defined funding thresholds (illustratively, operations-level review above $500K and compliance review above $2M; account-opening-compliance defines the canonical risk-based review tiers).
- **Concentrated positions** — clients transferring in concentrated stock positions may trigger review to ensure the concentration risk is acknowledged and addressed in the investment strategy.

**Hold management and aging:**
Accounts in regulatory hold must be tracked with: the date the hold was placed, the reason for the hold, the assigned reviewer, and the expected resolution date. Hold aging reports should highlight items approaching or exceeding the firm's service-level targets. Typical targets: supervisory review within 2 business days, compliance review within 5 business days, escalation at 10 business days.

**Escalation procedures:**
When a hold exceeds its target resolution time, the workflow should automatically escalate: first to the assigned reviewer's manager, then to the chief compliance officer or operations director, and finally to senior management. Escalation notifications should include the account details, the hold reason, the elapsed time, and any prior communications.

### Account Opening Automation and STP
Straight-through processing (STP) is the goal of account opening automation: the application flows from submission through account creation without manual intervention. Achieving high STP rates requires investment in technology, data quality, and process standardization.

**STP architecture:**
- **Data collection layer** — onboarding platform or advisor portal collects client data through structured forms with real-time validation. Data is captured once and propagated to all downstream forms and systems.
- **Validation engine** — a rules-based engine that checks every application against the document requirements matrix, custodian-specific validation rules, and regulatory requirements before submission. The engine produces a pass/fail result with specific error messages for any failures.
- **Document assembly** — automated generation of custodian-specific forms, pre-populated with validated client data. Form templates are maintained for each custodian and updated when custodians revise their forms.
- **Custodian integration** — API connections to custodian account opening systems for automated submission and status tracking. The integration handles authentication, data mapping (translating the firm's data model to the custodian's API schema), error handling, and response processing.
- **Exception routing** — applications that fail validation or require manual review are routed to the appropriate operations or compliance queue. STP handles the standard cases; exception-based processing handles the rest.
- **Status tracking and notification** — real-time visibility into the status of every account opening request, with automated notifications to advisors, clients, and operations staff at key milestones.

**OCR and data extraction:**
For firms that still receive paper applications or scanned documents, optical character recognition (OCR) and intelligent document processing (IDP) can extract data from forms and documents. Modern IDP platforms use machine learning to identify document types, extract field values, and flag low-confidence extractions for human review. OCR accuracy varies by document quality; validation against the client's profile data helps catch extraction errors.

**Automated validation rules:**
The validation engine should enforce rules including: all required fields populated and formatted correctly, SSN/EIN passes check-digit validation, name matches across all documents (fuzzy matching to handle minor variations), address is valid and complete (USPS address validation), account type code maps correctly to the custodian's type codes, all required documents are present per the document requirements matrix, all signature fields are completed, beneficiary percentages sum to 100% for retirement accounts, trust certification includes all required elements (trust name, date, trustees, powers), and beneficial ownership certification is complete for entity accounts.

**STP rate measurement:**
- **STP rate** — the percentage of account opening requests that flow from submission to account creation without any manual intervention. Measured overall and segmented by account type, custodian, and advisor.
- **Target STP rates by account type:** Individual taxable accounts: 85-95%; joint accounts: 80-90%; IRA accounts: 75-85%; trust accounts: 30-50%; entity accounts: 20-40%; estate accounts: under 10% (nearly always require manual processing).
- **Exception rate** — the inverse of STP rate; the percentage of applications requiring manual intervention. The goal is to minimize exceptions while maintaining quality and compliance.
- **Time-to-account-number** — elapsed time from submission to custodian account number assignment. For STP-eligible accounts, the target is minutes to hours. For manual accounts, measure against custodian-specific SLA targets.
- **Automation ROI** — compare the cost per account opened before and after automation. Include operations staff time, NIGO remediation cost, advisor time spent on corrections, and technology platform costs. Firms with mature STP typically achieve 60-70% reduction in per-account operations cost for standard account types.

### Multi-Custodian Operations
Firms that custody client assets across multiple custodians (commonly Schwab, Fidelity, Pershing, and others) face additional complexity in account opening. Each custodian has its own forms, validation rules, API specifications, processing timelines, and NIGO patterns.

**Managing custodian-specific requirements:**
- Maintain a separate document requirements matrix for each custodian, updated whenever the custodian revises its forms or requirements
- Map the firm's internal account type codes to each custodian's type codes; discrepancies in type mapping are a frequent source of NIGO rejections
- Maintain custodian-specific form templates for automated document assembly
- Track each custodian's API capabilities and limitations; not all account types are supported via API at all custodians
- Document each custodian's NIGO patterns and common rejection reasons; use this data to build custodian-specific validation rules

**Custodian-specific form requirements (representative examples):**
- Schwab: uses the Schwab Institutional new account application; supports API-based account opening for most standard account types; trust accounts require the Schwab trust certification form
- Fidelity: uses the Fidelity Institutional new account application; API support varies by account type; entity accounts often require manual submission through the Fidelity portal
- Pershing: uses the Pershing new account form (NAF); supports account opening through the NetX360 platform; has specific requirements for options and margin paperwork separate from the main application

**Parallel vs sequential submission:**
When a client is opening accounts at multiple custodians simultaneously (e.g., a trust account at Schwab and an IRA at Fidelity), the operations team must decide whether to submit in parallel or sequentially. Parallel submission is faster but requires the operations team to manage multiple concurrent workflows. Sequential submission is simpler to manage but extends the total processing time. Best practice: submit in parallel when the operations team has capacity and the account types are independent; submit sequentially when the accounts have dependencies (e.g., the IRA rollover depends on the trust account being established first).

**Cross-custodian reconciliation:**
After accounts are opened, the operations team must reconcile the firm's internal records with each custodian's records to ensure: account numbers are correctly mapped, registration details match, account features (margin, options) are correctly reflected, and beneficiary designations are consistent. Discrepancies discovered during reconciliation must be resolved promptly before the account is activated.

### Account Activation and Post-Opening
Account activation is the transition from "account created at custodian" to "account fully operational and ready for trading." Post-opening activities ensure the account is properly funded, configured, and integrated into the firm's systems.

**Funding verification:**
- Verify that the funding method initiated during onboarding is proceeding: ACH transfers should settle within 2-4 business days, wires within 1 business day, ACAT transfers within 4-6 business days
- For accounts funded by ACAT transfer, monitor the transfer status and resolve any rejected or partial transfers promptly
- For IRA rollovers, verify that the rollover is direct (trustee-to-trustee) or that the 60-day deadline for indirect rollovers is tracked
- Flag unfunded accounts at 10, 20, and 30 days; unfunded accounts that remain inactive beyond the custodian's inactivity threshold may be closed by the custodian

**Model portfolio assignment:**
- For discretionary accounts, link the funded account to the appropriate model portfolio in the portfolio management system (PMS) based on the client's risk profile and investment objectives
- Generate the initial rebalancing trades to align the account with the target model; the first trade may require advisor confirmation depending on the firm's policies
- For accounts funded via in-kind transfer (ACAT with existing positions), assess the transferred positions against the target model and develop a transition trading plan that considers tax implications, concentrated positions, and market conditions

**Initial trading enablement:**
- Verify that the account is configured for the correct trading capabilities: cash-only, margin-enabled, options-approved (at the correct level)
- For accounts with options or margin, verify that the custodian has activated these features and that the internal systems reflect the correct permissions
- Place any initial trades and confirm execution

**Welcome kit delivery:**
- Send the client a welcome package confirming the account opening, summarizing account details and features, providing login credentials for client-facing portals, and including any required disclosures not previously delivered
- Welcome communications should be customized by account type and may include educational materials about the client's specific account features

**30-day review:**
- Conduct a post-opening review at 30 days to verify: the account is funded, initial investments are in place and aligned with the investment strategy, all documentation is complete and filed, the client and advisor have no outstanding questions or issues, and the account data is consistent across all systems (CRM, PMS, custodian, billing)
- Any discrepancies or open items identified in the 30-day review must be resolved and documented

**Account maintenance handoff:**
- After the 30-day review, the account transitions from the account opening workflow to the ongoing account maintenance process
- The operations team records the account as fully onboarded and closes the account opening tracking record
- Ongoing activities (rebalancing, billing, performance reporting, regulatory filings) are managed through the account maintenance and servicing workflows

## Worked Examples

Three worked examples (multi-custodian RIA workflow design, NIGO reduction through automated pre-submission validation, and tiered approval workflows for complex account types) are in [references/examples.md](references/examples.md) — load it when designing or benchmarking a concrete account opening process.

## Common Pitfalls
- Treating account opening as a single uniform process rather than designing differentiated workflows by account type complexity — individual accounts and entity accounts have fundamentally different processing requirements
- Maintaining the document requirements matrix in spreadsheets or tribal knowledge rather than encoding it in the account opening system as enforced validation rules
- Not tracking custodian-specific form versions, leading to submissions on outdated forms that are automatically rejected
- Routing all complex accounts through a single approval queue instead of specialized queues with risk-based differentiation
- Allowing custodian submission before all required supervisory and compliance approvals are documented
- Not establishing clear SLAs for each stage of the account opening workflow, making it impossible to identify and address bottlenecks
- Failing to close the feedback loop between NIGO rejections and process improvement — tracking NIGO rates without analyzing root causes and implementing preventive controls
- Not verifying account data consistency across internal systems (CRM, PMS, billing, custodian) after account opening, leading to downstream errors in billing, reporting, and trading
- Treating account activation as automatic upon account number assignment — accounts should not be activated until funding is verified, model assignment is confirmed, and the 30-day review process is initiated
- Assuming that a single set of validation rules works across all custodians — each custodian has unique requirements that must be codified and maintained separately
- Not tracking unfunded accounts, which results in accounts being opened but never funded, wasting operations capacity and potentially violating custodian inactivity policies
- Building account opening automation without investing in exception handling — even the best STP systems will have exceptions, and the exception handling workflow must be as well-designed as the automated path
- Opening entity accounts without verifying that the authorized signer has legal authority to act on behalf of the entity — a corporate resolution or operating agreement authorizing the account must be obtained and reviewed, not just collected
- Failing to distinguish between revocable and irrevocable trusts during intake, leading to incorrect application of beneficial ownership requirements and potential CDD Rule violations
- Not maintaining a log of account opening processing times by stage, which prevents the operations team from identifying systemic delays and measuring the impact of process improvements
- Neglecting to reconcile account features (margin, options levels, check writing) between the firm's internal records and the custodian's records after opening — mismatches can cause trade rejections or unauthorized activity

## Cross-References
- **client-onboarding** (advisory-practice plugin): Covers the front-office, advisor-facing onboarding workflow that feeds into the back-office account opening process described in this skill; client-onboarding handles prospect intake, identity verification, suitability collection, and e-signature, while account-opening-workflow handles the operations processing, custodian submission, and account activation
- **account-maintenance** (client-operations plugin): Accounts transition from the account opening workflow to the account maintenance workflow after the 30-day post-opening review; maintenance covers ongoing updates to registration, beneficiaries, features, and documentation
- **know-your-customer** (compliance plugin): KYC/CIP requirements define the identity verification and due diligence standards that the account opening workflow must satisfy; KYC policies determine which clients require enhanced review during account opening
- **investment-suitability** (compliance plugin): Suitability data collected during onboarding is validated during the account opening supervisory review; the suitability profile must support the account type, features (margin, options), and investment strategy before the account is activated
- **client-disclosures** (compliance plugin): Disclosure delivery requirements (Form CRS, Form ADV, privacy notice, margin and options disclosures) must be satisfied at or before account opening; the account opening workflow must track and confirm disclosure delivery
- **books-and-records** (compliance plugin): Account opening documents, signed agreements, and approval records are books and records subject to retention requirements under SEC Rules 17a-3/17a-4 and Rule 204-2; the account opening workflow must ensure all documents are properly stored and indexed
- **portfolio-management-systems** (advisory-practice plugin): The PMS receives new accounts from the account opening workflow for model portfolio assignment and initial trading; the account opening confirmation triggers the PMS to associate the account with the appropriate model
- **anti-money-laundering** (compliance plugin): OFAC screening and AML checks are mandatory gates in the account opening workflow; accounts flagged by AML screening enter regulatory hold until compliance review is complete
- **account-opening-compliance** (client-operations plugin): Defines the regulatory requirements (CIP/KYC, suitability verification, OFAC screening, beneficial ownership) that the account opening workflow must enforce as processing gates; the compliance skill defines what must be checked, and this skill describes the operational workflow that implements those checks
- **fee-billing** (advisory-practice plugin): New accounts must be configured in the billing system with the correct fee schedule, billing method, and inception date; account opening confirmation triggers billing system setup
- **margin-operations** (trading-operations plugin): Margin account opening requires additional approval gates, documentation, and custodian configuration beyond standard account opening; the margin operations skill covers ongoing margin management after the account is opened and margin is activated
