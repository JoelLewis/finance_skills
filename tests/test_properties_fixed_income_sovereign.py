"""Property-based tests for the fixed-income-sovereign script.

Complements the four sovereign properties in test_properties.py (price falls
as yield rises, par pricing, modified duration as price sensitivity,
Macaulay duration within maturity) with the remaining bond and yield-curve
analytics.
"""

import math

import numpy as np
from hypothesis import assume, given
from hypothesis import strategies as st

from conftest import load_script

sovereign = load_script("fixed-income-sovereign")
Bond = sovereign.SovereignBond
YieldCurve = sovereign.YieldCurve

# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

coupon_rate = st.floats(0.0, 0.15)
maturity = st.integers(1, 60).map(lambda h: h / 2)   # 0.5 to 30 years
frequency = st.sampled_from([1, 2, 4, 12])
yield_ = st.floats(0.0001, 0.20)
face = st.floats(100.0, 1e7)

# Curve nodes on the semi-annual grid out to 30 years.
NODES = np.array([0.5, 1.0, 2.0, 3.0, 5.0, 7.0, 10.0, 20.0, 30.0])


@st.composite
def par_curve(draw):
    """Par yields at NODES: a starting level plus moves of at most 50bp per node.

    Arbitrary independent par yields are not a valid curve: e.g. 12.5% flat to
    20y then 14% at 30y implies a negative 20y-30y discount factor, so no
    bootstrap exists. Bounded node-to-node moves keep the curve arbitrage-free.
    """
    start = draw(st.floats(0.005, 0.12))
    steps = draw(st.lists(st.floats(-0.005, 0.005), min_size=len(NODES) - 1,
                          max_size=len(NODES) - 1))
    par = start + np.concatenate([[0.0], np.cumsum(steps)])
    return np.maximum(par, 0.001)


def close(a: float, b: float, rel: float = 1e-9, abs_: float = 1e-9) -> bool:
    return math.isclose(a, b, rel_tol=rel, abs_tol=abs_)


def make_bond(c, m, f, fv=1000.0):
    bond = Bond(fv, c, m, f)
    assume(bond.n_periods >= 1)  # e.g. 0.5y annual-pay has no coupon dates
    return bond


# ---------------------------------------------------------------------------
# SovereignBond
# ---------------------------------------------------------------------------

@given(coupon_rate, maturity, frequency, yield_)
def test_ytm_inverts_price(c, m, f, y):
    # Solving for the yield that reproduces price(y) must return y.
    bond = make_bond(c, m, f)
    assert close(bond.ytm(bond.price(y)), y, rel=1e-7, abs_=1e-9)


@given(coupon_rate, maturity, frequency, yield_)
def test_convexity_is_second_derivative_over_price(c, m, f, y):
    # Convexity = (d2P/dy2) / P with y the annual yield.
    bond = make_bond(c, m, f)
    h = 1e-4
    p0 = bond.price(y)
    second = (bond.price(y + h) - 2 * p0 + bond.price(y - h)) / h ** 2
    assert close(bond.convexity(y), second / p0, rel=1e-4)


@given(coupon_rate, maturity, frequency, yield_)
def test_dv01_matches_one_basis_point_reprice(c, m, f, y):
    # DV01 is the price drop for a 1bp rise, to first order: compare with the
    # symmetric 1bp finite difference (error is third order, far below 1e-5).
    bond = make_bond(c, m, f)
    bp = 1e-4
    fd = (bond.price(y - bp) - bond.price(y + bp)) / 2
    assert close(bond.dv01(y), fd, rel=1e-5)


@given(coupon_rate, maturity, frequency, yield_, st.floats(-0.01, 0.01))
def test_convexity_improves_duration_estimate(c, m, f, y, dy):
    # For yield moves up to 100bp, adding the convexity term brings the
    # estimate closer to the full reprice than duration alone, and the
    # components sum to the total.
    assume(abs(dy) > 1e-6)
    bond = make_bond(c, m, f)
    p0, p1 = bond.price(y), bond.price(y + dy)
    est = bond.price_change_estimate(y, dy)
    assert close(est["total_pct_change"],
                 est["duration_effect"] + est["convexity_effect"], abs_=1e-15)
    assert est["convexity_effect"] >= 0
    assert est["duration_effect"] * dy < 0
    duration_only = p0 * (1 + est["duration_effect"])
    assert abs(est["estimated_new_price"] - p1) <= abs(duration_only - p1) + 1e-9 * p0


