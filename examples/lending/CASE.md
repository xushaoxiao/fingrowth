# Synthetic lending case: cheaper acquisition can destroy value

All numbers are invented, not Shaoxiao's or any employer's results. See cohorts.json and the metric contract for population and dates.

## Architecture
Acquisition attribution → consent-aware registration → KYC → application → independent risk decision → offer → disbursement ledger → repayment ledger → eligible repeat journey. Growth owns orchestration; risk owns underwriting; finance reconciles economics; servicing owns complaints and repayment support. Reconcile disbursement events against ledger totals and retry idempotently.

## Metric tree and diagnosis
Baseline: 10,000 acquired, 1,400 funded, USD 14,000 acquisition cost, funded CAC 10. Contribution 42,000 − 14,000 − 14,000 − 5,000 − 3,000 − 2,000 = 4,000.

Cheap channel: 12,000 acquired, 1,400 funded, acquisition cost 10,000, funded CAC about 7.14. Contribution 42,000 − 10,000 − 23,000 − 5,000 − 3,000 − 2,000 = −1,000. Repayment counts fall from 1,300 to 1,100. These descriptive cohorts do not establish channel causation; mix, maturity or servicing differences may explain the result. Actual loss severity is supplied, not derived from unpaid counts.

## Experiment card
Hypothesis: clearer document-upload guidance increases completed KYC without worsening risk quality. Eligible: consenting new applicants with supported devices, before KYC; randomize once per person 1:1, persist assignment. Control: existing guidance; treatment: clarified instructions. Primary: KYC completion within 7 days / assigned eligible people (ITT). Monitor technical failure, complaints, fraud and mature credit loss; do not change underwriting. Finance also assesses mature contribution per assigned person. Baseline variance, MDE and sample size remain unknown: do not launch until calculated and approved. Predeclare fixed horizon and multiplicity approach; no repeated significance peeking. Risk owner defines numeric stop thresholds; operations owns rollback to control. Block scale-up until risk outcomes mature and finance reconciles totals.

## Decision
Investigate channel mix and onboarding failures; do not scale solely because CAC fell. This case demonstrates all four skill outputs but does not validate real-world uplift.
