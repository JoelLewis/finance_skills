# Worked Examples — Client Onboarding

## Table of Contents

1. [Designing a Digital Onboarding Flow for Individual Taxable Accounts](#example-1-designing-a-digital-onboarding-flow-for-individual-taxable-accounts) — Schwab/Salesforce/Orion integration, identity verification, pre-submission validation, 3-day time-to-funded target
2. [Onboarding a Trust Account for a High-Net-Worth Client](#example-2-onboarding-a-trust-account-for-a-high-net-worth-client) — irrevocable trust beneficial ownership, multi-account onboarding event, EDD and supervisory review
3. [Reducing a 35% NIGO Rate](#example-3-reducing-a-35-nigo-rate) — NIGO categorization, validation rules engine, automated document assembly, phased remediation

## Example 1: Designing a digital onboarding flow for individual taxable accounts
**Scenario:** A mid-sized RIA with $2B AUM and 50 advisors wants to implement digital onboarding for individual taxable accounts. The firm uses Schwab as its primary custodian, Salesforce as its CRM, and Orion as its portfolio management system. Currently, onboarding is paper-based, takes 7-10 business days, and has a 22% NIGO rate. The firm wants to reduce time-to-funded-account to under 3 business days and NIGO rate below 5%.

**Design Considerations:**
- The onboarding platform must integrate with Schwab's account opening API, Salesforce for client data pre-population, and Orion for model portfolio assignment
- Identity verification should use a database verification vendor (such as Alloy or LexisNexis) as the primary method, with document verification (ID upload) as fallback
- OFAC screening must be integrated as an automated gate that runs immediately after identity data is collected
- The suitability questionnaire should combine psychometric risk tolerance questions with financial data collection, producing a risk score that maps to the firm's model portfolios
- Document generation should be fully automated: the system assembles the Schwab new account form, W-9, advisory agreement, Form CRS, privacy notice, and trusted contact designation, pre-populated with collected data
- E-signature should be embedded in the onboarding flow (not email-based) to minimize drop-off, using DocuSign or Schwab's native e-signature
- Real-time validation must check for common NIGO causes before custodian submission: name consistency, SSN format, complete address, all required signatures present
- After Schwab returns the account number, the system should automatically initiate ACH funding (if the client linked a bank account during onboarding) and notify Orion to assign the account to the model portfolio matching the client's risk score

**Analysis:** The recommended flow is: (1) advisor initiates onboarding from Salesforce, pre-populating known client data; (2) client receives a secure link to complete onboarding digitally; (3) client enters personal information and the system runs real-time identity verification and OFAC screening; (4) client completes the suitability questionnaire and the system generates a risk score; (5) system presents the recommended model portfolio and the advisor confirms; (6) document package is generated and the client signs electronically; (7) system validates the complete package against Schwab's requirements; (8) application is submitted to Schwab via API; (9) Schwab returns the account number; (10) ACH funding is initiated and Orion receives the new account for model assignment. For the 22% NIGO rate, the primary remediation is step 7 — pre-submission validation that catches the errors Schwab would reject. Common causes like name mismatches, missing signatures, and incomplete forms can be caught in real time. The 3-business-day target is achievable for the digital path: identity verification and document signing can occur in a single session (day 1), Schwab API submission processes within hours (day 1-2), and ACH funding settles in 2-3 business days (day 2-3).

## Example 2: Onboarding a trust account for a high-net-worth client
**Scenario:** An advisor at a registered investment adviser is onboarding a new high-net-worth client who wants to invest $5M through a family irrevocable trust. The trust was established 3 years ago, has its own EIN, and names the client and her attorney as co-trustees. The trust has four beneficiaries (the client's adult children). The client also wants a personal taxable account and a Roth IRA.

**Design Considerations:**
- The irrevocable trust is a legal entity requiring full beneficial ownership certification under the FinCEN CDD Rule: identify all individuals owning 25% or more of the trust's beneficial interests and at least one control person
- With four beneficiaries who are the beneficial interest holders, the firm must determine if any owns 25% or more. If the trust splits evenly (25% each), all four meet the threshold and must be identified. The control persons are the co-trustees (the client and her attorney)
- The trust requires its own EIN, a trust certification (or relevant pages of the trust agreement showing formation, trustees, and investment powers), and verification that the trustees have authority to open investment accounts
- Enhanced due diligence considerations: $5M meets most firms' high-net-worth thresholds for supervisory review; irrevocable trust is a complex structure warranting additional scrutiny of the trust's purpose and source of funds
- The personal taxable account and Roth IRA can follow the standard individual onboarding flow; identity verification for the client carries across all three accounts
- Document packages differ substantially: the trust account requires the new account form in the trust's name, W-9 with the trust's EIN, trust certification, beneficial ownership form, and advisory agreement naming the trust as the client; the taxable account requires standard individual forms with the client's SSN; the Roth IRA requires the IRA adoption agreement, beneficiary designation, and IRA disclosure statement
- All three accounts should be linked to a single household in the CRM and PMS for consolidated reporting

**Analysis:** The onboarding workflow should handle this as a single onboarding event with multiple account openings. Start with client identity verification (CIP), which satisfies requirements for the individual accounts and verifies one of the trustees for the trust account. Then collect suitability data for each account (the trust may have different investment objectives than the personal accounts). Next, request the trust documentation: the full trust certification, trust EIN assignment letter, and identification information for the co-trustee (attorney) and all four beneficiaries. Run OFAC screening on all individuals (client, attorney co-trustee, four beneficiaries — six people total). Complete the FinCEN beneficial ownership certification form. Route the trust account application through supervisory review given the complexity and dollar amount. Generate three separate document packages, one per account. The trust account will likely require manual or semi-automated submission to the custodian even if the individual accounts can use API submission, due to the additional documentation. Expect the trust account to take 1-2 weeks from submission to account opening, while the individual accounts can be opened within days. Funding the trust account via wire transfer is common for this dollar amount; the taxable account can be funded via ACAT if the client has an existing brokerage account elsewhere; the Roth IRA may involve a rollover or contribution depending on the source of funds.

## Example 3: Reducing a 35% NIGO rate
**Scenario:** A broker-dealer and RIA with 200 advisors processes 500 new account applications per month through a combination of custodians (Schwab, Fidelity, Pershing). The firm's current NIGO rate is 35%, meaning 175 applications per month are rejected on first submission. Average remediation time for a NIGO rejection is 5 business days, and the operations team spends 60% of its time on NIGO resolution. The firm wants to reduce the NIGO rate to under 10%.

**Design Considerations:**
- First priority is to categorize existing NIGO rejections by cause. Common categories: missing signatures (often 20-30% of NIGOs), data inconsistencies between forms (15-25%), missing or expired documents (15-20%), incorrect account type coding (10-15%), incomplete beneficiary designations (5-10%), missing beneficial ownership for entities (5-10%)
- Each custodian has different form requirements and validation rules; the firm must maintain a rules engine that knows each custodian's specific requirements
- The root cause is often that advisors complete forms manually with no real-time validation, and errors are not caught until the custodian reviews the application days later
- Multi-custodian complexity amplifies the problem: advisors must know which forms and requirements apply to each custodian, and mistakes are more likely when switching between custodians

**Analysis:** A phased approach to reducing the NIGO rate from 35% to under 10%:

Phase 1 — Diagnose (weeks 1-2): Categorize the last 6 months of NIGO rejections by custodian, account type, rejection reason, and originating advisor. Identify the top 5 rejection reasons, which will typically account for 70-80% of all NIGOs. Identify whether certain advisors or offices have disproportionately high NIGO rates (indicating a training issue vs a systemic issue).

Phase 2 — Implement pre-submission validation (weeks 3-8): Build a validation rules engine that checks every application against the applicable custodian's requirements before submission. Critical validations: all required fields populated, signatures present on all required pages, name and SSN/TIN consistent across all forms, account type code matches the application data, beneficiary designation complete for retirement accounts, beneficial ownership form included for entity accounts, required supporting documents attached (trust certification, formation documents). The validation engine should prevent submission until all checks pass and provide clear error messages to the advisor or operations team.

Phase 3 — Automate document assembly (weeks 6-12): Replace manual form completion with automated document generation that pre-populates custodian-specific forms from a single data collection workflow. This eliminates the majority of data inconsistency errors because data is entered once and propagated to all forms. Support all three custodians with custodian-specific form templates and validation rules.

Phase 4 — Train and monitor (ongoing): Provide targeted training to advisors with high NIGO rates. Publish a weekly NIGO dashboard showing rates by custodian, account type, rejection reason, and advisor. Set NIGO rate targets (under 15% at 90 days, under 10% at 180 days) and review progress monthly.

Expected outcome: Pre-submission validation alone typically reduces NIGO rates by 50-60% (from 35% to 14-17%). Adding automated document assembly reduces the remaining errors by another 50% or more (to 7-10%). The combined effect should achieve the sub-10% target within 6 months, freeing the operations team to focus on complex account types rather than routine error remediation.
