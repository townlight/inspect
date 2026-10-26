Townlight Inspections

Townlight Inspections is the Townlight module for inspection support: repeat-case lookup, inspector-owned report drafting, notice draft support, staff review queues, review-required Townlight Code context packets, adversarial local integration mocks, and records-ready inspection exports.

Current state: Townlight Inspections v0.2.2 corrective demotion state. This narrow truth-repair release is no functional upgrade; it exists solely to supersede the false v1.0.0 release from 2026-05-21 in GitHub's Latest impression, with the Townlight Core pin unchanged. This repo provides a FastAPI package aligned to the Townlight Core v1.1.0 release wheel, deterministic and database-backed repeat-case lookup, persisted report-draft records, staff-only review queue workflows, review-required inspection context packets, adversarial local integration mocks, notice draft support, records-ready export checklists, and accessible public sample UI at /civicinspect.

Set CIVICINSPECT_CASE_DB_URL to enable persistent repeat-case, report-draft, and staff review records. Persisted staff routes require CIVICINSPECT_STAFF_API_KEY, X-CivicInspect-Role: staff or service, and matching X-CivicInspect-Staff-Key from a trusted staff or service workflow.

Townlight Inspections does not issue official findings, citations, fines, notices, inspection schedules, legal advice, live photo analysis, live LLM calls, or system-of-record updates.


## Connected candidate 0.3.0+dev.1

Connected desktop candidate 0.3.0+dev.1 adds migrated inspection revisions, original evidence hashes, actual saved repeat cases, public Code citations, server-attributed staff review and private/report versus separately edited Records-copy packets. Native staff authentication and the desktop inspections-preview profile are required. This is source work awaiting required CI and installed acceptance, not a published release. The standalone sample UI and historical 0.2.2 evidence remain unchanged. No official notice issuance, citation, fine, scheduling, image analysis or transcription is added.
