"""Property-based tests for the fixed-income-municipal script."""

import math

import numpy as np
from hypothesis import given
from hypothesis import strategies as st

from conftest import load_script

municipal = load_script("fixed-income-municipal")
Tax = municipal.MunicipalBondTax
DeMinimis = municipal.DeMinimis
AMT = municipal.AMTAdjustment
MuniRatio = municipal.MuniRatio

# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

yield_ = st.floats(0.0, 0.15)
fed = st.floats(0.0, 0.50)
state = st.floats(0.0, 0.15)
par = st.floats(100.0, 1e7)
years = st.floats(0.0, 40.0)


def close(a: float, b: float, rel: float = 1e-9, abs_: float = 1e-12) -> bool:
    return math.isclose(a, b, rel_tol=rel, abs_tol=abs_)


# ---------------------------------------------------------------------------
# Tax-equivalent yield
# ---------------------------------------------------------------------------

@given(yield_, fed, state)
def test_tey_taxed_back_gives_muni_yield(m, f, s):
    # TEY is defined so that a taxable bond yielding TEY nets exactly the
    # muni yield after tax.
    tey = Tax.tax_equivalent_yield_full(m, f, s)
    assert close(Tax.after_tax_yield(tey, f, s), m)
    tey_f = Tax.tax_equivalent_yield_federal(m, f)
    assert close(Tax.after_tax_yield(tey_f, f), m)


@given(yield_, fed, state)
def test_state_exemption_adds_to_tey(m, f, s):
    # An in-state exemption never lowers TEY; with no state tax the full
    # formula reduces to the federal-only one; TEY is never below the muni yield.
    full = Tax.tax_equivalent_yield_full(m, f, s)
    fed_only = Tax.tax_equivalent_yield_federal(m, f)
    assert full >= fed_only - 1e-15
    assert fed_only >= m
    assert close(Tax.tax_equivalent_yield_full(m, f, 0.0), fed_only)


@given(st.floats(0.0001, 0.15), fed, fed, state)
def test_tey_rises_with_tax_bracket(m, f1, f2, s):
    # A higher bracket makes the exemption worth more.
    lo, hi = sorted((f1, f2))
    assert Tax.tax_equivalent_yield_federal(m, hi) >= Tax.tax_equivalent_yield_federal(m, lo)
    assert Tax.tax_equivalent_yield_full(m, hi, s) >= Tax.tax_equivalent_yield_full(m, lo, s)


@given(yield_, yield_, fed, state)
def test_muni_preference_agrees_with_tey_comparison(m, t, f, s):
    # Comparing after-tax yields and comparing TEY with the taxable yield
    # are the same decision.
    out = Tax.compare_muni_vs_taxable(m, t, f, s)
    assert close(out["muni_advantage"], m - out["after_tax_taxable_yield"])
    gap = out["tax_equivalent_yield"] - t
    if abs(gap) > 1e-12:
        assert out["prefer_muni"] == (gap > 0)


# ---------------------------------------------------------------------------
# De minimis
# ---------------------------------------------------------------------------

@given(par, years)
def test_de_minimis_threshold_is_quarter_point_per_year(p, n):
    # Threshold = par - 0.25% x years x par, and scales with par.
    th = DeMinimis.threshold_price(p, n)
    assert close(p - th, 0.0025 * n * p, rel=1e-9, abs_=1e-6)
    assert close(DeMinimis.threshold_price(2 * p, n), 2 * th, rel=1e-12)


@given(par, years, st.floats(0.5, 1.2))
def test_taxable_gain_is_all_or_nothing(p, n, frac):
    # Below the threshold the whole discount is ordinary income; at or above
    # it nothing is. The taxable amount never exceeds the discount.
    price = frac * p
    gain = DeMinimis.taxable_gain(price, p, n)
    if DeMinimis.is_de_minimis(price, p, n):
        assert price < DeMinimis.threshold_price(p, n)
        assert close(gain, p - price)
    else:
        assert gain == 0.0
    assert 0.0 <= gain <= max(p - price, 0.0) + 1e-9


@given(par, years, st.floats(0.5, 1.2), st.floats(0.5, 1.2))
def test_lower_price_cannot_escape_de_minimis(p, n, f1, f2):
    # If a price triggers ordinary-income treatment, any lower price does too.
    lo, hi = sorted((f1, f2))
    if DeMinimis.is_de_minimis(hi * p, p, n):
        assert DeMinimis.is_de_minimis(lo * p, p, n)


# ---------------------------------------------------------------------------
# AMT
# ---------------------------------------------------------------------------

@given(yield_, st.floats(0.0, 0.5), st.floats(0.0, 0.5), fed)
def test_amt_reduces_yield_and_zero_amt_is_plain_tey(m, a1, a2, f):
    # AMT never raises the effective yield, a higher AMT rate costs more, and
    # with a zero AMT rate the AMT TEY collapses to the ordinary federal TEY.
    lo, hi = sorted((a1, a2))
    assert AMT.amt_adjusted_yield(m, hi) <= AMT.amt_adjusted_yield(m, lo) <= m
    assert close(AMT.amt_tax_equivalent_yield(m, f, 0.0),
                 Tax.tax_equivalent_yield_federal(m, f))
    assert AMT.amt_tax_equivalent_yield(m, f, hi) <= Tax.tax_equivalent_yield_federal(m, f) + 1e-15


# ---------------------------------------------------------------------------
# Muni / Treasury ratio
# ---------------------------------------------------------------------------

@given(st.lists(st.tuples(yield_, st.floats(0.001, 0.15)), min_size=1, max_size=12))
def test_ratio_curve_matches_pointwise_ratio(pairs):
    # The curve is the pointwise ratio, and ratio x Treasury = muni yield.
    muni = np.array([m for m, _ in pairs])
    tsy = np.array([t for _, t in pairs])
    curve = MuniRatio.ratio_curve(muni, tsy, np.arange(1, len(pairs) + 1))
    for r, m, t in zip(curve, muni, tsy):
        assert close(r, MuniRatio.yield_ratio(m, t))
        assert close(r * t, m)


@given(yield_, st.floats(0.001, 0.15))
def test_relative_value_label_follows_ratio(m, t):
    # Above 85% is cheap, below 70% rich, otherwise fair; deviation is
    # measured from the historical average.
    out = MuniRatio.relative_value_assessment(m, t)
    r = out["ratio"]
    expected = "cheap" if r > 0.85 else "rich" if r < 0.70 else "fair"
    assert out["assessment"] == expected
    assert close(out["deviation"], r - out["historical_average"])
    assert close(out["ratio_pct"], 100 * r)
