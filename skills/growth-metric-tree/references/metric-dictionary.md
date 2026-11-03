# Metric dictionary and reconciliation

| Metric | Formula / denominator | Population and time | Proposed source / owner | Limitation |
| --- | --- | --- | --- | --- |
| First-funded people | Deduplicated people with first ledger-confirmed disbursement | Acquisition cohort; stated funding horizon | Disbursement ledger / data + payments | A successful request is not funded money |
| Step conversion | People reaching next step / people at prior step | Same nested cohort and observation date | Journey events / product analytics | Pending events are not confirmed abandonment |
| Funded CAC | Cohort-attributed acquisition spend / first-funded people | Same currency and attribution policy | Ad-spend ledger + attribution / growth finance | Unknown at zero funded people; no LTV implied |
| Contribution | Recognized revenue − acquisition − credit loss − funding − servicing − incentives | Same cohort, currency and horizon | Reconciled finance totals / finance | Immature observed contribution must remain unknown |
| Full repayment share | Fully repaid first-loan people / funded first-loan people | Stated repayment horizon | Repayment ledger / servicing | Its complement is not automatically default rate |
| Repeat share | Eligible repeat borrowers / stated eligible prior borrowers | Fixed eligibility and repeat window | Loan ledger / retention | Repaid population and all funded people give different metrics |

Each deployed definition also needs timezone, refresh lag, maturity evidence, exclusions, named owner and version. The standalone analyzer uses a simplified nested first-loan person model; it does not implement a full loan-level accounting system.

## Synthetic example

```text
First-funded people
  = 10,000 × 60% × 80% × 75% × 50% × (1,500/1,800) × (1,400/1,500)
  = 1,400
Funded CAC = 14,000 / 1,400 = USD 10
Contribution = 42,000 − 14,000 − 14,000 − 5,000 − 3,000 − 2,000
             = USD 4,000
```

A second synthetic cohort has the same 1,400 funded people and USD 42,000 revenue, USD 10,000 acquisition and USD 23,000 credit loss, with the other costs unchanged. CAC is about USD 7.14, but contribution is USD −1,000. Lower CAC alone does not justify scaling. These aggregates do not establish why loss differs, or how a new channel would perform under randomization.
