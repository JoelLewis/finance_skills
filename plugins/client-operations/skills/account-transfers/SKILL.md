---
name: account-transfers
description: "Account transfers: ACAT transfers, non-ACAT transfers, partial transfers, journal entries, rollovers, estate transfers, and transfer tracking for brokerage operations."
allowed-tools: ["Bash", "Read", "Write", "Edit"]
---

# Account Transfers

## Purpose
Guide the processing and management of account transfers between financial institutions and within firms. Covers ACAT (Automated Customer Account Transfer) system, non-ACAT transfers, partial transfers, internal journal entries, retirement account rollovers, estate transfers, and transfer tracking. Enables designing and operating transfer processes that are efficient, accurate, and compliant with FINRA and ACATS rules.

## Layer
12 — Client Operations (Account Lifecycle & Servicing)

## Direction
both

## When to Use
- Processing or designing workflows for full or partial ACAT transfers between broker-dealers
- Handling non-ACAT transfers such as mutual fund direct transfers, DTC free deliveries, or physical certificate movements
- Setting up internal journal entries to move assets between accounts within the same firm
- Processing retirement account rollovers (direct, indirect, Roth conversions) and ensuring proper tax reporting
- Managing estate transfers from decedent accounts to beneficiaries or estate accounts
- Tracking transfer status, handling rejections, and managing escalation procedures
- Reconciling assets after transfer completion and processing residual credits or fractional shares
- Evaluating ACAT-eligible vs ineligible assets and determining alternative transfer methods for ineligible positions
- Advising on cost basis transfer requirements and tax lot selection during partial transfers
- Designing transfer tracking dashboards and client communication workflows
- Troubleshooting common ACAT rejection codes and determining remediation steps
- Handling margin account transfers and understanding the impact on margin balances and requirements
- Coordinating multi-account household transfers where different account types require different transfer mechanisms
- Ensuring compliance with FINRA Rule 11870 timelines for both receiving and delivering firm obligations
- Processing cost basis step-up calculations for estate transfers and documenting date-of-death valuations

## Core Concepts

### ACAT Transfer System
The Automated Customer Account Transfer Service (ACATS) is operated by DTCC's National Securities Clearing Corporation (NSCC) and provides a standardized, automated mechanism for transferring customer accounts between broker-dealers and banks. ACATS is the primary system for transferring brokerage accounts in the United States and is governed by FINRA Rule 11870 (Customer Account Transfer Contracts).

**How ACATS works — the transfer lifecycle:**

1. **Transfer Initiation (Day 0)** — The customer signs a Transfer Initiation Form (TIF) authorizing the transfer. The receiving firm submits the transfer request through ACATS, specifying whether the transfer is full or partial and listing the assets to be transferred.
2. **Validation (Days 1-3)** — The delivering firm receives the transfer request and has 3 business days to validate the account information and asset positions. The delivering firm must verify the customer's identity, account number, SSN/TIN, and the assets listed in the request. If the information matches, the delivering firm validates the request. If there are discrepancies, the delivering firm may reject the request with a specific reject code.
3. **Asset Transfer (Days 4-6)** — Once validated, the delivering firm must transfer the account assets within 3 business days (6 business days total from initiation). ACATS coordinates the settlement of securities between the firms through NSCC. Cash balances are transferred via the Federal Reserve wire system or NSCC settlement.
4. **Residual Processing (Days 7+)** — After the primary transfer completes, the delivering firm processes residual items: dividends or interest that were accrued but not yet paid, fractional shares (typically liquidated and sent as a residual credit), reorganization proceeds, and any other items that could not be transferred on the primary settlement date.

**Full ACAT vs partial ACAT:**
- A **full ACAT** transfers the entire account — all positions, cash, and account features. The delivering firm closes the account after transfer completion. Full ACATs are the most common transfer type and benefit from the highest degree of automation.
- A **partial ACAT** transfers only specified positions and/or cash amounts. The account remains open at the delivering firm with the remaining positions. Partial ACATs require the receiving firm to specify exactly which positions and quantities to transfer. Partial ACATs are used when a client wants to consolidate specific holdings, when certain assets are ineligible for ACAT transfer, or when the client is maintaining accounts at both firms.

