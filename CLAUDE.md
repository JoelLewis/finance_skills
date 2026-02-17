# Finance Skills — Project Instructions

## What This Is

A mono-repo of Claude Code skill plugins for financial services. Skills teach Claude
domain knowledge so it can assist with finance questions, build financial tools, and
flag compliance concerns. See `PLAN.md` for the full architecture and roadmap.

## Current State

81 skills across 7 plugin domains, organized under `plugins/`:
- **core** (3 skills) — math foundations (returns, TVM, statistics)
- **wealth-management** (31 skills) — investment knowledge, asset classes, portfolio construction, personal finance
- **compliance** (16 skills) — US securities regulatory guidance (FINRA, SEC, ERISA, FinCEN, CFA Institute GIPS)
- **advisory-practice** (10 skills) — advisor-facing systems, onboarding, CRM, portfolio management, proposals, billing
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
All skills follow the template documented in `PLAN.md`. Key sections:
- **Purpose** — what the skill enables
- **When to Use** — trigger phrases and situations
- **Core Concepts** — the domain knowledge
- **Worked Examples** — concrete scenarios with analysis
- **Common Pitfalls** — mistakes to avoid
- **Cross-References** — links to related skills

### Creating New Skills
1. Check `PLAN.md` for the planned skill list and plugin assignment
2. Create the skill directory under `plugins/<plugin-name>/skills/<skill-name>/`
3. Follow the SKILL.md template exactly
3. For quantitative skills: include Key Formulas and worked numerical examples
4. For compliance/operations skills: use scenario-based examples (Scenario / Compliance Issues / Analysis), cite specific rule numbers, omit Key Formulas and Reference Implementation sections
5. Add cross-references to related skills in both directions
6. Update `PLAN.md` implementation status when complete

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
- Cross-references include the layer/plugin and a brief description of the relationship
- Do not add features, tests, or tooling beyond what is explicitly requested
