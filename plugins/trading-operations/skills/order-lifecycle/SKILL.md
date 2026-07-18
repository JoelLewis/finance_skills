---
name: order-lifecycle
description: "Guide the design and implementation of order lifecycle management in trading systems. Owns FIX application-layer message flows (NewOrderSingle, ExecutionReport, cancel/replace) and order state. Use when building an order state machine for an OMS or EMS, handling cancel/replace race conditions, defining pre-submission validation rules (buying power, position limits, restricted lists), selecting order types and time-in-force instructions, designing multi-leg or OCO or bracket orders, building CAT-compliant audit trails, troubleshooting order rejections or unexpected state transitions, hardening an OMS against edge cases, or implementing order persistence and recovery for failover. Also covers execution-report handling, ClOrdID chaining, and partial fill aggregation. For FIX session management (logon, sequence gaps, disconnects) see exchange-connectivity."
---

# Order Lifecycle

## Core Concepts

### Order State Machine
The order state machine is the central abstraction in any order management system. It defines every state an order can occupy and every valid transition between states. A correctly implemented state machine prevents impossible transitions (such as filling a canceled order), ensures audit trail completeness, and provides the foundation for order status reporting to clients, counterparties, and regulators.

**Canonical order states:**

- **New:** The order has been created internally but not yet transmitted to an execution venue. This is the initial state in the OMS after order entry and validation.
- **Pending New:** The order has been transmitted to the execution venue but no acknowledgment has been received. The order is in flight. This state exists because network latency and venue processing time create a window between submission and acceptance.
- **Accepted (New on venue):** The execution venue has acknowledged receipt of the order and placed it on the order book. The FIX ExecType=New / OrdStatus=New acknowledgment has been received.
- **Partially Filled:** The order has received one or more executions but the full quantity has not yet been filled. The cumulative filled quantity is greater than zero but less than the order quantity.
- **Filled:** The order has been completely executed. The cumulative filled quantity equals the order quantity. This is a terminal state.
- **Pending Cancel:** A cancel request has been submitted for the order but the venue has not yet confirmed the cancellation. The original order may still receive fills during this window — this is a critical race condition.
- **Canceled:** The order has been successfully canceled by the venue. Any unfilled quantity is no longer eligible for execution. This is a terminal state. If partial fills occurred before cancellation, the order is sometimes described as "partially filled and canceled" — the fills stand and the remaining quantity is canceled.
- **Pending Replace:** A cancel/replace (amend) request has been submitted but not yet confirmed. As with Pending Cancel, fills may still arrive during this window.
- **Replaced:** The original order has been replaced by a new order with amended parameters (price, quantity, or other fields). The original order transitions to Replaced (terminal), and a new order is created with the amended terms. In FIX, replacement creates a chain linked by ClOrdID and OrigClOrdID.
- **Rejected:** The execution venue has rejected the order. Common rejection reasons include invalid symbol, invalid order type for the venue, price outside acceptable range, insufficient permissions, or market closed. This is a terminal state.
- **Expired:** The order's time-in-force instruction caused it to expire without being fully filled. A DAY order expires at market close; a GTD order expires on its specified date. This is a terminal state.
- **Suspended:** The order has been temporarily suspended by the venue, typically due to a trading halt on the security, a circuit breaker activation, or a regulatory halt. The order remains on the book but is not eligible for matching until the suspension is lifted.
- **Done for Day:** The order is not eligible for further execution on the current trading day but may resume on the next trading day. This applies to multi-day orders (GTC) that have not yet been fully filled.

**Terminal vs. non-terminal states:** Terminal states (Filled, Canceled, Replaced, Rejected, Expired) represent the end of an order's lifecycle — no further transitions are possible. Non-terminal states (New, Pending New, Accepted, Partially Filled, Pending Cancel, Pending Replace, Suspended, Done for Day) may transition to other states. The state machine must enforce the invariant that no transition out of a terminal state is ever permitted.

**Valid state transitions (representative, not exhaustive):**

