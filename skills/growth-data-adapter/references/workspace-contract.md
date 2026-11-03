# FinGrowth dashboard workspace contract 1.0

The dashboard consumes a JSON workspace. It does not connect to databases or execute source queries. Adapters convert **authorized aggregate cohorts**, not customer rows or independent event totals, into the exact shape below. Schema validation cannot prove privacy, authorization, event completeness or actual outcome maturity.

## Workspace shape

All top-level fields are required; extra fields are rejected:

Capacity limits shared with the browser: each string is at most 10,000 UTF-16 code units (JavaScript string length); at most 200 cohorts; at most 1,000 mappings, experiments or initiatives, and at most 1,000 guardrail strings per experiment. These limits bound a lightweight review workspace rather than a raw data store. Required text, including the description, remains nonempty.

The complete serialized workspace must also fit within **2,000,000 UTF-8 bytes**. The mapper validates the exact CLI serialization: `json.dumps(workspace, ensure_ascii=False, indent=2, allow_nan=False) + "\n"`, encoded as UTF-8. Individually valid strings or arrays can still exceed this whole-document limit. Unpaired Unicode surrogates are rejected because they are not valid UTF-8 output. Validation runs before writing or replacing the output file.

```text
{
  schema_version: "1.0",
  name: nonempty string,
  description: nonempty string,
  data_mode: "synthetic" | "approved_aggregate",
  provenance: {
    source: nonempty string,
    extracted_at: ISO date-time with explicit Z or UTC offset,
    timezone: nonempty declared timezone string,
    cohort_definition: nonempty string,
    approval_reference: nonempty string | null,
    mappings: [{target: string, source: string, transform: string}]
  },
  cohorts: [canonical cohort, ...],
  experiments: [{id, title, status, owner, primary_metric, hypothesis, guardrails: [string, ...], next_action}],
  initiatives: [{id, title, owner, status, acceptance, dependency}]
}
```

Experiment/initiative scalar fields are nonempty strings. Both arrays may be empty. IDs must be unique within their array. Guardrails is an array of nonempty strings and may be empty if evidence is not yet supplied. Planning statuses are display text, never approval or evidence of implementation. The demo labels every planning card hypothetical.

`cohorts` is a nonempty array; `(cohort, window)` is unique. `data_mode: synthetic` requires every row's actual `synthetic` flag to be true. `approved_aggregate` requires every flag false and a nonempty approval reference. Mixed modes are rejected. Do not include private credentials or the underlying approval document. A reference is an assertion to be checked by the authorized owner, not a certification.

Each mapping has exactly `target`, `source`, `transform`, all nonempty strings. Target fields must cover exactly every canonical scalar field, with each count addressed as `counts.<stage>`. Targets cannot repeat. The bundled mapper emits `transform: copy without coercion`. A manually produced adapter must document its real transformation; no scripts or expressions in this field are executed.

## Canonical cohort

All fields are required; no additional row or count fields:

| Field | Rule |
| --- | --- |
| cohort | Nonempty cohort label |
| window | Valid ordered inclusive `YYYY-MM-DD/YYYY-MM-DD` acquisition dates |
| outcome_as_of | Valid `YYYY-MM-DD`, no earlier than window end |
| currency | Exactly three uppercase letters; registry and exchange rates are not verified |
| synthetic | Actual boolean, matching the workspace mode |
| mature | Actual boolean supplied by source owner; not independent schedule-based verification |
| counts | Exactly the nine ordered stages below |
| acquisition_cost, revenue, credit_loss, funding_cost, servicing_cost, incentives | Finite JSON numbers, 0..1,000,000,000,000 each, with at most two decimal places |

Stages: `acquired`, `registered`, `kyc`, `applied`, `approved`, `accepted`, `disbursed`, `repaid`, `repeat`. Every count is an integer from 0 to 9,007,199,254,740,991, and no greater than its predecessor. Booleans and numeric strings are not counts. The fixed limits make monetary cents and counts safely representable in the dashboard. They are UI contract limits; the standalone Python analyzer has a separate input contract.

The model is nested unique people with at most one included first loan. KYC means completed/passed; disbursed means first ledger-confirmed funding. Repaid means full contractual repayment of the included first loan by the declared horizon; repeat is a subset of those fully repaid people. Additional repeat-loan exposures are excluded from cohort economics. Products with other legitimate paths must use a separately defined population/model rather than cap or reorder actual counts.

Revenue excludes principal and follows the stated recognition basis. Costs are mutually exclusive and aligned to the same currency, cohort, exposure scope and horizon. Credit loss is one selected measure, never expected plus realized loss on the same exposure. Missing values are unknown, not zero. `mature: true` alone cannot prove final outcomes. The dashboard displays immature contribution as unknown, and rankings are descriptive rather than causal.

## Mapping-profile input

The source file is a nonempty JSON array of aggregate objects. A profile has exactly:

- Required: `name`, `description`, `data_mode`, `provenance` and `field_map`.
- Optional: `experiments` and `initiatives`, defaulting to empty planning arrays.
- `provenance` has the five metadata fields above, without `mappings`; mappings are generated by the CLI.
- `field_map` contains exactly all canonical scalar targets, including the nine `counts.<stage>` keys, with string source object paths as values.

For example: `"counts.disbursed": "populations.first_funded"` copies the supplied value at that object path. Paths select dictionary keys separated by dots; arrays, literal-dot key escaping, constants, fallbacks and expressions are unsupported. Normalize a legitimate upstream shape separately and disclose that transformation. Missing mapped paths and malformed values fail; values are never coerced.

The generated workspace contains no unmapped source fields. This projection does not make unauthorized/customer data acceptable input; source approval and aggregation remain prerequisites. Duplicate JSON keys are rejected rather than silently using the last value.

The complete identity and renamed-field profiles ship in `assets/`. The CLI is deterministic for fixed source/profile files. It writes stdout by default or atomically replaces an explicitly selected output; errors go to stderr, exit status 2, with no partial workspace. It does not run the synthetic-only cohort analyzer or claim that imported actual aggregates are synthetic.

Extraction timestamps must have clock hours 00..23, minutes/seconds 00..59, and offset hours 00..23 and minutes 00..59. The adapter checks these fields before calendar parsing; it rejects normalized inputs such as `+01:60` instead of silently changing the source's timestamp.
