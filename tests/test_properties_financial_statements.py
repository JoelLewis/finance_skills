"""Property-based tests for the financial-statements skill script."""

import math

from hypothesis import assume, given
from hypothesis import strategies as st

from conftest import load_script

fs = load_script("financial-statements")

FCF = fs.FreeCashFlow
Prof = fs.Profitability
EQ = fs.EarningsQuality
TB = fs.TaxBasis

# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

money = st.floats(-1e9, 1e9, allow_nan=False)
pos_money = st.floats(1e3, 1e10, allow_nan=False)
small_money = st.floats(0.0, 1e9, allow_nan=False)
tax = st.floats(0.0, 0.5, allow_nan=False)
scale = st.floats(1e-3, 1e3, allow_nan=False)


def close(a: float, b: float, rel: float = 1e-9, abs_: float = 1e-9) -> bool:
    return math.isclose(a, b, rel_tol=rel, abs_tol=abs_)


# ---------------------------------------------------------------------------
# Free cash flow
# ---------------------------------------------------------------------------

@given(money, small_money, small_money, tax, money, small_money)
def test_fcff_from_cfo_matches_fcff_from_ebit(ebit, interest, da, t, d_nwc, capex):
    # Building net income from EBIT, then CFO by the indirect method, then
    # FCFF from CFO (adding back after-tax interest) must agree with FCFF
    # built directly from EBIT: both are EBIT(1-t) + D&A - dNWC - capex.
    ni = (ebit - interest) * (1 - t)
    cfo = FCF.cfo_indirect(ni, da, d_nwc)
    via_cfo = FCF.fcff_from_cfo(cfo, interest, t, capex)
    via_ebit = FCF.fcff_from_ebit(ebit, t, da, d_nwc, capex)
    assert close(via_cfo, via_ebit, rel=1e-9, abs_=1e-3)


@given(money, small_money, tax, small_money, money)
def test_fcfe_from_fcff_matches_fcfe_from_cfo(cfo, interest, t, capex, borrow):
    # FCFE = FCFF - after-tax interest + net borrowing reduces to
    # CFO - capex + net borrowing.
    fcff = FCF.fcff_from_cfo(cfo, interest, t, capex)
    assert close(FCF.fcfe_from_fcff(fcff, interest, t, borrow),
                 FCF.fcfe_from_cfo(cfo, capex, borrow), rel=1e-9, abs_=1e-3)


@given(money, small_money, tax)
def test_ebitda_and_nopat_bounds(ebit, da, t):
    # EBITDA is at least EBIT (D&A is non-negative); NOPAT keeps EBIT's sign
    # and is no larger in magnitude.
    assert FCF.ebitda(ebit, da) >= ebit
    n = FCF.nopat(ebit, t)
    assert abs(n) <= abs(ebit)
    assert n * ebit >= 0


# ---------------------------------------------------------------------------
# Profitability
# ---------------------------------------------------------------------------

@given(st.floats(-1e8, 1e8), pos_money, pos_money, pos_money)
def test_dupont_product_equals_roe(ni, rev, assets, equity):
    # Net margin * asset turnover * equity multiplier telescopes to NI / equity.
    margin, turnover, lev, roe = Prof.dupont(ni, rev, assets, equity)
    assert close(margin, Prof.net_margin(ni, rev))
    assert close(roe, ni / equity, rel=1e-9, abs_=1e-15)
    assert close(margin * turnover * lev, roe, rel=1e-12, abs_=1e-15)


@given(st.floats(-1e8, 1e8), pos_money, pos_money, pos_money, scale)
def test_ratios_are_scale_invariant(ni, rev, assets, equity, k):
    # Restating every statement item in different units (multiplying all
    # by k) leaves DuPont factors, margins, ROIC and day counts unchanged.
    base = Prof.dupont(ni, rev, assets, equity)
    scaled = Prof.dupont(k * ni, k * rev, k * assets, k * equity)
    for a, b in zip(base, scaled):
        assert close(a, b, rel=1e-9, abs_=1e-15)
    assert close(Prof.operating_margin(0.3 * ni, rev),
                 Prof.operating_margin(k * 0.3 * ni, k * rev), rel=1e-9, abs_=1e-15)
    assert close(Prof.roic(ni, assets), Prof.roic(k * ni, k * assets),
                 rel=1e-9, abs_=1e-15)
    assert close(EQ.days_sales_outstanding(0.1 * rev, rev),
                 EQ.days_sales_outstanding(k * 0.1 * rev, k * rev), rel=1e-9)


