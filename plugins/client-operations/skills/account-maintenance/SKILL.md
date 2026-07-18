---
name: account-maintenance
description: "Process account maintenance requests across the account lifecycle. Use when changing a client address or contact info with identity verification, updating beneficiary designations after marriage, divorce, birth, or death, re-registering or re-titling an account to a trust or new entity, selecting tax lot methods or fixing cost basis records, applying legal or compliance holds or Reg T freezes, setting up systematic withdrawals or standing instructions, processing a death notification and estate account setup, handling a QDRO, power of attorney, or guardianship, closing accounts and managing escheatment, or designing data quality review programs."
---

# Account Maintenance

## Core Concepts

### Contact Information Changes
Address and contact updates are among the most frequent account maintenance requests, but they carry meaningful fraud and elder abuse risk. Firms must balance client convenience with protective controls.

**Address change procedures:**
- **Client-initiated changes** may be submitted through the advisor, client portal, phone, or written request. Regardless of channel, the firm must verify the identity of the requesting party before processing the change. Common verification methods include knowledge-based authentication, callback to the phone number on file, or confirmation sent to the prior address or email.
- **Advisor-initiated changes** on behalf of a client should require documented client authorization. Verbal authorization must be noted with date, time, and the identity of the person providing authorization. Written or electronic authorization is preferred and creates a stronger audit trail.
- **Multi-system propagation** is a persistent operational challenge. When an address changes, the update must flow to all systems that store client contact data: CRM, custodian account master, correspondence system, billing system, and any third-party platforms. Failure to propagate consistently results in mail going to old addresses (privacy risk), incorrect tax form delivery (1099s, K-1s), and compliance exposure. Best practice is to designate a single system of record (typically CRM or custodian) and propagate changes outward via integration, rather than requiring manual updates in each system.
- **Temporary vs permanent changes** should be distinguished in the workflow. A client who is traveling or has a seasonal residence may need mail temporarily redirected without changing the legal address of record. The system should support a temporary address with an expiration date that reverts to the permanent address automatically.

**Third-party address change red flags:**
FINRA Regulatory Notice 07-43 and SEC guidance on senior investor protection highlight address changes as a key indicator of potential financial exploitation. Red flags that should trigger enhanced scrutiny include:
- Address change request from someone other than the account holder (especially if followed by a distribution request)
- Change to a P.O. Box when the prior address was a residential address
- Change to an address associated with a known bad actor or previously flagged account
- Multiple address changes in a short period
- Address change for a senior investor (age 65+) followed within 30 days by a large withdrawal or wire transfer
- Address change to a different state or country for a client with no known connection to that location

When a red flag is detected, the firm should place a temporary hold on the address change, contact the client at the prior contact information to confirm the request, and escalate to compliance or a designated senior investor protection contact if confirmation cannot be obtained.

**Notification requirements:**
Many custodians and regulatory expectations require that a confirmation of the address change be sent to both the old and new addresses. This dual notification provides the client an opportunity to detect an unauthorized change. The confirmation should include the date of the change, the new address, and instructions for contacting the firm if the change was not authorized.

### Beneficiary Management
Beneficiary designations determine the disposition of assets upon the account holder's death. Errors or omissions in beneficiary management are among the most consequential account maintenance failures because they are typically discovered only at death, when correction is impossible.

**Designation structure:**
- **Primary beneficiaries** receive assets first (percentages must total 100%); **contingent beneficiaries** receive assets only if all primaries predecease or disclaim.
- **Per stirpes vs per capita** — the election determines whether a predeceased beneficiary's share passes to their descendants (per stirpes) or redistributes to surviving beneficiaries (per capita). The operational requirement is to record the election explicitly on the custodian's form; an ambiguous or missing election is unresolvable at death.