- New -> Pending New (order submitted to venue)
- Pending New -> Accepted (venue acknowledges)
- Pending New -> Rejected (venue rejects)
- Accepted -> Partially Filled (first partial execution)
- Accepted -> Filled (single complete execution)
- Accepted -> Pending Cancel (cancel request sent)
- Accepted -> Pending Replace (replace request sent)
- Accepted -> Expired (time-in-force expiration)
- Accepted -> Suspended (trading halt)
- Partially Filled -> Partially Filled (additional partial execution)
- Partially Filled -> Filled (final execution completes order)
- Partially Filled -> Pending Cancel (cancel remaining quantity)
- Partially Filled -> Pending Replace (amend remaining quantity or price)
- Pending Cancel -> Canceled (cancel confirmed)
- Pending Cancel -> Filled (fill arrived before cancel was processed — race condition)
- Pending Cancel -> Partially Filled (partial fill during cancel processing)
- Pending Replace -> Replaced (replace confirmed, new order created)
- Pending Replace -> Filled (fill arrived before replace was processed)
- Pending Replace -> Partially Filled (partial fill during replace processing)
- Pending Replace -> Canceled (venue canceled instead of replacing, sometimes due to insufficient quantity after a fill)
- Suspended -> Accepted (halt lifted, order reactivated)
- Suspended -> Expired (order expires during halt)
- Done for Day -> Accepted (next trading day, order reactivated)
- Done for Day -> Expired (GTC expiration reached)

**State persistence and recovery:** The order state must be persisted durably — typically to a database or write-ahead log — before any acknowledgment is sent to the order originator or any action is taken on the order. If the OMS restarts after a crash, it must be able to reconstruct the current state of every active order from persisted state plus any messages received from execution venues during recovery. This requires idempotent message processing (handling duplicate execution reports without double-counting fills) and state reconciliation with venue order status queries.

### Order Types
Order types define the execution instructions that govern how an order interacts with the market.

- **Market order:** Execute immediately at the best available price. Guarantees execution (in liquid markets) but not price. Appropriate for urgent execution needs. Risk: slippage in volatile or illiquid markets; the execution price may differ substantially from the last quoted price.
- **Limit order:** Execute at the specified price or better (buy at or below the limit; sell at or above the limit). Guarantees price but not execution. Appropriate when price control is more important than execution certainty. Risk: the order may not fill if the market does not reach the limit price; partial fills may leave a residual position.
- **Stop order (stop-loss):** Becomes a market order when the stop price is reached (or traded through). Used to limit losses or protect profits on existing positions. Risk: once triggered, the order executes as a market order and may fill at a significantly worse price than the stop price in a gapping or volatile market.
- **Stop-limit order:** Becomes a limit order (not a market order) when the stop price is reached. The stop price triggers the order; the limit price controls execution. Provides more price protection than a stop order. Risk: the order may trigger but not fill if the market gaps through the limit price.
- **Trailing stop:** A stop order where the stop price adjusts automatically as the market moves in the order's favor. The stop is set as a fixed amount or percentage below (for sells) or above (for buys) the market price. As the market moves favorably, the stop trails the market; when the market reverses by the trail amount, the stop is triggered. Risk: same as stop orders once triggered; additionally, the trail amount must be calibrated to avoid triggering on normal market noise.
- **Market-on-close (MOC):** Execute at the closing auction price. Used for benchmark-tracking strategies and end-of-day portfolio adjustments. Exchanges impose cutoff times for MOC orders (NYSE: 3:50 PM Eastern). Risk: no price control; closing auction prices can be volatile.
- **Limit-on-close (LOC):** Execute at the closing auction price only if the closing price is at or better than the specified limit. Provides price protection for close-targeted execution. Risk: the order may not fill if the closing price exceeds the limit.
- **Pegged orders:** The order price is pegged to a reference price (typically the NBBO midpoint, best bid, or best offer) and adjusts automatically as the reference price moves. Used in algorithmic and institutional trading to passively follow the market. Behavior is venue-specific.
- **Iceberg (reserve) orders:** Only a portion of the total order quantity is displayed on the order book; the rest is hidden (the "reserve" quantity). As the displayed quantity is filled, additional shares from the reserve are replenished on the book. Used to minimize market impact for large orders by concealing the full order size. Risk: sophisticated participants may detect iceberg patterns; not all venues support reserve orders.

### Time-in-Force Instructions
Time-in-force (TIF) instructions specify how long an order remains active before it is automatically canceled or expires.

