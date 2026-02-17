---
name: tax-efficiency
description: "Tax-aware investing: asset location, tax-loss harvesting, gain/loss management, tax-efficient withdrawal sequencing."
allowed-tools: ["Bash", "Read", "Write", "Edit"]
---

# Tax-Efficient Investing

## Purpose
Maximize after-tax returns through strategic asset location, tax-loss harvesting, gain/loss management, and withdrawal sequencing. This skill addresses both the accumulation phase (minimizing tax drag) and the distribution phase (optimizing withdrawal order across account types).

## Layer
5 — Policy & Planning

## Direction
both

## When to Use
- Deciding which assets to hold in taxable vs tax-deferred vs tax-exempt (Roth) accounts
- Evaluating tax-loss harvesting opportunities and managing wash-sale compliance
- Computing after-tax returns and tax drag on portfolio performance
- Planning Roth conversion strategies and breakeven analysis
- Designing tax-efficient withdrawal sequences in retirement
- Evaluating charitable giving strategies with appreciated securities
- Managing tax lot selection to minimize realized gains
- Planning around Required Minimum Distributions (RMDs)

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
- **Wash-sale rule (30 days):** Cannot repurchase the same or substantially identical security within 30 days before or after the sale — applies across all accounts (including spouse's accounts and IRAs)
- **Tax alpha from TLH:** Estimated 0.5-1.5% per year in early years of a portfolio's life, declining as cost basis rises
- Best opportunities arise during market volatility and in the first few years of investing

### After-Tax Return
Different income types face different tax rates:

- **Interest income:** Taxed at ordinary income rates
- **Qualified dividends:** Taxed at long-term capital gains rates (0%, 15%, or 20% + 3.8% NIIT)
- **Short-term capital gains (held ≤ 1 year):** Ordinary income rates
- **Long-term capital gains (held > 1 year):** Preferential rates (0%, 15%, or 20% + 3.8% NIIT)
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
Mandatory annual withdrawals from tax-deferred accounts (Traditional IRA, 401k) beginning at age 73 (under SECURE 2.0):

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
- **Qualified Charitable Distributions (QCDs):** Donate up to $105,000/year directly from IRA to charity (counts toward RMD, excluded from taxable income); available at age 70½+
- **Donor-Advised Funds (DAFs):** Bunch multiple years of donations for itemized deduction, invest tax-free, distribute to charities over time

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| After-tax return (income) | R_at = R × (1 - t) | Bond/interest income after tax |
| After-tax return (deferred gains) | R_at = (1 + R)^n × (1 - t_cg) + t_cg)^(1/n) - 1 | Unrealized equity with deferral benefit |
| Tax-loss harvesting value | TLH_value = loss × marginal_tax_rate | Immediate tax benefit of harvesting |
| Roth conversion breakeven | t_now < t_future | Convert when current rate < future rate |
| RMD amount | RMD = balance_Dec31 / distribution_period | Required minimum distribution |
| Points breakeven (charitable) | Tax saved = FMV × t_income + gain × t_cg_avoided | Benefit of donating appreciated stock |

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
**Calculate:** Future marginal tax rate at which conversion breaks even.
**Solution:**
1. **Cost of conversion now:** $50,000 × 24% = $12,000 tax paid today.
2. **Traditional IRA path:** $50,000 grows to $50,000 × (1.07)^20 = $193,484. After-tax at withdrawal: $193,484 × (1 - t_future).
3. **Roth path:** $50,000 grows to $193,484 tax-free. Net cost: $193,484 - $12,000 × (1.07)^20 = $193,484 - $46,412 = $147,072 net benefit after accounting for lost growth on tax paid.
4. **Breakeven:** Set Traditional after-tax = Roth net value. $193,484 × (1 - t_future) = $193,484 - $46,412 → t_future = $46,412 / $193,484 = **24.0%**.
5. **Conclusion:** Breakeven future rate equals the current rate (24%). If the future rate exceeds 24%, the Roth conversion is beneficial. This result holds generally: conversion wins when future rate > current rate, assuming tax is paid from outside funds.

## Common Pitfalls
- TLH wash sale violations, including purchases in other accounts, IRAs, or a spouse's account within the 30-day window
- Over-harvesting losses that defer gains to higher tax brackets later (basis step-down compounds)
- Not considering state taxes in asset location decisions — state tax treatment varies significantly
- Ignoring the tax benefit of donating appreciated securities vs cash (avoids capital gains and gets full deduction)
- RMD-driven forced selling at inopportune times — plan withdrawals ahead of deadlines
- Roth converting too aggressively and pushing into a higher bracket in the conversion year
- Forgetting the 3.8% Net Investment Income Tax (NIIT) above income thresholds
- Not coordinating tax strategy across spouses' accounts

## Cross-References
- **investment-policy:** Tax constraint in IPS governs asset location and turnover management
- **performance-attribution:** After-tax return attribution requires tax-aware calculations
- **debt-management:** Mortgage interest deductibility interacts with tax planning
- **savings-goals:** Account type selection (Roth vs Traditional) is a core tax decision
- **liquidity-management:** Tax implications of accessing different account types affect liquidity planning

## Reference Implementation
See `scripts/tax-efficiency.py` for computational helpers.
