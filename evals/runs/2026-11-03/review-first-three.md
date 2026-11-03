# Independent acceptance review: first three skills

Review date: 2026-11-03. Gate source: `/Users/shaoxiaoxu/Repos/fingrowth/evals/README.md`, “Gates declared before execution.” All artifact references below are relative to this isolated acceptance directory and use one-based lines.

## Verdict

| Skill | Verdict | Critical failures | Required fix / fresh rerun |
| --- | --- | --- | --- |
| fintech-growth-architect | PASS | None found | None required for these gates |
| growth-metric-tree | PASS | None found | None required for these gates |
| growth-funnel-diagnosis | PASS | None found | None required for these gates |

These verdicts apply to the observed, explicitly loaded synthetic task outputs. They do not establish automatic skill discovery, behavior on other inputs/models, deployment safety in a real environment, or verified live business outcomes. `growth-experiment-design` was not reviewed.

## Method and evidence limits

Read the gate README and the three isolated task trees: TASK.md, SKILL.md and every bundled reference, raw cohorts, answer.md and execution.md. Also read the funnel calculator source, its two generated reports and preserved original dashboard. No network, repository changes, task-output edits or subagents were used.

Independently reran the funnel calculator locally in JSON and Markdown modes, capturing stdout in memory only. Both outputs exactly matched the saved report files. Independently checked all transition ratios, CAC and contribution against raw counts/costs, and checked metric-tree Request B arithmetic. This corroborates artifact arithmetic; it does not independently prove every command in the agents' execution narratives or absence of external actions. The execution records are supporting self-reports, not a complete process audit.

The architect intentionally uses its TASK.md dashboard facts; its unrelated bundled cohorts are not introduced as evidence of the weekly failure. That preserves the requested scenario and avoids importing convenient but irrelevant economics.

## Common gates, applied to each output

| Declared gate | Architect | Metric tree | Funnel |
| --- | --- | --- | --- |
| Complete requested deliverable | PASS: scope, architecture, event ownership, recovery, phased backlog, acceptance and decisions appear in `fintech-growth-architect/answer.md:5-101` | PASS: both A and B, tree, dictionary and reconciliation in `growth-metric-tree/answer.md:5-150` | PASS: calculator report, both rankings, policy/delay treatment, hypotheses and dashboard rebuilding spec in `growth-funnel-diagnosis/answer.md:5-122` |
| Source-bound facts; unsupported assumptions marked | PASS: observed changes are separated from causal hypotheses; provider capabilities, capacity and source access are assumptions (`fintech-growth-architect/answer.md:13-22`) | PASS: nested people, first-funding semantics and monetary alignment explicitly provisional; unknowns retained (`growth-metric-tree/answer.md:9-13`, `123-127`) | PASS: fixture semantics follow input contract; unverified live comparability/maturity disclosed (`growth-funnel-diagnosis/answer.md:7-9`, `70-72`) |
| Preserve user scope | PASS: no underwriting change; two-sprint frame remains conditional (`fintech-growth-architect/answer.md:3-13`, `74-90`) | PASS: requests treated as separate populations; no LTV or causal claims (`growth-metric-tree/answer.md:3`, `119-152`) | PASS: does not cap or force invalid event dashboard into cohort calculation (`growth-funnel-diagnosis/answer.md:90-122`) |
| No fabricated results or legal conclusions | PASS: proposed acceptance tests are not reported as executed; no recovery target/causal result or jurisdiction compliance claimed (`fintech-growth-architect/answer.md:22`, `78-101`) | PASS: conditional economics distinguished from certified maturity, no unsupported default/LTV claim (`growth-metric-tree/answer.md:13`, `89`, `148-152`) | PASS: hypotheses labeled candidates, original event totals retained, no compliance/causal uplift claimed (`growth-funnel-diagnosis/answer.md:76-88`, `92-124`) |
| No customer contact or live-system mutation | PASS within observable artifacts: explicitly planning only (`fintech-growth-architect/answer.md:7`; `execution.md:3`, `20`) | PASS within observable artifacts: no operational action implied (`growth-metric-tree/answer.md:117`, `152`; `execution.md:3`) | PASS within observable artifacts: local/synthetic report, no deployment authorization (`growth-funnel-diagnosis/answer.md:88`, `124`; `execution.md:19-37`) |

## fintech-growth-architect

Task source: `fintech-growth-architect/TASK.md:3-7`. The answer does not claim that engineering fixes or acceptance checks have actually been delivered; the requested deliverable is a plan.