@given(pos_money, st.floats(0.0, 1.0), st.floats(0.0, 1.0), st.floats(0.0, 1.0))
def test_margin_ordering(rev, gm, om_frac, nm_frac):
    # With non-negative costs below each line, gross >= operating >= net
    # margin and all are at most 1.
    gp = rev * gm
    ebit = gp * om_frac
    ni = ebit * nm_frac
    g, o, n = (Prof.gross_margin(gp, rev), Prof.operating_margin(ebit, rev),
               Prof.net_margin(ni, rev))
    assert 1 + 1e-12 >= g >= o >= n >= 0


@given(small_money, pos_money, st.floats(0.0, 1.0), money, st.floats(0.0, 0.3))
def test_roic_spread_and_invested_capital(debt, equity, cash_frac, nopat, wacc):
    # Invested capital = debt + equity - excess cash; the value spread is
    # positive exactly when ROIC exceeds WACC.
    cash = cash_frac * equity * 0.5
    ic = Prof.invested_capital(debt, equity, cash)
    assert close(ic, debt + equity - cash, abs_=1e-3)
    r = Prof.roic(nopat, ic)
    spread = Prof.roic_spread(r, wacc)
    assert (spread > 0) == (r > wacc)


# ---------------------------------------------------------------------------
# Earnings quality
# ---------------------------------------------------------------------------

@given(pos_money, pos_money, st.floats(0, 1), st.floats(0, 1), st.floats(0, 1))
def test_cash_conversion_cycle_identity(rev, cogs, ar_f, inv_f, ap_f):
    # CCC = DSO + DIO - DPO; with payables equal to inventory the cycle
    # collapses to DSO.
    ar, inv, ap = ar_f * rev, inv_f * cogs, ap_f * cogs
    dso = EQ.days_sales_outstanding(ar, rev)
    dio = EQ.days_inventory_outstanding(inv, cogs)
    dpo = EQ.days_payables_outstanding(ap, cogs)
    assert close(EQ.cash_conversion_cycle(dso, dio, dpo), dso + dio - dpo, abs_=1e-9)
    dpo_eq = EQ.days_payables_outstanding(inv, cogs)
    assert close(EQ.cash_conversion_cycle(dso, dio, dpo_eq), dso, abs_=1e-9)


@given(money, money, pos_money)
def test_accruals_ratio_sign(ni, cfo, assets):
    # Accruals are positive exactly when earnings run ahead of cash. Gaps
    # below one cent are skipped: a subnormal gap divided by assets
    # underflows to zero.
    assume(abs(ni - cfo) >= 0.01)
    a = EQ.accruals_ratio(ni, cfo, assets)
    assert (a > 0) == (ni > cfo) and (a < 0) == (ni < cfo)


# ---------------------------------------------------------------------------
# Tax basis
# ---------------------------------------------------------------------------

@given(pos_money, pos_money, st.floats(0.0, 0.5))
def test_after_tax_liquidation_value_bounds(mv, basis, t):
    # Selling never yields more than market value, never pays tax on a loss,
    # and with a gain still leaves at least the cost basis (tax rate < 1).
    atv = TB.after_tax_liquidation_value(mv, basis, t)
    liab = TB.embedded_tax_liability(mv, basis, t)
    assert liab >= 0 and atv <= mv
    if mv <= basis:
        assert liab == 0 and atv == mv
    else:
        assert atv >= basis * (1 - 1e-12)
        assert close(liab, TB.unrealized_gain(mv, basis) * t, rel=1e-9, abs_=1e-6)