- **DAY:** The order is valid for the current trading day only. If not filled by market close, it is canceled. This is the default TIF for most venues and order management systems. Overnight risk: DAY orders do not carry forward; if the advisor intends to maintain the order, it must be resubmitted the next trading day.
- **GTC (Good Til Canceled):** The order remains active until explicitly canceled by the originator or until the venue's maximum GTC duration is reached (commonly 60 to 90 calendar days, venue-dependent). GTC orders survive market close and are reactivated each trading day. Risk: stale GTC orders may execute at prices that no longer reflect the current investment thesis; firms must implement GTC order review processes to periodically reassess open GTC orders.
- **IOC (Immediate or Cancel):** The order must execute immediately, in whole or in part. Any portion not immediately filled is canceled. IOC orders never rest on the order book. Appropriate for liquidity-taking strategies where the trader wants to interact with currently available liquidity without posting a passive order.
- **FOK (Fill or Kill):** The order must be filled in its entirety immediately or canceled entirely. No partial fills are accepted. More restrictive than IOC. Appropriate when partial execution is unacceptable — for example, a hedging trade that must fully offset a risk position.
- **GTD (Good Til Date):** The order remains active until a specified date or until canceled. Behaves like GTC but with a defined expiration date. Useful for orders tied to a specific event or deadline.
- **OPG (At the Open):** The order participates in the opening auction only. If not filled during the opening process, it is canceled. Used when the opening price is the desired execution benchmark.
- **CLO (At the Close):** The order participates in the closing auction. Functionally similar to MOC but expressed as a time-in-force instruction rather than an order type. Venue implementations vary.

**Behavior at market close:** DAY orders are canceled. GTC and GTD orders transition to Done for Day and are reactivated the next trading day. IOC and FOK orders, by definition, will have already been filled or canceled before close. MOC and LOC orders execute during the closing auction. The OMS must correctly handle each TIF at the end-of-day transition, including generating appropriate cancel confirmations for expired DAY orders and updating state for multi-day orders.

**Overnight handling:** GTC orders that are Done for Day must be resubmitted or reactivated at the venue on the next trading day. Some venues maintain GTC orders natively; others require the OMS to resubmit them each morning. The OMS must track which GTC orders need resubmission and handle the resubmission process as part of the start-of-day workflow.

### FIX Protocol Fundamentals
The Financial Information eXchange (FIX) protocol is the dominant standard for electronic trading communication. Understanding FIX is essential for building or integrating with any execution venue, broker, or counterparty.

**FIX message types for order flow:**

- **NewOrderSingle (MsgType=D):** Submits a new order to the venue. Contains all order parameters: symbol, side, quantity, order type, price, time-in-force, and account.
- **ExecutionReport (MsgType=8):** The venue's primary response message. Used to acknowledge new orders (ExecType=New), report fills (ExecType=Trade or ExecType=Fill), report partial fills (ExecType=Trade with remaining quantity > 0), confirm cancellations (ExecType=Canceled), confirm replacements (ExecType=Replaced), report rejections (ExecType=Rejected), and report expirations (ExecType=Expired). The ExecutionReport is the most important message in the FIX order flow — it drives all state transitions in the OMS.
- **OrderCancelRequest (MsgType=F):** Requests cancellation of a previously submitted order. Includes the OrigClOrdID (the ClOrdID of the order to cancel) and a new ClOrdID for the cancel request itself.
- **OrderCancelReplaceRequest (MsgType=G):** Requests modification of a previously submitted order (price, quantity, or other parameters). Includes the OrigClOrdID and a new ClOrdID. The venue treats this as a cancel of the original order and acceptance of a new order with the amended terms — atomically, if possible.
- **OrderCancelReject (MsgType=9):** The venue's response when a cancel or replace request cannot be honored. Common reasons: the order has already been filled, the order has already been canceled, or the order is in a state that does not permit cancellation (e.g., suspended during a halt).

**Key FIX tags:** The tags that drive OMS state are ClOrdID (11) / OrderID (37) / OrigClOrdID (41) for order identification and chaining, OrdStatus (39) and ExecType (150) for state transitions, and CumQty (14) / LeavesQty (151) / AvgPx (6) for fill accounting. Trust the venue's LeavesQty rather than deriving remaining quantity independently — the two can diverge after partial fills and replacements.

