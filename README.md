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

## First business workflow

[Registration → profile → KYC → bank details → credit approval](examples/registration-credit/README.md) is the first selected business journey. Its aggregate intake keeps counts and observation windows unknown until supplied and reviewed. It is separate from the nine-stage synthetic calculator contract; no conversion or bottleneck is claimed yet.

## Use the Skills

| Skill | Use it for | Deliverable |
| --- | --- | --- |
| [fintech-growth-architect](skills/fintech-growth-architect/SKILL.md) | Design the system and delivery plan | System/event ownership map and phased backlog |
| [growth-metric-tree](skills/growth-metric-tree/SKILL.md) | Define risk-adjusted growth | Reconciled metric tree and dictionary |
| [growth-funnel-diagnosis](skills/growth-funnel-diagnosis/SKILL.md) | Investigate conversion and channel quality | Calculation report, hypotheses and evidence checks |
| [growth-experiment-design](skills/growth-experiment-design/SKILL.md) | Prepare a controlled test | Experiment card with power and delayed-risk gates |
| [growth-data-adapter](skills/growth-data-adapter/SKILL.md) | Adapt an authorized aggregate source | Validated dashboard workspace with field provenance |

Ask an agent to read the selected `SKILL.md`, or copy the **whole skill folder**, including references/assets/scripts, into the skill location supported by your agent. Each skill is self-contained. The funnel calculator is bundled with its skill; the repository command delegates to the same implementation. Copy-and-run portability is tested; automatic discovery and host-specific compatibility are not certified.

## Open the dashboard

The Next.js + HeroUI workspace brings funnel, economics, experiment plans, delivery and data provenance together. Import a workspace produced by the data-adapter Skill to reuse the views with another approved aggregate source. Choose Default, Tesla, NVIDIA, AMD, Meta, Google, Amazon or Uber inspired themes.

```sh
cd dashboard
npm ci
npm run dev
```

Read [the dashboard guide](docs/DASHBOARD.md) and [data contract](docs/DATA-CONTRACT.md). The app runs locally and exports as static files; imported data stays in tab memory.

## Plan one binary experiment (next iteration)

The working branch adds a dependency-free power planner for independent people, 1:1 allocation, a two-sided fixed-horizon test and one binary ITT primary outcome:

```sh
python3 scripts/plan_power.py --baseline 0.60 --mde-absolute 0.03 --alpha 0.05 --power 0.80 --eligible-per-day 400 --primary-followup-days 7 --format markdown
```

These invented assumptions require 4,129 people per arm. Recruitment and primary follow-up are separate from delayed credit-risk review. Calculating power does not approve a launch or demonstrate minimum business value. Read the [synthetic experiment card](examples/experiments/KYC-POWER.md) and [method limits](skills/growth-experiment-design/references/power-planning.md). This addition is not in the frozen v0.1.0 release assets.

## How it works

Synthetic aggregate cohorts → validated inputs → explainable metrics → evidence-led investigation → human-reviewed experiment.

Agents advise; scripts calculate; humans own lending, risk and launch decisions. The calculator accepts explicitly synthetic fixtures only. Skills can reason over approved anonymous aggregates using an authorized method; never relabel real data as synthetic.

Read the [complete case](examples/lending/CASE.md), [metric contract](docs/METRICS.md), [guardrails](docs/GUARDRAILS.md), [skill specification](docs/SKILL-SPEC.md) and [roadmap](docs/ROADMAP.md).

v0.1.0: see [Agent acceptance](evals/ACCEPTANCE.md), [release preparation](docs/releases/v0.1.0.md) and [changelog](CHANGELOG.md). Explicitly loaded Agent tasks are evaluated; automatic host discovery and real-world lending outcomes remain separate milestones. MIT licensed.
