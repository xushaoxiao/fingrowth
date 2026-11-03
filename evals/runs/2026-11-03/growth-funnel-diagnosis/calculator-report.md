# FinGrowth synthetic cohort report

Descriptive evidence only. No automatic launch or underwriting decision.

## baseline

Window: 2026-01-01/2026-01-31; outcomes as of 2026-10-31.
Currency: USD; declared mature: true.

Funded CAC: 10.00; contribution: 4,000.00.

| Transition | Population | Progressed | Not progressed | Conversion |
| --- | ---: | ---: | ---: | ---: |
| acquired → registered | 10000 | 6000 | 4000 | 60.00% |
| registered → kyc | 6000 | 4800 | 1200 | 80.00% |
| kyc → applied | 4800 | 3600 | 1200 | 75.00% |
| applied → approved | 3600 | 1800 | 1800 | 50.00% |
| approved → accepted | 1800 | 1500 | 300 | 83.33% |
| accepted → disbursed | 1500 | 1400 | 100 | 93.33% |
| disbursed → repaid | 1400 | 1300 | 100 | 92.86% |
| repaid → repeat | 1300 | 400 | 900 | 30.77% |

### Investigation candidates

- Largest count not progressing: acquired → registered.
- Lowest observed conversion: applied → approved.

These rankings use acquired → disbursed only. Confirm event delivery, cohort mix and policy reasons before assigning a cause.

### Evidence needed before action

- Data owner: check unique-person joins, event delays and ledger reconciliation.
- Product/engineering: split technical errors, abandonment and policy decisions with approved aggregate reason codes.
- Risk/finance: check comparable risk mix and mature loss before any scale decision.

- Synthetic descriptive cohorts do not establish causes or experiment uplift.
- Approval gaps include policy rejection; repayment/repeat are delayed outcomes, not UX drop-off.
- Maturity is declared by the fixture, not verified from exposure or repayment schedules.

contribution = revenue - acquisition - credit loss - funding - servicing - incentives; immature contribution is unknown

## cheap-channel

Window: 2026-01-01/2026-01-31; outcomes as of 2026-10-31.
Currency: USD; declared mature: true.

Funded CAC: 7.14; contribution: -1,000.00.

| Transition | Population | Progressed | Not progressed | Conversion |
| --- | ---: | ---: | ---: | ---: |
| acquired → registered | 12000 | 6500 | 5500 | 54.17% |
| registered → kyc | 6500 | 4600 | 1900 | 70.77% |
| kyc → applied | 4600 | 3500 | 1100 | 76.09% |
| applied → approved | 3500 | 1800 | 1700 | 51.43% |
| approved → accepted | 1800 | 1500 | 300 | 83.33% |
| accepted → disbursed | 1500 | 1400 | 100 | 93.33% |
| disbursed → repaid | 1400 | 1100 | 300 | 78.57% |
| repaid → repeat | 1100 | 350 | 750 | 31.82% |

### Investigation candidates

- Largest count not progressing: acquired → registered.
- Lowest observed conversion: applied → approved.

These rankings use acquired → disbursed only. Confirm event delivery, cohort mix and policy reasons before assigning a cause.

### Evidence needed before action

- Data owner: check unique-person joins, event delays and ledger reconciliation.
- Product/engineering: split technical errors, abandonment and policy decisions with approved aggregate reason codes.
- Risk/finance: check comparable risk mix and mature loss before any scale decision.

- Synthetic descriptive cohorts do not establish causes or experiment uplift.
- Approval gaps include policy rejection; repayment/repeat are delayed outcomes, not UX drop-off.
- Maturity is declared by the fixture, not verified from exposure or repayment schedules.

contribution = revenue - acquisition - credit loss - funding - servicing - incentives; immature contribution is unknown