**Beneficiary updates for life events:**
- **Marriage:** The client may want to add a spouse as primary beneficiary. For ERISA-governed retirement plans, the spouse is the default beneficiary unless the spouse provides written consent to a different designation. For IRAs and non-ERISA accounts, there is no automatic spousal beneficiary right, but advisors should prompt a review.
- **Divorce:** Beneficiary designations naming a former spouse are not automatically revoked by divorce in most states for non-ERISA accounts (the law varies by state and account type). The client must affirmatively update the designation. Failure to update after divorce is one of the most common and costly beneficiary errors. For ERISA plans, a QDRO may assign benefits to a former spouse regardless of the current designation.
- **Birth or adoption:** Clients should add new children as beneficiaries or adjust percentages. Per stirpes designations may automatically include new descendants, but per capita designations do not.
- **Death of a beneficiary:** If a primary beneficiary dies, the firm should notify the account holder and recommend updating the designation; the per stirpes/per capita election on file determines where the predeceased beneficiary's share goes.

**Retirement account beneficiary rules (SECURE Act):**
The SECURE Act of 2019 (and SECURE 2.0 Act of 2022) fundamentally changed inherited retirement account distribution rules:
- **Spouse beneficiaries** may roll the inherited account into their own IRA, treat it as their own, or take distributions over their life expectancy — the most flexible options.
- **Eligible designated beneficiaries** (minor children of the account holder, disabled or chronically ill individuals, individuals not more than 10 years younger than the deceased) may use the life expectancy method.
- **All other designated beneficiaries** (including adult children and non-spouse partners) must distribute the entire inherited account within 10 years of the account holder's death. There is no annual RMD requirement during the 10-year period if the account holder died before their required beginning date; if the account holder died after their required beginning date, annual distributions may be required within the 10-year window.
- **Non-designated beneficiaries** (estates, certain trusts, charities) follow either the 5-year rule or the deceased's remaining life expectancy, depending on whether the account holder died before or after the required beginning date.

These rules make beneficiary designation a critical planning decision. The choice between naming individuals, trusts, or other entities as beneficiaries has significant tax implications that should be coordinated with the tax-efficiency and financial-planning-integration skills.

**TOD/POD designations:**
TOD (brokerage) and POD (bank) designations pass assets to named beneficiaries outside probate and override the will — the operational requirements are to document the designation on the custodian's designated form, retain a copy, and flag the account for estate-planning coordination since a stale TOD silently defeats the client's will.

**Beneficiary review cadence:**
Best practice is to review beneficiary designations at every major life event and at minimum during the annual or biennial client review meeting. The firm should maintain a process to flag accounts with outdated or missing beneficiary designations — for example, accounts with no beneficiary on file, accounts where the designated beneficiary has a flagged death record, or accounts that have not had a beneficiary review in more than 3 years.

### Account Re-Registration and Re-Titling
Re-registration changes the legal ownership or titling of an account. This is operationally more complex than a simple data update because it affects the legal rights to the account assets, may trigger tax consequences, and typically requires custodian processing with supporting documentation.

**Common re-registration events:**
- **Individual to revocable trust:** The most frequent re-registration. Assets move from the individual's name into the trust's name. Because a revocable trust is a grantor trust (the individual retains control), this is generally not a taxable event. The trust uses the grantor's SSN as its TIN. Required documentation typically includes a trust certification, the account holder's written instruction, and (depending on the custodian) a medallion signature guarantee.
- **Name change (marriage or divorce):** The account title changes to reflect the new legal name. Required documentation: legal name change document (marriage certificate, court order), government-issued ID in the new name (or a combination of old ID plus name change document), updated W-9.
- **Joint to individual (death of co-owner):** For JTWROS accounts, the surviving owner becomes the sole owner. Required documentation: death certificate and letter of instruction from the surviving owner. The custodian removes the deceased owner's name from the account. For TIC accounts, the deceased owner's share passes to their estate, requiring a different process.
- **Individual to estate:** Upon death, the individual account may need to be re-titled to the estate while probate is underway. Required documentation: death certificate, letters testamentary or letters of administration, EIN for the estate.
- **Trust to beneficiaries (trust termination):** When a trust terminates per its terms, assets are distributed to trust beneficiaries. Required documentation: trustee certification of termination, distribution instructions, beneficiary identification and account setup.
- **Entity restructuring:** LLC converting to corporation, partnership changes, mergers. Required documentation: entity formation/conversion documents, corporate resolutions, updated operating agreements.

