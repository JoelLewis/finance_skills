# /// script
# dependencies = ["numpy"]
# requires-python = ">=3.11"
# ///
"""
Emergency Fund Planning
=======================
Compute emergency fund sizing (expense-based and income-based), tiered allocation,
opportunity cost analysis, drawdown modeling, and replenishment schedules.

Part of Layer 6 (Personal Finance) in the finance skills framework.
"""

import argparse
import sys
import numpy as np


class EmergencyFund:
    """Emergency fund sizing, allocation, and analysis computations.

    All methods are static — no instance state is required.
    """

    @staticmethod
    def expense_based_fund(
        monthly_essentials: float, months_coverage: int
    ) -> float:
        """Compute the emergency fund target using the expense-based method.

        Emergency fund = monthly essential expenses * months of coverage

        Parameters
        ----------
        monthly_essentials : float
            Total monthly essential (non-discretionary) expenses.
        months_coverage : int
            Desired months of expense coverage (typically 3-6).

        Returns
        -------
        float
            Target emergency fund size.
        """
        return monthly_essentials * months_coverage

    @staticmethod
    def income_based_fund(
        after_tax_monthly_income: float, months_coverage: int
    ) -> float:
        """Compute the emergency fund target using the income replacement method.

        Emergency fund = after-tax monthly income * months of coverage

        Parameters
        ----------
        after_tax_monthly_income : float
            Monthly take-home pay.
        months_coverage : int
            Desired months of income replacement.

        Returns
        -------
        float
            Target emergency fund size (upper bound estimate).
        """
        return after_tax_monthly_income * months_coverage

    @staticmethod
    def recommended_months(
        dual_income: bool = True,
        stable_employment: bool = True,
        variable_income: bool = False,
        high_search_risk: bool = False,
    ) -> tuple[int, int]:
        """Recommend months of coverage based on personal circumstances.

        Parameters
        ----------
        dual_income : bool, optional
            True if household has two income earners. Default is True.
        stable_employment : bool, optional
            True if employment is stable. Default is True.
        variable_income : bool, optional
            True if income is commission, freelance, or seasonal. Default is False.
        high_search_risk : bool, optional
            True if job search would be difficult (niche, senior). Default is False.

        Returns
        -------
        tuple[int, int]
            (minimum_months, recommended_months) of expense coverage.
        """
        if variable_income or high_search_risk:
            return (6, 12)
        if not stable_employment:
            return (6, 9)
        if dual_income and stable_employment:
            return (3, 4)
        return (3, 6)

    @staticmethod
    def tiered_allocation(
        total_fund: float, monthly_essentials: float
    ) -> dict:
        """Allocate an emergency fund across liquidity tiers.

        Tier 1 (checking): 1 month of expenses — instant access.
        Tier 2 (HYSA/money market): 2-3 months — 1-2 day access.
        Tier 3 (T-bills/CDs/I-bonds): remainder — slightly delayed access.

        Parameters
        ----------
        total_fund : float
            Total emergency fund target.
        monthly_essentials : float
            Monthly essential expenses (used to size tiers).

        Returns
        -------
        dict
            Keys: 'tier_1', 'tier_2', 'tier_3', each with 'amount',
            'months', and 'vehicle' fields.
        """
        tier_1 = min(monthly_essentials, total_fund)
        remaining = total_fund - tier_1

        # Tier 2: up to 3 months
        tier_2_target = monthly_essentials * 3.0
        tier_2 = min(tier_2_target, remaining)
        remaining -= tier_2

        # Tier 3: everything else
        tier_3 = max(remaining, 0.0)

        return {
            "tier_1": {
                "amount": round(tier_1, 2),
                "months": round(tier_1 / monthly_essentials, 1) if monthly_essentials > 0 else 0,
                "vehicle": "Checking / savings account",
            },
            "tier_2": {
                "amount": round(tier_2, 2),
                "months": round(tier_2 / monthly_essentials, 1) if monthly_essentials > 0 else 0,
                "vehicle": "High-yield savings / money market fund",
            },
            "tier_3": {
                "amount": round(tier_3, 2),
                "months": round(tier_3 / monthly_essentials, 1) if monthly_essentials > 0 else 0,
                "vehicle": "T-bills / CDs / I-bonds",
            },
        }

    @staticmethod
    def blended_yield(
        tier_amounts: list[float], tier_yields: list[float]
    ) -> float:
        """Compute the weighted average yield across fund tiers.

        Parameters
        ----------
        tier_amounts : list[float]
            Dollar amounts in each tier.
        tier_yields : list[float]
            Annual yield for each tier as a decimal.

        Returns
        -------
        float
            Blended annual yield as a decimal.
        """
        amounts = np.array(tier_amounts, dtype=np.float64)
        yields = np.array(tier_yields, dtype=np.float64)
        total = np.sum(amounts)
        if total <= 0:
            return 0.0
        return float(np.dot(amounts, yields) / total)

    @staticmethod
    def opportunity_cost(
        fund_balance: float,
        cash_yield: float,
        investment_return: float,
    ) -> float:
        """Compute the annual opportunity cost of holding cash reserves.

        Opportunity cost = fund balance * (investment return - cash yield)

        Parameters
        ----------
        fund_balance : float
            Total emergency fund balance.
        cash_yield : float
            Annual yield on emergency fund as a decimal.
        investment_return : float
            Expected annual return on investments as a decimal.

        Returns
        -------
        float
            Annual opportunity cost in dollars.
        """
        return fund_balance * max(investment_return - cash_yield, 0.0)

    @staticmethod
    def drawdown_schedule(
        fund_balance: float,
        monthly_draw: float,
        fund_yield: float = 0.0,
    ) -> np.ndarray:
        """Model emergency fund drawdown over time.

        Simulates monthly withdrawals from the fund, accounting for any
        yield earned on the remaining balance.

        Parameters
        ----------
        fund_balance : float
            Starting fund balance.
        monthly_draw : float
            Monthly withdrawal amount.
        fund_yield : float, optional
            Annual yield on fund as a decimal. Default is 0.0.

        Returns
        -------
        np.ndarray
            Structured array with columns: month, withdrawal, interest_earned,
            remaining_balance.
        """
        r = fund_yield / 12.0
        rows: list[tuple[int, float, float, float]] = []
        balance = fund_balance
        month = 0

        # If the draw does not exceed the interest on the balance, the fund
        # never depletes; cap the schedule at 1,200 months (100 years), the
        # same safety limit replenishment_schedule uses.
        while balance > 0.005 and month < 1200:
            month += 1
            interest = balance * r
            balance += interest
            withdrawal = min(monthly_draw, balance)
            balance -= withdrawal
            rows.append((month, withdrawal, interest, max(balance, 0.0)))

        dtype = np.dtype(
            [
                ("month", np.int32),
                ("withdrawal", np.float64),
                ("interest_earned", np.float64),
                ("remaining_balance", np.float64),
            ]
        )
        return np.array(rows, dtype=dtype)

    @staticmethod
    def drawdown_duration(
        fund_balance: float,
        monthly_draw: float,
        fund_yield: float = 0.0,
    ) -> float:
        """Compute how many months the emergency fund lasts.

        Parameters
        ----------
        fund_balance : float
            Starting fund balance.
        monthly_draw : float
            Monthly withdrawal amount.
        fund_yield : float, optional
            Annual yield on the fund. Default is 0.0.

        Returns
        -------
        float
            Number of months the fund can sustain withdrawals.
        """
        if monthly_draw <= 0 or monthly_draw <= fund_balance * fund_yield / 12.0:
            # Yield covers the draw: the balance never declines.
            return float("inf")
        schedule = EmergencyFund.drawdown_schedule(fund_balance, monthly_draw, fund_yield)
        return float(len(schedule))

    @staticmethod
    def replenishment_schedule(
        current_balance: float,
        target_balance: float,
        monthly_contribution: float,
        fund_yield: float = 0.0,
    ) -> dict:
        """Compute the timeline to rebuild the emergency fund after a drawdown.

        Parameters
        ----------
        current_balance : float
            Current fund balance after drawdown.
        target_balance : float
            Full emergency fund target.
        monthly_contribution : float
            Monthly amount allocated to replenishment.
        fund_yield : float, optional
            Annual yield earned during replenishment. Default is 0.0.

        Returns
        -------
        dict
            Keys: 'shortfall', 'months_to_rebuild', 'total_contributed',
            'interest_earned'.
        """
        shortfall = target_balance - current_balance
        if shortfall <= 0:
            return {
                "shortfall": 0.0,
                "months_to_rebuild": 0,
                "total_contributed": 0.0,
                "interest_earned": 0.0,
            }

        if monthly_contribution <= 0:
            return {
                "shortfall": round(shortfall, 2),
                "months_to_rebuild": float("inf"),
                "total_contributed": 0.0,
                "interest_earned": 0.0,
            }

        r = fund_yield / 12.0
        balance = current_balance
        total_contributed = 0.0
        total_interest = 0.0
        months = 0

        while balance < target_balance - 0.005:
            months += 1
            interest = balance * r
            total_interest += interest
            balance += interest + monthly_contribution
            total_contributed += monthly_contribution
            if months > 1200:  # safety limit
                break

        return {
            "shortfall": round(shortfall, 2),
            "months_to_rebuild": months,
            "total_contributed": round(total_contributed, 2),
            "interest_earned": round(total_interest, 2),
        }

    @staticmethod
    def variable_income_buffer(
        monthly_incomes: np.ndarray, monthly_essentials: float
    ) -> dict:
        """Analyze variable income and recommend a smoothing buffer.

        Parameters
        ----------
        monthly_incomes : np.ndarray
            Array of monthly income values over a historical period.
        monthly_essentials : float
            Monthly essential expenses.

        Returns
        -------
        dict
            Keys: 'average_income', 'min_income', 'max_income',
            'income_volatility', 'months_below_expenses',
            'recommended_buffer' (2-3 months of essentials).
        """
        incomes = np.asarray(monthly_incomes, dtype=np.float64)
        avg = float(np.mean(incomes))
        volatility = float(np.std(incomes, ddof=1)) if len(incomes) > 1 else 0.0
        below = int(np.sum(incomes < monthly_essentials))

        # Recommend buffer: 2 months if relatively stable, 3 if volatile
        cv = volatility / avg if avg > 0 else 0.0
        buffer_months = 3 if cv > 0.30 else 2
        buffer_amount = monthly_essentials * buffer_months

        return {
            "average_income": round(avg, 2),
            "min_income": round(float(np.min(incomes)), 2),
            "max_income": round(float(np.max(incomes)), 2),
            "income_volatility": round(volatility, 2),
            "coefficient_of_variation": round(cv, 4),
            "months_below_expenses": below,
            "recommended_buffer_months": buffer_months,
            "recommended_buffer": round(buffer_amount, 2),
        }


