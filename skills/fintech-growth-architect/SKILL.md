---
name: fintech-growth-architect
description: Design a consumer lending growth system or turn a growth objective into system ownership, event contracts and a delivery backlog. Use for architecture and cross-team planning.
---

# FinTech growth architect

Build a delivery plan that connects growth outcomes to engineering, product, risk and finance. Start with the requested objective; do not redesign every service by default.

## Establish scope

Use supplied context first. Identify product, jurisdiction, business goal, journey, authorized scope and system owners. Ask only for missing facts that block a decision; label other assumptions. Use synthetic or approved anonymous aggregates. No PII, credentials, employer documents or production exports.

## Design the system

1. Define success as an economic outcome with a population and time horizon, plus loss, fraud, complaint and consent constraints. Volume alone cannot establish success.
2. Map acquisition → registration → KYC → application → risk decision → approval → acceptance → disbursement → repayment → eligible repeat. Expand only the relevant stages. Separate business rejection, user abandonment and technical failure.
3. For each relevant transition, specify authoritative source, event meaning, owner and downstream dependency. Distinguish request accepted, provider success and ledger-confirmed funding. Include deduplication, idempotency, retries and reconciliation where asynchronous delivery can corrupt counts.
4. Define shared segmentation, orchestration, entitlement and experiment capabilities only where the use case needs them. Keep campaign rules separate from underwriting authority.
5. Sequence the backlog by dependencies and evidence. Each item needs owner role, observable acceptance, rollback/recovery and an unresolved-decision gate. Missing instrumentation precedes optimization.

Use [the delivery worksheet](references/delivery-worksheet.md) for system and backlog tables. It includes a fully synthetic failure scenario; treat it as a worked example, never evidence about the user.

## Deliver

Return scope/assumptions, a system map, an ownership/event table, a phased backlog and open decisions. For each recommendation, name the evidence that would support or overturn it. Role names are proposed owners until confirmed; do not invent people or commitments.

If only a metric definition, funnel calculation or experiment is requested, keep the answer focused on that task rather than forcing a full architecture.

## Decision boundaries

Do not infer protected traits or propose discriminatory targeting. No autonomous underwriting, customer contact, pricing change or deployment. Human owners retain lending and launch authority. Identify jurisdiction before discussing local obligations; qualified local review is needed for legal conclusions. Distinguish observations, hypotheses and recommendations; do not invent results or claim compliance.
