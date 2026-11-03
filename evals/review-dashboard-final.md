# Independent dashboard fixes verification

Review date: 2026-11-03. Source root: `/Users/shaoxiaoxu/Repos/fingrowth`. Scope: current working-tree fixes for the two P2 findings in `review-dashboard-source.md`, exact prior reproductions, relevant new source and regression tests. No repository edits, git, network or browser operations performed. Prior review is preserved unchanged.

## Verdict

**Both P2 findings are resolved in the current code and observed checks. No remaining material issue found within this bounded re-review.** This is source/parser/mapper verification, not browser acceptance or proof that final archives have been built from these changes.

| Previous required finding | Current verdict | Evidence |
| --- | --- | --- |
| Duplicate JSON keys silently overwrite imported values | RESOLVED | TypeScript parses a strict syntax tree and visits every object for duplicate decoded property names before JSON.parse (`dashboard/lib/workspace.ts:387-413`). Exact old conflicting-revenue text now throws the duplicate-field error; it no longer silently imports revenue 999. |
| Mapper emits otherwise-valid payloads larger than browser capacity | RESOLVED | `serialize_workspace` serializes the exact CLI format, checks UTF-8 encoding and 2,000,000-byte limit (`skills/growth-data-adapter/scripts/build_workspace.py:187-196`). Workspace validation calls it (`:181-184`), and CLI uses the same function before file creation/replacement (`:274-284`). Exact old 200-cohort reproduction now fails at build time. TypeScript checks both raw input and canonical emitted representation (`dashboard/lib/workspace.ts:329-333`, `387-389`). |

## Exact narrow reproductions rerun

1. **Duplicate money field:** loaded the valid demo text and replaced its first `"revenue": 42000` with `"revenue": 42000, "revenue": 999`, exactly as before. Executed actual current TypeScript parseWorkspace directly under Node, without browser/UI. Observed:

   `Duplicate JSON field. Resolve the source conflict before import.`

   This rejects the source conflict before object conversion and economic calculation. Existing page import ordering remains validate-before-setWorkspace (`dashboard/app/page.tsx:312-323`); an exception does not replace the old workspace. This state conclusion is source evidence, not a new browser interaction test.

2. **Combined capacity:** loaded the same canonical rows and identity profile, emptied planning arrays, created 200 valid row copies with unique exactly 10,000-character cohort names (`str(i).zfill(3) + "x" * 9997`). Actual current Python build_workspace now raises:

   `serialized workspace must be at most 2000000 UTF-8 bytes`

   The prior artifact size was 2,124,412 bytes; the same oversized content is no longer emitted successfully. No truncation, dropped rows, zero-fill or input modification is used.

3. **Valid path remains compatible:** built a normal two-cohort workspace with empty planning arrays using current Python build_workspace/serialize_workspace. Its 4,841-byte output was accepted by actual TypeScript parseWorkspace. This checks that the fixes did not simply reject all mapper exports.

4. **Explicit timestamp bounds:** actual Python helper rejects `+00:60`, `-00:99` and `24:00:00Z`; source now explicitly bounds hours/minutes/seconds and offset components (`skills/growth-data-adapter/scripts/build_workspace.py:51-67`).

## Tests executed

- Current `dashboard/tests/workspace.test.ts`: **12 passed, 0 failed**, using the installed local tsx runner; no network dependency installation. Covers demo reconciliation, separate count/rate leaders, cents, unknown outcomes, malformed imports, approved flags, currency separation, provenance, UTF-8 byte limits, clock bounds, duplicates/comments/trailing commas and combined payload capacity. New relevant cases at `dashboard/tests/workspace.test.ts:143-179`.
- Four focused Python tests: **4 passed, 0 failed**: combined UTF-8 capacity; canonical Unicode serialization/trailing newline; invalid clock/offset bounds; and oversized CLI failure preserving an existing output. Source tests at `tests/test_workspace.py:155-206`. Python bytecode writes were disabled. The CLI test used its isolated temporary directory, not repository outputs.

The combined-capacity CLI test confirms exit 2, empty stdout, a capacity error and unchanged existing output. This verifies the output-preservation requirement in addition to inspecting control flow.

## Limits and disposition

No optional polish is required to close either P2. The earlier report remains the historical failure record; this report records fresh evidence that both findings are fixed. Economics/ranking implementation remains unchanged in the reviewed sections and its existing direct reconciliation tests pass. Theme behavior, responsive layout, actual browser import interactions, release commit cleanliness, final archive determinism/checksums and publication remain separate checks owned by the parent.
