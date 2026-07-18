---
name: market-data
description: "Design and manage market data infrastructure — real-time and delayed feeds, Level 1/2/3 depth, consolidated tape vs direct feeds, vendor selection, licensing, and distribution architecture. Use when choosing between real-time and delayed data, evaluating market data vendors like Bloomberg or Refinitiv, designing ticker plants or fan-out architecture, managing exchange data licensing and entitlements, diagnosing stale quotes or missing ticks, deciding between SIP and direct exchange feeds, or assessing Level 2/3 depth-of-book requirements for trading. Trigger on: market data, Level 1/2/3, depth of book, consolidated tape, SIP, direct feed, NBBO, ticker plant, B-PIPE, data license, non-display use, market data entitlements, conflation, tick data, real-time feed."
---

# Market Data

## Core Concepts

### 1. Market Data Types

- **Trade data:** Last sale price, quantity, timestamp, condition codes (regular, odd lot,
  opening/closing), cumulative volume, VWAP.
- **Quote data:** NBBO (best bid/offer across all exchanges), bid/ask sizes. Quote updates
  vastly outnumber trade updates in liquid instruments.
- **Depth of book:** Multiple price levels beyond the NBBO with resting order quantities.
  Aggregated depth (size per level) or order-by-order (individual orders visible).
- **Index data:** Real-time index values, composition, weightings, total return values.
  Sources include exchange-calculated (S&P 500 via Cboe) and third-party (MSCI, FTSE Russell).
- **Fixed income pricing:** Dealer quotes, evaluated pricing (ICE, Bloomberg BVAL), TRACE
  trade reports for corporates, EMMA for municipals. Inherently less standardized than equities.
- **Options data:** Chains (strikes/expirations), Greeks, implied volatility, volume, open
  interest. OPRA provides the consolidated options feed.
- **Fundamental data:** Earnings, financial statements, corporate actions, analyst estimates.
  Sourced from vendors (Bloomberg, FactSet, S&P Capital IQ) rather than exchange feeds.
- **News and events:** Headlines, economic calendar (FOMC, employment), corporate events
  (earnings dates, ex-dates), sentiment scores.

### 2. Data Levels

**Level 1 — Top of Book:** NBBO, last sale, volume, daily OHLC. Sufficient for portfolio
management, client reporting, and order entry. Lowest cost and bandwidth.

**Level 2 — Market Depth:** Multiple price levels with aggregate size (top 5-20 levels per
side). Reveals liquidity beyond the NBBO. Essential for active trading, market impact
assessment, and algorithmic execution (TWAP, VWAP). Higher cost and bandwidth.

**Level 3 — Full Order Book:** Individual order detail (price, size, order ID) enabling
complete book reconstruction and order lifecycle tracking. Provided by direct feeds (Nasdaq
ITCH, NYSE Arca). Required for market making, HFT, and queue position modeling. Highest
cost — hundreds of thousands of messages per second per exchange.

| Use Case | Level | Rationale |
|---|---|---|
| Portfolio management / reporting | Level 1 | NBBO and last sale sufficient for valuation |
| Active equity trading desk | Level 2 | Traders assess depth before large orders |
| Algorithmic execution | Level 2 | Algorithms adapt pace based on available liquidity |
| Market making / HFT | Level 3 | Requires queue position and order flow modeling |
| Client-facing app (delayed) | Level 1 (delayed) | Display only, 15-minute delay acceptable |

### 3. Consolidated Tape vs Direct Feeds

**Securities Information Processors (SIPs):** CTA/CQS for NYSE-listed (Tape A/B), UTP for
Nasdaq-listed (Tape C), OPRA for options. SIPs collect data from all exchanges, compute the
NBBO, and disseminate a consolidated stream. Under Reg NMS, the SIP NBBO is the regulatory
benchmark for best execution.

**Direct exchange feeds:** Proprietary feeds from individual exchanges (NYSE Arca, Nasdaq
TotalView/ITCH, Cboe PITCH, IEX DEEP) delivering order-by-order data with lower latency
than the SIP. A firm must subscribe to multiple feeds and compute NBBO internally. Each
exchange uses different protocols requiring per-exchange parsers.

