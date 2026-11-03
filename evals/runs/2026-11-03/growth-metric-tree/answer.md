# Consumer lending metric contract and reconciliation

All data are synthetic. Request A uses `cohorts.json` as its only numeric source. Request B uses only the figures in TASK.md and is a separate population. Dollar figures below are USD; percentages and per-person figures are rounded for display, with exact fractions used in reconciliation.

## A. Two acquisition cohorts

### Measurement contract and status

Both records specify cohort window January 1–31, 2026, outcomes as of October 31, 2026, USD, and `mature: true`. The entry event for that window, timezone, product, jurisdiction, outcome horizon, refresh lag, and accounting policies are unknown. The cohort label does not establish a paid-only or blended attribution policy, nor prove that the cohorts are disjoint.

For this reconciliation only, interpret each funnel count as unique people in the same acquisition cohort, each successive stage as a subset of the preceding stage, and `disbursed` as people with their first ledger-confirmed funding. These are assumptions requiring validation, not facts established by aggregate counts. If `disbursed` instead counts loans or includes existing borrowers, first-funded people and funded CAC cannot be identified from this file.

Interpret `revenue` provisionally as recognized revenue net of reversals and treat each cost bucket as mutually exclusive and aligned to that cohort, currency, exposure scope and outcome window. Whether those monetary totals cover only first loans or also repeat loans is unresolved. Treat `credit_loss` as one supplied loss measure with its basis unknown. Thus the contribution amounts below are arithmetic reconciliations under this contract; they are not certified mature observed economics. A Boolean maturity label is insufficient evidence that all exposures and costs are complete.

### Metric tree

```text
North-star economics: cohort risk-adjusted contribution
  = recognized revenue
    − acquisition spend
    − a single non-overlapping credit-loss measure per exposure
    − funding cost − servicing cost − incentives

Acquisition and conversion diagnostics:
  acquired people × registration/acquired × KYC/registration
  × application/KYC × approval/application × acceptance/approval
  × first-funded/acceptance = first-funded people
  acquisition spend / first-funded people = funded CAC

Exposure bridge for economic reconciliation:
  first-funded people → first-loan exposures
  plus explicitly identified repeat-loan exposures → total exposure set
  → recognized revenue and aligned costs for that set

Risk and retention guardrails:
  full-repayment share at a defined horizon
  default incidence at a defined default rule and eligible horizon
  credit-loss dollars and loss rate on explicitly defined exposure
  repeat-borrower share among a defined eligible population and window
```

Principal advanced is an exposure measure, not revenue. Repeat borrowers are a separate bridge: a count of repeat people does not establish the number, balances or economics of repeat loans. Do not multiply first-loan economics by the repeat count or a presumed lifetime multiplier.

### Funnel reconciliation

| Stage | Baseline people | Conditional conversion | Cheap-channel people | Conditional conversion |
| --- | ---: | ---: | ---: | ---: |
| Acquired | 10,000 | — | 12,000 | — |
| Registered | 6,000 | 60.00% | 6,500 | 54.17% |
| KYC | 4,800 | 80.00% | 4,600 | 70.77% |
| Applied | 3,600 | 75.00% | 3,500 | 76.09% |
| Approved | 1,800 | 50.00% | 1,800 | 51.43% |
| Accepted | 1,500 | 83.33% | 1,500 | 83.33% |
| First funded, conditional on contract | 1,400 | 93.33% | 1,400 | 93.33% |

Each conditional rate divides the row by the preceding row. Exact telescoping products reconcile:

- Baseline: 10,000 × (6,000/10,000) × (4,800/6,000) × (3,600/4,800) × (1,800/3,600) × (1,500/1,800) × (1,400/1,500) = **1,400 people**.
- Cheap-channel: 12,000 × (6,500/12,000) × (4,600/6,500) × (3,500/4,600) × (1,800/3,500) × (1,500/1,800) × (1,400/1,500) = **1,400 people**.

Acquired-to-funded conversion is 14.00% versus 11.67%. Count ordering alone cannot prove that the underlying people are nested. Pending journeys are not automatically abandonment.

