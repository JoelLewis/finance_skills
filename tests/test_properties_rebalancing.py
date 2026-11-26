"""Property-based tests for the rebalancing script.

Each test states a rebalancing rule from the rebalancing SKILL.md (drift,
trade sizing, cash-flow rebalancing, costs, tax lots, Leland bands, the
rebalancing premium) that must hold for every valid input.
"""

import math

import numpy as np
from hypothesis import given
from hypothesis import strategies as st

from conftest import load_script

rb = load_script("rebalancing")

# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

portfolio_value = st.floats(1_000.0, 1e8)


def close(a: float, b: float, rel: float = 1e-9, abs_: float = 1e-9) -> bool:
    return math.isclose(a, b, rel_tol=rel, abs_tol=abs_)


@st.composite
def weights(draw, n: int) -> np.ndarray:
    """Positive weights that sum to 1."""
    raw = np.array(draw(st.lists(st.floats(0.01, 1.0), min_size=n, max_size=n)))
    return raw / raw.sum()


@st.composite
def target_and_current(draw, min_n: int = 2, max_n: int = 10):
    n = draw(st.integers(min_n, max_n))
    return draw(weights(n)), draw(weights(n))


@st.composite
def tax_lots(draw, min_size: int = 1, max_size: int = 8) -> list[dict]:
    price = draw(st.floats(1.0, 1_000.0))
    return draw(st.lists(
        st.fixed_dictionaries({
            "shares": st.floats(1.0, 10_000.0),
            "cost_basis": st.floats(0.5, 2_000.0),
            "current_price": st.just(price),
            "holding_days": st.integers(1, 3_650),
        }),
        min_size=min_size, max_size=max_size,
    ))


def by_asset(trades: list[dict]) -> dict:
    return {t["asset"]: t for t in trades}


# ---------------------------------------------------------------------------
# Drift and threshold triggers
# ---------------------------------------------------------------------------


@given(target_and_current())
def test_drift_sums_to_zero(tc):
    # Weights on both sides sum to 1, so overweights and underweights
    # offset exactly: sum_i (w_actual_i - w_target_i) = 0.
    target, current = tc
    d = rb.DriftAnalyzer(target).compute_drift(current)
    assert close(d.sum(), 0.0, abs_=1e-12)


@given(target_and_current(), st.floats(0.0, 0.5))
def test_threshold_triggers_iff_max_drift_exceeds_band(tc, band):
    # Absolute band rule: rebalance exactly when some asset's |drift| exceeds
    # the band; inside the band no trade is triggered.
    target, current = tc
    analyzer = rb.DriftAnalyzer(target)
    result = analyzer.check_threshold(current, absolute_threshold=band)
    assert result["triggered"] == (analyzer.max_absolute_drift(current) > band)


@given(target_and_current(), st.floats(0.0, 2.0))
def test_relative_breach_iff_abs_drift_exceeds_band_times_target(tc, band):
    # Relative band: asset i breaches when |drift_i| / w_target_i > band.
    target, current = tc
    analyzer = rb.DriftAnalyzer(target)
    result = analyzer.check_threshold(current, relative_threshold=band)
    abs_d = analyzer.absolute_drift(current)
    expected = {str(i) for i in range(len(target)) if abs_d[i] / target[i] > band}
    assert set(result["relative_breaches"]) == expected


# ---------------------------------------------------------------------------
# Trade generation
# ---------------------------------------------------------------------------


@given(target_and_current(), portfolio_value)
def test_trades_restore_target_weights(tc, value):
    # Applying the generated trades to the current dollar holdings lands
    # every asset exactly on its target dollar amount.
    target, current = tc
    trades = by_asset(rb.TradeGenerator(target).compute_trades(current, value))
    holdings = current * value
    for i in range(len(target)):
        t = trades.get(str(i))
        if t is not None:
            sign = 1.0 if t["direction"] == "BUY" else -1.0
            holdings[i] += sign * t["dollar_amount"]
    # Trades below 1e-10 of weight are skipped, so allow that much slack.
    assert np.allclose(holdings, target * value, rtol=1e-9, atol=1e-9 * value)


