"""Property-based tests for the tax-efficiency script.

Each test states a rule of after-tax investing from the tax-efficiency
SKILL.md (after-tax returns, deferral, tax drag, loss harvesting, asset
location, breakevens) that must hold for every valid input.
"""

import math

import numpy as np
import pytest
from hypothesis import given
from hypothesis import strategies as st

from conftest import load_script

te = load_script("tax-efficiency")

ATR = te.AfterTaxReturn
Drag = te.TaxDrag
TLH = te.TaxLossHarvesting
Loc = te.AssetLocation
BE = te.BreakevenAnalysis

# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

ret = st.floats(0.0, 0.25)            # annual pre-tax return
tax = st.floats(0.0, 0.6)             # any marginal rate incl. state taxes
years = st.integers(1, 50)
amount = st.floats(1.0, 1e8)


def close(a: float, b: float, rel: float = 1e-9, abs_: float = 1e-9) -> bool:
    return math.isclose(a, b, rel_tol=rel, abs_tol=abs_)


@st.composite
def assets_and_capacity(draw):
    n = draw(st.integers(1, 8))
    assets = [
        {
            "name": f"a{i}",
            # Whole-dollar scale: the overflow check uses a $1e-9 absolute
            # tolerance, so sub-cent portfolios are out of scope.
            "amount": draw(st.one_of(st.just(0.0), st.floats(1.0, 1e6))),
            "tax_inefficiency": draw(st.floats(0.0, 1.0)),
            "expected_growth": draw(st.floats(0.0, 0.12)),
        }
        for i in range(n)
    ]
    total = sum(a["amount"] for a in assets)
    # Split the total (plus optional slack) across the three account types.
    shares = np.array(draw(st.lists(st.floats(0.0, 1.0), min_size=3, max_size=3))) + 1e-9
    shares = shares / shares.sum()
    slack = draw(st.floats(1.0, 1.5))
    taxable, deferred, exempt = (shares * total * slack).tolist()
    return assets, taxable, deferred, exempt


# ---------------------------------------------------------------------------
# After-tax returns
# ---------------------------------------------------------------------------


@given(ret, tax, tax)
def test_income_return_below_pretax_and_falls_with_rate(r, t1, t2):
    # R_at = R(1 - t): never above R, equal at t = 0, lower for higher t.
    lo, hi = sorted((t1, t2))
    assert ATR.income_return(r, 0.0) == r
    assert ATR.income_return(r, lo) <= r
    assert ATR.income_return(r, hi) <= ATR.income_return(r, lo)


@given(ret, years, tax)
def test_deferred_gain_return_between_annual_taxation_and_pretax(r, n, t):
    # Deferring the gain to realization beats paying tax every year at the
    # same rate (equal when n = 1), and cannot beat the untaxed return.
    deferred = ATR.deferred_gain_return(r, n, t)
    assert deferred <= r + 1e-12
    assert deferred >= ATR.income_return(r, t) - 1e-12
    assert close(ATR.deferred_gain_return(r, n, 0.0), r, abs_=1e-12)
    assert close(ATR.deferred_gain_return(r, 1, t), ATR.income_return(r, t), abs_=1e-12)


@given(ret, st.integers(1, 49), tax)
def test_deferral_benefit_grows_with_holding_period(r, n, t):
    # A longer deferral period leaves more tax-free compounding, so the
    # annualized after-tax return rises (weakly) with n.
    assert ATR.deferred_gain_return(r, n + 1, t) >= ATR.deferred_gain_return(r, n, t) - 1e-12


@given(ret, years, tax)
def test_deferred_gain_return_reproduces_after_tax_terminal_wealth(r, n, t):
    # Compounding the annualized rate for n years gives the terminal value
    # after paying t on the gain: (1+R)^n - t[(1+R)^n - 1].
    at = ATR.deferred_gain_return(r, n, t)
    fv = (1 + r) ** n
    assert close((1 + at) ** n, fv - t * (fv - 1), rel=1e-9)


@given(ret, st.floats(0, 1), st.floats(0, 1), tax, tax)
def test_blended_return_bounds(r, f_inc, f_cg_raw, t_inc, t_cg):
    # The blended after-tax return is at most the pre-tax return, at least the
    # return taxed entirely at the higher rate, and equals it at zero rates.
    f_cg = f_cg_raw * (1 - f_inc)
    b = ATR.blended_return(r, f_inc, t_inc, f_cg, t_cg)
    assert b <= r + 1e-12
    assert b >= r * (1 - max(t_inc, t_cg)) - 1e-12
    assert close(ATR.blended_return(r, f_inc, 0.0, f_cg, 0.0), r, abs_=1e-12)
    assert close(ATR.blended_return(r, 1.0, t_inc, 0.0, t_cg), ATR.income_return(r, t_inc),
                 abs_=1e-12)