**Tax implications of re-registration:**
- **Cost basis transfer:** When assets are re-registered without a change in beneficial ownership (e.g., individual to revocable trust, name change), the cost basis carries over unchanged. The original acquisition dates and cost lots transfer to the new registration.
- **Step-up in basis:** When assets transfer due to death, the beneficiary generally receives a stepped-up cost basis equal to the fair market value of the assets on the date of death (or alternate valuation date if elected by the estate). This step-up eliminates unrealized capital gains that existed during the decedent's lifetime. Community property assets may receive a full step-up on both halves at the first spouse's death in community property states.
- **Taxable transfers:** Re-registration that constitutes a gift (e.g., transferring assets from parent to child) or a sale (e.g., transferring assets to an unrelated party) may trigger gift tax or capital gains tax. The firm should not provide tax advice but should flag these situations and recommend the client consult a tax advisor.

**Medallion signature guarantee requirements:**
A medallion signature guarantee is a certification by a financial institution that a signature is genuine and that the signer has the authority to execute the transaction. Medallion guarantees are commonly required for: transfers of securities to a different name or entity, requests to change account registration, physical stock certificate transfers, and certain large-value transactions. The three medallion guarantee programs are STAMP (Securities Transfer Agents Medallion Program), SEMP (Stock Exchanges Medallion Program), and MSP (NYSE Medallion Signature Program). Not all financial institutions participate in all programs; the firm must verify that the guarantee is from an institution participating in an accepted program.

**Custodian processing:**
Re-registration timelines vary significantly by custodian and complexity. Simple name changes may process in 1-3 business days. Trust re-registrations typically take 3-7 business days. Estate re-registrations and complex entity changes may take 1-4 weeks, particularly if the custodian's legal department must review trust or entity documents. During processing, the account may be in a restricted state where trading is limited. The firm should set client expectations regarding processing times and any trading restrictions during the re-registration period.

### Cost Basis Management
Accurate cost basis tracking is essential for tax reporting (1099-B), client tax planning, and regulatory compliance. The firm's obligations depend on whether shares are "covered" (acquired after the applicable effective date under the Emergency Economic Stabilization Act of 2008) or "uncovered."

**Tax lot accounting methods:**
- **Specific identification (Spec ID):** The client or advisor selects which specific tax lots to sell. This provides maximum tax control — the ability to choose lots with the highest cost basis (minimizing gains) or lowest basis (harvesting losses). Requires lot-level identification at the time of the trade, either proactively or within the settlement period.
- **First In, First Out (FIFO):** The oldest shares are deemed sold first. This is the IRS default method if no other method is elected. FIFO tends to produce long-term capital gains (favorable tax rates) but may not minimize total tax liability.
- **Last In, First Out (LIFO):** The most recently acquired shares are deemed sold first. This tends to produce short-term capital gains but may result in lower gain amounts if recent purchases were at higher prices.
- **Highest In, First Out (HIFO):** The shares with the highest cost basis are deemed sold first. This minimizes realized gains and is often the preferred method for taxable accounts focused on tax efficiency.
- **Average cost:** Available only for mutual fund shares and shares acquired through dividend reinvestment plans. The average cost of all shares is used as the basis for each share sold. Once elected for a specific fund, average cost applies to all shares of that fund in the account.

**Cost basis transfer rules:**
- **ACATS transfers:** Cost basis transfer mechanics between firms (covered vs uncovered shares, the CBRS 15-day window, IRC Section 6045A) are covered in account-transfers; the maintenance-side obligation is to verify the received basis against client records and resolve discrepancies promptly.
- **Re-registration transfers:** Cost basis carries over in non-taxable re-registrations (e.g., individual to revocable trust). For transfers due to death, the receiving account should reflect the stepped-up basis as of the date of death.
- **Gift transfers:** The recipient generally takes the donor's cost basis (carryover basis) for gains. If the fair market value at the time of gift is less than the donor's basis, special rules apply for determining basis for loss purposes (the basis is the FMV at the date of the gift).