@given(target_and_current(), portfolio_value)
def test_trades_are_cash_neutral_and_never_oversell(tc, value):
    # A full rebalance with no external cash flow: buys equal sells, and no
    # sale exceeds the dollar amount currently held in that asset.
    target, current = tc
    trades = rb.TradeGenerator(target).compute_trades(current, value)
    buys = sum(t["dollar_amount"] for t in trades if t["direction"] == "BUY")
    sells = sum(t["dollar_amount"] for t in trades if t["direction"] == "SELL")
    assert close(buys, sells, rel=1e-9, abs_=1e-9 * value)
    for t in trades:
        assert t["dollar_amount"] >= 0
        if t["direction"] == "SELL":
            assert t["dollar_amount"] <= current[int(t["asset"])] * value * (1 + 1e-12)


@given(st.integers(2, 10).flatmap(weights), portfolio_value)
def test_no_trades_when_on_target(target, value):
    # A portfolio already at its target weights needs no trades.
    assert rb.TradeGenerator(target).compute_trades(target.copy(), value) == []


@given(target_and_current(), portfolio_value, st.floats(0.0, 1.0))
def test_cash_flow_rebalance_invests_whole_deposit_without_selling(tc, value, frac):
    # Cash-flow rebalancing only buys (no sales) and invests the deposit:
    # purchases sum to the deposit, less any sub-cent amounts it skips.
    target, current = tc
    cash = frac * value
    purchases = rb.TradeGenerator(target).cash_flow_rebalance(current, value, cash)
    total = sum(p["dollar_amount"] for p in purchases)
    assert all(p["dollar_amount"] > 0 for p in purchases)
    assert total <= cash * (1 + 1e-12) + 1e-9
    assert total >= cash - 0.01 * len(target) - 1e-9 * value


@given(target_and_current(), portfolio_value, st.floats(0.001, 1.0))
def test_cash_flow_rebalance_never_increases_drift(tc, value, frac):
    # Directing new cash to underweight assets moves the portfolio toward
    # target: total absolute drift after the deposit is no larger than
    # before it.
    target, current = tc
    cash = frac * value
    purchases = rb.TradeGenerator(target).cash_flow_rebalance(current, value, cash)
    dollars = current * value
    for p in purchases:
        dollars[int(p["asset"])] += p["dollar_amount"]
    new_w = dollars / dollars.sum()
    before = np.abs(current - target).sum()
    after = np.abs(new_w - target).sum()
    # Purchases under $0.01 are skipped by design; allow that much drift.
    slack = 2 * 0.01 * len(target) / (value + cash)
    assert after <= before + slack + 1e-9


# ---------------------------------------------------------------------------
# Transaction costs
# ---------------------------------------------------------------------------


@given(
    # Trades are either zero or at least one cent (subnormal dollar amounts
    # lose all precision in the bps ratio).
    st.lists(st.one_of(st.just(0.0), st.floats(0.01, 1e7)), min_size=1, max_size=10),
    st.floats(0.0, 50.0),
    st.floats(0.0, 50.0),
    st.floats(0.0, 50.0),
)
def test_transaction_cost_components_add_up(trades, commission, spread, impact):
    # TC = commission + spread + impact; with zero commission the cost in bps
    # of traded value equals spread_bps + impact_bps.
    trades = np.array(trades)
    c = rb.TransactionCostEstimator.total_cost(trades, commission, spread, impact)
    assert close(c["total_cost"],
                 c["total_commission"] + c["total_spread_cost"] + c["total_impact_cost"],
                 rel=1e-12)
    assert c["total_commission"] == commission * int(np.sum(trades > 0))
    c0 = rb.TransactionCostEstimator.total_cost(trades, 0.0, spread, impact)
    if trades.sum() > 0:
        assert close(c0["cost_bps"], spread + impact, rel=1e-9, abs_=1e-9)


# ---------------------------------------------------------------------------
# Tax-aware lot selection
# ---------------------------------------------------------------------------


@given(tax_lots(), st.floats(0.0, 1.5))
def test_lot_selection_sells_exactly_what_is_needed_and_available(lots, frac):
    # Sales come from distinct lots, never exceed a lot's shares, and total
    # min(shares needed, shares held).
    held = sum(lot["shares"] for lot in lots)
    needed = frac * held
    sales = rb.TaxAwareLotSelector(lots).select_lots_min_tax(needed)
    idx = [s["lot_index"] for s in sales]
    assert len(idx) == len(set(idx))
    for s in sales:
        assert 0 < s["shares_to_sell"] <= lots[s["lot_index"]]["shares"]
    sold = sum(s["shares_to_sell"] for s in sales)
    assert close(sold, min(needed, held), rel=1e-9, abs_=1e-6)


