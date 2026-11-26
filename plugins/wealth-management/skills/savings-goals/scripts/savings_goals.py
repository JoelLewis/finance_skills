# /// script
# dependencies = []
# requires-python = ">=3.11"
# ///
"""
Savings Goals
=============
Compute required savings rates, future value projections, time-to-goal,
inflation-adjusted targets, and multi-goal prioritization.

Part of Layer 6 (Personal Finance) in the finance skills framework.
"""

import argparse
import math
import sys


class SavingsGoals:
    """Savings goal computations: required savings, projections, and goal analysis.

    All methods are static — no instance state is required.
    """

    @staticmethod
    def required_monthly_savings(
        future_value: float,
        annual_rate: float,
        years: int,
        current_savings: float = 0.0,
    ) -> float:
        """Compute the required monthly savings to reach a future goal.

        Uses the sinking fund formula: PMT = FV * r / [(1+r)^n - 1],
        adjusted for existing savings that will compound.

        Parameters
        ----------
        future_value : float
            Target amount in dollars (nominal or real, depending on rate used).
        annual_rate : float
            Expected annual return as a decimal (e.g., 0.07 for 7%).
        years : int
            Number of years until the goal.
        current_savings : float, optional
            Amount already saved toward this goal. Default is 0.0.

        Returns
        -------
        float
            Required monthly savings amount.
        """
        if years <= 0:
            return max(future_value - current_savings, 0.0)

        r = annual_rate / 12.0
        n = years * 12

        # Future value of current savings
        if current_savings > 0:
            fv_existing = current_savings * (1.0 + r) ** n
        else:
            fv_existing = 0.0

        remaining_fv = future_value - fv_existing
        if remaining_fv <= 0:
            return 0.0

        if r == 0:
            return remaining_fv / n

        # Sinking fund formula: PMT = FV * r / [(1+r)^n - 1]
        # expm1(n*log1p(r)) == (1+r)^n - 1, without cancellation near r = 0
        factor = math.expm1(n * math.log1p(r))
        return remaining_fv * r / factor

    @staticmethod
    def future_value_with_contributions(
        current_savings: float,
        monthly_contribution: float,
        annual_rate: float,
        years: int,
    ) -> float:
        """Project the future value of current savings plus regular contributions.

        FV = PV(1+r)^n + PMT * [(1+r)^n - 1] / r

        Parameters
        ----------
        current_savings : float
            Amount currently saved.
        monthly_contribution : float
            Regular monthly contribution.
        annual_rate : float
            Expected annual return as a decimal.
        years : int
            Number of years to project.

        Returns
        -------
        float
            Projected future value.
        """
        r = annual_rate / 12.0
        n = years * 12

        fv_lump = current_savings * (1.0 + r) ** n

        if r == 0:
            fv_annuity = monthly_contribution * n
        else:
            # expm1(n*log1p(r)) == (1+r)^n - 1, without cancellation near r = 0
            fv_annuity = monthly_contribution * math.expm1(n * math.log1p(r)) / r

        return fv_lump + fv_annuity

    @staticmethod
    def time_to_goal(
        future_value: float,
        monthly_contribution: float,
        annual_rate: float,
        current_savings: float = 0.0,
    ) -> float:
        """Compute the number of years to reach a savings goal.

        Solves n = ln(FV*r/PMT + 1) / ln(1+r), adjusted for existing savings.

        Parameters
        ----------
        future_value : float
            Target amount in dollars.
        monthly_contribution : float
            Regular monthly savings amount.
        annual_rate : float
            Expected annual return as a decimal.
        current_savings : float, optional
            Amount already saved. Default is 0.0.

        Returns
        -------
        float
            Years until the goal is reached. Returns inf if contributions
            are insufficient to ever reach the goal.
        """
        if current_savings >= future_value:
            return 0.0

        r = annual_rate / 12.0

        if r == 0:
            if monthly_contribution <= 0:
                return float("inf")
            months = (future_value - current_savings) / monthly_contribution
            return months / 12.0

        # We need to solve: PV*(1+r)^n + PMT*[(1+r)^n - 1]/r = FV
        # Let x = (1+r)^n:  PV*x + PMT*(x-1)/r = FV
        #   PV*x + PMT*x/r - PMT/r = FV
        #   x*(PV + PMT/r) = FV + PMT/r
        #   x = (FV + PMT/r) / (PV + PMT/r)
        # Written as x = 1 + y with y = (FV - PV) * r / (PV * r + PMT), so
        # log1p keeps full precision near r = 0. With r < 0 the goal can
        # still be reachable (the balance approaches PMT/|r|).
        denominator = current_savings * r + monthly_contribution
        if denominator == 0:
            return float("inf")
        y = (future_value - current_savings) * r / denominator
        if y <= -1.0:
            return float("inf")

        n_months = math.log1p(y) / math.log1p(r)
        if not n_months > 0:
            # Current savings are below the goal, so a non-positive solution
            # means the balance never reaches it.
            return float("inf")
        return n_months / 12.0

    @staticmethod
    def inflation_adjusted_goal(
        todays_cost: float, inflation_rate: float, years: int
    ) -> float:
        """Adjust a goal amount for inflation.

        FV_nominal = FV_today * (1 + inflation)^years

        Parameters
        ----------
        todays_cost : float
            Cost in today's dollars.
        inflation_rate : float
            Expected annual inflation as a decimal (e.g., 0.03 for 3%).
        years : int
            Years until the expense occurs.

        Returns
        -------
        float
            Inflation-adjusted (nominal) cost.
        """
        return todays_cost * (1.0 + inflation_rate) ** years

    @staticmethod
    def real_rate_of_return(nominal_rate: float, inflation_rate: float) -> float:
        """Compute the real (inflation-adjusted) rate of return.

        real_rate = (1 + nominal) / (1 + inflation) - 1

        Parameters
        ----------
        nominal_rate : float
            Nominal annual return as a decimal.
        inflation_rate : float
            Annual inflation rate as a decimal.

        Returns
        -------
        float
            Real rate of return as a decimal.
        """
        return (1.0 + nominal_rate) / (1.0 + inflation_rate) - 1.0

    @staticmethod
    def retirement_target(
        annual_spending: float, safe_withdrawal_rate: float = 0.04
    ) -> float:
        """Compute the target nest egg for retirement.

        Nest egg = annual spending / safe withdrawal rate

        Parameters
        ----------
        annual_spending : float
            Desired annual spending in retirement.
        safe_withdrawal_rate : float, optional
            Safe withdrawal rate as a decimal. Default is 0.04 (4%).

        Returns
        -------
        float
            Required retirement savings target.
        """
        if safe_withdrawal_rate <= 0:
            return float("inf")
        return annual_spending / safe_withdrawal_rate

    @staticmethod
    def savings_rate(total_savings: float, gross_income: float) -> float:
        """Compute the personal savings rate.

        Savings rate = total savings / gross income

        Parameters
        ----------
        total_savings : float
            Total amount saved in the period.
        gross_income : float
            Gross income for the period.

        Returns
        -------
        float
            Savings rate as a decimal.
        """
        if gross_income <= 0:
            return 0.0
        return total_savings / gross_income

    @staticmethod
    def contribution_shortfall(
        future_value: float,
        annual_rate: float,
        years: int,
        current_savings: float,
        current_monthly: float,
    ) -> dict:
        """Assess whether current contributions are on track for a goal.

        Parameters
        ----------
        future_value : float
            Target goal amount.
        annual_rate : float
            Expected annual return as a decimal.
        years : int
            Years until the goal.
        current_savings : float
            Amount already saved.
        current_monthly : float
            Current monthly contribution.

        Returns
        -------
        dict
            Keys: 'projected_value', 'target', 'surplus_or_shortfall',
            'required_monthly', 'additional_monthly_needed', 'on_track' (bool).
        """
        projected = SavingsGoals.future_value_with_contributions(
            current_savings, current_monthly, annual_rate, years
        )
        required = SavingsGoals.required_monthly_savings(
            future_value, annual_rate, years, current_savings
        )
        additional = max(required - current_monthly, 0.0)

        return {
            "projected_value": round(projected, 2),
            "target": round(future_value, 2),
            "surplus_or_shortfall": round(projected - future_value, 2),
            "required_monthly": round(required, 2),
            "additional_monthly_needed": round(additional, 2),
            "on_track": projected >= future_value,
        }

    @staticmethod
    def education_funding_plan(
        annual_cost_today: float,
        years_until_enrollment: int,
        years_of_education: int = 4,
        education_inflation: float = 0.05,
        investment_return: float = 0.07,
        current_529_balance: float = 0.0,
    ) -> dict:
        """Plan education funding with inflation-adjusted costs.

        Parameters
        ----------
        annual_cost_today : float
            Current annual cost of education.
        years_until_enrollment : int
            Years until the student begins education.
        years_of_education : int, optional
            Duration of education in years. Default is 4.
        education_inflation : float, optional
            Annual education cost inflation. Default is 0.05 (5%).
        investment_return : float, optional
            Expected annual return on 529 investments. Default is 0.07 (7%).
        current_529_balance : float, optional
            Current 529 plan balance. Default is 0.0.

        Returns
        -------
        dict
            Keys: 'total_cost_nominal', 'cost_by_year' (list),
            'required_monthly_savings', 'current_balance_fv'.
        """
        # Compute inflated cost for each year of education
        cost_by_year: list[float] = []
        total_cost = 0.0
        for i in range(years_of_education):
            year_number = years_until_enrollment + i
            inflated_cost = annual_cost_today * (1.0 + education_inflation) ** year_number
            cost_by_year.append(round(inflated_cost, 2))
            total_cost += inflated_cost

        # For simplicity, compute required savings to accumulate the total
        # by enrollment (conservative: need the full amount at enrollment)
        total_pv_at_enrollment = 0.0
        r_monthly = investment_return / 12.0
        for i in range(years_of_education):
            # Discount each year's cost back to enrollment date
            months_after_enrollment = i * 12
            if r_monthly > 0:
                pv_factor = 1.0 / (1.0 + r_monthly) ** months_after_enrollment
            else:
                pv_factor = 1.0
            total_pv_at_enrollment += cost_by_year[i] * pv_factor

        required_monthly = SavingsGoals.required_monthly_savings(
            total_pv_at_enrollment,
            investment_return,
            years_until_enrollment,
            current_529_balance,
        )

        fv_current = current_529_balance * (1.0 + r_monthly) ** (years_until_enrollment * 12)

        return {
            "total_cost_nominal": round(total_cost, 2),
            "cost_by_year": cost_by_year,
            "total_needed_at_enrollment": round(total_pv_at_enrollment, 2),
            "required_monthly_savings": round(required_monthly, 2),
            "current_balance_fv": round(fv_current, 2),
        }


