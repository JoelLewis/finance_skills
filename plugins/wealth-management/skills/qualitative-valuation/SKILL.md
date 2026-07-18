---
name: qualitative-valuation
description: "Assess business quality, competitive positioning, and sustainability of value creation beyond financial models. Use when the user asks about economic moats, competitive advantages, Porter's Five Forces, management quality, ESG integration, or business model analysis. Also trigger when users mention 'does this company have a moat', 'switching costs', 'network effects', 'brand value', 'management track record', 'capital allocation', 'insider ownership', 'red flags', or ask whether a company's advantage is durable."
---

# Qualitative Valuation

## Core Concepts

### Economic Moats (Morningstar Framework)
An economic moat is a structural advantage that protects a company's profits from competition. Five sources:

1. **Network Effects:** the product becomes more valuable as more people use it (payment networks, marketplaces)
2. **Switching Costs:** customers face significant cost, effort, or risk in moving to a competitor (enterprise software, banking relationships)
3. **Intangible Assets:** brands, patents, licenses, or regulatory approvals competitors cannot replicate; brands must confer pricing power to qualify
4. **Cost Advantages:** structural cost advantages from process technology, scale, location, or unique resources
5. **Efficient Scale:** a market that supports only a few players, where new entry would drive returns below the cost of capital (utilities, pipelines, railroads)

### Moat Width
- **Wide moat (20+ years):** multiple reinforcing moat sources, each backed by hard evidence
- **Narrow moat (10+ years):** at least one evidenced moat source with moderate durability
- **No moat:** commodity business with no structural advantage; competes on price

A moat claim is only as strong as its evidence. Do not award moat sources based on narrative — use the rubric below.

### Evidence Rubric: What Qualifies a Qualitative Claim
Anchor every claim in observable results, with retention and realized pricing as the strongest evidence:

| Claim | Qualifying evidence | Disqualifying signs |
|-------|--------------------|---------------------|
| Pricing power | Realized price increases at or above inflation with stable volumes and retention; gross margin held or expanded through input-cost cycles | Price increases followed by churn spikes; persistent discounting to hold share |
| Switching costs | Gross retention >90% (>95% for enterprise) or net revenue retention >100%; multi-year contracts; implementations measured in quarters; deep data/workflow integration | High churn; month-to-month terms; easy data export and low migration cost |
| Network effects | Unit economics measurably improve with scale (take rates, engagement, liquidity per user); winner-take-most share dynamics | User growth without any engagement, pricing, or cost benefit |
| Brand (intangible asset) | Sustained price premium over comparable products for years | Awareness without a premium; growth dependent on promotional spend |
| Cost advantage | Margins persistently above peers, traceable to scale, process, or resource access | One-off cost cuts; margin gap explained by product mix |
| Management quality | Multi-year ROIC > WACC; buybacks executed below subsequent intrinsic value; acquisitions that met stated return targets | Serial dilutive M&A; buybacks concentrated at price peaks; recurring guidance misses |

### Mapping Findings to Valuation Inputs
Translate qualitative conclusions into explicit adjustments to discount rate, fade period, or terminal assumptions in quantitative valuation. These ranges are judgment calibrations, not formulas — document the specific evidence behind each adjustment:

| Finding | Calibrated adjustment |
|---------|----------------------|
| Wide-moat evidence (2+ reinforcing, retention-backed sources) | Discount rate -0.5 to -1.0pp, or terminal multiple +1-2 turns, or extend the above-WACC return fade to 15-20 years |
| Narrow moat (one evidenced source) | Fade above-WACC returns over ~10 years; no discount-rate change |
| No moat | Fade returns to WACC by terminal year; terminal growth at or below inflation |
| Confirmed pricing power | Hold or modestly expand forecast margins; resist mean-reverting them prematurely |
| Governance red flags (see checklist) | Discount rate +0.5 to +1.5pp, haircut management guidance, or walk away |
| Material unmitigated ESG/regulatory exposure | Discount rate +0.5 to +1.5pp, or (often more transparent) probability-weight an impaired-earnings scenario |
| Key-person or succession risk | Discount rate +0.25 to +0.75pp |

