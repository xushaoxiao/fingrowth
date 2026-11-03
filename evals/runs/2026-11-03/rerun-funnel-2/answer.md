# Synthetic lending funnel diagnosis

These fixtures support investigation priorities, not causal findings or a live scale decision. The cheap channel should **not be scaled on this evidence**: it has lower funded CAC but a negative declared-mature contribution. The separate monthly dashboard cannot support sequential conversion. The extreme numeric fixture produces a verified arithmetic contribution of **−1 USD**, with no real-world inference.

## A. Two acquisition cohorts

### Scope and data quality

Both fixtures describe acquisition entry from 2026-01-01 through 2026-01-31, inclusive, with outcomes observed as of 2026-10-31, in USD. The unit is a unique person in the contract's nested first-loan journey. KYC means completed/passed KYC; repaid means full contractual repayment of the first loan within the observation horizon, and repeat is a subset of those repaid people. Repeat-loan exposure is excluded from economics.

The supplied source is synthetic aggregate JSON. Both rows declare maturity, but no repayment schedules establish it independently. Jurisdiction, geography, timezone, lending product/terms, attribution reconciliation, risk mix and causal evidence are unavailable. Identical declared dates and currency are necessary comparison conditions, not proof of aligned attribution, populations or outcome maturity. The calculator validates numeric nesting; it cannot independently verify person-level joins or ordered event histories. No PII or external data was used.

### Verified calculation tables

Every conversion below is progressed / population. “Not progressed” is the observed count difference; its cause is unknown.

#### baseline

| Transition | Progressed / population | Conversion | Not progressed |
| --- | ---: | ---: | ---: |
| acquired → registered | 6,000 / 10,000 | 60.00% | 4,000 |
| registered → kyc | 4,800 / 6,000 | 80.00% | 1,200 |
| kyc → applied | 3,600 / 4,800 | 75.00% | 1,200 |
| applied → approved | 1,800 / 3,600 | 50.00% | 1,800 |
| approved → accepted | 1,500 / 1,800 | 83.33% | 300 |
| accepted → disbursed | 1,400 / 1,500 | 93.33% | 100 |
| disbursed → repaid | 1,300 / 1,400 | 92.86% | 100 |
| repaid → repeat | 400 / 1,300 | 30.77% | 900 |

#### cheap-channel

| Transition | Progressed / population | Conversion | Not progressed |
| --- | ---: | ---: | ---: |
| acquired → registered | 6,500 / 12,000 | 54.17% | 5,500 |
| registered → kyc | 4,600 / 6,500 | 70.77% | 1,900 |
| kyc → applied | 3,500 / 4,600 | 76.09% | 1,100 |
| applied → approved | 1,800 / 3,500 | 51.43% | 1,700 |
| approved → accepted | 1,500 / 1,800 | 83.33% | 300 |
| accepted → disbursed | 1,400 / 1,500 | 93.33% | 100 |
| disbursed → repaid | 1,100 / 1,400 | 78.57% | 300 |
| repaid → repeat | 350 / 1,100 | 31.82% | 750 |

### Acquisition-to-funding investigation priorities

Rank 1 is the leading descriptive candidate. Equal ranks retain ties. Only acquired → disbursed transitions are included.

| Transition | Baseline: count rank (people) | Baseline: conversion rank (rate) | Cheap: count rank (people) | Cheap: conversion rank (rate) |
| --- | --- | --- | --- | --- |
| Acquired → registered | 1 (4,000) | 2 (60.00%) | 1 (5,500) | 2 (54.17%) |
| Registered → KYC | 3, tied (1,200) | 4 (80.00%) | 2 (1,900) | 3 (70.77%) |
| KYC → applied | 3, tied (1,200) | 3 (75.00%) | 4 (1,100) | 4 (76.09%) |
| Applied → approved | 2 (1,800) | 1 (50.00%) | 3 (1,700) | 1 (51.43%) |
| Approved → accepted | 5 (300) | 5 (83.33%) | 5 (300) | 5 (83.33%) |
| Accepted → disbursed | 6 (100) | 6 (93.33%) | 6 (100) | 6 (93.33%) |

**Count priority:** investigate acquisition → registration first in both cohorts, followed by baseline application → approval and cheap-channel registration → KYC. **Conversion priority:** application → approval leads in both cohorts, followed by acquisition → registration. Baseline's 1,200-person losses at registration → KYC and KYC → application are tied by count, not by conversion. A large count gap describes reach; a low conversion describes a conditional rate. Neither establishes recoverable people, business value or an actionable bottleneck.

### Policy and delayed outcomes

Application → approval is a risk decision. Its gap may include appropriate policy rejection, pending review, technical failure or other statuses. Determine the status/reason breakdown before assigning a cause; do not interpret the 50.00% / 51.43% approval rates as a recommendation to loosen underwriting. KYC gaps likewise require separation of verification/policy outcomes from errors, unfinished work and abandonment. The 300 approved people not accepting and 100 accepted people not funded in each cohort also need status, pending-time and failure evidence before calling them UX friction.

