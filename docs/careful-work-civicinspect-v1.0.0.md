<a id="civicinspect-v100-careful-work-evidence"></a>

# Townlight Inspections v1.0.0 Careful-Work Evidence

Date: 2026-05-21

## Scope

Finish the active Townlight Inspections v1.0.0 public-use module release without touching queued modules.

Allowed write scope:

- `C:\Users\scott\OneDrive\Desktop\Claude\civicinspect`

Read-only references:

- `CivicSuite/docs/CivicSuiteUnifiedSpec.md`
- recovered Townlight Permitting v1.0.0 staff queue and adversarial mock patterns
- recovered Townlight Code v1.0.0 Townlight Code context boundary

## Checklist Evidence

1. Read every caller or consumer.
   - Read `main.py`, helper modules, persistence, tests, docs, release script, and public UI.
2. Trace runtime context.
   - Public mode remains deterministic when `CIVICINSPECT_CASE_DB_URL` is unset; persisted staff mode uses `CIVICINSPECT_CASE_DB_URL` plus `CIVICINSPECT_STAFF_API_KEY`.
3. Fan out pattern search across the repo.
   - Compared current Townlight Inspections surfaces with recovered Townlight Permitting v1.0.0 staff queue, context, and adversarial mock behavior.
4. Identify the data contract changing.
   - Version moves to `1.0.0`; staff review queue payloads return `review_id`, report/inspection references, status, assignment, resolution, visibility, timestamps, and boundary copy.
5. State the blast radius before editing.
   - Changes are confined to Townlight Inspections runtime/API/docs/tests/QA artifacts; no queued module edits.
6. Re-read changed files end-to-end after editing.
   - Re-read source and docs through tests, release gate, and diff inspection.
7. Narrate one full code/data/render path.
   - Staff posts report draft with case DB configured -> `create_report` stores the report -> `create_staff_review_queue_item` stores review work -> staff lists and resolves the queue -> public UI and docs show v1.0.0 staff review boundary.
8. Prove new state is consumed or rendered.
   - Tests assert `staff_review_id`, staff review list/update/summary, auth rejection, context packets, adversarial mock findings, and public UI copy.
9. Run the 5-lens self-audit before commit.
   - Engineering: release gate passed.
   - UX: browser QA passed desktop/mobile public UI and docs.
   - Docs: current-facing docs updated and docs gate passed.
   - Security: staff-only queue routes reject missing/spoofed staff key.
   - Product: no official findings/citations/fines/notices/schedules/system-of-record behavior is claimed.

## Verification

- `python -m pytest -q`: 24 passed, 1 warning.
- `python -m ruff check .`: passed.
- `bash scripts/verify-docs.sh`: passed.
- Browser QA: `docs/browser-qa-civicinspect-v1.0.0-summary.md` and `docs/qa/current-civicinspect-release-qa/summary.md`.