def _demo() -> None:
    # ----------------------------------------------------------------
    # Demo: Emergency fund computations
    # ----------------------------------------------------------------
    EF = EmergencyFund

    print("=" * 60)
    print("Emergency Fund Planning - Demo")
    print("=" * 60)

    # --- Example 1: Expense-Based Sizing ---
    print("\n--- Example 1: Expense-Based Fund Sizing ---")
    monthly_exp = 4500
    min_mo, rec_mo = EF.recommended_months(dual_income=True, stable_employment=True)
    fund_min = EF.expense_based_fund(monthly_exp, min_mo)
    fund_rec = EF.expense_based_fund(monthly_exp, rec_mo)
    print(f"  Monthly essentials: ${monthly_exp:,.0f}")
    print(f"  Dual income, stable: {min_mo}-{rec_mo} months recommended")
    print(f"  Minimum fund: ${fund_min:,.0f}")
    print(f"  Recommended fund: ${fund_rec:,.0f}")

    # --- Example 2: Tiered Allocation ---
    print("\n--- Example 2: Tiered Allocation ---")
    total_fund = 27_000
    allocation = EF.tiered_allocation(total_fund, monthly_exp)
    for tier_name, tier_data in allocation.items():
        print(
            f"  {tier_name}: ${tier_data['amount']:,.2f} "
            f"({tier_data['months']:.1f} months) - {tier_data['vehicle']}"
        )

    # --- Example 3: Blended Yield ---
    print("\n--- Example 3: Blended Yield ---")
    amounts = [4500.0, 13500.0, 9000.0]
    yields = [0.0001, 0.045, 0.048]
    blended = EF.blended_yield(amounts, yields)
    print(f"  Tier amounts: {amounts}")
    print(f"  Tier yields:  {[f'{y:.2%}' for y in yields]}")
    print(f"  Blended yield: {blended:.4%}")
    print(f"  Annual earnings: ${total_fund * blended:,.2f}")

    # --- Example 4: Opportunity Cost ---
    print("\n--- Example 4: Opportunity Cost ---")
    opp_cost = EF.opportunity_cost(27_000, 0.04, 0.09)
    print(f"  Fund: $27K, cash yield: 4%, investment return: 9%")
    print(f"  Annual opportunity cost: ${opp_cost:,.2f}")
    print(f"  Think of this as the 'insurance premium' for liquidity")

    # --- Example 5: Drawdown Modeling ---
    print("\n--- Example 5: Drawdown Duration ---")
    duration = EF.drawdown_duration(27_000, 4_500, fund_yield=0.04)
    print(f"  $27K fund, $4.5K/mo withdrawals, 4% yield")
    print(f"  Fund lasts: {duration:.0f} months")

    schedule = EF.drawdown_schedule(27_000, 4_500, fund_yield=0.04)
    print(f"  {'Month':>5}  {'Withdrawal':>11}  {'Interest':>9}  {'Balance':>11}")
    for row in schedule:
        print(
            f"  {row['month']:5d}  ${row['withdrawal']:10,.2f}"
            f"  ${row['interest_earned']:8,.2f}  ${row['remaining_balance']:10,.2f}"
        )

    # --- Example 6: Replenishment ---
    print("\n--- Example 6: Replenishment Schedule ---")
    replenish = EF.replenishment_schedule(
        current_balance=10_000,
        target_balance=27_000,
        monthly_contribution=1_500,
        fund_yield=0.04,
    )
    print(f"  Balance: $10K, Target: $27K, Contributing: $1.5K/mo")
    print(f"  Shortfall: ${replenish['shortfall']:,.2f}")
    print(f"  Months to rebuild: {replenish['months_to_rebuild']}")
    print(f"  Total contributed: ${replenish['total_contributed']:,.2f}")
    print(f"  Interest earned:   ${replenish['interest_earned']:,.2f}")

    # --- Example 7: Variable Income Analysis ---
    print("\n--- Example 7: Variable Income Buffer ---")
    np.random.seed(42)
    # Simulate freelancer income: base $5K + variable $0-$10K
    incomes = 5000 + np.random.exponential(3000, size=24)
    analysis = EF.variable_income_buffer(incomes, monthly_essentials=5500)
    print(f"  Average income:      ${analysis['average_income']:,.2f}")
    print(f"  Min income:          ${analysis['min_income']:,.2f}")
    print(f"  Max income:          ${analysis['max_income']:,.2f}")
    print(f"  Income volatility:   ${analysis['income_volatility']:,.2f}")
    print(f"  Coeff. of variation: {analysis['coefficient_of_variation']:.4f}")
    print(f"  Months below expenses: {analysis['months_below_expenses']}")
    print(f"  Recommended buffer:  ${analysis['recommended_buffer']:,.2f} "
          f"({analysis['recommended_buffer_months']} months)")

    # --- Example 8: Single Income, Variable ---
    print("\n--- Example 8: Recommendations by Situation ---")
    situations = [
        ("Dual income, stable", dict(dual_income=True, stable_employment=True)),
        ("Single income, stable", dict(dual_income=False, stable_employment=True)),
        ("Single income, unstable", dict(dual_income=False, stable_employment=False)),
        ("Variable / self-employed", dict(dual_income=False, variable_income=True)),
        ("Niche / senior role", dict(dual_income=False, high_search_risk=True)),
    ]
    for label, kwargs in situations:
        lo, hi = EF.recommended_months(**kwargs)
        print(f"  {label:30s}: {lo}-{hi} months")

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

    # SKILL.md Example 1: dual-income sizing
    _check(failures, "Ex1 minimum fund (3 months)", EmergencyFund.expense_based_fund(4500, 3), 13500, 0)
    _check(failures, "Ex1 recommended fund (4 months)", EmergencyFund.expense_based_fund(4500, 4), 18000, 0)

    # SKILL.md Example 2: tiered allocation of $27,000
    alloc = EmergencyFund.tiered_allocation(27000, 4500)
    _check(failures, "Ex2 tier 1 amount", alloc["tier_1"]["amount"], 4500, 0)
    _check(failures, "Ex2 tier 2 amount", alloc["tier_2"]["amount"], 13500, 0)
    _check(failures, "Ex2 tier 3 amount", alloc["tier_3"]["amount"], 9000, 0)
    blended = EmergencyFund.blended_yield([4500.0, 13500.0, 9000.0], [0.0001, 0.045, 0.048])
    _check(failures, "Ex2 blended yield", blended, 0.038517, 1e-5)

    # Opportunity cost concept check
    _check(failures, "opportunity cost $27K at 5pp spread",
           EmergencyFund.opportunity_cost(27000, 0.04, 0.09), 1350.0, 1e-9)

    if failures:
        print(f"\n{len(failures)} check(s) FAILED: {', '.join(failures)}")
        sys.exit(1)
    print("\nAll checks passed.")

def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__.strip().splitlines()[2] if __doc__ else "",
        epilog=(
            "Provides: EmergencyFund. "
            "For programmatic use, import this module (emergency_fund) instead of running it. "
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
