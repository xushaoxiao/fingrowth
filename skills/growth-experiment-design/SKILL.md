---
name: growth-experiment-design
description: Turn a consumer lending growth hypothesis into a testable experiment with assignment rules, metric denominators, power requirements and delayed-risk decision gates. Use for experiment design or launch-readiness review.
---

# Growth experiment design

Produce an executable experiment specification and identify the decisions still needed before launch. An immediate conversion increase does not establish risk-adjusted value.

## Establish the decision

Use supplied business question, product, geography, target population, baseline, outcome horizon and authorized scope. Mark missing inputs unknown. Use synthetic or approved anonymous aggregates only. Do not request PII, credentials, employer documents or customer exports.

## Specify the experiment

1. Write a falsifiable hypothesis and distinguish the proposed intervention from underwriting, pricing and eligibility policies that remain under their owners' control.
2. Define eligible population, randomization unit, persistent assignment, allocation and contamination controls. For repeated devices/sessions, prevent reassignment of the same unit. State the treatment/control and rollback behavior.
3. Define one primary outcome with numerator, denominator, measurement horizon and intention-to-treat population. Do not condition primary analysis on post-treatment completion or approval. Add mature contribution per assigned eligible unit if the decision concerns economics.
4. Declare baseline, absolute/relative MDE, alpha, power, allocation, statistical method, exclusions and multiplicity plan. Calculate sample size with an appropriate verified method, or state **unresolved**. This skill does not include a power calculator. Do not invent a sample size from conversion counts alone. Estimate duration from eligible assignment traffic and add outcome follow-up; do not substitute total site traffic.
5. Define complaint, consent, technical failure, fraud and mature credit-loss guardrails. State denominator, horizon, owner, policy-approved numeric threshold and action. Missing thresholds block launch; immature risk outcomes block scale-up. Identify fair-treatment review using authorized methods, without inferring protected traits.
6. Predeclare the analysis horizon and stopping procedure. Fixed-horizon designs do not allow repeated significance peeking; sequential decisions need a specified valid method. State rollback owner, exposure limits and final risk/finance decision gates.

Fill [the experiment card](assets/experiment-card.md) rather than adding generic planning prose. Retain unknowns explicitly; do not make the card appear launch-ready when baseline, power or thresholds are missing.

## Deliver

Return the experiment card, instrumentation/assignment checks, proposed analysis and status: `draft`, `blocked before launch`, `ready for owner review`, or `awaiting mature outcomes`. “Ready for owner review” is not approval. Separate observations, hypotheses, assumptions and decisions. Do not claim uplift before a valid completed analysis.

## Decision boundaries

No autonomous underwriting, customer contact, pricing changes, deployment or experiment launch. Never relax underwriting to chase conversion. Human experiment, risk, finance and local compliance owners retain approval authority. Local obligations require jurisdiction-specific qualified review; do not claim regulatory compliance.
