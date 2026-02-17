"""
Time Value of Money - Layer 0 (Mathematical Foundations)

A comprehensive reference implementation for present value, future value,
NPV, IRR, annuities, perpetuities, amortization schedules, and compounding
conventions.

Usage:
    python time_value_of_money.py

Dependencies:
    numpy
"""

import math

import numpy as np


# ---------------------------------------------------------------------------
# Core TVM Functions
# ---------------------------------------------------------------------------

def present_value(future_value: float, rate: float, periods: float) -> float:
    """Compute the present value of a future cash flow.

    PV = FV / (1 + r)^n

    Args:
        future_value: The future cash flow amount.
        rate: Discount rate per period (as a decimal, e.g., 0.05 for 5%).
        periods: Number of compounding periods.

    Returns:
        The present value.
    """
    return future_value / (1.0 + rate) ** periods


def future_value(present_val: float, rate: float, periods: float) -> float:
    """Compute the future value of a present amount.

    FV = PV * (1 + r)^n

    Args:
        present_val: The current value / principal.
        rate: Interest rate per period (as a decimal).
        periods: Number of compounding periods.

    Returns:
        The future value.
    """
    return present_val * (1.0 + rate) ** periods


def npv(rate: float, cash_flows: list[float]) -> float:
    """Compute the Net Present Value of a series of cash flows.

    NPV = sum( CF_t / (1 + r)^t )  for t = 0, 1, 2, ...

    Args:
        rate: Discount rate per period (as a decimal).
        cash_flows: List of cash flows starting at t=0. Negative values
            represent outflows (investments), positive values represent
            inflows.

    Returns:
        The net present value.
    """
    total = 0.0
    for t, cf in enumerate(cash_flows):
        total += cf / (1.0 + rate) ** t
    return total


def irr(cash_flows: list[float], guess: float = 0.1) -> float:
    """Compute the Internal Rate of Return using Newton's method.

    Finds the rate r such that NPV(r) = 0.

    Args:
        cash_flows: List of cash flows starting at t=0. Typically the first
            value is negative (initial investment) and subsequent values
            are positive (returns).
        guess: Initial guess for the rate. Defaults to 0.1 (10%).

    Returns:
        The IRR as a decimal.

    Raises:
        RuntimeError: If Newton's method fails to converge.
    """
    rate = guess
    max_iterations = 1000
    tolerance = 1e-10

    for _ in range(max_iterations):
        npv_val = 0.0
        npv_deriv = 0.0
        for t, cf in enumerate(cash_flows):
            discount = (1.0 + rate) ** t
            npv_val += cf / discount
            if t > 0:
                npv_deriv -= t * cf / ((1.0 + rate) ** (t + 1))

        if abs(npv_val) < tolerance:
            return rate

        if abs(npv_deriv) < 1e-15:
            raise RuntimeError(
                "Newton's method derivative near zero; try a different guess."
            )

        rate = rate - npv_val / npv_deriv

    raise RuntimeError(
        f"Newton's method did not converge after {max_iterations} iterations."
    )


def annuity_pv(
    payment: float,
    rate: float,
    periods: int,
    due: bool = False,
) -> float:
    """Compute the present value of an annuity.

    Ordinary annuity (due=False):
        PV = PMT * [1 - (1 + r)^(-n)] / r

    Annuity due (due=True):
        PV = PMT * [1 - (1 + r)^(-n)] / r * (1 + r)

    Args:
        payment: The periodic payment amount.
        rate: Interest rate per period (as a decimal).
        periods: Total number of payment periods.
        due: If True, payments occur at the beginning of each period
            (annuity due). Defaults to False (ordinary annuity).

    Returns:
        The present value of the annuity.
    """
    if rate == 0:
        return payment * periods * (1.0 + rate if due else 1.0)
    pv = payment * (1.0 - (1.0 + rate) ** (-periods)) / rate
    if due:
        pv *= (1.0 + rate)
    return pv


def annuity_fv(
    payment: float,
    rate: float,
    periods: int,
    due: bool = False,
) -> float:
    """Compute the future value of an annuity.

    Ordinary annuity (due=False):
        FV = PMT * [(1 + r)^n - 1] / r

    Annuity due (due=True):
        FV = PMT * [(1 + r)^n - 1] / r * (1 + r)

    Args:
        payment: The periodic payment amount.
        rate: Interest rate per period (as a decimal).
        periods: Total number of payment periods.
        due: If True, payments occur at the beginning of each period.
            Defaults to False.

    Returns:
        The future value of the annuity.
    """
    if rate == 0:
        return payment * periods * (1.0 + rate if due else 1.0)
    fv = payment * ((1.0 + rate) ** periods - 1.0) / rate
    if due:
        fv *= (1.0 + rate)
    return fv


