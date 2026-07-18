---
name: fixed-income-municipal
description: "Analyze municipal bonds including tax-equivalent yield calculations, GO vs revenue bond evaluation, and muni credit analysis. Use when the user asks about municipal bonds, tax-exempt income, tax-equivalent yield, AMT bonds, callable bonds, yield-to-worst on munis, or muni credit quality. Also trigger when users mention 'muni bonds', 'tax-free bonds', 'state tax exemption', 'general obligation', 'revenue bonds', 'Build America Bonds', 'muni yield ratio', 'de minimis rule', or ask whether munis make sense for their tax bracket."
---

# Fixed Income — Municipal

## Core Concepts

### General Obligation (GO) Bonds
Backed by the full faith, credit, and taxing power of the issuing municipality. The issuer pledges to use any available revenue source (property tax, income tax, sales tax) to repay bondholders. GO bonds typically require voter approval and are considered safer due to the broad taxing pledge.

### Revenue Bonds
Backed solely by the revenue generated from a specific project or source — toll roads (toll collections), water/sewer systems (utility fees), hospitals (patient revenue), airports (landing fees, terminal rents). Revenue bonds typically carry higher yields than GO bonds of comparable maturity and credit quality because of the narrower revenue pledge.

### Tax-Equivalent Yield (TEY)
The core calculation for comparing municipal bonds to taxable alternatives:

Federal only: TEY = Muni Yield / (1 - federal_marginal_rate)

Federal + state (for in-state munis): TEY = Muni Yield / (1 - federal_rate - state_rate × (1 - federal_rate))

This converts a tax-exempt yield to the pre-tax yield a taxable bond would need to offer to match the muni's after-tax income.

Note: the state_rate × (1 - federal_rate) term assumes state income tax is fully deductible against federal tax. For taxpayers at or above the SALT deduction cap (or taking the standard deduction), state tax provides no incremental federal deduction, and the formula simplifies to TEY = Muni Yield / (1 - federal_rate - state_rate) — the combined formula above understates the in-state muni's advantage for capped itemizers and overstates the precision of the comparison generally. Check the client's actual SALT position before choosing the formula.

### Alternative Minimum Tax (AMT)
Certain private activity bonds generate interest that is subject to AMT. For taxpayers subject to AMT, the tax advantage of these bonds is reduced. AMT-subject bonds typically trade at slightly higher yields to compensate. Non-AMT munis (governmental purpose bonds) are not affected.

### Muni Credit Analysis
**GO bonds:** evaluate tax base diversity and trends, debt burden ratios (debt per capita, debt/assessed value), fund balance as % of expenditures, economic base (population, employment), pension/OPEB obligations.

**Revenue bonds:** evaluate debt service coverage ratio (DSCR = net revenue / annual debt service), rate covenants, additional bonds tests, demand analysis, and reserve fund adequacy.

### De Minimis Tax Rule
Discount bonds purchased below a threshold (typically par minus 0.25% per year to maturity) may lose tax-exempt status on the discount portion — the gain is taxed as ordinary income rather than being tax-exempt. This affects the after-tax return calculation for discount munis.

### Muni Yield Ratios
Muni yield / Treasury yield. Historically this ratio averages approximately 80% for AAA munis. Ratios above 80-85% suggest munis are cheap relative to Treasuries; below 70% suggests they are rich. The ratio varies with supply/demand, tax policy expectations, and credit conditions.

### Build America Bonds (BABs)
Taxable municipal bonds created under the 2009 stimulus. The federal government subsidizes 35% of interest cost. Expired for new issuance after 2010 but outstanding BABs continue to trade. They allowed issuers to access the broader taxable bond market.

### Pre-Refunded/Escrowed Bonds
When an issuer advance-refunds a callable bond, it places US Treasuries in escrow sufficient to pay remaining coupons and the call price. These defeased bonds are effectively AAA-quality and trade at very tight spreads.

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| TEY (federal only) | Muni Yield / (1 - federal_rate) | Compare muni to taxable bond |
| TEY (federal + state) | Muni Yield / (1 - fed_rate - state_rate × (1 - fed_rate)) | In-state muni comparison |
| DSCR | Net Revenue / Annual Debt Service | Revenue bond credit quality |
| De Minimis Threshold | Par - 0.25% × years to maturity | Tax treatment of discount munis |
| Muni Yield Ratio | Muni Yield / Treasury Yield | Relative value assessment |

## Worked Examples

### Example 1: Tax-Equivalent Yield with Federal and State Tax
**Given:** Muni yield = 3.5%, federal marginal rate = 37%, state marginal rate = 5%
**Calculate:** Tax-equivalent yield for an in-state bond
**Solution:**
TEY = 3.5% / (1 - 0.37 - 0.05 × (1 - 0.37))
TEY = 3.5% / (1 - 0.37 - 0.05 × 0.63)
TEY = 3.5% / (1 - 0.37 - 0.0315)
TEY = 3.5% / 0.5985
TEY = 5.85%

A taxable bond would need to yield 5.85% to match the after-tax income of this 3.5% muni for this taxpayer. The state tax benefit adds approximately 29bp of value compared to the federal-only TEY of 5.56%.

### Example 2: GO vs Revenue Bond Comparison
**Given:** Same issuer, same maturity (10 years). GO bond yields 3.2%, revenue bond (water/sewer) yields 3.6%. DSCR on revenue bond = 1.8x.
**Calculate:** Which bond offers better value?
**Solution:**
The revenue bond yields 40bp more than the GO bond. The DSCR of 1.8x is well above the typical 1.25x minimum for investment grade, indicating strong coverage. Water/sewer is an essential service with stable demand. The 40bp additional yield compensates for the narrower revenue pledge, but the strong coverage ratio suggests the credit risk is modest. For investors comfortable with revenue bond structures, the 40bp pickup may represent good relative value.

## Common Pitfalls
- Forgetting state tax benefits for in-state bonds — the combined federal+state TEY can be meaningfully higher than federal-only
- AMT implications for high-income investors — private activity bond interest may trigger AMT liability
- De minimis rule on discount munis — gains on deep-discount munis may be taxed as ordinary income
- Confusing call provisions — many munis are callable at par after 10 years; always check yield-to-worst

## Cross-References
- **time-value-of-money** (core plugin): present value and discounting fundamentals
- **fixed-income-sovereign** (wealth-management plugin): yield curve context and duration concepts
- **fixed-income-corporate** (wealth-management plugin): comparing muni spreads to corporate spreads
- **tax-efficiency** (wealth-management plugin): muni bonds as a primary tax management tool

## Running the Script

```bash
uv run scripts/fixed_income_municipal.py            # run the demo (uses PEP 723 inline deps)
uv run scripts/fixed_income_municipal.py --verify   # check demo outputs against the worked examples (exit 1 on mismatch)
python3 scripts/fixed_income_municipal.py            # alternative (requires: pip install numpy)
```

The demo prints the calculations covered above; its values match the worked examples in this skill. Run `--help` for a list of the classes and functions. For programmatic use, import the module rather than running it — the demo only executes under `python fixed_income_municipal.py`.
