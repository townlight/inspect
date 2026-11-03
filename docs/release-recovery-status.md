# Townlight Inspections Release-Recovery Status

Date: 2026-05-21

## Status

Townlight Inspections `v0.2.2` is the corrective demotion state after the mistaken 2026-05-21 `v1.0.0` release. This narrow truth-repair release is no functional upgrade; it exists solely to supersede the false v1.0.0 release from 2026-05-21 in GitHub's Latest impression. The previous v1.0.0 release was published in error and is superseded by this honest sub-1.0.0 label. The Townlight Core pin is unchanged.

## Current Runtime Boundary

The package provides deterministic and optional database-backed repeat-case lookup, inspector-owned report draft helpers, persisted report-draft records, staff review queues, notice draft helpers, records-ready export checklist support, review-required inspection context packets, adversarial local integration mocks, and a sample public UI at `/townlight_inspections`.

It does not issue official findings, citations, fines, notices, inspection schedules, legal advice, live photo analysis, live LLM calls, or system-of-record updates.

## Recovery Evidence

- Local `scripts/verify-release.sh` must pass with tests, documentation gate, placeholder import check, Ruff, wheel build, sdist build, and SHA256 generation before the release tag is moved.
- Browser QA covered `/townlight_inspections` and `docs/index.html` at desktop 1440 x 1000 and mobile 390 x 844.
- Historical browser QA recorded zero console messages, zero page errors, no horizontal overflow, visible staff review copy, and visible boundary copy, but it does not prove public-use readiness.
- Staff review queue tests prove create/list/update/summary and auth rejection behavior.
- Adversarial mock tests prove spoofed roles, attempted findings/citations/fines, stale context, and live photo-analysis claims are blocked for staff review.
- Browser QA summary: `docs/browser-qa-townlight_inspections-v1.0.0-summary.md`.

## Promotion Rule

Townlight Inspections may not be called v1.0.0, finished, shipping, city-ready, product-ready, or public-use ready until a future independent audit of the actual code signs off against the full Townlight Section 2 gate.