Disbursed → repaid is 1,300/1,400 (92.86%) for baseline and 1,100/1,400 (78.57%) for cheap-channel, leaving 100 and 300 not fully repaid by the stated horizon. These counts alone do not establish delinquency, default or loss severity: schedules, exposure, due dates, partial balances, repayment allocation and recoveries are missing. Repaid → repeat is 400/1,300 (30.77%) and 350/1,100 (31.82%), respectively. The latter conditional rate is slightly higher despite a lower repeat count; repeat opportunity, eligibility and time since repayment are unknown. Neither repayment nor repeat belongs in the acquisition-to-funding friction rankings.

### Economics and scale decision

| USD, same declared horizon | Baseline | Cheap channel |
| --- | ---: | ---: |
| Recognized revenue, excluding principal | 42,000 | 42,000 |
| Acquisition cost | 14,000 | 10,000 |
| Credit loss | 14,000 | 23,000 |
| Funding cost | 5,000 | 5,000 |
| Servicing cost | 3,000 | 3,000 |
| Incentives | 2,000 | 2,000 |
| Total included costs | 38,000 | 43,000 |
| Contribution | **4,000** | **−1,000** |
| Funded people | 1,400 | 1,400 |
| Funded CAC: acquisition cost / funded people | 10.00 | 7.14 |
| Contribution / funded person | 2.86 | −0.71 |

Contribution = revenue − acquisition cost − credit loss − funding cost − servicing cost − incentives. Within the fixture, cheap-channel saves 4,000 in acquisition cost but has 9,000 more credit loss, resulting in 5,000 less contribution. Funded CAC is 28.57% lower; that does not establish superior economics. The loss amounts are supplied financial totals, not estimates derived from unrepaid people.

Do not authorize broader scale based on cheaper acquisition. These synthetic numbers favor baseline on this contribution measure, but do not establish either channel's real performance or safety. Human risk/finance owners would need reconciled attribution, aligned population and risk mix, product/terms, verified maturity, exposure-adjusted loss and complete cost recognition before deciding. If maturity is not established, mature contribution for a real decision remains **unknown**, rather than zero or the fixture's asserted final result. No scaling action is taken here.

### Falsifiable investigation plan

Owners below are proposed accountable roles, not claims of assigned personnel. All hypotheses are unproven and require approved aggregate evidence.

| Priority / hypothesis | Disconfirming check | Needed aggregate evidence | Owner |
| --- | --- | --- | --- |
| Data validity: missing or late registration/KYC events exaggerate early losses | Reconcile source logs and unique-person joins to the cohort extract; completeness and no material late arrivals weaken this explanation | Deduplicated stage totals, identity-join coverage, event delivery/lag, source-to-extract reconciliation, attribution conflicts, timezone and window definitions | Analytics / data engineering |
| Count leader: registration friction contributes to the early gap, especially cheap-channel | Separate completed, pending, error and abandoned sessions; comparable error/completion-time distributions and no error concentration weaken a technical-friction explanation | Aligned acquisition denominators, aggregate registration start/completion/error reasons, latency, retries, device/app version, time-to-register and pending age | Product + registration engineering |
| Cheap-channel's 1,900 registration → KYC gap includes verification failures or technical friction | Partition KYC outcomes; evidence that gaps are pending or correctly applied policy decisions weakens a technical-failure explanation | Submitted versus passed KYC, pending duration, aggregate verification/policy reasons, provider errors and retries; comparable cohort windows | KYC operations + engineering, with risk oversight |
| Rate leader: application → approval gap is largely intended policy rejection | Reconcile all applications to approved/rejected/pending/technical statuses; material error or stuck-review share contradicts that hypothesis | Aggregate decision reasons, rule/model version, review age, policy eligibility and comparable permissible risk/exposure bands | Risk + credit operations; engineering for errors |
| Cheap-channel's higher loss reflects a different risk/exposure mix | Compare aligned mature groups by approved permissible risk/exposure bands and product/terms; persistent differences within comparable groups weaken a mix-only explanation | Funded principal/exposure, due schedules, mature loss and recoveries, loss recognition method, product/terms, attribution and eligibility mix | Risk analytics + finance |
| Repayment/repeat count differences partly reflect timing or eligibility rather than performance | Compare common time since disbursement/repayment with verified due/eligibility schedules; stable fully mature differences weaken the timing explanation | Due dates, paid-in-full definition, pending/overdue balances, recovery timing, repeat eligibility and observation opportunity | Credit operations + lifecycle analytics + finance |

### Next actions

