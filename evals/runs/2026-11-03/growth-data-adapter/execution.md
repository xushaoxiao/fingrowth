# Execution record

## Scope

All reads and writes were confined to this authorized workspace. No network, repositories, external systems or subagents were used. Skill files, task and source files were not modified.

## Files read

- `TASK.md`
- `source.json`
- `incomplete-source.json`
- `growth-data-adapter/SKILL.md`
- `growth-data-adapter/references/workspace-contract.md`
- `growth-data-adapter/assets/renamed-fields-profile.json`
- `growth-data-adapter/assets/identity-profile.json`
- `growth-data-adapter/scripts/build_workspace.py`
- Generated `profile.json` (by mapper) and `workspace.json` (verification).

## Actual commands and outcomes

1. `pwd && rg --files .` — exit 0; enumerated only the authorized workspace.
2. `cat TASK.md growth-data-adapter/SKILL.md growth-data-adapter/references/workspace-contract.md growth-data-adapter/assets/renamed-fields-profile.json growth-data-adapter/assets/identity-profile.json` — exit 0; read task, skill, contract and example profiles.
3. `cat source.json incomplete-source.json growth-data-adapter/scripts/build_workspace.py` — exit 0; reconciled supplied paths and read the bundled validation implementation.
4. `python3 - <<'PY' ... PY` — local Python orchestration: created the explicit 21-field profile, ran the following two actual subprocess commands, captured stdout/stderr/exit status separately, verified copied values/types and protected-file hashes, and wrote this record and answer. No upstream transformation was applied.

```sh
python3 growth-data-adapter/scripts/build_workspace.py source.json --profile profile.json --output workspace.json
python3 growth-data-adapter/scripts/build_workspace.py incomplete-source.json --profile profile.json --output incomplete-workspace.json
```

- Complete source: exit 0; stdout and stderr empty; workspace written.
- Incomplete source: exit 2; stdout empty; stderr preserved verbatim below and in `incomplete.stderr.txt`:

```text
Invalid workspace input: source[0]: a mapped source field is missing
```

- No partial incomplete workspace exists.
- Read-back verification passed: both source rows retained; all 21 mapped values per row match source values and Python types; 21 provenance mappings present; both planning arrays empty.
- Protected input/skill SHA-256 hashes were identical before and after artifact generation; `input-integrity.json` records them.

## Artifacts

`workspace.json`, `profile.json`, `answer.md`, `execution.md`, `input-integrity.json`, `valid.stdout.txt`, `valid.stderr.txt`, `valid.exit-status.txt`, `incomplete.stdout.txt`, `incomplete.stderr.txt`, `incomplete.exit-status.txt`.

## Limits

Validation covers the bundled dashboard contract and copied field fidelity. Economic recognition, loss basis, category alignment, detailed stage semantics and maturity have not been independently established. No import, publishing or external business action was attempted.
