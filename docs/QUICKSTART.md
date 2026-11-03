# From a growth question to a reviewable experiment

This walkthrough uses invented aggregate data and the four existing skills. Python 3.10+ is needed only for the deterministic funnel calculator; no external libraries, account access or production integration is required.

## 1. Run and inspect the evidence

From the repository root:

```sh
python3 scripts/analyze.py examples/lending/cohorts.json --format markdown
python3 scripts/analyze.py examples/lending/cohorts.json
```

The first command prints a readable report; the second prints JSON for downstream tools. See [REPORT.md](../examples/lending/REPORT.md) for the generated result and [the input contract](../skills/growth-funnel-diagnosis/references/input-contract.md) before changing the fixture. Invalid input exits with status 2 and no partial report.

Expected checks:

- Baseline funded CAC = USD 10; contribution = USD 4,000.
- Cheap-channel funded CAC ≈ USD 7.14; contribution = USD −1,000.
- Baseline acquired → registered has the largest count not progressing (4,000).
- Baseline applied → approved has the lowest observed acquisition-to-funding step conversion (50%). This includes policy decisions and is not permission to increase approval.
- The case does not establish why the second cohort has higher loss. Do not select a winning channel from CAC alone.

## 2. Give an agent a concrete task

Ask the agent to read the named skill file first. These prompts use repository-relative paths; resolve them from the checkout or supply your actual installed skill path. Separate agent-generated analysis from the calculator's verified arithmetic.

### Architecture

```text
Read skills/fintech-growth-architect/SKILL.md and its delivery worksheet.
Use examples/lending/CASE.md as a fully synthetic scenario.
Design the minimum delivery backlog to distinguish KYC technical failures,
policy rejection and abandonment. Include event owners, recovery paths,
acceptance checks and open decisions. Do not invent a jurisdiction or results.
```

### Metric tree

```text
Read skills/growth-metric-tree/SKILL.md.
Use examples/lending/cohorts.json and docs/METRICS.md.
Reconcile first-funded people, funded CAC and contribution for both cohorts.
Explain why their CAC ranking and contribution ranking differ.
Identify unknowns before using this model for loan-level or repeat-loan economics.
```

### Funnel diagnosis

```text
Read skills/growth-funnel-diagnosis/SKILL.md.
Run the bundled calculator on examples/lending/cohorts.json and produce Markdown.
Use the evidence to rank investigation candidates by count and conversion.
For each leading hypothesis, list a disconfirming check, needed aggregate evidence
and proposed owner. Distinguish policy outcomes from technical friction.
```

### Experiment design

```text
Read skills/growth-experiment-design/SKILL.md and fill its experiment-card asset.
Design a synthetic experiment on clearer document-upload guidance.
Primary outcome: KYC completion within seven days of assignment.
Baseline, MDE, eligible daily traffic and approved guardrail thresholds are unknown.
Keep these unresolved and state whether the design can launch or scale.
```

The final card should remain **blocked before launch** until power and numeric guardrails are resolved. A seven-day KYC outcome does not establish mature credit-loss performance.

## 3. Try a standalone copy

Copy an entire `skills/<name>/` folder to the skill location supported by your agent. Do not copy only `SKILL.md`: its linked resources are part of the workflow. This repository does not modify your agent configuration or overwrite existing installed skills.

To inspect portability without changing your agent settings, run from the repository root:

```sh
trial_dir="$(mktemp -d)"
cp -R skills/growth-funnel-diagnosis "$trial_dir/growth-funnel-diagnosis"
cp examples/lending/cohorts.json "$trial_dir/cohorts.json"
python3 "$trial_dir/growth-funnel-diagnosis/scripts/analyze.py" "$trial_dir/cohorts.json" --format markdown
```

You can also create a new synthetic fixture using the complete JSON example in the copied skill's `references/input-contract.md`. The script needs no repository files. This is a file-copy and execution check, not proof that a host automatically discovers or invokes the skill. Host-specific evaluation remains on the roadmap.

## 4. Validate changes

```sh
python3 -m unittest discover -s tests -v
python3 scripts/analyze.py examples/lending/cohorts.json --format markdown > examples/lending/REPORT.md
git diff -- examples/lending/REPORT.md
```

Tests cover calculations, population reconciliation, zero denominators, maturity, malformed input, CLI errors and copied-skill execution. If changing the fixture or report implementation, regenerate the checked-in report and review the diff. CI also checks reproducibility.
