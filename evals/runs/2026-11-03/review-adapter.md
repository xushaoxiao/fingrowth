# Independent growth-data-adapter acceptance review

Review date: 2026-11-03. Gate source: `/Users/shaoxiaoxu/Repos/fingrowth/evals/README.md`, common gates and “Dashboard extension: adapter acceptance.” Artifact references are relative to the isolated task root and use one-based lines.

## Verdict

**PASS for the observed growth-data-adapter task.** All critical gates are satisfied. No material correction or fresh acceptance rerun is required on these artifacts. The successful adaptation, missing-cost failure, exact mapping fidelity and input-integrity evidence are corroborated independently below. No dashboard/browser acceptance or cross-engine application arithmetic is inferred from this agent-output review.

## Scope and independent method

Read `growth-data-adapter/TASK.md`, bundled skill, workspace contract, both example profiles and mapper source; source/profile/workspace; incomplete input; answer/execution records; status/stdout/stderr artifacts; and input-integrity.json. Constructed the expected 21 target/source mappings independently from the source shape and canonical contract, then checked every mapping and all 42 copied scalar values and their exact Python types across both rows. Checked metadata, flags, planning arrays, complete provenance and current protected-file SHA-256 hashes against both recorded snapshots.

Reran the bundled mapper for both inputs with the same profile, omitting `--output` so review execution wrote no workspace files. Valid stdout exactly equals saved workspace.json; invalid input reproduced exit 2, empty stdout and exact saved stderr. The saved agent invocation with `--output` is recorded in execution.md; current absence of incomplete-workspace.json and source code ordering corroborate no partial output. No network, subagents, repository changes or task-output edits were used. Only this review file was created.

## Gate-by-gate assessment

| Gate | Verdict | Observed one-based evidence |
| --- | --- | --- |
| Complete requested deliverables and actual bundled execution | PASS | Reusable profile, workspace and concise lineage/limits/failure answer exist (`growth-data-adapter/profile.json:1-37`; `workspace.json:1-174`; `answer.md:3-27`). Actual two mapper commands/results recorded (`execution.md:24-39`), valid exit 0 preserved (`valid.exit-status.txt:1`). Reviewer reproduced exact valid workspace and failure response. |
| Truthful synthetic/approved status | PASS | TASK.md:1 declares invented aggregates. Source flags `invented: true` remain true (`source.json:7`, `34`); explicit mapping at `profile.json:17`; workspace `data_mode: synthetic` and both actual synthetic booleans true (`workspace.json:5`, `137`, `162`). Approval reference null is appropriate for synthetic data (`profile.json:10`; `workspace.json:11`). No real data is relabeled or approval invented. |
| Complete source field mapping | PASS | Independent expected set has exactly 21 canonical scalar targets: six metadata/flag scalars, six amounts and nine counts. Explicit profile covers each exactly once (`profile.json:13-33`), matching the actual source shape rather than copying the differently shaped example. Both source rows are retained and values/types match for every target. |
| Complete provenance | PASS | Correct source name, supplied extraction timestamp, UTC, cohort definition and null approval reference (`profile.json:6-10`; `workspace.json:7-11`). Generated mapping list covers all 21 unique targets with exact source paths and `copy without coercion` (`workspace.json:12-118`). Definition records first-loan nesting, repayment-before-repeat, excluded repeat economics, supplied maturity and unknown accounting/loss basis. |
| Exact preservation of counts and economics | PASS | Baseline source counts/amounts (`source.json:10-26`) match `workspace.json:123-144`; cheap counts/amounts (`source.json:37-53`) match `workspace.json:148-169`. No coercion, cap, aggregation, unit conversion or imputation found. Every copied scalar's type also matches. |
| Preserve supplied maturity rather than certify it | PASS | `outcomes_closed` booleans map to `mature` (`profile.json:18`; `workspace.json:138`, `163`). Provenance and answer explicitly identify maturity as supplied metadata, not schedule verification (`workspace.json:10`; `answer.md:11`, `15`). |
| Empty planning arrays | PASS | User requires empty cards (`TASK.md:1`). Profile arrays empty (`profile.json:35-36`) and workspace arrays empty (`workspace.json:172-173`); hypothetical example cards were not imported. |
| Reject missing cost without zero-fill | PASS | Incomplete baseline totals omit servicing cost (`incomplete-source.json:20-25`), while mapping still requires it (`profile.json:23`). Preserved exit 2 (`incomplete.exit-status.txt:1`) and exact error (`incomplete.stderr.txt:1`); stdout empty. Answer rejects zero and even rejects unjustified fallback from the complete file (`answer.md:17-25`). |
| No partial output or input mutation | PASS on available evidence | No incomplete-workspace.json exists. Mapper builds/validates before writing (`growth-data-adapter/scripts/build_workspace.py:238-248`), missing path fails (`scripts/build_workspace.py:165-200`). Recorded before/after SHA-256 values agree for all eight protected files (`input-integrity.json:3-23`); reviewer recomputed all current hashes and confirmed both snapshots. |
| Source-bound facts, assumptions and blockers | PASS | Answer distinguishes contract semantics from missing event-level proof (`answer.md:10`), discloses revenue/principal recognition, loss basis, mutual-exclusion/alignment and maturity gaps, and assigns next action to source/finance/data owners (`answer.md:13-15`). Does not claim business performance, compliance or launch readiness. |
| Preserve scope: no customer contact/external publication/live mutation | PASS within observable artifacts | No external access, dashboard import, publication or launch claimed (`answer.md:27`; `execution.md:5`, `48`). Work remains local aggregate adaptation; no private material or operational action introduced. |

