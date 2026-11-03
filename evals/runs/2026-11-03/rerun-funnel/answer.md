# Synthetic lending funnel diagnosis

All results describe invented data. No causal effect, real uplift, compliance conclusion or real channel winner is established.

## A. Scope and arithmetic

The cohorts enter through acquisition during January 1–31, 2026, and are observed as of October 31, 2026. Unit: unique people in a nested first-loan journey; economics exclude additional repeat-loan exposure. Both fixtures declare USD and mature=true. Maturity is an input assertion, not verified by contractual due dates. The calculator validates schema and arithmetic but cannot establish data completeness or accounting correctness.

Jurisdiction, timezone, product details, attribution reconciliation, risk mix, causal evidence and repayment maturity schedules are unavailable. The nominal date windows and currency match; this is insufficient to establish comparable channel quality. Acquisition means the supplied acquired population, with no further operational definition. The following preserved calculator report gives all numerators, denominators, differences and rates.

# FinGrowth synthetic cohort report

Descriptive evidence only. No automatic launch or underwriting decision.

## baseline

Window: 2026-01-01/2026-01-31; outcomes as of 2026-10-31.
Currency: USD; declared mature: true.

Funded CAC: 10.00; contribution: 4,000.00.

| Transition | Population | Progressed | Not progressed | Conversion |
| --- | ---: | ---: | ---: | ---: |
| acquired → registered | 10000 | 6000 | 4000 | 60.00% |
| registered → kyc | 6000 | 4800 | 1200 | 80.00% |
| kyc → applied | 4800 | 3600 | 1200 | 75.00% |
| applied → approved | 3600 | 1800 | 1800 | 50.00% |
| approved → accepted | 1800 | 1500 | 300 | 83.33% |
| accepted → disbursed | 1500 | 1400 | 100 | 93.33% |
| disbursed → repaid | 1400 | 1300 | 100 | 92.86% |
| repaid → repeat | 1300 | 400 | 900 | 30.77% |

### Investigation candidates

- Largest count not progressing: acquired → registered.
- Lowest observed conversion: applied → approved.

These rankings use acquired → disbursed only. Confirm event delivery, cohort mix and policy reasons before assigning a cause.

### Evidence needed before action

- Data owner: check unique-person joins, event delays and ledger reconciliation.
- Product/engineering: split technical errors, abandonment and policy decisions with approved aggregate reason codes.
- Risk/finance: check comparable risk mix and mature loss before any scale decision.

- Synthetic descriptive cohorts do not establish causes or experiment uplift.
- Approval gaps include policy rejection; repayment/repeat are delayed outcomes, not UX drop-off.
- Maturity is declared by the fixture, not verified from exposure or repayment schedules.

contribution = revenue - acquisition - credit loss - funding - servicing - incentives; immature contribution is unknown

## cheap-channel

Window: 2026-01-01/2026-01-31; outcomes as of 2026-10-31.
Currency: USD; declared mature: true.

Funded CAC: 7.14; contribution: -1,000.00.

| Transition | Population | Progressed | Not progressed | Conversion |
| --- | ---: | ---: | ---: | ---: |
| acquired → registered | 12000 | 6500 | 5500 | 54.17% |
| registered → kyc | 6500 | 4600 | 1900 | 70.77% |
| kyc → applied | 4600 | 3500 | 1100 | 76.09% |
| applied → approved | 3500 | 1800 | 1700 | 51.43% |
| approved → accepted | 1800 | 1500 | 300 | 83.33% |
| accepted → disbursed | 1500 | 1400 | 100 | 93.33% |
| disbursed → repaid | 1400 | 1100 | 300 | 78.57% |
| repaid → repeat | 1100 | 350 | 750 | 31.82% |

### Investigation candidates

- Largest count not progressing: acquired → registered.
- Lowest observed conversion: applied → approved.

These rankings use acquired → disbursed only. Confirm event delivery, cohort mix and policy reasons before assigning a cause.

### Evidence needed before action

- Data owner: check unique-person joins, event delays and ledger reconciliation.
- Product/engineering: split technical errors, abandonment and policy decisions with approved aggregate reason codes.
- Risk/finance: check comparable risk mix and mature loss before any scale decision.

- Synthetic descriptive cohorts do not establish causes or experiment uplift.
- Approval gaps include policy rejection; repayment/repeat are delayed outcomes, not UX drop-off.
- Maturity is declared by the fixture, not verified from exposure or repayment schedules.

contribution = revenue - acquisition - credit loss - funding - servicing - incentives; immature contribution is unknown


## Investigation order under both rankings

### baseline

Count ranking (largest first):

- Rank 1: acquired → registered: 4,000 not progressing; 6,000/10,000 = 60.00%.
- Rank 2: applied → approved: 1,800 not progressing; 1,800/3,600 = 50.00%.
- Rank 3: registered → kyc: 1,200 not progressing; 4,800/6,000 = 80.00%.
- Rank 3: kyc → applied: 1,200 not progressing; 3,600/4,800 = 75.00%.
- Rank 5: approved → accepted: 300 not progressing; 1,500/1,800 = 83.33%.
- Rank 6: accepted → disbursed: 100 not progressing; 1,400/1,500 = 93.33%.