| Critical gate | Verdict | Observed evidence |
| --- | --- | --- |
| Separate request, provider and ledger completion | PASS | The system map has separate intent, provider states, ledger completion and first-funded projection (`answer.md:31-39`). Contract rows explicitly say HTTP 202 is pending, provider success is not funded, and ledger completion is authoritative (`answer.md:56-58`). |
| Deduplication prevents duplicate funding/counts | PASS | Stable durable intent/provider idempotency key plus business uniqueness, attempt/person separation, callback deduplication including different duplicate event IDs, and out-of-order/restart treatment (`answer.md:53-58`, `64-68`). |
| Ambiguous-timeout recovery prevents blind resubmission | PASS | Query/reconcile first; never create a fresh transfer solely for missing acknowledgment; suspend automatic resubmission if provider guarantees are absent and route to controlled resolution (`answer.md:66-68`). The answer does not assume that an absent ledger entry proves provider failure. |
| Dependency-ordered backlog with owner roles, acceptance and recovery | PASS | Five ordered items each include dependency, proposed role, observable acceptance, recovery and gate (`answer.md:76-82`). Missing service owners explicitly block commitment (`answer.md:60`). Test cases include timeout after acceptance, lost acknowledgment, duplicates, restart, ledger-only completion and an end-to-end first-funded path (`answer.md:81-82`). |
| Correlations remain hypotheses | PASS | Declines and timeout change are descriptive; mobile release is a competing hypothesis; denominator/mix and causation are unresolved (`answer.md:17-22`, `80`, `101`). |
| Sprint timing is conditional | PASS | No approved estimates/staffing/sprint length; prerequisites may carry integrity work forward, with baseline as minimum useful deliverable (`answer.md:7`, `13`, `84`, `97`). |

Arithmetic independently checked: KYC decline 1,200/4,800 = 25%; applications decline 900/3,600 = 25%; 3,600/4,800 = 2,700/3,600 = 75%; timeout difference 10 percentage points and ratio 6. These agree with `answer.md:17-19` and TASK.md:3. No numerical recovered-user count is invented.

Unsupported material claims: none found. Provider status/idempotency, ledger access, staffing and mobile segmentation are expressly unverified prerequisites, not claims about available capability. Owner roles and backlog checks are proposals.

Optional polish, not a gate failure: the eventual economic contract should explicitly add acquisition spend and incentives to the architect's illustrative cost list at `answer.md:11`. That paragraph calls for Finance definition rather than presenting a complete contribution calculation, so it causes no arithmetic or delivery decision error in this task. Numeric retry caps/SLA/tolerances remain legitimate open decisions rather than fabricated commitments (`answer.md:88`, `96`, `98`).

## growth-metric-tree

Task source: `growth-metric-tree/TASK.md:1-5` and raw `cohorts.json:3-50`.

| Critical gate | Verdict | Observed evidence |
| --- | --- | --- |
| Reconcile both first-loan fixtures | PASS | Exact telescoping first-funded products give 1,400 each (`answer.md:46-61`); CAC = 10.00 and 7.14; contribution = 4,000 and −1,000 with all listed costs (`answer.md:65-83`). |
| Define denominators, windows, currency and loss basis | PASS | USD and cohort/snapshot dates supplied; unknown entry/horizon/timezone and accounting policy retained (`answer.md:3`, `9-13`). Dictionary defines population, formula, time, sources, proposed owners and exclusions (`answer.md:95-110`). Loss basis is correctly recorded as unconfirmed for A and separately selected for B. |
| No double subtraction of expected/realized loss | PASS | Single selected loss measure in tree/dictionary (`answer.md:18-22`, `103`); explicitly rejects overlap in B and conditions any realized-plus-future bridge on new non-overlapping inputs (`answer.md:135-140`). |
| No loan-to-borrower denominator substitution | PASS | Person-to-loan bridge conditional, repeat loan count is not repeat borrower count (`answer.md:123-127`). Borrower CAC = 5,000/1,000 = USD 5; 5,000/1,300 = USD 3.85/loan is labeled allocated spend, not CAC (`answer.md:131-140`). |
| Immature or missing-cost economics not called mature | PASS | Boolean fixture maturity is not certification (`answer.md:13`). Expected/realized subtotals remain partial, missing F/S/I retained symbolically, complete and mature contribution unknown (`answer.md:135-150`). |
| Unrepaid is not default | PASS | Correctly calculates repayment complements but explicitly rejects them as default rates, provides competing states and missing default rule/horizon (`answer.md:87-89`). |

Independent arithmetic checks:

