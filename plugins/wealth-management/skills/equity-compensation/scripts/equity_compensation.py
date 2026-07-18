# /// script
# dependencies = []
# requires-python = ">=3.11"
# ///
"""
Equity Compensation
===================
RSU vesting income, withholding-gap estimation, NSO/ISO exercise tax outcomes
including a simplified AMT spread computation, qualifying vs disqualifying
disposition comparison, and ESPP (Section 423) discount taxation.

Simplifications: federal tax only; AMT modeled with user-supplied exemption,
phaseout, and bracket parameters (indexed figures change annually — verify);
no payroll tax, state tax, or NIIT unless folded into the supplied rates.
"""


class EquityCompensation:
    """Equity compensation tax calculations (RSU, NSO, ISO/AMT, ESPP)."""

    # ------------------------------------------------------------------ RSU

    @staticmethod
    def rsu_vest(
        shares_vesting: int,
        fmv_at_vest: float,
        marginal_rate: float,
        withholding_rate: float = 0.22,
    ) -> dict:
        """RSU vesting income, net-share settlement, and withholding gap.

        Parameters
        ----------
        shares_vesting : int
            Number of RSUs vesting.
        fmv_at_vest : float
            Fair market value per share on the vest date.
        marginal_rate : float
            Client's actual federal marginal tax rate (decimal).
        withholding_rate : float, optional
            Flat supplemental wage withholding rate. Default 0.22 (the rate
            for supplemental wages up to $1M cumulative, as of 2026; a
            mandatory 0.37 applies to the excess above $1M).

        Returns
        -------
        dict
            Keys: "ordinary_income", "tax_withheld", "shares_withheld",
            "net_shares", "actual_tax", "withholding_gap". A positive
            withholding_gap is additional tax due at filing.
        """
        income = shares_vesting * fmv_at_vest
        withheld = income * withholding_rate
        shares_withheld = withheld / fmv_at_vest
        actual_tax = income * marginal_rate
        return {
            "ordinary_income": float(income),
            "tax_withheld": float(withheld),
            "shares_withheld": float(shares_withheld),
            "net_shares": float(shares_vesting - shares_withheld),
            "actual_tax": float(actual_tax),
            "withholding_gap": float(actual_tax - withheld),
        }

    # ------------------------------------------------------------------ NSO

    @staticmethod
    def nso_exercise(
        shares: int,
        strike: float,
        fmv_at_exercise: float,
        ordinary_rate: float,
    ) -> dict:
        """NSO exercise: spread is ordinary income; basis steps up to FMV.

        Parameters
        ----------
        shares : int
            Number of options exercised.
        strike : float
            Exercise (strike) price per share.
        fmv_at_exercise : float
            Fair market value per share at exercise.
        ordinary_rate : float
            Ordinary income tax rate on the spread (decimal).

        Returns
        -------
        dict
            Keys: "spread_income", "tax", "exercise_cost",
            "basis_per_share", "total_outlay" (exercise cost + tax).
        """
        spread = shares * max(fmv_at_exercise - strike, 0.0)
        tax = spread * ordinary_rate
        cost = shares * strike
        return {
            "spread_income": float(spread),
            "tax": float(tax),
            "exercise_cost": float(cost),
            "basis_per_share": float(fmv_at_exercise),
            "total_outlay": float(cost + tax),
        }

    # ------------------------------------------------------------------ ISO / AMT

    @staticmethod
    def iso_exercise_amt(
        shares: int,
        strike: float,
        fmv_at_exercise: float,
        other_amti: float,
        regular_tax: float,
        amt_exemption: float,
        phaseout_threshold: float | None = None,
        phaseout_rate: float = 0.25,
        bracket_breakpoint: float = 220_000.0,
        low_rate: float = 0.26,
        high_rate: float = 0.28,
    ) -> dict:
        """Simplified AMT computation for an exercise-and-hold ISO transaction.

        The ISO spread is an AMT preference item (a deferral item), so any
        AMT due also becomes a minimum tax credit carryforward.

        Parameters
        ----------
        shares : int
            Number of ISOs exercised (and held past year-end).
        strike : float
            Exercise price per share.
        fmv_at_exercise : float
            Fair market value per share at exercise.
        other_amti : float
            AMTI from all other sources (income after regular deductions,
            with other AMT adjustments already applied), before the spread.
        regular_tax : float
            Regular federal income tax for the year.
        amt_exemption : float
            AMT exemption amount (inflation-indexed annually — supply the
            current-year figure).
        phaseout_threshold : float or None, optional
            AMTI level above which the exemption phases out. None (default)
            disables the phaseout. Thresholds and the phaseout rate were
            changed by 2025 tax legislation effective 2026 — verify.
        phaseout_rate : float, optional
            Exemption reduction per dollar of AMTI above the threshold.
        bracket_breakpoint : float, optional
            AMT base above which the high rate applies (indexed — verify).
        low_rate, high_rate : float, optional
            The two AMT rates (26% / 28%).

        Returns
        -------
        dict
            Keys: "amt_preference" (the spread), "amti", "exemption_used",
            "amt_base", "tentative_minimum_tax", "amt_due", "amt_credit"
            (equals amt_due for a pure deferral item), "amt_basis_per_share".
        """
        spread = shares * max(fmv_at_exercise - strike, 0.0)
        amti = other_amti + spread

        exemption = amt_exemption
        if phaseout_threshold is not None and amti > phaseout_threshold:
            exemption = max(
                0.0, amt_exemption - phaseout_rate * (amti - phaseout_threshold)
            )

        base = max(amti - exemption, 0.0)
        if base <= bracket_breakpoint:
            tmt = base * low_rate
        else:
            tmt = bracket_breakpoint * low_rate + (base - bracket_breakpoint) * high_rate
        amt_due = max(0.0, tmt - regular_tax)

        return {
            "amt_preference": float(spread),
            "amti": float(amti),
            "exemption_used": float(exemption),
            "amt_base": float(base),
            "tentative_minimum_tax": float(tmt),
            "amt_due": float(amt_due),
            "amt_credit": float(amt_due),
            "amt_basis_per_share": float(fmv_at_exercise),
        }

    # ------------------------------------------------------------------ ISO dispositions

    @staticmethod
    def iso_disposition(
        shares: int,
        strike: float,
        fmv_at_exercise: float,
        sale_price: float,
        qualifying: bool,
        ordinary_rate: float,
        stcg_rate: float,
        ltcg_rate: float,
        long_term_capital_portion: bool = False,
    ) -> dict:
        """Tax outcome of selling ISO shares (qualifying or disqualifying).

        Qualifying disposition: sale > 2 years from grant AND > 1 year from
        exercise; the entire gain over strike is long-term capital gain.

        Disqualifying disposition: ordinary income equals the exercise-date
        spread, capped at the actual gain if the stock fell (and zero if sold
        below strike, where the result is a capital loss). Gain above the
        exercise-date FMV is capital gain — short-term unless
        ``long_term_capital_portion`` is True.

        Parameters
        ----------
        shares, strike, fmv_at_exercise, sale_price : as named, per share.
        qualifying : bool
            True for a qualifying disposition.
        ordinary_rate, stcg_rate, ltcg_rate : float
            Applicable federal rates (decimal).
        long_term_capital_portion : bool, optional
            For a disqualifying sale held > 1 year from exercise (but failing
            the 2-year-from-grant test), tax the capital portion at LTCG.

        Returns
        -------
        dict
            Keys: "ordinary_income", "capital_gain", "ordinary_tax",
            "capital_tax", "total_tax", "total_gain".
        """
        total_gain = shares * (sale_price - strike)

        if qualifying:
            ordinary = 0.0
            capital = total_gain
            ordinary_tax = 0.0
            capital_tax = max(capital, 0.0) * ltcg_rate
        else:
            spread = max(fmv_at_exercise - strike, 0.0)
            gain_per_share = sale_price - strike
            ordinary_per_share = min(spread, max(gain_per_share, 0.0))
            ordinary = shares * ordinary_per_share
            capital = total_gain - ordinary
            ordinary_tax = ordinary * ordinary_rate
            cap_rate = ltcg_rate if long_term_capital_portion else stcg_rate
            capital_tax = max(capital, 0.0) * cap_rate

        return {
            "ordinary_income": float(ordinary),
            "capital_gain": float(capital),
            "ordinary_tax": float(ordinary_tax),
            "capital_tax": float(capital_tax),
            "total_tax": float(ordinary_tax + capital_tax),
            "total_gain": float(total_gain),
        }

    @staticmethod
    def iso_disposition_comparison(
        shares: int,
        strike: float,
        fmv_at_exercise: float,
        sale_price: float,
        ordinary_rate: float,
        stcg_rate: float,
        ltcg_rate: float,
    ) -> dict:
        """Side-by-side qualifying vs disqualifying ISO disposition.

        Returns
        -------
        dict
            Keys: "qualifying", "disqualifying" (each an iso_disposition
            result dict) and "tax_difference" (disqualifying minus
            qualifying total tax; positive = cost of disqualifying).
        """
        q = EquityCompensation.iso_disposition(
            shares, strike, fmv_at_exercise, sale_price, True,
            ordinary_rate, stcg_rate, ltcg_rate,
        )
        d = EquityCompensation.iso_disposition(
            shares, strike, fmv_at_exercise, sale_price, False,
            ordinary_rate, stcg_rate, ltcg_rate,
        )
        return {
            "qualifying": q,
            "disqualifying": d,
            "tax_difference": float(d["total_tax"] - q["total_tax"]),
        }

    # ------------------------------------------------------------------ ESPP

    @staticmethod
    def espp_purchase(
        offer_date_fmv: float,
        purchase_date_fmv: float,
        discount: float = 0.15,
        lookback: bool = True,
    ) -> dict:
        """Qualified Section 423 ESPP purchase price and bargain element.

        Parameters
        ----------
        offer_date_fmv : float
            FMV per share on the offering (grant) date.
        purchase_date_fmv : float
            FMV per share on the purchase date.
        discount : float, optional
            Plan discount (maximum 0.15 for a qualified plan). Default 0.15.
        lookback : bool, optional
            If True (default), the discount applies to the lower of the two
            prices.

        Returns
        -------
        dict
            Keys: "purchase_price", "bargain_element" (per share, FMV at
            purchase minus price paid).
        """
        reference = min(offer_date_fmv, purchase_date_fmv) if lookback else purchase_date_fmv
        price = reference * (1.0 - discount)
        return {
            "purchase_price": float(price),
            "bargain_element": float(purchase_date_fmv - price),
        }

    @staticmethod
    def espp_disposition(
        offer_date_fmv: float,
        purchase_date_fmv: float,
        sale_price: float,
        qualifying: bool,
        ordinary_rate: float,
        stcg_rate: float,
        ltcg_rate: float,
        discount: float = 0.15,
        lookback: bool = True,
    ) -> dict:
        """Per-share tax outcome of selling qualified ESPP shares.

        Qualifying (> 2 years from offering date and > 1 year from purchase):
        ordinary income = min(actual gain, discount x offer-date FMV), the
        remainder is long-term capital gain. Disqualifying: ordinary income =
        full bargain element (FMV at purchase - purchase price), even at an
        overall loss; the remainder is capital gain or loss (short-term rate
        assumed here).

        Returns
        -------
        dict
            Per-share keys: "purchase_price", "ordinary_income",
            "capital_gain", "ordinary_tax", "capital_tax", "total_tax".
        """
        p = EquityCompensation.espp_purchase(
            offer_date_fmv, purchase_date_fmv, discount, lookback
        )
        price = p["purchase_price"]
        actual_gain = sale_price - price

        if qualifying:
            ordinary = min(max(actual_gain, 0.0), discount * offer_date_fmv)
            capital = actual_gain - ordinary
            capital_tax = max(capital, 0.0) * ltcg_rate
        else:
            ordinary = p["bargain_element"]
            capital = sale_price - purchase_date_fmv
            capital_tax = max(capital, 0.0) * stcg_rate

        ordinary_tax = ordinary * ordinary_rate
        return {
            "purchase_price": float(price),
            "ordinary_income": float(ordinary),
            "capital_gain": float(capital),
            "ordinary_tax": float(ordinary_tax),
            "capital_tax": float(capital_tax),
            "total_tax": float(ordinary_tax + capital_tax),
        }


