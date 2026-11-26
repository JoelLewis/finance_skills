# /// script
# dependencies = ["numpy"]
# requires-python = ">=3.11"
# ///
"""
Liquidity Management
====================
Compute liquidity ratios, cash flow projections, liquidity tier analysis,
net liquid assets, CD/bond ladder construction, income smoothing, and
cash runway estimation.

Part of Layer 6 (Personal Finance) in the finance skills framework.
"""

import argparse
import math
import sys

import numpy as np


class LiquidityManagement:
    """Liquidity planning and cash flow management computations.

    All methods are static — no instance state is required.
    """

    @staticmethod
    def liquidity_ratio(liquid_assets: float, monthly_expenses: float) -> float:
        """Compute the liquidity ratio.

        Liquidity ratio = liquid assets / monthly expenses

        Parameters
        ----------
        liquid_assets : float
            Total liquid assets (cash, HYSA, money market, T-bills).
        monthly_expenses : float
            Average monthly expenses.

        Returns
        -------
        float
            Liquidity ratio. Target >= 3-6 for personal finance.
        """
        if monthly_expenses <= 0:
            return float("inf")
        return liquid_assets / monthly_expenses

    @staticmethod
    def cash_reserve_ratio(
        cash_and_near_cash: float, total_portfolio: float
    ) -> float:
        """Compute the cash reserve ratio.

        Cash reserve ratio = (cash + near-cash) / total portfolio

        Parameters
        ----------
        cash_and_near_cash : float
            Cash and highly liquid near-cash assets.
        total_portfolio : float
            Total investable portfolio value.

        Returns
        -------
        float
            Cash reserve ratio as a decimal.
        """
        if total_portfolio <= 0:
            return float("inf") if cash_and_near_cash > 0 else 0.0
        return cash_and_near_cash / total_portfolio

    @staticmethod
    def current_ratio(current_assets: float, current_liabilities: float) -> float:
        """Compute the current ratio (business liquidity metric).

        Current ratio = current assets / current liabilities

        Parameters
        ----------
        current_assets : float
            Total current assets (due within one year).
        current_liabilities : float
            Total current liabilities (due within one year).

        Returns
        -------
        float
            Current ratio. Target > 1.5 for healthy businesses.
        """
        if current_liabilities <= 0:
            return float("inf") if current_assets > 0 else 0.0
        return current_assets / current_liabilities

    @staticmethod
    def quick_ratio(
        current_assets: float, inventory: float, current_liabilities: float
    ) -> float:
        """Compute the quick (acid-test) ratio.

        Quick ratio = (current assets - inventory) / current liabilities

        Parameters
        ----------
        current_assets : float
            Total current assets.
        inventory : float
            Inventory value (excluded from quick assets).
        current_liabilities : float
            Total current liabilities.

        Returns
        -------
        float
            Quick ratio. More conservative than current ratio.
        """
        if current_liabilities <= 0:
            return float("inf") if (current_assets - inventory) > 0 else 0.0
        return (current_assets - inventory) / current_liabilities

    @staticmethod
    def net_liquid_assets(
        liquid_assets: float, short_term_liabilities: float
    ) -> float:
        """Compute net liquid assets.

        Net liquid assets = liquid assets - short-term liabilities

        Parameters
        ----------
        liquid_assets : float
            Total liquid assets.
        short_term_liabilities : float
            Liabilities due within the liquidity horizon.

        Returns
        -------
        float
            Net liquid assets in dollars.
        """
        return liquid_assets - short_term_liabilities

    @staticmethod
    def cash_flow_projection(
        monthly_income: np.ndarray,
        monthly_fixed_expenses: float,
        monthly_variable_expenses: np.ndarray,
        periodic_expenses: np.ndarray | None = None,
        starting_cash: float = 0.0,
    ) -> np.ndarray:
        """Project monthly cash flows and cumulative cash balance.

        Parameters
        ----------
        monthly_income : np.ndarray
            Array of monthly income amounts for each projected month.
        monthly_fixed_expenses : float
            Fixed monthly expenses (constant each month).
        monthly_variable_expenses : np.ndarray
            Array of variable expenses for each projected month.
        periodic_expenses : np.ndarray or None, optional
            Array of one-time or periodic expenses per month (e.g.,
            quarterly taxes, annual premiums). Use 0 for months with none.
            Default is None (no periodic expenses).
        starting_cash : float, optional
            Starting cash balance. Default is 0.0.

        Returns
        -------
        np.ndarray
            Structured array with columns: month, income, total_expenses,
            net_cash_flow, cumulative_balance.
        """
        n_months = len(monthly_income)
        income = np.asarray(monthly_income, dtype=np.float64)
        variable = np.asarray(monthly_variable_expenses, dtype=np.float64)

        if periodic_expenses is not None:
            periodic = np.asarray(periodic_expenses, dtype=np.float64)
        else:
            periodic = np.zeros(n_months, dtype=np.float64)

        total_expenses = monthly_fixed_expenses + variable + periodic
        net_flow = income - total_expenses
        cumulative = starting_cash + np.cumsum(net_flow)

        dtype = np.dtype(
            [
                ("month", np.int32),
                ("income", np.float64),
                ("total_expenses", np.float64),
                ("net_cash_flow", np.float64),
                ("cumulative_balance", np.float64),
            ]
        )
        rows = [
            (i + 1, income[i], total_expenses[i], net_flow[i], cumulative[i])
            for i in range(n_months)
        ]
        return np.array(rows, dtype=dtype)

    @staticmethod
    def cash_runway(
        liquid_assets: float,
        monthly_burn: float,
        cash_yield: float = 0.0,
    ) -> float:
        """Estimate how many months liquid assets can cover expenses.

        Parameters
        ----------
        liquid_assets : float
            Total liquid assets available.
        monthly_burn : float
            Monthly net cash outflow (expenses minus any income).
        cash_yield : float, optional
            Annual yield on liquid assets. Default is 0.0.

        Returns
        -------
        float
            Months of runway. Returns inf if burn rate is zero or negative.
        """
        if monthly_burn <= 0:
            return float("inf")

        r = cash_yield / 12.0
        if r <= 0:
            return liquid_assets / monthly_burn

        # Solve: balance * (1+r)^n - PMT * [(1+r)^n - 1] / r = 0
        # where PMT = monthly_burn (withdrawal)
        # (1+r)^n * (balance - PMT/r) = -PMT/r
        # If balance * r < PMT, fund depletes
        if liquid_assets * r >= monthly_burn:
            return float("inf")  # interest covers withdrawals

        # n = ln(PMT / (PMT - balance*r)) / ln(1+r)
        import math
        # log1p avoids precision loss (and division by zero) near r = 0
        n = -math.log1p(-liquid_assets * r / monthly_burn) / math.log1p(r)
        return n

    @staticmethod
    def liquidity_tier_analysis(
        tiers: list[dict],
    ) -> dict:
        """Analyze liquidity across asset tiers.

        Parameters
        ----------
        tiers : list[dict]
            Each dict has keys: 'name' (str), 'amount' (float),
            'yield_rate' (float, annual decimal), 'access_days' (int).

        Returns
        -------
        dict
            Keys: 'total_liquid_assets', 'blended_yield',
            'weighted_avg_access_days', 'tier_breakdown' (list of dicts
            with added 'pct_of_total' field).
        """
        total = sum(t["amount"] for t in tiers)
        if total <= 0:
            return {
                "total_liquid_assets": 0.0,
                "blended_yield": 0.0,
                "weighted_avg_access_days": 0.0,
                "tier_breakdown": [],
            }

        blended_yield = sum(t["amount"] * t["yield_rate"] for t in tiers) / total
        weighted_days = sum(t["amount"] * t["access_days"] for t in tiers) / total

        breakdown = []
        for t in tiers:
            breakdown.append(
                {
                    "name": t["name"],
                    "amount": t["amount"],
                    "yield_rate": t["yield_rate"],
                    "access_days": t["access_days"],
                    "pct_of_total": round(t["amount"] / total, 4),
                }
            )

        return {
            "total_liquid_assets": round(total, 2),
            "blended_yield": round(blended_yield, 6),
            "weighted_avg_access_days": round(weighted_days, 1),
            "tier_breakdown": breakdown,
        }

    @staticmethod
    def cd_ladder(
        total_amount: float,
        num_rungs: int,
        rung_yields: list[float] | None = None,
        maturity_interval_months: int = 2,
    ) -> dict:
        """Construct a CD ladder and compute blended yield.

        Parameters
        ----------
        total_amount : float
            Total amount to deploy across the ladder.
        num_rungs : int
            Number of CDs in the ladder.
        rung_yields : list[float] or None, optional
            Annual yield for each rung as a decimal. If None, yields are
            estimated assuming a flat term structure.
        maturity_interval_months : int, optional
            Months between each rung maturity. Default is 2.

        Returns
        -------
        dict
            Keys: 'rungs' (list of dicts with maturity_month, amount, yield),
            'blended_yield', 'liquidity_interval_months'.
        """
        per_rung = total_amount / num_rungs
        if rung_yields is None:
            # Default: slight upward slope
            base = 0.042
            slope = 0.001
            rung_yields = [base + slope * i for i in range(num_rungs)]

        rungs = []
        for i in range(num_rungs):
            rungs.append(
                {
                    "rung": i + 1,
                    "maturity_month": (i + 1) * maturity_interval_months,
                    "amount": round(per_rung, 2),
                    "yield_rate": round(rung_yields[i], 6),
                }
            )

        blended = sum(y for y in rung_yields) / num_rungs

        return {
            "rungs": rungs,
            "blended_yield": round(blended, 6),
            "liquidity_interval_months": maturity_interval_months,
            "total_amount": round(total_amount, 2),
        }

    @staticmethod
    def income_smoothing(
        monthly_incomes: np.ndarray,
        monthly_essentials: float,
    ) -> dict:
        """Analyze variable income and compute smoothing metrics.

        Parameters
        ----------
        monthly_incomes : np.ndarray
            Historical monthly income values (12-24 months recommended).
        monthly_essentials : float
            Monthly essential expenses (base budget).

        Returns
        -------
        dict
            Keys: 'average_income', 'base_budget', 'average_surplus',
            'smoothing_reserve_target', 'deficit_months',
            'surplus_months'.
        """
        incomes = np.asarray(monthly_incomes, dtype=np.float64)
        avg_income = float(np.mean(incomes))
        surplus = avg_income - monthly_essentials

        deficit_count = int(np.sum(incomes < monthly_essentials))
        surplus_count = int(np.sum(incomes >= monthly_essentials))

        # Smoothing reserve: 3 months of essentials
        reserve_target = monthly_essentials * 3.0

        return {
            "average_income": round(avg_income, 2),
            "base_budget": round(monthly_essentials, 2),
            "average_surplus": round(surplus, 2),
            "smoothing_reserve_target": round(reserve_target, 2),
            "deficit_months": deficit_count,
            "surplus_months": surplus_count,
            "total_months_analyzed": len(incomes),
        }

    @staticmethod
    def cd_breakeven_penalty(
        cd_rate: float,
        savings_rate: float,
        penalty_months: int,
    ) -> float:
        """Compute how long a CD must be held to beat savings after penalty.

        If you break a CD early, you lose N months of interest. This computes
        the minimum holding period (in months) where the CD net of penalty
        beats a savings account.

        Parameters
        ----------
        cd_rate : float
            CD annual rate as a decimal.
        savings_rate : float
            Alternative savings account annual rate as a decimal.
        penalty_months : int
            Early withdrawal penalty expressed as months of CD interest.

        Returns
        -------
        float
            Minimum months to hold the CD for it to be worthwhile.
            Returns inf if CD rate is not higher than savings rate.
        """
        rate_diff = cd_rate - savings_rate
        if rate_diff <= 0:
            return float("inf")
        # Penalty = penalty_months * (cd_rate / 12) * principal
        # Need: months * (cd_rate / 12) - penalty_months * (cd_rate / 12) > months * (savings_rate / 12)
        # months * cd_rate - penalty_months * cd_rate > months * savings_rate
        # months * (cd_rate - savings_rate) > penalty_months * cd_rate
        # months > penalty_months * cd_rate / (cd_rate - savings_rate)
        return penalty_months * cd_rate / rate_diff


