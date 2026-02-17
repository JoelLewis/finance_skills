"""
Return Calculations - Layer 0 (Mathematical Foundations)

A comprehensive reference implementation for computing investment return metrics
including time-weighted returns, money-weighted returns, CAGR, annualization,
sub-period linking, and arithmetic/geometric/log return conversions.

Usage:
    python return_calculations.py

Dependencies:
    numpy
"""

import math
from typing import Optional

import numpy as np


class Returns:
    """Compute and convert investment return metrics.

    This class provides static methods for all standard return calculations
    used in investment performance measurement. All methods are stateless
    and operate on the inputs provided.
    """

    @staticmethod
    def holding_period_return(
        begin_value: float,
        end_value: float,
        distributions: float = 0.0,
    ) -> float:
        """Compute the simple holding period return.

        R = (V1 - V0 + D) / V0

        Args:
            begin_value: Portfolio value at the start of the period (V0).
            end_value: Portfolio value at the end of the period (V1).
            distributions: Income received during the period (dividends,
                interest, etc.). Defaults to 0.

        Returns:
            The holding period return as a decimal (e.g., 0.05 for 5%).

        Raises:
            ValueError: If begin_value is zero.
        """
        if begin_value == 0:
            raise ValueError("begin_value must be non-zero.")
        return (end_value - begin_value + distributions) / begin_value

    @staticmethod
    def time_weighted_return(sub_period_returns: list[float]) -> float:
        """Compute the time-weighted return by geometrically linking sub-period returns.

        TWR = prod(1 + r_i) - 1

        Eliminates the impact of external cash flows, making it the standard
        for evaluating investment manager performance (GIPS-compliant).

        Args:
            sub_period_returns: A list of sub-period returns as decimals.

        Returns:
            The cumulative time-weighted return as a decimal.
        """
        product = np.prod([1.0 + r for r in sub_period_returns])
        return float(product - 1.0)

    @staticmethod
    def money_weighted_return(
        cash_flows: list[tuple[int, float]],
        guess: float = 0.1,
    ) -> float:
        """Compute the money-weighted return (IRR) using Newton's method.

        Finds the rate r such that:
            sum( CF_t / (1 + r)^t ) = 0

        Cash flows should be signed: negative for contributions (money in),
        positive for withdrawals or terminal value (money out).

        Args:
            cash_flows: List of (time_period, cash_flow_amount) tuples.
                Time periods are integers (e.g., day counts or period indices).
                The first cash flow is typically the initial investment (negative),
                and the last includes the terminal value (positive).
            guess: Initial guess for the rate. Defaults to 0.1 (10%).

        Returns:
            The money-weighted return (IRR) as a decimal.

        Raises:
            RuntimeError: If Newton's method fails to converge.
        """
        rate = guess
        max_iterations = 1000
        tolerance = 1e-10

        for _ in range(max_iterations):
            npv = 0.0
            npv_deriv = 0.0
            for t, cf in cash_flows:
                discount = (1.0 + rate) ** t
                npv += cf / discount
                if t != 0:
                    npv_deriv -= t * cf / ((1.0 + rate) ** (t + 1))

            if abs(npv) < tolerance:
                return rate

            if abs(npv_deriv) < 1e-15:
                raise RuntimeError(
                    "Newton's method derivative near zero; try a different guess."
                )

            rate = rate - npv / npv_deriv

        raise RuntimeError(
            f"Newton's method did not converge after {max_iterations} iterations."
        )

    @staticmethod
    def cagr(begin_value: float, end_value: float, years: float) -> float:
        """Compute the Compound Annual Growth Rate.

        CAGR = (V_end / V_start)^(1/n) - 1

        Args:
            begin_value: Starting value of the investment.
            end_value: Ending value of the investment.
            years: Number of years in the holding period.

        Returns:
            The CAGR as a decimal.

        Raises:
            ValueError: If begin_value is zero or years is zero.
        """
        if begin_value == 0:
            raise ValueError("begin_value must be non-zero.")
        if years == 0:
            raise ValueError("years must be non-zero.")
        return (end_value / begin_value) ** (1.0 / years) - 1.0

    @staticmethod
    def annualize(
        total_return: float,
        periods: float,
        periods_per_year: float,
    ) -> float:
        """Annualize a return observed over a given number of periods.

        R_annual = (1 + R_total)^(periods_per_year / periods) - 1

        Args:
            total_return: The cumulative return over the observation window
                as a decimal.
            periods: The number of periods in the observation window.
            periods_per_year: The number of such periods in one year
                (e.g., 252 for trading days, 12 for months, 4 for quarters).

        Returns:
            The annualized return as a decimal.
        """
        return (1.0 + total_return) ** (periods_per_year / periods) - 1.0

    @staticmethod
    def link_returns(returns: list[float]) -> float:
        """Link (chain) a sequence of periodic returns into a cumulative return.

        R_cumulative = (1 + r_1)(1 + r_2)...(1 + r_n) - 1

        Args:
            returns: A list of periodic returns as decimals.

        Returns:
            The cumulative linked return as a decimal.
        """
        product = np.prod([1.0 + r for r in returns])
        return float(product - 1.0)

    @staticmethod
    def arithmetic_mean(returns: list[float]) -> float:
        """Compute the arithmetic mean of a series of returns.

        R_arith = sum(r_i) / n

        The arithmetic mean is the best unbiased estimate of the expected
        single-period return and is used as an input for mean-variance
        optimization. It overstates the realized compound growth rate.

        Args:
            returns: A list of periodic returns as decimals.

        Returns:
            The arithmetic mean return as a decimal.
        """
        return float(np.mean(returns))

    @staticmethod
    def geometric_mean(returns: list[float]) -> float:
        """Compute the geometric mean of a series of returns.

        R_geom = [prod(1 + r_i)]^(1/n) - 1

        The geometric mean represents the actual per-period compound growth
        rate. It is always less than or equal to the arithmetic mean;
        the gap approximates sigma^2 / 2.

        Args:
            returns: A list of periodic returns as decimals.

        Returns:
            The geometric mean return as a decimal.
        """
        n = len(returns)
        product = np.prod([1.0 + r for r in returns])
        return float(product ** (1.0 / n) - 1.0)

    @staticmethod
    def log_return(begin_value: float, end_value: float) -> float:
        """Compute the continuously compounded (log) return.

        r_log = ln(V1 / V0)

        Log returns are additive across time but NOT across assets.

        Args:
            begin_value: Value at the start of the period.
            end_value: Value at the end of the period.

        Returns:
            The log return as a decimal.

        Raises:
            ValueError: If begin_value or end_value is non-positive.
        """
        if begin_value <= 0 or end_value <= 0:
            raise ValueError("Both begin_value and end_value must be positive.")
        return math.log(end_value / begin_value)

    @staticmethod
    def log_to_simple(log_ret: float) -> float:
        """Convert a log return to a simple return.

        r_simple = e^(r_log) - 1

        Args:
            log_ret: The log (continuously compounded) return.

        Returns:
            The equivalent simple return as a decimal.
        """
        return math.exp(log_ret) - 1.0

    @staticmethod
    def simple_to_log(simple_ret: float) -> float:
        """Convert a simple return to a log return.

        r_log = ln(1 + r_simple)

        Args:
            simple_ret: The simple return as a decimal.

        Returns:
            The equivalent log return.

        Raises:
            ValueError: If simple_ret <= -1 (total loss or worse).
        """
        if simple_ret <= -1.0:
            raise ValueError("simple_ret must be greater than -1.")
        return math.log(1.0 + simple_ret)


