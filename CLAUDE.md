# Finance Skills — Project Instructions

## What This Is

A mono-repo of Claude Code skill plugins for financial services. Skills teach Claude
domain knowledge so it can assist with finance questions, build financial tools, and
flag compliance concerns. The plugin catalog lives in `marketplace.json`.

## Current State

91 skills across 7 plugin domains, organized under `plugins/`:
- **core** (3 skills) — math foundations (returns, TVM, statistics)
- **wealth-management** (38 skills) — investment knowledge, asset classes, portfolio construction, personal finance
- **compliance** (17 skills) — US securities regulatory guidance (FINRA, SEC, ERISA, FinCEN, CFA Institute GIPS)
- **advisory-practice** (12 skills) — advisor-facing systems, onboarding, CRM, portfolio management, proposals, billing
- **trading-operations** (9 skills) — order lifecycle, execution, settlement, margin, exchange connectivity, operational risk
- **client-operations** (8 skills) — account opening, maintenance, transfers, reconciliation, corporate actions, STP
- **data-integration** (4 skills) — reference data, market data, integration patterns, data quality

Skills are installed into a project's `.claude/skills/` via `install.sh`.

## Working With Skills

### Skill Structure
Each skill is a directory in `plugins/<plugin-name>/skills/` containing a `SKILL.md`
and optionally a `scripts/` subdirectory with Python reference implementations. The
SKILL.md teaches domain knowledge; scripts provide runnable computation.

### Template
All skills follow this template:
- **No Purpose, Layer, or Direction sections in the body.** Triggering is
  carried entirely by the frontmatter `description`; the body starts with
  domain content (Core Concepts).
- **Core Concepts** — the domain knowledge
- **Worked Examples** — concrete scenarios with analysis. When the body
  exceeds ~250 lines, move worked examples to `references/examples.md`
  inside the skill directory and link to them from the body.
- **Common Pitfalls** — mistakes to avoid
- **Cross-References** — links to related skills
- **Time anchoring:** any indexed threshold, rate, limit, or effective date
  carries an as-of anchor (e.g. "$X as of 2026", "effective March 2026").
  Never state an inflation-indexed number bare.
- **Script-bearing skills** include a `## Running the script` section with
  the exact invocation (arguments and expected output) and a `--verify` mode
  that self-checks the script's outputs against the SKILL.md examples.

### Creating New Skills
1. Choose the plugin (see the plugin list above and `marketplace.json`)
2. Create the skill directory under `plugins/<plugin-name>/skills/<skill-name>/`
3. Follow the SKILL.md template exactly
4. For quantitative skills: include Key Formulas and worked numerical examples
5. For compliance/operations skills: use scenario-based examples (Scenario / Compliance Issues / Analysis), cite specific rule numbers, omit Key Formulas and Reference Implementation sections
6. Add cross-references to related skills in both directions
7. Update the skill counts in `marketplace.json` and this file

### Python Scripts
Only quantitative skills (core, wealth-management) get Python scripts. Scripts should:
- Use Python 3.11+ with only numpy/scipy/pandas dependencies
- Be standalone (runnable without installation)
- Use class-based organization with static methods
- Include comprehensive docstrings and type hints
- Match the formulas documented in the corresponding SKILL.md

## Conventions

- Skill directories: `lowercase-hyphenated` (e.g., `fixed-income-sovereign`)
- Python files: `lowercase_underscore` (e.g., `fixed_income_sovereign.py`)
- No emojis in skill content
- Compliance skills cite specific rule numbers and act sections inline
- Cross-references include the plugin name and a brief description of the relationship
- Do not add features, tests, or tooling beyond what is explicitly requested

## Linear

- **Project**: Finance Skills (team: Joellewis)
- Reference issue IDs (e.g., JOE-42) in commit messages and PR titles
- Issues discovered during implementation go to Triage with `agent-drafted` label