1. Data owner verifies denominator integrity, event order/delivery, timezone, attribution and nested cohort construction before interpreting channel gaps.
2. Product/engineering and KYC owners classify the acquisition → registration and registration → KYC gaps; risk owns the application → approval decomposition in parallel. Record pending, policy, abandonment and technical outcomes separately.
3. Risk/finance reconcile loss and cost ledgers and establish maturity from schedules. Compare like-for-like risk and exposure groups before any scale decision.
4. Only if reliable instrumentation identifies a specific registration or KYC technical issue, consider a controlled product experiment after human review. Define one change, randomization unit, primary stage completion metric and observation window in advance; monitor downstream funded contribution, mature credit loss, complaints and verification integrity. Fix no policy threshold as part of a UX experiment. The current fixtures cannot supply expected uplift, experiment sample size, duration or safe launch thresholds; owners must set these from valid baseline evidence.

## B. Unrelated monthly event dashboard

**Reject the proposed cap.** Registration at 1,200 versus acquisition at 1,000 is compatible with unrelated monthly raw-event totals, but incompatible with this nested unique-person calculator. Capping it to 1,000 changes the facts and creates an artificial 100% acquisition → registration rate. The other descending totals do not prove shared persons, cohort entry or event order.

No sequential conversion or subtraction-based person drop-off is calculated from this dashboard. I did not submit an invented cohort fixture to the calculator, so there is no invalid-run error to preserve. No date, maturity, currency or cost metadata was fabricated to make these raw totals pass validation.

### Immediate deliverable: faithful volume snapshot

The months are unrelated and their specific dates were not supplied. Keep these as raw event volumes, without a funnel interpretation.

| Event | Supplied raw count |
| --- | ---: |
| Acquired | 1,000 |
| Registered | 1,200 |
| KYC | 900 |
| Applied | 800 |
| Approved | 600 |
| Accepted | 550 |
| Disbursed | 500 |
| Repaid | 300 |
| Repeat | 100 |

### Next useful deliverable: cohort rebuild specification

| Work item | Required definition / acceptance | Proposed owner |
| --- | --- | --- |
| Establish scope | Choose acquisition-entry dates, reporting timezone, geography, product and outcome-as-of date; retain event month separately | Analytics + product |
| Rebuild person population | Use authorized internal person-level joins to deduplicate and assign each person to the acquisition cohort; provide only approved aggregate results for this analysis | Data engineering |
| Define event semantics | Specify acquisition and channel attribution, registration, passed KYC, application, approval, acceptance and actual funding; distinguish first and repeat loans | Analytics + lending operations |
| Enforce cohort order | For each cohort person count ordered milestones within agreed windows; separate reapplications and retries. Verify each downstream population is a subset of its predecessor. If the real journey does not match the model, use a suitable journey model instead | Data engineering + product |
| Expose pending and policy | Add aggregate pending ages, technical failures, abandonment and policy reason buckets rather than treating every missing next stage as a failure | Product/engineering + risk |
| Establish delayed-outcome maturity | Define repayment/eligibility horizons from loan schedules; reconcile first-loan repayment and repeat opportunity separately from monthly repayment events | Risk + credit operations |
| Add financial alignment | Reconcile recognized revenue and mutually exclusive acquisition, credit loss, funding, servicing and incentive costs to the same cohort, currency and horizon | Finance |
| Quality gate | Reconcile retained raw event volumes to source reports; document deduplication, cross-month membership, unmatched records and attribution changes; publish unique-person cohort denominators | Analytics / data engineering |

The requested follow-up dataset is an aggregate stage table for a defined cohort and horizon with a documented reconciliation, plus a maturity/financial schedule. Until it exists, sequential rates and mature contribution are **unknown**. For future approved non-synthetic aggregates, use an authorized calculation method other than this synthetic-only bundled tool; do not relabel real data as synthetic.

## C. Extreme synthetic numeric scale

The bundled calculator accepted `large-amounts.json` under the documented numeric contract and returned contribution **−1.0 USD**. The input's recognized revenue is 10^28 USD, acquisition cost is 10^28 + 1 USD, and all other costs are zero:

`10^28 − (10^28 + 1) = −1 USD`.

A separate high-precision Decimal calculation confirmed exactly −1. All four calculator executions (JSON and Markdown for each input file) exited successfully. The result demonstrates that this fixture's small negative residual survives cancellation at the extreme input scale; it does not validate financial realism, accounting completeness, loss recognition or any real-world profitability claim. These are synthetic inputs with declared, unverified maturity. The output is descriptive arithmetic and is not an accounting engine or a lifetime-value estimate.

## Preserved calculation artifacts

- `cohorts-calculator.md`: unmodified bundled readable report.
- `cohorts-calculator.json`: machine-readable steps, economics and both rankings.
- `large-amounts-calculator.md` and `.json`: unmodified large-number reports.
- `calculator-execution.json`: exact calculator command arguments and exit statuses.
- Four `*-json.stderr.txt` / `*-markdown.stderr.txt` files: stderr preserved for every invocation; all are empty because all four inputs/runs succeeded.

Execution used only local Python and supplied workspace files, without network access or external state changes. The skill and source fixtures were not modified.
