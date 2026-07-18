# /// script
# dependencies = []
# requires-python = ">=3.11"
# ///
"""
Retirement Decumulation
=======================
Simulate withdrawal plans against return sequences (sequence-of-returns risk),
apply Guyton-Klinger-style guardrail adjustments, compute Required Minimum
Distributions from the IRS Uniform Lifetime Table, and evaluate Social
Security claiming factors and breakeven ages.

Statutory parameters embedded here: Social Security early-claiming reduction
(5/9 of 1% per month for the first 36 months, 5/12 of 1% beyond) and delayed
retirement credits (2/3 of 1% per month up to age 70); the SECURE 2.0 missed
RMD excise tax (25%, reduced to 10% if corrected timely). The Uniform Lifetime
Table divisors are from the IRS table effective 2022 (current as of 2026).
"""

import argparse
import math
import sys

# IRS Uniform Lifetime Table (effective 2022, current as of 2026), ages 72-100.
UNIFORM_LIFETIME_TABLE: dict[int, float] = {
    72: 27.4, 73: 26.5, 74: 25.5, 75: 24.6, 76: 23.7,
    77: 22.9, 78: 22.0, 79: 21.1, 80: 20.2, 81: 19.4,
    82: 18.5, 83: 17.7, 84: 16.8, 85: 16.0, 86: 15.2,
    87: 14.4, 88: 13.7, 89: 12.9, 90: 12.2, 91: 11.5,
    92: 10.8, 93: 10.1, 94: 9.5, 95: 8.9, 96: 8.4,
    97: 7.8, 98: 7.3, 99: 6.8, 100: 6.4,
}


