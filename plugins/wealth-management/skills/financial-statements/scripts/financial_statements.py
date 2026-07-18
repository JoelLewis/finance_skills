# /// script
# dependencies = ["numpy"]
# requires-python = ">=3.11"
# ///
"""
Financial Statements
====================
EBITDA and free cash flow derivation (FCFF/FCFE), ROIC and invested capital,
margin analysis and DuPont decomposition, earnings-quality metrics (accruals
ratio, cash conversion cycle), and embedded-tax / cost-basis helpers for
tax-aware rebalancing.

Reference implementation for the financial-statements skill.
"""

import argparse
import math
import sys

import numpy as np

DAYS_PER_YEAR: float = 365.0


class FreeCashFlow:
    """EBITDA and free cash flow (FCFF/FCFE) derivation from the statements."""

    @staticmethod
    def ebitda(ebit: float, depreciation_amortization: float) -> float:
        """EBITDA from operating profit.

        Parameters
        ----------
        ebit : float
            Earnings before interest and taxes (operating income).
        depreciation_amortization : float
            Depreciation and amortization expense for the period.

        Returns
        -------
        float
            EBITDA = EBIT + D&A.
        """
        return float(ebit + depreciation_amortization)

    @staticmethod
    def nopat(ebit: float, tax_rate: float) -> float:
        """Net operating profit after tax.

        Parameters
        ----------
        ebit : float
            Earnings before interest and taxes.
        tax_rate : float
            Marginal tax rate (decimal, e.g., 0.25).

        Returns
        -------
        float
            NOPAT = EBIT * (1 - tax_rate).
        """
        return float(ebit * (1.0 - tax_rate))

    @staticmethod
    def cfo_indirect(
        net_income: float,
        depreciation_amortization: float,
        change_in_nwc: float,
    ) -> float:
        """Cash flow from operations via the indirect method (simplified).

        Parameters
        ----------
        net_income : float
            Net income for the period.
        depreciation_amortization : float
            Non-cash D&A added back.
        change_in_nwc : float
            Increase in net working capital (positive = cash consumed).

        Returns
        -------
        float
            CFO = NI + D&A - change_in_nwc.
        """
        return float(net_income + depreciation_amortization - change_in_nwc)

    @staticmethod
    def fcff_from_cfo(
        cfo: float,
        interest_expense: float,
        tax_rate: float,
        capex: float,
    ) -> float:
        """Free cash flow to the firm starting from CFO.

        Parameters
        ----------
        cfo : float
            Cash flow from operations.
        interest_expense : float
            Interest expense for the period.
        tax_rate : float
            Marginal tax rate (decimal).
        capex : float
            Capital expenditures.

        Returns
        -------
        float
            FCFF = CFO + interest * (1 - tax_rate) - capex.
        """
        return float(cfo + interest_expense * (1.0 - tax_rate) - capex)

    @staticmethod
    def fcff_from_ebit(
        ebit: float,
        tax_rate: float,
        depreciation_amortization: float,
        change_in_nwc: float,
        capex: float,
    ) -> float:
        """Free cash flow to the firm built from the income statement.

        Parameters
        ----------
        ebit : float
            Earnings before interest and taxes (EBITDA - D&A).
        tax_rate : float
            Marginal tax rate (decimal).
        depreciation_amortization : float
            D&A added back as a non-cash charge.
        change_in_nwc : float
            Increase in net working capital (positive = cash consumed).
        capex : float
            Capital expenditures.

        Returns
        -------
        float
            FCFF = EBIT * (1 - tax_rate) + D&A - change_in_nwc - capex.
        """
        return float(
            ebit * (1.0 - tax_rate)
            + depreciation_amortization
            - change_in_nwc
            - capex
        )

    @staticmethod
    def fcfe_from_cfo(cfo: float, capex: float, net_borrowing: float) -> float:
        """Free cash flow to equity starting from CFO.

        Parameters
        ----------
        cfo : float
            Cash flow from operations.
        capex : float
            Capital expenditures.
        net_borrowing : float
            New debt issued minus debt repaid.

        Returns
        -------
        float
            FCFE = CFO - capex + net_borrowing.
        """
        return float(cfo - capex + net_borrowing)

    @staticmethod
    def fcfe_from_fcff(
        fcff: float,
        interest_expense: float,
        tax_rate: float,
        net_borrowing: float,
    ) -> float:
        """Free cash flow to equity derived from FCFF.

        Parameters
        ----------
        fcff : float
            Free cash flow to the firm.
        interest_expense : float
            Interest expense for the period.
        tax_rate : float
            Marginal tax rate (decimal).
        net_borrowing : float
            New debt issued minus debt repaid.

        Returns
        -------
        float
            FCFE = FCFF - interest * (1 - tax_rate) + net_borrowing.
        """
        return float(fcff - interest_expense * (1.0 - tax_rate) + net_borrowing)


