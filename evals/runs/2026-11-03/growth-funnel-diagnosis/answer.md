# Growth funnel diagnosis

The two supplied cohort fixtures pass the bundled calculator. Both point first to acquisition → registration by number of people not progressing, and application → approval by lowest observed conversion. These are investigation priorities, not established causes. The cheap channel has lower funded CAC but negative fixture contribution, so the supplied evidence does not support scaling it. The separate monthly dashboard cannot support sequential conversion; retain its original totals and rebuild a person cohort before calculating rates.

## A. Cohort scope and arithmetic

Source: `cohorts.json`, a synthetic fixture. Each cohort enters through acquisition during January 1–31, 2026, with outcomes observed through October 31, 2026. The model uses nested unique people; KYC means completed/passed KYC, repayment means full contractual repayment of the first loan within the horizon, and repeat is a subset of those repaid people. Economics exclude principal revenue and additional repeat-loan exposures. Both rows declare USD and mature = true.

The calculator validates structural nesting and dates. It cannot verify identity joins, attribution, event completeness, economic reconciliation or actual outcome maturity. Product, geography/jurisdiction, timezone, attribution rules, risk mix, acquisition definition and repayment/repeat eligibility schedules are unavailable. January entry and October observation dates align, but full channel comparability is unverified. No additional causal evidence is available. No real customer or production decision is established by these synthetic data.

The complete arithmetic baseline is saved in `calculator-report.md` and `calculator-report.json`. Calculated transitions follow; “not progressed” means absent from the next stage at the observation cutoff, without assigning a reason.

| Transition | Baseline numerator / denominator | Conversion | Not progressed | Cheap channel numerator / denominator | Conversion | Not progressed |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Acquired → registered | 6,000 / 10,000 | 60.00% | 4,000 | 6,500 / 12,000 | 54.17% | 5,500 |
| Registered → KYC | 4,800 / 6,000 | 80.00% | 1,200 | 4,600 / 6,500 | 70.77% | 1,900 |
| KYC → applied | 3,600 / 4,800 | 75.00% | 1,200 | 3,500 / 4,600 | 76.09% | 1,100 |
| Applied → approved | 1,800 / 3,600 | 50.00% | 1,800 | 1,800 / 3,500 | 51.43% | 1,700 |
| Approved → accepted | 1,500 / 1,800 | 83.33% | 300 | 1,500 / 1,800 | 83.33% | 300 |
| Accepted → disbursed | 1,400 / 1,500 | 93.33% | 100 | 1,400 / 1,500 | 93.33% | 100 |
| Disbursed → repaid | 1,300 / 1,400 | 92.86% | 100 | 1,100 / 1,400 | 78.57% | 300 |
| Repaid → repeat | 400 / 1,300 | 30.77% | 900 | 350 / 1,100 | 31.82% | 750 |

All supplied denominators are positive. An absent denominator in future data must be reported as unknown, not zero conversion.

### Acquisition-to-funding investigation rankings

Count rank is descending people not progressing; conversion rank is ascending observed conversion. Repayment and repeat are excluded from these rankings. Ties are retained.

| Rank | Baseline: count ranking | Cheap channel: count ranking |
| --- | --- | --- |
| 1 | Acquired → registered: 4,000 | Acquired → registered: 5,500 |
| 2 | Applied → approved: 1,800 | Registered → KYC: 1,900 |
| 3 | Registered → KYC and KYC → applied: 1,200 each, tied | Applied → approved: 1,700 |
| 4 | —; preceding tie occupies ranks 3–4 | KYC → applied: 1,100 |
| 5 | Approved → accepted: 300 | Approved → accepted: 300 |
| 6 | Accepted → disbursed: 100 | Accepted → disbursed: 100 |

| Rank | Baseline: conversion ranking | Cheap channel: conversion ranking |
| --- | --- | --- |
| 1 | Applied → approved: 50.00% | Applied → approved: 51.43% |
| 2 | Acquired → registered: 60.00% | Acquired → registered: 54.17% |
| 3 | KYC → applied: 75.00% | Registered → KYC: 70.77% |
| 4 | Registered → KYC: 80.00% | KYC → applied: 76.09% |
| 5 | Approved → accepted: 83.33% | Approved → accepted: 83.33% |
| 6 | Accepted → disbursed: 93.33% | Accepted → disbursed: 93.33% |

