"""Property-based tests for the fund-vehicles skill script."""

import math

import numpy as np
from hypothesis import given
from hypothesis import strategies as st

from conftest import load_script

fund_vehicles = load_script("fund-vehicles")

EA = fund_vehicles.ExpenseAnalysis
TrackingAnalysis = fund_vehicles.TrackingAnalysis
NAV = fund_vehicles.NAVAnalysis
FundOverlap = fund_vehicles.FundOverlap
TE = fund_vehicles.TaxEfficiency

# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

amount = st.floats(1e3, 1e7, allow_nan=False)
gross = st.floats(0.0, 0.15, allow_nan=False)
fee = st.floats(0.0, 0.025, allow_nan=False)
years = st.integers(1, 50)
tax_rate = st.floats(0.0, 0.5, allow_nan=False)
price = st.floats(1.0, 1000.0, allow_nan=False)
period_ret = st.floats(-0.05, 0.05, allow_nan=False)


def close(a: float, b: float, rel: float = 1e-9, abs_: float = 1e-9) -> bool:
    return math.isclose(a, b, rel_tol=rel, abs_tol=abs_)


@st.composite
def holdings(draw):
    """Two funds with fully-invested weights over a shared name universe."""
    names = [f"T{i}" for i in range(draw(st.integers(1, 15)))]
    out = []
    for _ in range(2):
        held = [n for n in names if draw(st.booleans())] or names[:1]
        raw = np.array(draw(st.lists(st.floats(0.01, 1.0),
                                     min_size=len(held), max_size=len(held))))
        out.append(dict(zip(held, (raw / raw.sum()).tolist())))
    return out


# ---------------------------------------------------------------------------
# Expense drag
# ---------------------------------------------------------------------------

@given(amount, gross, fee, years)
def test_net_terminal_never_exceeds_gross(v0, g, er, n):
    # Fees can only reduce wealth; drag is zero exactly when the fee is zero.
    res = EA.fee_impact(v0, g, er, n)
    assert res["terminal_value"] <= res["gross_terminal_value"]
    assert res["total_fee_drag"] >= 0
    assert 0 <= res["fee_drag_pct"] <= 1
    if er == 0:
        assert res["total_fee_drag"] == 0


@given(amount, gross, fee, fee, years, st.integers(1, 20))
def test_fee_drag_grows_with_fee_and_horizon(v0, g, er1, er2, n, extra):
    # A higher expense ratio, or a longer horizon, loses a larger share of
    # gross terminal wealth to fees.
    lo, hi = sorted((er1, er2))
    pct = lambda er, yrs: EA.fee_impact(v0, g, er, yrs)["fee_drag_pct"]
    assert pct(hi, n) >= pct(lo, n) - 1e-12
    assert pct(hi, n + extra) >= pct(hi, n) - 1e-12


@given(amount, gross, st.lists(fee, min_size=1, max_size=8), years)
def test_compare_funds_cheapest_has_zero_drag(v0, g, ers, n):
    # Ranking by terminal value matches ranking by fee; the cheapest fund
    # has zero drag versus cheapest and matches fee_impact.
    names = [f"F{i}" for i in range(len(ers))]
    res = EA.compare_funds(v0, g, ers, names, n)
    cheapest = min(res, key=lambda r: r["expense_ratio"])
    assert cheapest["fee_drag_vs_cheapest"] == 0
    for r in res:
        assert r["fee_drag_vs_cheapest"] >= 0
        assert close(r["terminal_value"],
                     EA.fee_impact(v0, g, r["expense_ratio"], n)["terminal_value"])


@given(fee, fee, st.floats(-0.03, 0.03), gross)
def test_breakeven_exists_iff_alpha_beats_fee_gap(er_a, er_b, alpha, g):
    # The active fund can only catch up when its alpha exceeds the extra fee.
    be = EA.breakeven_years(er_a, er_b, alpha, g)
    net_gap = (g + alpha - er_a) - (g - er_b)
    if net_gap > 1e-12:
        assert be is not None and be >= 0
    elif net_gap < -1e-12:
        assert be is None


# ---------------------------------------------------------------------------
# Tracking
# ---------------------------------------------------------------------------

@given(st.data(), st.integers(2, 60))
def test_perfect_replication_has_zero_tracking(data, n):
    # A fund whose returns equal the index has zero tracking difference,
    # tracking error and information ratio.
    r = np.array(data.draw(st.lists(period_ret, min_size=n, max_size=n)))
    ta = TrackingAnalysis(r, r.copy())
    assert ta.tracking_difference() == 0
    assert ta.tracking_error() == 0
    assert ta.information_ratio() == 0