def _demo() -> None:
    """Demo: equity compensation calculations (default bare-run output)."""
    EC = EquityCompensation

    print("=" * 65)
    print("Equity Compensation - Demo")
    print("=" * 65)

    # --- RSU vest and withholding gap (SKILL.md Example 1) ---
    print("\n--- RSU Vest: Withholding Gap ---")
    rsu = EC.rsu_vest(10_000, 40.0, marginal_rate=0.35, withholding_rate=0.22)
    print("10,000 RSUs vest at $40; 22% supplemental withholding; 35% marginal")
    print(f"  Ordinary income:    ${rsu['ordinary_income']:>10,.0f}")
    print(f"  Withheld (22%):     ${rsu['tax_withheld']:>10,.0f}  "
          f"({rsu['shares_withheld']:,.0f} shares; {rsu['net_shares']:,.0f} net)")
    print(f"  Actual tax (35%):   ${rsu['actual_tax']:>10,.0f}")
    print(f"  Withholding gap:    ${rsu['withholding_gap']:>10,.0f} due at filing")

    # --- NSO exercise ---
    print("\n--- NSO Exercise ---")
    nso = EC.nso_exercise(3_000, 12.0, 30.0, ordinary_rate=0.35)
    print("3,000 NSOs, strike $12, FMV $30, 35% ordinary rate")
    print(f"  Spread income: ${nso['spread_income']:,.0f}; tax ${nso['tax']:,.0f}; "
          f"basis ${nso['basis_per_share']:.0f}/sh; total outlay ${nso['total_outlay']:,.0f}")

    # --- ISO exercise AMT (SKILL.md Example 2) ---
    print("\n--- ISO Exercise-and-Hold: Simplified AMT ---")
    iso = EC.iso_exercise_amt(
        shares=5_000, strike=10.0, fmv_at_exercise=50.0,
        other_amti=250_000.0, regular_tax=60_000.0,
        amt_exemption=137_000.0, bracket_breakpoint=220_000.0,
    )
    print("5,000 ISOs, strike $10, FMV $50; other AMTI $250K; regular tax $60K")
    print("(illustrative exemption $137K, 28% breakpoint $220K — indexed, verify)")
    print(f"  AMT preference (spread):  ${iso['amt_preference']:>10,.0f}")
    print(f"  AMTI:                     ${iso['amti']:>10,.0f}")
    print(f"  AMT base:                 ${iso['amt_base']:>10,.0f}")
    print(f"  Tentative minimum tax:    ${iso['tentative_minimum_tax']:>10,.0f}")
    print(f"  AMT due (= credit c/f):   ${iso['amt_due']:>10,.0f}")

    # --- ISO disposition comparison (SKILL.md Example 3) ---
    print("\n--- ISO Disposition: Qualifying vs Disqualifying ---")
    cmp_ = EC.iso_disposition_comparison(
        shares=2_000, strike=15.0, fmv_at_exercise=35.0, sale_price=60.0,
        ordinary_rate=0.35, stcg_rate=0.35, ltcg_rate=0.15,
    )
    q, d = cmp_["qualifying"], cmp_["disqualifying"]
    print("2,000 ISOs, strike $15, exercised at $35, sold at $60 (35%/15% rates)")
    print(f"  Qualifying:    LTCG ${q['capital_gain']:,.0f} -> tax ${q['total_tax']:,.0f}")
    print(f"  Disqualifying: ordinary ${d['ordinary_income']:,.0f} + STCG "
          f"${d['capital_gain']:,.0f} -> tax ${d['total_tax']:,.0f}")
    print(f"  Cost of disqualifying: ${cmp_['tax_difference']:,.0f}")

    # --- ESPP ---
    print("\n--- ESPP (Qualified Section 423, 15% discount, lookback) ---")
    purchase = EC.espp_purchase(20.0, 30.0)
    print(f"Offer-date FMV $20, purchase-date FMV $30 -> purchase price "
          f"${purchase['purchase_price']:.2f}, bargain element "
          f"${purchase['bargain_element']:.2f}/sh")
    for label, qualifying in (("Qualifying", True), ("Disqualifying", False)):
        r = EC.espp_disposition(
            20.0, 30.0, sale_price=40.0, qualifying=qualifying,
            ordinary_rate=0.35, stcg_rate=0.35, ltcg_rate=0.15,
        )
        print(f"  {label:13s} sale at $40: ordinary ${r['ordinary_income']:.2f}, "
              f"capital ${r['capital_gain']:.2f}, tax ${r['total_tax']:.2f}/sh")

    print("\n" + "=" * 65)
    print("Demo complete.")
    print("=" * 65)