| Dimension | SIP (Consolidated) | Direct Feeds |
|---|---|---|
| Latency | Higher (~10-50 microseconds SIP processing) | Lower (bypasses SIP) |
| NBBO | Provided directly | Must compute from multiple feeds |
| Data depth | Level 1 (NBBO + last sale) | Level 2/3 (full depth, order-by-order) |
| Cost | Lower, predictable | Higher, scales with exchange count |
| Normalization | Pre-normalized | Requires per-exchange parsers |
| Typical consumer | Buy-side, advisory, retail | Prop trading, market making, HFT |

### 4. Market Data Vendors

Cost figures throughout this skill reflect 2024-2025 list pricing; verify current pricing with vendors before budgeting.

**Bloomberg:** Terminal ($20K-$25K/user/year), B-PIPE (enterprise real-time feed), Data
License (bulk EOD/reference data), BEAP (cloud API).

**Refinitiv (LSEG):** Eikon (desktop, lower cost than Bloomberg, strong FX/FI), Elektron/
LSEG Real-Time (enterprise feed), DataScope (bulk EOD), Tick History (historical ticks).

**ICE Data Services:** Consolidated feeds, evaluated fixed income pricing (widely used for
NAV and regulatory reporting), ICE Benchmark Administration.

**FactSet:** Research-oriented, flexible API delivery, competitive pricing for smaller
buy-side, strong Excel/portfolio management integration.

**S&P Capital IQ / Market Intelligence:** Comprehensive fundamentals, credit ratings,
company filings. **Morningstar:** Fund/ETF data, ratings, Morningstar Direct for research.

**Free/open sources:** Exchange websites and financial portals provide delayed (15-min)
quotes. Useful for non-time-sensitive display but limited reliability and coverage.

**Vendor selection criteria:** Asset class coverage, latency, reliability/uptime SLA, API
quality, total licensing cost (including exchange fees), historical data depth, support,
data quality handling.

### 5. Market Data Licensing and Entitlements

**License categories:** Non-professional (retail, personal use, lower fees) vs professional
(business use, significantly higher). Display (human views on screen) vs non-display
(automated systems: algorithms, risk engines, pricing — fees based on application type, not
per-user). Derived data (substantially transformed; redistribution may be permitted if
original data cannot be reverse-engineered; policies vary by exchange).

**Licensing models:** Per-user/per-device (exact monthly count required), enterprise (flat
fee covering a defined entity), usage-based non-display (fees by application category:
trading, risk, valuation).

**Reporting obligations:** Monthly/quarterly subscriber counts submitted to each exchange or
via data vendor. Under-reporting triggers back-billing, penalties, and contract termination.

**Redistribution:** Raw exchange data requires explicit redistribution agreements and
additional fees for client-facing display. Vendors typically handle redistribution for data
consumed through their platforms.

**Cost management:** Audit usage periodically to eliminate unused subscriptions. Use delayed
data where real-time is unnecessary. Track non-display use — many firms discover unreported
non-display obligations only during exchange audits.

### 6. Market Data Distribution Architecture

**Ticker plant:** Central ingestion and normalization layer. Parses exchange protocols (ITCH,
PITCH, FIX), normalizes to unified schema, maps symbology, caches latest values, applies
conflation, and monitors feed health.

**Fan-out patterns:** Topic-based pub-sub (dominant pattern; middleware: Solace, TIBCO,
29West, Kafka for lower-latency needs), request-reply (REST for on-demand lookups),
multicast (network-level fan-out for ultra-low-latency co-located environments).

**Conflation:** Throttles update rates for slower consumers. Time-based (deliver latest
value every N ms), change-based (suppress duplicates), priority-based (never conflate
trades; conflate quotes for slower consumers).

**APIs:** REST for historical/reference data, WebSocket for real-time streaming to web/mobile
applications, proprietary binary APIs for ultra-low-latency consumers.

**Cloud services:** AWS Data Exchange, Google Cloud Marketplace, Azure Data Share. Adds
network latency (unsuitable for latency-sensitive trading) but appropriate for analytics,
portfolio management, and client-facing applications.

### 7. Historical Market Data

**EOD databases:** Daily OHLCV. Sufficient for portfolio analytics and long-horizon
backtesting. **Tick-level data:** Every trade/quote with microsecond timestamps. Required for
intraday backtesting and microstructure research. A single day of U.S. equity ticks may
exceed 10-20 TB. Providers: Refinitiv Tick History, NYSE TAQ, LOBSTER.

**Adjusted vs unadjusted prices:** Unadjusted for trade-level analysis and regulatory
records. Split-adjusted and fully adjusted (splits + dividends) for return calculations.

