# Two-sprint plan to recover verified first-funded users

The first delivery goal is to establish a trustworthy funding baseline and recover proven technical failures. The supplied dashboard does not establish the size or cause of a first-funded-user decline: it counts provider HTTP 202 responses as funding, while KYC request events can count the same person repeatedly. Underwriting remains unchanged throughout this plan.

## Scope, success and feasibility assumptions

This is a proposed consumer-lending architecture and backlog, not an approved delivery commitment or launch. All owners below are proposed role owners. Growth product must secure named accountable owners, capacity and estimates before committing scope. No jurisdiction, eligibility policy, repayment maturity or approved stop thresholds was supplied. This plan authorizes no deployment, customer contact, pricing change or underwriting action.

Define the primary recovery measure as unique, eligible first-funded people with a first authoritative ledger-confirmed disbursement, attributed to a fixed entry cohort and measured within an agreed conversion window. Deduplicate a person across attempts and loans; exclude previously funded people using reconciled history. Publish both the count and the rate from the fixed cohort denominator, alongside pending outcomes and cohort age. Calendar-week ledger funding is a useful operations count but is not interchangeable with cohort conversion.

Economic success requires recovered net contribution, not merely more disbursements: finance should define funded principal, revenue, funding cost, variable provider/servicing cost and expected/realized credit losses on consistent cohorts. Risk and finance must approve the loss and fraud measures, maturity windows and comparison rules. Track complaints, duplicate disbursement incidents and applicable consent constraints as guardrails. Preserve current policy and record its version. Until outcome maturity and risk mix are reconciled, report operational recovery only; do not declare improved profitability or unchanged credit quality.

Proposed feasibility assumptions: ledger history and KYC/application outcomes are accessible to the assigned engineers and data team; privacy-safe stable join keys can be used; provider status lookup and idempotency capabilities can be confirmed promptly; the mobile release can be segmented by version; operations can handle exceptions. Sprint length, staffing and estimates are unknown. The two-sprint frame is a sequencing envelope, with each sprint ending in a gate. If prerequisites fail, carry unfinished integrity work forward and defer optimization. A reliable baseline is the smallest useful deliverable even if repair cannot fit.

## What the supplied figures establish

- Reported KYC completions fell 1,200, or 25%; reported applications fell 900, also 25%.
- The aggregate applications/KYC ratio is 75% in both weeks. It is not a person-level transition rate unless populations, timestamps, deduplication and conversion windows align.
- Timeout share rose by 10 percentage points, from 2% to 12% (sixfold). Its request denominator and provider/stage are not specified. It cannot be translated into lost people or loans.
- A mobile release occurred midweek. Timing creates a competing hypothesis, not proof of a regression. Attribution, risk mix, reporting completeness, traffic volume and cohort maturity remain unresolved.

Investigate provider degradation, mobile regression and measurement distortion together. Compare stage-specific outcomes and latency by attempt, unique person, mobile version, platform, release exposure time, provider and acquisition cohort. Reconcile traffic/attribution and risk-policy mix before interpreting subgroup differences. Old and new mobile versions can have different populations; observational comparisons alone do not prove a release effect. There is no defensible numeric first-funded recovery target or causal effect estimate yet.

## Minimal architecture

```text
Acquisition / registration (denominator and attribution reconciliation)
    → KYC case + attempt records [identity]
    → persisted application [application service; owner to confirm]
    → existing risk decision → approval → customer acceptance [unchanged]
    → durable disbursement intent [payments]
    → provider accepted / pending / succeeded / failed
    → authoritative completion in payments ledger
    → deduplicated first-funded projection [data]

KYC outcome records ──────────────┐
Application / decision records ───┼→ replayable event or extract ingestion
Payments intent / provider log ──┤   → cohort funnel + pending/error counts
Payments ledger ─────────────────┘   → daily source reconciliation

Scheduled reconciliation + exception queue → operations + engineering
```

Use existing durable records and a small ingestion/projection job first. An outbox or equivalent durable change feed is appropriate where event publication must follow a committed state change. Do not require a new central orchestration platform. Separate business rejection, user abandonment, technical failure and unresolved/pending states. An absent event is unknown until source reconciliation establishes what happened; abandonment requires an agreed inactivity rule and must not silently absorb timeouts.

## Event and source ownership

Every proposed contract carries an event ID, schema version, privacy-safe logical subject key, case/application/intent key as applicable, attempt key, occurrence and ingestion timestamps, source, state/reason category and policy/app version where relevant. This specifies semantics, not customer payloads. Restrict identifier access; publish aggregate outputs. Data owns projection logic and source tie-outs, while each producer owns its business facts.