def _verify() -> int:
    """Re-run the demo computations and assert the SKILL.md worked-example numbers.

    Returns 0 on success, 1 on any mismatch.
    """
    import math

    EC = EquityCompensation
    failures: list[str] = []

    def check(name: str, actual: float, expected: float, rel_tol: float = 1e-6) -> None:
        if math.isclose(actual, expected, rel_tol=rel_tol, abs_tol=1e-9):
            print(f"  PASS  {name}: {actual:,.6g} (expected {expected:,.6g})")
        else:
            failures.append(name)
            print(f"  FAIL  {name}: {actual:,.6g} (expected {expected:,.6g})")

    print("Verifying equity_compensation.py against SKILL.md worked examples...")

    # --- SKILL.md Example 1: RSU withholding gap ---
    rsu = EC.rsu_vest(10_000, 40.0, marginal_rate=0.35, withholding_rate=0.22)
    check("Example 1: ordinary income", rsu["ordinary_income"], 400_000.0)
    check("Example 1: tax withheld", rsu["tax_withheld"], 88_000.0)
    check("Example 1: shares withheld", rsu["shares_withheld"], 2_200.0)
    check("Example 1: net shares", rsu["net_shares"], 7_800.0)
    check("Example 1: actual tax", rsu["actual_tax"], 140_000.0)
    check("Example 1: withholding gap", rsu["withholding_gap"], 52_000.0)

    # --- SKILL.md Example 2: ISO exercise AMT ---
    iso = EC.iso_exercise_amt(
        shares=5_000, strike=10.0, fmv_at_exercise=50.0,
        other_amti=250_000.0, regular_tax=60_000.0,
        amt_exemption=137_000.0, bracket_breakpoint=220_000.0,
    )
    check("Example 2: AMT preference", iso["amt_preference"], 200_000.0)
    check("Example 2: AMTI", iso["amti"], 450_000.0)
    check("Example 2: AMT base", iso["amt_base"], 313_000.0)
    check("Example 2: tentative minimum tax", iso["tentative_minimum_tax"], 83_240.0)
    check("Example 2: AMT due", iso["amt_due"], 23_240.0)
    check("Example 2: AMT credit", iso["amt_credit"], 23_240.0)

    # --- SKILL.md Example 3: qualifying vs disqualifying ISO disposition ---
    cmp_ = EC.iso_disposition_comparison(
        shares=2_000, strike=15.0, fmv_at_exercise=35.0, sale_price=60.0,
        ordinary_rate=0.35, stcg_rate=0.35, ltcg_rate=0.15,
    )
    q, d = cmp_["qualifying"], cmp_["disqualifying"]
    check("Example 3: qualifying LTCG", q["capital_gain"], 90_000.0)
    check("Example 3: qualifying tax", q["total_tax"], 13_500.0)
    check("Example 3: disqualifying ordinary income", d["ordinary_income"], 40_000.0)
    check("Example 3: disqualifying STCG", d["capital_gain"], 50_000.0)
    check("Example 3: disqualifying tax", d["total_tax"], 31_500.0)
    check("Example 3: cost of disqualifying", cmp_["tax_difference"], 18_000.0)

    # Disqualifying at a price below exercise-date FMV: ordinary income is
    # capped at the actual gain (sold at $18, strike $15, FMV $35 -> $3/sh).
    fallen = EC.iso_disposition(
        1_000, 15.0, 35.0, 18.0, qualifying=False,
        ordinary_rate=0.35, stcg_rate=0.35, ltcg_rate=0.15,
    )
    check("disqualifying below FMV: ordinary capped at gain",
          fallen["ordinary_income"], 3_000.0)
    check("disqualifying below FMV: no capital gain", fallen["capital_gain"], 0.0)

    # --- Demo: ESPP with lookback ---
    purchase = EC.espp_purchase(20.0, 30.0)
    check("ESPP: purchase price (85% of $20)", purchase["purchase_price"], 17.0)
    check("ESPP: bargain element", purchase["bargain_element"], 13.0)

    espp_q = EC.espp_disposition(20.0, 30.0, 40.0, True, 0.35, 0.35, 0.15)
    check("ESPP qualifying: ordinary = 15% x offer FMV", espp_q["ordinary_income"], 3.0)
    check("ESPP qualifying: LTCG remainder", espp_q["capital_gain"], 20.0)

    espp_d = EC.espp_disposition(20.0, 30.0, 40.0, False, 0.35, 0.35, 0.15)
    check("ESPP disqualifying: ordinary = bargain element",
          espp_d["ordinary_income"], 13.0)
    check("ESPP disqualifying: capital gain above purchase FMV",
          espp_d["capital_gain"], 10.0)

    # ESPP disqualifying at an overall loss still has full ordinary income.
    espp_loss = EC.espp_disposition(20.0, 30.0, 16.0, False, 0.35, 0.35, 0.15)
    check("ESPP disqualifying at a loss: ordinary income unchanged",
          espp_loss["ordinary_income"], 13.0)
    check("ESPP disqualifying at a loss: capital loss",
          espp_loss["capital_gain"], -14.0)

    if failures:
        print(f"\nFAIL: {len(failures)} check(s) failed: {', '.join(failures)}")
        return 1
    print("\nPASS: all checks passed.")
    return 0


if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        description=(
            "Equity compensation reference implementation. Class "
            "EquityCompensation provides: rsu_vest (vest income, net-share "
            "settlement, withholding gap), nso_exercise (spread income and "
            "tax), iso_exercise_amt (simplified AMT on an exercise-and-hold, "
            "with exemption phaseout and 26%/28% brackets), iso_disposition "
            "and iso_disposition_comparison (qualifying vs disqualifying), "
            "espp_purchase and espp_disposition (Section 423 lookback "
            "pricing and disposition taxation)."
        ),
        epilog=(
            "This file is primarily meant to be imported as a module: "
            "from equity_compensation import EquityCompensation. "
            "Run without arguments to print a demonstration of each calculation."
        ),
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help=(
            "run the demo computations and assert key outputs match the "
            "SKILL.md worked examples; prints PASS/FAIL and exits nonzero "
            "on mismatch"
        ),
    )
    args = parser.parse_args()

    if args.verify:
        sys.exit(_verify())
    _demo()