Conversion ranking (lowest first):

- Rank 1: applied → approved: 1,800 not progressing; 1,800/3,600 = 50.00%.
- Rank 2: acquired → registered: 4,000 not progressing; 6,000/10,000 = 60.00%.
- Rank 3: kyc → applied: 1,200 not progressing; 3,600/4,800 = 75.00%.
- Rank 4: registered → kyc: 1,200 not progressing; 4,800/6,000 = 80.00%.
- Rank 5: approved → accepted: 300 not progressing; 1,500/1,800 = 83.33%.
- Rank 6: accepted → disbursed: 100 not progressing; 1,400/1,500 = 93.33%.
### cheap-channel

Count ranking (largest first):

- Rank 1: acquired → registered: 5,500 not progressing; 6,500/12,000 = 54.17%.
- Rank 2: registered → kyc: 1,900 not progressing; 4,600/6,500 = 70.77%.
- Rank 3: applied → approved: 1,700 not progressing; 1,800/3,500 = 51.43%.
- Rank 4: kyc → applied: 1,100 not progressing; 3,500/4,600 = 76.09%.
- Rank 5: approved → accepted: 300 not progressing; 1,500/1,800 = 83.33%.
- Rank 6: accepted → disbursed: 100 not progressing; 1,400/1,500 = 93.33%.

Conversion ranking (lowest first):

- Rank 1: applied → approved: 1,700 not progressing; 1,800/3,500 = 51.43%.
- Rank 2: acquired → registered: 5,500 not progressing; 6,500/12,000 = 54.17%.
- Rank 3: registered → kyc: 1,900 not progressing; 4,600/6,500 = 70.77%.
- Rank 4: kyc → applied: 1,100 not progressing; 3,500/4,600 = 76.09%.
- Rank 5: approved → accepted: 300 not progressing; 1,500/1,800 = 83.33%.
- Rank 6: accepted → disbursed: 100 not progressing; 1,400/1,500 = 93.33%.

In baseline, the first count priority is acquisition → registration (4,000); the lowest conversion is application → approval (50%). Registration → KYC and KYC → application tie at 1,200 people. In cheap-channel, acquisition → registration leads both rankings (5,500; 54.17%); application → approval is next by conversion (51.43%). These are investigation candidates, not proven actionable bottlenecks. Approval rates are risk/policy outcomes and do not justify weaker underwriting.

The channel differences concentrate upstream and in repayment: cheap-channel has 2,000 more acquired people but the same 1,400 funded people. Its acquisition-to-funding conversion is 11.67% versus baseline 14.00%. It has 200 fewer fully repaid people at the observation date. This does not imply 200 defaults, a specific loss severity, or a UX failure. Unrepaid can include not-yet-due, delinquent, partial repayment and other statuses. Repeat conversion depends on repayment, eligibility and time available to return; it cannot be interpreted without comparable exposure windows.

## Hypotheses and evidence plan

Each hypothesis below is unproven. Requested evidence is restricted to approved aggregate reason codes and reconciled counts; no PII or credentials are needed.

| Candidate hypothesis | Falsifiable/disconfirming check | Needed aggregate evidence | Accountable owner |
| --- | --- | --- | --- |
| Acquisition → registration has technical friction, especially on cheap-channel | Disconfirm if reconciled cohorts show normal error/latency rates and the gap persists among successful landing sessions | Delivery/deduplication checks, landing-to-registration paths, error codes and latency by channel/device, pending versus abandoned status | Analytics with acquisition and registration engineering |
| Low-intent or misattributed acquisition explains the upstream channel difference | Disconfirm if attribution is reconciled and conversion remains different within aligned campaign, product and non-sensitive risk strata | Unique-person channel allocation, overlap/attribution windows, campaign and product aggregates, matched observation periods | Growth analytics |
| Baseline KYC or application gaps include technical failures | Disconfirm if failed/pending technical states are negligible and policy/incomplete-document outcomes explain the gap | KYC attempts/completions, provider response reasons, pending age, application errors, consented aggregate status categories | KYC operations and product engineering |
| Application → approval reflects differences in policy eligibility or application completeness | Disconfirm the mix explanation if aligned eligible strata with the same policy version still have different decision outcomes | Decision/pending/withdrawal reason codes, policy versions, application completeness and risk aggregates without protected-trait inference | Human risk owner with analytics |
| Funded-to-repaid differences reflect observation maturity rather than worse credit outcomes | Disconfirm if due schedules and exposure ages align and mature repayment/loss differences persist | Due-date and exposure-age buckets, full/partial repayment, delinquency buckets and reconciled loss ledger | Risk analytics and servicing |
| Cheap-channel economics are worse because credit loss offsets acquisition savings | Disconfirm if reconciliation or aligned mature risk/exposure windows remove the loss difference | Same-horizon revenue/cost ledger, mutually exclusive cost definitions, attribution reconciliation and mature exposure loss | Finance with human risk owner |

