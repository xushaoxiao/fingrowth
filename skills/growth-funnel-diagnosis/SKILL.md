---
name: growth-funnel-diagnosis
description: Calculate and diagnose consumer lending cohort funnels, distinguish technical friction from policy outcomes, and produce evidence-backed investigation priorities. Use for conversion drops or channel-quality questions.
---

# Growth funnel diagnosis

Locate an investigation priority without turning a descriptive funnel into a causal claim.

## Validate the question and data

Establish cohort entry, unit, dates, timezone, geography, product, currency, outcome maturity, source and authorized scope. Use supplied context and mark unknowns; ask only for information that blocks the requested conclusion. Use synthetic or approved anonymous aggregates; never request PII, credentials or internal employer exports.

For deterministic calculations on **synthetic** nested cohorts, read [the input contract](references/input-contract.md), then run the bundled script with Python 3.10+:

```sh
python3 <skill-directory>/scripts/analyze.py <cohorts.json>
python3 <skill-directory>/scripts/analyze.py <cohorts.json> --format markdown
```

Resolve `<skill-directory>` from this file's location, not the current working directory. The script ships with this skill and requires no repository checkout or third-party dependencies. It writes stdout only. A nonzero exit means invalid input: explain the contract failure and correct it before using results. Never relabel real data as synthetic to bypass the restriction. For approved non-synthetic aggregates, use another authorized calculation method and disclose that the bundled tool was not used. If execution is unavailable, disclose that and do not claim a verified report.

## Interpret the funnel

1. Confirm nested unique-person counts and ordered windows. If data are event counts, independent monthly totals or overlapping loan populations, stop sequential-rate calculation and specify the aggregation fix.
2. Show numerator, denominator, conversion and people not progressing for each transition. Rank acquisition-to-funding transitions by both count not progressing and observed conversion. Retain ties; neither ranking establishes an actionable bottleneck by itself.
3. Separate technical failure, user abandonment, pending work and policy rejection. Approval is a risk decision; repayment/repeat are delayed outcomes. Do not label them UX failures or recommend relaxing underwriting.
4. Compare channels only with aligned windows, currency, attribution, risk mix and maturity. Lower funded CAC can coexist with worse contribution. Do not aggregate incompatible cohorts or infer loss severity from unrepaid counts.
5. For each leading hypothesis, propose a disconfirming check, needed aggregate evidence and owner. Suggest an experiment only after instrumentation and safety prerequisites are clear.

Before finalizing priority prose, check each named leader against its own calculated ranking. For bundled output, use `investigation_candidates.by_not_progressed` for count leaders and `investigation_candidates.by_lowest_conversion` for rate leaders, including all ties. An empty list has no observed leader. Do not carry the count leader into the rate conclusion: different transitions can lead the two rankings even within one cohort. Reconcile the narrative, table and JSON values before delivery.

## Deliver

Return scope/quality gaps, the calculation table, investigation candidates under both rankings, an evidence/hypothesis table, proposed next actions and limits. The bundled Markdown report is the arithmetic baseline; enrich it with actual supplied evidence, not invented root causes. Label unknown denominators and immature contribution as unknown, not zero.

## Decision boundaries

No protected-trait inference, discriminatory targeting, autonomous underwriting, customer contact, pricing changes or deployment. Human risk/finance owners decide scale. Local obligations depend on jurisdiction and qualified review. Do not claim compliance, real uplift or causation from a synthetic fixture.
