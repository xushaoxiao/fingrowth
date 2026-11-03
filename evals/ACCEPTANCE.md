# FinGrowth Agent and dashboard acceptance

Date: 2026-11-03. Status: the four original Skills and the added data-adapter Skill pass the observed task gates after correction of a funnel narrative error. These are explicitly loaded isolated-agent tasks, not automatic host discovery or live lending acceptance.

## Actual Agent runs

Fresh agents received only their task, copied Skill/resources and synthetic inputs. Outputs were saved without rewriting, then independently reviewed. The reviewer reproduced calculations/mappings where applicable. [Predeclared gates](README.md), [raw run artifacts](runs/2026-11-03/) and [snapshot/artifact hashes](runs/2026-11-03/manifest.json) are retained, including the failed run.

| Skill | Actual task | Final evidence | Result |
| --- | --- | --- | --- |
| fintech-growth-architect | Two-sprint recovery plan with duplicated KYC events, payment 202 counting, ambiguous timeouts and unverified causation | [Output](runs/2026-11-03/fintech-growth-architect/answer.md), [independent review](runs/2026-11-03/review-first-three.md) | PASS |
| growth-metric-tree | Reconcile two cohorts; handle repeated loans, overlapping ECL/realized loss, missing costs and immature exposures | [Output](runs/2026-11-03/growth-metric-tree/answer.md), [independent review](runs/2026-11-03/review-first-three.md) | PASS |
| growth-funnel-diagnosis | Execute calculator, compare both rankings, reject capped unrelated events and check extreme numeric cancellation | [Final fresh output](runs/2026-11-03/rerun-funnel-2/answer.md), [final review](runs/2026-11-03/review-funnel-final.md) | PASS after correction |
| growth-experiment-design | Draft document-guidance test with missing power/thresholds; assess post-treatment denominator, daily peeking and zero losses before due dates | [Output](runs/2026-11-03/growth-experiment-design/answer.md), [independent review](runs/2026-11-03/review-final-two.md) | PASS |
| growth-data-adapter | Create a reusable profile for renamed source fields; preserve 42 values/types and fail an incomplete cost export | [Output](runs/2026-11-03/growth-data-adapter/answer.md), [independent review](runs/2026-11-03/review-adapter.md) | PASS |

The initial original-cohort funnel task passed. A subsequent fresh run with a numeric regression case produced correct tables but contradictory cheap-channel prose: it incorrectly said registration led both rankings. [That failure](runs/2026-11-03/rerun-funnel/answer.md) and [its review](runs/2026-11-03/review-final-two.md) remain unchanged. The Skill now requires narrative leaders to be checked against each corresponding ranking list. A new agent, given the same task and raw inputs, produced the accepted final output. This is observed correction on these tasks, not proof of perfect future reasoning.

## Calculation fix discovered during release checks

The accepted input contract allowed costs above Decimal's default 28-digit precision. Summing a cost of `10**28 + 1` plus zero costs rounded away the final unit, making contribution zero instead of −1 against revenue `10**28`. Precision is now sized to the accepted values before summation/subtraction. Regression tests cover the −1 result and fractional `0.3 − 0.1 − 0.2 = 0`; the fresh funnel agent and reviewer also independently checked the extreme result. Such invented magnitudes do not establish production accounting suitability.

## Dashboard integration acceptance

The Next.js static dashboard uses HeroUI components. The browser run exercised:

- Every view: overview, funnel, economics, experiments, delivery and sources.
- Cohort switching: the cheap channel shows funded CAC USD 7.14, contribution USD −1,000, registration as count leader and approval as lowest-conversion leader.
- Invalid JSON workspace recovery: an incomplete import shows a contract error and keeps the existing workspace.
- Importing the **actual data-adapter Agent's generated workspace**: source field mapping appears as `segment`, `people.*` and `totals.*`, metrics reconcile and unsupplied planning arrays stay empty.
- Empty planning states and restoring the fully synthetic demo.

Browser testing caught a HeroUI collection-key collision between column and row IDs. IDs are now separately namespaced (`column-*` and `row-*`); the final rendered tables and navigation were then exercised successfully. The calculator/adapter tests do not substitute for this browser check.

The final browser pass exercised all eight theme choices through the HeroUI selector, observed a different sidebar palette for each brand, and confirmed the headline funded count remained 1,400. NVIDIA persisted after reload. At 1440×1000 and 390×844, document width matched the viewport (no whole-page horizontal overflow). The original default palette was preserved. Theme preference alone is stored; reloading returned imported data to the demo as specified. [Default desktop screenshot](../docs/images/dashboard-desktop.jpg), [NVIDIA screenshot](../docs/images/dashboard-nvidia.jpg) and [narrow screenshot](../docs/images/dashboard-mobile.jpg) shows the actual rendered workspace. Full source and release provenance live in the release manifest, not in a claimed production deployment.

## Verification limits

The original four Skills are unchanged from their accepted snapshots except the explicitly rerun funnel correction and calculator precision fix. The adapter subsequently received stricter shared browser-capacity validation; focused regression tests cover that validation delta. No task result is silently relabeled after editing its output.

Exact model identity and a complete process audit are not independently recorded; execution summaries are supporting self-reports, while artifacts, input hashes and reviewer reruns provide concrete evidence. This suite does not prove automatic discovery, all-model compatibility, legal compliance, real source approval, mature credit outcomes, live workflow execution or publication. No real customer-level data or production integrations were used.

## Final source-review corrections

An independent [source review](review-dashboard-source.md) found two material import-contract bugs: duplicate JSON fields silently overwrote values in the browser, and the mapper could emit individually valid fields whose full serialized workspace exceeded the browser capacity. The browser now parses strict JSON and rejects duplicate keys before replacing state. The mapper and browser enforce the 2,000,000-byte UTF-8 limit on canonical workspaces; timestamp clock/offset ranges are also validated explicitly to prevent normalization of malformed offsets. The [fresh bounded re-review](review-dashboard-final.md) reproduced both former failures against the corrected code and found them resolved, while normal mapper output still imported.

Final browser observations are retained in [dashboard-browser.json](dashboard-browser.json). Python/TypeScript regression tests, copied-Skill execution, strict parsing, cross-engine arithmetic and build checks remain separate evidence layers. The release manifest identifies the exact committed source used for packaging.
