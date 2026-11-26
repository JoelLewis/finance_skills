# /// script
# dependencies = ["numpy"]
# requires-python = ">=3.11"
# ///
"""
Lending Analysis
================
Compute loan payments (fixed-rate), amortization, LTV, DSCR, interest-only and
balloon payments, points breakeven, extra payment savings, and refinance analysis.

Part of Layer 6 (Personal Finance) in the finance skills framework.
"""

import argparse
import math
import sys

import numpy as np


class LendingAnalysis:
    """Lending and mortgage analysis computations.

    All methods are static — no instance state is required.
    """

    @staticmethod
    def monthly_payment(principal: float, apr: float, term_months: int) -> float:
        """Compute the fixed monthly payment for a fully amortizing loan.

        PMT = P * [r(1+r)^n] / [(1+r)^n - 1]

        Parameters
        ----------
        principal : float
            Loan amount in dollars.
        apr : float
            Annual percentage rate as a decimal (e.g., 0.065 for 6.5%).
        term_months : int
            Loan term in months.

        Returns
        -------
        float
            Monthly payment amount.
        """
        if principal <= 0:
            return 0.0
        r = apr / 12.0
        if r == 0:
            return principal / term_months
        # P*r*(1+r)^n / [(1+r)^n - 1] == P*r / [1 - (1+r)^-n]; expm1/log1p
        # avoid cancellation (and division by zero) near r = 0
        return principal * r / -math.expm1(-term_months * math.log1p(r))

    @staticmethod
    def total_interest(principal: float, apr: float, term_months: int) -> float:
        """Compute total interest paid over the life of a loan.

        Total interest = (n * PMT) - P

        Parameters
        ----------
        principal : float
            Loan amount.
        apr : float
            Annual percentage rate as a decimal.
        term_months : int
            Loan term in months.

        Returns
        -------
        float
            Total interest paid in dollars.
        """
        pmt = LendingAnalysis.monthly_payment(principal, apr, term_months)
        return term_months * pmt - principal

    @staticmethod
    def remaining_balance(
        principal: float, apr: float, term_months: int, payments_made: int
    ) -> float:
        """Compute the remaining balance after k payments.

        B_k = P * [(1+r)^n - (1+r)^k] / [(1+r)^n - 1]

        Parameters
        ----------
        principal : float
            Original loan amount.
        apr : float
            Annual percentage rate as a decimal.
        term_months : int
            Original loan term in months.
        payments_made : int
            Number of payments already made.

        Returns
        -------
        float
            Remaining principal balance.
        """
        r = apr / 12.0
        if r == 0:
            return principal * (1.0 - payments_made / term_months)
        n = term_months
        k = payments_made
        # [(1+r)^n - (1+r)^k] / [(1+r)^n - 1] rewritten with expm1/log1p to
        # avoid cancellation near r = 0
        log_g = math.log1p(r)
        balance = principal * (
            math.expm1(n * log_g) - math.expm1(k * log_g)
        ) / math.expm1(n * log_g)
        return max(balance, 0.0)

    @staticmethod
    def loan_to_value(loan_amount: float, property_value: float) -> float:
        """Compute the loan-to-value ratio.

        LTV = loan amount / property value

        Parameters
        ----------
        loan_amount : float
            Outstanding loan balance.
        property_value : float
            Appraised property value.

        Returns
        -------
        float
            LTV as a decimal (e.g., 0.80 = 80%).
        """
        if property_value <= 0:
            return float("inf")
        return loan_amount / property_value

    @staticmethod
    def combined_ltv(
        first_mortgage: float, heloc_limit: float, property_value: float
    ) -> float:
        """Compute the combined loan-to-value ratio.

        CLTV = (first mortgage + HELOC) / property value

        Parameters
        ----------
        first_mortgage : float
            First mortgage balance.
        heloc_limit : float
            HELOC credit limit (or second mortgage balance).
        property_value : float
            Appraised property value.

        Returns
        -------
        float
            CLTV as a decimal.
        """
        if property_value <= 0:
            return float("inf")
        return (first_mortgage + heloc_limit) / property_value

    @staticmethod
    def debt_service_coverage_ratio(
        net_operating_income: float, annual_debt_service: float
    ) -> float:
        """Compute the debt service coverage ratio (DSCR).

        DSCR = NOI / annual debt service

        Parameters
        ----------
        net_operating_income : float
            Annual net operating income.
        annual_debt_service : float
            Annual total debt payments (principal + interest).

        Returns
        -------
        float
            DSCR ratio. Values > 1.0 indicate sufficient income to cover debt.
        """
        if annual_debt_service <= 0:
            return float("inf")
        return net_operating_income / annual_debt_service

    @staticmethod
    def interest_only_payment(principal: float, apr: float) -> float:
        """Compute the monthly interest-only payment.

        IO payment = P * r / 12

        Parameters
        ----------
        principal : float
            Outstanding loan balance.
        apr : float
            Annual percentage rate as a decimal.

        Returns
        -------
        float
            Monthly interest-only payment.
        """
        return principal * apr / 12.0

    @staticmethod
    def balloon_payment(
        principal: float,
        apr: float,
        amortization_months: int,
        balloon_month: int,
    ) -> float:
        """Compute the balloon payment due at a specified month.

        The loan is amortized over a longer term but the remaining balance
        is due as a lump sum at the balloon date.

        Parameters
        ----------
        principal : float
            Original loan amount.
        apr : float
            Annual percentage rate as a decimal.
        amortization_months : int
            Amortization schedule term in months (e.g., 360 for 30-year).
        balloon_month : int
            Month at which the balloon payment is due (e.g., 84 for 7 years).

        Returns
        -------
        float
            Balloon payment amount (remaining balance at balloon month).
        """
        return LendingAnalysis.remaining_balance(
            principal, apr, amortization_months, balloon_month
        )

    @staticmethod
    def points_breakeven(
        loan_amount: float,
        points: float,
        rate_reduction: float,
        term_months: int,
        original_rate: float,
    ) -> float:
        """Compute the breakeven period for buying mortgage points.

        Parameters
        ----------
        loan_amount : float
            Loan amount in dollars.
        points : float
            Number of points purchased (1 point = 1% of loan amount).
        rate_reduction : float
            Rate reduction achieved as a decimal (e.g., 0.0025 for 0.25%).
        term_months : int
            Loan term in months.
        original_rate : float
            Original interest rate as a decimal.

        Returns
        -------
        float
            Months to break even on the points cost.
        """
        cost = loan_amount * points / 100.0
        pmt_old = LendingAnalysis.monthly_payment(loan_amount, original_rate, term_months)
        pmt_new = LendingAnalysis.monthly_payment(
            loan_amount, original_rate - rate_reduction, term_months
        )
        savings = pmt_old - pmt_new
        if savings <= 0:
            return float("inf")
        return cost / savings

    @staticmethod
    def refinance_breakeven(
        closing_costs: float,
        old_payment: float,
        new_payment: float,
    ) -> float:
        """Compute the refinancing breakeven period in months.

        Breakeven = closing costs / (old payment - new payment)

        Parameters
        ----------
        closing_costs : float
            Total closing costs for refinancing.
        old_payment : float
            Current monthly payment.
        new_payment : float
            New monthly payment after refinancing.

        Returns
        -------
        float
            Months to recoup refinancing costs.
        """
        savings = old_payment - new_payment
        if savings <= 0:
            return float("inf")
        return closing_costs / savings

    @staticmethod
    def refinance_total_savings(
        old_balance: float,
        old_rate: float,
        old_remaining_months: int,
        new_rate: float,
        new_term_months: int,
        closing_costs: float,
    ) -> dict:
        """Compare total cost of existing loan vs refinanced loan.

        Parameters
        ----------
        old_balance : float
            Remaining balance on the current loan.
        old_rate : float
            Current loan APR as a decimal.
        old_remaining_months : int
            Months remaining on the current loan.
        new_rate : float
            New loan APR as a decimal.
        new_term_months : int
            Term of the new loan in months.
        closing_costs : float
            Total closing costs for refinancing.

        Returns
        -------
        dict
            Keys: 'old_total_cost', 'new_total_cost', 'net_savings',
            'old_payment', 'new_payment', 'breakeven_months'.
        """
        old_pmt = LendingAnalysis.monthly_payment(
            old_balance, old_rate, old_remaining_months
        )
        new_pmt = LendingAnalysis.monthly_payment(
            old_balance, new_rate, new_term_months
        )
        old_total = old_pmt * old_remaining_months
        new_total = new_pmt * new_term_months + closing_costs
        breakeven = LendingAnalysis.refinance_breakeven(closing_costs, old_pmt, new_pmt)

        return {
            "old_payment": round(old_pmt, 2),
            "new_payment": round(new_pmt, 2),
            "old_total_cost": round(old_total, 2),
            "new_total_cost": round(new_total, 2),
            "net_savings": round(old_total - new_total, 2),
            "breakeven_months": round(breakeven, 1),
        }

    @staticmethod
    def extra_payment_savings(
        principal: float, apr: float, term_months: int, extra_monthly: float
    ) -> dict:
        """Compute the interest savings and time saved from extra payments.

        Parameters
        ----------
        principal : float
            Loan amount.
        apr : float
            Annual percentage rate as a decimal.
        term_months : int
            Original loan term in months.
        extra_monthly : float
            Additional monthly payment toward principal.

        Returns
        -------
        dict
            Keys: 'original_months', 'new_months', 'months_saved',
            'original_interest', 'new_interest', 'interest_saved'.
        """
        r = apr / 12.0
        base_pmt = LendingAnalysis.monthly_payment(principal, apr, term_months)
        original_interest = term_months * base_pmt - principal

        # Simulate with extra payments
        balance = principal
        total_pmt = base_pmt + extra_monthly
        new_interest = 0.0
        new_months = 0
        while balance > 0.005:
            new_months += 1
            interest = balance * r
            new_interest += interest
            principal_portion = min(total_pmt - interest, balance)
            balance -= principal_portion
            if total_pmt <= interest:
                break
            if new_months > term_months * 2:
                break

        return {
            "original_months": term_months,
            "new_months": new_months,
            "months_saved": term_months - new_months,
            "original_interest": round(original_interest, 2),
            "new_interest": round(new_interest, 2),
            "interest_saved": round(original_interest - new_interest, 2),
        }

    @staticmethod
    def amortization_schedule(
        principal: float, apr: float, term_months: int, extra: float = 0.0
    ) -> np.ndarray:
        """Generate a full amortization schedule.

        Parameters
        ----------
        principal : float
            Loan amount.
        apr : float
            Annual percentage rate as a decimal.
        term_months : int
            Loan term in months.
        extra : float, optional
            Extra monthly principal payment. Default is 0.0.

        Returns
        -------
        np.ndarray
            Structured array with columns: month, payment, interest,
            principal, extra_principal, remaining_balance.
        """
        r = apr / 12.0
        base_pmt = LendingAnalysis.monthly_payment(principal, apr, term_months)
        rows: list[tuple[int, float, float, float, float, float]] = []
        balance = principal

        month = 0
        while balance > 0.005:
            month += 1
            interest = balance * r
            base_principal = min(base_pmt - interest, balance)
            if base_principal < 0:
                break
            balance -= base_principal
            extra_applied = min(extra, balance)
            balance -= extra_applied
            actual_pmt = interest + base_principal + extra_applied
            rows.append(
                (month, actual_pmt, interest, base_principal, extra_applied, max(balance, 0.0))
            )

        dtype = np.dtype(
            [
                ("month", np.int32),
                ("payment", np.float64),
                ("interest", np.float64),
                ("principal", np.float64),
                ("extra_principal", np.float64),
                ("remaining_balance", np.float64),
            ]
        )
        return np.array(rows, dtype=dtype)

    @staticmethod
    def pmi_cost(loan_amount: float, pmi_rate: float = 0.008) -> float:
        """Estimate annual PMI cost.

        Parameters
        ----------
        loan_amount : float
            Outstanding loan balance.
        pmi_rate : float, optional
            Annual PMI rate as a decimal. Default is 0.008 (0.8%).

        Returns
        -------
        float
            Monthly PMI payment.
        """
        return loan_amount * pmi_rate / 12.0

    @staticmethod
    def arm_payment_after_reset(
        remaining_balance: float,
        index_rate: float,
        margin: float,
        remaining_months: int,
        rate_cap: float | None = None,
        initial_rate: float | None = None,
    ) -> dict:
        """Compute the new payment after an ARM rate adjustment.

        Parameters
        ----------
        remaining_balance : float
            Balance at the time of rate adjustment.
        index_rate : float
            Current index rate (e.g., SOFR) as a decimal.
        margin : float
            ARM margin as a decimal (e.g., 0.0275 for 2.75%).
        remaining_months : int
            Months remaining on the loan.
        rate_cap : float or None, optional
            Lifetime rate cap (maximum rate increase above initial).
        initial_rate : float or None, optional
            Original fixed rate for cap calculation.

        Returns
        -------
        dict
            Keys: 'fully_indexed_rate', 'capped_rate', 'new_payment'.
        """
        fully_indexed = index_rate + margin
        capped = fully_indexed
        if rate_cap is not None and initial_rate is not None:
            max_rate = initial_rate + rate_cap
            capped = min(fully_indexed, max_rate)

        new_pmt = LendingAnalysis.monthly_payment(
            remaining_balance, capped, remaining_months
        )
        return {
            "fully_indexed_rate": round(fully_indexed, 6),
            "capped_rate": round(capped, 6),
            "new_payment": round(new_pmt, 2),
        }