If combined adjustments exceed roughly 2pp on the discount rate in either direction, the qualitative overlay is driving the valuation — re-examine the base-case cash flow assumptions instead of stacking adjustments.

### Qualitative Red Flags Checklist
Any single flag warrants deeper investigation before relying on a valuation model:

- **Aggressive accounting:** revenue recognition changes, newly capitalized expenses, non-GAAP adjustments that always exceed GAAP. Check: trend in the non-GAAP-to-GAAP gap over 3+ years.
- **Related-party transactions:** deals with insider-controlled entities that may not be at arm's length. Check: proxy statement and footnote disclosures.
- **Excessive M&A:** serial acquisitions that obscure weak organic growth and add integration risk. Check: organic growth disclosed vs reported growth.
- **High management turnover:** frequent CFO or auditor changes signal potential problems. Check: 8-K filings for departures and stated reasons.
- **Divergent cash flow and earnings:** net income growing while operating cash flow stagnates. Check: accruals (net income minus OCF) as a share of assets over time.

## Worked Examples

### Example 1: Moat Assessment — Enterprise Software Company
**Given:**
- Cloud-based ERP platform with 95% gross retention, 120% net revenue retention
- Average customer implementation takes 12-18 months
- Data integration with customer systems creates deep embedding
- No network effects; moderate brand value; costs in line with peers

**Assess:** Moat sources and width, using the evidence rubric

**Solution:**

1. **Switching Costs — STRONG (qualifies):** 95% gross retention and 120% net revenue retention clear the rubric thresholds, and 12-18 month implementations with deep data integration explain why. The 120% net retention also evidences realized pricing power: existing customers are paying more each year without offsetting churn.
2. **Network Effects — ABSENT:** an ERP system does not become more valuable to one customer because another adopts it.
3. **Intangible Assets — DOES NOT QUALIFY:** the brand is recognized but confers no measurable price premium over peers.
4. **Cost Advantages — ABSENT:** cost structure in line with competitors.
5. **Efficient Scale — ABSENT:** the market supports multiple competitors.

Assessment: **Narrow-to-wide moat.** One moat source, but with unusually strong retention evidence; durability 15-20+ years barring a technology shift. Valuation-input mapping: extend the above-WACC return fade toward 15-20 years and hold forecast margins, but skip the full wide-moat discount-rate reduction because there is no second reinforcing source.

### Example 2: Governance and Regulatory Risk — Discount Rate Calibration
**Given:** Base cost of equity 9.0%. The company operates in a high-carbon industry with no transition plan; pending carbon-tax legislation could reduce EBIT by 15%. Governance is strong: independent board, aligned compensation, no red flags.

**Calibrate:** Adjusted cost of equity

**Solution:**
- Unmitigated regulatory/environmental exposure: +1.5pp (top of the +0.5 to +1.5pp range — exposure is material, unmitigated, and legislation is pending)
- Strong governance: -0.25pp partial offset (well-governed firms adapt better)

Adjusted cost of equity = 9.0% + 1.5% - 0.25% = **10.25%**

Alternative (often more transparent): keep the 9% discount rate and probability-weight a scenario in which EBIT falls 15% when the carbon tax passes. Both approaches capture the same risk; do not apply both at once.

## Common Pitfalls
- Narrative fallacy: a compelling story is not evidence — require the rubric's observable results before crediting a moat
- Confirmation bias: seeking information that supports a pre-existing thesis while dismissing contradictory evidence
- Moat erosion: technology disruption can destroy moats faster than historical patterns suggest (e.g., retail disrupted by e-commerce)
- Double-counting: adjusting the discount rate and the cash flows for the same risk overstates the impact
- Overweighting management charisma: a compelling CEO presentation does not equal good capital allocation — check the multi-year ROIC and M&A record
- Static analysis: moats, competitive positioning, and regulatory risks evolve — reassess periodically

## Cross-References
- **quantitative-valuation** (wealth-management plugin): quantitative models that qualitative analysis informs and contextualizes
- **financial-statements** (wealth-management plugin): ROIC, margins, and cash flow patterns that validate qualitative assessments
- **forward-risk** (wealth-management plugin): risk premium adjustments from ESG and business quality factors
- **diversification** (wealth-management plugin): qualitative sector/factor analysis informs diversification decisions