# ---------------------------------------------------------------------------
# Tax drag
# ---------------------------------------------------------------------------


@given(st.floats(0.001, 0.25), tax, years, amount)
def test_tax_drag_identities(r, t, n, a):
    # Drag = pre - after; the tax cost ratio of a fully taxed income return is
    # the tax rate; cumulative drag is non-negative and zero with no tax.
    after = ATR.income_return(r, t)
    assert close(Drag.annual_drag(r, after) + after, r, abs_=1e-15)
    assert close(Drag.tax_cost_ratio(r, after), t, abs_=1e-12)
    assert Drag.cumulative_drag(r, after, n, a) >= 0
    assert Drag.cumulative_drag(r, r, n, a) == 0


# ---------------------------------------------------------------------------
# Tax-loss harvesting
# ---------------------------------------------------------------------------


@given(amount, amount, tax, tax)
def test_immediate_benefit_grows_with_loss_and_rate(l1, l2, t1, t2):
    # TLH value = loss x rate: monotone in both, and the sign of the loss
    # input does not matter.
    (lo_l, hi_l), (lo_t, hi_t) = sorted((l1, l2)), sorted((t1, t2))
    b = TLH.immediate_benefit
    assert b(hi_l, lo_t) >= b(lo_l, lo_t)
    assert b(lo_l, hi_t) >= b(lo_l, lo_t)
    assert b(-lo_l, lo_t) == b(lo_l, lo_t)
    assert close(b(lo_l, lo_t), lo_l * lo_t, rel=1e-12)


@given(amount, tax, st.integers(0, 40), st.integers(0, 40), st.floats(0.0, 0.15))
def test_net_benefit_at_equal_rates_is_time_value_of_deferral(loss, t, n1, n2, d):
    # With equal current and future rates, harvesting only defers tax: the NPV
    # is zero with no deferral or no discounting, never negative, never above
    # the immediate benefit, and grows with the deferral period.
    lo, hi = sorted((n1, n2))
    nb = TLH.net_benefit
    assert close(nb(loss, t, t, 0, d), 0.0, abs_=1e-9 * loss)
    assert close(nb(loss, t, t, lo, 0.0), 0.0, abs_=1e-9 * loss)
    assert -1e-9 * loss <= nb(loss, t, t, lo, d) <= TLH.immediate_benefit(loss, t) + 1e-9
    assert nb(loss, t, t, hi, d) >= nb(loss, t, t, lo, d) - 1e-9 * loss


@given(st.lists(st.tuples(st.floats(0.0, 1e6), st.floats(1.0, 1e6)), min_size=1, max_size=20),
       st.floats(0.0, 0.5), st.floats(0.0, 0.5))
def test_harvest_scan_totals_losses_and_threshold_narrows(pairs, th1, th2):
    # The scan finds exactly the positions below cost, totals their losses,
    # and a higher loss threshold only removes candidates.
    mv = np.array([p[0] for p in pairs])
    cb = np.array([p[1] for p in pairs])
    res = TLH.annual_harvesting_opportunities(mv, cb)
    assert set(res["eligible_indices"].tolist()) == set(np.where(mv < cb)[0].tolist())
    assert close(res["total_harvestable"], float(np.maximum(cb - mv, 0).sum()), rel=1e-12)
    lo, hi = sorted((th1, th2))
    lo_set = set(TLH.annual_harvesting_opportunities(mv, cb, lo)["eligible_indices"].tolist())
    hi_set = set(TLH.annual_harvesting_opportunities(mv, cb, hi)["eligible_indices"].tolist())
    assert hi_set <= lo_set


# ---------------------------------------------------------------------------
# Asset location
# ---------------------------------------------------------------------------


@given(amount, st.floats(0.0, 0.15), st.floats(0.0, 1.0), tax, tax, st.floats(0, 1))
def test_taxable_drag_non_negative_linear_and_zero_without_tax(a, r, y_frac, t_inc, t_cg, turn):
    # Annual taxable drag is non-negative, scales linearly with the dollars
    # held, and vanishes when both tax rates are zero.
    y = y_frac * r
    d = Loc.tax_drag_by_account(a, r, y, t_inc, t_cg, turn)
    assert d >= 0
    assert close(Loc.tax_drag_by_account(2 * a, r, y, t_inc, t_cg, turn), 2 * d, rel=1e-12)
    assert Loc.tax_drag_by_account(a, r, y, 0.0, 0.0, turn) == 0


