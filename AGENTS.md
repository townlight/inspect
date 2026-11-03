<a id="townlight_inspections-agent-contract"></a>

# Townlight Inspections Agent Contract

## Governing contract and candidate identity

Scott's bounded completion contract governs. Legacy skills, automatic delegation,
milestone/review loops and generic extra gates require explicit invocation.
Preserve actual product requirements, required CI/release checks, security/data
safeguards and installed acceptance. Reuse unaffected evidence with its limits.

Current distribution: `townlight-inspections` 0.3.0+dev.2; principal import:
`townlight_inspections`. Shared dependency: `townlight-core==1.3.0.dev2`. Use the exact
coordinated source pins and local candidate wheels in the README; never fabricate
renamed historical release URLs. Source tests do not establish installed acceptance
or publication. The original [agent contract](docs/history/pre-naming-2026-11/AGENTS.md)
is retained as history, not current session authorization.

The candidate supports fresh branded databases and fresh profiles only. Preserve
existing data and refuse unmarked legacy initialization; no in-place upgrade or
old import shim is provided. The sole approved old active identifier is
`%LOCALAPPDATA%\CivicSuite` for that profile path only. Other retained old active
identifiers require Scott's approval in the single exception registry. Preserve
historical identities, third-party attribution and standalone CivicCast.

## Source of Truth

- Upstream suite spec: `townlight/townlight/docs/TownlightUnifiedSpec.md`, especially the Townlight Inspections catalog entry and suite-wide non-negotiables.
- Townlight Inspections supports inspection report drafting, repeat-case lookup, notice draft support, and records-ready exports.
- Inspectors own every decision.

## Hard Boundaries

- Townlight Inspections never issues official findings, citations, fines, notices, schedules inspections, or updates an inspection system of record.
- Townlight Inspections never provides legal advice.
- Optional configured photo/audio analysis follows the existing selected provider/model and manual; it produces review-required drafts, never official findings. Do not add providers, change the selected model or rely on production case-system integrations.
- Report and notice drafts must be marked review-required.
- Townlight Inspections depends on Townlight Core; Townlight Core must never depend on Townlight Inspections.
- Townlight Inspections may reference Townlight Code concepts only through the pinned candidate contracts or deterministic sample data; preserve the documented deployment boundary.

## Verification

Run meaningful affected checks and the required `bash scripts/verify-release.sh` release gate. Record actual failures/skips; preserve required CI and installed acceptance.
