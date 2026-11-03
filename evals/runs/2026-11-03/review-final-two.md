# Independent review: experiment design and funnel rerun

Review date: 2026-11-03. Gate source: `/Users/shaoxiaoxu/Repos/fingrowth/evals/README.md`, predeclared common, experiment and funnel gates. References below are task-root-relative with one-based line numbers. These are fresh verdicts on the artifacts reviewed, not inherited from the earlier run.

## Verdicts

| Task | Verdict | Material findings |
| --- | --- | --- |
| growth-experiment-design | PASS | No critical failure found; explicit launch blockers and delayed-risk scale gates are preserved. |
| rerun-funnel | FAIL | `answer.md:131` reverses the cheap-channel conversion ranking in its decision summary, contradicting the correct table and calculator. |

The rerun's extreme-scale contribution is correctly **USD −1**, independently verified from raw integers. That numeric success does not cure the separate ranking interpretation error. No repository or task output was edited. Only this review file was created.

## Method

Read both TASK.md files, the bundled SKILL.md files, all references/assets, raw inputs, answer.md and execution.md. For the funnel rerun, also read the calculator source and all saved calculator outputs/stderr artifacts. Reran all four valid calculator invocations with stdout/stderr captured in memory; each exited 0 and matched the saved corresponding files exactly. Independently calculated rates and rankings using raw integer counts/rational comparisons, contributions using Python's arbitrary-precision integer arithmetic, and pilot proportions using exact fractions. No network, external mutations or subagents were used.

Execution records remain self-reported command histories. Reproducible artifacts corroborate calculations, but do not independently establish a full historical process audit or live behavior. Neither task claims to have launched anything.

## growth-experiment-design gate assessment

Sources: `growth-experiment-design/TASK.md:3-5`, `growth-experiment-design/growth-experiment-design/SKILL.md:14-31` and its card asset at `assets/experiment-card.md:3-27`.

| Gate | Verdict | Artifact evidence |
| --- | --- | --- |
| Complete the supplied experiment card and requested pilot review | PASS | All asset fields are populated or explicitly unresolved in `growth-experiment-design/answer.md:3-37`; pilot arithmetic, objections and next action are addressed at `answer.md:39-65`. |
| ITT outcome and assignment denominator | PASS | Person randomized before exposure; one persistent 1:1 assignment across devices/sessions; atomic get-or-create and duplicate identity rules (`answer.md:7-10`). Seven-day numerator over all assigned eligible people, regardless of upload/exposure/approval, with missing data distinguished from observed non-completion (`answer.md:10`). |
| Contamination controls | PASS | Stable person identity required, no device/session randomization fallback, frozen copy/version, concurrency checks, crossovers retained in original assignment, overlap prevention (`answer.md:8-9`, `29-32`). |
| Baseline, MDE, power and eligible traffic unknowns | PASS | Unknown inputs remain unknown; proposed alpha 0.05/power 80% are explicitly approval proposals; verified sample size unresolved and not inferred from pilot counts (`answer.md:12`). Recruitment uses eligible unique assignment traffic and adds follow-up (`answer.md:13`). Unrelated channel cohorts are not used as the experiment baseline (`answer.md:5`). |
| Numeric guardrails | PASS | Guardrail table defines denominators, horizons, proposed owner and action for technical failure, complaints, consent, fraud and mature credit loss (`answer.md:16-22`). Every missing numeric threshold remains unresolved and blocks launch (`answer.md:24`, `35`). This satisfies the skill's missing-threshold behavior; inventing numerical limits would violate source-boundness. |
| Stopping procedure and multiplicity | PASS | Fixed horizon, no repeated significance testing to stop for success, separate safety monitoring and only a valid prespecified sequential alternative (`answer.md:14`). Pilot daily p<0.05 proposal explicitly rejected; retroactive stopping rules do not validate prior peeking (`answer.md:56`). |
| Delayed risk gates and scale decision | PASS | Seven-day KYC result cannot authorize economic scale; mature credit-loss horizon/review date and risk/finance gates remain unresolved (`answer.md:11`, `22`, `36`). Pilot zero loss before due dates is explicitly immature (`answer.md:57`, `61-65`). |
| Pilot descriptive proportions and supported effect arithmetic | PASS | 120/200 = 60%; 140/200 = 70%; difference 10 percentage points; relative change 16.7%; 20 observed completions and 400 displayed assignments (`answer.md:43-49`). Not claimed as causal uplift. Whole-pilot balance and seven-day endpoint comparability remain unverified (`answer.md:51`). |
| Reject post-treatment denominator | PASS | Uploaders are explicitly rejected as the primary denominator; upload metrics are exploratory diagnostics (`answer.md:55`). |
| Source-bound facts and marked assumptions | PASS | Stable identity, backend timestamp reliability and pre-assignment device eligibility labeled assumptions (`answer.md:5`). Unavailable jurisdiction, traffic, numerical limits, power and mature horizon remain missing; no fabricated results or unsupported compliance claims. |
| Scope/no customer contact or live changes | PASS within observable artifacts | Scope restricted to copy, unchanged policy/pricing/eligibility, no live authorization (`answer.md:4`, `65`); execution limitations recorded (`execution.md:3`, `18-20`). |