def _demo() -> None:
    # ----------------------------------------------------------------
    # Demo: Liquidity management computations
    # ----------------------------------------------------------------
    LM = LiquidityManagement

    print("=" * 60)
    print("Liquidity Management - Demo")
    print("=" * 60)

    # --- Example 1: Liquidity Ratios ---
    print("\n--- Example 1: Liquidity Ratios ---")
    liquid = 45_000
    monthly_exp = 7_500
    lr = LM.liquidity_ratio(liquid, monthly_exp)
    print(f"  Liquid assets: ${liquid:,.0f}")
    print(f"  Monthly expenses: ${monthly_exp:,.0f}")
    print(f"  Liquidity ratio: {lr:.1f} months ({'Adequate' if lr >= 3 else 'Low'})")

    crr = LM.cash_reserve_ratio(liquid, 500_000)
    print(f"  Cash reserve ratio: {crr:.1%} of $500K portfolio")

    # --- Example 2: Cash Flow Projection ---
    print("\n--- Example 2: 12-Month Cash Flow Projection ---")
    np.random.seed(42)
    income = np.full(12, 8000.0)  # stable salary
    variable_exp = np.random.normal(2000, 300, 12)
    # Quarterly estimated taxes in months 3, 6, 9, 12
    periodic = np.zeros(12)
    periodic[[2, 5, 8, 11]] = 3000.0
    projection = LM.cash_flow_projection(
        monthly_income=income,
        monthly_fixed_expenses=4000.0,
        monthly_variable_expenses=variable_exp,
        periodic_expenses=periodic,
        starting_cash=10_000,
    )
    print(f"  {'Month':>5}  {'Income':>8}  {'Expenses':>10}  {'Net Flow':>10}  {'Balance':>10}")
    for row in projection:
        print(
            f"  {row['month']:5d}  ${row['income']:7,.0f}"
            f"  ${row['total_expenses']:9,.0f}  ${row['net_cash_flow']:9,.0f}"
            f"  ${row['cumulative_balance']:9,.0f}"
        )
    min_balance = float(np.min(projection["cumulative_balance"]))
    print(f"  Minimum balance: ${min_balance:,.0f}")
    print(f"  {'WARNING: Cash goes negative!' if min_balance < 0 else 'Cash stays positive throughout.'}")

    # --- Example 3: Cash Runway ---
    print("\n--- Example 3: Cash Runway ---")
    runway = LM.cash_runway(50_000, 5_000, cash_yield=0.04)
    print(f"  $50K liquid, $5K/mo burn, 4% yield")
    print(f"  Runway: {runway:.1f} months ({runway/12:.1f} years)")

    runway_no_yield = LM.cash_runway(50_000, 5_000, cash_yield=0.0)
    print(f"  Without yield: {runway_no_yield:.1f} months")

    # --- Example 4: Liquidity Tier Analysis ---
    print("\n--- Example 4: Liquidity Tier Analysis ---")
    tiers = [
        {"name": "Checking", "amount": 5000, "yield_rate": 0.001, "access_days": 0},
        {"name": "HYSA", "amount": 25000, "yield_rate": 0.045, "access_days": 1},
        {"name": "Money Market", "amount": 15000, "yield_rate": 0.043, "access_days": 1},
        {"name": "T-Bill Ladder", "amount": 30000, "yield_rate": 0.048, "access_days": 7},
        {"name": "CD Ladder", "amount": 20000, "yield_rate": 0.050, "access_days": 30},
    ]
    analysis = LM.liquidity_tier_analysis(tiers)
    print(f"  Total liquid assets: ${analysis['total_liquid_assets']:,.2f}")
    print(f"  Blended yield: {analysis['blended_yield']:.4%}")
    print(f"  Weighted avg access: {analysis['weighted_avg_access_days']:.1f} days")
    print(f"  {'Tier':<15}  {'Amount':>10}  {'Yield':>7}  {'Days':>5}  {'% Total':>8}")
    for t in analysis["tier_breakdown"]:
        print(
            f"  {t['name']:<15}  ${t['amount']:>9,.0f}"
            f"  {t['yield_rate']:>6.2%}  {t['access_days']:>5d}"
            f"  {t['pct_of_total']:>7.1%}"
        )

    # --- Example 5: CD Ladder ---
    print("\n--- Example 5: CD Ladder Construction ---")
    ladder = LM.cd_ladder(
        total_amount=60_000,
        num_rungs=6,
        rung_yields=[0.042, 0.044, 0.045, 0.046, 0.047, 0.048],
        maturity_interval_months=2,
    )
    print(f"  Total: ${ladder['total_amount']:,.0f}, Liquidity every {ladder['liquidity_interval_months']} months")
    print(f"  Blended yield: {ladder['blended_yield']:.4%}")
    for rung in ladder["rungs"]:
        print(
            f"    Rung {rung['rung']}: ${rung['amount']:,.2f} "
            f"matures month {rung['maturity_month']:2d} @ {rung['yield_rate']:.2%}"
        )

    # --- Example 6: Income Smoothing ---
    print("\n--- Example 6: Variable Income Smoothing ---")
    np.random.seed(99)
    freelance_income = 5000 + np.random.exponential(3000, size=24)
    smoothing = LM.income_smoothing(freelance_income, monthly_essentials=5500)
    print(f"  Average income:       ${smoothing['average_income']:,.2f}")
    print(f"  Base budget:          ${smoothing['base_budget']:,.2f}")
    print(f"  Average surplus:      ${smoothing['average_surplus']:,.2f}")
    print(f"  Smoothing reserve:    ${smoothing['smoothing_reserve_target']:,.2f}")
    print(f"  Deficit months:       {smoothing['deficit_months']}/{smoothing['total_months_analyzed']}")
    print(f"  Surplus months:       {smoothing['surplus_months']}/{smoothing['total_months_analyzed']}")

    # --- Example 7: CD Breakeven Penalty ---
    print("\n--- Example 7: CD Breakeven Penalty ---")
    breakeven = LM.cd_breakeven_penalty(
        cd_rate=0.048, savings_rate=0.040, penalty_months=3
    )
    print(f"  CD rate: 4.8%, Savings rate: 4.0%, Penalty: 3 months interest")
    print(f"  Minimum hold: {breakeven:.1f} months to beat savings account")

    # --- Example 8: Net Liquid Assets ---
    print("\n--- Example 8: Net Liquid Assets ---")
    nla = LM.net_liquid_assets(95_000, 12_000)
    print(f"  Liquid assets: $95K, Short-term liabilities: $12K")
    print(f"  Net liquid assets: ${nla:,.0f}")

    print("\n" + "=" * 60)
    print("Demo complete.")
    print("=" * 60)