### Economic reconciliation

| USD unless stated | Baseline | Cheap-channel |
| --- | ---: | ---: |
| Recognized revenue, provisional interpretation | 42,000 | 42,000 |
| Acquisition spend | 14,000 | 10,000 |
| Credit loss, basis unconfirmed | 14,000 | 23,000 |
| Funding | 5,000 | 5,000 |
| Servicing | 3,000 | 3,000 |
| Incentives | 2,000 | 2,000 |
| Total listed costs | 38,000 | 43,000 |
| Reconciled contribution | **4,000** | **−1,000** |
| First-funded people, assumed | 1,400 | 1,400 |
| Funded CAC, USD/person | **10.00** | **7.14** |
| Contribution per first-funded person, USD/person | 2.86 | −0.71 |

Baseline: 42,000 − 14,000 − 14,000 − 5,000 − 3,000 − 2,000 = **4,000**.

Cheap-channel: 42,000 − 10,000 − 23,000 − 5,000 − 3,000 − 2,000 = **−1,000**.

The cheap cohort saves 4,000 in acquisition but has 9,000 more supplied credit loss. With all other supplied totals unchanged, contribution falls by 5,000. Its CAC is 28.57% lower, but that does not make it the economic winner. Subject to aligned accounting and maturity, baseline has the stronger observed arithmetic. These aggregates do not show that channel choice caused higher loss or predict marginal performance at greater scale.

### Repayment, default and repeat lending

If `repaid` means unique first-loan people who fully repaid by the observation date, full-repayment share is 1,300/1,400 = **92.86%** for baseline and 1,100/1,400 = **78.57%** for cheap-channel. The complements are **7.14%** and **21.43%**, respectively, representing 100 and 300 people not classified as fully repaid at that snapshot.

**Reject the proposal to call these complements default rates.** A person can be current, partially repaid, not yet due, delinquent but below the default threshold, restructured, or unresolved. Fully repaid people might also have defaulted earlier and then recovered. Default requires its own event rule, due-date/aging information, cure policy and eligible observation horizon. Neither probability of default nor a valid exposure loss rate follows from these counts. Credit-loss dollars divided by people would have units of dollars/person, not a default percentage.

A provisional descriptive repeat share among all funded people is 400/1,400 = **28.57%** versus 350/1,400 = **25.00%**, if `repeat` counts unique members of those funded cohorts reaching a subsequent disbursement in the same specified window. A different, hypothetical denominator of repaid people produces 30.77% versus 31.82%, but those are not valid repaid-to-repeat conversion rates unless the repeat people are proven to be a subset of the relevant repaid, eligible people. The denominator can reverse a ranking; establish eligibility and time at risk before comparing retention.

### Useful metric dictionary

The shared contract for every row must store product, jurisdiction, currency, timezone, cohort-entry event and dates, observation date, event/outcome window, refresh lag, exposure scope, definition version and named accountable owner. Unknown fields remain unknown. Proposed source systems and owner roles below are contracts to implement, not sources inspected in this exercise.