**FIX session vs. application layer:** FIX operates on two layers: the session layer (connection management, heartbeats, sequence numbers, gap recovery) and the application layer (orders, executions, cancels — the subject of this skill). Session-layer management is owned by the exchange-connectivity skill (trading-operations); a lost session requires reconnection and sequence reconciliation there before application-level messaging can resume.

**FIX versions:** FIX 4.2 remains widely deployed and is the baseline for many venues. FIX 4.4 added improvements including better support for multi-leg orders and allocation messaging. FIX 5.0 introduced the FIXT transport layer (separating session and application protocols) and added support for market data and post-trade messaging. When connecting to a new venue, confirm which FIX version and which message extensions (if any) the venue supports.

### Cancel and Replace Workflows
Cancel and replace workflows are among the most operationally sensitive parts of order lifecycle management. They involve concurrent state changes, race conditions, and the possibility of unexpected outcomes.

**Cancel request flow:**
1. The OMS sends an OrderCancelRequest (MsgType=F) to the venue, referencing the OrigClOrdID of the order to cancel and assigning a new ClOrdID to the cancel request.
2. The order transitions to Pending Cancel in the OMS.
3. The venue responds with either an ExecutionReport (ExecType=Canceled, OrdStatus=Canceled) confirming the cancel, or an OrderCancelReject (MsgType=9) rejecting the cancel request.
4. If canceled, the order transitions to Canceled (terminal). If rejected, the order reverts to its prior state (Accepted or Partially Filled).

**Replace (amend) request flow:**
1. The OMS sends an OrderCancelReplaceRequest (MsgType=G) to the venue, referencing the OrigClOrdID and providing the amended order parameters (new price, new quantity, or both) with a new ClOrdID.
2. The order transitions to Pending Replace.
3. The venue responds with either an ExecutionReport (ExecType=Replaced, OrdStatus=Replaced) confirming the replacement, or an OrderCancelReject rejecting the request.
4. If replaced, the original order transitions to Replaced (terminal) and a new order is created in the OMS with the amended parameters and the new ClOrdID. If rejected, the original order reverts to its prior state.

**Race conditions — cancel vs. fill:** The most critical race condition occurs when a cancel request and a fill cross in flight. The OMS sends a cancel request, but before the venue processes it, the order fills (fully or partially). The venue may respond with a fill ExecutionReport followed by an OrderCancelReject (because the order is now filled and cannot be canceled), or with both a fill and a cancel confirmation (if only a partial fill occurred and the remaining quantity was canceled). The OMS must handle all possible message orderings:
- Fill arrives first, then CancelReject: The order is Filled. The cancel request is moot.
- CancelReject arrives first, then Fill: The OMS must not revert from Pending Cancel to the prior state until it processes the fill. Sequence matters.
- Partial Fill and Cancel confirmation: The order was partially filled before the cancel took effect. The partial fill stands; the remaining quantity is canceled.

**Order chaining (ClOrdID to OrigClOrdID linking):** Each cancel or replace creates a new link in the order chain. The original order has ClOrdID=A. A replace request references OrigClOrdID=A and assigns ClOrdID=B. A subsequent replace references OrigClOrdID=B and assigns ClOrdID=C. The OMS must maintain this chain to correctly correlate all messages belonging to the same logical order. Breaking the chain — for example, referencing the wrong OrigClOrdID — will cause the venue to reject the request or, worse, cancel or replace the wrong order.

**Pending state discipline:** While an order is in Pending Cancel or Pending Replace, the OMS should not submit additional cancel or replace requests for the same order. Submitting concurrent cancel/replace requests creates ambiguity about which request the venue is processing and can lead to unexpected outcomes. Queue any new cancel or replace intent until the pending request is resolved.

### Order Validation
Order validation is the set of checks performed before an order is submitted to an execution venue. Thorough validation catches errors early, prevents rejections at the venue, and enforces risk management and compliance constraints.

**Pre-submission validation (OMS-level):**