def _verify() -> int:
    """Assert that demo computations match the SKILL.md worked examples."""
    LM = LiquidityManagement
    failures: list[str] = []

    def check(label: str, actual: float, expected: float, rel_tol: float = 1e-3) -> None:
        ok = math.isclose(actual, expected, rel_tol=rel_tol)
        print(f"  {'PASS' if ok else 'FAIL'}: {label}: got {actual:,.4f}, expected {expected:,.4f}")
        if not ok:
            failures.append(label)

    print("Verifying against SKILL.md worked examples...")

    # Example 1: CD ladder — $60K, 6 rungs every 2 months, blended yield ~4.53%
    ladder = LM.cd_ladder(
        total_amount=60_000,
        num_rungs=6,
        rung_yields=[0.042, 0.044, 0.045, 0.046, 0.047, 0.048],
        maturity_interval_months=2,
    )
    check("Ex1 rung amount ($10,000)", ladder["rungs"][0]["amount"], 10_000.0, rel_tol=1e-9)
    check("Ex1 blended yield (~4.53%)", ladder["blended_yield"], 0.0453, rel_tol=2e-3)
    check("Ex1 liquidity interval (2 months)", ladder["liquidity_interval_months"], 2, rel_tol=1e-9)

    # Example 2: income smoothing — avg income $8,000, essentials $5,500
    smoothing = LM.income_smoothing(np.full(12, 8_000.0), monthly_essentials=5_500)
    check("Ex2 average income ($8,000)", smoothing["average_income"], 8_000.0, rel_tol=1e-9)
    check("Ex2 average surplus ($2,500)", smoothing["average_surplus"], 2_500.0, rel_tol=1e-9)
    check(
        "Ex2 smoothing reserve target ($16,500)",
        smoothing["smoothing_reserve_target"],
        16_500.0,
        rel_tol=1e-9,
    )

    if failures:
        print(f"FAIL: {len(failures)} check(s) did not match SKILL.md.")
        return 1
    print("PASS: all checks match SKILL.md worked examples.")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Liquidity management reference implementation: liquidity ratios, "
            "cash flow projections, cash runway, liquidity tier analysis, "
            "CD ladders, income smoothing, and CD breakeven analysis."
        ),
        epilog=(
            "Main class:\n"
            "  LiquidityManagement -- static methods: liquidity_ratio,\n"
            "    cash_reserve_ratio, current_ratio, quick_ratio, net_liquid_assets,\n"
            "    cash_flow_projection, cash_runway, liquidity_tier_analysis,\n"
            "    cd_ladder, income_smoothing, cd_breakeven_penalty\n"
            "\n"
            "This file is primarily meant to be imported as a module:\n"
            "  from liquidity_management import LiquidityManagement\n"
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