| Metric | Formula; numerator / denominator | Population and window | Proposed source / owner | Maturity and exclusions |
| --- | --- | --- | --- | --- |
| First-funded people | Count distinct people with first successful ledger disbursement; denominator none | Members of acquisition-entry cohort first funded within defined conversion window | Person identity + disbursement ledger / Data and Payments | Confirm deduplication and first-ever funding; exclude failed, reversed and repeat disbursements under explicit reversal policy; incomplete conversion window is provisional |
| Step conversion | Distinct people reaching next stage / same people eligible at prior stage | Nested acquisition cohort, same cutoff and transition horizon | Journey events reconciled to ledger / Product Analytics | Define KYC pass and other success events; exclude duplicate events; unresolved cases stay pending; zero denominator gives unknown |
| Funded CAC | Attributed acquisition spend / first-funded people | Same acquisition cohort, conversion window, currency and attribution scope | Spend ledger + attribution + funded people / Growth Finance | Specify paid-only versus blended, organic treatment and allocation; acquisition incentives must not appear twice; zero denominator gives unknown |
| Recognized revenue | Sum recognized revenue net of reversals; denominator none | Explicit first/repeat exposure set, recognition window and cutoff | Finance subledger / Finance | Exclude principal advanced; define fees, interest, waivers, reversals and accrual basis; reconcile pending adjustments |
| Credit loss | Sum one selected loss measure per exposure; denominator none | Same exposure set and economic horizon | Risk loss model or write-off/recovery ledger / Risk and Finance | Record expected versus realized basis, gross/net recoveries, fraud and cutoffs; never subtract overlapping expected and realized amounts |
| Funding / servicing / incentives | Sum each mutually exclusive allocated cost bucket; denominator none | Same cohort and exposure set over stated horizon | Treasury, servicing and incentive ledgers / Treasury and Finance | Document allocation, accrual and collection-cost treatment; exclude costs already in acquisition or loss; missing costs are unknown, not zero |
| Contribution | Revenue − acquisition − credit loss − funding − servicing − incentives; denominator none | Aligned cohort, currency, exposure scope and economic horizon | Reconciled preceding sources / Finance | Label modeled or immature as such; mature observed requires completed outcomes and reconciled late costs/recoveries; report excluded overhead explicitly |
| Contribution per first-funded person | Aligned cohort contribution / first-funded people | Same cohort; specify if numerator includes repeat exposure economics | Finance reconciliation + funded people / Finance | Not pure first-loan margin when repeats are included; inherits numerator maturity and zero-denominator rule |
| Full-repayment share | Distinct first-loan people fully repaid / first-funded people | Same first-loan cohort, defined repayment horizon | Loan and repayment ledgers / Servicing | Requires full-repayment rule, reversals and enough follow-up; complement is not default |
| Default incidence | Distinct eligible people meeting default rule within horizon / eligible first-funded people with that horizon observed | Defined borrower cohort and complete follow-up; loan incidence must use loan denominator instead | Due schedules, aging and default records / Risk | Specify threshold, cure, restructuring and observation method; censored cases cannot silently be treated as nondefaults; unavailable here |
| Credit-loss rate | Selected loss dollars / specified original principal or exposure measure | Same exposure set, currency and horizon | Risk ledger/model + principal ledger / Risk and Finance | Name denominator and loss basis; default incidence is a different metric; principal denominator unavailable here |
| Repeat-borrower share | Distinct eligible cohort people with subsequent funding / defined eligible prior people | Fixed eligibility anchor and repeat window | Loan ledger + eligibility history / Retention Analytics | Specify all funded versus repaid/eligible denominator; track censoring; no loan-count or lifetime-value inference |

### Decisions and missing evidence

- **Finance:** confirm that revenue is recognized and net of reversals; define first versus repeat scope; reconcile ledger totals, mutually exclusive cost allocation, loss basis, fraud, recoveries and collection costs. The two contribution totals are usable planning reconciliations pending those checks.
- **Growth Finance and Data:** fix cohort entry, identity, attribution window and model, paid/blended scope, organic allocation and channel overlap. Validate nested funnel membership and first-funded status.
- **Risk and Servicing:** establish default and full-repayment rules, contractual due dates, extensions, outstanding balances, recovery/write-off status, eligibility and full follow-up. Confirm economic closure or disclose residual estimates. An October snapshot of January entrants alone does not prove maturity.
- **Recommendation:** do not scale the cheap channel on CAC alone. Use aligned risk-adjusted contribution as the economic decision metric, conversion as diagnosis, and default/loss outcomes as guardrails. Finance and Risk should own the scale decision after comparability and maturity are established. An appropriately designed test would be needed to support a causal channel claim. No underwriting, pricing or deployment action is authorized or implied.

## B. Product proposal with repeat loans and overlapping losses

### Usable contract

