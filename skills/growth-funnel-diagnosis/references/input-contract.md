# Synthetic aggregate input contract

The file is a nonempty JSON array. Each row contains exactly these fields:

| Field | Type / rule | Meaning |
| --- | --- | --- |
| cohort | Nonempty string | Synthetic cohort label; unique with window |
| window | YYYY-MM-DD/YYYY-MM-DD | Inclusive acquisition entry dates; ordered |
| outcome_as_of | YYYY-MM-DD | Observation date no earlier than window end |
| currency | Three uppercase letters | Single declared currency; syntax checked, currency registry not verified |
| synthetic | true | Explicitly invented fixture; not a privacy or anonymity test |
| mature | Boolean | Supplied outcome-maturity assertion, not independently established |
| counts | Object with exactly the nine stages below | Nested unique people, not raw events |
| revenue | Finite nonnegative JSON number | Recognized cohort revenue, excluding principal |
| acquisition_cost, credit_loss, funding_cost, servicing_cost, incentives | Finite nonnegative JSON numbers | Mutually exclusive totals, same cohort/currency/horizon |

Stages in order: `acquired`, `registered`, `kyc`, `applied`, `approved`, `accepted`, `disbursed`, `repaid`, `repeat`. Each is a nonnegative integer no greater than its predecessor. `kyc` means completed/passed KYC in this simplified model. `repaid` means full contractual repayment of the first loan within the declared horizon; `repeat` is a subset of those people. Additional repeat-loan exposures are excluded from the economics. This nesting is a model assumption, not a universal lending journey.

Example file contents:

```json
[
  {
    "cohort": "synthetic-baseline",
    "window": "2026-01-01/2026-01-31",
    "outcome_as_of": "2026-10-31",
    "currency": "USD",
    "synthetic": true,
    "mature": true,
    "counts": {
      "acquired": 10000, "registered": 6000, "kyc": 4800,
      "applied": 3600, "approved": 1800, "accepted": 1500,
      "disbursed": 1400, "repaid": 1300, "repeat": 400
    },
    "acquisition_cost": 14000, "revenue": 42000, "credit_loss": 14000,
    "funding_cost": 5000, "servicing_cost": 3000, "incentives": 2000
  }
]
```

Step conversion = next / previous; zero denominator gives JSON `null` / report `unknown`. Funded CAC = acquisition cost / disbursed. Contribution = revenue − acquisition − credit loss − funding − servicing − incentives; immature contribution is null. Credit loss is one measure, never expected plus realized loss on the same exposure. Arithmetic is descriptive; not an accounting engine or lifetime-value estimator.

## Output and compatibility

Default output remains a JSON array with the original `cohort`, `currency`, `mature`, `rates`, `funded_cac`, `contribution` and `explanation` fields. Added fields: window, observation date, step counts, investigation rankings and interpretation warnings. Ranking lists cover acquired → disbursed only, stable in journey order for ties. No benchmark or causal bottleneck score is fabricated. Cohorts are reported independently; the tool never sums currencies or selects a winning channel.

Missing/extra fields, duplicate JSON keys, duplicate cohort/window pairs, invalid dates, invalid monetary values, non-boolean maturity and non-nested counts are errors. All rows validate before any report is printed. Exit status is 0 on success and 2 for invalid input or command arguments; errors go to stderr. An input document cannot establish privacy, outcome maturity, event completeness or fair-treatment suitability by declaration alone.