class Profitability:
    """Margins, ROIC, and the DuPont decomposition of ROE."""

    @staticmethod
    def gross_margin(gross_profit: float, revenue: float) -> float:
        """Gross margin = gross profit / revenue (decimal)."""
        return float(gross_profit / revenue)

    @staticmethod
    def operating_margin(ebit: float, revenue: float) -> float:
        """Operating margin = EBIT / revenue (decimal)."""
        return float(ebit / revenue)

    @staticmethod
    def net_margin(net_income: float, revenue: float) -> float:
        """Net margin = net income / revenue (decimal)."""
        return float(net_income / revenue)

    @staticmethod
    def invested_capital(
        total_debt: float,
        total_equity: float,
        excess_cash: float = 0.0,
    ) -> float:
        """Invested capital from the financing side of the balance sheet.

        Parameters
        ----------
        total_debt : float
            Short-term plus long-term interest-bearing debt.
        total_equity : float
            Total shareholders' equity.
        excess_cash : float, optional
            Cash not required for operations. Default is 0.0.

        Returns
        -------
        float
            Invested capital = debt + equity - excess cash.
        """
        return float(total_debt + total_equity - excess_cash)

    @staticmethod
    def roic(nopat: float, invested_capital: float) -> float:
        """Return on invested capital.

        Parameters
        ----------
        nopat : float
            Net operating profit after tax.
        invested_capital : float
            Invested capital (debt + equity - excess cash).

        Returns
        -------
        float
            ROIC = NOPAT / invested capital (decimal).
        """
        if invested_capital <= 0:
            raise ValueError("invested_capital must be positive.")
        return float(nopat / invested_capital)

    @staticmethod
    def roic_spread(roic: float, wacc: float) -> float:
        """Value-creation spread: ROIC - WACC (positive = value creating)."""
        return float(roic - wacc)

    @staticmethod
    def dupont(
        net_income: float,
        revenue: float,
        total_assets: float,
        total_equity: float,
    ) -> tuple[float, float, float, float]:
        """Three-factor DuPont decomposition of ROE.

        Parameters
        ----------
        net_income : float
            Net income for the period.
        revenue : float
            Total revenue for the period.
        total_assets : float
            Total assets.
        total_equity : float
            Total shareholders' equity.

        Returns
        -------
        tuple[float, float, float, float]
            (net_margin, asset_turnover, equity_multiplier, roe), where
            ROE = net_margin * asset_turnover * equity_multiplier.
        """
        margin = net_income / revenue
        turnover = revenue / total_assets
        leverage = total_assets / total_equity
        roe = margin * turnover * leverage
        return (float(margin), float(turnover), float(leverage), float(roe))


class EarningsQuality:
    """Accruals ratio and cash conversion cycle diagnostics."""

    @staticmethod
    def accruals_ratio(
        net_income: float,
        cfo: float,
        avg_total_assets: float,
    ) -> float:
        """Cash-flow-based accruals ratio.

        Parameters
        ----------
        net_income : float
            Reported net income.
        cfo : float
            Cash flow from operations.
        avg_total_assets : float
            Average total assets over the period.

        Returns
        -------
        float
            (net_income - cfo) / avg_total_assets. Persistently positive
            values indicate earnings running ahead of cash (lower quality).
        """
        if avg_total_assets <= 0:
            raise ValueError("avg_total_assets must be positive.")
        return float((net_income - cfo) / avg_total_assets)

    @staticmethod
    def days_sales_outstanding(receivables: float, revenue: float) -> float:
        """DSO = receivables / revenue * 365."""
        return float(receivables / revenue * DAYS_PER_YEAR)

    @staticmethod
    def days_inventory_outstanding(inventory: float, cogs: float) -> float:
        """DIO = inventory / COGS * 365."""
        return float(inventory / cogs * DAYS_PER_YEAR)

    @staticmethod
    def days_payables_outstanding(payables: float, cogs: float) -> float:
        """DPO = payables / COGS * 365."""
        return float(payables / cogs * DAYS_PER_YEAR)

    @staticmethod
    def cash_conversion_cycle(dso: float, dio: float, dpo: float) -> float:
        """CCC = DSO + DIO - DPO (days).

        A lengthening cycle consumes cash as the business grows; a negative
        cycle means customers fund the working capital.
        """
        return float(dso + dio - dpo)


