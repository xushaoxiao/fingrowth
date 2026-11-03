---
name: growth-metric-tree
description: Define a consumer lending metric tree, denominators and risk-adjusted contribution. Use when choosing a north star, reconciling CAC with loss or writing a metric dictionary.
---

# Growth metric tree

Translate the requested business goal into measurable drivers and guardrails. A tree is useful only when its arithmetic, populations and source ownership reconcile.

## Establish the measurement contract

Identify product, jurisdiction, population unit (person, loan or exposure), cohort-entry rule, timezone, observation date, outcome horizon, currency, source and loss basis. Mark missing fields unknown. Never compare currencies or mix loan and borrower denominators without an explicit bridge. Use synthetic or approved anonymous aggregates; do not request customer rows or internal employer materials.

## Build and reconcile

- Start with contribution = recognized revenue − acquisition − credit loss − funding − servicing − incentives. Principal advanced is not revenue. Costs must be mutually exclusive, in the same currency, population and horizon. Recognized revenue means net of reversals according to the stated accounting basis.
- Choose one loss measure for each exposure. Expected and realized loss on the same exposure cannot both be subtracted. Fraud, recoveries and collection costs need an explicit treatment to avoid counting them twice.
- Link first-funded people to acquisition volume and sequential conditional conversion rates only if populations are nested. Treat repeat lending as a separate loan/exposure bridge, not an automatic multiplication of first-loan economics.
- Define funded CAC = acquisition spend / first-funded people. Zero denominator means unknown. Explain paid-only versus blended spend and organic attribution.
- Keep mature observed contribution separate from modeled/immature economics. A `mature: true` label alone does not prove outcome completeness.

Use [the metric dictionary and worked example](references/metric-dictionary.md) for concrete definitions and a reconciliation check.

## Deliver

Provide a metric tree, dictionary (formula, numerator/denominator, population, window, source, owner, maturity and exclusions), reconciled example and unresolved measurement issues. Separate north-star economics from diagnostic conversion rates and risk guardrails. Do not estimate lifetime value, APR, default probability or causal uplift from unsupported aggregate counts.

## Decision boundaries

Do not recommend discriminatory targeting or infer protected traits. No autonomous underwriting, customer contact, pricing changes or deployment. Risk/finance own loss treatment and scale decisions. Local obligations require jurisdiction-specific qualified review; do not claim compliance. Label observation, model and recommendation explicitly.