# Income yield is restricted to at most the total return (non-negative price
# return); compare_locations credits negative price returns at the capital
# gains rate, which is outside the scope of these properties.
@given(amount, st.floats(0.0, 0.15), st.floats(0.0, 1.0), tax, tax, st.floats(0, 1), years)
def test_roth_dominates_and_zero_tax_equalizes_accounts(a, r, y_frac, t_inc, t_cg, turn, n):
    # Tax-exempt (Roth) wealth is at least taxable and tax-deferred wealth;
    # with zero tax rates all three account types end at A(1+R)^n.
    y = y_frac * r
    w = Loc.compare_locations(a, r, y, t_inc, t_cg, turn, n)
    assert w["tax_exempt"] >= w["taxable"] * (1 - 1e-12)
    assert w["tax_exempt"] >= w["tax_deferred"] * (1 - 1e-12)
    z = Loc.compare_locations(a, r, y, 0.0, 0.0, turn, n)
    gross = a * (1 + r) ** n
    assert all(close(v, gross, rel=1e-12) for v in z.values())


@given(amount, ret, tax, years)
def test_taxable_buy_and_hold_matches_deferred_gain_return(a, r, t, n):
    # A non-dividend asset with zero turnover in a taxable account is a pure
    # deferred gain: terminal wealth = A(1 + deferred_gain_return)^n.
    w = Loc.compare_locations(a, r, 0.0, 0.3, t, 0.0, n)["taxable"]
    assert close(w, a * (1 + ATR.deferred_gain_return(r, n, t)) ** n, rel=1e-9)


@given(assets_and_capacity())
def test_placement_allocates_everything_within_capacity(args):
    # Every dollar of every asset is placed, no account receives more than its
    # capacity, and no placement is negative.
    assets, taxable, deferred, exempt = args
    placements = Loc.optimal_placement(assets, taxable, deferred, exempt)
    cap = {"taxable": taxable, "tax_deferred": deferred, "tax_exempt": exempt}
    used = dict.fromkeys(cap, 0.0)
    for a in assets:
        locs = placements[a["name"]]
        assert all(p["amount"] > 0 for p in locs)
        assert close(sum(p["amount"] for p in locs), a["amount"], rel=1e-9, abs_=1e-6)
        for p in locs:
            used[p["account"]] += p["amount"]
    for acct, c in cap.items():
        assert used[acct] <= c + 1e-6


@given(assets_and_capacity(), st.floats(1.01, 2.0))
def test_placement_rejects_portfolio_larger_than_capacity(args, k):
    # If the assets exceed total account capacity the placement is refused
    # rather than silently dropping the excess.
    assets, taxable, deferred, exempt = args
    total = sum(a["amount"] for a in assets)
    cap = taxable + deferred + exempt
    if total < 1.0:
        return
    scale = k * cap / total
    big = [{**a, "amount": a["amount"] * scale} for a in assets]
    with pytest.raises(ValueError):
        Loc.optimal_placement(big, taxable, deferred, exempt)


# ---------------------------------------------------------------------------
# Breakevens
# ---------------------------------------------------------------------------


@given(st.floats(0.0, 0.6), st.floats(-0.05, 0.15), years, amount)
def test_roth_breakeven_equalizes_traditional_and_roth_paths(t_now, r, n, a):
    # SKILL.md Example 2 (tax paid from outside funds): at the breakeven future
    # rate, Traditional after-tax wealth A(1+r)^n(1 - t*) equals the Roth value
    # net of the side fund's forgone growth, A(1+r)^n - A t_now (1+r)^n. The
    # from-IRA variant equalizes A(1+r)^n(1 - t*) with A(1 - t_now)(1+r)^n.
    g = (1 + r) ** n
    t_out = BE.roth_conversion_breakeven(t_now, r, n)
    t_ira = BE.roth_conversion_breakeven_from_ira(t_now, r, n)
    assert close(a * g * (1 - t_out), a * g - a * t_now * g, rel=1e-12, abs_=1e-9)
    assert close(a * g * (1 - t_ira), a * (1 - t_now) * g, rel=1e-12, abs_=1e-9)


@given(st.floats(0.0, 0.6), st.floats(0.0, 0.6), st.floats(-0.1, 0.25))
def test_ltcg_breakeven_holding_period(t_st, t_lt, r):
    # No breakeven exists (0) when the long-term rate offers no advantage or
    # the return is not positive. Otherwise, holding for the returned period
    # and paying the long-term rate at the end is at least as good as
    # realizing gains every year at the short-term rate.
    n = BE.capital_gains_holding_period(t_st, t_lt, r)
    if t_lt >= t_st or r <= 0:
        assert n == 0.0
    else:
        assert 1 <= n < math.inf
        k = int(n)
        assert ATR.deferred_gain_return(r, k, t_lt) >= ATR.income_return(r, t_st) - 1e-12