class TaxBasis:
    """Cost basis and embedded capital gains tax for tax-aware rebalancing."""

    @staticmethod
    def unrealized_gain(market_value: float, cost_basis: float) -> float:
        """Unrealized gain (or loss if negative) = market value - cost basis."""
        return float(market_value - cost_basis)

    @staticmethod
    def embedded_tax_liability(
        market_value: float,
        cost_basis: float,
        tax_rate: float,
    ) -> float:
        """Tax due if the position were sold today.

        Parameters
        ----------
        market_value : float
            Current market value of the position.
        cost_basis : float
            Tax cost basis (purchase price adjusted for reinvested
            distributions, return of capital, and wash sales).
        tax_rate : float
            Applicable capital gains rate (decimal). Top federal long-term
            rate is 0.238 (20% LTCG + 3.8% NIIT) as of 2026.

        Returns
        -------
        float
            max(gain, 0) * tax_rate. Losses produce zero liability here
            (loss harvesting is handled in the tax-efficiency skill).
        """
        gain = market_value - cost_basis
        return float(max(gain, 0.0) * tax_rate)

    @staticmethod
    def after_tax_liquidation_value(
        market_value: float,
        cost_basis: float,
        tax_rate: float,
    ) -> float:
        """Market value net of embedded tax if fully liquidated today."""
        return float(
            market_value
            - TaxBasis.embedded_tax_liability(market_value, cost_basis, tax_rate)
        )