- **Buying power / margin check:** Verify that the account has sufficient cash or margin to cover the order. For buy orders, check available cash or buying power. For short sell orders, check margin availability and locate requirements (Reg SHO).
- **Position limits:** Verify that the order would not cause the account (or the firm aggregate) to exceed position limits, either regulatory (exchange-imposed position limits for options and futures) or internal (risk management limits).
- **Restricted list screening:** Check the security against the firm's restricted list. Orders for restricted securities are hard-blocked. This check is a legal and compliance requirement to prevent trading on material non-public information.
- **Market hours validation:** Verify that the order is being submitted during appropriate market hours for the venue and security. Pre-market and after-hours orders require explicit eligibility and may only support certain order types (typically limit orders).
- **Symbol validation:** Verify that the security identifier (ticker, CUSIP, ISIN, SEDOL) is valid and maps to an active, tradable security on the target venue.
- **Lot size validation:** Verify that the order quantity conforms to the venue's lot size requirements (round lot, odd lot, or mixed lot). Some venues reject odd-lot orders or route them differently.
- **Price reasonableness:** For limit orders, check that the limit price is within a reasonable range of the current market price. An order to buy at 10x the current price is likely an error. Configurable thresholds (e.g., limit price must be within 10% of the last traded price) catch fat-finger errors.
- **Duplicate order detection:** Check whether an identical or near-identical order was recently submitted for the same account and security. Duplicates may indicate double-entry errors.

**Exchange-level validation:** Even after OMS validation, the exchange performs its own checks: valid symbol for the venue, order type supported by the venue, price within the venue's price band (limit-up/limit-down), quantity within the venue's maximum order size, and participant permissions. Exchange rejections result in a FIX Reject or ExecutionReport with ExecType=Rejected and a reason code.

**Reject handling and error codes:** When an order is rejected — either by the OMS or by the venue — the rejection reason must be captured, logged, and communicated to the order originator. FIX Tag 103 (OrdRejReason) provides standardized rejection codes: broker/exchange option (0), unknown symbol (1), exchange closed (2), order exceeds limit (3), too late to enter (4), unknown order (5), duplicate order (6), and others. The OMS should map venue-specific rejection codes to actionable error messages for traders and operations staff.

### Multi-Leg and Contingent Orders
Trading systems must support orders that involve multiple legs or contingent execution logic.

- **OCO (One Cancels Other):** Two orders are linked such that when one is filled (or partially filled), the other is automatically canceled. Common use case: a profit target limit order and a stop-loss order bracketing an existing position. When one triggers, the other becomes unnecessary. The OMS must monitor both orders and initiate the cancel of the surviving order when the first one fills.
- **Bracket orders:** A three-part structure: an entry order, a profit target order, and a stop-loss order. The profit target and stop-loss are submitted only after the entry order fills, and they form an OCO pair. Bracket orders require conditional logic in the OMS — the child orders depend on the parent order's state.
- **Conditional orders:** Orders that are activated only when a specified condition is met — for example, "submit a buy limit order for AAPL at $150 if the S&P 500 drops below 4,000." The OMS must monitor the condition in real time and submit the order when the condition triggers.
- **Order lists:** A group of orders submitted together with a defined execution strategy (e.g., all-or-none for the list, sequential execution, or independent execution). FIX supports order list messaging through the NewOrderList (MsgType=E) message.
- **Parent-child relationships:** Complex order structures where a parent order spawns child orders upon execution. For example, a parent buy order for 10,000 shares may spawn multiple child orders routed to different venues as part of a smart order routing strategy. The OMS must track the relationship between parent and children and aggregate child fills to update the parent order's status.

### Order Audit Trail
Regulatory requirements mandate comprehensive audit trails for all order activity.

**Consolidated Audit Trail (CAT):** CAT, which replaced FINRA's OATS (Order Audit Trail System), requires broker-dealers and certain other participants to report detailed lifecycle events for every order in NMS securities and listed options. Reportable events include order receipt, order origination, order routing, order modification (cancel/replace), order execution, and order cancellation. CAT requires customer identification at the point of order origination, enabling regulators to trace every order from inception through execution or cancellation, across all venues and intermediaries.