def _demo() -> None:
    # ----------------------------------------------------------------
    # Demo: Savings goals computations
    # ----------------------------------------------------------------
    SG = SavingsGoals

    print("=" * 60)
    print("Savings Goals - Demo")
    print("=" * 60)

    # --- Example 1: College Savings (529) ---
    print("\n--- Example 1: College Savings (529) ---")
    monthly = SG.required_monthly_savings(200_000, 0.07, 18, current_savings=0)
    print(f"  Goal: $200,000 in 18 years @ 7% annual return")
    print(f"  Required monthly savings: ${monthly:,.2f}")

    # Verify with future value projection
    fv = SG.future_value_with_contributions(0, monthly, 0.07, 18)
    print(f"  Verification (FV of contributions): ${fv:,.2f}")

    # --- Example 2: Retirement Accumulation ---
    print("\n--- Example 2: Retirement Accumulation ---")
    target = SG.retirement_target(80_000, 0.04)
    print(f"  $80K/yr spending, 4% SWR -> target: ${target:,.0f}")
    monthly_ret = SG.required_monthly_savings(target, 0.08, 35, current_savings=50_000)
    print(f"  Age 30, $50K saved, 35 years @ 8%: ${monthly_ret:,.2f}/mo needed")
    with_match = monthly_ret - 200
    print(f"  With $200/mo employer match: ${with_match:,.2f}/mo personal")

    # --- Example 3: Time to Goal ---
    print("\n--- Example 3: Time to Goal ---")
    years = SG.time_to_goal(100_000, 500, 0.06, current_savings=10_000)
    print(f"  $100K goal, saving $500/mo @ 6%, starting with $10K")
    print(f"  Time to goal: {years:.1f} years ({years * 12:.0f} months)")

    # --- Example 4: Inflation Adjustment ---
    print("\n--- Example 4: Inflation-Adjusted Goal ---")
    today_cost = 25_000  # annual college cost today
    future_cost = SG.inflation_adjusted_goal(today_cost, 0.05, 18)
    print(f"  $25K/yr college cost today, 5% education inflation, 18 years")
    print(f"  Future annual cost: ${future_cost:,.2f}")
    total_4yr = sum(
        SG.inflation_adjusted_goal(today_cost, 0.05, 18 + i) for i in range(4)
    )
    print(f"  Total 4-year cost: ${total_4yr:,.2f}")

    # --- Example 5: Shortfall Analysis ---
    print("\n--- Example 5: Contribution Shortfall Analysis ---")
    analysis = SG.contribution_shortfall(
        future_value=500_000,
        annual_rate=0.07,
        years=20,
        current_savings=30_000,
        current_monthly=400,
    )
    print(f"  Goal: $500K in 20 years @ 7%")
    print(f"  Currently: $30K saved, contributing $400/mo")
    print(f"  Projected value:     ${analysis['projected_value']:,.2f}")
    print(f"  Target:              ${analysis['target']:,.2f}")
    print(f"  Surplus/shortfall:   ${analysis['surplus_or_shortfall']:,.2f}")
    print(f"  Required monthly:    ${analysis['required_monthly']:,.2f}")
    print(f"  Additional needed:   ${analysis['additional_monthly_needed']:,.2f}")
    print(f"  On track:            {analysis['on_track']}")

    # --- Example 6: Education Funding Plan ---
    print("\n--- Example 6: Education Funding Plan ---")
    plan = SG.education_funding_plan(
        annual_cost_today=25_000,
        years_until_enrollment=18,
        years_of_education=4,
        education_inflation=0.05,
        investment_return=0.07,
        current_529_balance=5_000,
    )
    print(f"  Annual cost today: $25K, enrollment in 18 years")
    print(f"  Total nominal cost: ${plan['total_cost_nominal']:,.2f}")
    print("  Year-by-year costs:")
    for i, cost in enumerate(plan["cost_by_year"], 1):
        print(f"    Year {i}: ${cost:,.2f}")
    print(f"  Needed at enrollment: ${plan['total_needed_at_enrollment']:,.2f}")
    print(f"  Current $5K grows to: ${plan['current_balance_fv']:,.2f}")
    print(f"  Required monthly:     ${plan['required_monthly_savings']:,.2f}")

    # --- Example 7: Savings Rate ---
    print("\n--- Example 7: Savings Rate ---")
    sr = SG.savings_rate(18_000, 120_000)
    print(f"  $18K saved on $120K gross income -> savings rate: {sr:.1%}")

    # --- Example 8: Real Rate of Return ---
    print("\n--- Example 8: Real Rate of Return ---")
    real = SG.real_rate_of_return(0.08, 0.03)
    print(f"  8% nominal, 3% inflation -> real return: {real:.2%}")

    print("\n" + "=" * 60)
    print("Demo complete.")
    print("=" * 60)