class RetirementDecumulation:
    """Decumulation computations: withdrawal simulation, guardrails, RMDs,
    and Social Security claiming math.

    All methods are static — no instance state is required.
    """

    @staticmethod
    def simulate_fixed_real_withdrawals(
        initial_balance: float,
        initial_withdrawal: float,
        returns: list[float],
        inflation: float = 0.0,
    ) -> dict:
        """Simulate a fixed-real withdrawal plan against a return sequence.

        Each year the withdrawal (grown by inflation) is taken at the start of
        the year, and the remainder earns that year's return:
        B_t = (B_{t-1} - W_t) * (1 + r_t), with W_t = W_1 * (1 + i)^(t-1).

        Parameters
        ----------
        initial_balance : float
            Starting portfolio value.
        initial_withdrawal : float
            First-year withdrawal in dollars.
        returns : list[float]
            Annual returns as decimals (e.g., -0.20 for -20%), in order.
        inflation : float, optional
            Annual inflation applied to the withdrawal. Default is 0.0.

        Returns
        -------
        dict
            Keys: 'balances' (end-of-year list), 'withdrawals' (list),
            'ending_balance', 'depleted_year' (1-based year of depletion,
            or None if the portfolio survives).
        """
        balance = initial_balance
        withdrawal = initial_withdrawal
        balances: list[float] = []
        withdrawals: list[float] = []
        depleted_year: int | None = None

        for year, r in enumerate(returns, start=1):
            taken = min(withdrawal, balance)
            balance = (balance - taken) * (1.0 + r)
            balances.append(round(balance, 2))
            withdrawals.append(round(taken, 2))
            if balance <= 0 and depleted_year is None:
                depleted_year = year
            withdrawal *= 1.0 + inflation

        return {
            "balances": balances,
            "withdrawals": withdrawals,
            "ending_balance": balances[-1] if balances else round(balance, 2),
            "depleted_year": depleted_year,
        }

    @staticmethod
    def sequence_risk_comparison(
        initial_balance: float,
        initial_withdrawal: float,
        returns: list[float],
        inflation: float = 0.0,
    ) -> dict:
        """Compare a return sequence against its reversal under withdrawals.

        The two orderings share the same arithmetic and geometric mean return,
        so any difference in ending wealth is pure sequence-of-returns risk.

        Parameters
        ----------
        initial_balance : float
            Starting portfolio value.
        initial_withdrawal : float
            First-year withdrawal in dollars.
        returns : list[float]
            Annual returns as decimals, in the "forward" order.
        inflation : float, optional
            Annual inflation applied to the withdrawal. Default is 0.0.

        Returns
        -------
        dict
            Keys: 'forward_ending', 'reversed_ending', 'gap'
            (reversed minus forward), 'no_withdrawal_ending'
            (identical for both orderings).
        """
        sim = RetirementDecumulation.simulate_fixed_real_withdrawals
        forward = sim(initial_balance, initial_withdrawal, returns, inflation)
        backward = sim(initial_balance, initial_withdrawal, returns[::-1], inflation)

        growth = 1.0
        for r in returns:
            growth *= 1.0 + r

        return {
            "forward_ending": forward["ending_balance"],
            "reversed_ending": backward["ending_balance"],
            "gap": round(backward["ending_balance"] - forward["ending_balance"], 2),
            "no_withdrawal_ending": round(initial_balance * growth, 2),
        }

    @staticmethod
    def guardrails_adjustment(
        current_withdrawal: float,
        portfolio_value: float,
        initial_rate: float,
        guardrail_band: float = 0.20,
        adjustment: float = 0.10,
    ) -> dict:
        """Apply Guyton-Klinger-style guardrail rules to a planned withdrawal.

        The current withdrawal rate is tested against guardrails set at
        +/- guardrail_band of the initial rate. Above the upper guardrail the
        withdrawal is cut by `adjustment` (capital-preservation rule); below
        the lower guardrail it is raised by `adjustment` (prosperity rule).

        Parameters
        ----------
        current_withdrawal : float
            This year's planned (inflation-adjusted) withdrawal in dollars.
        portfolio_value : float
            Current portfolio value.
        initial_rate : float
            Initial withdrawal rate as a decimal (e.g., 0.05).
        guardrail_band : float, optional
            Band width around the initial rate. Default is 0.20 (20%).
        adjustment : float, optional
            Spending adjustment size. Default is 0.10 (10%).

        Returns
        -------
        dict
            Keys: 'current_rate', 'upper_guardrail', 'lower_guardrail',
            'action' ('cut', 'raise', or 'none'), 'adjusted_withdrawal',
            'adjusted_rate'.
        """
        current_rate = current_withdrawal / portfolio_value
        upper = initial_rate * (1.0 + guardrail_band)
        lower = initial_rate * (1.0 - guardrail_band)

        if current_rate > upper:
            action = "cut"
            adjusted = current_withdrawal * (1.0 - adjustment)
        elif current_rate < lower:
            action = "raise"
            adjusted = current_withdrawal * (1.0 + adjustment)
        else:
            action = "none"
            adjusted = current_withdrawal

        return {
            "current_rate": round(current_rate, 6),
            "upper_guardrail": round(upper, 6),
            "lower_guardrail": round(lower, 6),
            "action": action,
            "adjusted_withdrawal": round(adjusted, 2),
            "adjusted_rate": round(adjusted / portfolio_value, 6),
        }

    @staticmethod
    def uniform_lifetime_divisor(age: int) -> float:
        """Look up the Uniform Lifetime Table divisor for an age.

        Parameters
        ----------
        age : int
            Age attained during the distribution year (72-100 supported).

        Returns
        -------
        float
            Distribution period divisor from the IRS table effective 2022.

        Raises
        ------
        KeyError
            If the age is outside the embedded table range.
        """
        return UNIFORM_LIFETIME_TABLE[age]

    @staticmethod
    def rmd(prior_year_end_balance: float, divisor: float) -> float:
        """Compute a Required Minimum Distribution.

        RMD = prior December 31 balance / distribution period divisor.

        Parameters
        ----------
        prior_year_end_balance : float
            Account balance on December 31 of the prior year.
        divisor : float
            Distribution period from the applicable IRS life-expectancy table
            (e.g., 26.5 at age 73 under the Uniform Lifetime Table).

        Returns
        -------
        float
            The required minimum distribution in dollars.
        """
        if divisor <= 0:
            raise ValueError("divisor must be positive")
        return prior_year_end_balance / divisor

    @staticmethod
    def rmd_penalty(shortfall: float, corrected_timely: bool = False) -> float:
        """Compute the excise tax on a missed RMD under SECURE 2.0.

        The penalty is 25% of the shortfall, reduced to 10% if the shortfall
        is corrected within the correction window.

        Parameters
        ----------
        shortfall : float
            The RMD amount not taken by the deadline.
        corrected_timely : bool, optional
            True if corrected within the correction window. Default is False.

        Returns
        -------
        float
            Excise tax in dollars.
        """
        rate = 0.10 if corrected_timely else 0.25
        return shortfall * rate

    @staticmethod
    def ss_claiming_factor(claim_age: float, fra: float = 67.0) -> float:
        """Compute the Social Security benefit factor for a claiming age.

        Early claiming: benefit reduced by 5/9 of 1% per month for the first
        36 months before FRA and 5/12 of 1% per month beyond 36. Delayed
        claiming: 2/3 of 1% per month (8%/year) of delayed retirement credits,
        capped at age 70.

        Parameters
        ----------
        claim_age : float
            Claiming age in years (fractional ages allowed; 62 minimum, 70
            effective maximum for credits).
        fra : float, optional
            Full retirement age in years. Default is 67.0 (born 1960+).

        Returns
        -------
        float
            Multiplier applied to the Primary Insurance Amount (PIA).
        """
        months = round((claim_age - fra) * 12)
        if months < 0:
            early = -months
            reduction_pct = min(early, 36) * (5.0 / 9.0) + max(early - 36, 0) * (5.0 / 12.0)
            return 1.0 - reduction_pct / 100.0
        capped_months = min(months, round((70.0 - fra) * 12))
        return 1.0 + capped_months * (2.0 / 3.0) / 100.0

    @staticmethod
    def ss_monthly_benefit(pia: float, claim_age: float, fra: float = 67.0) -> float:
        """Compute the monthly benefit for a given PIA and claiming age.

        Parameters
        ----------
        pia : float
            Primary Insurance Amount (monthly benefit at FRA).
        claim_age : float
            Claiming age in years.
        fra : float, optional
            Full retirement age. Default is 67.0.

        Returns
        -------
        float
            Monthly benefit in dollars.
        """
        return pia * RetirementDecumulation.ss_claiming_factor(claim_age, fra)

    @staticmethod
    def ss_breakeven_age(
        early_age: float,
        early_benefit: float,
        late_age: float,
        late_benefit: float,
    ) -> float:
        """Compute the breakeven age between two Social Security claiming ages.

        Ignoring COLAs and discounting (COLAs scale both paths equally), the
        early claimer's head start is early_benefit * months_between; the late
        claimer gains (late_benefit - early_benefit) per month thereafter:
        breakeven months after the late claim = head start / monthly gain.

        Parameters
        ----------
        early_age : float
            Earlier claiming age in years.
        early_benefit : float
            Monthly benefit if claimed at early_age.
        late_age : float
            Later claiming age in years.
        late_benefit : float
            Monthly benefit if claimed at late_age.

        Returns
        -------
        float
            The age (in years) at which cumulative benefits are equal.
            Returns inf if the later benefit is not larger.
        """
        if late_benefit <= early_benefit:
            return float("inf")
        months_between = (late_age - early_age) * 12.0
        head_start = early_benefit * months_between
        months_after = head_start / (late_benefit - early_benefit)
        return late_age + months_after / 12.0