Independent pilot arithmetic: control = 3/5; treatment = 7/10; difference = 1/10 = 10 percentage points; relative difference = (1/10)/(3/5) = 1/6 = 16.6666…%. These are descriptive sample proportions. A p-value or power result is not required to answer the requested pilot review and is appropriately not fabricated.

Unsupported material claims: none found. Proposed methods, owners and thresholds are distinguishable from approved decisions. Status “awaiting mature outcomes” also expressly retains assignment/endpoint/guardrail blockers (`answer.md:61`), so it does not suggest maturity is the only outstanding issue.

Required correction/fresh rerun: none for this observed experiment output. Optional polish: none necessary for acceptance.

## rerun-funnel gate assessment

Sources: `rerun-funnel/TASK.md:3-8`, bundled skill interpretation requirements at `rerun-funnel/growth-funnel-diagnosis/SKILL.md:25-33`, and raw `cohorts.json` / `large-amounts.json`.

| Gate | Verdict | Artifact evidence |
| --- | --- | --- |
| Execute bundled calculator and preserve reports | PASS | All four invocations and preserved stdout/stderr listed in `rerun-funnel/execution.md:19-26`; independently reproduced `cohorts.md`, `cohorts.report.json`, `large-amounts.md`, `large-amounts.report.json` exactly with empty matching stderr. |
| Preserve fixture arithmetic | PASS for numeric tables and contribution | All cohort numerators, denominators, rates and gaps agree with raw counts (`answer.md:20-31`, `57-68`; `cohorts.md:10-21`, `47-58`). CAC 10.00/7.14 and contribution 4,000/−1,000 reconcile. C's −1 contribution is independently correct (`answer.md:195`; `large-amounts.report.json:19`). |
| Distinguish count versus rate priorities correctly throughout the deliverable | **FAIL** | The detailed cheap-channel rate table correctly places approval at 51.43% first and registration at 54.17% second (`answer.md:124-125`). But the decision summary says registration “leads both rankings” and approval is “next by conversion” (`answer.md:131`). Raw fractions are 1,800/3,500 = 51.4286…% versus 6,500/12,000 = 54.1667…%, so approval is the lowest conversion. Calculator also says so (`cohorts.md:62-63`). This is an incorrect priority interpretation, not stylistic polish. |
| Retain count ties | PASS | Baseline registered→KYC and KYC→applied both retain rank 3 at 1,200 (`answer.md:98-99`). |
| Distinguish policy and delayed outcomes | PASS | Approval remains a risk/policy outcome; unrepaid not default, repayment maturity/partial states and repeat timing are explicit (`answer.md:131-133`). Hypothesis/action plan separates technical, policy, pending and abandonment and preserves underwriting (`answer.md:139-148`). |
| Falsifiable/disconfirming checks and owners | PASS | Six hypothesis rows provide disconfirming checks, needed aggregate evidence and functional owners; interventions follow measurement/reason reconciliation (`answer.md:137-148`). |
| Reject independent event populations without corrected counts | PASS | Original 1,200 registered events preserved; sequential conversions unknown; rejects cap and specifies legitimate rebuild/alternate model (`answer.md:168-191`). No B fixture was created, so conditional invalid-calculator-error preservation is not triggered (`answer.md:191`). |
| Conditional maturity and source comparability | PASS | Declared maturity distinguished from due-date verification and unknown attribution/risk mix (`answer.md:7-9`). No scale recommendation from cheap CAC, and no channel causality or real-world scale claim (`answer.md:152-164`). |
| C: extreme monetary contribution and claim limits | PASS | Raw integer subtraction gives −1 independently; output and explanation agree (`large-amounts.json:20-25`; `large-amounts.md:10`; `answer.md:195`). Synthetic arithmetic only, no real financial/scale inference; floating-point CAC limitation acknowledged (`answer.md:197`). |
| Source-bound facts/no material unsupported claims | **FAIL for ranking statement only** | Unsupported and directly contradicted claim at `answer.md:131`; remaining hypotheses and unknowns are identified. No fabricated numeric inputs, root cause, maturity, jurisdiction or compliance result found. |
| No customer contact/live mutation | PASS within observable artifacts | No pricing/underwriting/contact/deployment action (`answer.md:164`); local-only scope and limitations (`execution.md:3`, `28`). |