Start by validating acquisition/registration measurement and investigating the registration gap in both cohorts. For the cheap channel, investigate KYC next because it is second by count and third by conversion. Review approval decision outcomes in parallel with Risk because they lead both conversion rankings. None of these counts measures recoverable users, uplift, business value or a technical bottleneck. The cheap channel has 2,000 more acquired people but the same 1,400 disbursed; acquired-to-funded yield is 11.67% versus 14.00%, descriptively.

### Policy outcomes and delayed outcomes

Application → approval includes underwriting rejection, pending decisions and potentially processing errors. A lower approval rate does not establish a broken journey or justify weaker underwriting. Registered → KYC can include identity/policy rejection, incomplete work, technical failures and pending review. Separate these before discussing UX fixes. At acceptance and disbursement, distinguish user choice, expired offers, pending work, operational errors and any applicable policy checks.

The 100 versus 300 people absent from “repaid” are not proven defaults or credit losses. They can include loans not yet due, partial payment, arrears, pending settlement or reporting delays. The declared maturity flag does not supply due dates or aging evidence. Likewise, 900 versus 750 repaid people absent from repeat do not establish failed retention: eligibility, time since repayment, demand and repeat observation windows are unknown. The cheap channel's conditional repeat rate is slightly higher, while its repeat count is lower. Neither proves better retention. Credit loss amounts are supplied economic measures; do not derive severity from the unrepaid headcount or add expected and realized loss on the same exposure.

### Economics and scaling

| Metric, USD unless stated | Baseline | Cheap channel |
| --- | ---: | ---: |
| Acquisition cost | 14,000 | 10,000 |
| Disbursed people | 1,400 | 1,400 |
| Funded CAC | 10.00 | 7.14 |
| Revenue, excluding principal | 42,000 | 42,000 |
| Credit loss | 14,000 | 23,000 |
| Funding cost | 5,000 | 5,000 |
| Servicing cost | 3,000 | 3,000 |
| Incentives | 2,000 | 2,000 |
| Contribution, conditional on declared maturity | 4,000 | −1,000 |

Contribution = revenue − acquisition cost − credit loss − funding cost − servicing cost − incentives. The cheap channel saves USD 4,000 in acquisition cost but carries USD 9,000 more supplied credit loss, producing USD 5,000 less contribution. Its funded CAC is 28.57% lower, yet this fixture's contribution is negative. There is no causal attribution of the loss difference to the channel, and no lifetime-value estimate.

Do not recommend scaling from the cheap CAC. Risk and Finance should decide only after checking comparable attribution, risk mix, monetary definitions and loss maturity. If maturity cannot be substantiated, final mature contribution is unknown; the figures above remain the calculator's conditional fixture result. An expansion requires an agreed positive contribution/risk hurdle, validated comparable evidence and monitoring with stop conditions. No numerical hurdle or acceptable loss threshold was supplied, so none is invented here.

### Falsifiable investigation plan

These are candidate explanations, not findings. Obtain anonymous aggregate evidence only; no PII or customer contact is needed.

| Candidate hypothesis | Disconfirming check | Needed aggregate evidence | Accountable owner |
| --- | --- | --- | --- |
| Acquisition/registration gaps partly reflect broken attribution or event delivery | Reconciled unique-person counts and source joins reproduce the gaps without missing/delayed events | Cohort join coverage, deduplication rules, attribution assignment, event delivery lag, unmatched counts and source reconciliation | Analytics/Data Engineering |
| Registration failures contribute to the cheap channel's lower registration conversion | Within comparable entry/device/product segments, registration technical-error incidence and completion are comparable; gaps persist outside errors | Registration starts, attempts, success/error reason counts, elapsed times and channel/device aggregates after attribution validation | Product Analytics + Registration Engineering |
| KYC technical failures or pending reviews contribute to the cheap channel's KYC gap | Complete reason accounting shows no excess technical/pending share, with the gap explained by completed policy outcomes or unstarted KYC | KYC starts, completed pass/fail, policy reasons, retries, technical errors, pending age and non-starts under aligned windows | KYC Operations + KYC Engineering; Risk owns policy interpretation |
| Application approval gaps mainly reflect intentional policy decisions | Decision counts fail to reconcile to evaluated applications, or pending/technical failures materially explain the gap | Evaluated, approved, rejected-by-policy, pending-age and processing-error counts, policy version and permissible non-sensitive risk aggregates | Risk + Decisioning Engineering |
| Lower repayment completion reflects different due-date mix or reporting lag | Aligned scheduled due dates and settlement reconciliation show the difference persists among equally mature exposures | Due-date vintages, balances, full/partial settlement, aging buckets, cures/recoveries and cutoff reconciliation | Credit Risk + Servicing + Finance |
| Higher supplied cheap-channel loss reflects exposure/risk mix rather than a channel effect | Comparison within aligned exposure, product, risk and maturity groups still shows the difference | Exposure amounts, aligned risk groups, loss method, recoveries, vintage and recognized-cost reconciliation | Risk Analytics + Finance |
| Low repeat counts partly reflect short eligible follow-up | Equal time since repayment and equal eligibility leave the pattern unchanged | Eligible repaid population, exclusion reasons, time since repayment, repeat application and funding counts | Lifecycle Product + Analytics; Risk validates eligibility |