def _demo() -> None:
    RD = RetirementDecumulation

    print("=" * 60)
    print("Retirement Decumulation - Demo")
    print("=" * 60)

    # --- Example 1: Sequence-of-returns risk ---
    print("\n--- Example 1: Sequence-of-Returns Risk ---")
    returns = [-0.20, 0.10, 0.25]
    cmp = RD.sequence_risk_comparison(1_000_000, 50_000, returns)
    print(f"  $1M portfolio, $50K start-of-year withdrawals, returns {returns}")
    print(f"  Crash-first ending (A):   ${cmp['forward_ending']:,.2f}")
    print(f"  Crash-last ending (B):    ${cmp['reversed_ending']:,.2f}")
    print(f"  Gap from ordering alone:  ${cmp['gap']:,.2f}")
    print(f"  No-withdrawal ending:     ${cmp['no_withdrawal_ending']:,.2f} (identical either way)")

    # --- Example 2: Guardrails adjustments ---
    print("\n--- Example 2: Guardrails (5.0% initial, +/-20% bands, 10% moves) ---")
    cut = RD.guardrails_adjustment(51_500, 780_000, 0.05)
    print(f"  Bad year: $51,500 planned on $780,000 -> rate {cut['current_rate']:.2%}")
    print(f"  Action: {cut['action']} -> ${cut['adjusted_withdrawal']:,.2f} "
          f"(rate {cut['adjusted_rate']:.2%})")
    raise_ = RD.guardrails_adjustment(52_000, 1_400_000, 0.05)
    print(f"  Good year: $52,000 planned on $1,400,000 -> rate {raise_['current_rate']:.2%}")
    print(f"  Action: {raise_['action']} -> ${raise_['adjusted_withdrawal']:,.2f} "
          f"(rate {raise_['adjusted_rate']:.2%})")

    # --- Example 3: RMD at age 73 ---
    print("\n--- Example 3: RMD at Age 73 ---")
    divisor = RD.uniform_lifetime_divisor(73)
    rmd = RD.rmd(850_000, divisor)
    print(f"  $850,000 prior Dec 31 balance, age-73 divisor {divisor}")
    print(f"  RMD: ${rmd:,.2f} ({rmd / 850_000:.2%} of balance)")
    print(f"  Penalty if missed:        ${RD.rmd_penalty(rmd):,.2f} (25%)")
    print(f"  Penalty if corrected:     ${RD.rmd_penalty(rmd, corrected_timely=True):,.2f} (10%)")

    # --- Example 4: Social Security claiming ---
    print("\n--- Example 4: Social Security Claiming (PIA $2,000, FRA 67) ---")
    b62 = RD.ss_monthly_benefit(2_000, 62)
    b67 = RD.ss_monthly_benefit(2_000, 67)
    b70 = RD.ss_monthly_benefit(2_000, 70)
    print(f"  Claim at 62: factor {RD.ss_claiming_factor(62):.2f} -> ${b62:,.2f}/mo")
    print(f"  Claim at 67: factor {RD.ss_claiming_factor(67):.2f} -> ${b67:,.2f}/mo")
    print(f"  Claim at 70: factor {RD.ss_claiming_factor(70):.2f} -> ${b70:,.2f}/mo")
    be_62_67 = RD.ss_breakeven_age(62, b62, 67, b67)
    be_67_70 = RD.ss_breakeven_age(67, b67, 70, b70)
    print(f"  Breakeven 62 vs 67: age {be_62_67:.1f}")
    print(f"  Breakeven 67 vs 70: age {be_67_70:.1f}")

    print("\n" + "=" * 60)
    print("Demo complete.")
    print("=" * 60)


