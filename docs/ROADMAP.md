# Roadmap and operations

## v0.1 — reference foundation

Implemented on main: four skill entrypoints, aggregate analyzer, synthetic lending case, calculation tests and contributor boundaries. Reference implementation; a successful CI run does not establish real-world outcomes or host compatibility.

## v0.1.0 candidate — usable skills and growth workspace

Implemented candidate scope:

- Each skill ships its own task-specific worksheet, dictionary, input contract or experiment card.
- Funnel calculation produces JSON and readable Markdown, with denominators and distinct investigation rankings by count and conversion.
- Invalid shape, dates, maturity, duplicate fields/cohorts and population ordering fail before output.
- The funnel skill runs after a standalone copy, with no repository imports or third-party libraries.
- The synthetic case report is reproducible in CI, alongside tests across Python 3.10, 3.11 and 3.13.

The original four Skills and added data-adapter Skill have observed isolated-Agent acceptance with independent artifact review; see evals/ACCEPTANCE.md. The Next.js + HeroUI dashboard adds local workspace import/export, six connected views and eight selectable palettes. Browser interaction checks and CI remain distinct from live business acceptance. Release tagging/publication and automatic host discovery are separate milestones.

## Next — v0.2 measurement and experiment tooling

1. Version the input schema and specify migration rules before adding event-level inputs.
2. Generate reproducible synthetic events with deduplication, delayed/pending outcomes and loan-level exposure accounting. Acceptance: reconcile known events to cohort aggregates and reject incompatible populations.
3. Verify maturity using schedules and observation windows rather than trusting a boolean. Acceptance: immature and censored exposures cannot support realized-economics claims.
4. Add a power calculator for a narrowly specified experiment design. Acceptance: documented statistical assumptions, reference-value checks, invalid-input tests and separation of recruitment from risk follow-up.

## Later — v0.3 evaluation and adoption

Benchmark tasks for the four skills, bilingual case walkthroughs and host-specific installation/invocation checks. Recruit practitioner feedback before claiming production readiness. No production integrations without a separate threat model and authorization.

## Operations

Weekly review: reproducible usage reports, issue quality and qualified practitioner feedback. Monthly review: milestone acceptance and the next evidence gap. Publish only verified capabilities. Do not claim employer endorsement, real lending uplift or regulatory certification.

Repository remains the source of truth. Feishu synchronization remains pending a confirmed writable workspace; no synchronization is claimed by this iteration.