**Corporate action adjustments:**
Corporate actions frequently alter cost basis, and errors in corporate action processing are a leading source of cost basis inaccuracies:
- **Stock splits and reverse splits:** The total cost basis remains the same; per-share basis adjusts proportionally. A 2-for-1 split halves the per-share basis; a 1-for-10 reverse split multiplies per-share basis by 10.
- **Mergers and acquisitions:** If the merger is a tax-free reorganization (stock-for-stock exchange), the cost basis of the old shares carries over to the new shares, allocated proportionally. If the merger involves cash consideration (cash-and-stock deal), the cash portion is taxable and reduces the basis allocated to the new shares.
- **Spin-offs:** The cost basis of the parent company shares is allocated between the parent and the spun-off entity based on the relative fair market values on the distribution date. The IRS typically provides allocation guidance or the companies publish allocation percentages.
- **Return of capital distributions:** Reduce the cost basis of the shares. If return of capital exceeds the cost basis, the excess is treated as capital gain. Accurate tracking of return of capital distributions over time is critical for partnerships, REITs, and MLPs.

**Wash sale tracking:**
The wash sale rule (IRC Section 1091) disallows a loss deduction if substantially identical securities are purchased within 30 days before or after the sale. The disallowed loss is added to the cost basis of the replacement shares. Firms must track wash sales within the same account and, for tax reporting purposes, across all accounts of the same taxpayer at the firm. Cross-account and cross-firm wash sale tracking remains the taxpayer's responsibility, but the firm should provide tools and reporting to assist.

**Covered vs uncovered shares and 1099-B reporting:**
For covered shares, the broker is required to report cost basis to the IRS on Form 1099-B and to apply the client's elected accounting method. For uncovered shares, the broker reports the sale proceeds but is not required to report cost basis (Box 1e is left blank). The client is responsible for reporting basis on their tax return for uncovered shares. The firm should maintain whatever historical basis records it has for uncovered shares and make them available to clients, but the obligation to report accurate basis to the IRS rests with the taxpayer.

### Account Restrictions and Holds
Restrictions limit or prevent transactions on an account. They may be imposed by the firm, a regulator, a court, or by operation of law. Proper restriction management protects the firm from liability and ensures compliance with legal and regulatory requirements.

**Types of restrictions:**
- **Death notification hold:** Upon receipt of a death notification, the firm must immediately restrict the deceased's accounts to prevent unauthorized transactions. No new trades, distributions, or changes should be processed until the firm receives appropriate legal documentation (death certificate, letters testamentary/administration, or beneficiary claim forms). Joint accounts with rights of survivorship are an exception — the surviving owner retains trading authority, but the deceased's name must be removed via re-registration.
- **Divorce/domestic relations hold:** When the firm receives a divorce decree or court order related to a domestic dispute, affected accounts may be restricted pending asset division. The restriction should prevent both parties from making withdrawals or transfers until the division is executed per the court order. QDRO processing for retirement accounts requires special handling (see Life Event Processing below).
- **Legal hold (litigation/subpoena):** A legal hold preserves account records and may restrict transactions when the firm receives a subpoena, litigation hold notice, or regulatory investigation notification. The hold prevents destruction of relevant records and may restrict the account holder's ability to close the account or transfer assets.
- **Compliance hold:** The firm's compliance department may restrict an account pending investigation of suspicious activity (SAR filing), suitability concerns, or other compliance issues. The restriction scope is determined by the nature of the concern — it may be a full freeze or limited to specific transaction types.
- **Reg T freeze:** Under Regulation T, if a client purchases securities and fails to pay for them by the payment date (settlement date), the account may be frozen for 90 days. During the freeze, the client can only purchase securities if the full purchase price is deposited in advance (cash before trade). The restriction is lifted after 90 days or upon application to the firm's credit department.
- **Margin restriction:** When a margin account is in a margin call (maintenance call, Reg T call, or house call) and the client fails to meet the call, the firm may restrict trading to liquidation-only until the call is met.
- **OFAC match:** If an account holder or associated party matches a name on the OFAC Specially Designated Nationals (SDN) list, the account must be blocked (frozen) immediately. All assets in the account are blocked and no transactions may be processed. The firm must file a blocking report with OFAC within 10 business days. The block remains until OFAC provides a specific license to unblock or the match is resolved as a false positive.
- **Garnishment and levy:** When the firm receives a valid garnishment order, tax levy (IRS or state), or attachment order from a court or government agency, the firm must comply by freezing the specified amount and/or remitting funds as directed. Retirement accounts have limited protection under ERISA and state law, requiring careful analysis before responding to a garnishment.