# ---------------------------------------------------------------------------
# Demonstration
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    calc = Returns()

    print("=" * 60)
    print("Return Calculations - Reference Implementation Demo")
    print("=" * 60)

    # 1. Holding Period Return
    hpr = calc.holding_period_return(begin_value=100_000, end_value=108_000, distributions=2_000)
    print(f"\n1. Holding Period Return: {hpr:.4%}")
    print(f"   (Invested $100k, ended at $108k, received $2k dividends)")

    # 2. Time-Weighted Return
    sub_returns = [0.05, -0.02, 0.03, 0.04]
    twr = calc.time_weighted_return(sub_returns)
    print(f"\n2. Time-Weighted Return: {twr:.4%}")
    print(f"   Sub-period returns: {sub_returns}")

    # 3. Money-Weighted Return (IRR)
    # Invest $100k at t=0, add $50k at t=1, end value $165k at t=2
    cash_flows = [(0, -100_000), (1, -50_000), (2, 165_000)]
    mwr = calc.money_weighted_return(cash_flows)
    print(f"\n3. Money-Weighted Return (IRR): {mwr:.4%}")
    print(f"   Cash flows: {cash_flows}")

    # 4. CAGR
    cagr_val = calc.cagr(begin_value=100_000, end_value=160_000, years=5)
    print(f"\n4. CAGR (5 years, $100k -> $160k): {cagr_val:.4%}")

    # 5. Annualization
    monthly_return = 0.08  # 8% over 6 months
    ann = calc.annualize(total_return=monthly_return, periods=6, periods_per_year=12)
    print(f"\n5. Annualized Return (8% in 6 months): {ann:.4%}")

    # 6. Linking Returns
    monthly_rets = [0.01, 0.02, -0.005, 0.015, 0.008, -0.01]
    linked = calc.link_returns(monthly_rets)
    print(f"\n6. Linked Return (6 months): {linked:.4%}")
    print(f"   Monthly returns: {monthly_rets}")

    # 7. Arithmetic vs Geometric Mean
    returns = [0.10, -0.05, 0.08, -0.03, 0.12]
    arith = calc.arithmetic_mean(returns)
    geom = calc.geometric_mean(returns)
    std = float(np.std(returns, ddof=0))
    print(f"\n7. Arithmetic Mean: {arith:.4%}")
    print(f"   Geometric Mean:  {geom:.4%}")
    print(f"   Difference:      {arith - geom:.4%}")
    print(f"   sigma^2 / 2:     {std**2 / 2:.4%}")

    # 8. Log Returns
    log_r = calc.log_return(begin_value=100, end_value=110)
    simple_r = calc.log_to_simple(log_r)
    back_to_log = calc.simple_to_log(simple_r)
    print(f"\n8. Log Return ($100 -> $110):   {log_r:.6f}")
    print(f"   Converted to simple:         {simple_r:.6f}")
    print(f"   Converted back to log:       {back_to_log:.6f}")

    print("\n" + "=" * 60)
    print("All calculations completed successfully.")
    print("=" * 60)
