# Trigger Evals

Tests whether the right skill triggers (and the wrong ones stay quiet) for the
fifteen skill clusters with the highest description overlap:

1. `financial-planning-workflow` vs `financial-planning-integration`
2. `stp-automation` vs `workflow-automation` vs `account-opening-workflow`
3. `advertising-compliance` vs `gips-compliance`
4. `know-your-customer` vs `anti-money-laundering`
5. `tax-efficiency` vs `tax-loss-harvesting` vs `rebalancing`
6. `order-lifecycle` vs `exchange-connectivity` (FIX protocol)
7. `trade-execution` vs `post-trade-compliance` (best execution)
8. `margin-operations` vs `counterparty-risk`
9. `retirement-decumulation` vs `savings-goals` (plus `tax-efficiency` on RMD tax planning)
10. `estate-gifting` vs `tax-efficiency` (charitable/QCD/asset-location vs exemption/gifting/trusts)
11. `equity-compensation` vs `tax-efficiency` vs `tax-loss-harvesting` (wash sale on RSU vest)
12. `factor-investing` vs `performance-metrics` vs `statistics-fundamentals` (CAPM beta)
13. `financial-statements` vs `quantitative-valuation` vs `equities` (multiples by sector)
14. `private-placements` vs `alternatives` vs `investment-suitability`
15. `insurance-planning` vs `retirement-decumulation` vs `emergency-fund` (annuities, income floors)

## Files

- `queries.json` — 203 labeled queries (`{query, expected_skill, cluster}`).
  `expected_skill: null` marks a near-miss query that should NOT trigger any
  skill in its cluster (e.g. "Rebalance the load across our Kubernetes nodes").
- `run_trigger_evals.sh` — the harness. Runs each query through
  `claude -p "<query>" --output-format json`, detects Skill tool invocations,
  repeats 3 times per query, and writes `trigger_results.json`.

## Cost Warning

A full run is **203 queries x 3 runs = ~609 claude invocations**, each a
complete model call. Scope your runs:

```bash
# One cluster only (10-17 queries x 3 runs = ~30-50 invocations)
./run_trigger_evals.sh --cluster kyc-vs-aml

# Smoke test: first 5 queries, 1 run each
./run_trigger_evals.sh --limit 5 --runs 1
```

## How to Run

1. Install the skills under test into a scratch project:

   ```bash
   mkdir -p /tmp/trigger-test/.claude
   /path/to/finance_skills/install.sh --plugin all --target /tmp/trigger-test
   cd /tmp/trigger-test
   ```

2. Run the harness from that project directory (the `claude` CLI picks up
   `.claude/skills/` from the working directory):

   ```bash
   /path/to/finance_skills/evals/trigger/run_trigger_evals.sh --cluster order-lifecycle-vs-exchange-connectivity
   ```

3. Read `trigger_results.json`: per-query trigger rates plus a per-cluster
   pass summary.

## Pass Criteria

- **Should-trigger** (`expected_skill` set): the expected skill must be
  invoked in **more than 0.5** of runs (i.e. 2 of 3).
- **Should-not-trigger** (`expected_skill: null`): skills from that cluster
  must be invoked in **fewer than 0.5** of runs. Invoking an unrelated skill
  outside the cluster does not fail a null query.

A cluster is healthy when both directions pass: every skill wins its own
queries AND stays quiet on its siblings' queries and the near-misses.

## Train/Validation Split

Do not tune skill descriptions against all of these queries — that overfits
the description to the test. Recommended practice:

- Treat roughly **two-thirds of each cluster's queries as the training set**:
  iterate on frontmatter `description` wording until they pass.
- Hold out the remaining third (including at least one should-trigger per
  skill and one near-miss) as a **validation set**: run it only after
  description changes are final. If validation disagrees with training,
  the description is overfit — generalize the wording rather than adding
  more trigger phrases verbatim from the failures.
- When adding new queries, add them to the validation side first.

## Interpreting Failures

- **Expected skill never triggers**: the description lacks the vocabulary of
  the query. Add the missing *concepts* (not the literal query) to the
  description.
- **Sibling skill triggers instead**: the two descriptions overlap. Sharpen
  the contrast — state what each skill is NOT for (e.g. "settlement and
  lifecycle states, not FIX session mechanics").
- **Null queries trigger**: the description is too broad ("anything about
  margins"). Anchor it to the financial-operations context.