**Restriction application and removal procedures:**
Restrictions should be applied immediately upon receipt of the triggering event (death notification, court order, compliance directive). The restriction should be documented in the account master record and visible to all users who access the account, including advisors, operations staff, and client service representatives. Removal of restrictions requires documented authorization: compliance sign-off for compliance holds, receipt of legal documentation for death and divorce holds, passage of time for Reg T freezes, and OFAC license or false positive determination for OFAC blocks.

### Standing Instructions
Standing instructions are pre-authorized, recurring or default instructions on an account that execute automatically without requiring individual authorization for each occurrence.

**Common standing instruction types:**
- **Systematic withdrawal plan (SWP):** Periodic distributions from the account (monthly, quarterly, annually) in a fixed dollar amount or percentage. Common for retirement income accounts. The plan should specify the source (which holdings to sell or cash to distribute), the distribution method (check, ACH, wire), and tax withholding elections (federal and state).
- **Automatic investment plan (AIP):** Periodic contributions to the account, typically via ACH from a bank account, invested according to a specified allocation (model portfolio, specific funds, or dollar-cost averaging into specified securities).
- **Dividend reinvestment (DRIP):** Elections to reinvest dividends and capital gains distributions rather than receiving cash. DRIP elections may be set at the account level (all holdings) or at the individual security level. Reinvested shares create new tax lots at the reinvestment price.
- **Fee debit instructions:** Authorization for the firm to deduct advisory fees directly from the account. The instruction should specify the fee schedule, billing frequency (monthly, quarterly), and the billing source (which account to debit if the client has multiple accounts). SEC guidance requires that the fee authorization be documented in writing and that the client receive advance notice of fee debits.
- **Cash sweep instructions:** Direction for uninvested cash to be automatically swept into a designated vehicle — money market fund, bank deposit program (FDIC-insured sweep), or interest-bearing cash account. Sweep elections are typically set at account opening but may be changed.
- **Standing wire/ACH instructions:** Pre-authorized instructions for recurring or on-demand transfers to a specific external account (bank account, third-party account). Standing wire instructions reduce fraud risk by limiting wire destinations to pre-verified accounts. Adding a new wire destination should require enhanced verification (callback, written authorization, hold period before first use).

**Instruction modification procedures:**
Modifications to standing instructions should follow the same identity verification procedures as other account changes. Changes to fee debit instructions and distribution methods should be documented in writing. The firm should maintain an audit trail of all instruction changes, including the prior instruction, the new instruction, the date of change, and the identity of the requesting party and the processor.

### Life Event Processing
Life events trigger complex, multi-step account maintenance workflows that cut across multiple accounts and registration types. These events have legal, tax, and operational dimensions that require coordinated processing.

**Death notification and estate processing:**
1. **Receive and verify the death notification.** The firm may learn of a death from a family member, advisor, estate attorney, or obituary monitoring service. The firm should verify the notification by requesting a certified death certificate. A verbal notification is sufficient to trigger an immediate account restriction, but documentation is required before any further processing.
2. **Restrict all accounts.** Upon notification, immediately restrict all accounts in the deceased's name — individual accounts, the deceased's interest in joint accounts, retirement accounts, and any accounts where the deceased was an authorized party. For JTWROS accounts, the surviving owner retains access but the account must be re-registered.
3. **Identify account types and disposition paths.** Each account type follows a different disposition path:
   - *Individual taxable accounts:* Assets pass to the estate (if no TOD) or to TOD beneficiaries (if TOD is on file). Estate distribution requires letters testamentary.
   - *Joint accounts (JTWROS):* Assets pass to the surviving owner automatically. Re-register by removing the deceased's name upon receipt of the death certificate.
   - *Joint accounts (TIC):* The deceased's proportional share passes to their estate. The surviving owner retains their share.
   - *Retirement accounts (IRA, 401k):* Assets pass to the named beneficiary per the beneficiary designation on file. Beneficiary claims require the death certificate and a beneficiary claim form. Inherited IRA accounts must be established for each beneficiary.
   - *Trust accounts:* Disposition depends on the trust terms. The successor trustee takes control upon the death of the original trustee. If the trust terminates, assets are distributed to trust beneficiaries per the trust instrument.
   - *TOD accounts:* Assets transfer directly to named TOD beneficiaries upon receipt of the death certificate and beneficiary claim forms, bypassing probate.
