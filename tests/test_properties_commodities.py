"""Property-based tests for the commodities skill script."""

import math

import numpy as np
from hypothesis import given
from hypothesis import strategies as st

from conftest import load_script

commodities = load_script("commodities")

FP = commodities.FuturesPricing
CurveAnalysis = commodities.CurveAnalysis
RD = commodities.ReturnDecomposition

# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

spot = st.floats(1.0, 5000.0, allow_nan=False)
rate = st.floats(0.0, 0.10, allow_nan=False)
storage = st.floats(0.0, 0.15, allow_nan=False)
conv = st.floats(0.0, 0.30, allow_nan=False)
tenor = st.floats(0.02, 5.0, allow_nan=False)
fut_price = st.floats(1.0, 5000.0, allow_nan=False)


def close(a: float, b: float, rel: float = 1e-9, abs_: float = 1e-9) -> bool:
    return math.isclose(a, b, rel_tol=rel, abs_tol=abs_)


# ---------------------------------------------------------------------------
# Cost of carry
# ---------------------------------------------------------------------------

@given(spot, rate, storage, conv)
def test_futures_converge_to_spot_at_expiry(s, r, u, y):
    # With no time left there is no carry, so F = S.
    assert close(FP.theoretical_futures_price(s, r, u, y, 0.0), s)


@given(spot, rate, storage, conv, tenor)
def test_contango_iff_carry_exceeds_convenience_yield(s, r, u, y, t):
    # F > S exactly when net carry r + u - y is positive (contango), F < S
    # when it is negative (backwardation).
    f = FP.theoretical_futures_price(s, r, u, y, t)
    net = r + u - y
    if net > 1e-12:
        assert f > s
    elif net < -1e-12:
        assert f < s


@given(spot, rate, storage, conv, tenor, tenor)
def test_carry_compounds_across_tenors(s, r, u, y, t1, t2):
    # Continuous carry is multiplicative: carrying to t1 then on for t2 gives
    # the same price as carrying straight to t1 + t2.
    f1 = FP.theoretical_futures_price(s, r, u, y, t1)
    f12 = FP.theoretical_futures_price(f1, r, u, y, t2)
    assert close(f12, FP.theoretical_futures_price(s, r, u, y, t1 + t2), rel=1e-12)


@given(spot, rate, storage, conv, tenor)
def test_implied_convenience_yield_round_trips(s, r, u, y, t):
    # Backing the convenience yield out of the model price recovers it.
    f = FP.theoretical_futures_price(s, r, u, y, t)
    assert close(FP.implied_convenience_yield(s, f, r, u, t), y, abs_=1e-10)


@given(spot, fut_price, fut_price, rate, storage, tenor)
def test_higher_futures_price_implies_lower_convenience_yield(s, f1, f2, r, u, t):
    # Holding carry costs fixed, a richer futures price means the market
    # assigns less benefit to holding the physical.
    lo, hi = sorted((f1, f2))
    assert (FP.implied_convenience_yield(s, hi, r, u, t)
            <= FP.implied_convenience_yield(s, lo, r, u, t))


# ---------------------------------------------------------------------------
# Curve analysis
# ---------------------------------------------------------------------------

@given(fut_price, st.floats(-0.3, 0.3), st.floats(7.0, 400.0))
def test_roll_yield_sign_matches_curve_shape(near, slope, days):
    # Roll yield is negative in contango, positive in backwardation, and the
    # annualized figure has the same sign as the per-roll figure. Adjacent
    # contracts are kept within 30% of each other and at least a week apart
    # so the (near/far)^(365/days) annualization stays within float range.
    far = near * (1.0 + slope)
    ca = CurveAnalysis(np.array([near, far]), np.array([days]))
    ry = ca.front_roll_yield()
    ann = ca.annualized_roll_yield()
    if far > near:
        assert ca.is_contango() and not ca.is_backwardation()
        assert ry < 0 and ann < 0
        assert ca.curve_shape() == "contango"
    elif near > far:
        assert ca.is_backwardation() and not ca.is_contango()
        assert ry > 0 and ann > 0
        assert ca.curve_shape() == "backwardation"
    else:
        assert ry == 0 and ann == 0


@given(st.lists(fut_price, min_size=2, max_size=12))
def test_term_structure_front_row_matches_front_metrics(prices):
    # The first row of the term structure is the front-to-second roll.
    ca = CurveAnalysis(np.array(prices))
    ts = ca.term_structure()
    assert len(ts) == len(prices) - 1
    assert close(ts[0]["roll_yield"], ca.front_roll_yield())
    assert close(ts[0]["annualized_roll_yield"], ca.annualized_roll_yield())


@given(st.lists(fut_price, min_size=2, max_size=12, unique=True))
def test_curve_shape_is_monotone_classification(prices):
    # Strictly increasing prices are contango, strictly decreasing are
    # backwardation, regardless of the curve length.
    up = CurveAnalysis(np.array(sorted(prices)))
    down = CurveAnalysis(np.array(sorted(prices, reverse=True)))
    assert up.curve_shape() == "contango"
    assert down.curve_shape() == "backwardation"


# ---------------------------------------------------------------------------
# Return decomposition
# ---------------------------------------------------------------------------

@given(spot, spot, st.floats(-0.5, 0.5), rate)
def test_decomposition_components_sum_to_total(s0, s1, ry, rf):
    # Total = spot return + roll yield + collateral yield, and decompose
    # agrees with total_return and multi_period_spot_return.
    d = RD.decompose(s0, s1, ry, rf)
    assert close(d["total_return"],
                 d["spot_return"] + d["roll_yield"] + d["collateral_yield"], abs_=1e-12)
    assert close(d["total_return"], RD.total_return(d["spot_return"], ry, rf), abs_=1e-12)
    assert close(d["spot_return"], RD.multi_period_spot_return(np.array([s0, s1])),
                 abs_=1e-12)


@given(st.lists(spot, min_size=2, max_size=30))
def test_multi_period_spot_return_links_period_returns(prices):
    # Cumulative return equals the product of period gross returns minus 1.
    p = np.array(prices)
    linked = float(np.prod(p[1:] / p[:-1]) - 1.0)
    assert close(RD.multi_period_spot_return(p), linked, rel=1e-9, abs_=1e-9)
