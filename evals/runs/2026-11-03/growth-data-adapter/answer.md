# Synthetic partner export adaptation

The bundled mapper ran successfully (exit **0**) and produced `workspace.json` with two synthetic cohorts, all 21 canonical scalar mappings, and empty experiments and initiatives. `profile.json` is reusable for exports with the same field paths and meanings; update provenance for each extraction.

## Lineage and definitions

- Source: **Synthetic partner export**, provided as `source.json`; extracted **2026-11-03T00:00:00Z**, timezone **UTC**, currency **USD**. All numbers are invented aggregate data; no live systems or customer records were used.
- Acquisition dates: **2026-01-01 through 2026-01-31**, inclusive. Observation cutoff: **2026-10-31**. The cohorts are `baseline` and `cheap-channel`.
- `segment → cohort`, `entry_dates → window`, `observed_on → outcome_as_of`, `money_unit → currency`, `invented → synthetic`, and `outcomes_closed → mature`. Each `people.<stage>` maps to `counts.<stage>`; each of the six `totals.<amount>` fields maps to its canonical amount field. The complete explicit mapping is in `profile.json` and generated workspace provenance.
- Counts represent nested unique first-loan people. Contract definitions require KYC completed/passed, disbursed as first ledger-confirmed funding, repaid as full contractual first-loan repayment by the cutoff, and repeat as a subset of repaid people. The task establishes the nested population and repayment-before-repeat model; it supplies no independent event-level evidence for those stage semantics.
- Repeat-loan economics are excluded. Maturity is copied from supplied boolean metadata; no schedules were supplied for independent verification. Source values and types were copied unchanged: no aggregation, unit conversion, coercion, capping or imputation occurred.

## Assumptions and blockers

The complete source has no missing mapped fields and passes the dashboard contract. Schema validation does not establish final maturity, causal uplift or readiness for a business decision. The source does not specify revenue recognition/exclusion of principal, the chosen credit-loss measure (expected or realized), or evidence that cost categories are mutually exclusive and aligned to the declared first-loan horizon. These remain economic-interpretation gaps, not a claim that the mapper verified them. The source/finance owner should document and reconcile these definitions before interpreting contribution or comparing economic performance. A data owner should confirm exact stage semantics and maturity from the declared model and schedules before relying on final outcomes.

`incomplete-source.json` was attempted using the same mapping and failed with exit **2**:

```text
Invalid workspace input: source[0]: a mapped source field is missing
```

The missing field is `totals.servicing_cost` for `baseline`. No partial `incomplete-workspace.json` was created. The original stderr and status are preserved in `incomplete.stderr.txt` and `incomplete.exit-status.txt` (stdout is empty and preserved separately).

Reject the suggestion to replace the missing servicing cost with zero: absent means unknown; zero would assert a known absence of cost and overstate contribution by the unknown amount. The complete source contains baseline servicing cost of USD 3,000, but a separate file is not a justified fallback without confirmation that the extracts are equivalent. Obtain a corrected aggregate or explicit source-owner evidence of the actual value, then rerun the unchanged mapping. Neither source file was modified.

Only local artifacts were created. No dashboard import, external access, publication, experiment launch or deployment was performed.