| Transition / event | Completion meaning and authoritative source | Proposed owner / consumer | Counting and dependency |
| --- | --- | --- | --- |
| Registered/eligible cohort entry | Durable registration plus agreed eligibility rule; source must be identified | Growth product defines population; data maps source | One person per entry cohort; attribution must reconcile before channel comparisons |
| KYC submitted / attempt outcome | Attempt records explain technical responses; persisted KYC case outcome determines verification completion | Identity engineering produces; data consumes | Count attempts separately; one qualifying completion per person/case definition; rejection and timeout remain distinct |
| Application submitted | Persisted business application, not button click or request acceptance; source to confirm | Application-service ownership unresolved; growth product coordinates, data consumes | Unique applications plus unique applicants; stable KYC/application join required |
| Risk decision / approval / acceptance | Existing decision and customer acceptance records, with policy version | Risk owns policy/interpretation; executing service owner to confirm | Preserve existing authority; distinguish rejection from technical error; accepted population feeds payments |
| Disbursement intent created | Durable intent linking accepted loan and stable provider idempotency key | Payments engineering | Unique logical disbursement, with multiple delivery attempts; enforce business uniqueness across requests |
| Provider accepted / status updated | HTTP 202 means accepted/pending only; authenticated callback or status response describes provider state | Payments engineering; operations handles exceptions | Event IDs deduplicate delivery; intent state handles different duplicate event IDs and out-of-order messages; provider success is not funded |
| Ledger funding confirmed | Authoritative disbursement-completion entry; finance and payments confirm qualifying entry type, effective date and correction treatment | Payments engineering owns source; finance validates meaning; data projects | Unique ledger entry and logical disbursement; first-ever qualifying funding per person; corrections update projections through auditable rules |

Registration/application and executing risk-service owners are prerequisites, not assumed members of identity or payments. If no responsible service owner can be assigned from the available team, the affected integration is outside the two-sprint commitment.

## Recovery behavior

**KYC.** Persist case and attempt state before exposing retry options. Retry eligible technical failures with bounded exponential backoff and jitter using provider-supported request/case keys. Do not retry policy rejections as technical failures. Resolve ambiguous provider outcomes through status lookup or reconciliation before creating another paid or conflicting verification. Cap attempts and elapsed time; unresolved cases enter an approved operations queue. Resume the same journey without bypassing verification. A successful retry must not generate a second person completion.

**Payments.** Persist a unique disbursement intent and idempotency key before dispatch; all retries reuse the same logical key. A 202 response or a timeout leaves the intent pending/unknown. A timeout may mean the provider accepted the transfer: query status and reconcile with the ledger before retrying. Never create a new transfer merely because an acknowledgment is absent. If the provider cannot guarantee idempotency/status lookup, suspend automatic resubmission for ambiguous intents and route them to controlled operations resolution. This capability gap can prevent an automated repair within two sprints.

Authenticate callbacks using the provider's supported mechanism; durably record and acknowledge them, deduplicate deliveries and apply valid state transitions. A stale callback must not regress a terminal state. Different callback IDs for the same success still refer to one intent. Provider success without a qualifying ledger entry remains a reconciliation exception, not funded. Ledger completion must reach the dashboard even if its callback was lost. Use durable ingestion checkpoints, replay and uniqueness constraints so restarts do not double count or silently skip entries. Age pending intents against an agreed SLA and escalate; crossing an SLA alone never means failed or funded.

**Reconciliation.** Each run accounts for requests/intents as pending, rejected/failed or completed, with age and reason categories, and ties completed funding to the ledger. Record run watermark, counts, discrepancies and resolution owner. Never rewrite financial history to make a dashboard balance. Historical dashboard restatement must carry a definition/version and before/after bridge; retain the old output for audit, clearly marked invalid for funding decisions.

## Smallest useful phased backlog

No parallel experiment platform, new campaigns, entitlement service or targeting system is required. Workstreams may overlap only after owner/capacity confirmation; data work and financial-state safety take precedence over conversion optimization.

