---
name: growth-data-adapter
description: Adapt authorized aggregate growth exports into a FinGrowth dashboard workspace with explicit field mappings, source provenance and measurement limits. Use when connecting a new data source or importing a cohort workspace.
---

# Growth data adapter

Translate source-specific aggregates into the shared dashboard contract while preserving their meaning. The dashboard is a review surface; a successful import does not establish privacy, maturity, causal uplift or permission to launch.

## Establish the source contract

Use only invented fixtures or aggregates already authorized for this purpose. Identify the source, extraction timestamp, timezone, cohort-entry rule, unique population unit, observation cutoff, currency, loss basis and approved scope. For non-synthetic aggregates, record an approval reference without copying private policy documents. Do not request customer rows, personal identifiers, credentials, production configuration or employer exports without authorization. Connecting a source does not authorize queries or mutations beyond the user's scope.

Read [the workspace contract](references/workspace-contract.md) before mapping. Every canonical cohort value must come from a supplied source field or a separately documented and reviewed upstream aggregation. Missing data remains missing and blocks that cohort's import; never fill absent costs with zero, cap non-nested counts or relabel actual data as synthetic. If the source consists of raw events or loan-level records, provide an aggregation specification and obtain an approved aggregate export instead of feeding rows directly into this adapter.

## Map and validate

1. Build an explicit canonical-target → source-path profile. Distinguish definitions, source names and units; a renamed column is not necessarily the same metric. Reconcile nested unique first-loan people and aligned monetary totals before treating source rows as cohorts.
2. Use the [identity profile](assets/identity-profile.json) for existing FinGrowth fixtures, or [renamed-field profile](assets/renamed-fields-profile.json) for a source with `metadata`, `populations` and `economics` objects. Source paths select object keys only. The bundled mapper copies values without coercion and never runs expressions, SQL or network calls.
3. With Python 3.10+, run the script relative to this skill's location:

```sh
python3 <skill-directory>/scripts/build_workspace.py <aggregate-source.json> --profile <mapping-profile.json> --output <workspace.json>
```

The copied skill includes everything the mapper requires. In a repository checkout, `python3 scripts/build_workspace.py` delegates to the same implementation. Exit 2 means invalid input; explain the gap and obtain corrected evidence rather than changing facts to satisfy the schema. The command writes no partial workspace on validation failure and never overwrites its input/profile path.
4. Use `synthetic` mode only when every cohort truthfully has `synthetic: true`. Use `approved_aggregate` only when every cohort has `synthetic: false` and an approval reference is supplied. This declaration is provenance, not an automated privacy review. The original synthetic-only funnel calculator remains separate; the adapter does not bypass it.
5. Preserve source-to-target mappings and interpretation limits in provenance. Planning cards may be empty. If adding hypothetical examples, label them hypothetical; status strings do not confer approval. Validate the whole workspace before importing it into the dashboard.

## Deliver

Provide the workspace JSON, mapping profile, a concise source/definition reconciliation, uncovered fields and the next action for each blocker. Report whether the bundled mapper actually ran and its result. Explain any upstream transformations separately; the mapper's `copy without coercion` record must not conceal prior unit conversion or aggregation. Keep real approval evidence and sensitive source material outside the public repository.

No customer contact, autonomous underwriting, source mutation, pricing change, experiment launch or deployment is authorized by this skill. Human data, risk, finance and relevant local owners retain their decision authority.
