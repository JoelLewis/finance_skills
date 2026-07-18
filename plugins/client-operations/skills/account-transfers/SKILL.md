---
name: account-transfers
description: "Process and manage account transfers between and within financial institutions. Use when handling full or partial ACAT transfers between broker-dealers, troubleshooting ACAT rejection codes or FINRA Rule 11870 timelines, setting up non-ACAT transfers (Fund/SERV, DTC free delivery, physical certificates), processing internal journal entries, handling retirement rollovers or Roth conversions with proper tax reporting, transferring cost basis under IRC Section 6045A, moving decedent assets to beneficiaries with date-of-death step-up, or reconciling residual credits and fractional shares after transfer completion."
---

# Account Transfers

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
A Roth conversion moves funds from a Traditional IRA (or employer plan) to a Roth IRA. The converted amount is included in the client's taxable income for the year of conversion (except for amounts attributable to non-deductible contributions, which have already been taxed). There is no income limit for Roth conversions. The converted amount is not subject to the 10% early withdrawal penalty. Roth conversions are reported on Form 1099-R (distribution) and Form 5498 (contribution to the Roth IRA). Conversion strategies include: converting in low-income years to minimize the tax impact, partial conversions spread over multiple years to manage bracket creep, and converting before RMDs begin — age 73 (SECURE 2.0; rises to 75 in 2033) — to reduce future RMD obligations.

**Tax reporting:**
- **Form 1099-R:** Issued by the distributing institution for the calendar year of distribution. Reports the gross distribution, taxable amount, federal and state withholding, and distribution code. Key distribution codes: 1 (early distribution), 2 (early distribution — exception applies), 7 (normal distribution), G (direct rollover to qualified plan), H (direct rollover to Roth IRA).
- **Form 5498:** Issued by the receiving institution for the calendar year of the contribution/rollover. Reports rollover contributions, regular contributions, fair market value of the account, and RMD amounts. Form 5498 is due to the IRS by May 31 of the year following the contribution.

### Estate Transfers
Estate transfers move assets from a decedent's account to beneficiaries, estate accounts, or trust accounts established under the decedent's will. Estate transfers are among the most complex operational transactions due to the legal documentation required, tax basis adjustments, and the emotional sensitivity of working with bereaved families.

**Death notification, account freeze, and estate documentation:**
The death notification workflow — immediate account restriction, death certificate verification, letters testamentary or administration, small estate affidavits, and JTWROS survivor handling — is covered in account-maintenance. This skill picks up once documentation is in hand and assets must move: basis step-up, inherited IRA establishment, and beneficiary distributions.

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

Three worked examples — a five-account household ACAT migration (LP interests, proprietary funds, UTMA authorization), a 401(k)-to-IRA split rollover with Roth conversion bracket analysis (Notice 2014-54), and a multi-beneficiary estate transfer (JTWROS, probate, inherited IRAs under the SECURE Act) — are in [references/examples.md](references/examples.md); load it when working through a concrete transfer, rollover, or estate distribution.

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
- **account-opening-workflow** (client-operations plugin): New accounts must be established at the receiving firm before transfers can be initiated; transfer processing depends on proper account setup and registration matching
- **account-maintenance** (client-operations plugin): Account re-registration (name changes, trust re-titling) and beneficiary updates are often prerequisites for successful transfers; maintenance workflows handle post-transfer clean-up tasks
- **settlement-clearing** (trading-operations plugin): ACAT transfers settle through NSCC/DTCC infrastructure; understanding settlement cycles and DTC delivery mechanisms is essential for transfer processing and reconciliation
- **tax-efficiency** (wealth-management plugin): Transfer decisions (in-kind vs liquidate, tax lot selection, Roth conversion timing) have significant tax implications; the tax-efficiency skill informs optimal transfer strategies for taxable accounts
- **books-and-records** (compliance plugin): Transfer documentation (TIFs, rollover forms, death certificates, letters testamentary) must be retained per SEC and FINRA recordkeeping rules; transfer records are commonly requested during regulatory examinations
- **client-onboarding** (advisory-practice plugin): Transfers are a primary funding mechanism during client onboarding; the onboarding workflow initiates and tracks ACAT transfers as part of the new client setup process
- **corporate-actions** (client-operations plugin): Pending corporate actions (dividends, mergers, splits) during the transfer period require coordination between delivering and receiving firms to ensure proper processing and allocation
- **reconciliation** (client-operations plugin): Post-transfer asset reconciliation verifies that all positions, cash balances, and cost basis were transferred accurately; reconciliation processes detect and resolve transfer discrepancies
