# Security

Current source package: `townlight-inspections` 0.3.0+dev.2. Windows MSI 1.7.0.1 is [published](https://github.com/townlight/townlight/releases/tag/townlight-beta-1-windows-1.7.0.1). Its [acceptance summary](https://github.com/townlight/townlight/releases/download/townlight-beta-1-windows-1.7.0.1/ACCEPTANCE-Windows-1.7.0.1.md) identifies the tested workflows and limits; standalone source checks remain separate.

Townlight Inspections is municipal inspection-support software. Current version: 0.2.3. This is a narrow truth-repair release with no functional upgrade. The previous v1.0.0 release was published in error and does not prove public-use readiness. Do not deploy it as a system of record unless the deployment adds production identity, tenant scoping, audit logging, backup, and operations controls.

When `TOWNLIGHT_INSPECTIONS_CASE_DB_URL` is configured, persisted staff review queue routes require `TOWNLIGHT_INSPECTIONS_STAFF_API_KEY`, `X-Townlight-Inspections-Role: staff`, and a matching `X-Townlight-Inspections-Staff-Key` from a trusted staff workflow. Townlight Inspections uses Townlight Core `staff_key_gate` for timing-safe staff-key comparison. This local API-key gate is a release safeguard, not a replacement for production identity, tenant scoping, and audit logging.

Report suspected vulnerabilities privately to the project maintainer. Do not open public issues containing exploit details, secrets, or sensitive municipal data.


## Connected candidate 0.3.0+dev.1

Connected desktop candidate 0.3.0+dev.1 adds migrated inspection revisions, original evidence hashes, actual saved repeat cases, public Code citations, server-attributed staff review and private/report versus separately edited Records-copy packets. Native staff authentication and the desktop inspections-preview profile are required. This is source work awaiting required CI and installed acceptance, not a published release. The standalone sample UI and historical 0.2.2 evidence remain unchanged. No official notice issuance, citation, fine, scheduling, image analysis or transcription is added.