def _verify() -> int:
    """Assert that demo computations match the SKILL.md worked examples."""
    SG = SavingsGoals
    failures: list[str] = []

    def check(label: str, actual: float, expected: float, rel_tol: float = 1e-3) -> None:
        ok = math.isclose(actual, expected, rel_tol=rel_tol)
        print(f"  {'PASS' if ok else 'FAIL'}: {label}: got {actual:,.2f}, expected {expected:,.2f}")
        if not ok:
            failures.append(label)

    print("Verifying against SKILL.md worked examples...")

    # Example 1: $200K in 18 years @ 7% from $0 -> $464.34/month
    pmt_529 = SG.required_monthly_savings(200_000, 0.07, 18, current_savings=0)
    check("Ex1 required monthly savings ($464.34)", pmt_529, 464.34)
    fv_check = SG.future_value_with_contributions(0, pmt_529, 0.07, 18)
    check("Ex1 FV of contributions ($200,000)", fv_check, 200_000.0, rel_tol=1e-6)

    # Example 2: $80K/yr spending @ 4% SWR -> $2M target;
    # age 30, $50K saved, 35 years @ 8% -> ~$517/month ($317 after $200 match)
    target = SG.retirement_target(80_000, 0.04)
    check("Ex2 retirement target ($2,000,000)", target, 2_000_000.0, rel_tol=1e-9)
    pmt_ret = SG.required_monthly_savings(target, 0.08, 35, current_savings=50_000)
    check("Ex2 required monthly savings ($517)", pmt_ret, 517.0)
    check("Ex2 personal after $200 match ($317)", pmt_ret - 200, 317.0, rel_tol=2e-3)

    if failures:
        print(f"FAIL: {len(failures)} check(s) did not match SKILL.md.")
        return 1
    print("PASS: all checks match SKILL.md worked examples.")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Savings goals reference implementation: required monthly savings, "
            "future value projections, time-to-goal, inflation adjustment, "
            "retirement targets, shortfall analysis, and education funding plans."
        ),
        epilog=(
            "Main class:\n"
            "  SavingsGoals -- static methods: required_monthly_savings,\n"
            "    future_value_with_contributions, time_to_goal,\n"
            "    inflation_adjusted_goal, real_rate_of_return, retirement_target,\n"
            "    savings_rate, contribution_shortfall, education_funding_plan\n"
            "\n"
            "This file is primarily meant to be imported as a module:\n"
            "  from savings_goals import SavingsGoals\n"
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
