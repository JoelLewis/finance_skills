"""Property-based tests for the equities skill script."""

import math

import numpy as np
from hypothesis import assume, given
from hypothesis import strategies as st

from conftest import load_script

equities = load_script("equities")

EV = equities.EquityValuation
FactorAnalysis = equities.FactorAnalysis
SectorAllocation = equities.SectorAllocation

# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

price = st.floats(0.5, 5000.0, allow_nan=False)
eps = st.floats(0.01, 500.0, allow_nan=False)
rate = st.floats(0.0, 0.20, allow_nan=False)
beta = st.floats(-1.0, 3.0, allow_nan=False)
growth = st.floats(-0.05, 0.10, allow_nan=False)
dividend = st.floats(0.01, 50.0, allow_nan=False)


def close(a: float, b: float, rel: float = 1e-9, abs_: float = 1e-9) -> bool:
    return math.isclose(a, b, rel_tol=rel, abs_tol=abs_)


@st.composite
def weights(draw, n: int) -> np.ndarray:
    raw = np.array(draw(st.lists(st.floats(0.01, 1.0), min_size=n, max_size=n)))
    return raw / raw.sum()


# ---------------------------------------------------------------------------
# Valuation ratios
# ---------------------------------------------------------------------------

@given(price, eps)
def test_pe_and_earnings_yield_are_reciprocals(p, e):
    # Earnings yield is defined as the inverse of P/E.
    assert close(EV.pe_ratio(p, e) * EV.earnings_yield(e, p), 1.0)


@given(price, eps, st.floats(0.1, 50.0))
def test_peg_scales_pe_by_growth(p, e, g):
    # PEG = P/E / growth (growth in percent), so PEG * growth recovers P/E.
    pe = EV.pe_ratio(p, e)
    assert close(EV.peg_ratio(pe, g) * g, pe)


@given(st.floats(1e3, 1e12), st.floats(0, 1e11), st.floats(0, 1e11),
       st.floats(1e2, 1e11), st.floats(0, 1e11))
def test_ev_ebitda_rises_with_debt_and_falls_with_cash(mcap, debt, cash, ebitda, extra):
    # Enterprise value = market cap + debt - cash: more debt raises EV/EBITDA,
    # more cash lowers it, dollar for dollar per unit EBITDA.
    base = EV.ev_ebitda(mcap, debt, cash, ebitda)
    assert EV.ev_ebitda(mcap, debt + extra, cash, ebitda) >= base
    assert EV.ev_ebitda(mcap, debt, cash + extra, ebitda) <= base
    assert close(EV.ev_ebitda(mcap, debt + extra, cash + extra, ebitda), base,
                 rel=1e-9, abs_=1e-6)


@given(price, price, st.floats(0.0, 100.0))
def test_total_return_is_price_return_plus_dividend_yield(p0, p1, d):
    # Total return decomposes into price return plus dividend yield on P0.
    total = EV.total_return(p0, p1, d)
    assert close(total, (p1 - p0) / p0 + EV.dividend_yield(d, p0), abs_=1e-12)


# ---------------------------------------------------------------------------
# CAPM and Gordon growth
# ---------------------------------------------------------------------------

@given(rate, rate, beta)
def test_capm_endpoints_and_linearity(rf, rm, b):
    # beta 0 earns the risk-free rate, beta 1 the market, and the expected
    # return is linear in beta (security market line).
    assert close(EV.capm_expected_return(rf, 0.0, rm), rf)
    assert close(EV.capm_expected_return(rf, 1.0, rm), rm)
    mid = EV.capm_expected_return(rf, b, rm)
    assert close(mid, rf + b * (rm - rf), abs_=1e-12)


@given(dividend, growth, st.floats(0.02, 0.20), st.floats(0.001, 0.05))
def test_gordon_value_falls_as_required_return_rises(d1, g, r, bump):
    # A higher discount rate lowers the present value of the dividend stream.
    r = max(r, g + 0.005)
    v_low = EV.gordon_growth_model(d1, g, r)
    v_high = EV.gordon_growth_model(d1, g, r + bump)
    assert v_high < v_low


@given(dividend, growth, st.floats(0.02, 0.20))
def test_gordon_implied_return_is_dividend_yield_plus_growth(d1, g, r):
    # Rearranging P = D1/(r - g) gives r = D1/P + g.
    r = max(r, g + 0.005)
    p = EV.gordon_growth_model(d1, g, r)
    assert close(EV.dividend_yield(d1, p) + g, r, abs_=1e-12)


# ---------------------------------------------------------------------------
# Factor analysis
# ---------------------------------------------------------------------------

@given(st.data(), st.integers(12, 60), st.floats(-2.0, 2.0), st.floats(-0.01, 0.01))
def test_ols_recovers_exact_linear_factor_model(data, n, b, alpha):
    # Returns built exactly as alpha + beta * F (no noise) must be fit
    # perfectly: the regression recovers alpha and beta and R^2 = 1.
    f = np.array(data.draw(st.lists(st.floats(-0.1, 0.1), min_size=n, max_size=n)))
    assume(np.std(f) > 1e-3)  # a near-constant factor has no identifiable beta
    r = alpha + b * f
    fa = FactorAnalysis(r, f.reshape(-1, 1))
    res = fa.ols_regression()
    assert close(res["alpha"], alpha, abs_=1e-9)
    assert close(res["betas"]["F1"], b, rel=1e-7, abs_=1e-8)
    assert close(fa.beta()["F1"], b, rel=1e-7, abs_=1e-8)
    if np.std(r) > 1e-6:
        assert res["r_squared"] > 1 - 1e-9


# ---------------------------------------------------------------------------
# Sector allocation
# ---------------------------------------------------------------------------

@given(st.integers(1, 11).flatmap(lambda n: weights(n)))
def test_concentration_bounds(w):
    # For weights summing to 1, HHI lies in [1/n, 1] and the effective
    # number of sectors lies in [1, n].
    n = len(w)
    sa = SectorAllocation({f"S{i}": float(x) for i, x in enumerate(w)})
    c = sa.concentration()
    assert 1.0 / n - 1e-12 <= c["herfindahl"] <= 1.0 + 1e-12
    assert 1.0 - 1e-9 <= c["effective_sectors"] <= n + 1e-9
    assert c["top_weight"] == max(w)


@given(st.integers(1, 11).flatmap(lambda n: st.tuples(weights(n), weights(n))))
def test_active_weights_sum_to_zero(wb):
    # When both portfolio and benchmark are fully invested, overweights and
    # underweights net to zero.
    w_p, w_b = wb
    sa = SectorAllocation({f"S{i}": float(x) for i, x in enumerate(w_p)},
                          {f"S{i}": float(x) for i, x in enumerate(w_b)})
    assert abs(sum(sa.active_weights().values())) < 1e-12
