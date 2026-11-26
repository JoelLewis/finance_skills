"""Property-based tests for historical-risk (wealth-management plugin)."""

import math

import numpy as np
from hypothesis import assume, given
from hypothesis import strategies as st

from conftest import load_script

hr = load_script("historical-risk")
HRA = hr.HistoricalRiskAnalyzer

# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

# Daily simple returns; losses stop short of -100% so the wealth path stays
# strictly positive.
daily_ret = st.floats(-0.5, 0.5, allow_nan=False)
rets = st.lists(daily_ret, min_size=2, max_size=120).map(np.array)
confidence = st.floats(0.5, 0.995)
ppy = st.sampled_from([12, 52, 252])


def close(a: float, b: float, rel: float = 1e-9, abs_: float = 1e-9) -> bool:
    return math.isclose(a, b, rel_tol=rel, abs_tol=abs_)


# ---------------------------------------------------------------------------
# Volatility
# ---------------------------------------------------------------------------

# Volatility ignores a constant shift and scales by |k|.
@given(rets, st.floats(-0.01, 0.01), st.floats(0.1, 10.0), st.booleans(), ppy)
def test_annualized_volatility_shift_and_scale(r, c, k, flip, p):
    kk = -k if flip else k
    base = HRA(r, p).annualized_volatility()
    assert base >= 0
    assert close(HRA(r + c, p).annualized_volatility(), base, rel=1e-6, abs_=1e-9)
    assert close(HRA(kk * r, p).annualized_volatility(), abs(kk) * base, rel=1e-9, abs_=1e-12)
    assert close(base, np.std(r, ddof=1) * math.sqrt(p), rel=1e-12)


# Rolling vol: NaN warm-up, then each value is the vol of its window; a full
# window reproduces the whole-sample annualised vol.
@given(rets, st.data())
def test_rolling_volatility_windows(r, data):
    w = data.draw(st.integers(2, len(r)))
    model = HRA(r)
    roll = model.rolling_volatility(window=w)
    assert np.all(np.isnan(roll[: w - 1]))
    assert close(roll[-1], HRA(r[-w:]).annualized_volatility(), rel=1e-12, abs_=1e-15)
    assert close(model.rolling_volatility(window=len(r))[-1],
                 model.annualized_volatility(), rel=1e-12, abs_=1e-15)


# Parkinson vol depends only on H/L: rescaling prices leaves it unchanged and
# a zero range gives zero.
@given(st.lists(st.tuples(st.floats(10, 500), st.floats(0.0, 0.1)), min_size=1, max_size=60),
       st.floats(0.01, 100.0))
def test_parkinson_volatility_price_scale_invariant(bars, c):
    lows = np.array([b[0] for b in bars])
    highs = lows * (1 + np.array([b[1] for b in bars]))
    model = HRA(np.array([0.0, 0.01]))
    base = model.parkinson_volatility(highs, lows)
    assert base >= 0
    assert close(model.parkinson_volatility(c * highs, c * lows), base, rel=1e-9, abs_=1e-12)
    assert model.parkinson_volatility(lows, lows) == 0.0


# ---------------------------------------------------------------------------
# Drawdowns
# ---------------------------------------------------------------------------

# Drawdowns lie in (-1, 0]; the series starts at 0 and is identically zero
# for a path that never falls.
@given(rets)
def test_drawdown_series_bounds(r):
    dd = HRA(r).drawdown_series()
    assert len(dd) == len(r)
    assert np.all(dd <= 0) and np.all(dd > -1)
    if r[0] >= 0:
        assert dd[0] == 0
    assert np.all(HRA(np.abs(r)).drawdown_series() == 0)


# Max drawdown is the minimum of the drawdown series and equals the loss
# from the identified peak to the identified trough; peak precedes trough,
# and recovery (if any) is the first later point back at the peak.
@given(rets)
def test_max_drawdown_consistent_with_path(r):
    model = HRA(r)
    mdd = model.max_drawdown()
    dd = model.drawdown_series()
    wealth = np.cumprod(1 + r)
    assert -1 < mdd["depth"] <= 0
    assert close(mdd["depth"], dd.min(), abs_=1e-15)
    s, t, rec = mdd["start_idx"], mdd["trough_idx"], mdd["recovery_idx"]
    assert 0 <= s <= t < len(r)
    assert close(mdd["depth"], wealth[t] / wealth[s] - 1, abs_=1e-12)
    if rec is None:
        assert np.all(wealth[t + 1:] < wealth[s])
    else:
        assert rec > t and wealth[rec] >= wealth[s]
        assert np.all(wealth[t + 1:rec] < wealth[s])


# ---------------------------------------------------------------------------
# VaR and downside measures
# ---------------------------------------------------------------------------

# Historical VaR rises with confidence and lies within the observed range.
@given(rets, confidence, confidence)
def test_historical_var_monotone_and_bounded(r, c1, c2):
    model = HRA(r)
    lo, hi = sorted((c1, c2))
    assert model.historical_var(lo) <= model.historical_var(hi) + 1e-15
    assert -r.max() - 1e-15 <= model.historical_var(hi) <= -r.min() + 1e-15


# Downside deviation is non-negative, zero when no return falls below the
# threshold, non-decreasing in the threshold, and never above the RMS
# deviation from the threshold.
@given(rets, st.floats(-0.05, 0.05), st.floats(-0.05, 0.05), ppy)
def test_downside_deviation_monotone_in_threshold(r, t1, t2, p):
    model = HRA(r, p)
    lo, hi = sorted((t1, t2))
    d_lo, d_hi = model.downside_deviation(lo), model.downside_deviation(hi)
    assert 0 <= d_lo <= d_hi + 1e-15
    assert d_hi <= math.sqrt(np.mean((r - hi) ** 2) * p) * (1 + 1e-12)
    assert model.downside_deviation(float(r.min())) == 0.0


# Semi-variance (below-mean squared deviations) is non-negative and at most
# the population variance; for a series symmetric about its mean it is
# exactly half.
@given(rets)
def test_semi_variance_bounds_and_symmetry(r):
    sv = HRA(r).semi_variance()
    assert 0 <= sv <= np.var(r) * (1 + 1e-12) + 1e-18
    sym = np.concatenate([r, -r])
    assert close(HRA(sym).semi_variance(), np.var(sym) / 2, rel=1e-9, abs_=1e-15)


# Tracking error is zero against itself, symmetric between portfolio and
# benchmark, and equals the portfolio's own vol against a constant benchmark.
@given(st.integers(2, 80).flatmap(lambda n: st.tuples(
    st.lists(daily_ret, min_size=n, max_size=n),
    st.lists(daily_ret, min_size=n, max_size=n),
)), st.floats(-0.01, 0.01))
def test_tracking_error_properties(pb, c):
    p, b = np.array(pb[0]), np.array(pb[1])
    mp, mb = HRA(p), HRA(b)
    assert mp.tracking_error(p) == 0.0
    assert close(mp.tracking_error(b), mb.tracking_error(p), rel=1e-12, abs_=1e-15)
    assert close(mp.tracking_error(np.full(len(p), c)), mp.annualized_volatility(),
                 rel=1e-6, abs_=1e-9)
