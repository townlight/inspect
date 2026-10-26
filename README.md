<a id="civicinspect"></a>

# Townlight Inspections

Townlight Inspections is the Townlight module for inspection support: repeat-case lookup, inspector-owned report drafting, notice draft support, staff review queues, review-required Townlight Code context packets, adversarial local integration mocks, and records-ready inspection exports.

Current state: **v0.2.2 corrective demotion state - deterministic scaffold; no real AI layer, full frontend, Alembic migrations, real municipal data/search, or public-use gate. This narrow truth-repair release is no functional upgrade; it exists solely to supersede the false v1.0.0 release from 2026-05-21 in GitHub's Latest impression. The Townlight Core pin is unchanged.**. This repo provides a FastAPI package aligned to the Townlight Core v1.1.0 release wheel, health/root endpoints, documentation gates, deterministic and database-backed repeat-case lookup, persisted report-draft records, staff-only review queue workflows, review-required inspection context packets, adversarial local integration mocks, notice draft support, records-ready export checklists, and accessible public sample UI at `/civicinspect`.

<a id="what-civicinspect-does"></a>

## What Townlight Inspections Does

- Looks up deterministic or configured repeat-case context for a property.
- Drafts inspection report outlines from inspector-provided notes and observation text.
- Persists report drafts and staff review queue records when `CIVICINSPECT_CASE_DB_URL` is configured.
- Routes review work through staff-only queue endpoints protected by `CIVICINSPECT_STAFF_API_KEY`.
- Carries Townlight Code and inspection case context IDs into review-required inspection packets without calling those systems live.
- Validates adversarial local integration mocks for spoofed roles, attempted findings, citations, fines, stale context, and live photo-analysis claims.
- Drafts notice text for staff review without issuing notices.
- Produces records-ready export checklists for inspection case files.
- Demonstrates a public inspection-support UI at `/civicinspect`.

<a id="what-civicinspect-does-not-do"></a>

## What Townlight Inspections Does Not Do

- It does not issue official findings, citations, fines, or notices.
- It does not perform live image recognition or photo analysis.
- It does not schedule inspections or update an inspection system of record.
- It does not provide legal advice.
- It does not call live LLMs in this release.

## API Surface

- `GET /` returns the shipped/planned boundary.
- `GET /health` returns package and Townlight Core versions.
- `GET /civicinspect` returns the accessible public sample UI.
- `POST /api/v1/civicinspect/cases/repeat-lookup` returns repeat-case context.
- `POST /api/v1/civicinspect/reports/draft` returns an inspector-review-required report draft.
- `GET /api/v1/civicinspect/reports/{report_id}` retrieves persisted report records when `CIVICINSPECT_CASE_DB_URL` is configured.
- `POST /api/v1/civicinspect/context/inspection-review` returns review-required CivicCode/case context.
- `POST /api/v1/civicinspect/integrations/mock/inspection-context` validates adversarial local integration mocks.
- `POST /api/v1/civicinspect/notices/draft` returns a notice draft with required staff actions.
- `POST /api/v1/civicinspect/staff/reviews` creates a staff-only review queue item.
- `GET /api/v1/civicinspect/staff/reviews` lists staff-only review queue items.
- `PATCH /api/v1/civicinspect/staff/reviews/{review_id}` updates staff-only review queue status, assignment, and resolution.
- `GET /api/v1/civicinspect/staff/reviews/summary` returns staff queue counts.
- `POST /api/v1/civicinspect/export` returns a records-ready inspection export checklist.

Set `CIVICINSPECT_CASE_DB_URL` to enable persistent repeat-case, report-draft, and staff review records. Persisted staff routes require `CIVICINSPECT_STAFF_API_KEY`, `X-CivicInspect-Role: staff`, and matching `X-CivicInspect-Staff-Key` from a trusted staff workflow. The shared Townlight Core `staff_key_gate` validates the key with timing-safe comparison.

## Local Development

```bash
python -m pip install -e ".[dev]"
python -m pytest -q
bash scripts/verify-release.sh
```

## License

Code: AGPL-3.0-only, with the TownLight Public Institution Exception for qualifying deployments. See [LICENSE](LICENSE) and [LICENSE-EXCEPTION.md](LICENSE-EXCEPTION.md).
Documentation: CC BY 4.0 ([LICENSE-DOCS](LICENSE-DOCS)).


## Connected candidate 0.3.0+dev.1

Connected desktop candidate 0.3.0+dev.1 adds migrated inspection revisions, original evidence hashes, actual saved repeat cases, public Code citations, server-attributed staff review and private/report versus separately edited Records-copy packets. Native staff authentication and the desktop inspections-preview profile are required. This is source work awaiting required CI and installed acceptance, not a published release. The standalone sample UI and historical 0.2.2 evidence remain unchanged. No official notice issuance, citation, fine, scheduling, image analysis or transcription is added.
