---
name: exchange-connectivity
description: "Guide the design and management of trading venue connectivity and market data infrastructure. Owns the FIX session layer (logon, heartbeats, sequence number gaps, resend and gap recovery, disconnects). Use when building or troubleshooting FIX sessions for order routing or drop copy, integrating exchange protocols like OUCH, ITCH, PITCH, or Pillar, designing market data feed architecture (consolidated SIP vs direct feeds), handling trading halts or circuit breakers or LULD bands, planning co-location or failover and disaster recovery for exchange connectivity, implementing Rule 15c3-5 market access controls, or mapping symbology across venues and data sources. For order state machines and execution-report handling see order-lifecycle."
---

# Exchange Connectivity

## Core Concepts

### Venue Connectivity Architecture
Trading venues expose electronic interfaces through which broker-dealers, market makers, and institutional participants submit orders and receive execution reports. The connectivity architecture between a firm and its execution venues is a foundational component of trading infrastructure.

**Direct Market Access (DMA):** DMA allows a firm to send orders directly to an exchange's matching engine without intermediation by another broker's order management system. The firm maintains its own FIX session (or proprietary protocol connection) with the exchange and is responsible for pre-trade risk controls. DMA is used by broker-dealers with exchange memberships and by proprietary trading firms.

**Sponsored Access:** In a sponsored access arrangement, a non-member firm routes orders to an exchange through a sponsoring broker-dealer's market participant identifier (MPID). The sponsoring broker is responsible for pre-trade risk controls under SEC Rule 15c3-5 (the Market Access Rule). Sponsored access may be "filtered" (orders pass through the sponsor's risk checks before reaching the exchange) or "unfiltered" (orders bypass the sponsor's systems and go directly to the exchange, with the sponsor relying on exchange-level risk controls). The SEC effectively prohibited unfiltered sponsored access through Rule 15c3-5, which requires the broker-dealer providing market access to implement risk management controls and supervisory procedures that are reasonably designed to prevent the entry of erroneous orders.

**FIX Protocol Connectivity:** The Financial Information eXchange (FIX) protocol is the dominant standard for order routing and execution reporting in equities, options, fixed income, and foreign exchange markets. FIX is a tag-value message format (e.g., Tag 35=D for a New Order Single, Tag 35=8 for an Execution Report). Most U.S. equity exchanges accept FIX for order entry, and FIX is the standard interface for broker-to-broker and broker-to-buy-side connectivity. FIX versions in common use include FIX 4.2 (widely supported, still in use at many venues), FIX 4.4 (added support for multi-leg instruments, allocation instructions), and FIX 5.0/FIXT 1.1 (separated transport and application layers).

**Proprietary Exchange Protocols:** Several exchanges offer proprietary binary protocols that provide lower latency than FIX due to more compact message encoding and reduced parsing overhead:
- **OUCH** — Nasdaq's order entry protocol. Binary format, supports order submission, cancellation, and replacement. Commonly used by high-frequency and low-latency participants on Nasdaq and its affiliated venues.
- **ITCH** — Nasdaq's market data dissemination protocol. Provides a full order-by-order (Level 3) view of the Nasdaq order book, including every order add, modify, cancel, and execute event. ITCH is the basis for Nasdaq's TotalView data product.
- **PITCH** — Cboe's market data protocol for the BZX, BYX, EDGX, and EDGA exchanges. Like ITCH, PITCH provides order-by-order depth-of-book data.
- **Pillar** — NYSE's integrated trading technology platform, supporting both order entry and market data across NYSE, NYSE Arca, NYSE American, and NYSE National. Pillar uses binary protocols for gateway connectivity.
- **BOE (Binary Order Entry)** — Cboe's proprietary order entry protocol, offering lower-latency order submission than FIX on Cboe equity exchanges.

**Co-location and Proximity Hosting:** Exchanges offer co-location services that allow firms to place their trading servers in the same data center as the exchange's matching engine. Co-location minimizes network latency (measured in microseconds) by reducing the physical distance between the firm's server and the exchange. Proximity hosting refers to placing servers in a data center near (but not inside) the exchange's facility, offering somewhat higher latency than co-location but often at lower cost. Major U.S. exchange data centers include the NYSE data center in Mahwah, New Jersey and the Nasdaq data center in Carteret, New Jersey.

**Connectivity Providers and Extranets:** Financial extranets are private networks that connect market participants to multiple exchanges and trading venues through a single physical connection. Major extranets include:
- **TNS (Transaction Network Services)** — Provides managed connectivity to global exchanges and trading venues.
- **IPC (now part of Atos)** — Operates the Connexus Cloud financial extranet connecting trading firms to exchanges, market data providers, and service bureaus.
- **BSO (Boldon Smart Operations)** — Offers low-latency network infrastructure for financial markets.
- **Options Technology** — Provides connectivity and managed infrastructure for trading firms.
Extranets reduce the operational burden of maintaining individual point-to-point connections to each venue but introduce a shared network dependency.

**Redundancy and Failover:** Production exchange connectivity must include redundant paths. Standard practice includes: primary and backup FIX sessions to each venue (typically on separate physical network paths), primary and secondary network connections through different extranets or carriers, cross-connect redundancy within co-location facilities, and geographic redundancy where the firm maintains a disaster recovery site capable of resuming trading.

### FIX Session Management
The FIX protocol defines a session layer that handles connection establishment, message sequencing, heartbeating, and recovery. Correct session management is essential for reliable order flow.

**Session-Level Messages:**
- **Logon (MsgType=A):** Initiates a FIX session. Contains the SenderCompID, TargetCompID, and agreed heartbeat interval. The exchange or counterparty responds with its own Logon message to confirm the session. Some venues require encryption or authentication tokens in the Logon message.
- **Logout (MsgType=5):** Gracefully terminates a FIX session. Either side may initiate. A well-behaved implementation sends Logout and waits for the counterparty's Logout response before closing the TCP connection.
- **Heartbeat (MsgType=0):** Sent at the agreed interval (typically 30 seconds) when no other messages are being exchanged. Confirms the session is alive. If no Heartbeat is received within the expected interval (plus a tolerance), the counterparty should send a TestRequest.
- **TestRequest (MsgType=1):** Sent when a Heartbeat is overdue. The receiving side must respond with a Heartbeat containing the TestReqID from the TestRequest. Failure to respond indicates a broken connection.
- **ResendRequest (MsgType=2):** Requests retransmission of messages within a sequence number range. Used when a sequence number gap is detected — for example, the receiving side expects sequence number 100 but receives 105, indicating messages 100-104 were missed.
- **SequenceReset (MsgType=4):** Used in two modes. Gap-fill mode (GapFillFlag=Y) advances the expected sequence number past administrative messages that do not need to be retransmitted. Reset mode (GapFillFlag=N) forces the sequence number to a new value, typically used only during session initialization or error recovery. Reset mode is dangerous because it can cause message loss if used improperly.
- **Reject (MsgType=3):** Sent when a message fails session-level validation (malformed tags, invalid data type, required field missing). A Reject does not indicate a business-level rejection — it means the message could not be parsed.

**Session Configuration:**
- **SenderCompID / TargetCompID:** Unique identifiers for each side of the FIX session. Assigned by the exchange or agreed between counterparties. A firm typically has a distinct SenderCompID for each FIX session it maintains.
- **Heartbeat interval:** Agreed during Logon. Common values are 30 seconds for order sessions and 10-30 seconds for market data sessions.
- **ResetOnLogon:** Some implementations reset sequence numbers to 1 on each Logon. Others persist sequence numbers across sessions and rely on ResendRequest/SequenceReset for gap recovery. Exchange-specific documentation governs which approach is required.
- **Message encoding:** Standard FIX uses ASCII tag=value pairs separated by SOH (0x01) delimiters. Some venues support FAST (FIX Adapted for Streaming) encoding for market data, which uses binary compression to reduce bandwidth.

**Sequence Number Management:** Each side of a FIX session maintains two sequence number counters: the outgoing sequence number (incremented with each message sent) and the expected incoming sequence number (incremented with each message received). If the incoming message's sequence number exceeds the expected value, a gap has been detected and a ResendRequest must be issued. If the incoming sequence number is below the expected value (and the message is not flagged as PossDup), the session is in an unrecoverable state and should be disconnected. Sequence numbers are typically persisted to disk so that sessions can recover after restarts without resetting.

**Gap Detection and Recovery:** When a sequence gap is detected, the receiver sends a ResendRequest specifying the range of missing sequence numbers (BeginSeqNo to EndSeqNo, where EndSeqNo=0 means "infinity" or "to the latest"). The sender retransmits the missing messages with PossDupFlag=Y, indicating they are possible duplicates. The receiver must handle PossDup messages idempotently — for example, an execution report received as a PossDup should not trigger a second fill in the OMS if the original was already processed.

**Session Scheduling:** Exchange FIX sessions operate on defined schedules aligned with market hours:
- **Pre-market session:** Many exchanges accept orders starting at 7:00 or 8:00 ET (some as early as 4:00 ET for extended hours). The FIX session may need to be established before order entry begins to allow for Logon, sequence synchronization, and any pre-open messaging.
- **Market hours:** 9:30-16:00 ET for U.S. equities. FIX sessions must be fully operational before the opening auction.
- **Post-market session:** Order entry may continue until 17:00 or 20:00 ET depending on the venue. Some venues require separate session parameters for extended hours.
- **End-of-day:** Sessions may be logged out and sequence numbers reset (or persisted) at the end of the trading day. The specific end-of-day procedure varies by exchange.

### Market Data Feeds
Market data feeds deliver price, volume, and order book information from trading venues to market participants. The architecture of market data infrastructure directly impacts a firm's ability to price securities, make trading decisions, and meet best execution obligations.

**Data depth tiers:** Level 1 (top of book — NBBO and last sale) suffices for most portfolio and compliance workflows; Level 2 (per-venue depth of book) supports market impact estimation and book-imbalance strategies; Level 3 (order-by-order feeds such as Nasdaq ITCH and Cboe PITCH) enables full book reconstruction for market makers and latency-sensitive strategies. The architectural decision is which tier each consuming application actually needs — feed costs, bandwidth, and feed-handler complexity scale steeply with depth.

**Consolidated Feeds (SIP):**
The Securities Information Processor (SIP) is the regulatory mechanism that produces a consolidated view of quotations and trades across all U.S. equity exchanges. Two SIP plans operate:
- **CTA/CQS (Consolidated Tape Association / Consolidated Quotation System):** Consolidates trades and quotes for securities listed on NYSE, NYSE Arca, NYSE American, and other exchanges. CTA produces the consolidated tape (last sale data) and CQS produces consolidated quotations (NBBO).
- **UTP (Unlisted Trading Privileges Plan):** Consolidates trades and quotes for Nasdaq-listed securities across all venues.
The SIP feeds represent the "official" NBBO and are used as the reference for Regulation NMS trade-through protection. SIP data has historically been slower than direct exchange feeds due to the consolidation process, introducing latency differences that have been the subject of regulatory debate.

**Direct Feeds (Exchange Proprietary):**
Each exchange disseminates its own market data directly to subscribers. Direct feeds provide data only for activity on that specific exchange but arrive faster than the consolidated SIP because they do not go through the consolidation step. Firms that require the lowest latency (market makers, statistical arbitrage, latency-sensitive algorithms) typically subscribe to direct feeds from each exchange and build their own internal NBBO from the individual exchange feeds. This is sometimes called a "synthetic NBBO" or "direct NBBO."

**Market Data Normalization:**
Firms receiving data from multiple sources (SIP, multiple direct feeds, vendor feeds) must normalize the data into a unified internal format. Normalization involves: mapping exchange-specific symbology to the firm's internal security master, converting exchange-specific message formats to a common schema, sequencing messages from different sources by exchange timestamp, handling different price formats (decimal, fractional for fixed income), and deduplicating events that appear on both consolidated and direct feeds.

**Data Vendor Integration:**
Major data vendors provide aggregated and enriched market data:
- **Bloomberg** — The Bloomberg Terminal and Bloomberg B-PIPE provide real-time and historical market data, reference data, and analytics. Bloomberg uses its own symbology (Bloomberg tickers, FIGIs) and data delivery APIs (BLPAPI).
- **Refinitiv (LSEG)** — Refinitiv Elektron provides real-time market data and the Refinitiv Eikon terminal provides analytics. Refinitiv uses RIC (Reuters Instrument Code) symbology.
- **ICE Data Services** — Provides real-time data, reference data, and evaluated pricing across asset classes.
Vendor feeds simplify connectivity by providing a single interface to data from hundreds of venues, but introduce vendor-specific latency, symbology layers, and contractual obligations (exchange data redistribution agreements, per-user licensing).

### Trading Halts and Circuit Breakers
Trading halts and circuit breakers are mechanisms that suspend trading to protect market integrity during periods of extreme volatility or when material information is pending. Systems that interact with exchange order flow must detect, respect, and respond to halts correctly.

**Market-Wide Circuit Breakers (MWCB):**
Market-wide circuit breakers halt trading across all U.S. equity exchanges based on declines in the S&P 500 index. The thresholds are calculated daily based on the prior day's closing value of the S&P 500:
- **Level 1 (7% decline):** If triggered before 3:25 PM ET, trading halts for 15 minutes. If triggered at or after 3:25 PM ET, trading continues.
- **Level 2 (13% decline):** If triggered before 3:25 PM ET, trading halts for 15 minutes. If triggered at or after 3:25 PM ET, trading continues.
- **Level 3 (20% decline):** Trading halts for the remainder of the trading day, regardless of when triggered.
Each level can only be triggered once per day. A Level 1 halt does not prevent a subsequent Level 2 or Level 3 halt if the market continues to decline after trading resumes.

**Limit Up-Limit Down (LULD):**
LULD prevents trades in individual NMS securities from occurring outside specified price bands. The mechanism operates as follows:
- **Reference price:** The arithmetic mean of the reported transaction prices over the preceding five-minute window, updated every 30 seconds during regular trading hours.
- **Price bands:** Calculated as a percentage above and below the reference price. The percentage varies by security tier: 5% for Tier 1 securities (S&P 500, Russell 1000, and certain ETPs) and 10% for Tier 2 securities (all other NMS securities). Wider bands (20%) apply during the first 15 minutes and last 25 minutes of the trading day.
- **Limit state:** If the NBBO reaches the upper or lower price band (i.e., the best offer equals the lower band or the best bid equals the upper band), the security enters a "limit state." Trading continues but orders that would execute outside the bands are not permitted.
- **Trading pause:** If the limit state persists for 15 seconds, the primary listing exchange declares a five-minute trading pause. After the pause, trading resumes through a re-opening auction.
Systems must monitor LULD bands in real time and prevent the submission of orders that would violate the bands.

**Regulatory Halts:**
- **News pending (T1 halt):** The primary listing exchange may halt trading when material news is expected (e.g., an earnings preannouncement, merger announcement, or other market-moving disclosure). Trading resumes after the news is disseminated and the exchange determines that sufficient time has elapsed for the market to absorb the information.
- **News dissemination (T2 halt):** Issued after material news has been released, providing additional time for the market to process the information.
- **SEC trading suspension (Section 12(k)):** The SEC may suspend trading in any security for up to 10 business days if it determines that a suspension is necessary to protect investors and the public interest. SEC suspensions are typically triggered by concerns about the accuracy of publicly available information, insider trading, or market manipulation.
- **IPO/Direct listing halts:** Pre-opening halts for newly listed securities that remain in effect until the opening auction establishes a fair price.

**Exchange-Specific Halts:** Individual exchanges may implement their own halt mechanisms (e.g., volatility interruptions, matching engine issues). These are communicated through exchange-specific market data messages and administrative notices.

**System Handling of Halted Securities:**
When a trading halt is detected, systems should: (1) immediately stop sending new orders for the halted security to the affected venue(s), (2) determine the disposition of open orders — some halt types cause exchanges to cancel all resting orders; others leave them on the book, (3) alert traders and portfolio managers, (4) decide whether to queue new order requests for submission when trading resumes or to reject them, (5) monitor for the resumption message and re-opening auction, and (6) log the halt event for regulatory reporting (CAT reporting includes halt-related order events).

### Symbology and Security Identification
Trading systems must correctly identify securities across venues, data sources, and internal systems. Multiple identification schemes exist, and a single security typically has different identifiers in different contexts.

**Identifier landscape:** Ticker symbols are exchange-assigned, change with corporate actions, and are not globally unique. CUSIP (US/Canada) is proprietary and requires a license from CUSIP Global Services; ISIN wraps the CUSIP for US securities and is required for cross-border settlement and regulatory reporting; SEDOL covers UK and Irish listings; FIGI is Bloomberg's open-license identifier with composite (global) and share-class (venue-level) granularity. The operational problems are licensing, change management, and mapping — not the identifier formats themselves.

**Symbology Mapping:** A security master or symbology mapping service is required to translate between identifier types. For example, Apple Inc. common stock has ticker AAPL (on Nasdaq), CUSIP 037833100, ISIN US0378331005, and FIGI BBG000B9XRY4. When an order is routed to an exchange, the system must use the exchange's expected symbology. When market data arrives from a vendor, the system must map the vendor's identifier to the firm's internal identifier. Symbology mapping must handle: one-to-many relationships (a single corporate entity may have multiple listed securities — common stock, preferred stock, warrants, rights), changes over time (ticker changes, CUSIP changes due to corporate actions), and venue-specific suffixes or extensions.

**Corporate Action Impacts on Symbology:** Corporate actions frequently change identifiers. A ticker change (rebranding) replaces the trading symbol. A CUSIP change occurs when a security's fundamental terms change (stock split resulting in new shares, merger creating a new entity, conversion of a class of shares). Systems must consume reference data updates (typically distributed by exchanges and data vendors overnight and sometimes intraday) to keep symbology current.

**Special Symbols:** Certain suffixes and identifiers denote special trading conditions: "WI" (when-issued — trading before the security is formally issued), "RT" (rights), "WS" (warrants), "U" (units), and exchange-specific suffixes for different share classes (e.g., "A" and "B" for dual-class structures).

### Market Hours and Sessions
U.S. equity markets operate on a defined schedule with distinct trading sessions. Trading systems must enforce session-specific rules for order types, pricing, and routing.

**Pre-Market Session (4:00 AM - 9:30 AM ET):** Some exchanges and ECNs accept orders as early as 4:00 AM ET. Pre-market trading typically has lower liquidity, wider spreads, and may restrict certain order types (e.g., only limit orders permitted, no market orders). Not all securities are available for pre-market trading.

**Regular Trading Session (9:30 AM - 4:00 PM ET):** The primary trading session during which all NMS protections apply (Reg NMS trade-through rules, LULD bands, market-wide circuit breakers). The session begins with an opening auction and ends with a closing auction.

**Post-Market Session (4:00 PM - 8:00 PM ET):** Extended-hours trading after the regular session close. Similar restrictions to pre-market: lower liquidity, limit orders only on many venues, wider spreads.

**Opening Auction (Opening Cross):** Exchanges conduct an opening auction to establish the opening price. During the pre-open period, orders accumulate and the exchange publishes indicative match price and volume. At 9:30 AM ET, the exchange matches accumulated orders at a single clearing price that maximizes executable volume. Nasdaq calls this the "Opening Cross"; NYSE uses its Designated Market Maker (DMM) system to facilitate the open.

**Closing Auction (Closing Cross):** The closing auction determines the official closing price, which is used for NAV calculations, index rebalancing, and benchmarking. On Nasdaq, the Closing Cross accepts Market-On-Close (MOC) and Limit-On-Close (LOC) orders. On NYSE, the DMM facilitates the close. Closing auction volume has grown significantly — on many days, 5-10% or more of total daily volume executes in the closing auction.

**Half-Day Sessions:** U.S. markets close early (1:00 PM ET) on the day before Independence Day (July 3, or July 2 if July 3 is a weekend), the day after Thanksgiving (Black Friday), and Christmas Eve (December 24, or December 23 if December 24 is a weekend). Systems must have a holiday calendar that adjusts session times and early close handling.

**Holiday Calendar Management:** Trading systems must maintain a calendar of market holidays (New Year's Day, MLK Day, Presidents Day, Good Friday, Memorial Day, Juneteenth, Independence Day, Labor Day, Thanksgiving, Christmas) and half-day sessions. The calendar must be updated annually as the exchanges publish their schedules. Holiday calendar errors can result in orders being sent to closed markets (rejected) or orders not being sent when markets are open.

### Connectivity Resilience
Exchange connectivity must be designed for high availability. Failures in connectivity can prevent order submission, cause missed fills, and create compliance and financial risk.

**Primary/Backup Connections:** Every production FIX session or data feed should have a backup. The primary and backup connections should use different physical network paths (different switches, different extranets, different ISPs) to avoid common-mode failures. Some firms maintain primary connectivity through one extranet (e.g., TNS) and backup through another (e.g., IPC) to ensure that a single provider outage does not take down all venue connectivity.

**Failover Testing:** Failover from primary to backup connections must be tested regularly — not only in annual DR (disaster recovery) exercises but through periodic controlled failovers during production trading. Untested failover procedures frequently fail when needed in a real outage.

**Heartbeat Monitoring:** At the FIX session level, heartbeats detect broken connections. At the infrastructure level, firms typically implement additional monitoring: network-level health checks (ping, TCP connect), application-level health checks (periodic test messages or timing checks on data feed throughput), and latency monitoring that alerts on degradation (e.g., round-trip time exceeding a threshold). Monitoring systems should alert both technologists and trading desks when connectivity degrades or fails.

**Session Recovery Procedures:** When a FIX session disconnects unexpectedly, the recovery procedure involves: (1) detecting the disconnection (heartbeat timeout or TCP reset), (2) attempting reconnection with exponential backoff to avoid overwhelming the exchange gateway, (3) re-establishing the session with the persisted sequence numbers, (4) performing gap recovery via ResendRequest/SequenceReset to synchronize state, and (5) reconciling open order state — orders that were submitted before the disconnect may have been filled, partially filled, or canceled during the outage, and the firm must determine the current state of each order upon reconnection.

**Disaster Recovery and Cross-Region Connectivity:** Firms must maintain the ability to resume trading from a secondary site in the event of a primary site failure. DR sites typically have their own exchange connectivity (FIX sessions, market data feeds, network infrastructure) that are kept in standby or warm-standby mode. Critical design decisions include: RTO (Recovery Time Objective) — how quickly must trading resume after a primary site failure, RPO (Recovery Point Objective) — how much order/position state can be lost, and whether the DR site uses the same or different SenderCompIDs (same CompIDs allow seamless continuation; different CompIDs require exchange coordination).

**Performance Monitoring:** Ongoing monitoring of connectivity performance includes: network latency (one-way and round-trip, measured at the application layer), message throughput (messages per second during peak periods), packet loss rates, order acknowledgment latency (time from order submission to exchange acknowledgment), and market data timeliness (gap between exchange timestamp and firm receipt timestamp). Latency spikes or throughput degradation may indicate network congestion, hardware issues, or exchange gateway problems.

### Regulatory Requirements
Firms that connect to exchanges and trading venues are subject to specific regulatory requirements governing their systems, controls, and reporting.

**Regulation SCI (Systems Compliance and Integrity):** SEC Regulation SCI (adopted in 2014, effective November 2015) applies to "SCI entities" — exchanges, certain ATSs that meet volume thresholds (approximately 5% of NMS volume), clearing agencies, the SIP processors, and certain exempt clearing agencies. SCI entities must: establish policies and procedures reasonably designed to ensure that their systems have adequate capacity, integrity, resiliency, availability, and security; conduct periodic reviews and testing of these systems (including business continuity testing); promptly notify the SEC of "SCI events" (system disruptions, system intrusions, and significant system compliance issues); and provide the SEC with annual SCI reviews. While Reg SCI directly applies to exchanges and large ATSs (not to broker-dealers connecting to them), broker-dealers should understand Reg SCI because exchange system failures affect their connectivity and because broker-dealers operating large ATSs may themselves become SCI entities.

**Consolidated Audit Trail (CAT):** The CAT is a comprehensive order tracking system operated by FINRA on behalf of the SROs. CAT requires broker-dealers and exchanges to report the full lifecycle of every order in NMS securities and OTC equity securities — from order origination through routing, modification, cancellation, and execution. CAT reporting includes: customer identification (via the FDID — Firm Designated Identifier), order receipt and origination timestamps, order routing events (including the destination venue), order modifications and cancellations, and execution details (price, quantity, venue). Firms must assign CAT Reporter IDs, map customer accounts to FDIDs, and submit daily reports to the CAT processor. Exchange connectivity infrastructure must capture the timestamps and routing details required for CAT compliance.

**Market Access Controls (SEC Rule 15c3-5):** Rule 15c3-5 requires every broker-dealer that provides market access (including access to an exchange or ATS) to establish, document, and maintain a system of risk management controls and supervisory procedures reasonably designed to manage the financial, regulatory, and other risks of market access. Required controls include: pre-trade controls that prevent the entry of orders that exceed pre-set credit or capital thresholds, prevent the entry of erroneous orders (e.g., price reasonability checks, order size limits, duplicate order detection), restrict access to trading systems to authorized persons, and comply with all applicable regulatory requirements (e.g., short sale restrictions, trading halts). The controls must be under the direct and exclusive control of the broker-dealer — they cannot be delegated to the customer or another party. The broker-dealer must conduct regular reviews (at least annually) of the effectiveness of its market access controls.

**Pre-Trade Risk Controls for Market Access:** Specific controls required or expected under Rule 15c3-5 and exchange rules include: order price collars (rejecting orders with prices far from the current market), maximum order size limits, position limits and capital exposure limits per symbol and aggregate, duplicative order detection, kill switches that can halt all order flow from a firm if a risk threshold is breached, restricted securities lists (preventing trading in halted, delisted, or restricted securities), and short sale compliance checks. These controls must operate in real time with minimal latency impact.

## Worked Examples

Three worked examples are in [references/examples.md](references/examples.md) — load for an end-to-end scenario: (1) designing FIX connectivity to five equity venues with Rule 15c3-5 controls, (2) building market data infrastructure with consolidated and direct feeds, (3) implementing trading halt handling across OMS, SOR, and market data systems.

## Common Pitfalls
- Failing to persist FIX sequence numbers across application restarts, leading to sequence number resets that can cause duplicate order submissions or missed execution reports
- Using a single network path for both primary and backup FIX sessions, so that a single switch or carrier failure takes down both connections simultaneously
- Not handling PossDupFlag correctly during gap recovery — processing a PossDup execution report as a new fill results in double-counting
- Relying solely on the SIP for NBBO when the firm's trading strategy is latency-sensitive — the SIP is slower than direct feeds by hundreds of microseconds to single-digit milliseconds
- Ignoring LULD price band updates in the order router, leading to orders being rejected by the exchange for violating price bands
- Treating all halt types identically — different halt types have different implications for resting orders, resume mechanisms, and regulatory obligations
- Not maintaining a current and tested holiday calendar, causing the system to attempt trading on market holidays or to miss half-day early closes
- Deploying pre-trade risk controls (Rule 15c3-5) that can be circumvented, overridden, or disabled by trading staff — the controls must be under the exclusive control of the broker-dealer's risk management function
- Failing to test failover procedures regularly — an untested backup connection that does not work during a real outage provides no resilience
- Using ticker symbols as the sole identifier in internal systems — ticker symbols change, are reused, and are not globally unique; internal systems should use stable identifiers (CUSIP, ISIN, or internal IDs) with symbology mapping
- Not accounting for the difference between exchange timestamps and receipt timestamps when analyzing latency — the two clocks may not be synchronized, and one-way latency measurements require clock synchronization (e.g., PTP or GPS)
- Assuming that a FIX session Logon means the exchange is ready to accept orders — many exchanges have separate "trading session status" messages that indicate when the matching engine transitions from pre-open to open

## Cross-References
- **order-lifecycle** (trading-operations plugin): Order states, order types, and the order lifecycle from creation through execution or cancellation — exchange connectivity is the transport layer that carries order lifecycle events
- **trade-execution** (trading-operations plugin): Execution algorithms, venue selection, and smart order routing depend on the connectivity and market data infrastructure described in this skill
- **pre-trade-compliance** (trading-operations plugin): Pre-trade risk controls (Rule 15c3-5) are a regulatory requirement for market access and must be integrated into the exchange connectivity architecture
- **settlement-clearing** (trading-operations plugin): Post-execution, trades flow from exchange connectivity systems through clearing and settlement — correct venue and execution identifiers are critical for downstream processing
- **operational-risk** (trading-operations plugin): Exchange connectivity failures are a significant source of operational risk, and the resilience, failover, and monitoring practices in this skill are operational risk controls
- **books-and-records** (compliance plugin): Order and execution data captured through exchange connectivity must be retained per SEC Rules 17a-3 and 17a-4, and CAT reporting obligations require comprehensive audit trail data from connectivity systems
