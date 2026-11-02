# FinGrowth

Open-source Agent Skills for Consumer FinTech / Lending Growth.

**Growth is not just marketing; it is a system architecture problem.**

Risk-adjusted growth connects acquisition, onboarding, credit, servicing and unit economics. Built as an independent public framework; no employer systems, results or data are represented here.

## Run the synthetic demo

Python 3.10+; no external dependencies.

```sh
python3 scripts/analyze.py examples/lending/cohorts.json
python3 -m unittest discover -s tests -v
```

## Skills

- [fintech-growth-architect](skills/fintech-growth-architect/SKILL.md): map systems and decision ownership.
- [growth-metric-tree](skills/growth-metric-tree/SKILL.md): define risk-adjusted economics and denominators.
- [growth-funnel-diagnosis](skills/growth-funnel-diagnosis/SKILL.md): locate friction without claiming causation.
- [growth-experiment-design](skills/growth-experiment-design/SKILL.md): design controlled tests with delayed-risk gates.

Copy a selected folder under `skills/` into your agent's skill directory, or ask your agent to read its SKILL.md. Repository documents provide extended context; the skill entrypoints are standalone. Host compatibility is not certified.

## Architecture

Aggregate cohort JSON → strict validation → explainable metrics → diagnosis → human-reviewed experiment.

Agents advise; scripts calculate; humans own lending, risk and launch decisions. No production APIs or automated underwriting are included.

Read the [complete case](examples/lending/CASE.md), [metric contract](docs/METRICS.md), [guardrails](docs/GUARDRAILS.md), [skill specification](docs/SKILL-SPEC.md) and [roadmap](docs/ROADMAP.md).

v0.1 is a local reference implementation with synthetic data, not a production lending platform. MIT licensed.
