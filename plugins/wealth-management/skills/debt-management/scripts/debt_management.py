# /// script
# dependencies = ["numpy"]
# requires-python = ">=3.11"
# ///
"""
Debt Management
===============
Compute debt payoff strategies (avalanche vs snowball), amortization schedules,
refinancing breakeven, debt-to-income ratios, and opportunity cost analysis.

Part of Layer 6 (Personal Finance) in the finance skills framework.
"""

import argparse
import sys
import math
from dataclasses import dataclass

import numpy as np


@dataclass
class Debt:
    """Represents a single debt obligation.

    Parameters
    ----------
    name : str
        Descriptive label for the debt.
    balance : float
        Current outstanding balance in dollars.
    apr : float
        Annual percentage rate as a decimal (e.g., 0.22 for 22%).
    minimum_payment : float
        Required minimum monthly payment in dollars.
    """

    name: str
    balance: float
    apr: float
    minimum_payment: float


class DebtManagement:
    """Debt management computations: payoff strategies, amortization,
    refinancing, and DTI analysis.

    Parameters
    ----------
    debts : list[Debt]
        List of Debt objects representing outstanding obligations.
    extra_payment : float, optional
        Additional monthly payment above all minimums. Default is 0.0.
    """

    def __init__(self, debts: list[Debt], extra_payment: float = 0.0):
        self.debts = [Debt(d.name, d.balance, d.apr, d.minimum_payment) for d in debts]
        self.extra_payment = extra_payment

    @staticmethod
    def months_to_payoff(balance: float, apr: float, payment: float) -> float:
        """Compute months to pay off a debt with fixed payments.

        Uses n = -ln(1 - P*r/PMT) / ln(1+r).

        Parameters
        ----------
        balance : float
            Outstanding principal.
        apr : float
            Annual percentage rate as a decimal.
        payment : float
            Monthly payment amount.

        Returns
        -------
        float
            Number of months to payoff. Returns inf if payment does not
            cover interest.
        """
        if balance <= 0:
            return 0.0
        r = apr / 12.0
        if r == 0:
            return balance / payment if payment > 0 else float("inf")
        if payment <= balance * r:
            return float("inf")
        # log1p avoids precision loss (and division by zero) near r = 0
        n = -math.log1p(-(balance * r) / payment) / math.log1p(r)
        return n

    @staticmethod
    def total_interest(balance: float, apr: float, payment: float) -> float:
        """Compute total interest paid over the life of a debt.

        Parameters
        ----------
        balance : float
            Outstanding principal.
        apr : float
            Annual percentage rate as a decimal.
        payment : float
            Monthly payment amount.

        Returns
        -------
        float
            Total interest paid in dollars.
        """
        n = DebtManagement.months_to_payoff(balance, apr, payment)
        if math.isinf(n):
            return float("inf")
        # Last payment may be partial, so simulate
        r = apr / 12.0
        total_interest_paid = 0.0
        remaining = balance
        while remaining > 0:
            interest = remaining * r
            total_interest_paid += interest
            principal_portion = min(payment - interest, remaining)
            remaining -= principal_portion
            if payment <= interest:
                return float("inf")
        return total_interest_paid

    @staticmethod
    def amortization_schedule(
        balance: float, apr: float, payment: float, extra: float = 0.0
    ) -> np.ndarray:
        """Generate a full amortization schedule.

        Parameters
        ----------
        balance : float
            Loan principal.
        apr : float
            Annual percentage rate as a decimal.
        payment : float
            Base monthly payment.
        extra : float, optional
            Extra monthly principal payment. Default is 0.0.

        Returns
        -------
        np.ndarray
            Structured array with columns: month, payment, interest,
            principal, extra_principal, remaining_balance.
        """
        r = apr / 12.0
        rows: list[tuple[int, float, float, float, float, float]] = []
        remaining = balance
        month = 0
        while remaining > 0.005:  # threshold for rounding
            month += 1
            interest = remaining * r
            base_principal = min(payment - interest, remaining)
            if base_principal < 0:
                # Payment doesn't cover interest
                break
            remaining -= base_principal
            extra_applied = min(extra, remaining)
            remaining -= extra_applied
            actual_payment = interest + base_principal + extra_applied
            rows.append(
                (month, actual_payment, interest, base_principal, extra_applied, max(remaining, 0.0))
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
    def apr_to_effective_rate(apr: float, compounding_periods: int = 12) -> float:
        """Convert APR to effective annual rate.

        EAR = (1 + APR/m)^m - 1

        Parameters
        ----------
        apr : float
            Nominal annual percentage rate as a decimal.
        compounding_periods : int, optional
            Number of compounding periods per year. Default is 12 (monthly).

        Returns
        -------
        float
            Effective annual rate as a decimal.
        """
        # expm1(m*log1p(APR/m)) == (1+APR/m)^m - 1, without cancellation near 0
        return math.expm1(compounding_periods * math.log1p(apr / compounding_periods))

    @staticmethod
    def after_tax_rate(apr: float, marginal_tax_rate: float) -> float:
        """Compute the effective after-tax interest rate for tax-deductible debt.

        effective_rate = apr * (1 - marginal_tax_rate)

        Parameters
        ----------
        apr : float
            Annual interest rate as a decimal.
        marginal_tax_rate : float
            Marginal tax rate as a decimal.

        Returns
        -------
        float
            After-tax effective rate as a decimal.
        """
        return apr * (1.0 - marginal_tax_rate)

    @staticmethod
    def debt_to_income(
        monthly_debt_payments: float, gross_monthly_income: float
    ) -> float:
        """Compute the back-end debt-to-income ratio.

        DTI = monthly debt payments / gross monthly income

        Parameters
        ----------
        monthly_debt_payments : float
            Total monthly debt obligations.
        gross_monthly_income : float
            Gross monthly income before taxes.

        Returns
        -------
        float
            DTI ratio as a decimal (e.g., 0.36 = 36%).
        """
        if gross_monthly_income <= 0:
            return float("inf")
        return monthly_debt_payments / gross_monthly_income

    @staticmethod
    def front_end_dti(
        monthly_housing_cost: float, gross_monthly_income: float
    ) -> float:
        """Compute the front-end (housing) debt-to-income ratio.

        Front-end DTI = housing costs / gross monthly income

        Parameters
        ----------
        monthly_housing_cost : float
            Monthly housing payment (PITI: principal, interest, taxes, insurance).
        gross_monthly_income : float
            Gross monthly income before taxes.

        Returns
        -------
        float
            Front-end DTI ratio as a decimal.
        """
        if gross_monthly_income <= 0:
            return float("inf")
        return monthly_housing_cost / gross_monthly_income

    @staticmethod
    def refinance_breakeven(
        closing_costs: float, old_payment: float, new_payment: float
    ) -> float:
        """Compute the refinancing breakeven period in months.

        Breakeven = closing costs / monthly savings

        Parameters
        ----------
        closing_costs : float
            Total refinancing closing costs.
        old_payment : float
            Current monthly payment.
        new_payment : float
            New monthly payment after refinancing.

        Returns
        -------
        float
            Months to breakeven. Returns inf if new payment is not lower.
        """
        savings = old_payment - new_payment
        if savings <= 0:
            return float("inf")
        return closing_costs / savings

    def payoff_avalanche(self) -> dict:
        """Simulate debt payoff using the avalanche strategy (highest rate first).

        Returns
        -------
        dict
            Keys: 'total_months', 'total_interest', 'total_paid',
            'payoff_order' (list of dicts with name, month_paid_off, interest_paid).
        """
        return self._simulate_payoff(strategy="avalanche")

    def payoff_snowball(self) -> dict:
        """Simulate debt payoff using the snowball strategy (smallest balance first).

        Returns
        -------
        dict
            Keys: 'total_months', 'total_interest', 'total_paid',
            'payoff_order' (list of dicts with name, month_paid_off, interest_paid).
        """
        return self._simulate_payoff(strategy="snowball")

    def _simulate_payoff(self, strategy: str) -> dict:
        """Simulate multi-debt payoff month by month.

        Parameters
        ----------
        strategy : str
            'avalanche' (highest APR first) or 'snowball' (lowest balance first).

        Returns
        -------
        dict
            Payoff results including total months, interest, and order.
        """
        # Deep copy balances
        balances = {d.name: d.balance for d in self.debts}
        rates = {d.name: d.apr / 12.0 for d in self.debts}
        minimums = {d.name: d.minimum_payment for d in self.debts}
        interest_paid = {d.name: 0.0 for d in self.debts}
        paid_off: set[str] = set()
        payoff_order: list[dict] = []
        total_paid = 0.0
        month = 0
        max_months = 1200  # safety limit (100 years)

        while any(b > 0.005 for b in balances.values()) and month < max_months:
            month += 1
            # Determine priority order for extra payment
            active = [name for name in balances if balances[name] > 0.005]
            if not active:
                break
            if strategy == "avalanche":
                active.sort(key=lambda n: rates[n], reverse=True)
            else:  # snowball
                active.sort(key=lambda n: balances[n])

            # Apply interest to all active debts
            for name in active:
                interest = balances[name] * rates[name]
                interest_paid[name] += interest
                balances[name] += interest

            # Freed minimums from already-paid-off debts snowball into the
            # extra payment every month for the rest of the simulation.
            extra_available = self.extra_payment + sum(
                minimums[name] for name in paid_off
            )

            # Pay minimums on active debts
            for name in list(active):
                pay = min(minimums[name], balances[name])
                balances[name] -= pay
                total_paid += pay
                if balances[name] <= 0.005:
                    # Unused portion of this debt's minimum is freed this month
                    extra_available += minimums[name] - pay
                    balances[name] = 0.0
                    paid_off.add(name)
                    payoff_order.append(
                        {
                            "name": name,
                            "month_paid_off": month,
                            "interest_paid": round(interest_paid[name], 2),
                        }
                    )

            # Apply extra payment + freed minimums to priority debt(s)
            # Recalculate active after minimum payments
            active = [name for name in balances if balances[name] > 0.005]
            if strategy == "avalanche":
                active.sort(key=lambda n: rates[n], reverse=True)
            else:
                active.sort(key=lambda n: balances[n])

            for name in active:
                if extra_available <= 0:
                    break
                apply = min(extra_available, balances[name])
                balances[name] -= apply
                total_paid += apply
                extra_available -= apply
                if balances[name] <= 0.005:
                    balances[name] = 0.0
                    paid_off.add(name)
                    payoff_order.append(
                        {
                            "name": name,
                            "month_paid_off": month,
                            "interest_paid": round(interest_paid[name], 2),
                        }
                    )

        total_interest = sum(interest_paid.values())

        return {
            "total_months": month,
            "total_interest": round(total_interest, 2),
            "total_paid": round(total_paid, 2),
            "payoff_order": payoff_order,
        }

    def compare_strategies(self) -> dict:
        """Compare avalanche and snowball strategies side by side.

        Returns
        -------
        dict
            Keys: 'avalanche', 'snowball', 'interest_difference',
            'months_difference'.
        """
        avalanche = self.payoff_avalanche()
        snowball = self.payoff_snowball()
        return {
            "avalanche": avalanche,
            "snowball": snowball,
            "interest_difference": round(
                snowball["total_interest"] - avalanche["total_interest"], 2
            ),
            "months_difference": snowball["total_months"] - avalanche["total_months"],
        }


def _demo() -> None:
    # ----------------------------------------------------------------
    # Demo: Debt management computations
    # ----------------------------------------------------------------
    print("=" * 60)
    print("Debt Management - Demo")
    print("=" * 60)

    # --- Example 1: Avalanche vs Snowball ---
    print("\n--- Example 1: Avalanche vs Snowball Comparison ---")
    debts = [
        Debt("Credit Card", 5000, 0.22, 100),
        Debt("Student Loan", 12000, 0.06, 200),
        Debt("Personal Loan", 3000, 0.15, 75),
    ]
    dm = DebtManagement(debts, extra_payment=500)
    comparison = dm.compare_strategies()

    for strategy_name in ("avalanche", "snowball"):
        result = comparison[strategy_name]
        print(f"\n  {strategy_name.upper()}:")
        print(f"    Total months:   {result['total_months']}")
        print(f"    Total interest: ${result['total_interest']:,.2f}")
        for entry in result["payoff_order"]:
            print(
                f"      {entry['name']:20s} paid off month {entry['month_paid_off']:3d}"
                f"  (interest: ${entry['interest_paid']:,.2f})"
            )

    print(f"\n  Avalanche saves ${comparison['interest_difference']:,.2f} in interest")
    print(f"  Avalanche saves {comparison['months_difference']} month(s)")

    # --- Example 2: Amortization Schedule ---
    print("\n--- Example 2: Amortization Schedule (first 6 months) ---")
    schedule = DebtManagement.amortization_schedule(
        balance=300_000, apr=0.065, payment=1896, extra=200
    )
    print(f"  {'Month':>5}  {'Payment':>10}  {'Interest':>10}  {'Principal':>10}  {'Extra':>8}  {'Balance':>12}")
    for row in schedule[:6]:
        print(
            f"  {row['month']:5d}  ${row['payment']:9,.2f}  ${row['interest']:9,.2f}"
            f"  ${row['principal']:9,.2f}  ${row['extra_principal']:7,.2f}  ${row['remaining_balance']:11,.2f}"
        )
    print(f"  ... total months: {len(schedule)}")
    total_int = float(np.sum(schedule["interest"]))
    print(f"  Total interest paid: ${total_int:,.2f}")

    # --- Example 3: Refinance Breakeven ---
    print("\n--- Example 3: Refinance Breakeven ---")
    old_pmt = 2028
    new_pmt = 1838
    costs = 6000
    be_months = DebtManagement.refinance_breakeven(costs, old_pmt, new_pmt)
    print(f"  Old payment:    ${old_pmt:,.2f}/mo")
    print(f"  New payment:    ${new_pmt:,.2f}/mo")
    print(f"  Closing costs:  ${costs:,.2f}")
    print(f"  Breakeven:      {be_months:.1f} months ({be_months/12:.1f} years)")

    # --- Example 4: DTI Ratios ---
    print("\n--- Example 4: Debt-to-Income Ratios ---")
    gross_income = 8500
    housing = 1800
    total_debt = 1800 + 500 + 200 + 100  # housing + car + student + cc
    fe_dti = DebtManagement.front_end_dti(housing, gross_income)
    be_dti = DebtManagement.debt_to_income(total_debt, gross_income)
    print(f"  Gross monthly income: ${gross_income:,.2f}")
    print(f"  Front-end DTI:        {fe_dti:.2%} (guideline: <28%)")
    print(f"  Back-end DTI:         {be_dti:.2%} (guideline: <36%)")

    # --- Example 5: APR to Effective Rate ---
    print("\n--- Example 5: APR to Effective Rate ---")
    apr_val = 0.22
    ear = DebtManagement.apr_to_effective_rate(apr_val)
    after_tax = DebtManagement.after_tax_rate(0.065, 0.24)
    print(f"  22% APR (monthly compounding) -> EAR = {ear:.4%}")
    print(f"  6.5% mortgage (24% tax bracket) -> after-tax rate = {after_tax:.4%}")

    print("\n" + "=" * 60)
    print("Demo complete.")
    print("=" * 60)

def _check(failures: list, name: str, actual: float, expected: float, tol: float) -> None:
    """Record a verification check result."""
    ok = abs(actual - expected) <= tol
    status = "PASS" if ok else "FAIL"
    print(f"  [{status}] {name}: actual={actual:.6g}, expected={expected:.6g}, tol={tol:.2g}")
    if not ok:
        failures.append(name)

def _verify() -> None:
    """Verify key outputs against the SKILL.md worked examples."""
    failures: list = []

    # SKILL.md Example 1: avalanche vs snowball
    debts = [
        Debt("Credit Card", 5000, 0.22, 100),
        Debt("Student Loan", 12000, 0.06, 200),
        Debt("Personal Loan", 3000, 0.15, 75),
    ]
    dm = DebtManagement(debts, extra_payment=500)
    av = dm.payoff_avalanche()
    sb = dm.payoff_snowball()
    _check(failures, "Ex1 avalanche months", av["total_months"], 26, 0)
    _check(failures, "Ex1 avalanche interest", av["total_interest"], 1945.92, 1.0)
    _check(failures, "Ex1 avalanche total paid = principal + interest",
           av["total_paid"], 20000 + av["total_interest"], 0.5)
    _check(failures, "Ex1 avalanche first payoff (CC) month",
           av["payoff_order"][0]["month_paid_off"], 10, 0)
    _check(failures, "Ex1 snowball months", sb["total_months"], 26, 0)
    _check(failures, "Ex1 snowball interest", sb["total_interest"], 2104.35, 1.0)
    _check(failures, "Ex1 snowball first payoff (PL) month",
           sb["payoff_order"][0]["month_paid_off"], 6, 0)

    # SKILL.md Example 2: refinance breakeven
    _check(failures, "Ex2 refinance breakeven months",
           DebtManagement.refinance_breakeven(6000, 2028, 1838), 31.58, 0.01)

    if failures:
        print(f"\n{len(failures)} check(s) FAILED: {', '.join(failures)}")
        sys.exit(1)
    print("\nAll checks passed.")

def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__.strip().splitlines()[2] if __doc__ else "",
        epilog=(
            "Provides: Debt, DebtManagement. "
            "For programmatic use, import this module (debt_management) instead of running it. "
            "Bare run executes a demo whose printed values match the SKILL.md worked examples; "
            "--verify asserts those values and exits nonzero on mismatch."
        ),
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="run the verification checks against the SKILL.md worked-example values",
    )
    args = parser.parse_args()
    if args.verify:
        _verify()
    else:
        _demo()


if __name__ == "__main__":
    main()