**Survivorship bias:** Databases including only current listings inflate backtested returns.
Point-in-time databases (showing the universe as it existed historically) are required for
unbiased research. **Point-in-time data** also applies to fundamentals: initial earnings
reports may be restated; using restated data introduces look-ahead bias.

### 8. Market Data Quality

**Stale data detection:** Flag quotes not updated within expected timeframes during market
hours. Suppress stale data from trading and valuation decisions.

**Gap detection:** Feed-level (sequence number gaps in ITCH/PITCH) and application-level
(expected vs actual data frequency).

**Erroneous tick filtering:** Process exchange trade-bust messages. Filter outlier prints
(prices far from NBBO, adjusted for spread and volatility). Distinguish legitimate unusual
trades (blocks, auctions, after-hours) from errors.

**Monitoring and alerting:** Feed health dashboards, latency tracking (exchange-to-receipt),
volume monitoring against baselines, automated alerts for disconnections, latency spikes,
staleness, and gaps.

**Failover:** Primary/secondary feed architecture with automatic failover on disconnection,
excessive latency, or quality breach. Downstream systems must handle graceful degradation
(e.g., losing Level 3 depth when failing from direct feed to SIP).

| Metric | Target |
|---|---|
| Feed uptime (trading hours) | > 99.95% |
| Median latency | < 1ms (direct), < 50ms (SIP) |
| 99th percentile latency | < 10ms (direct), < 100ms (SIP) |
| Staleness rate | < 0.1% of instruments |
| Gap rate | < 0.01% of expected messages |

## Worked Examples

Three worked scenarios (vendor selection and licensing for a mid-size RIA, SIP-plus-direct-feed architecture for an electronic trading platform, and entitlement/exchange-audit remediation with cost exposure tables) are in `references/examples.md`. Load that file when designing a concrete market data stack, comparing vendor costs, or working an entitlement compliance problem.

## Common Pitfalls

1. **Conflating SIP NBBO with direct feed best prices.** The SIP NBBO is the Reg NMS
   regulatory benchmark. A firm's internally computed NBBO from direct feeds may differ
   due to latency. For best execution compliance, the SIP NBBO is authoritative.

2. **Under-reporting exchange subscribers.** Estimating rather than counting professional
   users and non-display applications risks material back-billing during exchange audits.

3. **Ignoring non-display use fees.** Any system consuming exchange data for automated
   purposes (algorithms, risk, pricing) typically requires a separate non-display license.

4. **Treating delayed data as free.** Vendor delivery costs and professional-user fees
   for delayed data through certain platforms still apply. Verify terms per use case.

5. **Over-subscribing to market data.** Firms accumulate unused subscriptions over time.
   Periodic usage audits identify significant cost savings.

6. **Neglecting data quality monitoring.** Consuming data without staleness, gap, and
   erroneous tick monitoring exposes the firm to silent failures. VaR computed on stale
   prices is dangerously misleading.

7. **Failing to plan for peak data rates.** Volumes spike during market events. Size
   infrastructure for 2-3x typical peak volumes to avoid failures when data matters most.

8. **Ignoring survivorship bias in historical data.** Use point-in-time, survivorship-free
   databases for strategy research to avoid inflated backtest returns.

9. **Distributing raw exchange data without redistribution licenses.** Client-facing
   real-time quotes require explicit redistribution agreements. Violations risk license
   termination and legal liability.

## Cross-References

- **reference-data** (data-integration plugin) — Security master and symbology underpin market data
  infrastructure; market data systems rely on reference data for symbol mapping and
  corporate action processing.
- **exchange-connectivity** (trading-operations plugin) — Physical and logical exchange connections over
  which market data feeds travel; covers co-location and protocol handling.
- **trade-execution** (trading-operations plugin) — Smart order routers and execution algorithms consume
  Level 2/3 market data for routing decisions and execution pacing.
- **portfolio-management-systems** (advisory-practice plugin) — PMS platforms consume market data for
  position valuation, drift monitoring, and rebalancing triggers.
- **performance-metrics** (wealth-management plugin) — EOD pricing feeds provide closing prices for daily
  return calculations; data quality directly affects computed metrics.
- **volatility-modeling** (wealth-management plugin) — Implied volatility derived from OPRA options data;
  GARCH/EWMA models calibrated on historical price series from market data infrastructure.
- **equities** (wealth-management plugin) — Equity market structure and instruments; this skill covers the
  data infrastructure delivering equity market information to consuming systems.