### Material finding: reversed cheap-channel rate priority

`rerun-funnel/answer.md:131` conflicts with its own table and the preserved calculator report. Count ranking and conversion ranking answer different investigation questions:

- Largest not-progressed count: acquisition→registration, 5,500 people.
- Lowest observed conversion: application→approval, 1,800/3,500 = 51.43%.
- Acquisition→registration is second by lowest conversion at 6,500/12,000 = 54.17%.

A reader using the summary would investigate the wrong rate priority. The presence of correct tables elsewhere does not remove the contradictory decision instruction. The README requires no material decision error, so this observed rerun cannot pass.

Narrow required correction: align the prose summary with the existing numeric rankings and check every summary/action priority against the tables. Counts and calculator arithmetic do not need changing. Record the failure and require a fresh isolated output/review demonstrating consistent rankings; a calculator-only test cannot catch this interpretation failure. This review makes no edits and does not count as a corrected run.

### Independent C calculation, without trusting the calculator

Raw input `rerun-funnel/large-amounts.json:20-25` contains integer revenue 10000000000000000000000000000, acquisition cost 10000000000000000000000000001, and all four other cost buckets zero. Python integer subtraction, independent of the bundled Decimal implementation, yields:

```text
10000000000000000000000000000
− 10000000000000000000000000001
− 0 − 0 − 0 − 0
= −1 USD
```

This matches both JSON contribution −1.0 (`large-amounts.report.json:19`) and Markdown contribution −1.00 (`large-amounts.md:10`). The bundled source does size a local Decimal precision before subtraction (`growth-funnel-diagnosis/scripts/analyze.py:67-75`), supporting the explanatory claim at `answer.md:195` for this fixture.

The extreme funded CAC display is floating-point approximate, as acknowledged at `answer.md:197`. Exact raw-cost/1,400 is 7,142,857,142,857,142,857,142,857.143571…; `large-amounts.md:10` renders 7,142,857,142,857,142,737,305,600.00. This is not exact to cents. C specifically asks for contribution and real-world limits; the answer expressly disclaims exact CAC precision and real-world suitability, so this acknowledged limitation is not a second critical decision failure. If the standalone calculator report is intended to communicate exact currency at extreme scales, change its numeric representation/format and test that separately; do not describe the present CAC as exact.

## Required outcome

Experiment output passes the declared gates. Funnel rerun fails on the contradictory rate-priority statement at `rerun-funnel/answer.md:131`; the monetary cancellation result passes. Preserve this failed artifact and record a narrow interpretation fix plus fresh agent rerun/review before claiming the updated funnel run passes. This review does not revise the earlier separate task outputs or their verdicts.
