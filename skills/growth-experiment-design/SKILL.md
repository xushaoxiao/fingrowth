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
4. Declare baseline, absolute/relative MDE, alpha, power, allocation, statistical method, exclusions and multiplicity plan. For one independent binary ITT outcome, 1:1 allocation and a two-sided fixed-horizon test, use the bundled [power planner](scripts/plan_power.py) after reading [its method and limits](references/power-planning.md). Supply MDE as an **absolute fraction**: `0.03` means three percentage points. For other designs use a separately verified method, or state **unresolved**; do not force them into this calculator. Do not invent a baseline or MDE from conversion counts alone. Estimate duration from eligible assignment traffic and add outcome follow-up; do not substitute total site traffic. Keep delayed-risk review separate from the primary readout.
5. Define complaint, consent, technical failure, fraud and mature credit-loss guardrails. State denominator, horizon, owner, policy-approved numeric threshold and action. Missing thresholds block launch; immature risk outcomes block scale-up. Identify fair-treatment review using authorized methods, without inferring protected traits.
6. Predeclare the analysis horizon and stopping procedure. Fixed-horizon designs do not allow repeated significance peeking; sequential decisions need a specified valid method. State rollback owner, exposure limits and final risk/finance decision gates.

Fill [the experiment card](assets/experiment-card.md) rather than adding generic planning prose. Retain unknowns explicitly; do not make the card appear launch-ready when baseline, power or thresholds are missing.

For example, relative to this skill's location:

```sh
python3 <skill-directory>/scripts/plan_power.py --baseline 0.60 --mde-absolute 0.03 --alpha 0.05 --power 0.80 --eligible-per-day 400 --primary-followup-days 7 --format markdown
```

The command uses only Python 3.10+ standard-library modules. Default output is JSON; invalid inputs exit 2 without a partial report. Its approximate power and timing are planning assumptions, not observed outcomes, guardrail power or approval. Power is evaluated at the assumed MDE against a zero-difference null; it does not prove the true effect exceeds a minimum worthwhile threshold. A decision requiring that claim needs a different reviewed hypothesis/design. Missing approved numeric risk thresholds still block launch even when sample-size calculation succeeds.

## Deliver

Return the experiment card, instrumentation/assignment checks, proposed analysis and status: `draft`, `blocked before launch`, `ready for owner review`, or `awaiting mature outcomes`. “Ready for owner review” is not approval. Separate observations, hypotheses, assumptions and decisions. Do not claim uplift before a valid completed analysis.

## Decision boundaries

No autonomous underwriting, customer contact, pricing changes, deployment or experiment launch. Never relax underwriting to chase conversion. Human experiment, risk, finance and local compliance owners retain approval authority. Local obligations require jurisdiction-specific qualified review; do not claim regulatory compliance.