**Timestamp precision:** CAT requires timestamps with millisecond precision at minimum, and many firms capture microsecond or nanosecond precision for internal analytics and compliance. Clock synchronization across all systems in the order flow is essential — FINRA Rule 4590 requires clocks to be synchronized within specified tolerances (generally one second for manual events, 50 milliseconds for electronic events). Timestamp drift between the OMS, FIX gateway, and execution venues can create audit trail inconsistencies that are difficult to resolve.

**Order event logging:** Every state transition, every message sent, and every message received must be logged with a timestamp, the message content (or key fields), and the system component that processed the event. The log must be immutable — entries cannot be modified or deleted after creation. This event log forms the basis for regulatory reporting, dispute resolution, and operational forensics.

**Reconstruction capability:** Regulators may request a complete reconstruction of order activity for a specific time period, security, account, or trader. The audit trail must support reconstruction at any level of granularity: a single order's complete lifecycle, all orders for a security during a trading session, or all orders originated by a specific desk or individual. Reconstruction requires correlating OMS records, FIX message logs, execution venue reports, and clearing/settlement records.

## Worked Examples

Three worked examples are in [references/examples.md](references/examples.md) — load for an end-to-end scenario: (1) designing an order state machine for a broker-dealer's OMS, (2) implementing cancel/replace workflows with race-condition handling, (3) integrating FIX connectivity to a new execution venue (see exchange-connectivity for session-layer detail).

## Common Pitfalls
- Implementing the state machine as a denylist (blocking specific transitions) rather than an allowlist (permitting only explicitly defined transitions) — the denylist approach lets novel invalid transitions through silently
- Failing to handle the cancel-vs-fill race condition, resulting in dropped fills when a fill ExecutionReport arrives for an order in PendingCancel state
- Updating the ClOrdID optimistically before the venue confirms a replace, causing subsequent requests to reference a ClOrdID the venue does not recognize
- Permitting concurrent cancel and replace requests for the same order, creating ambiguous state at the venue
- Not persisting order state before acknowledging or acting on inbound messages, causing state loss on system restart
- Treating FIX sequence numbers casually — skipping gap fill processing or resetting sequence numbers without bilateral agreement leads to lost messages
- Ignoring LeavesQty in ExecutionReports and calculating remaining quantity independently, which can diverge from the venue's view after partial fills and replacements
- Implementing GTC orders without a periodic review process, allowing stale limit orders to execute at prices that no longer reflect the investment thesis
- Validating orders only at the venue (relying on exchange rejections) rather than performing pre-submission validation in the OMS, which increases rejection rates and round-trip latency
- Assuming all venues implement FIX identically — each venue has interpretation differences, custom tags, and specific message flow behaviors that must be discovered during certification
- Logging order events without sufficient timestamp precision or clock synchronization, producing an audit trail that cannot support regulatory reconstruction requirements
- Failing to implement idempotent message processing, causing duplicate ExecutionReports (common during FIX session recovery) to double-count fills and corrupt position tracking
- Not enforcing terminal state immutability, allowing application bugs to transition orders out of Filled, Canceled, or Rejected states

## Cross-References
- **trade-execution** (trading-operations plugin): Execution algorithms, venue selection, smart order routing, and market microstructure that determine how orders are executed once they leave the OMS.
- **pre-trade-compliance** (trading-operations plugin): Compliance checks that gate order submission, including restricted list screening, position limits, and regulatory constraints integrated into the order validation workflow.
- **post-trade-compliance** (trading-operations plugin): Compliance monitoring after execution, including trade surveillance, best execution analysis, and exception reporting that consumes order lifecycle data.
- **settlement-clearing** (trading-operations plugin): The downstream process after order execution — trade matching, clearing through CCP or bilateral netting, and settlement of securities and cash that completes the order lifecycle.
- **order-management-advisor** (advisory-practice plugin): Advisor-specific order management covering block trading, allocation, model-driven trading, and custodian routing that builds on the order lifecycle concepts defined here.
- **exchange-connectivity** (trading-operations plugin): Technical infrastructure for connecting to exchanges and execution venues, including FIX engine configuration, network architecture, and failover design.
- **books-and-records** (compliance plugin): Recordkeeping requirements under SEC Rules 17a-3/17a-4 and Rule 204-2 that govern retention of order tickets, execution records, and audit trail data generated throughout the order lifecycle.
