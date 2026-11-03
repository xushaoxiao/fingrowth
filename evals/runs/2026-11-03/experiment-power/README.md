# Experiment power forward-use evidence

Date: 2026-11-03. Scope: one synthetic KYC planning task using the explicitly loaded experiment-design Skill. No live experiment, data-source connection, customer data or business outcome is represented.

## Two records, preserved separately

1. `TASK.md`, `answer.md`, `execution.json` and `power-plan.*` record the initial separate-Agent use. JSON and Markdown both exited 0. The card correctly retained `blocked before launch`, 4,129 people per arm, 21 recruitment days plus seven primary follow-up days, and unknown delayed risk maturity. The initial script hash belongs to the pre-clarification version; it is not silently reassigned to the final source.
2. That Agent identified an interpretation gap: power at a planned +3 percentage-point alternative tests zero difference; it is not an 80% probability of proving the effect exceeds a three-point minimum worthwhile threshold. The implementer added this distinction to the Skill, method, output limits and synthetic case without changing the calculation. `followup/TASK.md`, `followup/review.md`, `followup/execution.json` and `followup/power-plan.*` retain the bounded final-source re-execution. Both commands again exited 0; numeric results remained unchanged. The final outputs explicitly preserve the statistical-versus-business-threshold distinction and unassessed launch/risk gates.

The follow-up used the same evaluating Agent; it is not another independently sampled task or a new full benchmark. The evaluator was separate from the implementer but inherited session conversation context. This was not a blinded evaluation, automatic skill discovery, cross-model study, production acceptance or independent audit of the entire process. Exact model identity was not independently recorded. The Python version in the execution records is the evaluator's recorded environment.

## Public-copy handling and hashes

The original local run artifacts were retained without rewriting. The initial answer, initial execution metadata and both runs' calculator output files are copied byte for byte; `followup/review.md` and empty stderr files are likewise unchanged. `TASK.md` and `followup/TASK.md` are public task representations with harness paths removed, not raw prompt bytes.

`followup/execution.json` is an explicitly sanitized public copy. Its command executable is normalized to `python3` and its script path made repository-relative; raw absolute machine paths are omitted. Its original execution-file SHA-256 is retained. No input values, versions, exit statuses, source hashes or output hashes were changed. The portable commands describe the same invocation arguments, rather than pretending they were the exact original executable paths.

`snapshot-manifest.json` lists final evaluated source hashes and public-artifact hashes. Those final source files were checked against the follow-up record when these artifacts were saved. It also records the original artifact hashes to distinguish unchanged copies from sanitization. Source changes after this snapshot require separately scoped validation; no Git commit or release identity is inferred from these hashes.

## Interpretation

The current calculator is a two-sided, fixed-horizon, equal-allocation normal approximation for one independent binary ITT outcome. Its output neither tests a nonzero minimum-effect null nor powers risk or monetary outcomes. Approved numeric guardrails, exposure limits, named owners and mature risk/economic review remain outside this calculation. The completed synthetic task supports the observed planning behavior only.
