---
name: tax-efficiency
description: "Maximizes after-tax returns through strategic asset location, gain/loss management, and withdrawal sequencing. Use when the user asks about asset location, Roth conversions, tax-efficient withdrawals, tax lot selection, or charitable giving with appreciated securities. Also trigger when users mention 'which account should I hold bonds in', 'tax drag', 'Roth vs Traditional', 'RMD planning', 'bracket stuffing', 'HIFO vs FIFO', or ask how to minimize taxes on investments. For tax-loss harvesting execution and wash-sale mechanics, see the tax-loss-harvesting skill."
---

# Tax-Efficient Investing

## Core Concepts

### Asset Location
Place tax-inefficient assets in tax-advantaged accounts and tax-efficient assets in taxable accounts:

- **Tax-deferred accounts (Traditional IRA, 401k):** Bonds, REITs, high-turnover funds, TIPS — assets generating ordinary income
- **Tax-exempt accounts (Roth IRA, Roth 401k):** Highest expected growth assets — all growth is permanently tax-free
- **Taxable accounts:** Index equity funds (low turnover, qualified dividends, tax-loss harvesting eligible), municipal bonds, tax-managed funds

The benefit of asset location increases with the spread between ordinary income tax rates and capital gains rates, and with the size of the tax-advantaged accounts relative to total portfolio.

### Tax-Loss Harvesting (TLH)
Realize investment losses to offset capital gains, reducing current tax liability while maintaining market exposure:

- Sell a losing position, immediately buy a similar (but not "substantially identical") replacement
- Harvested losses offset gains dollar-for-dollar; net losses offset up to $3,000 of ordinary income per year; excess carries forward indefinitely
- **Wash-sale rule (61-day window):** Cannot repurchase the same or substantially identical security within the 61-day window (30 days before + sale date + 30 days after) — applies across all accounts (including spouse's accounts and IRAs)
- **Tax alpha from TLH:** Estimated 0.5-1.5% per year in early years of a portfolio's life, declining as cost basis rises
- Best opportunities arise during market volatility and in the first few years of investing

### After-Tax Return
Different income types face different tax rates:

- **Interest income:** Taxed at ordinary income rates
- **Qualified dividends:** Taxed at long-term capital gains rates (0%, 15%, or 20% + 3.8% NIIT)
- **Short-term capital gains (held ≤ 1 year):** Ordinary income rates
- **Long-term capital gains (held > 1 year):** Preferential rates (0%, 15%, or 20% + 3.8% NIIT)
- The 3.8% NIIT applies above $250,000 MAGI (MFJ) — a statutory threshold that is not inflation-indexed
- After-tax return on income: R_at = R × (1 - t)
- Capital gains are taxed only at realization, providing a deferral benefit

### Tax Drag
The annual cost of taxes on investment returns:

- Tax drag = pre-tax return - after-tax return
- High-turnover funds generate more short-term gains → higher tax drag
- Index funds with low turnover minimize tax drag
- ETFs generally more tax-efficient than mutual funds (in-kind creation/redemption process)

### Tax Lot Management
When selling partial positions, the method of selecting which lots to sell affects tax liability:

- **Specific identification:** Choose exactly which lots to sell
- **HIFO (Highest In, First Out):** Sell highest-cost-basis lots first to minimize gains
- **FIFO (First In, First Out):** Default method; may realize larger gains on older lots
- **Tax-optimal:** Select lots to minimize current-year tax liability considering holding period and gains/losses

### Roth Conversion
Convert Traditional IRA/401k assets to Roth, paying ordinary income tax now for tax-free growth and withdrawals later:

- **Breakeven analysis:** Conversion is beneficial if current marginal tax rate < expected future marginal tax rate
- **Factors favoring conversion:** Long time horizon, low current income year, expectation of higher future rates, desire to reduce future RMDs, estate planning benefits
- **Partial conversions:** Convert just enough to fill current tax bracket ("bracket stuffing")
- Tax on conversion: conversion amount × current marginal rate

### Required Minimum Distributions (RMDs)
Mandatory annual withdrawals from tax-deferred accounts (Traditional IRA, 401k) beginning at age 73 (under SECURE 2.0, rising to 75 in 2033):

- RMD = account balance (Dec 31 prior year) / distribution period (from IRS Uniform Lifetime Table)
- Failure penalty: 25% excise tax on shortfall (reduced from prior 50%)
- RMDs are taxed as ordinary income and can push retirees into higher brackets
- Roth IRAs have no RMDs during the owner's lifetime

### Withdrawal Sequencing
The order of withdrawals from different account types in retirement:

- **General rule:** Taxable → Tax-deferred → Roth (preserves tax-free growth longest)
- **Optimized approach:** Withdraw from taxable first, then fill low tax brackets with tax-deferred withdrawals, use Roth to avoid bracket jumps
- **Dynamic strategy:** Adjust each year based on income, deductions, and bracket thresholds

### Charitable Giving Strategies
- **Donate appreciated stock:** Avoid capital gains tax and deduct full fair market value (must be held > 1 year)
- **Qualified Charitable Distributions (QCDs):** Donate up to $111,000/year (2026 limit, indexed annually) directly from IRA to charity (counts toward RMD, excluded from taxable income); available at age 70½+
- **Donor-Advised Funds (DAFs):** Bunch multiple years of donations for itemized deduction, invest tax-free, distribute to charities over time

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| After-tax return (income) | R_at = R × (1 - t) | Bond/interest income after tax |
| After-tax return (deferred gains) | R_at = ((1 + R)^n × (1 - t_cg) + t_cg)^(1/n) - 1 | Unrealized equity with deferral benefit |
| Tax-loss harvesting value | TLH_value = loss × marginal_tax_rate | Immediate tax benefit of harvesting |
| Roth conversion breakeven | t_now < t_future | Convert when current rate < future rate |
| RMD amount | RMD = balance_Dec31 / distribution_period | Required minimum distribution |
| Appreciated-stock donation benefit | Tax saved = FMV × t_income + gain × t_cg_avoided | Tax benefit of donating appreciated stock (deduction + avoided gains tax) |

## Worked Examples

### Example 1: Asset location optimization
**Given:** $500K in taxable brokerage + $500K in Traditional IRA. Portfolio target: 50% bonds (yielding 5%) and 50% equities (expected 10% total return, 2% qualified dividends). Marginal tax rate: 32% ordinary, 15% LTCG.
**Calculate:** Optimal asset placement and annual tax savings vs naive allocation.
**Solution:**
1. **Optimal placement:** Bonds ($500K) in IRA; Equities ($500K) in taxable.
2. **Naive placement (50/50 each):** Taxable has $250K bonds + $250K equities; IRA has $250K bonds + $250K equities.
3. **Tax drag — naive:** Taxable bonds: $250K × 5% × 32% = $4,000. Taxable equity dividends: $250K × 2% × 15% = $750. Total tax = $4,750.
4. **Tax drag — optimal:** Taxable equity dividends only: $500K × 2% × 15% = $1,500. Total tax = $1,500.
5. **Annual tax savings:** $4,750 - $1,500 = **$3,250/year** (0.325% of total portfolio).
6. Over 20 years compounded, this adds significantly to after-tax wealth.

### Example 2: Roth conversion breakeven
**Given:** Consider converting $50,000 from Traditional IRA to Roth. Current marginal tax rate: 24%. Tax on conversion paid from outside funds. Investment horizon: 20 years. Expected return: 7%.
**Simplifying assumption:** Assume the $12,000, if not used for conversion tax, would grow at the same 7% with no tax drag — i.e., side-fund growth itself is untaxed.
**Calculate:** Future marginal tax rate at which conversion breaks even.
**Solution:**
1. **Cost of conversion now:** $50,000 × 24% = $12,000 tax paid today.
2. **Traditional IRA path:** $50,000 grows to $50,000 × (1.07)^20 = $193,484. After-tax at withdrawal: $193,484 × (1 - t_future).
3. **Roth path:** $50,000 grows to $193,484 tax-free, but the $12,000 side fund forgoes growth to $12,000 × (1.07)^20 = $46,436. Roth net value: $193,484 - $46,436 = $147,048.
4. **Breakeven:** Set Traditional after-tax = Roth net value. $193,484 × (1 - t_future) = $193,484 - $46,436 → t_future = $46,436 / $193,484 = **24.0%**.
5. **Conclusion:** Under this simplification the breakeven future rate equals the current rate (24%) — both sides scale by the same (1.07)^20, so the horizon and return cancel. In reality the taxable side fund suffers tax drag on its dividends and realized gains, so paying conversion tax from outside funds tilts the comparison toward Roth even when the future rate merely equals the current rate.

## Common Pitfalls
- TLH wash sale violations, including purchases in other accounts, IRAs, or a spouse's account within the 61-day wash-sale window (30 days before through 30 days after the sale)
- Over-harvesting losses that defer gains to higher tax brackets later (basis step-down compounds)
- Not considering state taxes in asset location decisions — state tax treatment varies significantly
- Ignoring the tax benefit of donating appreciated securities vs cash (avoids capital gains and gets full deduction)
- RMD-driven forced selling at inopportune times — plan withdrawals ahead of deadlines
- Roth converting too aggressively and pushing into a higher bracket in the conversion year
- Forgetting the 3.8% Net Investment Income Tax (NIIT) above $250,000 MAGI (MFJ) — a statutory threshold that is not inflation-indexed, so it captures more taxpayers each year
- Not coordinating tax strategy across spouses' accounts

## Cross-References
- **investment-policy** (wealth-management plugin): Tax constraint in IPS governs asset location and turnover management
- **performance-attribution** (wealth-management plugin): After-tax return attribution requires tax-aware calculations
- **debt-management** (wealth-management plugin): Mortgage interest deductibility interacts with tax planning
- **savings-goals** (wealth-management plugin): Account type selection (Roth vs Traditional) is a core tax decision
- **liquidity-management** (wealth-management plugin): Tax implications of accessing different account types affect liquidity planning
- **tax-loss-harvesting** (wealth-management plugin): dedicated TLH workflow skill with detailed candidate identification, wash-sale tracking, and execution planning
- **financial-planning-workflow** (advisory-practice plugin): tax-aware strategies are core recommendations in comprehensive financial plans

## Running the script
Run with `uv run scripts/tax_efficiency.py` (the PEP 723 header resolves dependencies automatically) or with `python3 scripts/tax_efficiency.py` after `pip install numpy scipy`. The bare run prints a demo covering after-tax returns, tax drag, TLH benefit, asset location placement, and Roth conversion breakeven. Pass `--verify` to assert the demo outputs match this skill's worked examples (prints PASS/FAIL), or `--help` for an overview of the available classes. The file is primarily meant to be imported as a module (e.g., `from tax_efficiency import AfterTaxReturn, AssetLocation, BreakevenAnalysis`).
