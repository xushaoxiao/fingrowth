# Independent dashboard / release source review

Review date: 2026-11-03. Scope: `/Users/shaoxiaoxu/Repos/fingrowth` sources requested by the parent, relevant adapter/dashboard/release tests, and narrow in-memory parser/mapper probes. **Two required P2 contract fixes found before packaging.** No repository edits, git commands, network access or browser work performed. This review does not claim browser validation or a completed release build.

## Required fixes

### [P2] Reject duplicate JSON object keys before replacing the current workspace

Evidence: `dashboard/lib/workspace.ts:377-380` calls native JSON.parse, which silently keeps the last occurrence of a duplicate key. The Python adapter rejects duplicate keys at `skills/growth-data-adapter/scripts/build_workspace.py:232-243`. Thus input rejected by the adapter can be imported by the UI with silently changed economics or provenance.

Confirmed minimal reproduction, entirely in memory using the existing valid demo workspace:

1. Read `examples/dashboard/workspace.json` as text.
2. Replace only its first `"revenue": 42000` with `"revenue": 42000, "revenue": 999`.
3. Pass the resulting text to the actual exported TypeScript `parseWorkspace` function, executed directly under Node with type stripping.
4. Observed accepted revenue **999**, calculated contribution **−37,001**. The adapter's duplicate-object hook rejects the identical text with **duplicate JSON field**.

This is a data-integrity/acceptance mismatch, not a rendering issue. Source validation runs after JSON.parse, so it cannot recover the discarded first value. Required correction: use a duplicate-aware JSON reader or equivalent structural detection before native object construction; reject duplicates at every object depth, including numeric, flag and provenance fields. Preserve the current workspace on that failure. Add a parser regression with duplicate nested money/flag/provenance keys and confirm the failure path does not replace state. Do not repair or silently choose one value.

### [P2] Enforce browser payload capacity in the mapper before emitting a supposedly importable workspace

Evidence: `dashboard/lib/workspace.ts:378-379` and `dashboard/app/page.tsx:327-329` reject payloads above 2,000,000 UTF-8 bytes. Python validates individual strings/array counts (`skills/growth-data-adapter/scripts/build_workspace.py:23-25`, `33-38`, `104-108`, `160-164`) but has no total serialized size check before successful stdout/file output (`build_workspace.py:255-270`). This permits a successful bundled adaptation whose actual artifact the dashboard cannot import.

Confirmed minimal reproduction with actual `build_workspace` and `parseWorkspace`, no disk outputs:

1. Load canonical `examples/lending/cohorts.json` and the bundled identity profile; clear both planning arrays.
2. Create 200 copies of its first valid cohort, giving each a unique exactly 10,000-character name: `str(i).zfill(3) + "x" * 9997`.
3. Actual Python `build_workspace(rows, profile)` succeeds: each field and collection satisfies the documented limits.
4. Serialize using the CLI's exact `json.dumps(workspace, indent=2, allow_nan=False) + "\n"` format. Result is **2,124,412 UTF-8 bytes**.
5. Feed that exact output to actual TypeScript `parseWorkspace`; observed **Workspace exceeds the 2 MB limit.** Even compact serialization in the preliminary probe was already over 2 MB.

Required correction: apply the shared 2,000,000-byte limit to the actual emitted serialization before writing stdout or replacing an output file. Fail nonzero without partial output, preserve existing artifacts, explain capacity, and keep inputs unchanged. Add a mapper→browser capacity regression that combines individually valid fields into an oversized payload; existing tests cover per-field/array sizes but miss their combined byte size. Trimming source strings or dropping cohorts is not an acceptable fix.

## Checks with no material bug found

- **Economics and ranking definitions:** `dashboard/lib/workspace.ts:120-132` converts bounded decimal inputs into integer cents; five cost buckets sum safely within the chosen bounds, and `metrics:326-374` handles zero denominators, separate acquisition-to-funding count/rate leaders, ties and immature contribution correctly. The source intentionally uses the bounded dashboard contract rather than the standalone Python analyzer's extreme-scale contract; that separation is not a bug.
- **Displayed conclusions:** `dashboard/app/page.tsx:248-272` takes each leader from its own leader array; `:543-547`, `:646-650`, `:721-724`, `:795-811` disclose conditional maturity, comparability, delayed outcomes and single-loss treatment. No fabricated default rate, channel winner or mature economic claim found.
- **Import atomicity:** `dashboard/app/page.tsx:312-323` parses and validates before setWorkspace. Existing validation exceptions only set the error; they do not replace the old workspace or cohort. File-read failure and 2 MB checks similarly avoid replacement (`:325-336`). The duplicate-key issue above is an erroneously accepted input, not a catch-path state bug.
- **Theme/data separation:** `dashboard/app/page.tsx:278-297` persists only the resolved allowlisted theme ID under `fingrowth-theme`; imported workspace remains React state (`:299-310`). `dashboard/lib/themes.ts:1-16` allows only eight known theme IDs. Theme CSS contains scoped local palette overrides, no imports/remote URLs; it preserves semantic positive/negative colors. No imported values are copied into theme preference, browser storage, network calls or exported theme metadata in these sources.
- **Timestamp candidate disconfirmed:** an in-memory `+00:60` extraction-offset probe is rejected by both current Python and TypeScript implementations. No required offset bug is asserted from that candidate.
- **Release source provenance:** `scripts/build_release.py:31-47` requires a clean committed checkout, pins HEAD, checks source after dashboard build, and reads source/skill content from pinned committed objects. `:21-28` sorts ZIP entries and fixes timestamp/mode; `:77-91` records commit/tree and byte-level checksums. The dashboard variant explicitly builds and packages the static output (`:39-45`, `:69-76`). No material deterministic source-pack provenance bug found by reading this implementation.

## Validation limits and disposition

Read the corresponding tests in `dashboard/tests/workspace.test.ts`, `tests/test_workspace.py` and `tests/test_release.py`; they support the intended behavior but were not run as a suite during this bounded review. Only the direct in-memory Node/Python reproductions above were executed. Release tests use git, so none was executed under the no-git restriction. Browser behavior, hydration, viewport layout, theme contrast and final archive reproducibility are the parent's separate checks.

Fix the two confirmed parser/capacity mismatches, add focused regressions, then rerun the relevant contract checks before final packaging. No optional visual/style polish is a release requirement from this review.
