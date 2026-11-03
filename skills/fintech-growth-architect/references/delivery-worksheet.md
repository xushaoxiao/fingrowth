# Delivery worksheet

## System and evidence

| Transition | Business completion | Authoritative source | Owner role | Failure/recovery | Evidence gap |
| --- | --- | --- | --- | --- | --- |
| KYC submitted → completed | Verification outcome persisted | KYC outcome record | Identity engineering | Bounded retry; route eligible unresolved cases to approved support | Distinguish timeout, rejection and abandonment |
| Accepted → funded | Ledger-confirmed first disbursement | Disbursement ledger | Payments engineering | Idempotent provider request; reconcile ambiguous responses | Provider success alone is insufficient |

These rows are examples, not statements about an existing system. A proposed event contract should define event ID, schema version, logical subject/join key, occurrence/ingestion time, completion semantics, reason category and deduplication rule. Specify the contract without publishing customer payloads or identifiers.

## Backlog

| Priority | Deliverable | Dependency | Proposed owner | Acceptance | Recovery | Decision gate |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Separate KYC technical failures from policy outcomes | Approved aggregate reason taxonomy | Data + identity engineering | Known synthetic timeout/rejection paths appear in distinct counters; retries do not double count | Revert counter consumer; replay from authoritative events | Data owner verifies denominator |
| 2 | Clearer document guidance experiment | Reliable events and baseline | Product + experiment owner | Assignment persisted; primary metric reproducible from assignment population | Return eligible traffic to control | Risk defines stop rules; power unresolved until calculated |

## Synthetic scenario

Funded-user volume falls. KYC completion also falls, while provider timeouts rise in the same window. This supports investigating a dependency failure; it does not prove causation. Check release timing, provider response categories, missing events and population mix. Restore/verify the dependency path before interpreting the period as an onboarding experiment. Do not weaken KYC or underwriting as a conversion fix.

Acceptance for the investigation: reconcile submitted requests and terminal outcomes, account for pending/retried requests, and explain the remaining discrepancy with the data owner. A repaired endpoint alone does not establish business-path recovery.