def _demo() -> None:
    """Run the demonstration calculations (bare-run default)."""
    print("=" * 65)
    print("Financial Statements - Demo")
    print("=" * 65)

    # --- Example 1: Income statement build, EBITDA, FCFF, FCFE ---
    print("\n--- Income Statement Build ($M) ---")
    revenue, cogs, sga, dna = 500.0, 300.0, 80.0, 30.0
    interest, tax_rate = 10.0, 0.25
    gross_profit = revenue - cogs
    ebit = gross_profit - sga - dna
    ebitda = FreeCashFlow.ebitda(ebit, dna)
    pretax = ebit - interest
    net_income = pretax * (1.0 - tax_rate)
    print(f"Revenue: ${revenue:.0f}  Gross Profit: ${gross_profit:.0f} "
          f"({Profitability.gross_margin(gross_profit, revenue):.1%})")
    print(f"EBIT: ${ebit:.0f} ({Profitability.operating_margin(ebit, revenue):.1%})"
          f"  EBITDA: ${ebitda:.0f}")
    print(f"Net Income: ${net_income:.0f} "
          f"({Profitability.net_margin(net_income, revenue):.1%})")

    print("\n--- Free Cash Flow Bridges ($M) ---")
    change_nwc, capex, net_borrowing = 15.0, 35.0, 5.0
    cfo = FreeCashFlow.cfo_indirect(net_income, dna, change_nwc)
    fcff_a = FreeCashFlow.fcff_from_cfo(cfo, interest, tax_rate, capex)
    fcff_b = FreeCashFlow.fcff_from_ebit(ebit, tax_rate, dna, change_nwc, capex)
    fcfe_a = FreeCashFlow.fcfe_from_cfo(cfo, capex, net_borrowing)
    fcfe_b = FreeCashFlow.fcfe_from_fcff(fcff_a, interest, tax_rate, net_borrowing)
    print(f"CFO: ${cfo:.1f}")
    print(f"FCFF (from CFO):  ${fcff_a:.1f}")
    print(f"FCFF (from EBIT): ${fcff_b:.1f}  (routes agree)")
    print(f"FCFE (from CFO):  ${fcfe_a:.1f}")
    print(f"FCFE (from FCFF): ${fcfe_b:.1f}  (routes agree)")

    # --- Example 2: ROIC vs WACC and DuPont ---
    print("\n--- ROIC vs WACC ($M) ---")
    nopat = FreeCashFlow.nopat(ebit, tax_rate)
    ic = Profitability.invested_capital(
        total_debt=150.0, total_equity=300.0, excess_cash=50.0,
    )
    roic = Profitability.roic(nopat, ic)
    wacc = 0.09
    print(f"NOPAT: ${nopat:.1f}  Invested Capital: ${ic:.0f}")
    print(f"ROIC: {roic:.3%}  WACC: {wacc:.1%}  "
          f"Spread: {Profitability.roic_spread(roic, wacc):+.3%}")

    print("\n--- DuPont Decomposition ---")
    margin, turnover, leverage, roe = Profitability.dupont(
        net_income=60.0, revenue=500.0, total_assets=600.0, total_equity=300.0,
    )
    print(f"Net Margin: {margin:.1%}  Asset Turnover: {turnover:.4f}  "
          f"Equity Multiplier: {leverage:.1f}x")
    print(f"ROE = {margin:.1%} x {turnover:.4f} x {leverage:.1f} = {roe:.1%}")

    # --- Example 3: Earnings quality ---
    print("\n--- Accruals Ratio ---")
    acc_x = EarningsQuality.accruals_ratio(80.0, 30.0, 500.0)
    acc_y = EarningsQuality.accruals_ratio(80.0, 95.0, 500.0)
    print(f"Company X (NI $80M, CFO $30M): {acc_x:+.1%}  <- red flag")
    print(f"Company Y (NI $80M, CFO $95M): {acc_y:+.1%}  <- cash-backed")

    print("\n--- Cash Conversion Cycle ---")
    dso = EarningsQuality.days_sales_outstanding(75.0, 500.0)
    dio = EarningsQuality.days_inventory_outstanding(60.0, 300.0)
    dpo = EarningsQuality.days_payables_outstanding(45.0, 300.0)
    ccc = EarningsQuality.cash_conversion_cycle(dso, dio, dpo)
    print(f"DSO: {dso:.2f} days  DIO: {dio:.2f} days  DPO: {dpo:.2f} days")
    print(f"CCC: {ccc:.2f} days")

    # --- Embedded tax for rebalancing ---
    print("\n--- Embedded Tax (Cost Basis) ---")
    mv, basis, ltcg = 150_000.0, 100_000.0, 0.238
    gain = TaxBasis.unrealized_gain(mv, basis)
    tax = TaxBasis.embedded_tax_liability(mv, basis, ltcg)
    after_tax = TaxBasis.after_tax_liquidation_value(mv, basis, ltcg)
    print(f"Market Value: ${mv:,.0f}  Cost Basis: ${basis:,.0f}")
    print(f"Unrealized Gain: ${gain:,.0f}  Tax @ {ltcg:.1%} (as of 2026): ${tax:,.0f}")
    print(f"After-Tax Liquidation Value: ${after_tax:,.0f}")
    print(f"Tax cost of full sale: {tax / mv:.1%} of position value")

    print("\n" + "=" * 65)
    print("Demo complete.")
    print("=" * 65)


