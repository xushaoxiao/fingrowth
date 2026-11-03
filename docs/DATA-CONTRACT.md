# Dashboard data contract

FinGrowth's lightweight dashboard reads workspace JSON, allowing different aggregate data sources to use the same growth-engineering views. The canonical, standalone specification lives in [the data-adapter skill contract](../skills/growth-data-adapter/references/workspace-contract.md).

The contract carries cohort definitions, source provenance, explicit field mappings, truthful synthetic/approved-aggregate status, planning experiments and delivery initiatives. A new source needs a reviewed mapping, not source-specific UI logic. The mapper accepts aggregate JSON exports and performs no database query, remote request or code execution. Source retrieval, authorization and upstream aggregation remain separate responsibilities.

## Run the synthetic adapter

From the repository root:

```sh
python3 scripts/build_workspace.py examples/lending/cohorts.json \
  --profile skills/growth-data-adapter/assets/identity-profile.json \
  --output examples/dashboard/workspace.json
```

The checked-in workspace is fully invented. Its extraction timestamp is fixed synthetic fixture metadata; its three experiment and three initiative cards are hypothetical plans, not running experiments or completed work.

For another source, begin with [the renamed-field profile](../skills/growth-data-adapter/assets/renamed-fields-profile.json), reconcile the source meanings and replace its metadata with accurate evidence. The CLI maps canonical target fields to dotted source-object paths and copies values without coercion. Missing economics never becomes zero, non-nested populations are rejected, and dates/maturity/types are validated. Currency syntax is checked without FX conversion. Cohort amounts are limited to 1e12 with at most two decimals; counts must be JavaScript-safe integers.

Actual approved anonymous aggregates require `data_mode: approved_aggregate`, every row's truthful `synthetic: false`, and an approval reference. This is a declared authorization boundary, not a privacy or compliance scanner. It does not bypass or relabel input for the separate synthetic-only funnel calculator. Keep sensitive source exports and approval documents outside the public repository.

The mapper is bundled inside `growth-data-adapter`; the root entrypoint delegates to it. Copying the entire skill folder preserves this capability. See [SKILL.md](../skills/growth-data-adapter/SKILL.md) for the adaptation workflow and decision boundaries.

To match the browser's lightweight workspace capacity, strings are limited to 10,000 characters, cohorts to 200, and mappings, experiments, initiatives and per-experiment guardrails to 1,000 entries. Required text remains nonempty. Invalid timestamp clock values or UTC offsets are rejected rather than normalized into an extraction claim.

The complete generated JSON must fit within 2,000,000 UTF-8 bytes, including two-space indentation and its trailing newline. The mapper uses one serialization helper for validation and emission (`ensure_ascii=False`, `indent=2`, `allow_nan=False`), so non-ASCII data is counted by its actual UTF-8 bytes. Payloads made from individually valid but collectively oversized cards fail before output replacement. UTC offset minutes such as `+01:60` are explicitly rejected.