Use **people** for funded CAC and **loans/exposures** for revenue, loss and cost reconciliation. Supplied figures are 1,000 first-funded people, 1,300 loans including repeats, USD 30,000 recognized revenue, USD 5,000 acquisition spend, USD 7,000 expected credit loss and USD 4,000 realized loss on the same exposures. Some loans are not due. Product, jurisdiction, cohort-entry rule/dates, observation date, timezone, term, loss horizon, refresh lag and attribution policy are unknown.

Require a mapping from those 1,000 people to the 1,300 unique funded loans and their exposure records. If each first-funded person has exactly one included first loan and every included loan belongs to this population, the bridge is **1,000 first loans + 300 repeat loans = 1,300 loans**, or 1.30 loans/person. These conditions need confirmation. This does not imply 300 repeat borrowers: a person may have multiple repeat loans. If the loans include other borrower cohorts, the proposed numerator/denominator alignment fails.

The dictionary above applies with this separate cohort and exposure set. Version the contract before use and add due dates, status and loss measure per exposure; revenue net-of-reversal policy; cost allocations; attribution; and the chosen reporting basis. Finance owns recognition and contribution, Growth Finance owns CAC attribution, Data owns identity/cohort joins, and Risk owns loss definition and maturity evidence.

### Supported calculations and labels

| Calculation | Result | Valid interpretation / condition |
| --- | ---: | --- |
| 5,000 / 1,000 | **USD 5.00/person** | Funded CAC if spend is attributable to these same first-funded people under the chosen acquisition policy |
| 5,000 / 1,300 | **USD 3.85/loan** | Acquisition spend allocated per included loan; not borrower CAC |
| 30,000 − 5,000 − 7,000 | **USD 18,000** | Expected-loss-basis partial subtotal before funding, servicing and incentives; requires the expected-loss figure to be the single appropriate loss measure for this exposure set |
| 30,000 − 5,000 − 4,000 | **USD 21,000** | Realized-loss-to-date partial subtotal before funding, servicing and incentives; future losses remain unresolved |

**Do not subtract both USD 7,000 and USD 4,000 as supplied.** They overlap on the same exposures. If expected loss represents a total forecast that already includes realized loss, use the total forecast once. If an additional future-loss estimate is required alongside realized loss, Risk/Finance must supply and reconcile that non-overlapping amount; the supplied USD 7,000 cannot be assumed to be incremental remaining loss. A provision balance, expense flow and cumulative lifetime loss also cannot be interchanged without reconciliation.

Product's proposed expression, (30,000 − 5,000 − 7,000 − 4,000) / 1,300, is arithmetically USD 10.77/loan. It is **not an accepted metric**: it double-counts overlapping losses, omits three cost categories and has a net-economic numerator rather than an acquisition-spend numerator. Dividing it by loans cannot yield borrower CAC.

### What remains unknown and how to finish

With F = funding, S = servicing and I = incentives in USD for the same exposure set and horizon:

- Expected-loss-basis contribution would be **18,000 − F − S − I**, subject to reconciling the USD 7,000 loss basis and horizon.
- Realized-loss-to-date contribution would be **21,000 − F − S − I**, clearly labeled immature and subject to aligned realized accounting.
- A numeric complete contribution and a **mature observed contribution are unknown**. Missing costs must not be set to zero, and realized losses to date do not establish final losses on loans that are not yet due.

To complete the contract, Finance/Treasury/Servicing must supply funding, servicing and incentive totals or agreed allocation rules, including future/accrued costs and exclusions. Risk/Finance must select the loss basis, reconcile the overlapping measures and identify recoveries, fraud, write-offs and collection costs without duplication. Data must confirm the person-to-loan bridge and cohort/attribution alignment. Servicing/Risk must establish contractual maturity, subsequent outcome follow-up and resolution of outstanding/censored exposures; Finance must close reversals and late costs. If a model estimates remaining outcomes, report modeled contribution with its horizon and assumptions instead of calling it mature observed contribution.

No LTV, APR, default probability or causal growth uplift is supported by these aggregates. No external systems or customer data were accessed, and no operational changes were made.