@given(tax_lots(min_size=2), st.floats(0.0, 1.0), st.data())
def test_min_tax_selection_beats_any_other_ordering(lots, frac, data):
    # Selling in ascending tax-per-share order is optimal for a fixed share
    # count (a fractional-knapsack argument): any other lot ordering yields
    # at least as much tax.
    needed = frac * sum(lot["shares"] for lot in lots)
    selector = rb.TaxAwareLotSelector(lots)
    best = sum(s["tax_impact"] for s in selector.select_lots_min_tax(needed))
    order = data.draw(st.permutations(range(len(lots))))
    remaining, other = needed, 0.0
    for i in order:
        sell = min(remaining, lots[i]["shares"])
        if sell <= 0:
            break
        other += selector._lot_tax_impact(lots[i], sell)
        remaining -= sell
    assert best <= other + 1e-6 * max(1.0, abs(other))


@given(tax_lots(), st.floats(0.0, 0.5), st.floats(0.0, 0.5))
def test_harvest_candidates_are_losses_with_benefit_equal_loss_times_rate(lots, lt, extra):
    # TLH: exactly the lots with an unrealized loss are candidates, each
    # benefit = |loss| x applicable rate (long-term only if held > 365 days),
    # and candidates are ranked by benefit.
    st_rate = lt + extra
    selector = rb.TaxAwareLotSelector(lots, short_term_rate=st_rate, long_term_rate=lt)
    cands = selector.tax_loss_harvest_candidates()
    losers = {i for i, lot in enumerate(lots) if lot["current_price"] < lot["cost_basis"]}
    assert {c["lot_index"] for c in cands} == losers
    for c in cands:
        lot = lots[c["lot_index"]]
        rate = lt if lot["holding_days"] > 365 else st_rate
        assert c["unrealized_loss"] < 0
        assert close(c["tax_benefit"], -c["unrealized_loss"] * rate, rel=1e-12)
    benefits = [c["tax_benefit"] for c in cands]
    assert benefits == sorted(benefits, reverse=True)


# ---------------------------------------------------------------------------
# Leland band and rebalancing premium
# ---------------------------------------------------------------------------


@given(
    st.floats(1e-4, 0.02), st.floats(0.5, 10.0), st.floats(0.0004, 0.16),
    st.floats(1.01, 4.0),
)
def test_leland_band_comparative_statics(tc, lam, var, k):
    # band ~ (3 tc / (2 lambda sigma^2))^(1/3): wider with higher costs,
    # narrower with higher risk aversion or variance, and scaling tc by k
    # scales the band by k^(1/3).
    band = rb.leland_optimal_band(tc, lam, var)
    assert band > 0
    assert rb.leland_optimal_band(tc * k, lam, var) > band
    assert rb.leland_optimal_band(tc, lam * k, var) < band
    assert rb.leland_optimal_band(tc, lam, var * k) < band
    assert close(rb.leland_optimal_band(tc * k, lam, var), band * k ** (1 / 3), rel=1e-12)


@given(st.integers(1, 8).flatmap(lambda n: st.tuples(
    weights(n),
    st.lists(st.floats(0.03, 0.40), min_size=n, max_size=n),
    st.lists(st.floats(-1, 1), min_size=n * n, max_size=n * n),
)))
def test_rebalancing_premium_non_negative_and_zero_without_diversification(args):
    # RP ~ (1/2)(sum w_i sigma_i^2 - sigma_p^2) >= 0 because portfolio
    # variance never exceeds the weighted average variance (correlation <= 1);
    # it is zero when all assets are perfectly correlated with equal vols.
    w, vols, a = args
    n = len(w)
    vols = np.array(vols)
    a = np.array(a).reshape(n, n)
    g = a @ a.T + 1e-6 * np.eye(n)
    d = np.sqrt(np.diag(g))
    cov = np.outer(vols, vols) * (g / np.outer(d, d))
    rp = rb.rebalancing_premium_estimate(w, vols ** 2, float(w @ cov @ w))
    assert rp >= -1e-12
    s = float(vols[0])
    flat = np.full((n, n), s * s)
    assert close(rb.rebalancing_premium_estimate(w, np.full(n, s * s), float(w @ flat @ w)),
                 0.0, abs_=1e-12)