def growing_annuity_pv(
    payment: float,
    rate: float,
    growth_rate: float,
    periods: int,
) -> float:
    """Compute the present value of a growing annuity.

    PV = PMT / (r - g) * [1 - ((1 + g) / (1 + r))^n]

    Args:
        payment: The first period's payment amount.
        rate: Discount rate per period (as a decimal).
        growth_rate: Growth rate of payments per period (as a decimal).
        periods: Total number of payment periods.

    Returns:
        The present value of the growing annuity.

    Raises:
        ValueError: If rate equals growth_rate (use annuity_pv instead).
    """
    if abs(rate - growth_rate) < 1e-12:
        # When r == g, PV = PMT * n / (1 + r)
        return payment * periods / (1.0 + rate)
    return (
        payment
        / (rate - growth_rate)
        * (1.0 - ((1.0 + growth_rate) / (1.0 + rate)) ** periods)
    )


def perpetuity_pv(
    payment: float,
    rate: float,
    growth_rate: float = 0.0,
) -> float:
    """Compute the present value of a perpetuity.

    Constant perpetuity:    PV = PMT / r
    Growing perpetuity:     PV = PMT / (r - g),  requires r > g

    Args:
        payment: The periodic payment amount (first payment for growing).
        rate: Discount rate per period (as a decimal).
        growth_rate: Growth rate of payments (as a decimal). Defaults to 0.

    Returns:
        The present value of the perpetuity.

    Raises:
        ValueError: If rate <= growth_rate (PV would be infinite or negative).
    """
    if rate <= growth_rate:
        raise ValueError(
            f"rate ({rate}) must be greater than growth_rate ({growth_rate}) "
            "for a finite perpetuity value."
        )
    return payment / (rate - growth_rate)


def fisher_rate(nominal: float, inflation: float) -> float:
    """Compute the real rate of return using the Fisher equation.

    r_real = (1 + r_nominal) / (1 + inflation) - 1

    Args:
        nominal: The nominal interest rate (as a decimal).
        inflation: The inflation rate (as a decimal).

    Returns:
        The real rate of return as a decimal.
    """
    return (1.0 + nominal) / (1.0 + inflation) - 1.0


def continuous_compounding(rate: float, time: float) -> float:
    """Compute the growth factor under continuous compounding.

    Growth factor = e^(r * t)

    Multiply by the principal to get the future value:
        FV = PV * e^(r * t)

    Args:
        rate: The continuously compounded annual rate (as a decimal).
        time: Time in years.

    Returns:
        The growth factor (not the future value).
    """
    return math.exp(rate * time)


# ---------------------------------------------------------------------------
# Amortization Schedule
# ---------------------------------------------------------------------------

class AmortizationSchedule:
    """Generate a full amortization schedule for a fixed-rate loan.

    Each period's payment is split into interest and principal components.
    Early payments are interest-heavy; later payments are principal-heavy.

    Args:
        principal: The initial loan amount.
        annual_rate: The annual interest rate (as a decimal, e.g., 0.06).
        periods: Total number of payment periods.
        periods_per_year: Number of payment periods per year (default 12
            for monthly payments).
    """

    def __init__(
        self,
        principal: float,
        annual_rate: float,
        periods: int,
        periods_per_year: int = 12,
    ) -> None:
        self.principal = principal
        self.annual_rate = annual_rate
        self.periods = periods
        self.periods_per_year = periods_per_year
        self.periodic_rate = annual_rate / periods_per_year

    def _compute_payment(self) -> float:
        """Compute the fixed periodic payment.

        PMT = PV * r / [1 - (1 + r)^(-n)]
        """
        r = self.periodic_rate
        n = self.periods
        if r == 0:
            return self.principal / n
        return self.principal * r / (1.0 - (1.0 + r) ** (-n))

    def schedule(self) -> list[dict]:
        """Generate the full amortization schedule.

        Returns:
            A list of dictionaries, one per period, each containing:
                - period: int (1-indexed)
                - payment: float
                - principal_payment: float
                - interest_payment: float
                - remaining_balance: float
        """
        payment = self._compute_payment()
        balance = self.principal
        rows: list[dict] = []

        for period_num in range(1, self.periods + 1):
            interest = balance * self.periodic_rate
            principal_pmt = payment - interest

            # Handle final period rounding
            if period_num == self.periods:
                principal_pmt = balance
                payment = principal_pmt + interest

            balance -= principal_pmt

            rows.append({
                "period": period_num,
                "payment": round(payment, 2),
                "principal_payment": round(principal_pmt, 2),
                "interest_payment": round(interest, 2),
                "remaining_balance": round(max(balance, 0.0), 2),
            })

        return rows

    def total_interest(self) -> float:
        """Compute the total interest paid over the life of the loan.

        Returns:
            The sum of all interest payments.
        """
        return sum(row["interest_payment"] for row in self.schedule())

    def total_payments(self) -> float:
        """Compute the total amount paid over the life of the loan.

        Returns:
            The sum of all payments (principal + interest).
        """
        return sum(row["payment"] for row in self.schedule())