def _verify() -> int:
    """Assert that demo computations match the SKILL.md worked examples."""
    RD = RetirementDecumulation
    failures: list[str] = []

    def check(label: str, actual: float, expected: float, rel_tol: float = 1e-4) -> None:
        ok = math.isclose(actual, expected, rel_tol=rel_tol)
        print(f"  {'PASS' if ok else 'FAIL'}: {label}: got {actual:,.4f}, expected {expected:,.4f}")
        if not ok:
            failures.append(label)

    print("Verifying against SKILL.md worked examples...")

    # Example 1: sequence risk — A ends $913,750; B ends $961,000;
    # no-withdrawal ending $1,100,000; gap $47,250.
    cmp = RD.sequence_risk_comparison(1_000_000, 50_000, [-0.20, 0.10, 0.25])
    check("Ex1 crash-first ending ($913,750)", cmp["forward_ending"], 913_750.0, rel_tol=1e-9)
    check("Ex1 crash-last ending ($961,000)", cmp["reversed_ending"], 961_000.0, rel_tol=1e-9)
    check("Ex1 gap ($47,250)", cmp["gap"], 47_250.0, rel_tol=1e-9)
    check("Ex1 no-withdrawal ending ($1,100,000)", cmp["no_withdrawal_ending"], 1_100_000.0, rel_tol=1e-9)

    # Example 2: guardrails — 6.60% rate triggers cut to $46,350 (5.94%);
    # 3.71% rate triggers raise to $57,200 (4.09%).
    cut = RD.guardrails_adjustment(51_500, 780_000, 0.05)
    check("Ex2 bad-year rate (6.60%)", cut["current_rate"], 0.0660, rel_tol=1e-3)
    check("Ex2 cut withdrawal ($46,350)", cut["adjusted_withdrawal"], 46_350.0, rel_tol=1e-9)
    check("Ex2 post-cut rate (5.94%)", cut["adjusted_rate"], 0.0594, rel_tol=1e-3)
    if cut["action"] != "cut":
        print(f"  FAIL: Ex2 expected action 'cut', got '{cut['action']}'")
        failures.append("Ex2 action cut")
    raise_ = RD.guardrails_adjustment(52_000, 1_400_000, 0.05)
    check("Ex2 good-year rate (3.71%)", raise_["current_rate"], 0.0371, rel_tol=2e-3)
    check("Ex2 raised withdrawal ($57,200)", raise_["adjusted_withdrawal"], 57_200.0, rel_tol=1e-9)
    check("Ex2 post-raise rate (4.09%)", raise_["adjusted_rate"], 0.0409, rel_tol=2e-3)
    if raise_["action"] != "raise":
        print(f"  FAIL: Ex2 expected action 'raise', got '{raise_['action']}'")
        failures.append("Ex2 action raise")

    # Example 3: RMD — $850,000 / 26.5 = $32,075.47; penalties $8,018.87 / $3,207.55.
    divisor = RD.uniform_lifetime_divisor(73)
    check("Ex3 age-73 divisor (26.5)", divisor, 26.5, rel_tol=1e-9)
    rmd = RD.rmd(850_000, divisor)
    check("Ex3 RMD ($32,075.47)", rmd, 32_075.47, rel_tol=1e-6)
    check("Ex3 missed penalty ($8,018.87)", RD.rmd_penalty(rmd), 8_018.87, rel_tol=1e-6)
    check("Ex3 corrected penalty ($3,207.55)", RD.rmd_penalty(rmd, True), 3_207.55, rel_tol=1e-6)

    # Example 4: SS — 62 factor 0.70 -> $1,400; 70 factor 1.24 -> $2,480;
    # breakeven 62v67 at 78.67, 67v70 at 82.5.
    check("Ex4 factor at 62 (0.70)", RD.ss_claiming_factor(62), 0.70, rel_tol=1e-9)
    check("Ex4 factor at 70 (1.24)", RD.ss_claiming_factor(70), 1.24, rel_tol=1e-9)
    b62 = RD.ss_monthly_benefit(2_000, 62)
    b70 = RD.ss_monthly_benefit(2_000, 70)
    check("Ex4 benefit at 62 ($1,400)", b62, 1_400.0, rel_tol=1e-9)
    check("Ex4 benefit at 70 ($2,480)", b70, 2_480.0, rel_tol=1e-9)
    check("Ex4 breakeven 62 vs 67 (78.67)", RD.ss_breakeven_age(62, b62, 67, 2_000), 78.6667, rel_tol=1e-4)
    check("Ex4 breakeven 67 vs 70 (82.5)", RD.ss_breakeven_age(67, 2_000, 70, b70), 82.5, rel_tol=1e-9)

    if failures:
        print(f"FAIL: {len(failures)} check(s) did not match SKILL.md.")
        return 1
    print("PASS: all checks match SKILL.md worked examples.")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Retirement decumulation reference implementation: withdrawal "
            "simulation and sequence-of-returns comparison, guardrails "
            "adjustments, RMD calculation and penalties, and Social Security "
            "claiming factors and breakeven ages."
        ),
        epilog=(
            "Main class:\n"
            "  RetirementDecumulation -- static methods:\n"
            "    simulate_fixed_real_withdrawals, sequence_risk_comparison,\n"
            "    guardrails_adjustment, uniform_lifetime_divisor, rmd,\n"
            "    rmd_penalty, ss_claiming_factor, ss_monthly_benefit,\n"
            "    ss_breakeven_age\n"
            "\n"
            "This file is primarily meant to be imported as a module:\n"
            "  from retirement_decumulation import RetirementDecumulation\n"
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
