# Execution record

## Files read

- `TASK.md`: task requests A, B and C and limitations.
- `growth-funnel-diagnosis/SKILL.md`: workflow and decision boundaries.
- `growth-funnel-diagnosis/references/input-contract.md`: accepted synthetic data and output contract.
- `growth-funnel-diagnosis/scripts/analyze.py`: bundled calculator implementation.
- `cohorts.json` and `large-amounts.json`: unchanged input fixtures.
- Generated calculator JSON reports were read to construct and reconcile `answer.md`.

## Commands run

All commands ran in this workspace; no network or repository access was used.

1. `cat TASK.md && cat growth-funnel-diagnosis/SKILL.md` — read instructions.
2. `find . -type f -maxdepth 4 -print` — inventory workspace files.
3. `cat growth-funnel-diagnosis/references/input-contract.md cohorts.json large-amounts.json growth-funnel-diagnosis/scripts/analyze.py` — read contract, fixtures and implementation.
4. Local `python3` heredoc — invoked the bundled calculator four times with Python 3, saved unmodified stdout and stderr and recorded exact arguments/exit codes in `calculator-execution.json`; printed rankings and cross-checked the extreme contribution with Decimal precision 80. Equivalent calculator commands were:
   - `python3 growth-funnel-diagnosis/scripts/analyze.py cohorts.json --format json`
   - `python3 growth-funnel-diagnosis/scripts/analyze.py cohorts.json --format markdown`
   - `python3 growth-funnel-diagnosis/scripts/analyze.py large-amounts.json --format json`
   - `python3 growth-funnel-diagnosis/scripts/analyze.py large-amounts.json --format markdown`
5. Local `python3` heredoc — read generated report JSON and wrote `answer.md` and this record. Reused calculator step values to render both funnel tables.
6. Final local `python3` heredoc — checked saved reports, contribution, rank leaders/ties, key input values against the supplied fixture facts, and presence of the finished deliverables. See tool execution for assertion result.

## Results and limits

- Four calculator runs exited 0. All stderr files are retained and empty. No calculator error occurred.
- The unrelated monthly dashboard was not run through the cohort calculator. Its original values are preserved in `answer.md`; no cap or fabricated metadata was applied.
- Large fixture contribution is −1.0 from the bundled tool and exactly −1 from the independent Decimal calculation.
- Only local supplied files and generated files were used. No external verification, causal evidence, jurisdiction, timezone, attribution reconciliation or maturity schedule was available. No scale, underwriting, customer-contact or deployment action was taken.
- `TASK.md`, the skill and both input fixtures remain unmodified.
