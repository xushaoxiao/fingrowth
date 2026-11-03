# Execution record

Scope: local-only work inside the authorized growth-experiment-design workspace. No network requests, repository access, customer contact, live experiment changes or subagents.

Files read:
- `TASK.md` — the two synthetic design requests and required deliverables.
- `growth-experiment-design/SKILL.md` — specification, status and decision-boundary requirements.
- `growth-experiment-design/assets/experiment-card.md` — required card and synthetic fragment.
- `cohorts.json` — supplied synthetic channel cohorts; not used as the experiment baseline because they do not establish the relevant seven-day randomized outcome.

Commands run, in order:
1. `pwd && rg --files .` — identify the workspace and inventory its files.
2. `cat TASK.md growth-experiment-design/SKILL.md growth-experiment-design/assets/experiment-card.md cohorts.json` — read task and bundled materials.
3. A local `python3` calculation of 120/200, 140/200, their absolute/relative differences, the completion-count difference and total supplied assignments. Outputs: 60%, 70%, 10 percentage points, 16.666667%, 20 and 400.
4. Local heredoc writes creating `answer.md` and this execution record.
5. `wc -l answer.md execution.md` and `tail -n 8 answer.md` — confirm deliverables were written and inspect the final decision text.

Deliverables: `answer.md` and `execution.md`. Skill files and `TASK.md` were not modified.

Limitations: no power calculation was possible without approved baseline/MDE; no eligible traffic or numeric thresholds were supplied; jurisdiction, complete pilot integrity/guardrail evidence and mature credit-loss horizon remain unknown. Pilot arithmetic is descriptive. No inferential uplift or mature economic/risk conclusion is claimed.
