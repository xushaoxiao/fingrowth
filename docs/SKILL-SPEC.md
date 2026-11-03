# Skill specification

Each `skills/<name>/SKILL.md` contains YAML frontmatter with a matching kebab-case name and a task-specific description. The body defines required evidence, workflow, decision boundaries and an observable deliverable. Each entrypoint and all linked resources must work when the **entire folder** is copied on its own; repository documents are optional extended context.

Current resources:

| Skill | Bundled resource | Purpose |
| --- | --- | --- |
| fintech-growth-architect | references/delivery-worksheet.md | Event ownership and acceptance-driven backlog |
| growth-metric-tree | references/metric-dictionary.md | Metric definitions and arithmetic reconciliation |
| growth-funnel-diagnosis | references/input-contract.md, scripts/analyze.py | Strict synthetic calculations and report |
| growth-experiment-design | assets/experiment-card.md | Fillable experiment specification with unresolved launch gates |

The funnel implementation has no external dependencies. `scripts/analyze.py` at repository root delegates to it; there is no second copy of the calculation logic. Tests run a copied folder in Python isolated mode outside the checkout. This verifies execution portability, not host automatic discovery or the quality of every agent response.

Skill installation never authorizes mutation of a lending system. Changes require realistic examples and observable calculation tests where relevant. Avoid tests that merely match skill wording; behavioral evaluation should use representative tasks and explicitly track missing evidence. Host-specific invocation, independent behavioral evaluation and real practitioner acceptance remain separate milestones.