@given(st.data(), st.integers(3, 60), st.floats(-0.001, 0.001))
def test_constant_return_gap_has_zero_tracking_error(data, n, gap):
    # A constant per-period shortfall (e.g. a fee) shifts the mean active
    # return but adds no tracking error. Tracking error is shift-invariant.
    idx = np.array(data.draw(st.lists(period_ret, min_size=n, max_size=n)))
    noise = np.array(data.draw(st.lists(st.floats(-0.01, 0.01), min_size=n, max_size=n)))
    base = TrackingAnalysis(idx + noise, idx)
    shifted = TrackingAnalysis(idx + noise + gap, idx)
    assert close(shifted.mean_active_return(), base.mean_active_return() + gap,
                 abs_=1e-12)
    assert close(shifted.tracking_error(), base.tracking_error(), rel=1e-6, abs_=1e-9)
    assert TrackingAnalysis(idx + gap, idx).tracking_error() < 1e-9


# ---------------------------------------------------------------------------
# NAV premium / discount
# ---------------------------------------------------------------------------

@given(price, price)
def test_premium_zero_at_nav_and_sign(p, nav):
    # Trading at NAV is zero premium; the sign follows price versus NAV.
    assert NAV.premium_discount(nav, nav) == 0.0
    pd = NAV.premium_discount(p, nav)
    assert (pd > 0) == (p > nav) and (pd < 0) == (p < nav)


@given(st.lists(st.tuples(price, price), min_size=2, max_size=50))
def test_premium_series_bounds(pairs):
    # The series statistics bracket each observation and agree pointwise
    # with the single-observation function.
    p = np.array([a for a, _ in pairs])
    nav = np.array([b for _, b in pairs])
    s = NAV.premium_discount_series(p, nav)
    assert s["max_discount"] <= s["mean_premium"] + 1e-12
    assert s["mean_premium"] <= s["max_premium"] + 1e-12
    for i in range(len(p)):
        assert close(s["premiums"][i], NAV.premium_discount(p[i], nav[i]))


@given(st.floats(1e6, 1e10), st.floats(0.0, 0.5), st.floats(1e3, 1e8))
def test_nav_per_share_times_shares_is_net_assets(assets, liab_share, shares):
    # NAV per share * shares outstanding recovers net assets.
    liab = assets * liab_share
    assert close(NAV.nav_per_share(assets, liab, shares) * shares, assets - liab,
                 rel=1e-12)


# ---------------------------------------------------------------------------
# Overlap
# ---------------------------------------------------------------------------

@given(holdings())
def test_overlap_is_symmetric_and_bounded(hs):
    # Overlap is symmetric, lies in [0, 1], is 1 for a fund with itself, and
    # cannot exceed the shared weight held by either fund.
    a, b = hs
    ov = FundOverlap.overlap_coefficient(a, b)
    assert close(ov, FundOverlap.overlap_coefficient(b, a), abs_=1e-15)
    assert -1e-12 <= ov <= 1 + 1e-12
    assert close(FundOverlap.overlap_coefficient(a, a), 1.0, abs_=1e-12)
    d = FundOverlap.overlap_detail(a, b)
    assert close(d["overlap_coefficient"], ov)
    assert ov <= min(d["shared_weight_a"], d["shared_weight_b"]) + 1e-12
    assert d["shared_count"] + d["unique_to_a"] + d["unique_to_b"] == d["total_unique"]


# ---------------------------------------------------------------------------
# Tax efficiency
# ---------------------------------------------------------------------------

@given(st.floats(-0.3, 0.4), st.floats(-0.3, 0.4))
def test_tax_cost_ratio_round_trip(pre, post):
    # 1 + after-tax = (1 + pre-tax)(1 - tax cost ratio); zero when equal.
    tcr = TE.tax_cost_ratio(pre, post)
    assert close((1 + pre) * (1 - tcr), 1 + post, abs_=1e-12)
    assert TE.tax_cost_ratio(pre, pre) == 0


@given(amount, st.floats(0.01, 0.15), fee, st.floats(0.0, 0.15), tax_rate, years)
def test_tax_deferral_never_hurts_with_positive_returns(v0, g, er, dist, t, n):
    # With positive net returns, deferring all gains to liquidation (ETF)
    # leaves at least as much after tax as paying tax on annual
    # distributions (mutual fund). The two match when nothing is
    # distributed or the tax rate is zero.
    if g <= er:
        g = er + 0.01
    res = TE.deferred_vs_annual_tax(v0, g, er, dist, t, n)
    assert res["tax_advantage"] >= -1e-9 * v0
    assert res["mf_aftertax_terminal"] <= res["mf_pretax_terminal"] + 1e-9
    if dist == 0 or t == 0:
        assert close(res["etf_aftertax_terminal"], res["mf_aftertax_terminal"],
                     rel=1e-9)
