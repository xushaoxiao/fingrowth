# FinGrowth binary experiment power plan

Planning estimate only. Launch readiness is not assessed; risk thresholds and approvals are unknown.

Design: independent assigned eligible people, 1:1 allocation, two-sided, fixed horizon, one binary ITT primary metric.

Baseline: 0.6; absolute MDE: 0.03 (3 percentage points); treatment at MDE: 0.63.
Alpha: 0.05; target power: 0.8.

Required sample: **4,129 per arm; 8,258 total**.
Approximate power at n: 0.800035179; at n − 1 per arm: 0.799940156.
Smallest expected success/failure cell: 1527.73 (scope gate: ≥ 10).

## Timing assumptions

Eligible assignments/day across both arms: 400.0.
Recruitment days at assumed traffic: 21.
Primary follow-up days after the last assignment: 7.
Earliest primary readout day after start: 28.
Delayed-risk review day: unknown; determine separately from loan schedules and observation maturity.

## Explainable method

Null variance uses the pooled probability; alternative variance uses the two separate probabilities. Integer bisection finds the smallest per-arm sample meeting the target under the two-tail normal approximation.
`SF((zcrit*sd_null-delta*sqrt(n))/sd_alt) + CDF((-zcrit*sd_null-delta*sqrt(n))/sd_alt)`

Method reference: https://www.statsmodels.org/v0.14.6/generated/statsmodels.stats.proportion.power_proportions_2indep.html

## Limits and decision gates

- Planning approximation, not exact binomial power or a guarantee of observed uplift.
- Independent binary ITT outcomes, one primary metric, equal allocation, no interim peeking.
- No clustered/repeated units, sequential or multiple-outcome designs, or loss/amount-mean power.
- At least 10 expected successes and failures per arm is a conservative scope gate, not proof of accuracy.
- Traffic and follow-up are supplied assumptions; operational delays and missing outcomes can extend timing.
- Primary-metric power does not power fraud, complaints, credit loss or contribution guardrails.
- Missing approved numeric guardrails or owner approvals still block launch; immature risk blocks scale-up.