@given(coupon_rate, maturity, frequency, yield_, face)
def test_price_scales_with_face_and_durations_do_not(c, m, f, y, fv):
    # Doubling the position doubles price and DV01; duration and convexity
    # are per-dollar measures and do not change.
    unit = make_bond(c, m, f, 1.0)
    big = make_bond(c, m, f, fv)
    assert close(big.price(y), fv * unit.price(y), rel=1e-12)
    assert close(big.dv01(y), fv * unit.dv01(y), rel=1e-12)
    assert close(big.modified_duration(y), unit.modified_duration(y), rel=1e-12)
    assert close(big.convexity(y), unit.convexity(y), rel=1e-12)


@given(st.floats(0.001, 0.15), maturity, frequency, yield_)
def test_current_yield_lies_between_coupon_and_ytm(c, m, f, y):
    # Premium bond: coupon > current yield > YTM; discount bond: the reverse.
    assume(abs(c - y) > 1e-6)
    bond = make_bond(c, m, f)
    cy = bond.current_yield(bond.price(y))
    lo, hi = sorted((c, y))
    assert lo - 1e-12 <= cy <= hi + 1e-12


@given(maturity, frequency, yield_)
def test_zero_coupon_macaulay_duration_equals_maturity(m, f, y):
    # A zero has a single cash flow, so its Macaulay duration is its maturity
    # and its price is the face discounted over n periods.
    bond = make_bond(0.0, m, f)
    t = bond.n_periods / f
    assert close(bond.macaulay_duration(y), t, rel=1e-12)
    assert close(bond.price(y), 1000.0 / (1 + y / f) ** bond.n_periods, rel=1e-12)


# ---------------------------------------------------------------------------
# YieldCurve
# ---------------------------------------------------------------------------

@given(par_curve())
def test_bootstrapped_curve_reprices_input_par_bonds(par):
    # Bootstrapping is exact: each input par bond is worth 1.0 off the curve.
    curve = YieldCurve(NODES, par)
    for mat, py in zip(NODES, par):
        assert close(curve.price_par_bond(mat, py), 1.0, abs_=1e-9)


@given(st.floats(0.001, 0.15), st.floats(0.0, 29.5), st.floats(0.25, 30.0))
def test_flat_par_curve_has_equal_spot_and_forward_rates(r, t1, length):
    # With a flat par curve every spot and forward rate equals the par yield
    # (all on the same semi-annual convention).
    curve = YieldCurve(NODES, np.full(len(NODES), r))
    assert np.allclose(curve.spot_rates, r, rtol=0, atol=1e-10)
    t2 = min(t1 + length, 30.0)
    assume(t2 - t1 > 0.1)
    assert close(curve.forward_rate(t1, t2), r, abs_=1e-9)


@given(st.floats(0.001, 0.10), st.lists(st.floats(0.0, 0.005),
       min_size=len(NODES) - 1, max_size=len(NODES) - 1))
def test_upward_par_curve_puts_spot_at_or_above_par(start, steps):
    # On an upward-sloping par curve the zero rate is at or above the par
    # yield at every maturity (coupons are discounted at lower short rates).
    par = start + np.concatenate([[0.0], np.cumsum(steps)])
    curve = YieldCurve(NODES, par)
    assert np.all(curve.spot_rates >= par - 1e-10)


@given(par_curve(), st.floats(0.0, 29.0), st.floats(0.5, 15.0), st.floats(0.5, 15.0))
def test_forward_rates_chain_discount_factors(par, t1, a, b):
    # No-arbitrage: investing to t1, then forward to t2, then forward to t3
    # must equal the direct t1 -> t3 forward (compounded semi-annually).
    t2 = min(t1 + a, 29.75)
    t3 = min(t2 + b, 30.0)
    assume(t2 - t1 > 0.1 and t3 - t2 > 0.1)
    curve = YieldCurve(NODES, par)
    g12 = (1 + curve.forward_rate(t1, t2) / 2) ** (2 * (t2 - t1))
    g23 = (1 + curve.forward_rate(t2, t3) / 2) ** (2 * (t3 - t2))
    g13 = (1 + curve.forward_rate(t1, t3) / 2) ** (2 * (t3 - t1))
    assert close(g12 * g23, g13, rel=1e-10)
    assert close(curve.discount_factor(t1) / curve.discount_factor(t3), g13, rel=1e-10)