4. **Process beneficiary claims and estate distributions.** For each account, collect the required documentation (death certificate, beneficiary claim form, letters testamentary, trust certification of successor trustee) and process the transfer or distribution. Establish new accounts as needed (inherited IRA for each beneficiary, estate account for the personal representative).
5. **Adjust cost basis.** Apply the step-up in basis to all assets as of the date of death (or alternate valuation date). Update cost basis records in the account master and portfolio management system.
6. **Tax reporting.** The deceased's final 1099 covers activity from January 1 through the date of death. Subsequent activity is reported under the estate's EIN or the beneficiary's SSN, depending on how and when assets are distributed.

**Divorce decree processing:**
- **Non-retirement accounts:** The divorce decree or marital settlement agreement specifies how accounts are divided. The firm processes the division by transferring the specified assets or dollar amounts to the receiving spouse's account. If the receiving spouse does not have an account, one must be opened. The transfer between spouses incident to divorce is not a taxable event (IRC Section 1041); cost basis carries over to the receiving spouse.
- **Retirement accounts — QDRO:** Division of ERISA-governed retirement plan assets requires a Qualified Domestic Relations Order (QDRO). The QDRO must be reviewed and accepted by the plan administrator. For IRAs (which are not ERISA-governed), a transfer incident to divorce is processed per the divorce decree without a QDRO, pursuant to IRC Section 408(d)(6).
- **Account restrictions during divorce:** The firm should restrict affected accounts upon receiving a court order or notification from either party's attorney. Restrictions prevent either party from depleting assets before the division is executed.

**Marriage processing:**
- **Name change:** Process the name change re-registration with supporting documentation (marriage certificate, updated ID).
- **Beneficiary review:** Prompt the client to review and update beneficiary designations on all accounts.
- **Account consolidation:** If both spouses have accounts at the firm, they may wish to establish joint accounts or consolidate household accounts. New joint account opening follows standard onboarding procedures.

**Incapacity:**
- **Power of attorney (POA):** A POA grants an agent authority to act on the account holder's behalf. The firm must review the POA document to confirm it grants authority over financial accounts, verify the agent's identity, and determine whether the POA is durable (survives incapacity) or springs into effect only upon incapacity. Many custodians have specific POA acceptance requirements and may require their own POA form.
- **Guardianship/conservatorship:** A court-appointed guardian or conservator presents court documentation granting authority over the incapacitated person's financial affairs. The firm must verify the court order, confirm its scope and jurisdiction, and establish the guardian/conservator as the authorized party on the account. Transactions by the guardian/conservator may be subject to court oversight and reporting requirements.
- **Senior investor protections:** The FINRA Rule 2165 temporary-hold safe harbor and Rule 4512 trusted contact requirements are covered in account-opening-compliance; operationally, when exploitation is suspected during a maintenance request, place the disbursement hold, notify the trusted contact, and document the basis for the hold.

### Account Closure
Account closure is the final stage of the account lifecycle. Whether voluntary or involuntary, the closure process must ensure complete asset disposition, final billing, and regulatory-compliant record retention.

**Voluntary closure:**
The account holder (or authorized party) requests closure. The firm processes the request by: (1) confirming the client's identity and authorization, (2) determining asset disposition — transfer to another firm via ACAT, liquidation and check/wire, or in-kind transfer to a specific account, (3) processing final fee billing and any outstanding charges, (4) generating final account statements and tax documents, and (5) closing the account in the custodian and internal systems. The firm should document the reason for closure (client-provided or advisor-noted) for business analytics and regulatory purposes.

**Involuntary closure:**
The firm may close an account without the holder's request in certain circumstances: prolonged inactivity (no activity and zero or de minimis balance for a defined period), failure to provide required documentation (CIP/KYC deficiencies), compliance determination (AML concerns, pattern of trading violations, unsuitable activity), or business decision (exiting a client segment, platform consolidation). Involuntary closure requires advance written notice to the account holder (typically 30 days), an opportunity for the client to transfer assets, and compliance review and approval.