## Complete mapping and value reconciliation

All mappings below were independently checked, including exact types. Metadata strings remain strings, both flags remain actual booleans, and all supplied counts/amounts remain integers.

| Canonical target | Source path | Baseline | Cheap channel |
| --- | --- | --- | --- |
| cohort | segment | baseline | cheap-channel |
| window | entry_dates | 2026-01-01/2026-01-31 | 2026-01-01/2026-01-31 |
| outcome_as_of | observed_on | 2026-10-31 | 2026-10-31 |
| currency | money_unit | USD | USD |
| synthetic | invented | true | true |
| mature | outcomes_closed | true | true |
| counts.acquired | people.acquired | 10000 | 12000 |
| counts.registered | people.registered | 6000 | 6500 |
| counts.kyc | people.kyc | 4800 | 4600 |
| counts.applied | people.applied | 3600 | 3500 |
| counts.approved | people.approved | 1800 | 1800 |
| counts.accepted | people.accepted | 1500 | 1500 |
| counts.disbursed | people.disbursed | 1400 | 1400 |
| counts.repaid | people.repaid | 1300 | 1100 |
| counts.repeat | people.repeat | 400 | 350 |
| acquisition_cost | totals.acquisition_cost | 14000 | 10000 |
| revenue | totals.revenue | 42000 | 42000 |
| credit_loss | totals.credit_loss | 14000 | 23000 |
| funding_cost | totals.funding_cost | 5000 | 5000 |
| servicing_cost | totals.servicing_cost | 3000 | 3000 |
| incentives | totals.incentives | 2000 | 2000 |

Line evidence: source metadata at `source.json:3-8`, `30-35`; counts/economics at `source.json:10-26`, `37-53`; explicit mapping at `profile.json:13-33`; canonical rows at `workspace.json:123-169`; generated provenance at `workspace.json:12-118`. No field is omitted, duplicated, renamed to a wrong semantic target, or assigned a fallback constant.

Provenance top-level metadata was checked for exact equality with profile metadata. Name/description/data mode are preserved, schema_version is 1.0, source extraction UTC timestamp agrees with TASK.md:1, and both observed windows/cutoffs agree with the source. Unknown loss/recognition details remain explicitly unknown rather than fabricated definitions.

## Incomplete-input and integrity evidence

The actual reproduced error is:

```text
Invalid workspace input: source[0]: a mapped source field is missing
```

The error identifies the first source row; manual path comparison establishes the specific missing `totals.servicing_cost`. The source is not patched. Baseline servicing cost in the complete source remains 3000, but the answer correctly refuses to infer that it supplies the missing value for a separate extract without source-owner confirmation (`answer.md:23-25`). This is stronger evidence than a generic “missing means unknown” declaration because the actual mapper failure and unchanged missing key are observed.

The SHA-256 manifest covers TASK.md, both source files, SKILL.md, workspace-contract.md, both asset profiles and build_workspace.py. All eight current protected files match their recorded before and after digests. This corroborates the observed immutable inputs, while recognizing that the manifest itself is an agent-produced history rather than independent original ingestion attestation. The read-only review reruns did not write output files.

## Required corrections and limits

No required correction found. No unsupported material claim or arithmetic/decision error found in the adaptation. The answer truthfully limits success to contract validation and faithful copying; semantic/accounting review remains an identified downstream requirement. Browser layout, Next.js/HeroUI behavior, actual dashboard import and cross-engine metric arithmetic are separate milestones and are not validated by this review.