def _verify() -> None:
    """Assert demo computations against the SKILL.md worked examples."""
    checks: list[tuple[str, float, float]] = []

    # SKILL.md Example 1: EBITDA, FCFF, and FCFE
    revenue, cogs, sga, dna = 500.0, 300.0, 80.0, 30.0
    interest, tax_rate = 10.0, 0.25
    gross_profit = revenue - cogs
    ebit = gross_profit - sga - dna
    net_income = (ebit - interest) * (1.0 - tax_rate)
    cfo = FreeCashFlow.cfo_indirect(net_income, dna, change_in_nwc=15.0)
    checks.append(("Example 1 EBITDA ($M)", FreeCashFlow.ebitda(ebit, dna), 120.0))
    checks.append(("Example 1 net income ($M)", net_income, 60.0))
    checks.append((
        "Example 1 gross margin",
        Profitability.gross_margin(gross_profit, revenue), 0.40,
    ))
    checks.append((
        "Example 1 operating margin",
        Profitability.operating_margin(ebit, revenue), 0.18,
    ))
    checks.append((
        "Example 1 net margin",
        Profitability.net_margin(net_income, revenue), 0.12,
    ))
    checks.append(("Example 1 CFO ($M)", cfo, 75.0))
    checks.append((
        "Example 1 FCFF from CFO ($M)",
        FreeCashFlow.fcff_from_cfo(cfo, interest, tax_rate, capex=35.0), 47.5,
    ))
    checks.append((
        "Example 1 FCFF from EBIT ($M)",
        FreeCashFlow.fcff_from_ebit(ebit, tax_rate, dna, 15.0, 35.0), 47.5,
    ))
    checks.append((
        "Example 1 FCFE from CFO ($M)",
        FreeCashFlow.fcfe_from_cfo(cfo, capex=35.0, net_borrowing=5.0), 45.0,
    ))
    checks.append((
        "Example 1 FCFE from FCFF ($M)",
        FreeCashFlow.fcfe_from_fcff(47.5, interest, tax_rate, 5.0), 45.0,
    ))

    # SKILL.md Example 2: ROIC vs WACC and DuPont
    nopat = FreeCashFlow.nopat(ebit, tax_rate)
    ic = Profitability.invested_capital(150.0, 300.0, 50.0)
    checks.append(("Example 2 NOPAT ($M)", nopat, 67.5))
    checks.append(("Example 2 invested capital ($M)", ic, 400.0))
    checks.append(("Example 2 ROIC", Profitability.roic(nopat, ic), 0.16875))
    margin, turnover, leverage, roe = Profitability.dupont(60.0, 500.0, 600.0, 300.0)
    checks.append(("Example 2 DuPont net margin", margin, 0.12))
    checks.append(("Example 2 DuPont asset turnover", turnover, 500.0 / 600.0))
    checks.append(("Example 2 DuPont equity multiplier", leverage, 2.0))
    checks.append(("Example 2 DuPont ROE", roe, 0.20))

    # SKILL.md Example 3: Earnings quality and embedded tax
    checks.append((
        "Example 3 accruals ratio X",
        EarningsQuality.accruals_ratio(80.0, 30.0, 500.0), 0.10,
    ))
    checks.append((
        "Example 3 accruals ratio Y",
        EarningsQuality.accruals_ratio(80.0, 95.0, 500.0), -0.03,
    ))
    dso = EarningsQuality.days_sales_outstanding(75.0, 500.0)
    dio = EarningsQuality.days_inventory_outstanding(60.0, 300.0)
    dpo = EarningsQuality.days_payables_outstanding(45.0, 300.0)
    checks.append(("Example 3 DSO (days)", dso, 54.75))
    checks.append(("Example 3 DIO (days)", dio, 73.0))
    checks.append(("Example 3 DPO (days)", dpo, 54.75))
    checks.append((
        "Example 3 CCC (days)",
        EarningsQuality.cash_conversion_cycle(dso, dio, dpo), 73.0,
    ))
    checks.append((
        "Example 3 embedded tax ($)",
        TaxBasis.embedded_tax_liability(150_000.0, 100_000.0, 0.238), 11_900.0,
    ))
    checks.append((
        "Example 3 after-tax value ($)",
        TaxBasis.after_tax_liquidation_value(150_000.0, 100_000.0, 0.238),
        138_100.0,
    ))

    failures = 0
    for name, got, expected in checks:
        ok = math.isclose(got, expected, rel_tol=1e-3, abs_tol=1e-9)
        print(f"{'PASS' if ok else 'FAIL'}: {name}: got {got:,.6g}, expected {expected:,.6g}")
        failures += 0 if ok else 1
    if failures:
        print(f"FAIL: {failures} of {len(checks)} checks failed.")
        sys.exit(1)
    print(f"PASS: all {len(checks)} checks passed.")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="financial_statements.py",
        description=(
            "Financial statement analysis reference implementation. Main "
            "classes: FreeCashFlow (ebitda, nopat, cfo_indirect, "
            "fcff_from_cfo, fcff_from_ebit, fcfe_from_cfo, fcfe_from_fcff), "
            "Profitability (gross_margin, operating_margin, net_margin, "
            "invested_capital, roic, roic_spread, dupont), EarningsQuality "
            "(accruals_ratio, days_sales_outstanding, "
            "days_inventory_outstanding, days_payables_outstanding, "
            "cash_conversion_cycle), TaxBasis (unrealized_gain, "
            "embedded_tax_liability, after_tax_liquidation_value)."
        ),
        epilog=(
            "Primarily intended to be imported as a module: "
            "from financial_statements import FreeCashFlow, Profitability, "
            "EarningsQuality, TaxBasis. "
            "Run with no arguments to print a demo."
        ),
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help=(
            "run the demo computations and assert key outputs match the "
            "SKILL.md worked examples (exits nonzero on mismatch)"
        ),
    )
    return parser


if __name__ == "__main__":
    args = _build_parser().parse_args()
    if args.verify:
        _verify()
    else:
        _demo()
