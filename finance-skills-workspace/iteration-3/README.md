# Iteration 3 — Benchmark Scaffolds

Scaffolds for the next with-skill / without-skill benchmark run, covering the seven
skills added in the 2026-07 review: financial-statements, equity-compensation,
retirement-decumulation, factor-investing, insurance-planning, estate-gifting, and
private-placements. Each `eval-<id>-<shortname>/` directory holds the
`eval_metadata.json` (prompt and assertions) for the matching domain-accuracy eval
(ids 31-37) in `evals/evals.json`. The `with_skill/` and `without_skill/` response
directories are produced by the runner; grading uses `../grade_responses.py`.