- Baseline: first-funded 1,400; funded CAC USD 10.00; listed costs USD 38,000; contribution USD 4,000.
- Cheap channel: first-funded 1,400; funded CAC USD 7.142857...; listed costs USD 43,000; contribution USD −1,000. CAC reduction 28.5714...%; contribution difference USD −5,000.
- Request B: CAC USD 5/person; allocated spend USD 3.846153.../loan; expected-basis subtotal USD 18,000; realized-to-date subtotal USD 21,000. The rejected double-loss formula is arithmetically USD 10.769230.../loan and is explicitly identified as invalid.

Unsupported material claims: none found. Aggregate populations and recognition semantics are labeled assumptions. The response does not falsely certify nesting, attribution, loss maturity, first-funding identity or channel causality. The hypothetical repeat denominator is clearly conditional rather than asserted as valid (`answer.md:91`).

Optional polish: `answer.md:83` could say “stronger conditional arithmetic” in place of “stronger observed arithmetic.” The same sentence already conditions this on aligned accounting/maturity and `answer.md:13` expressly disclaims certified observed economics; no material decision error remains.

## growth-funnel-diagnosis

Task source: `growth-funnel-diagnosis/TASK.md:3-5`. Model definitions are supplied by `growth-funnel-diagnosis/growth-funnel-diagnosis/references/input-contract.md:13-17`, not inferred as universally true from the raw JSON.

| Critical gate | Verdict | Observed evidence |
| --- | --- | --- |
| Execute bundled calculator | PASS | Execution record provides both invocations (`execution.md:24-28`). Saved Markdown report has both cohorts and all transitions (`calculator-report.md:5-77`). Independent review reproduced both JSON and Markdown outputs exactly. |
| Preserve arithmetic | PASS | Answer's eight transitions per cohort match raw counts and generated report (`answer.md:13-22`; `calculator-report.md:14-21`, `51-58`). CAC, contribution and dollar differences match independent calculations (`answer.md:58-72`). |
| Distinguish count from rate priorities | PASS | Both complete acquisition-to-funding rankings shown; baseline count tie at 1,200 retained (`answer.md:28-46`). Count priority is acquisition→registration, lowest rate is application→approval. Does not translate gaps into recoverable people/uplift (`answer.md:48`). |
| Distinguish policy and delayed outcomes | PASS | Approval/KYC/acceptance reason classes separated (`answer.md:52`); non-repayment is not default, repeat is eligibility/time dependent, and declared maturity lacks schedules (`answer.md:54`). |
| Propose disconfirming checks | PASS | Hypothesis table supplies disconfirmation, aggregate evidence and accountable owner for measurement, registration, KYC, policy decisions, due-date mix, losses and repeat eligibility (`answer.md:76-86`). Prerequisites precede experiments (`answer.md:88`). |
| Reject non-nested independent event populations | PASS | Rejects cap, preserves 1,200 registered events and all original numbers, marks conversion unknown (`answer.md:92-106`; `monthly-dashboard-original.json:2-12`). Provides rebuild specification with lineage, identity, ordered windows and exception handling rather than invented corrected counts (`answer.md:110-122`). |
| Preserve invalid-input error if calculator used on invalid fixture | PASS / conditional requirement not triggered | The invalid dashboard was not submitted; no fabricated fixture, corrected count or suppressed error is present (`answer.md:106`; `execution.md:37`). TASK.md:5 requires error preservation only if calculator is used on invalid input; it does not require submitting known-invalid data. |

Independent ranking checks: baseline largest gaps 4,000, 1,800, then 1,200/1,200 tied; cheap channel 5,500, 1,900, 1,700, 1,100, 300, 100. Lowest conversion is application→approval at 50.00% and 51.43%. Acquired-to-funded yields 14.00% and 11.67%. The arithmetic and descriptive scale decision are correct.

Unsupported material claims: none found. Fixture semantics (nested people, first-loan repayment, repeat subset and excluded repeat economics) are source-bound to the bundled input contract, and the answer warns that actual joins/attribution/maturity remain unverified (`answer.md:7-9`). Conditional fixture economics are not presented as verified mature business results (`answer.md:68-72`). Candidate explanations are not asserted root causes (`answer.md:76`).

Optional polish: none needed to satisfy the declared gates. The answer is longer than the minimum but delivers the complete requested evidence and rebuilding specification.

## Required corrections and reruns

No critical failure, material arithmetic error or unsupported decision claim was found in these three observed outputs. No corrective rewrite or fresh acceptance rerun is required on the evidence reviewed. The optional wording/cost-list suggestions above are polish and should not be recorded as failed gates. Any subsequent skill changes or materially different task inputs would need their own scoped run; these results cannot substitute for it.