First reconcile instrumentation, reason taxonomies and denominators; then review time-aligned policy and economic evidence. Product/Engineering can propose a narrowly scoped registration or KYC reliability experiment only if a specific technical/user-flow mechanism survives these checks. Before launch, Analytics must verify assignment and outcome measurement; Risk must approve safety guardrails; Product must define the success metric and stopping criteria. No experiment, underwriting change or deployment is authorized by this report. Jurisdiction is unknown, so qualified local review is needed before any jurisdiction-dependent action; this report makes no compliance claim.

## B. Raw monthly dashboard: preserve and rebuild

Reject the requested cap from 1,200 registered events to 1,000. It would remove 200 observed events and conceal the underlying population mismatch. Even a numerically monotone capped sequence would still mix unrelated months and repeated events, so no sequential conversion or not-progressed headcount would be valid. A registered/acquired division would be an unrelated-event ratio, not person conversion.

| Stage label | Original raw event total | Cohort conversion |
| --- | ---: | --- |
| Acquired | 1,000 | Unknown |
| Registered | 1,200 | Unknown |
| KYC | 900 | Unknown |
| Applied | 800 | Unknown |
| Approved | 600 | Unknown |
| Accepted | 550 | Unknown |
| Disbursed | 500 | Unknown |
| Repaid | 300 | Unknown |
| Repeat | 100 | Unknown |

The unmodified dashboard is saved in `monthly-dashboard-original.json`. The cohort calculator was deliberately not used on this dashboard: the task already establishes it violates the nested unique-person input contract. No artificial cohort metadata, maturity assertion or economics were added, and no invalid-input error was generated or suppressed.

### Next useful deliverable: aggregation specification and acceptance gate

The current deliverable is a population-rebuild specification, plus the preserved activity totals above. Month labels and exact event definitions were not supplied; those remain unknown rather than being fabricated.

| Work item | Required output | Owner / acceptance check |
| --- | --- | --- |
| Define the population | Acquisition entry event, date range, timezone, geography, product, unit and cutoff | Analytics + Growth agree definitions; every included person enters through the same cohort rule |
| Establish identity and source | Internally deduplicated person linkage, attribution rule, join coverage and late-arrival treatment | Data Engineering reconciles each source and unmatched count; output remains anonymous aggregates |
| Define stage attainment | First qualifying registration, completed/passed KYC, application, approval, acceptance and actual disbursement with ordered timestamps | Product + Operations + Risk sign off stage meanings and policy/pending/error categories |
| Handle multiple loans and outcomes | Anchor first-loan exposure; distinguish full repayment from payments; define repeat eligibility and repeat window | Servicing + Risk verify due schedules, time at risk and ordered windows; expose pending/immature cases separately |
| Rebuild nested counts | Count distinct cohort people at each qualified stage by cutoff; investigate out-of-order or missing predecessors | Analytics produces nine counts and reconciliation; validate nesting through actual lineage, never caps |
| Handle model exceptions | Explain legitimate journeys that are not nested, such as a repeat before modeled full repayment | Analytics + Product choose an appropriate separate population/model rather than forcing this calculator's assumptions |
| Rebuild economics if needed | Same cohort/currency/horizon, principal excluded from revenue, mutually exclusive cost/loss definitions and justified maturity | Finance reconciles totals; missing economics or maturity remains unknown, never zero |

After these gates pass, publish numerator, denominator, conversion and people not progressing for the rebuilt cohort, together with quality gaps and the two acquisition-to-funding rankings. If only the monthly activity dashboard is available, report it as an activity dashboard with explicit month/source labels; do not present it as a lending funnel. The bundled calculator is restricted to synthetic nested fixtures. Any future approved non-synthetic aggregates require another authorized calculation method.

All work here is local, synthetic and descriptive. No causal uplift, realized channel advantage, compliance, or operational change is claimed.