| Phase / priority | Deliverable and dependency | Proposed accountable role | Observable acceptance | Rollback / recovery | Decision gate and evidence that changes the recommendation |
| --- | --- | --- | --- | --- | --- |
| Sprint 1 / 1 | Agree cohort, first-funded definition, entry window, taxonomy, guardrails and source map; obtain named service owners and access | Growth product, with data/risk/finance approval | Reproducible definition with explicit pending and maturity treatment; jurisdiction, ownership and missing thresholds recorded | Version definitions; retain original extracts and mark unvalidated outputs | Approved scope/capacity required. If ledger semantics or identifiers are unresolved, limit work to source reconciliation |
| Sprint 1 / 2 | Build minimal ledger-derived first-funded baseline and KYC/application deduplication; depends on 1 | Data, with payments and identity source sign-off | Controlled fixture with repeated KYC attempts and repeated callbacks counts one person; all qualifying ledger rows map or appear in an explained exception total; rerun produces identical totals | Disable new dashboard consumer and replay from source/checkpoint; do not fall back to calling 202 funded | Finance validates qualifying ledger entries and historical first-funding coverage. Unmapped history blocks a reliable first-ever label |
| Sprint 1 / 3 | Diagnose provider and mobile hypotheses; inspect payments duplicate-transfer exposure immediately; depends on source access, with final analysis using 2 | Identity engineering for KYC; payments engineering for disbursement; growth product coordinates release investigation | Attempt-to-case/intents reconcile; pending, retries, rejections and unknowns accounted for; version/provider timelines and attribution/risk mix reviewed; residual discrepancy has owner | Preserve logs/records; reversible mitigation only through approved release process | Provider traces supporting failures justify bounded recovery; version-specific reproducible failure justifies mobile repair. If counts shift after deduplication or mix adjustment, revise diagnosis. No causal claim from timing alone |
| Sprint 2 / 4 | Deliver the narrow confirmed failure fix, plus durable intent/idempotency protection and ambiguous-payment reconciliation where missing; depends on 3 and provider capability | Payments engineering for payments; identity engineering for KYC; application/mobile owner must be assigned if implicated | Timeout-after-acceptance, lost acknowledgment, duplicate/out-of-order callback, process restart and ledger-only completion scenarios pass; one logical payment creates at most one transfer and one funding count; KYC retry creates one completion | Disable automatic retries/affected feature; keep ambiguous intents queued and continue ledger reconciliation; replay events safely | Engineering confirms provider guarantees and estimates; operations accepts queue. If no fault is established, deliver integrity/reconciliation only and continue diagnosis; do not invent a conversion fix |
| Sprint 2 / 5 | Validate complete business path and publish reconciled recovery report; depends on 2 and completed 4 | Growth product, with data/finance/risk and operations sign-off | Approved test path proceeds KYC → application → unchanged decision → acceptance → qualifying ledger entry → exactly one dashboard first-funded person. Pending/failed paths count zero; backfill and second reconciliation produce no unexplained changes | Revert dashboard publication or feature exposure; retain new financial safeguards and investigate exceptions; preserve audit trail | Human release authority approves any rollout separately. Require source tie-out, no unresolved duplicate-payment exposure, agreed guardrails and a monitored window. Correct endpoint responses alone do not pass |

Sprint 1 exit: a reconciled baseline, explicit remaining discrepancies, a ranked failure hypothesis and a scoped Sprint 2 estimate. Sprint 2 exit: completed integrity work and any evidence-supported fix, business-path validation and an honest recovery report. A numerical uplift or mature economic outcome is not guaranteed within these sprints.

## Acceptance and later optimization

Before a proposed live rollout, use synthetic controlled cases for all failure modes above, prove safe replay/backfill, and demonstrate that technical recovery preserves existing risk/KYC policy. Any subsequent approved observation must tie ledger outcomes to the same cohort definitions and compare comparable windows, separating pending from mature outcomes. Data and finance should explain every material reconciliation difference against agreed tolerances; no tolerance has been supplied, so none is silently assumed.

Do not interpret a before/after repair as a randomized experiment. If reliable instrumentation, operational stability, capacity and a credible optimization hypothesis later exist, a small persisted assignment table can precede a full assignment service. It must have a stable randomization unit, immutable control/treatment assignment before exposure, exposure logging, policy-consistent eligibility, intent-to-treat analysis, contamination checks, guardrail stop rules, and a power calculation using corrected baseline/variance. Growth product proposes it; data validates design; risk and the applicable human authority approve it. Without those prerequisites, defer the experiment beyond this plan. Never randomize payment correctness or relax underwriting as a treatment.

## Open decisions to close

1. **Growth product + risk:** jurisdiction, product eligibility, journey entry population, conversion window and permitted scope; obtain qualified local review before making local legal conclusions or changing consent-related flows.
2. **Data + finance:** qualifying ledger completion/correction semantics, historical coverage, stable person linkage, time zone, late-arrival watermark and publication tolerance. Determine whether past 202-based reports need restatement.
3. **Identity + payments:** which provider's timeout share is reported, its denominator, status lookup/idempotency guarantees, callback authentication, retry caps and pending SLAs. Confirm existing protections before building replacements.
4. **Growth product + service owners:** release version/timing, rollback mechanism, registration/application/mobile ownership, named owners, sprint length, capacity and estimates. Do not allocate unowned work as a commitment.
5. **Risk + finance + operations:** risk-mix reconciliation, loss/fraud maturity, complaint and consent measures, queue capacity/escalation and quantitative stop rules. Identify the accountable rollout authority.
6. **Growth product + data:** corrected baseline and practical recovery target, attribution reliability, observation duration and whether an experiment is warranted after repair.

The evidence can establish whether reported counts are correct, where people are stuck and whether a specific technical repair restores ledger-confirmed funding. It cannot yet establish causation for the weekly decline, a funded-user uplift magnitude, profitability, long-term credit quality or compliance in an unidentified jurisdiction.