def _demo() -> None:
    # ----------------------------------------------------------------
    # Demo: Lending analysis computations
    # ----------------------------------------------------------------
    LA = LendingAnalysis

    print("=" * 60)
    print("Lending Analysis - Demo")
    print("=" * 60)

    # --- Example 1: 30-year vs 15-year ---
    print("\n--- Example 1: 30-Year vs 15-Year Mortgage ---")
    principal = 400_000
    pmt_30 = LA.monthly_payment(principal, 0.065, 360)
    pmt_15 = LA.monthly_payment(principal, 0.059, 180)
    int_30 = LA.total_interest(principal, 0.065, 360)
    int_15 = LA.total_interest(principal, 0.059, 180)
    print(f"  Loan amount: ${principal:,.0f}")
    print(f"  30-year @ 6.5%: ${pmt_30:,.2f}/mo, total interest ${int_30:,.2f}")
    print(f"  15-year @ 5.9%: ${pmt_15:,.2f}/mo, total interest ${int_15:,.2f}")
    print(f"  Payment difference: ${pmt_15 - pmt_30:,.2f}/mo more")
    print(f"  Interest savings:   ${int_30 - int_15:,.2f}")

    # --- Example 2: Extra Payment Savings ---
    print("\n--- Example 2: Extra Payment Impact ---")
    result = LA.extra_payment_savings(300_000, 0.065, 360, 200)
    print(f"  $300K @ 6.5% 30-year + $200/mo extra:")
    print(f"    Original term:   {result['original_months']} months")
    print(f"    New term:        {result['new_months']} months ({result['new_months']/12:.1f} years)")
    print(f"    Months saved:    {result['months_saved']} ({result['months_saved']/12:.1f} years)")
    print(f"    Interest saved:  ${result['interest_saved']:,.2f}")

    # --- Example 3: LTV and PMI ---
    print("\n--- Example 3: LTV and PMI ---")
    home_value = 500_000
    down = 50_000
    loan = home_value - down
    ltv = LA.loan_to_value(loan, home_value)
    pmi_monthly = LA.pmi_cost(loan)
    print(f"  Home value: ${home_value:,.0f}, Down: ${down:,.0f}, Loan: ${loan:,.0f}")
    print(f"  LTV: {ltv:.1%}")
    print(f"  PMI required: {'Yes' if ltv > 0.80 else 'No'}")
    print(f"  Estimated PMI: ${pmi_monthly:,.2f}/mo")

    # --- Example 4: DSCR ---
    print("\n--- Example 4: Debt Service Coverage Ratio ---")
    noi = 120_000
    annual_debt = 90_000
    dscr = LA.debt_service_coverage_ratio(noi, annual_debt)
    print(f"  NOI: ${noi:,.0f}, Annual debt service: ${annual_debt:,.0f}")
    print(f"  DSCR: {dscr:.2f} ({'Adequate' if dscr >= 1.25 else 'Marginal'})")

    # --- Example 5: Balloon Payment ---
    print("\n--- Example 5: Balloon Payment ---")
    balloon = LA.balloon_payment(500_000, 0.06, 360, 84)
    print(f"  $500K loan, 30-year amortization, 7-year balloon:")
    print(f"  Balloon payment: ${balloon:,.2f}")

    # --- Example 6: Refinance Analysis ---
    print("\n--- Example 6: Refinance Analysis ---")
    refi = LA.refinance_total_savings(
        old_balance=300_000,
        old_rate=0.065,
        old_remaining_months=300,
        new_rate=0.055,
        new_term_months=300,
        closing_costs=6_000,
    )
    print(f"  Old payment: ${refi['old_payment']:,.2f}/mo")
    print(f"  New payment: ${refi['new_payment']:,.2f}/mo")
    print(f"  Breakeven:   {refi['breakeven_months']:.1f} months")
    print(f"  Net savings: ${refi['net_savings']:,.2f}")

    # --- Example 7: Points Breakeven ---
    print("\n--- Example 7: Mortgage Points Breakeven ---")
    be_months = LA.points_breakeven(
        loan_amount=400_000,
        points=1.0,
        rate_reduction=0.0025,
        term_months=360,
        original_rate=0.065,
    )
    print(f"  1 point on $400K (cost: $4,000), rate reduction: 0.25%")
    print(f"  Breakeven: {be_months:.1f} months ({be_months/12:.1f} years)")

    # --- Example 8: ARM Reset ---
    print("\n--- Example 8: ARM Rate Reset ---")
    arm = LA.arm_payment_after_reset(
        remaining_balance=380_000,
        index_rate=0.05,
        margin=0.0275,
        remaining_months=300,
        rate_cap=0.05,
        initial_rate=0.045,
    )
    print(f"  Balance: $380K, SOFR: 5.0%, Margin: 2.75%")
    print(f"  Fully indexed rate: {arm['fully_indexed_rate']:.2%}")
    print(f"  Capped rate:        {arm['capped_rate']:.2%}")
    print(f"  New payment:        ${arm['new_payment']:,.2f}/mo")

    print("\n" + "=" * 60)
    print("Demo complete.")
    print("=" * 60)