First, analytics validates joins, nesting, attribution and event delays. Product and operations then split each gap into technical failure, user abandonment, pending work and policy rejection. Finance and risk reconcile mature economics. Only after those checks identify an actionable technical or user-flow mechanism should product propose a bounded experiment, with instrumentation verified, fixed underwriting policy, predeclared success/guardrail metrics and human review. Experiment uplift is currently unknown.

## Should cheap-channel scale?

No scale recommendation is supported. Keep expansion on hold pending human finance/risk review and evidence above. The synthetic fixture points against selecting it on CAC alone:

| USD metric | Baseline | Cheap-channel |
| --- | ---: | ---: |
| Acquisition cost | 14,000 | 10,000 |
| Funded CAC | 10.00 | 7.14 |
| Revenue | 42,000 | 42,000 |
| Credit loss | 14,000 | 23,000 |
| Funding + servicing + incentives | 10,000 | 10,000 |
| Declared-mature contribution | 4,000 | -1,000 |
| Contribution per funded person | 2.86 | -0.71 |

Cheap-channel saves USD 4,000 in acquisition expense but has USD 9,000 more recorded credit loss, lowering contribution by USD 5,000. This is a descriptive decomposition, not evidence that the channel caused the loss. Even baseline's positive fixture contribution does not establish incremental profit or justify real-world scale. No pricing, targeting, underwriting, customer-contact or deployment action is taken.

## B. Raw monthly dashboard: preserve facts and rebuild the measurement

Reject the proposed cap. Registration is 1,200 raw events, exceeding 1,000 acquisition events; changing it to 1,000 would destroy supplied facts and still would not create a nested cohort. All stages come from unrelated months and may contain repeated events or unrelated people. Sequential conversion is undefined for this dashboard. An event-count ratio could be calculated mathematically but would not answer person-level funnel conversion; none is presented as such.

| Raw event label | Supplied count | Sequential conversion |
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

The next useful deliverable is this aggregation specification, ready for analytics to implement after definitions are supplied:

1. **Measurement owner / analytics:** choose one acquisition-entry interval, explicit timezone, geography, product and observation cutoff. Define acquisition and person-level inclusion/exclusion rules; specify whether the model's repayment-before-repeat ordering fits the product.
2. **Data engineering:** use an authorized pseudonymous person key internally to deduplicate acquisitions and subsequent stage events. Enforce stage order and event-time windows, first-loan identity, and first qualifying event per stage. Publish only approved aggregates; do not export personal keys.
3. **Operations / risk:** define KYC passed/completed, complete application, decision states and approval, acceptance, actual funding, full contractual repayment and repeat qualification. Separate pending, policy decline, technical failure and abandonment; state maturity by due schedules and exposure age.
4. **Finance:** add currency and cohort/horizon-aligned recognized revenue and mutually exclusive acquisition, credit loss, funding, servicing and incentive totals. Unknown values remain unknown; do not populate missing economics with zeros.
5. **Analytics QA:** reconcile raw event counts separately from unique people; inspect unmatched joins, duplicates, out-of-order events and attribution conflicts. Explain exclusions and confirm each downstream population is a subset of its predecessor. A numerically decreasing sequence alone does not prove nesting.
6. **Deliverable acceptance:** provide a stage table with entry-window/cutoff metadata, eligible unique-person denominator, progressed numerator, pending population, gap reason counts and maturity status; sign off reconciliation before rates. If genuine journeys are not nested, use explicitly eligible transition populations or a state/loan-level model and an authorized method instead of forcing this calculator.

No B fixture was created and the calculator was not run on B: required dates, cohort identity and economics are absent, and the raw events violate its population contract. Thus there is no calculator error to preserve for B. The supplied dashboard remains intact above. The bundled calculator is synthetic-only; any future actual aggregate data needs another authorized calculation method.

## C. Extreme-scale numeric fixture

The bundled calculator ran successfully on unchanged large-amounts.json; both its Markdown and JSON reports are preserved. Reported contribution is **USD -1.00**. Revenue is exactly 10,000,000,000,000,000,000,000,000,000 and acquisition expense is exactly 10,000,000,000,000,000,000,000,000,001; all other listed costs are zero. Exact integer subtraction independently yields -1. The calculator uses decimal precision sized to these accepted inputs before subtraction, preserving the one-unit difference despite the extreme common magnitude.

This verifies cancellation for this fixture, not arbitrary monetary precision or production accounting suitability. Funded CAC is emitted through floating-point division at an extreme scale and should not be treated as exact to cents. The accepted numeric contract and successful exit do not establish realistic amounts, valid source accounts, true maturity, compliance, actual profitability or causation. The result warrants only a synthetic arithmetic claim; it warrants no real-world financial or scale conclusion.
