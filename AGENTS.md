<a id="civicinspect-agent-contract"></a>

# Townlight Inspections Agent Contract

## Source of Truth

- Upstream suite spec: `townlight/townlight/docs/CivicSuiteUnifiedSpec.md`, especially the Townlight Inspections catalog entry and suite-wide non-negotiables.
- Townlight Inspections supports inspection report drafting, repeat-case lookup, notice draft support, and records-ready exports.
- Inspectors own every decision.

## Hard Boundaries

- Townlight Inspections never issues official findings, citations, fines, notices, schedules inspections, or updates an inspection system of record.
- Townlight Inspections never provides legal advice.
- Townlight Inspections v0.1.0 must not call live LLMs, perform live photo analysis, or rely on production case-system integrations.
- Report and notice drafts must be marked review-required.
- Townlight Inspections depends on Townlight Core; Townlight Core must never depend on Townlight Inspections.
- Townlight Inspections may reference Townlight Code concepts only through released contracts or deterministic sample data in v0.1.0.

## Verification

Run `bash scripts/verify-release.sh` before every push or release.