**Abandoned property (escheatment):**
State unclaimed property laws require firms to identify and report abandoned accounts — accounts with no client-initiated activity for the state's dormancy period (typically 3-5 years, varying by state and property type). Before escheatment, the firm must conduct due diligence to locate the account holder (mailing, email, phone attempts, database searches). If the owner cannot be located, the assets are remitted to the state of the owner's last known address (or the firm's state of incorporation if no address is on file). Escheatment processing requires careful tracking because each state has different dormancy periods, due diligence requirements, reporting deadlines, and remittance procedures.

**Record retention post-closure:**
Closing an account does not terminate the firm's recordkeeping obligations. SEC Rule 17a-4 (broker-dealers) and Rule 204-2 (investment advisers) require retention of account records for specified periods after the account is closed — generally 6 years for most account records. The firm must maintain access to closed account records for regulatory examinations, client inquiries, and potential litigation. Records should be archived in a searchable, retrievable format.

## Worked Examples


Three worked examples — an individual-to-revocable-trust re-registration (including the close-and-reopen cost basis reset gotcha), a multi-account death notification across five registration types (JTWROS, IRA spousal rollover, trust succession, step-up processing), and a firm-wide data quality review program — are in [references/examples.md](references/examples.md); load it when processing a concrete re-registration, death notification, or data remediation project.

## Common Pitfalls
- Processing an address change without adequate identity verification, enabling unauthorized changes or elder financial exploitation
- Failing to update beneficiary designations after a divorce — the former spouse may inherit retirement account assets if the designation is not changed, regardless of the divorce decree (for non-ERISA accounts in most states)
- Re-registering an account as a close-and-reopen rather than a title change, which can reset cost basis records and create phantom taxable events
- Applying the wrong tax lot accounting method after an ACATS transfer because the receiving firm's default differs from the client's prior election
- Not placing an immediate restriction on all of a deceased client's accounts upon death notification, allowing unauthorized transactions
- Processing a power of attorney without verifying that the document grants authority over financial accounts and that the POA is durable (survives incapacity)
- Failing to distinguish between covered and uncovered shares when processing cost basis transfers, leading to incorrect 1099-B reporting
- Allowing a standing wire instruction to be added or changed without enhanced verification (callback, hold period), creating wire fraud exposure
- Not tracking return-of-capital distributions on partnerships, REITs, and MLPs, leading to overstated cost basis and incorrect gain/loss calculations
- Processing estate distributions before receiving letters testamentary or letters of administration, exposing the firm to liability if the distribution is challenged
- Neglecting escheatment obligations for dormant accounts, resulting in regulatory penalties from state unclaimed property audits
- Treating all joint accounts the same upon a co-owner's death — JTWROS and TIC accounts have fundamentally different disposition rules

## Cross-References
- **account-opening-workflow** (client-operations plugin): Account opening establishes the initial registration, beneficiary designations, and standing instructions that this skill maintains throughout the account lifecycle
- **books-and-records** (compliance plugin): Recordkeeping obligations for account maintenance documentation, including retention of change requests, authorizations, and correspondence per SEC Rules 17a-3/17a-4 and Rule 204-2
- **privacy-data-security** (compliance plugin): Address changes, contact updates, and account data maintenance involve nonpublic personal information protected by Reg S-P; data quality processes must comply with privacy requirements
- **tax-efficiency** (wealth-management plugin): Cost basis management, tax lot accounting method selection, and step-up in basis processing directly affect tax-efficient investing outcomes
- **client-onboarding** (advisory-practice plugin): Onboarding collects the initial data (beneficiaries, suitability, contact information) that account maintenance keeps current throughout the relationship
- **corporate-actions** (client-operations plugin): Corporate actions (splits, mergers, spin-offs, return of capital) alter cost basis and require coordination with the cost basis management processes described in this skill
- **account-transfers** (client-operations plugin): ACATS and non-ACATS transfers interact with cost basis transfer rules and re-registration procedures; transfer processing often triggers account maintenance updates at the receiving firm
