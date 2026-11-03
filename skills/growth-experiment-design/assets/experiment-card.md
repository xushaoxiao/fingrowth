# Experiment card

- Status and decision owner:
- Business decision / scope / jurisdiction:
- Evidence and unresolved assumptions:
- Falsifiable hypothesis:
- Eligible population and pre-treatment exclusions:
- Randomization unit, allocation, persistent assignment and contamination control:
- Control / treatment / exposure cap:
- Primary metric: numerator / assigned eligible denominator (ITT) / horizon / source:
- Economic outcome and loss basis, if relevant:
- Baseline, absolute or relative MDE, alpha, power, method and sample size:
- Eligible assignments per day, recruitment duration and follow-up:
- Multiplicity and stopping procedure:

| Guardrail | Numerator / denominator | Horizon / maturity | Approved numeric stop threshold | Owner | Stop / recovery action |
| --- | --- | --- | --- | --- | --- |
| Technical failure | Define | Define | Unresolved | Engineering | Define |
| Complaints / consent | Define | Define | Unresolved | Operations / privacy | Define |
| Fraud / credit loss | Define loss basis and exposure | Define mature observation | Unresolved | Risk / finance | Define |

- Instrumentation checks: assignment balance, sample-ratio mismatch, event deduplication, missing outcomes and reconciliation:
- Rollback owner and control restoration:
- Primary analysis and segment/multiplicity treatment:
- Launch prerequisites and named approvals still needed:
- Scale decision and delayed-risk review date:
- What would invalidate the conclusion:

## Worked synthetic design fragment

Hypothesis: clearer document-upload instructions improve KYC completion within seven days. Randomize eligible consenting new applicants once, before KYC, 1:1; persist assignment. Primary = assigned people completing KYC within seven days / all assigned eligible people. Keep risk policy unchanged. Technical error reason codes help interpret the result but do not replace ITT analysis.

Baseline/MDE, sample size, numeric guardrails and eligible daily traffic are not supplied. Status: **blocked before launch**. A seven-day KYC horizon is not a mature credit-loss horizon; even an immediate primary-metric win cannot authorize economic scale-up.
