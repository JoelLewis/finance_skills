---
name: account-opening-compliance
description: "Embed compliance controls into account opening and verify regulatory readiness. Use when designing CIP/KYC identity verification gates, implementing OFAC and sanctions screening at onboarding, collecting beneficial ownership certification for entity or trust accounts, building risk-based approval tiers that route applications by risk level, defining compliance screening requirements and exception tracking, adding senior investor protections (FINRA Rules 2165/4512) or trusted contact procedures, establishing CDD risk ratings and ongoing monitoring triggers, or preparing account opening procedures for SEC or FINRA examination. For the operational pipeline these controls plug into, see account-opening-workflow."
---

# Account Opening Compliance

## Core Concepts

### CIP Integration in Account Opening
The Customer Identification Program is the first compliance gate in any account opening workflow. Under USA PATRIOT Act Section 326 and its implementing regulations, a firm must verify the identity of each customer before or at the time of account opening. The account opening process must be designed so that no account becomes active until CIP is satisfied.

**Verification timing.** The regulations permit two approaches: (1) verify identity before the account is opened, which is the most conservative approach and prevents any transactional activity until verification is complete; or (2) verify identity within a reasonable time after the account is opened, provided the firm has procedures to manage the risk of incomplete verification (such as restricting account activity until verification is complete). Most firms implementing digital onboarding choose the first approach — identity verification occurs in real time during the application flow, and the application cannot proceed until verification returns a pass result. The second approach — opening with restricted activity pending verification — is used primarily for paper-based or advisor-assisted workflows where verification cannot occur in real time, and requires the firm to document the risk mitigation procedures (no trading, no disbursements, no margin until verification completes).

**Database verification** is the primary method for digital account opening. The onboarding system sends applicant data (name, date of birth, address, SSN/TIN) to an identity verification vendor (LexisNexis Risk Solutions, Alloy, Equifax, TransUnion) via API. The vendor cross-references the data against credit bureau records, public records, and government databases and returns a pass, fail, or inconclusive result, typically within seconds. Database verification satisfies CIP's non-documentary verification requirement.

