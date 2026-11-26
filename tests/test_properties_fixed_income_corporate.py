"""Property-based tests for the fixed-income-corporate script."""

import math

import numpy as np
from hypothesis import assume, given
from hypothesis import strategies as st

from conftest import load_script

corporate = load_script("fixed-income-corporate")
CreditSpread = corporate.CreditSpread
CreditRisk = corporate.CreditRisk
MigrationMatrix = corporate.MigrationMatrix

# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

prob = st.floats(0.0, 1.0)
spread = st.floats(0.0, 0.15)
ead = st.floats(1.0, 1e9)


@st.composite
def bond_and_curve(draw):
    """Bullet bond cash flows with an upward- or downward-sloping spot curve."""
    c = draw(st.floats(0.0, 0.12))
    freq = draw(st.sampled_from([1, 2, 4]))
    n = draw(st.integers(1, 30 * freq))
    times = np.arange(1, n + 1) / freq
    cfs = np.full(n, 100.0 * c / freq)
    cfs[-1] += 100.0
    s0 = draw(st.floats(0.0, 0.10))
    slope = draw(st.floats(-0.002, 0.002))
    spots = np.clip(s0 + slope * times, 0.0, 0.15)
    return cfs, times, spots


def pv(cfs, times, spots, z):
    return float(np.sum(cfs / (1.0 + spots + z) ** times))


@st.composite
def migration_matrix(draw):
    """Row-stochastic rating matrix with an absorbing default state last."""
    k = draw(st.integers(2, 8))
    rows = []
    for _ in range(k - 1):
        raw = np.array(draw(st.lists(st.floats(0.0, 1.0), min_size=k, max_size=k)))
        assume(raw.sum() > 0.1)
        rows.append(raw / raw.sum())
    rows.append(np.eye(k)[-1])
    labels = [f"R{i}" for i in range(k - 1)] + ["D"]
    return MigrationMatrix(np.array(rows), labels)


def close(a: float, b: float, rel: float = 1e-9, abs_: float = 1e-9) -> bool:
    return math.isclose(a, b, rel_tol=rel, abs_tol=abs_)


# ---------------------------------------------------------------------------
# CreditSpread
# ---------------------------------------------------------------------------

@given(bond_and_curve(), spread)
def test_z_spread_round_trips(bc, z):
    # Pricing at spot + z and solving for the Z-spread recovers z.
    cfs, times, spots = bc
    cs = CreditSpread(cfs, times, pv(cfs, times, spots, z), spots)
    assert close(cs.z_spread(), z, abs_=1e-8)


@given(bond_and_curve())
def test_z_spread_is_zero_at_risk_free_price(bc):
    # A bond priced exactly off the risk-free curve has no spread.
    cfs, times, spots = bc
    rf = CreditSpread(cfs, times, 1.0, spots).risk_free_price()
    assert close(CreditSpread(cfs, times, rf, spots).z_spread(), 0.0, abs_=1e-8)


@given(bond_and_curve(), spread, spread)
def test_lower_price_means_wider_z_spread(bc, z1, z2):
    # Price and Z-spread move inversely: the cheaper bond has the wider spread,
    # and it trades below the risk-free price exactly when its spread is positive.
    assume(abs(z1 - z2) > 1e-5)
    cfs, times, spots = bc
    p1, p2 = pv(cfs, times, spots, z1), pv(cfs, times, spots, z2)
    s1 = CreditSpread(cfs, times, p1, spots)
    s2 = CreditSpread(cfs, times, p2, spots)
    assert (p1 < p2) == (s1.z_spread() > s2.z_spread())
    if z1 > 1e-6:
        assert p1 < s1.risk_free_price()


@given(bond_and_curve(), spread, st.floats(-0.02, 0.05), st.floats(0.0, 0.2),
       st.floats(0.0, 0.2))
def test_summary_spreads_are_consistent(bc, z, option_cost, ytm, tsy):
    # OAS + option cost = Z-spread; G-spread = bond YTM - Treasury YTM.
    cfs, times, spots = bc
    cs = CreditSpread(cfs, times, pv(cfs, times, spots, z), spots)
    out = cs.summary(ytm, tsy, option_cost)
    assert close(out["oas"] + option_cost, out["z_spread"], abs_=1e-12)
    assert close(out["g_spread"], ytm - tsy, abs_=1e-15)


