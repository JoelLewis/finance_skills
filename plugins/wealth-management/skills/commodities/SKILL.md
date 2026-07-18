---
name: commodities
description: "Analyze commodity markets including futures curve dynamics, roll yield, and supply/demand fundamentals. Use when the user asks about commodity investing, commodity ETFs, contango, backwardation, roll yield, commodity indices (GSCI, BCOM), or commodities as an inflation hedge. Also trigger when users mention 'oil prices', 'gold as a safe haven', 'agricultural futures', 'convenience yield', 'storage costs', 'natural gas', 'copper demand', or ask why commodity ETF returns differ from spot price changes."
---

# Commodities

## Core Concepts

### Spot vs Futures Pricing
The futures price is related to the spot price through the cost-of-carry model:

F = S × e^((r + u - y) × t)

where S = spot price, r = risk-free rate, u = storage cost, y = convenience yield, t = time to expiration. The convenience yield represents the benefit of holding the physical commodity (e.g., avoiding production shutdowns).

### Contango
When F > S, the futures curve is upward-sloping. Storage costs and financing costs exceed the convenience yield. Contango creates negative roll yield because investors must sell cheaper expiring contracts and buy more expensive later contracts. Contango is common in well-supplied markets and for storable commodities like oil and natural gas.

### Backwardation
When F < S, the futures curve is downward-sloping. The convenience yield exceeds storage and financing costs, often due to near-term supply scarcity. Backwardation creates positive roll yield because investors sell expensive expiring contracts and buy cheaper later contracts. Backwardation is common in tight supply environments.

### Sources of Commodity Return
Total commodity return has three components:

1. **Spot return:** Change in the spot price of the commodity
2. **Roll yield:** Gain or loss from rolling expiring futures into the next contract
3. **Collateral yield:** Interest earned on the margin/collateral posted to hold futures positions

Total Return = Spot Return + Roll Yield + Collateral Yield

### Roll Yield
The gain or loss realized when an expiring futures contract is replaced by a longer-dated contract. In contango (upward curve), roll yield is negative. In backwardation (downward curve), roll yield is positive. Roll yield can be a significant drag or boost to total returns — in deep contango, roll yield can eliminate or even exceed spot price gains.

### Commodity Sectors
- **Energy:** crude oil, natural gas, gasoline, heating oil — largest sector by production value
- **Precious metals:** gold, silver, platinum, palladium — safe haven and industrial uses
- **Industrial metals:** copper, aluminum, zinc, nickel — tied to global economic activity
- **Agriculture:** corn, wheat, soybeans, coffee, sugar, cotton — weather and harvest dependent
- **Livestock:** live cattle, lean hogs — demand-driven

### Commodity Indices
- **S&P GSCI:** production-weighted, heavily tilted toward energy (~60%+ as of 2024-2025; weights are rebalanced annually, so check the current composition). Represents global commodity production.
- **Bloomberg Commodity Index (BCOM):** diversified with sector caps (33%) and single commodity caps (15%). More balanced exposure.
- Index construction affects returns significantly — energy-heavy indices behave very differently from diversified indices.

### Inflation Hedge Properties
Commodities tend to correlate positively with unexpected inflation, making them a potential hedge. The mechanism is direct: rising commodity prices are a component of inflation. However, the hedge is imperfect and works better for supply-driven inflation than demand-driven or monetary inflation.

### Seasonality
Agricultural commodities show harvest-related patterns (supply increases at harvest, depressing prices). Energy shows heating/cooling demand patterns (natural gas peaks in winter, gasoline in summer driving season). Seasonality is well-known and partially priced in, but seasonal patterns can still affect futures curve shape.

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| Cost of Carry | F = S × e^((r+u-y)×t) | Theoretical futures price |
| Roll Yield (approx) | (F_near - F_far) / F_near | Return from contract rolling |
| Total Return | Spot Return + Roll Yield + Collateral Yield | Complete commodity return |
| Annualized Roll Yield | ((F_near/F_far)^(365/days_between) - 1) | Annualized roll impact |
| Convenience Yield | y = r + u - (1/t) × ln(F/S) | Implied convenience yield |

## Worked Examples

### Example 1: Roll Yield in Contango
**Given:** Front month crude oil futures at $50, next month at $52 (contango), 1-month roll period
**Calculate:** Annualized roll yield
**Solution:**
Monthly roll yield = (F_near - F_far) / F_near = ($50 - $52) / $50 = -4.0%
This is a 1-month loss of 4.0%.
Annualized roll yield ≈ -4.0% × 12 = -48% (simple annualization)
Compounded over 12 monthly rolls: (50/52)^12 - 1 = (0.9615)^12 - 1 = -37.5%
Using the day-count formula above with a 30-day roll: (50/52)^(365/30) - 1 = -37.9%

This illustrates how severe contango can create enormous roll yield drag. In practice, front-to-second-month contango is rarely this steep, but the example shows why curve shape matters enormously for commodity investors.

### Example 2: Total Return Decomposition for a Commodity ETF
**Given:** Over one year, spot crude oil rises from $70 to $77 (+10%). Roll yield = -6%. Collateral yield (T-bill rate) = 5%.
**Calculate:** Total return of a futures-based commodity ETF
**Solution:**
Total Return = Spot Return + Roll Yield + Collateral Yield
Total Return = 10% + (-6%) + 5% = 9%

Despite a 10% spot price increase, the futures-based investor earned only 9% due to 6% roll yield drag, partially offset by 5% collateral yield. A physical holder (no roll cost, no collateral yield) would have earned 10%.

## Common Pitfalls
- Confusing spot returns with futures-based returns — most investors access commodities through futures, where roll yield matters
- Ignoring roll yield drag in contango markets — contango can erode returns substantially over time
- Commodity ETFs track futures, not spot prices — ETF returns can diverge significantly from spot price movements
- Storage costs matter for physical but not financial investors — financial investors face roll yield, not storage costs

## Cross-References
- **historical-risk** (wealth-management plugin): return and risk measurement basics
- **real-assets** (wealth-management plugin): physical and collectible commodity ownership (bullion, farmland, timberland). Division of labor: this skill owns gold accessed via futures and the gold-as-safe-haven allocation question; real-assets owns physical/collectible gold ownership and storage
- **currencies-and-fx** (wealth-management plugin): commodity currency relationships
- **asset-allocation** (wealth-management plugin): commodities as a portfolio diversifier

## Running the Script

```bash
uv run scripts/commodities.py            # run the demo (uses PEP 723 inline deps)
uv run scripts/commodities.py --verify   # check demo outputs against the worked examples (exit 1 on mismatch)
python3 scripts/commodities.py            # alternative (requires: pip install numpy)
```

The demo prints the calculations covered above; its values match the worked examples in this skill. Run `--help` for a list of the classes and functions. For programmatic use, import the module rather than running it — the demo only executes under `python commodities.py`.