**Documentary verification** serves as a fallback when database verification is inconclusive or unavailable. The applicant uploads a photo of a government-issued ID (driver's license, passport, state ID). OCR extracts data fields, and the system may compare the document photo to a selfie for liveness detection. Documentary verification is slower and introduces friction but is necessary for applicants who cannot be verified through database methods — non-US persons, thin-file individuals, and cases where database results are ambiguous.

**Verification failure handling.** The account opening workflow must define clear paths for each verification outcome:
- **Pass** — proceed to the next compliance gate
- **Fail** — halt the application; notify the applicant that the account cannot be opened; document the reason; retain records per CIP recordkeeping requirements
- **Inconclusive** — route to an exception queue for manual review; request additional identifying information or documentary verification; set a time limit for resolution (e.g., 5 business days) after which the application is closed

**Exception processing for inconclusive results** is operationally critical. Common causes of inconclusive results include name mismatches (legal name vs preferred name, hyphenated names, transliteration differences for non-English names), address mismatches (recent moves, PO boxes), and thin credit files (young adults, recent immigrants). The exception processing workflow should collect additional documentation, perform manual database searches, and escalate to compliance when standard exception procedures do not resolve the issue. The firm should track exception rates by cause to identify systemic issues — for example, a high rate of transliteration-related exceptions may indicate a need to improve the verification vendor's handling of non-Latin character sets.

**Non-US persons and foreign accounts.** CIP verification for non-US persons presents additional complexity. Acceptable identification numbers include a passport number and country of issuance, an alien identification card number, or a number and country of issuance of any other unexpired government-issued document evidencing nationality or residence that bears a photograph. Database verification coverage is weaker for non-US persons, making documentary verification (passport upload with liveness check) the primary method. The account opening workflow should detect non-US applicants early and route them to the documentary verification path without requiring a failed database check first.

**Recordkeeping requirements.** CIP regulations require retention of identifying information (name, date of birth, address, identification number), a description of the documents or methods used to verify identity, and the resolution of any discrepancies. These records must be retained for 5 years after the account is closed. The account opening system should automatically generate and store a CIP verification record for each application, including the verification method, vendor response, timestamp, and outcome.

### OFAC and Sanctions Screening
OFAC screening is a mandatory compliance gate that must clear before any account is opened. Unlike CIP, which verifies that the applicant is who they claim to be, OFAC screening determines whether the applicant — or any person associated with the account — is a sanctioned individual or entity with whom the firm is prohibited from doing business.

**Scope of screening.** The firm must screen all individuals associated with the account, not just the primary applicant. This includes:
- Account holders (all owners for joint accounts)
- Beneficial owners (25% equity holders and control persons for entity accounts)
- Authorized signers and persons with trading authority
- Trustees (for trust accounts)
- Custodians under UTMA/UGMA accounts
- Any other person with authority over or beneficial interest in the account

**Lists screened.** At minimum, screening must cover the OFAC SDN (Specially Designated Nationals and Blocked Persons) list. Best practice extends screening to the Sectoral Sanctions Identifications (SSI) list, the Non-SDN Menu-Based Sanctions list, the Foreign Sanctions Evaders (FSE) list, and consolidated non-OFAC lists such as the FinCEN 314(a) list and any firm-specific restricted lists. Automated screening platforms typically screen against all OFAC lists simultaneously.

**Screening frequency.** OFAC screening must occur at account opening and on an ongoing basis thereafter. Ongoing screening is triggered by: (1) OFAC list updates (the SDN list is updated frequently, sometimes multiple times per week), (2) changes to account ownership or authorized parties, and (3) periodic rescreening on a risk-based schedule. At account opening, the screening must occur before the account is activated and before any funds are accepted or transactions are processed.

**Potential match handling.** When the screening system generates a potential match (also called an alert), the workflow must:
1. Halt the account opening process — no account activation until the alert is resolved
2. Route the alert to a trained compliance analyst for manual review
3. Compare all available identifying information (full name, aliases, date of birth, nationality, address, passport number) between the applicant and the list entry
4. Determine whether the match is a true positive (the applicant is the listed person) or a false positive (a different person with similar identifying information)
5. Document the analysis, the data points compared, and the disposition decision
6. For true positives: block the account application, block any associated property, and file a blocked property report with OFAC within 10 business days
7. For false positives: document the basis for the determination, retain the record, and allow the application to proceed

**False positive management** is an ongoing operational challenge. Common names, transliteration variations, and incomplete identifying data on OFAC lists generate high false positive rates. Firms should tune their screening algorithms to balance detection sensitivity against operational burden. Reducing false positives without degrading detection requires maintaining and updating known false positive records, using multiple data points for matching (not just name), and calibrating fuzzy match thresholds. All tuning decisions must be documented and defensible.

**Documentation of screening results.** Regardless of outcome, the account opening record must include a log of every screening run: the lists screened, the individuals screened, the screening timestamp, the algorithm version or configuration, the raw results, and the disposition. For no-match results, the system log is sufficient. For potential matches resolved as false positives, the record must include the analyst's comparison of identifying data points and the rationale for the false-positive determination. For true positives, the record must include the blocking report, the notification to OFAC, and any subsequent correspondence. These records must be retained for the life of the account plus 5 years after closure and must be producible for regulatory examination.

### Beneficial Ownership Certification
The FinCEN CDD Rule (31 CFR 1010.230, effective May 2018) requires covered financial institutions to identify and verify the beneficial owners of legal entity customers at the time of account opening.

**Who must be identified.** For each legal entity customer, the firm must identify:
- Every individual who directly or indirectly owns 25% or more of the equity interests in the entity (the ownership prong)
- At least one individual who has significant responsibility for controlling, managing, or directing the entity — such as a CEO, CFO, COO, managing member, general partner, president, vice president, or treasurer (the control prong)

A single individual may satisfy both prongs (e.g., a sole owner who is also the manager). The maximum number of beneficial owners reported is typically five (four under the ownership prong plus one under the control prong), though an entity with more than four 25% owners must report all of them.

**25% ownership threshold.** Ownership is calculated on a direct and indirect basis. If an individual owns 30% of Entity A, and Entity A owns 100% of Entity B (the account applicant), the individual indirectly owns 30% of Entity B and must be identified as a beneficial owner. Multi-layered ownership structures require the firm to trace ownership through intermediate entities to identify the natural persons who ultimately hold 25% or more.

**Exempt entity types.** Certain entities are exempt from the beneficial ownership requirement because their ownership is already transparent through other regulatory mechanisms:
- Publicly traded companies listed on a US stock exchange (or a foreign exchange meeting equivalent standards)
- SEC-registered investment companies and investment advisers
- Insurance companies regulated by a state
- Banks, credit unions, and other depository institutions regulated by a federal banking agency
- Broker-dealers registered with the SEC
- Entities established by federal or state government
- Pooled investment vehicles operated by a financial institution (but not the underlying investors)

**Certification form management.** The firm collects beneficial ownership information on a certification form (based on FinCEN's standard form or the firm's equivalent). The account opening workflow must present this form when the applicant is a legal entity, collect the required information for each beneficial owner, and verify the identity of each identified beneficial owner using the firm's CIP procedures. The form must be signed (physically or electronically) by the individual opening the account on behalf of the entity, certifying the accuracy of the information. The firm must retain the certification form and verification records for 5 years after the account is closed.

**Ongoing monitoring for ownership changes.** The CDD Rule requires firms to update beneficial ownership information on a risk basis. The account opening process should establish triggers for ownership updates: periodic review (typically annually for high-risk entities, every 3 years for standard risk), event-driven updates (notification of ownership change, corporate restructuring, merger), and customer-initiated updates. The account opening system should flag the next review date and route it to the appropriate review queue.

**Corporate Transparency Act interaction.** The Corporate Transparency Act (CTA) originally required most companies to report beneficial ownership information directly to FinCEN beginning in 2024. As of FinCEN's March 2025 interim final rule, however, all entities formed in the United States (the former "domestic reporting companies") and their beneficial owners are exempt from CTA reporting; only entities formed under foreign law and registered to do business in the US remain reporting companies, and they need not report US-person beneficial owners. The practical consequence for account opening: CTA-reported data is not a substitute for the firm's own beneficial ownership collection, and the CTA does not relieve financial institutions of their CDD Rule obligations. Firms must continue to collect and verify beneficial ownership independently through the certification form process, and should verify the current state of CTA rulemaking, which remains in flux.

### Tax Compliance: FATCA and CRS
Account opening must collect information to satisfy international tax reporting obligations. These requirements apply regardless of the account holder's citizenship and are triggered by indicators of foreign tax residency.

**FATCA (Foreign Account Tax Compliance Act).** US financial institutions must determine whether account holders are US persons (requiring W-9 collection) or non-US persons (requiring W-8BEN or W-8BEN-E collection and FATCA classification). For entity accounts such as trusts, the firm must classify the entity under FATCA (e.g., Active NFFE, Passive NFFE, Financial Institution) and, for Passive NFFEs, identify any controlling persons who are US persons. Failure to collect valid W-8/W-9 forms triggers backup withholding at 24% on reportable payments.

**CRS (Common Reporting Standard).** If any account holder or controlling person is tax-resident in a CRS-participating jurisdiction (most countries outside the US), the firm must collect a self-certification of tax residency, including the foreign taxpayer identification number (TIN). For the family trust scenario with a UK-resident trustee, CRS requires reporting the account to HMRC via the firm's CRS reporting channel. The self-certification must be collected at or before account opening.

**Integration with account opening workflow.** The tax compliance gate should:
- Collect W-9 from all US persons and W-8BEN from all non-US persons at account opening
- Classify entity accounts under FATCA (Active/Passive NFFE, Financial Institution, etc.)
- Collect CRS self-certification forms from any person with foreign tax residency indicators
- Validate TIN format against the issuing country's known format (e.g., UK NI number format: 2 letters + 6 digits + 1 letter)
- Flag accounts with missing or expired tax forms for remediation before activation
- Set renewal triggers for W-8 forms (expire every 3 years unless a change of circumstances occurs)

**Cross-border complexity.** When account holders have tax obligations in multiple jurisdictions (e.g., a US-UK dual national, or a trust with trustees in different countries), the firm may need to report under both FATCA and CRS. The account opening system should identify multi-jurisdictional reporting obligations based on the tax residency declarations collected and route these accounts for compliance review.

### Suitability Assessment at Opening
Account opening is the primary data collection event for investment suitability. The compliance framework requires that the firm gather sufficient information to evaluate the suitability of any subsequent investment recommendation before or at the time of the first recommendation.

**Documenting the investment profile.** The account opening process must collect all elements of the customer's investment profile as defined by FINRA Rule 2111 and Regulation Best Interest: investment objectives, risk tolerance, time horizon, liquidity needs, financial situation (income, net worth, liquid net worth), investment experience, tax status, and any other information the customer discloses. The profile must be documented in a durable, retrievable format — not just captured in a questionnaire that is discarded after scoring.

**Mapping to appropriate products and models.** The suitability data collected at opening drives the mapping of the account to an investment model or strategy. The account opening system should produce a risk score or category from the suitability questionnaire and map that score to a defined range of models or strategies. This mapping must be documented, consistently applied across advisors, and periodically reviewed for reasonableness. Deviations from the mapping (e.g., an advisor selecting a more aggressive model than the client's risk score indicates) should trigger a compliance review.

**Reg BI care obligation for account type recommendation.** Under Regulation Best Interest, the recommendation of an account type itself (e.g., brokerage vs advisory, IRA vs taxable, fee-based vs commission-based) is subject to the Care Obligation. The account opening process for broker-dealers must document that the recommended account type is in the customer's best interest, considering reasonably available alternatives and the customer's investment profile. This means the compliance controls at account opening must capture not just the account type selected but the rationale for selecting it over alternatives.

**Suitability documentation requirements.** The firm must retain documentation of the customer's investment profile, the risk assessment or score, the recommended model or strategy, and the basis for the recommendation. For discretionary accounts, the investment policy statement (IPS) should be established at account opening. For Reg BI accounts, Form CRS must be delivered before or at the time of the recommendation, and the basis for the recommendation must be documented.

**Investment adviser fiduciary considerations at opening.** For RIA accounts, the fiduciary duty of care requires that the adviser understand the client's financial situation and investment objectives before making any recommendation. The account opening suitability questionnaire serves as the foundation for the adviser's duty of care analysis. The adviser must also identify and disclose any material conflicts of interest that may affect the advice provided. The account opening process should include delivery of Form ADV Part 2A and Part 2B (or the brochure supplement), collection of the client's acknowledgment of receipt, and execution of the investment advisory agreement. These disclosure obligations are not just suitability requirements — they are fiduciary obligations that, if not met at account opening, create ongoing compliance risk throughout the advisory relationship.

**Enhanced suitability review triggers.** Certain conditions detected during the account opening process should trigger an enhanced suitability review before the account is activated:
- The client selects an investment objective or risk tolerance inconsistent with their financial situation (e.g., aggressive growth with limited liquid net worth)
- The client requests products or features not typically consistent with their profile (e.g., options trading for a conservative investor)
- The client is a senior investor (age 65 or older)
- The client has limited investment experience and selects a complex strategy
- The client's stated time horizon is inconsistent with the account type (e.g., short-term horizon in a long-term retirement account)
- The client declines to provide certain suitability information — the firm must narrow the range of suitable recommendations accordingly and document the refusal
- The account involves a rollover from an employer plan, triggering Reg BI analysis of whether the rollover recommendation is in the customer's best interest compared to remaining in the plan

### Risk-Based Review Tiers
Not all account applications present the same compliance risk. A risk-based approach assigns each application to a review tier based on risk indicators, ensuring that higher-risk applications receive enhanced scrutiny while standard applications proceed efficiently.

**Standard review** applies to the majority of account openings: individual or joint taxable accounts, IRAs, and other common account types for US persons with clean CIP verification, clear OFAC screening, and a straightforward investment profile. Standard review may be fully automated — the system verifies that all compliance gates have passed and approves the application without manual intervention. An operations supervisor or compliance designee may review a sample of auto-approved accounts on a post-hoc basis.

**Enhanced review triggers.** The following indicators should escalate an application from standard to enhanced review, requiring manual compliance review before account activation:
- **Politically Exposed Persons (PEPs)** — foreign senior political figures, their family members, and close associates, as identified through PEP screening databases
- **High-risk jurisdictions** — applicants with citizenship, residence, or significant ties to countries identified as high risk by FATF, FinCEN advisories, or the firm's own risk assessment
- **Complex ownership structures** — multi-layered entities, nominees, trusts with opaque beneficiary structures, accounts with multiple authorized parties
- **Source of wealth concerns** — stated source of wealth inconsistent with known employment or business, unusually large initial funding amount relative to the applicant's profile, funds originating from high-risk jurisdictions
- **Negative media or adverse information** — screening results revealing adverse news, litigation, regulatory actions, or criminal history
- **Senior investors** — applicants age 65 or older, triggering age-based review under FINRA Rules 2165 and 4512
- **Large initial deposits** — funding amounts exceeding firm-defined thresholds (e.g., $1M or more) warranting source-of-funds review
- **Discretionary authority** — accounts granting trading discretion require supervisory review of the advisory agreement and investment authority

**Risk scoring at account opening.** Many firms assign a numeric risk score to each account at opening based on a weighted assessment of risk factors. Common scoring dimensions include:
- Customer type (individual, entity, trust, foreign national, PEP)
- Geographic risk (customer domicile, citizenship, fund flow jurisdictions)
- Product complexity (standard brokerage, advisory, margin, options, alternatives)
- Funding source (ACH from verified bank, wire from domestic bank, wire from foreign bank, third-party check)
- Relationship characteristics (new client, existing client opening additional account, referral source)
- Account size (accounts above defined thresholds warrant higher scores)

The risk score determines the initial CDD risk rating, which in turn drives the frequency and depth of ongoing monitoring. The scoring model should be documented, validated periodically, and applied consistently. Firms should avoid models that are so coarse that they assign nearly all accounts to the same tier, or so sensitive that they escalate a disproportionate share of routine accounts.

**Escalation to compliance.** When enhanced review is triggered, the application routes to a compliance analyst or compliance officer for manual review. The reviewer evaluates the risk factors, may request additional documentation from the applicant (source of funds statement, additional identification, purpose of account), and makes an approve/deny/escalate decision. If the reviewer cannot resolve the risk, the application escalates to senior compliance or the Chief Compliance Officer. All review decisions, supporting analysis, and documentation must be retained.

**Documentation requirements per tier.** Standard review requires retention of the automated compliance check results (CIP, OFAC, suitability score). Enhanced review requires, in addition: the specific risk factor(s) that triggered escalation, the reviewer's analysis, any additional documentation collected, the approval decision and rationale, and the identity of the approver. The documentation standard increases with risk tier — a PEP account, for example, should have a detailed memo explaining the source of wealth analysis and the basis for approval.

**Account denial procedures.** When compliance determines that an account should not be opened, the denial must be handled carefully. The firm should document the specific reasons for denial, retain the documentation in the compliance file, and communicate the denial to the applicant in a manner that does not reveal OFAC screening results or SAR-related information (to avoid tipping-off violations). The denial letter should state that the firm is unable to open the account at this time without providing the specific compliance reason. If the denial is related to OFAC or AML concerns, the firm should evaluate whether a SAR filing is warranted. Denied applications should be tracked in a centralized log to identify patterns (e.g., repeated attempts by the same individual to open accounts, or a pattern of denials from a particular referral source).

### Senior Investor Protections
Account opening for senior investors (generally age 65 and older, though some firms use age 60) triggers additional compliance obligations designed to protect against financial exploitation and diminished capacity.

**FINRA Rule 4512 — Trusted Contact Person.** Effective February 2018, FINRA Rule 4512 requires firms to make reasonable efforts to obtain the name and contact information of a trusted contact person for each customer's account. The trusted contact is not an authorized party — they cannot transact on the account. The purpose is to provide the firm with a resource to contact if the firm suspects financial exploitation, diminished capacity, or has concerns about the customer's welfare. The account opening process must include a trusted contact designation as a standard field, and the firm must make reasonable efforts to obtain this information for all customers, not just seniors. However, the trusted contact is particularly important for senior investors.

**FINRA Rule 2165 — Financial Exploitation of Specified Adults.** Effective February 2018, this rule provides a safe harbor for firms to place temporary holds on disbursements from the accounts of specified adults (persons age 65 or older, or persons age 18 or older who the firm reasonably believes have a mental or physical impairment that renders them unable to protect their own interests). At account opening, the firm should:
- Document the customer's age and any observable indicators of diminished capacity
- Explain the trusted contact person designation and its purpose
- Record the trusted contact information in the account record
- Flag the account in the firm's system for age-based monitoring and enhanced review

**Age-based triggers for enhanced review at opening.** When the applicant is 65 or older, the account opening process should trigger:
- Mandatory collection of trusted contact person information (with documentation of efforts if the customer declines)
- Enhanced suitability review — is the recommended account type, investment strategy, and product mix appropriate for the customer's age, time horizon, liquidity needs, and cognitive capacity?
- Review for potential financial exploitation indicators — is a third party exerting undue influence over the account opening? Is the customer being pressured into inappropriate products?
- State-specific protections — some states impose additional requirements (such as mandatory reporting of suspected elder financial exploitation) that the account opening process must accommodate

**Diminished capacity indicators** that may be observed during the account opening process:
- Confusion about the purpose of the account or the nature of the investment
- Inability to understand or recall information provided during the application
- Reliance on a third party to answer questions or make decisions
- Significant changes from previously known behavior or decision-making patterns (for existing clients opening new accounts)
- Inconsistent or contradictory responses to suitability questions

When these indicators are present, the firm should pause the account opening, document the observations, consult with a supervisor and potentially the trusted contact person, and determine whether proceeding is in the customer's interest.

**Temporary hold authority.** FINRA Rule 2165 authorizes the firm to place a temporary hold on a disbursement of funds or securities from the account of a specified adult if the firm reasonably believes that financial exploitation has occurred, is occurring, has been attempted, or will be attempted. The hold may last up to 15 business days, extendable to 25 business days if the firm has reported the matter to a state regulator or agency or court of competent jurisdiction. While this authority applies post-opening, the account opening process is the point at which the firm establishes the infrastructure — trusted contact, system flags, monitoring triggers — that enables effective use of hold authority when needed.

**State-level protections.** Many states have adopted their own senior investor protection statutes, often modeled on NASAA's Model Act to Protect Vulnerable Adults from Financial Exploitation. These state laws may impose mandatory reporting obligations (requiring the firm to report suspected exploitation to adult protective services or a state securities regulator), provide additional hold authority beyond FINRA Rule 2165, or create penalties for failure to report. The account opening compliance framework must identify the applicable state law based on the customer's residence and ensure that state-specific obligations are incorporated into the workflow.

### Compliance Automation
Manual compliance processes do not scale. As account volumes grow, firms must automate compliance screening, approval routing, exception tracking, and audit trail generation to maintain both efficiency and control quality.

**Automated screening workflows.** The core compliance checks at account opening — CIP verification, OFAC screening, PEP screening, negative media screening, and beneficial ownership verification for entities — should execute automatically as the application progresses through the workflow. Each screening step fires via API call, the result is captured in the application record, and the workflow engine advances or halts the application based on the result. No manual intervention is required for applications that pass all screens.

**Rules-based approval routing.** The workflow engine should evaluate each application against a configurable rules set to determine the approval path:
- Applications passing all automated screens with no enhanced review triggers route to auto-approval (or to a light-touch operations review)
- Applications with one or more enhanced review triggers route to the appropriate reviewer based on the nature of the trigger (compliance analyst for OFAC alerts, senior compliance for PEPs, operations supervisor for documentation issues)
- Applications with multiple concurrent triggers or the highest-risk indicators route to the CCO or a senior compliance committee

The rules engine must be configurable by compliance (not hardcoded by IT), auditable (all rule changes logged with effective dates and approver), and testable (new rules can be validated against historical applications before deployment).

**Compliance checklist automation.** Each account type has a defined set of compliance requirements. The system should generate an automated checklist at the start of each application based on the account type and features, track completion of each item, and prevent submission until all required items are satisfied. The checklist should be visible to the operations team, the advisor, and compliance. Example checklists by account type:

- **Individual taxable:** CIP verification (pass), OFAC screening (clear), suitability questionnaire (complete), risk score (generated), Form CRS (delivered), privacy notice (delivered), trusted contact (collected or documented refusal), new account form (signed)
- **Entity (LLC/Corp):** All individual checklist items for each authorized party, plus: entity classification (documented), beneficial ownership certification (complete), beneficial owner CIP verification (pass for each), beneficial owner OFAC screening (clear for each), formation documents (collected), corporate resolution or operating agreement (collected), EIN verification (confirmed), compliance review (approved)
- **Trust:** Trustee CIP verification (pass for each), trust classification (revocable vs irrevocable — documented), trust certification or agreement (collected), beneficial ownership determination (documented with rationale), OFAC screening for all associated persons, compliance review if irrevocable or complex structure
- **IRA/Retirement:** Standard individual checklist, plus: IRA adoption agreement (signed), beneficiary designation (complete), IRA disclosure statement (delivered), rollover/transfer documentation (if applicable), Reg BI analysis for rollover recommendation (if applicable)

**Exception tracking.** When an application enters an exception state (inconclusive CIP, OFAC potential match, missing documentation, triggered enhanced review), the system must track the exception from creation through resolution. Exception tracking should include: the exception type, the date raised, the assigned reviewer, the current status, the resolution (approved, denied, pending additional information), the resolution date, and the supporting documentation. Aging exception reports should surface applications that have been in exception status beyond defined thresholds (e.g., 3 business days for CIP exceptions, 1 business day for OFAC alerts).

**Audit trail generation.** Every compliance action during the account opening process must be logged in an immutable audit trail: who performed the action, what the action was, when it occurred, and the result. This includes automated actions (system ran OFAC screening at 14:23:07 — result: no match) and manual actions (compliance analyst J. Smith reviewed OFAC alert #4521 at 15:10:22 — disposition: false positive — rationale: different date of birth and passport number). The audit trail must be retained for the life of the account plus the applicable regulatory retention period (5-6 years after account closure) and must be producible for regulatory examinations.

**Compliance dashboard for the opening pipeline.** A real-time dashboard provides compliance and operations management with visibility into the account opening pipeline: total applications in progress, applications by stage, applications in exception status, aging exceptions, approval rates, auto-approval rates, average time-to-open, and NIGO rates. The dashboard enables compliance to identify bottlenecks, staffing needs, and emerging risk patterns (e.g., a spike in OFAC alerts from a particular region).

**Vendor management for compliance screening.** Most firms rely on third-party vendors for identity verification, OFAC screening, PEP databases, and adverse media feeds. The compliance automation framework must include vendor oversight: initial due diligence on the vendor's data sources and accuracy rates, contractual service-level agreements (SLAs) for response time and uptime, periodic validation testing (running known positives and known negatives through the vendor's system to verify accuracy), and contingency procedures for vendor outages. If the screening vendor is unavailable, the firm must have a fallback process — manual screening against downloadable OFAC lists, for example — to avoid either opening accounts without screening or halting all account openings during the outage.

**Regulatory technology (RegTech) considerations.** The compliance automation landscape is evolving rapidly. Firms evaluating RegTech solutions for account opening compliance should assess: integration capabilities with existing account opening platforms and custodian APIs; configurability of screening rules and thresholds by compliance (not requiring developer intervention); quality of audit trail and reporting outputs; ability to handle multi-entity, multi-jurisdiction screening in a single workflow; and the vendor's regulatory track record (has the vendor's technology been examined by regulators, and what were the findings?). The firm should retain ownership of the compliance decision — automation assists but does not replace compliance judgment on escalated cases.

### Ongoing Monitoring Triggers Set at Opening
The account opening process does not end when the account is activated. The compliance decisions made at opening establish the framework for ongoing monitoring throughout the life of the account.

**CDD risk rating assignment.** Every account receives a CDD risk rating at opening (e.g., low, medium, high, or a numeric score). The risk rating is derived from the risk factors assessed during the opening process: customer type, geographic exposure, product complexity, source of wealth, PEP status, and any enhanced review findings. The risk rating determines the intensity and frequency of ongoing monitoring — high-risk accounts receive more frequent transaction monitoring, periodic reviews, and closer scrutiny of unusual activity.

**Event-driven review triggers.** The account opening process should establish the events that will trigger a compliance review during the life of the account:
- Material changes to account ownership or authorized parties
- Significant changes to the investment profile (objectives, risk tolerance, financial situation)
- Large deposits or withdrawals inconsistent with the established account activity pattern
- Transactions involving high-risk jurisdictions
- Addition of margin, options, or other features that increase risk
- OFAC list updates that produce a new potential match against existing account holders
- Negative media hits on account holders or beneficial owners
- Customer reaching age 65 (triggering senior investor protections)
- Customer complaint or litigation involving the account
- Death of an account holder or beneficial owner
- Regulatory inquiry or subpoena involving the account holder
- Significant change in account balance (increase or decrease) beyond expected thresholds
- Account inactivity for an extended period followed by sudden high-volume activity

**Periodic review scheduling.** Based on the CDD risk rating assigned at opening, the system should schedule the next periodic review: annually for high-risk accounts, every 2-3 years for medium-risk accounts, and every 3-5 years for low-risk accounts. The periodic review confirms that the customer's profile remains current, the risk rating remains appropriate, and no new risk factors have emerged.

**Account activity monitoring thresholds.** The account opening process should establish baseline expectations for account activity based on the customer's profile, account type, and stated purpose. These baselines feed into the firm's transaction monitoring system, which generates alerts when activity deviates significantly from expectations. For example, an account opened for "long-term retirement savings" that begins executing high-frequency trades should generate an alert for compliance review.

**Handoff from opening compliance to ongoing compliance.** The transition from account opening to the ongoing compliance lifecycle must be explicit and documented. When the account opening process is complete, the system should transmit the following to the ongoing monitoring infrastructure: the CDD risk rating, the beneficial ownership record (for entities), the next scheduled periodic review date, any conditions of approval imposed during enhanced review (e.g., "monitor for source-of-funds consistency for the first 6 months"), the trusted contact person record, and the suitability profile. This handoff ensures that the compliance decisions made at opening are not lost and that ongoing monitoring reflects the risk assessment established during the opening process. A gap in the handoff — for example, an account approved with conditions but no system to track compliance with those conditions — is a significant control weakness.

## Worked Examples


Three worked examples — automated compliance screening for a high-volume broker-dealer, beneficial ownership verification for complex entity structures (ownership tracing, trust classification), and a four-tier risk-based review framework (auto-approval through CCO review, with $500K and $2M funding thresholds) — are in [references/examples.md](references/examples.md); load it when designing a concrete screening, beneficial ownership, or review-tier program.

## Common Pitfalls
- Opening an account before CIP verification is complete — the PATRIOT Act requires verification before or at account opening, and "reasonable time after" is narrowly construed by examiners
- Screening only the primary account holder against OFAC and neglecting joint owners, trustees, beneficial owners, and authorized signers — all associated individuals must be screened
- Collecting the FinCEN beneficial ownership certification form but not verifying the identities of the reported beneficial owners — the CDD Rule requires both identification and verification
- Not tracing indirect ownership through intermediate entities — a natural person owning 40% of a parent entity that owns 100% of the applicant entity is a 40% beneficial owner and must be reported
- Applying the same review intensity to every application regardless of risk — this overwhelms compliance resources and paradoxically reduces scrutiny of high-risk accounts
- Treating suitability data collection as a box-checking exercise rather than gathering actionable information that drives investment decisions and compliance review
- Failing to document the rationale for account type recommendations under Reg BI — the account type itself is a recommendation subject to the Care Obligation
- Not obtaining trusted contact information for senior investors or failing to document reasonable efforts when the customer declines
- Relying on manual OFAC screening processes that cannot keep pace with frequent list updates — screening must be automated and triggered by list changes
- Hardcoding compliance rules in the workflow system without providing compliance with the ability to modify rules as regulations and firm policies evolve
- Generating compliance audit trails that record outcomes but not rationale — examiners want to see not just what decision was made but why
- Setting CDD risk ratings at account opening and never updating them — risk ratings must be dynamic, responsive to new information and changing circumstances
- Allowing exception queues to age without escalation — a stale exception is an unresolved compliance risk that grows with time
- Not coordinating account opening compliance across affiliated entities (e.g., a broker-dealer and an investment adviser under common ownership opening accounts for the same client) — this can create duplicative or inconsistent compliance records
- Failing to track the FinCEN 2024 final rule extending BSA/AML requirements to SEC-registered investment advisers — its effective date was postponed from January 1, 2026 to January 1, 2028 (FinCEN final rule, December 2025), and FinCEN intends to revisit the rule's substance before then; advisers should monitor the rulemaking and verify current status rather than assume the 2026 obligations apply
- Overlooking state-level senior investor protection statutes that may impose reporting obligations beyond what FINRA rules require

## Cross-References
- **know-your-customer** (compliance plugin): Defines the CIP, CDD, and ongoing monitoring requirements that this skill implements within the account opening workflow
- **anti-money-laundering** (compliance plugin): OFAC screening, SAR filing, and AML program requirements that intersect with account opening compliance gates
- **investment-suitability** (compliance plugin): Suitability obligations that drive the investment profile data collection at account opening
- **reg-bi** (compliance plugin): Regulation Best Interest's Care and Disclosure Obligations that apply to account type recommendations and initial investment recommendations at opening
- **account-opening-workflow** (client-operations plugin): The operational account opening process into which these compliance controls are embedded; this skill focuses on the compliance layer, that skill on the operational flow
- **client-onboarding** (advisory-practice plugin): The broader client onboarding experience that encompasses account opening compliance as one component of the end-to-end onboarding process
- **privacy-data-security** (compliance plugin): Protection of sensitive personal information (SSN, financial data, identity documents) collected during the account opening compliance process
- **examination-readiness** (compliance plugin): Preparing account opening compliance documentation and procedures for regulatory examination
- **books-and-records** (compliance plugin): Recordkeeping requirements for CIP records, OFAC screening results, beneficial ownership certifications, and suitability documentation generated during account opening
- **sales-practices** (compliance plugin): Ongoing senior investor protections (FINRA Rules 2165/4512 temporary holds and conduct standards) that build on the trusted contact and senior-review infrastructure established at account opening