def _verify() -> int:
    """Assert that demo computations match the SKILL.md worked examples."""
    LA = LendingAnalysis
    failures: list[str] = []

    def check(label: str, actual: float, expected: float, rel_tol: float = 1e-3) -> None:
        ok = math.isclose(actual, expected, rel_tol=rel_tol)
        print(f"  {'PASS' if ok else 'FAIL'}: {label}: got {actual:,.2f}, expected {expected:,.2f}")
        if not ok:
            failures.append(label)

    print("Verifying against SKILL.md worked examples...")

    # Example 1: $400K, 30-year @ 6.5% vs 15-year @ 5.9%
    check("Ex1 30-year payment", LA.monthly_payment(400_000, 0.065, 360), 2_528.0)
    check("Ex1 30-year total interest", LA.total_interest(400_000, 0.065, 360), 510_178.0)
    check("Ex1 15-year payment", LA.monthly_payment(400_000, 0.059, 180), 3_354.0)
    check("Ex1 15-year total interest", LA.total_interest(400_000, 0.059, 180), 203_694.0)

    # Example 2: $300K, 30-year @ 6.5%, $200/month extra
    check("Ex2 base payment", LA.monthly_payment(300_000, 0.065, 360), 1_896.20)
    check("Ex2 baseline total interest", LA.total_interest(300_000, 0.065, 360), 382_633.0)
    extra = LA.extra_payment_savings(300_000, 0.065, 360, 200)
    check("Ex2 payoff months (277)", extra["new_months"], 277, rel_tol=1e-9)
    check("Ex2 months saved (83)", extra["months_saved"], 83, rel_tol=1e-9)
    check("Ex2 total interest with extra", extra["new_interest"], 279_185.0)
    check("Ex2 interest saved", extra["interest_saved"], 103_449.0)

    if failures:
        print(f"FAIL: {len(failures)} check(s) did not match SKILL.md.")
        return 1
    print("PASS: all checks match SKILL.md worked examples.")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Lending analysis reference implementation: loan payments, "
            "amortization, extra-payment savings, LTV/CLTV, DSCR, balloon "
            "payments, points and refinance breakevens, PMI, and ARM resets."
        ),
        epilog=(
            "Main class:\n"
            "  LendingAnalysis -- static methods: monthly_payment, total_interest,\n"
            "    remaining_balance, loan_to_value, combined_ltv,\n"
            "    debt_service_coverage_ratio, interest_only_payment, balloon_payment,\n"
            "    points_breakeven, refinance_breakeven, refinance_total_savings,\n"
            "    extra_payment_savings, amortization_schedule, pmi_cost,\n"
            "    arm_payment_after_reset\n"
            "\n"
            "This file is primarily meant to be imported as a module:\n"
            "  from lending import LendingAnalysis\n"
            "\n"
            "Run with no arguments to print a worked demo."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="recompute the demo figures and assert they match the SKILL.md worked examples",
    )
    args = parser.parse_args()

    if args.verify:
        sys.exit(_verify())
    _demo()


if __name__ == "__main__":
    main()