# ---------------------------------------------------------------------------
# CreditRisk
# ---------------------------------------------------------------------------

@given(prob, prob, ead, st.floats(0.0, 1000.0))
def test_expected_loss_bounded_and_linear_in_exposure(pd_, lgd, e, k):
    # 0 <= EL <= EAD, EL scales with exposure, and LGD = 1 - recovery.
    el = CreditRisk.expected_loss(pd_, lgd, e)
    assert 0.0 <= el <= e
    assert close(CreditRisk.expected_loss(pd_, lgd, k * e), k * el, rel=1e-12)
    rr = CreditRisk.recovery_rate(lgd)
    assert 0.0 <= rr <= 1.0
    assert close(CreditRisk.expected_loss(pd_, 1.0 - rr, e), el, rel=1e-9, abs_=1e-6)


@given(spread, st.floats(0.05, 1.0))
def test_implied_pd_reproduces_spread(s, lgd):
    # The spread ~ PD x LGD approximation inverts exactly: the implied PD
    # times LGD gives back the spread (expected loss per unit exposure).
    pd_ = CreditRisk.implied_default_probability(s, lgd)
    assert close(CreditRisk.expected_loss(pd_, lgd, 1.0), s, abs_=1e-15)


@given(st.floats(0.0, 0.5), st.integers(0, 50), st.integers(0, 50))
def test_cumulative_pd_is_a_probability_and_compounds(p, n, m):
    # Cumulative PD lies in [0, 1], equals the annual PD at one year, never
    # falls with horizon, and survival multiplies across consecutive windows.
    cum = CreditRisk.cumulative_default_probability
    assert 0.0 <= cum(p, n) <= 1.0
    assert close(cum(p, 1), p, abs_=1e-15)
    assert cum(p, n + m) >= cum(p, n) - 1e-15
    assert close(1 - cum(p, n + m), (1 - cum(p, n)) * (1 - cum(p, m)), abs_=1e-12)


@given(st.floats(-0.05, 0.25), st.lists(st.floats(-0.05, 0.25), max_size=10))
def test_yield_to_worst_is_the_lowest_yield(ytm, ytcs):
    # YTW is no higher than YTM or any YTC, and is one of them.
    ytw = CreditRisk.yield_to_worst(ytm, ytcs)
    assert ytw <= ytm and all(ytw <= y for y in ytcs)
    assert ytw in [ytm] + ytcs


# ---------------------------------------------------------------------------
# MigrationMatrix
# ---------------------------------------------------------------------------

@given(migration_matrix())
def test_upgrade_stay_downgrade_partition_each_row(mm):
    # From any rating, upgrade + stay + downgrade covers every outcome.
    for r in mm.rating_labels:
        total = (mm.upgrade_probability(r) + mm.transition_probability(r, r)
                 + mm.downgrade_probability(r))
        assert close(total, 1.0, abs_=1e-12)
        if r != "D":  # default is one of the downgrade outcomes
            assert 0.0 <= mm.default_probability(r) <= mm.downgrade_probability(r) + 1e-15


@given(migration_matrix(), st.integers(0, 20), st.integers(0, 20))
def test_multi_period_matrix_is_stochastic_and_chains(mm, a, b):
    # M^(a+b) = M^a M^b (Chapman-Kolmogorov), rows stay probability vectors,
    # and cumulative default never falls with horizon (default is absorbing).
    ma, mb, mab = mm.multi_period_matrix(a), mm.multi_period_matrix(b), mm.multi_period_matrix(a + b)
    assert np.allclose(mab, ma @ mb, atol=1e-12)
    assert np.allclose(mab.sum(axis=1), 1.0, atol=1e-12)
    assert np.all(mab >= -1e-15) and np.all(mab <= 1 + 1e-12)
    assert np.all(mab[:, -1] >= ma[:, -1] - 1e-12)