**ACAT-eligible vs ineligible assets:**
- **Eligible:** Equities (common stock, preferred stock, ADRs), fixed income (corporate bonds, municipal bonds, treasury securities), options (listed options — transferred with assignment of the Options Clearing Corporation position), mutual funds (if the fund is available on the receiving firm's platform), ETFs, unit investment trusts, and cash balances.
- **Ineligible or restricted:** Proprietary products of the delivering firm (proprietary mutual funds, structured notes), limited partnerships and direct participation programs (often require manual transfer), annuities (transferred directly between insurance carriers, not through ACATS), physical certificates held outside DTC, bank deposits (CDs, money market deposit accounts at the bank level), alternative investments (hedge funds, private equity — transferred via assignment or redemption/re-subscription), 529 plan accounts, and certain foreign securities not held at DTC.

When a full ACAT encounters ineligible assets, those assets remain at the delivering firm in a residual account while all eligible assets transfer. The receiving firm and client must then coordinate the manual transfer of ineligible assets or the client must decide whether to liquidate them.

**Transfer Initiation Form (TIF):**
The TIF is the customer's written authorization for the transfer. It must include: customer name, SSN/TIN, delivering firm account number, receiving firm account number, transfer type (full or partial), and for partial transfers, the specific assets and quantities to be transferred. The customer's signature on the TIF is required. Many firms now accept electronic signatures on TIFs. The receiving firm retains the TIF as part of its account records and must produce it upon regulatory request.

**Receiving firm responsibilities:**
- Obtain the signed TIF from the customer
- Submit the ACATS transfer request within one business day of receiving the completed TIF
- Ensure the account is open and properly registered at the receiving firm before submitting the transfer request
- Monitor the transfer status and communicate progress to the customer
- Reconcile received assets against the expected transfer and investigate discrepancies
- Process residual credits as they arrive from the delivering firm

**Delivering firm responsibilities (FINRA Rule 11870):**
- Validate or reject the transfer request within 3 business days — the delivering firm cannot unreasonably delay or refuse a valid transfer request
- Complete the transfer of assets within 3 business days after validation (6 business days total)
- Process and forward residual items (dividends, interest, fractional share proceeds) promptly after the transfer
- Provide cost basis information for transferred securities as required by IRS regulations
- Not charge unreasonable fees for account transfers (FINRA prohibits fees designed to discourage transfers)

### Non-ACAT Transfers
Not all asset movements between firms use the ACATS system. Non-ACAT transfers are used for assets ineligible for ACATS, transfers between non-ACATS-participating institutions, and situations where alternative transfer mechanisms are more appropriate.

**Mutual fund direct transfers (NSCC Fund/SERV):**
Mutual fund shares can be transferred between firms through NSCC's Fund/SERV system without going through ACATS. This is commonly used when the receiving firm has a direct relationship with the fund company. Fund/SERV transfers typically settle in 1-3 business days and preserve the original purchase date, cost basis, and share lot information. The receiving firm submits a transfer request through Fund/SERV, and the fund company re-registers the shares in the receiving firm's name.

**DTC free delivery:**
A DTC free delivery (also called a free receipt/free delivery or DTC transfer) moves securities between DTC participant accounts without a corresponding cash payment. This is used for in-kind transfers where no sale is involved, such as gifting securities, moving positions between related accounts at different firms, or charitable donations of appreciated stock. The delivering firm initiates the delivery through DTC's Deposit/Withdrawal at Custodian (DWAC) system, and the receiving firm must confirm receipt. DTC deliveries typically settle same-day or next-day.

**Physical certificate transfers:**
When securities are held in physical certificate form (increasingly rare but still encountered), the transfer process requires: the certificate to be submitted to the transfer agent with a stock power (signed assignment form) and a medallion signature guarantee. The transfer agent re-registers the shares in the new owner's name and issues a new certificate or deposits the shares into DTC in book-entry form. Medallion Signature Guarantee programs (STAMP, SEMP, MSP) provide the guarantee, and only eligible financial institutions (banks, broker-dealers, credit unions) can provide them. Physical transfers can take 2-4 weeks.

**Alternative investment transfers:**
- **Limited partnerships:** Transferred by assignment — the general partner must approve the transfer. The receiving firm must verify it can hold the partnership interest on its books (many firms restrict which alternative investments they will custody). Transfer may take 4-8 weeks due to GP approval requirements.
- **Hedge funds:** Typically cannot be transferred in-kind. The investor redeems from the fund (subject to redemption terms, lock-up periods, and gate provisions) and re-subscribes at the new firm. Alternatively, some prime brokers can transfer hedge fund positions between accounts.
- **Private placements:** Transferred by assignment or novation, requiring issuer consent. Transfer documentation includes assignment agreements and updated subscription documents.

**International transfers:**
Cross-border transfers involve additional complexity: SWIFT messaging for international wire transfers, correspondent banking relationships, foreign exchange conversion, regulatory considerations (OFAC screening, tax treaty withholding), and potentially different settlement conventions. International security transfers may use Euroclear or Clearstream for European securities, or bilateral arrangements between custodians for other markets.

**Wire transfers for cash:**
Cash-only transfers between firms are typically executed via Fedwire (domestic) or SWIFT (international). Wire transfers settle same-day for domestic transfers initiated before the cutoff time. The receiving firm must verify the wire instructions and authenticate the source. For large wire transfers, firms typically require verbal confirmation and callback verification.

### Partial Transfers
Partial transfers require additional planning because the client is selectively moving specific positions while leaving others in place. This creates considerations around tax lots, cost basis, margin impact, and documentation.

**Selecting specific positions:**
The receiving firm must specify each position to be transferred, including CUSIP, quantity, and for fixed income, par value. The client and advisor should review the full account holdings to determine which positions to transfer and which to leave behind. Common reasons for partial transfers: consolidating duplicate positions held at multiple firms, moving specific asset classes to a specialist manager, transferring appreciated positions for tax-loss harvesting at the new firm, and retaining positions that are ineligible for transfer.

**Tax lot selection implications:**
When transferring a partial position (some but not all shares of a security), the delivering firm must determine which tax lots to transfer. If the account uses specific identification as its tax lot method, the client should specify which lots to move. If the account uses FIFO, the earliest-acquired lots transfer first. The choice of which lots transfer can significantly impact the client's tax situation — transferring high-cost-basis lots leaves the low-basis lots behind (and vice versa). The advisor should evaluate the tax implications before selecting positions for partial transfer.

**Cost basis transfer requirements:**
Under IRS regulations (IRC Section 6045A), the delivering firm must provide cost basis information for transferred securities to the receiving firm. For covered securities (generally acquired after 2011 for equities, 2012 for mutual funds, 2014 for fixed income), the delivering firm must electronically transfer the cost basis to the receiving firm within 15 days of the transfer settlement. The receiving firm must maintain the original cost basis, acquisition date, and holding period for each lot. For uncovered securities (acquired before the applicable dates), cost basis transfer is optional but recommended. Clients should verify cost basis accuracy after the transfer completes, as discrepancies are common and can result in incorrect tax reporting.

**Partial transfer impact on margin accounts:**
Transferring assets out of a margin account reduces the account's equity and may trigger a margin call at the delivering firm. Before initiating a partial transfer from a margin account, the advisor should: calculate the post-transfer equity and margin requirements, ensure the remaining positions maintain sufficient margin collateral, consider whether to pay down the margin debit before or during the transfer, and communicate with the client about the potential margin call. If the transfer would create a margin deficiency, the delivering firm may reject the transfer or require the client to deposit additional funds.

**In-kind vs liquidate-and-transfer:**
- **In-kind transfer** moves the securities as-is, preserving the cost basis and avoiding a taxable event. This is preferred for long-term holdings with significant unrealized gains.
- **Liquidate-and-transfer** involves selling the positions at the delivering firm and transferring the cash proceeds. This creates a taxable event but may be preferable when: the securities are not available on the receiving firm's platform, the client wants to restructure the portfolio anyway, or the positions are small and not worth the complexity of in-kind transfer.

### Internal Journal Entries
Journal entries move assets between accounts within the same firm. Because the assets do not leave the firm, journal entries do not use ACATS and are processed internally through the firm's account management system. Journals are one of the most common operational transactions at brokerage firms.

**Journal types:**
- **Free journal (non-valued):** Moves securities or cash between accounts without a corresponding payment. Used for gifts, estate distributions, trust funding, and household rebalancing. A free journal of securities between accounts with different registrations (e.g., individual to trust) may have tax implications and should be documented accordingly.
- **Valued journal:** Moves securities between accounts with a corresponding cash payment. Used for internal buy/sell transactions between accounts, typically at market value. Valued journals are less common and require additional documentation to ensure fair pricing.

**Common journal scenarios:**
- **Household rebalancing:** Moving securities between family member accounts to optimize asset allocation across the household. For example, concentrating tax-exempt bonds in a taxable account and growth equities in an IRA. Note: journals between accounts with different beneficial owners (e.g., spouse A to spouse B) may constitute gifts for tax purposes.
- **Trust funding:** Transferring assets from an individual account to a trust account. This is a common event when a client establishes a trust and needs to re-title assets. The journal documents the transfer for trust accounting purposes.
- **Gift transfers:** Journaling securities from a donor's account to a recipient's account. The donor's cost basis carries over to the recipient (carryover basis for gifts), and the annual gift tax exclusion applies. The firm should document the fair market value at the date of the gift for tax reporting.
- **Account consolidation:** Merging multiple accounts belonging to the same client into a single account. The firm journals all positions and cash from the closing accounts to the surviving account.
- **Entity restructuring:** Moving assets when a client changes the account registration (e.g., individual to LLC, general partnership to limited partnership).

**Journal approval workflows:**
Most firms require supervisory approval for journal entries, especially when:
- The journal is between accounts with different registrations or beneficial owners
- The journal amount exceeds a specified threshold
- The journal involves retirement accounts (to ensure compliance with distribution and contribution rules)
- The journal is initiated by someone other than the account holder

The approval workflow typically includes: request initiation by the advisor or operations, documentation of the reason for the journal, supervisory review and approval, execution of the journal, and confirmation sent to both account holders.

**Tax implications of journals between different registrations:**
- Individual to revocable trust (same SSN): generally not a taxable event because the grantor and the trust are the same tax entity
- Individual to irrevocable trust: may be a taxable gift; gift tax return (Form 709) may be required; cost basis carries over for gifts below fair market value
- Individual to spouse (community property state): generally not taxable as a transfer between spouses
- Individual to spouse (separate property state): may be a gift; however, interspousal transfers during marriage are generally tax-free under IRC Section 1041
- Any account to an estate account: only occurs upon death; triggers cost basis step-up (or step-down) to fair market value at date of death
- Retirement account to non-retirement account: this is a distribution, not a journal; it triggers taxable income and potentially early withdrawal penalties

### Retirement Account Rollovers
Retirement account rollovers move funds between qualified retirement plans and IRAs. Rollovers are subject to specific IRS rules that differ based on the type of rollover, the source and destination accounts, and the method of transfer. Errors in rollover processing can result in unintended tax consequences, penalties, and plan disqualification.

**Direct rollover (trustee-to-trustee):**
In a direct rollover, the distributing plan or IRA transfers the funds directly to the receiving IRA or plan. The funds are never in the client's possession. Direct rollovers are the preferred method because: there is no mandatory 20% federal tax withholding (which applies to indirect rollovers from employer plans), there is no 60-day deadline to complete the rollover, and the transaction is reported as a non-taxable rollover on Form 1099-R (distribution code G for direct rollovers to eligible retirement plans, or code H for direct rollovers to Roth IRAs). The receiving firm initiates the direct rollover by submitting a rollover request to the distributing institution, accompanied by the client's signed rollover authorization.

**Indirect rollover (60-day rule):**
In an indirect rollover, the distributing plan or IRA pays the funds to the client, who then has 60 calendar days to deposit the funds into an eligible receiving plan or IRA. If the client fails to complete the rollover within 60 days, the distribution is taxable and may be subject to a 10% early withdrawal penalty if the client is under age 59 1/2. For distributions from employer plans, the plan must withhold 20% for federal taxes — meaning the client receives only 80% of the distribution and must contribute the full amount (including the 20% withheld) to the receiving IRA to avoid tax on the shortfall. The IRS may grant a waiver of the 60-day requirement for hardship, error, or circumstances beyond the client's control (Revenue Procedure 2020-46 provides a self-certification procedure).

**Employer plan to IRA rollovers:**
- **401(k), 403(b), 457(b) to Traditional IRA:** Pre-tax contributions and earnings roll over tax-free. After-tax contributions (non-Roth) can be rolled to a Traditional IRA or separated — the after-tax basis rolls to a Roth IRA and the earnings roll to a Traditional IRA (a split rollover under Notice 2014-54).
- **401(k) Roth to Roth IRA:** Designated Roth contributions and earnings from an employer plan can be directly rolled to a Roth IRA. The 5-year holding period for qualified distributions restarts at the Roth IRA.
- **Required documentation:** Distribution request form from the employer plan, rollover election form, receiving firm's IRA application (if a new IRA is being established), and a letter of acceptance from the receiving custodian.

**IRA-to-IRA rollovers (one-per-year rule):**
The IRS imposes a one-per-year rule on indirect (60-day) IRA-to-IRA rollovers: a taxpayer may make only one indirect rollover from an IRA to another IRA (or the same IRA) in any 12-month period. This rule applies in aggregate across all of the taxpayer's IRAs (Traditional, Roth, SEP, SIMPLE). Violating the one-per-year rule results in the second rollover being treated as a taxable distribution plus a 6% excess contribution penalty if deposited into the receiving IRA. Direct (trustee-to-trustee) transfers are not subject to the one-per-year rule, which is why direct transfers are strongly preferred for IRA-to-IRA movements.

**Roth conversions:**
A Roth conversion moves funds from a Traditional IRA (or employer plan) to a Roth IRA. The converted amount is included in the client's taxable income for the year of conversion (except for amounts attributable to non-deductible contributions, which have already been taxed). There is no income limit for Roth conversions. The converted amount is not subject to the 10% early withdrawal penalty. Roth conversions are reported on Form 1099-R (distribution) and Form 5498 (contribution to the Roth IRA). Conversion strategies include: converting in low-income years to minimize the tax impact, partial conversions spread over multiple years to manage bracket creep, and converting before RMDs begin (age 73) to reduce future RMD obligations.

**Tax reporting:**
- **Form 1099-R:** Issued by the distributing institution for the calendar year of distribution. Reports the gross distribution, taxable amount, federal and state withholding, and distribution code. Key distribution codes: 1 (early distribution), 2 (early distribution — exception applies), 7 (normal distribution), G (direct rollover to qualified plan), H (direct rollover to Roth IRA).
- **Form 5498:** Issued by the receiving institution for the calendar year of the contribution/rollover. Reports rollover contributions, regular contributions, fair market value of the account, and RMD amounts. Form 5498 is due to the IRS by May 31 of the year following the contribution.

### Estate Transfers
Estate transfers move assets from a decedent's account to beneficiaries, estate accounts, or trust accounts established under the decedent's will. Estate transfers are among the most complex operational transactions due to the legal documentation required, tax basis adjustments, and the emotional sensitivity of working with bereaved families.

**Notification of death and account freeze:**
When a firm is notified of an account holder's death, the account is immediately frozen (restricted from trading and withdrawals) pending receipt of required documentation. The firm must: verify the death (typically by requesting an official death certificate), restrict the account to prevent unauthorized activity, notify relevant parties (advisor, operations, compliance), and begin the estate processing workflow. For joint accounts with right of survivorship (JTWROS), the surviving owner may continue to access the account after providing a death certificate — the decedent's name is removed from the registration. For all other account types, the account remains frozen until proper legal documentation is received.

**Required documentation:**
- **Death certificate:** Certified copy (not a photocopy) of the official death certificate. Most firms require at least one original certified copy.
- **Letters testamentary (testate estates):** Court-issued document appointing the executor named in the will. Grants the executor authority to act on behalf of the estate. Must be current — most firms require letters issued within the past 60 days (some accept up to 12 months).
- **Letters of administration (intestate estates):** Court-issued document appointing an administrator when the decedent died without a will. Grants similar authority to the administrator.
- **Beneficiary claim form:** The firm's internal form that the beneficiary or estate representative completes to claim the assets. Specifies the receiving account, distribution instructions, and tax withholding elections.
- **Small estate affidavit:** For estates below a state-specific threshold (varies by state, typically $50,000 to $150,000), a small estate affidavit may substitute for letters testamentary/administration, avoiding the need for full probate.
- **Trust documentation (if applicable):** If assets are to be distributed to a trust created under the will (testamentary trust), the trust instrument and trustee identification are required.
- **Tax waivers (certain states):** Some states require a state tax waiver or release before estate assets can be distributed. The firm must verify whether the decedent's state of residence or the state of the firm's jurisdiction requires this.

**Cost basis step-up processing:**
Upon death, the cost basis of the decedent's assets is generally stepped up (or stepped down) to the fair market value as of the date of death (IRC Section 1014). The alternate valuation date (6 months after death) may be elected by the estate executor on the federal estate tax return (Form 706), but only if it reduces the gross estate value. The firm must: determine the fair market value of each position as of the date of death, update the cost basis records to reflect the stepped-up basis, and transfer the stepped-up basis to the receiving account (beneficiary, estate, or trust). For community property states, the surviving spouse's half of community property also receives a step-up in basis (full step-up for both halves), which is a significant tax benefit.

**Inherited IRA setup:**
When the decedent held an IRA, the beneficiary designation on file determines the distribution of the IRA assets — the will does not override the IRA beneficiary designation. Processing depends on the beneficiary type:
- **Spouse beneficiary:** May roll the inherited IRA into their own IRA (treating it as their own), transfer to an inherited IRA in their name, or take a lump-sum distribution. Rolling to their own IRA allows continued tax-deferred growth and delays RMDs until the spouse's own required beginning date.
- **Non-spouse individual beneficiary (SECURE Act):** Under the SECURE Act of 2019, most non-spouse beneficiaries must distribute the entire IRA within 10 years of the account owner's death (the 10-year rule). Exceptions (eligible designated beneficiaries): minor children of the account owner (until age of majority), disabled individuals, chronically ill individuals, and individuals not more than 10 years younger than the decedent. The inherited IRA must be titled in the decedent's name for the benefit of the beneficiary (e.g., "John Smith, Deceased, FBO Jane Smith, Beneficiary").
- **Entity or estate beneficiary:** Subject to the 5-year rule (all assets must be distributed within 5 years of death) if the account owner died before the required beginning date, or the remaining life expectancy method if death occurred on or after the required beginning date.

**Multi-beneficiary allocation:**
When an IRA or investment account names multiple beneficiaries, the firm must allocate assets proportionally based on the beneficiary designation percentages. Each beneficiary receives their share in a separately established account. For inherited IRAs, establishing separate inherited IRA accounts for each beneficiary by December 31 of the year following the year of death allows each beneficiary to use their own life expectancy for RMD calculations (if applicable). Failure to separate the accounts by this deadline requires all beneficiaries to use the oldest beneficiary's life expectancy.

**Estate distribution scheduling:**
The executor or administrator determines when and how to distribute estate assets. The firm processes distributions based on the executor's instructions, which may include: in-kind distribution of securities to beneficiaries (preserving the stepped-up basis), liquidation and cash distribution, partial distributions over time (common when estate settlement takes months or years), and specific bequests of particular securities to named beneficiaries. Each distribution must be documented and reconciled against the total estate.

### Transfer Tracking and Reconciliation
Transfer tracking is critical for operational efficiency and client satisfaction. Transfers involve multiple systems, firms, and settlement cycles, creating opportunities for errors, delays, and miscommunication.

**Transfer status monitoring:**
Firms should maintain a centralized transfer tracking system that captures: transfer request date, transfer type (ACAT, non-ACAT, journal, rollover), current status (submitted, validated, in progress, completed, rejected), expected completion date, actual completion date, and any exceptions or holds. ACATS provides real-time status updates through NSCC, which the firm's back office system should capture and display. Operations teams should review outstanding transfers daily and escalate transfers that exceed expected timelines.

**Common ACAT rejection codes and remediation:**
- **Code 01 — Account number not on file:** The account number provided does not match the delivering firm's records. Remediation: verify the account number with the client and resubmit.
- **Code 02 — SSN/TIN mismatch:** The SSN or TIN on the transfer request does not match the delivering firm's records. Remediation: confirm the correct SSN/TIN with the client; may require the client to update records at the delivering firm before resubmission.
- **Code 03 — Account title mismatch:** The account registration on the transfer request does not match the delivering firm's records (e.g., "John A. Smith" vs "John Smith"). Remediation: match the exact registration at the delivering firm or have the client update their registration.
- **Code 04 — Invalid transfer type for this account:** The transfer type requested (full or partial) is not valid for the account. Remediation: verify the account type and correct the transfer request.
- **Code 05 — Duplicate request:** A transfer request for this account is already in progress. Remediation: check for an existing pending transfer and cancel the duplicate.
- **Code 07 — Account in transfer:** The account is already in the process of being transferred. Remediation: wait for the existing transfer to complete before initiating a new request.
- **Code 08 — Account restricted:** The account has a legal restriction (lien, court order, margin liquidation) preventing transfer. Remediation: work with the client and delivering firm to resolve the restriction.

**Escalation procedures:**
When a transfer is delayed beyond expected timelines or encounters repeated rejections, escalation steps include: contacting the delivering firm's transfer department directly, filing a FINRA complaint if the delivering firm is unreasonably delaying (FINRA Rule 11870 prohibits unreasonable delays), involving the client in communicating with the delivering firm, and escalating within the receiving firm's operations management chain. FINRA requires delivering firms to complete validated transfers within 3 business days, and patterns of delay may result in regulatory action.

**Client communication during transfers:**
Proactive client communication reduces anxiety and support inquiries during the transfer process. Best practices include: setting expectations at transfer initiation (explain the timeline, potential for delays, and what to expect), providing status updates at key milestones (validation, asset movement, completion), promptly notifying the client of any rejections or issues requiring their action, confirming completion and providing a summary of transferred assets, and following up after completion to address any discrepancies (missing positions, incorrect cost basis).

**Asset reconciliation post-transfer:**
After a transfer completes, the receiving firm must reconcile the received assets against the expected transfer. Reconciliation checks include: verifying that all expected positions were received in the correct quantities, confirming cash balances match expectations, verifying cost basis information was received and is accurate, checking for positions that may have settled at the delivering firm after the transfer date (late-settling trades), and identifying any corporate action adjustments that occurred during the transfer period (stock splits, dividends, mergers).

**Clean-up processing:**
Post-transfer clean-up addresses residual items that were not part of the primary transfer:
- **Residual credits:** Small cash amounts (typically under $100) sent by the delivering firm after the primary transfer — often from final dividend payments, interest accruals, or fractional share liquidation proceeds. The receiving firm must post these credits to the client's account and notify the client.
- **Fractional shares:** ACATS cannot transfer fractional shares. The delivering firm liquidates fractional shares and sends the cash proceeds as a residual credit. The client should be informed that fractional shares will be liquidated.
- **Accrued income:** Interest or dividends that accrued before the transfer but are paid after the transfer date. The delivering firm is responsible for forwarding these to the receiving firm or directly to the client.
- **Pending transactions:** Trades that were executed before the transfer but settle after the transfer date must be accounted for at the appropriate firm based on trade date vs settlement date conventions.

### Regulatory Requirements
Account transfers are governed by specific FINRA rules, ACATS operating procedures, and IRS regulations for retirement accounts.

**FINRA Rule 11870 — Customer Account Transfer Contracts:**
Rule 11870 establishes the requirements for customer account transfers between FINRA member firms. Key provisions: the receiving firm must submit the transfer request within one business day of receiving the customer's signed TIF; the delivering firm must validate or take exception to the transfer within 3 business days; validated transfers must be completed within 3 business days after validation (6 business days total); the delivering firm must promptly resolve any exceptions and may not unreasonably delay or refuse a valid transfer; and residual credit balances must be forwarded to the receiving firm within 5 business days of the delivering firm's next credit cycle.

**ACATS operating rules:**
ACATS operates under the NSCC Rules and Procedures, which supplement FINRA Rule 11870. ACATS rules define: the electronic format for transfer requests and responses, valid rejection codes and their appropriate use, settlement procedures for transferred assets, timeframes for each stage of the transfer process, and reporting requirements for transfer activity.

**Delivering firm obligations:**
The delivering firm has a regulatory obligation not to impede valid transfer requests. Prohibited practices include: rejecting transfers for pretextual reasons, delaying validation to retain assets, imposing unreasonable transfer fees designed to discourage transfers, and failing to process residual items promptly. FINRA examinations specifically review delivering firm transfer practices, and patterns of delay or obstruction can result in enforcement actions and fines.

**Cost basis reporting requirements:**
Under IRC Section 6045A and associated Treasury Regulations, the delivering firm must transfer cost basis information for covered securities to the receiving firm. The transfer must be electronic (using the CBRS — Cost Basis Reporting System) and must occur within 15 days of the transfer settlement date. The receiving firm must maintain the transferred basis and use it for subsequent tax reporting on Form 1099-B. Failure to transfer cost basis accurately can result in incorrect tax reporting, IRS penalties, and customer complaints.

**ERISA considerations for retirement transfers:**
Transfers involving ERISA-governed retirement plans (401(k), 403(b), pension plans) require compliance with ERISA's fiduciary rules. The plan fiduciary must approve rollover distributions, confirm the receiving institution is an eligible retirement plan, and ensure the participant receives required disclosures (including a Special Tax Notice under IRC Section 402(f)). Plan-to-IRA rollovers must be processed as either direct rollovers or eligible rollover distributions with mandatory 20% withholding.

**Asset validation and due diligence:**
Both the receiving and delivering firms must validate the assets being transferred. The receiving firm must confirm it can hold and service each asset type (some firms restrict certain alternative investments, foreign securities, or thinly traded positions). The delivering firm must verify that the positions are free of liens, pledges, or legal holds before releasing them. For margin accounts, the delivering firm must confirm the transfer will not create an unsecured debit balance. Both firms must maintain an audit trail of the transfer validation process for regulatory examination purposes.

## Worked Examples

### Example 1: Managing a full ACAT transfer for a high-net-worth household moving from a competitor
**Scenario:** A high-net-worth household with $8M across five accounts is moving from a competitor firm to your firm. The accounts are: (1) a joint taxable account with $3M in individual equities and ETFs, (2) the husband's Traditional IRA with $1.5M in mutual funds and bonds, (3) the wife's Roth IRA with $800K in equities and ETFs, (4) a revocable family trust with $2.2M in a diversified portfolio including equities, fixed income, and a limited partnership interest valued at $200K, and (5) a custodial UTMA account for their minor child with $500K in mutual funds. The advisor wants to complete the transfer as efficiently as possible and invest the assets into the firm's model portfolios.

**Design Considerations:**
- Five separate ACAT transfers must be initiated — each account is a distinct ACATS transfer request
- The limited partnership in the trust account is likely ACAT-ineligible and will require separate handling
- The mutual funds in the IRA and UTMA accounts must be verified for availability on the receiving firm's platform — proprietary funds of the competitor may not be transferable in-kind
- The joint taxable account and trust account may have significant unrealized gains, making in-kind transfer critical to avoid unnecessary taxable events
- Cost basis must transfer accurately for all taxable accounts (joint, trust, UTMA); retirement accounts (IRA, Roth IRA) do not have cost basis reporting requirements during the transfer but should be tracked internally
- The UTMA account requires that the custodian (parent) authorize the transfer

**Analysis:** Begin by opening all five accounts at the receiving firm with proper registrations matching the delivering firm exactly (account title mismatches are the most common cause of ACAT rejections). Obtain signed TIFs for all five accounts. For the trust account, ensure the trust certification and EIN documentation are on file. For the UTMA, verify the custodian designation matches.

Submit all five ACAT requests simultaneously. For the trust account, submit a partial ACAT excluding the limited partnership position. Contact the limited partnership's general partner to initiate a separate assignment/transfer process for the LP interest — this will require: a transfer of ownership form from the GP, the receiving firm's confirmation that it can hold the LP interest on its books, and potentially a 30-60 day processing period for GP approval.

For the mutual funds, pre-verify each fund's availability on the receiving firm's platform. If any funds are proprietary to the delivering firm, discuss with the client: (a) liquidate at the delivering firm before the ACAT (taxable event in the IRA/UTMA is not a concern since these are tax-advantaged accounts, but taxable for the joint/trust accounts), or (b) transfer via ACAT and the positions will arrive as "ineligible" and need to be liquidated at the receiving firm, or (c) leave the proprietary fund positions behind and transfer only eligible assets.

Monitor all five transfers daily through ACATS status updates. The expected timeline is: validation within 3 business days, asset delivery within 6 business days total. After the primary transfer settles, reconcile all positions against the delivering firm's final statement. Verify cost basis information was received for the joint, trust, and UTMA accounts. Process any residual credits (fractional shares, pending dividends) as they arrive over the following 2-4 weeks.

Once all assets are received and reconciled, assign each account to the appropriate model portfolio. For the joint and trust accounts with existing equity positions, the advisor should evaluate which positions to retain (to avoid realizing gains) and which to sell for model alignment, factoring in tax-loss harvesting opportunities. Provide the client with a transfer completion summary showing all positions received, cost basis, and any residual items pending.

### Example 2: Processing retirement account rollovers from a 401(k) to an IRA with Roth conversion
**Scenario:** A 55-year-old client has recently left her employer and has a 401(k) with $750K, consisting of $600K in pre-tax contributions and earnings and $150K in after-tax (non-Roth) contributions and earnings. The client wants to roll the funds into an IRA at your firm and convert a portion to a Roth IRA. The client's current-year taxable income is $180K (married filing jointly), placing her in the 24% federal bracket. The client wants to manage the tax impact of the Roth conversion.

**Design Considerations:**
- The 401(k) contains both pre-tax and after-tax funds, which enables a split rollover under IRS Notice 2014-54
- Under Notice 2014-54, the client can direct the pre-tax portion ($600K) to a Traditional IRA and the after-tax contributions (basis) to a Roth IRA, with the earnings on after-tax contributions going to the Traditional IRA
- The after-tax contribution basis of $150K includes both the original contributions and earnings on those contributions — the plan administrator must provide a breakdown. Assume $120K is after-tax basis and $30K is earnings on those contributions
- The $120K after-tax basis can be converted to a Roth IRA with zero tax because it has already been taxed. The $30K in earnings would be taxable if converted to Roth
- A direct rollover avoids the 20% mandatory withholding that applies to indirect rollovers from employer plans
- The client may want to convert additional pre-tax funds to Roth, but must weigh the tax cost

**Analysis:** Step 1: Open a Traditional IRA and a Roth IRA at the receiving firm. Step 2: Request a split direct rollover from the 401(k) plan administrator. The rollover instruction directs: pre-tax contributions and all earnings ($600K pre-tax + $30K earnings on after-tax = $630K) to the Traditional IRA, and after-tax contribution basis ($120K) to the Roth IRA. Under Notice 2014-54, this allocation is permitted because the after-tax basis is directed to the Roth IRA and the pre-tax/earnings portion is directed to the Traditional IRA.

Tax impact of the split rollover: the $120K direct rollover to the Roth IRA from after-tax contributions has zero tax because the basis has already been taxed. The $630K direct rollover to the Traditional IRA is not currently taxable.

Step 3: Evaluate additional Roth conversion. The client is in the 24% bracket at $180K income. The top of the 24% bracket for married filing jointly is approximately $383K. The client has approximately $203K of room in the 24% bracket ($383K minus $180K). Converting $203K from the Traditional IRA to the Roth IRA would keep the client in the 24% bracket and cost approximately $48,720 in federal tax ($203K multiplied by 24%). Alternatively, the client could convert less to stay well within the bracket or spread conversions over multiple years.

Step 4: Process the Roth conversion. After the direct rollover to the Traditional IRA settles (allow 1-2 weeks for the 401(k) distribution and IRA deposit), initiate a Roth conversion for the agreed-upon amount. The conversion is processed as a distribution from the Traditional IRA and a contribution to the Roth IRA. The firm issues a 1099-R for the conversion in the year it occurs.

Step 5: Tax reporting. The 401(k) plan administrator issues Form 1099-R for the direct rollover distribution (code G). The receiving firm issues Form 5498 for the rollover contribution to the Traditional IRA and the Roth IRA. If a subsequent Roth conversion is done, the receiving firm issues an additional 1099-R for the conversion distribution and an additional 5498 for the Roth conversion contribution.

Step 6: Document the multi-year Roth conversion strategy. If the client plans to convert additional amounts in future years, document the plan: target conversion amount per year, bracket analysis, and the expected timeline to convert the desired total. This becomes part of the client's financial plan and should be reviewed annually as income and tax brackets change.

### Example 3: Handling estate account transfers to multiple beneficiaries with different account types
**Scenario:** A client passed away holding three accounts at your firm: (1) an individual taxable account with $2M in equities and bonds, (2) a Traditional IRA with $500K, and (3) a joint taxable account (JTWROS) with his spouse holding $1M in diversified funds. The will names the spouse as the sole beneficiary of the estate (for the individual taxable account). The IRA beneficiary designation names the spouse (60%) and the two adult children (20% each). The date of death is January 15, and the firm was notified on January 22.

**Design Considerations:**
- The joint JTWROS account passes automatically to the surviving spouse by operation of law — this is not a probate asset and does not go through the estate
- The individual taxable account is a probate asset that passes under the will to the spouse through the estate
- The IRA passes by beneficiary designation, not by will — the 60/20/20 split controls
- All assets in the individual taxable and joint accounts receive a cost basis step-up to fair market value as of the date of death (January 15)
- In a community property state, the spouse's half of the joint account also receives a step-up; in a common law state, only the decedent's half steps up, but for JTWROS the entire account passes to the surviving spouse regardless
- The spouse can roll the 60% IRA share into her own IRA; the adult children must take their shares as inherited IRAs subject to the SECURE Act 10-year rule
- The inherited IRAs must be established as separate accounts by December 31 of the year following the year of death to allow each beneficiary to use their own distribution timeline

**Analysis:**

**Joint account (JTWROS) — immediate processing:** Upon receipt of the certified death certificate, remove the decedent's name from the joint account registration. The account becomes solely the surviving spouse's individual account. No letters testamentary are needed — a death certificate is sufficient. Process the cost basis step-up for the decedent's portion of the holdings (or the full step-up if the couple was in a community property state). This can typically be completed within 1-2 weeks of receiving the death certificate.

**Individual taxable account — estate processing:** Freeze the account upon notification of death. Request the following documentation: certified death certificate, letters testamentary (the spouse must be appointed as executor by the probate court), estate EIN (obtained by the executor from the IRS via Form SS-4), and the firm's beneficiary claim form. Once letters testamentary are received, re-title the account as an estate account ("Estate of [Decedent Name], [Spouse Name], Executor"). Process the cost basis step-up to the January 15 date-of-death values for all positions. The executor may then either: (a) distribute the assets in-kind to the spouse's individual account (preserving the stepped-up basis), (b) liquidate the positions and distribute cash, or (c) maintain the estate account during the probate process and distribute upon estate settlement. Given that the spouse is the sole beneficiary, in-kind distribution to the spouse's account is typically the most tax-efficient approach, preserving the stepped-up basis.

**Traditional IRA — beneficiary distribution:** The IRA beneficiary designation controls. Three separate inherited IRA accounts must be established:

1. **Spouse's inherited IRA (60% = $300K):** The spouse has three options: (a) roll the $300K into her own existing Traditional IRA — this is the most common choice as it allows continued tax-deferred growth, new beneficiary designations, and delays RMDs until the spouse's own required beginning date; (b) transfer to an inherited IRA in the spouse's name — this preserves the ability to take distributions without early withdrawal penalty regardless of age, which is beneficial if the spouse is under 59 1/2 and needs access to funds; or (c) take a lump-sum distribution (fully taxable and rarely advisable). For a spouse who does not need immediate access and is over 59 1/2, spousal rollover is typically preferred.

2. **Child 1 inherited IRA (20% = $100K):** Establish an inherited IRA titled "Decedent Name, Deceased, FBO Child 1 Name, Beneficiary." Under the SECURE Act, Child 1 must distribute the entire inherited IRA by December 31 of the 10th year following the year of death (by December 31 of Year 11 counting from the year after death). There are no annual RMDs required during the 10-year period (assuming the decedent died before the required beginning date); however, the entire balance must be distributed by the end of the 10th year. If the decedent had already reached the required beginning date, annual RMDs are required during the 10-year period based on the beneficiary's life expectancy.

3. **Child 2 inherited IRA (20% = $100K):** Same structure and rules as Child 1.

**Timeline and coordination:** Establish the three inherited IRA accounts as quickly as documentation allows, and no later than December 31 of the year following the year of death to preserve separate account treatment. Process the IRA distributions per the beneficiary designation percentages. Provide each beneficiary with documentation of their inherited IRA, the distribution rules that apply, and the deadline for full distribution. Coordinate with the estate attorney on the probate timeline for the individual taxable account.

**Cost basis documentation:** Prepare a date-of-death valuation report for all three accounts showing: each position, the number of shares or par value, the closing price on January 15 (or the average of the high and low for that date), and the total stepped-up basis. This report becomes part of the estate records and is provided to the executor, the tax preparer, and each beneficiary for their records. The stepped-up basis applies to the individual taxable account and the joint account but does not apply to the IRA (IRA distributions are taxed as ordinary income regardless of basis step-up).

## Common Pitfalls
- Submitting ACAT transfer requests with account title mismatches — even minor discrepancies (middle initial, suffix, trust name variation) cause rejections that delay the transfer by days
- Failing to identify ACAT-ineligible assets before initiating a full ACAT, leading to unexpected residual positions at the delivering firm and confused clients
- Not verifying mutual fund availability on the receiving firm's platform before transfer — proprietary funds of the delivering firm cannot be held in-kind and must be liquidated
- Processing an indirect rollover when a direct rollover was intended, triggering mandatory 20% withholding and creating a 60-day compliance deadline
- Violating the one-per-year IRA-to-IRA indirect rollover rule by processing a second indirect rollover within 12 months — this creates a taxable distribution and excess contribution penalty
- Failing to separate inherited IRA accounts for multiple beneficiaries by the December 31 deadline of the year following the year of death, forcing all beneficiaries to use the oldest beneficiary's life expectancy
- Initiating a partial transfer from a margin account without calculating the post-transfer margin impact, resulting in a margin call at the delivering firm
- Not following up on residual credits from the delivering firm — small amounts of dividends, fractional share proceeds, and interest can remain undelivered for months if not tracked
- Accepting a death certificate photocopy rather than a certified copy, causing processing delays when the operations team rejects the documentation
- Confusing a Roth conversion (taxable event) with a Roth contribution (subject to income and contribution limits) — these are different transactions with different rules and reporting
- Failing to transfer cost basis for covered securities within the required 15-day window, resulting in regulatory issues and incorrect tax reporting at the receiving firm
- Processing estate distributions without proper letters testamentary or letters of administration, exposing the firm to liability if the distributions are later challenged

## Cross-References
- **account-opening-workflow** (Layer 12, client-operations): New accounts must be established at the receiving firm before transfers can be initiated; transfer processing depends on proper account setup and registration matching
- **account-maintenance** (Layer 12, client-operations): Account re-registration (name changes, trust re-titling) and beneficiary updates are often prerequisites for successful transfers; maintenance workflows handle post-transfer clean-up tasks
- **settlement-clearing** (Layer 12, client-operations): ACAT transfers settle through NSCC/DTCC infrastructure; understanding settlement cycles and DTC delivery mechanisms is essential for transfer processing and reconciliation
- **tax-efficiency** (Layer 6, portfolio-construction): Transfer decisions (in-kind vs liquidate, tax lot selection, Roth conversion timing) have significant tax implications; the tax-efficiency skill informs optimal transfer strategies for taxable accounts
- **books-and-records** (Layer 9, compliance): Transfer documentation (TIFs, rollover forms, death certificates, letters testamentary) must be retained per SEC and FINRA recordkeeping rules; transfer records are commonly requested during regulatory examinations
- **client-onboarding** (Layer 10, advisory-practice): Transfers are a primary funding mechanism during client onboarding; the onboarding workflow initiates and tracks ACAT transfers as part of the new client setup process
- **corporate-actions** (Layer 12, client-operations): Pending corporate actions (dividends, mergers, splits) during the transfer period require coordination between delivering and receiving firms to ensure proper processing and allocation
- **reconciliation** (Layer 12, client-operations): Post-transfer asset reconciliation verifies that all positions, cash balances, and cost basis were transferred accurately; reconciliation processes detect and resolve transfer discrepancies
