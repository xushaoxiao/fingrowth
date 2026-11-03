# FinGrowth

Open-source Agent Skills for Consumer FinTech / Lending Growth.

**Growth is not just marketing; it is a system architecture problem.**

Connect acquisition, onboarding, credit quality, servicing and economics. Built as an independent public framework; no employer systems, results or data are represented here.

## Try the synthetic case

Python 3.10+; no external dependencies or credentials.

```sh
git clone https://github.com/xushaoxiao/fingrowth.git
cd fingrowth
python3 scripts/analyze.py examples/lending/cohorts.json --format markdown
python3 -m unittest discover -s tests -v
```

The case shows why cheaper acquisition need not create more value:

| Synthetic cohort | First-funded people | Funded CAC (USD) | Mature contribution (USD) |
| --- | ---: | ---: | ---: |
| Baseline | 1,400 | 10.00 | 4,000 |
| Cheap channel | 1,400 | 7.14 | −1,000 |

The report includes step denominators, investigation candidates by count and conversion, evidence gaps and maturity limits. The default command without `--format markdown` still outputs JSON. [Read the generated report](examples/lending/REPORT.md) or follow [the end-to-end walkthrough](docs/QUICKSTART.md).

## Use the four Skills

| Skill | Use it for | Deliverable |
| --- | --- | --- |
| [fintech-growth-architect](skills/fintech-growth-architect/SKILL.md) | Design the system and delivery plan | System/event ownership map and phased backlog |
| [growth-metric-tree](skills/growth-metric-tree/SKILL.md) | Define risk-adjusted growth | Reconciled metric tree and dictionary |
| [growth-funnel-diagnosis](skills/growth-funnel-diagnosis/SKILL.md) | Investigate conversion and channel quality | Calculation report, hypotheses and evidence checks |
| [growth-experiment-design](skills/growth-experiment-design/SKILL.md) | Prepare a controlled test | Experiment card with power and delayed-risk gates |

Ask an agent to read the selected `SKILL.md`, or copy the **whole skill folder**, including references/assets/scripts, into the skill location supported by your agent. Each skill is self-contained. The funnel calculator is bundled with its skill; the repository command delegates to the same implementation. Copy-and-run portability is tested; automatic discovery and host-specific compatibility are not certified.

## How it works

Synthetic aggregate cohorts → validated inputs → explainable metrics → evidence-led investigation → human-reviewed experiment.

Agents advise; scripts calculate; humans own lending, risk and launch decisions. The calculator accepts explicitly synthetic fixtures only. Skills can reason over approved anonymous aggregates using an authorized method; never relabel real data as synthetic.

Read the [complete case](examples/lending/CASE.md), [metric contract](docs/METRICS.md), [guardrails](docs/GUARDRAILS.md), [skill specification](docs/SKILL-SPEC.md) and [roadmap](docs/ROADMAP.md).

Current iteration: v0.1 usability work. A reference implementation with synthetic data; release tagging, host evaluation and real-world validation are separate milestones. MIT licensed.