# ---------------------------------------------------------------------------
# Demonstration
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 60)
    print("Time Value of Money - Reference Implementation Demo")
    print("=" * 60)

    # 1. Present Value
    pv = present_value(future_value=10_000, rate=0.05, periods=10)
    print(f"\n1. PV of $10,000 in 10 years at 5%: ${pv:,.2f}")

    # 2. Future Value
    fv = future_value(present_val=10_000, rate=0.05, periods=10)
    print(f"2. FV of $10,000 in 10 years at 5%: ${fv:,.2f}")

    # 3. NPV
    cfs = [-100_000, 30_000, 35_000, 40_000, 45_000]
    npv_val = npv(rate=0.10, cash_flows=cfs)
    print(f"\n3. NPV at 10%: ${npv_val:,.2f}")
    print(f"   Cash flows: {cfs}")

    # 4. IRR
    irr_val = irr(cash_flows=cfs)
    print(f"4. IRR: {irr_val:.4%}")
    print(f"   Verification NPV at IRR: ${npv(irr_val, cfs):,.6f}")

    # 5. Annuity PV
    ordinary = annuity_pv(payment=1_000, rate=0.05, periods=20)
    due = annuity_pv(payment=1_000, rate=0.05, periods=20, due=True)
    print(f"\n5. PV of $1,000/yr annuity, 20 years, 5%:")
    print(f"   Ordinary: ${ordinary:,.2f}")
    print(f"   Due:      ${due:,.2f}")

    # 6. Annuity FV
    fv_ord = annuity_fv(payment=500, rate=0.06, periods=30)
    print(f"\n6. FV of $500/yr ordinary annuity, 30 years, 6%: ${fv_ord:,.2f}")

    # 7. Growing Annuity
    ga = growing_annuity_pv(payment=50_000, rate=0.08, growth_rate=0.03, periods=25)
    print(f"\n7. PV of growing annuity ($50k, 3% growth, 8% discount, 25 yr): ${ga:,.2f}")

    # 8. Perpetuity
    perp = perpetuity_pv(payment=10_000, rate=0.05)
    grow_perp = perpetuity_pv(payment=10_000, rate=0.05, growth_rate=0.02)
    print(f"\n8. Perpetuity ($10k/yr at 5%):         ${perp:,.2f}")
    print(f"   Growing perpetuity (2% growth):     ${grow_perp:,.2f}")

    # 9. Fisher Equation
    real = fisher_rate(nominal=0.07, inflation=0.03)
    print(f"\n9. Real rate (7% nominal, 3% inflation): {real:.4%}")

    # 10. Continuous Compounding
    factor = continuous_compounding(rate=0.05, time=10)
    print(f"10. Continuous compounding factor (5%, 10yr): {factor:.6f}")
    print(f"    FV of $10,000: ${10_000 * factor:,.2f}")

    # 11. Amortization Schedule
    print(f"\n11. Amortization Schedule: $250,000 mortgage, 6% annual, 360 months")
    amort = AmortizationSchedule(
        principal=250_000, annual_rate=0.06, periods=360, periods_per_year=12
    )
    sched = amort.schedule()

    print(f"    Monthly Payment: ${sched[0]['payment']:,.2f}")
    print(f"    Total Interest:  ${amort.total_interest():,.2f}")
    print(f"    Total Payments:  ${amort.total_payments():,.2f}")
    print(f"\n    First 5 periods:")
    print(f"    {'Period':>6} {'Payment':>10} {'Interest':>10} {'Principal':>10} {'Balance':>12}")
    for row in sched[:5]:
        print(
            f"    {row['period']:>6} "
            f"${row['payment']:>9,.2f} "
            f"${row['interest_payment']:>9,.2f} "
            f"${row['principal_payment']:>9,.2f} "
            f"${row['remaining_balance']:>11,.2f}"
        )
    print(f"    ...")
    print(f"    Last 3 periods:")
    for row in sched[-3:]:
        print(
            f"    {row['period']:>6} "
            f"${row['payment']:>9,.2f} "
            f"${row['interest_payment']:>9,.2f} "
            f"${row['principal_payment']:>9,.2f} "
            f"${row['remaining_balance']:>11,.2f}"
        )

    print("\n" + "=" * 60)
    print("All calculations completed successfully.")
    print("=" * 60)
