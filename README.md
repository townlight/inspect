Windows x64 Beta 1 · MSI 1.7.0.1

The signed [Windows x64 beta 1.7.0.1](https://github.com/townlight/townlight/releases/tag/townlight-beta-1-windows-1.7.0.1) passed the documented fresh Windows Sandbox checks with synthetic data.

- <a href="https://townlight.github.io/manuals/inspections.html#townlight-inspections-manual" id="toc-townlight-inspections-manual">Townlight Inspections Manual</a>
  - <a href="https://townlight.github.io/manuals/inspections.html#contents" id="toc-contents">Contents</a>
  - <a href="https://townlight.github.io/manuals/inspections.html#using-this-manual" id="toc-using-this-manual">Using this manual</a>
  - <a href="https://townlight.github.io/manuals/inspections.html#beta-identity" id="toc-beta-identity">Beta identity</a>
  - <a href="https://townlight.github.io/manuals/inspections.html#first-run" id="toc-first-run">First run</a>
  - <a href="https://townlight.github.io/manuals/inspections.html#daily-workflow" id="toc-daily-workflow">Daily workflow</a>
  - <a href="https://townlight.github.io/manuals/inspections.html#connected-workflows" id="toc-connected-workflows">Connected workflows</a>
  - <a href="https://townlight.github.io/manuals/inspections.html#architecture" id="toc-architecture">Architecture</a>
  - <a href="https://townlight.github.io/manuals/inspections.html#evidence-limits-outlines-and-previous-cases" id="toc-evidence-limits-outlines-and-previous-cases">Evidence limits outlines and previous cases</a>
  - <a href="https://townlight.github.io/manuals/inspections.html#technical-specifications" id="toc-technical-specifications">Technical specifications</a>
  - <a href="https://townlight.github.io/manuals/inspections.html#configuration-and-administration" id="toc-configuration-and-administration">Configuration and administration</a>
  - <a href="https://townlight.github.io/manuals/inspections.html#api-and-integration-examples" id="toc-api-and-integration-examples">API and integration examples</a>
  - <a href="https://townlight.github.io/manuals/inspections.html#mcp-and-automation-boundary" id="toc-mcp-and-automation-boundary">MCP and automation boundary</a>
  - <a href="https://townlight.github.io/manuals/inspections.html#security-and-permissions" id="toc-security-and-permissions">Security and permissions</a>
  - <a href="https://townlight.github.io/manuals/inspections.html#backup-recovery-and-maintenance" id="toc-backup-recovery-and-maintenance">Backup recovery and maintenance</a>
  - <a href="https://townlight.github.io/manuals/inspections.html#troubleshooting" id="toc-troubleshooting">Troubleshooting</a>
  - <a href="https://townlight.github.io/manuals/inspections.html#verified-workflows-and-limits" id="toc-verified-workflows-and-limits">Verified workflows and limits</a>
  - <a href="https://townlight.github.io/manuals/inspections.html#terms-of-service-and-license" id="toc-terms-of-service-and-license">Terms of service and license</a>
  - <a href="https://townlight.github.io/manuals/inspections.html#glossary" id="toc-glossary">Glossary</a>
  - <a href="https://townlight.github.io/manuals/inspections.html#alphabetical-subject-index" id="toc-alphabetical-subject-index">Alphabetical subject index</a>
  - <a href="https://townlight.github.io/manuals/inspections.html#source-and-document-control" id="toc-source-and-document-control">Source and document control</a>

# Townlight Inspections Manual

**Townlight Beta 1** · Naming candidate documentation edition 2 November 2026

## Contents

- [Using this manual](https://townlight.github.io/manuals/inspections.html#using-this-manual)
- [Beta identity](https://townlight.github.io/manuals/inspections.html#beta-identity)
- [First run](https://townlight.github.io/manuals/inspections.html#first-run)
- [Daily workflow](https://townlight.github.io/manuals/inspections.html#daily-workflow)
- [Connected workflows](https://townlight.github.io/manuals/inspections.html#connected-workflows)
- [Architecture](https://townlight.github.io/manuals/inspections.html#architecture)
- [Evidence limits outlines and previous cases](https://townlight.github.io/manuals/inspections.html#evidence-limits-outlines-and-previous-cases)
- [Technical specifications](https://townlight.github.io/manuals/inspections.html#technical-specifications)
- [Configuration and administration](https://townlight.github.io/manuals/inspections.html#configuration-and-administration)
- [API and integration examples](https://townlight.github.io/manuals/inspections.html#api-and-integration-examples)
- [MCP and automation boundary](https://townlight.github.io/manuals/inspections.html#mcp-and-automation-boundary)
- [Security and permissions](https://townlight.github.io/manuals/inspections.html#security-and-permissions)
- [Backup recovery and maintenance](https://townlight.github.io/manuals/inspections.html#backup-recovery-and-maintenance)
- [Troubleshooting](https://townlight.github.io/manuals/inspections.html#troubleshooting)
- [Verified workflows and limits](https://townlight.github.io/manuals/inspections.html#verified-workflows-and-limits)
- [Terms of service and license](https://townlight.github.io/manuals/inspections.html#terms-of-service-and-license)
- [Glossary](https://townlight.github.io/manuals/inspections.html#glossary)
- [Alphabetical subject index](https://townlight.github.io/manuals/inspections.html#alphabetical-subject-index)
- [Source and document control](https://townlight.github.io/manuals/inspections.html#source-and-document-control)

## Using this manual

Townlight Inspections helps inspectors and authorized reviewing staff. Inspections retains original evidence, supplied observations and optional configured photo/audio analysis, then supports reviewed case workpapers and a separate Records copy. Automatic output is a draft for inspector review.

Staff should begin with First run and Daily workflow. Administrators should also read Architecture, Technical specifications, Configuration, Security and Recovery. Developers should use the exact API/data dictionary and examples. The table of contents and alphabetical subject index link to the relevant sections in the HTML edition; the PDF preserves headings and searchable text. An editable Word edition is included with the same documentation companion.

## Beta identity

| Identity | Value |
|----|----|
| Documentation | Townlight Beta 1 naming, Access and Notice candidate |
| Intended installer version | 1.7.0.1 |
| Product component | townlight-inspections 0.3.0+dev.2 |
| Principal import package | townlight_inspections |
| Native desktop source version | 1.7.0-1 |
| Candidate hashes | [SHA-256 checksums](https://github.com/townlight/townlight/releases/download/townlight-beta-1-windows-1.7.0.1/SHA256SUMS-Windows-1.7.0.1.txt) and [Windows acceptance summary](https://github.com/townlight/townlight/releases/download/townlight-beta-1-windows-1.7.0.1/ACCEPTANCE-Windows-1.7.0.1.md) |
| Current owned software license | AGPL-3.0-only |
| Acceptance composition | Fresh Windows x64 profile; inspections-preview; Station configured separately |

Use an empty database and fresh Windows profile. The installer refuses legacy profile initialization. The approved profile path is `%LOCALAPPDATA%\CivicSuite`. Keep existing profiles and backups.

## First run

1.  Download the signed MSI, matching source companion and checksums from the [public Windows release](https://github.com/townlight/townlight/releases/tag/townlight-beta-1-windows-1.7.0.1).
2.  Verify the MSI hash and Authenticode publisher before installing on a fresh Windows profile. See the [Windows acceptance summary](https://github.com/townlight/townlight/releases/download/townlight-beta-1-windows-1.7.0.1/ACCEPTANCE-Windows-1.7.0.1.md) for the tested setup.
3.  Launch Townlight under the intended named Windows account. Choose the storage folders. Select **Townlight Inspections candidate** (`inspections-preview`) for the bounded desktop composition, including Access and Notice. A narrower default selection will not expose all workspaces.
4.  Enter the city profile, time zone and contacts. Create the first named local administrator, sign in and choose protected backup storage. **Continue without local AI** is valid for the deterministic workflows.
5.  Run Health Check and wait for readiness. Open Townlight. In System Health select **Finish Records Migration** to activate the canonical Python/PostgreSQL runtime. Do not fabricate migration receipts or seed accounts.
6.  Create named staff through Settings. Import authorized sources using each product’s source library. All examples in this package are synthetic; they are not municipal authority.
7.  Provision Station separately if it is part of the beta exercise. Selecting the desktop composition does not start or configure Station. Configure vision explicitly only if automatic photo drafting is selected.

## Daily workflow

<span id="workflow-1"></span>

### 1. Create the case

Enter the property/case context and inspector observations. Keep staff-only notes and identifiers in their intended fields. Save before moving away from the workspace.

<span id="workflow-2"></span>

### 2. Retain originals

Add original supported files using the existing evidence control. Inspect the filename, size and retained hash. Preserve originals separately from any derivative draft.

<span id="workflow-3"></span>

### 3. Choose supplied or automatic text

Use supplied photo observations and a supplied voice summary for deterministic work. If configured, Analyse originals calls the image-capable provider and bundled audio transcriber. Read unavailable/failed results as such; do not label supplied text automatic.

<span id="workflow-4"></span>

### 4. Review the analysis and citations

Compare automatic wording to the original evidence. Correct errors, uncertainty and Code citations. A model output is neither an official finding nor a notice.

<span id="workflow-5"></span>

### 5. Save and record review

Save the case and explicitly record inspector/staff review of that revision. Later edits create a draft requiring renewed review. Retain the case history.

<span id="workflow-6"></span>

### 6. Prepare the Records copy

Separately edit and review the public summary. Preview the Records copy and confirm that private observations, property/address detail and staff notes are excluded according to its contract.

<span id="workflow-7"></span>

### 7. Hand off exact bytes

Attach the reviewed copy to an existing Records request. Inspect its attachment/hash in Records. Attachment does not issue an enforcement action or approve a public-records response.

### Working safely

Use your own named account and save before leaving a screen. A saved draft is durable; unsaved form text may not be. If a write has an unknown result, reopen its record before repeating it.

Read source jurisdiction, dates, citation, version and visibility. A copied source hash identifies exact bytes, not their legal applicability. If a source changes or permission is removed, resolve the source problem rather than substituting stale cached content.

Keep originals and derivatives separate. Review the intended audience before export. A public summary excludes private fields only through the applicable copy contract and your review. A renamed private packet is still private content.

Drafting, review, approval, attachment, export, fulfillment and publication are separate operations. A Townlight workpaper does not itself adopt law, issue a permit, impose a fine or release a records response. The responsible staff member records the applicable decision.

## Connected workflows

Consumes cited Code and Core contracts; supplies a reviewed copy to Records. It does not imply an automatic permit-system or enforcement-system writeback.

| Direction | Material |
|----|----|
| Input | Inspector-supplied text, original supported photographs or audio, a configured image-capable provider when photo analysis is selected, and permitted Code authority. |
| Output | Retained evidence with provenance, editable automatic drafts where configured, reviewed cases and exact audience-specific packets. |

### Product boundary

The bundled Whistle CPU engine executes raw-audio transcription. Automatic photo analysis requires explicit vision configuration; missing configuration reports unavailable. Synthetic execution proves that adapters run, not field recognition accuracy. No official citation/fine issuance, inspection scheduling or enforcement-system writeback is provided.

## Architecture

<figure>
<img src="https://townlight.github.io/assets/inspections-architecture.svg" alt="Townlight Inspections architecture and evidence flow" />
<figcaption aria-hidden="true">Townlight Inspections architecture and evidence flow</figcaption>
</figure>

The drawing shows the principal staff/evidence path. Native commands carry trusted identity to Python business services; PostgreSQL and retained original files hold durable state. A downstream copy does not silently transfer decision authority. Station has its own configured authority/media boundary, database and mutable files. The connected-workflow text supplies the drawing’s reading order and accessibility alternative.

## Evidence limits outlines and previous cases

### Select supported original files

The retained-original contract accepts the following MIME types, up to **10,000,000 bytes per original**. This is a decimal byte limit, not 10 MiB. An unsupported type or oversized file is refused; preserve the original outside the import and choose a supported derivative deliberately rather than changing its filename to disguise the type.

| Material | Accepted MIME types |
|----|----|
| Photographs | `image/jpeg`, `image/png`, `image/webp` |
| Audio | `audio/webm`, `audio/ogg`, `audio/wav`, `audio/mpeg`, `audio/mp4` |
| Plain text | `text/plain` |
| Document | `application/pdf` |

The case input bounds evidence to ten items; the browser’s upload-body guard can be more restrictive when encoding/combining files. Read the actual refusal and reduce the selected batch rather than assuming the per-file limit guarantees the entire request will fit. Accepted retention of text/PDF does not promise photo analysis of that format. Configure an image-capable vision model for photographs. Whistle handles supported raw audio when provisioned; TextFlowKit is a separately configured alternative. Missing configuration is unavailable, not a fabricated successful analysis.

Retain the original filename, MIME type, byte count and SHA256. Compare generated observations/transcript with the evidence, correct the draft and record review of the saved case revision. Supplied photo observations or a supplied voice summary must remain labeled supplied text.

### Find earlier retained cases

Use the existing repeat-case lookup or authenticated `POST /desktop/v1/inspections/repeat-cases` with:

``` json
{"property_reference":"Synthetic parcel A"}
```

Use the same property reference as the saved synthetic case. The mounted implementation matches the normalized property reference against saved case heads, verifies each revision hash and returns up to 50 entries with entity/revision identity, title and review state, plus `sample_data: false`. Empty results mean no matching retained cases in this store. This is separate from the lower-level `townlight_inspections.case_lookup.lookup_repeat_cases` helper, which returns sample context and is not the mounted saved-case query. Neither route queries an external enforcement system. Keep any real prior case identity and facts separate from a model’s proposed narrative. No GIS capture or external enforcement-system connection is implied.

### Prepare an outline for review

The mounted `POST /desktop/v1/inspections/notice-draft` accepts the same `InspectionInput` shape as the saved workflow, not an arbitrary notice recipient or enforcement command. For example:

``` json
{"title":"Synthetic review","property_reference":"Synthetic parcel A","inspection_reference":"SYN-001","dataset_kind":"fictional","inspector_notes":"Synthetic loose panel observed","photo_observations":["Synthetic panel appears loose"],"voice_notes":"Inspector supplied summary"}
```

Inspect the returned draft/outline and its limitations. The lower-level `townlight_inspections.notice_draft.draft_notice` takes case identity, property reference, violation type and supplied observations. This source helper supplies a reviewable outline; it does not issue a citation, serve notice, choose an official fine or make an enforcement determination. Where no native button exists, technical staff use the current authenticated API rather than an invented screen.

Revise the saved case’s `notice_draft` only after checking the actual evidence and applicable Code source. Save and record review again; a new revision does not inherit the previous review. The staff packet and separately reviewed Records copy retain their existing audience/exclusion rules. A drafted outline is neither a Records release nor proof that a notice was delivered.

Source contracts: `townlight_inspections/media_analysis.py`, `case_lookup.py`, `notice_draft.py`, workflow models and `townlight_runtime/inspections_bridge.py`.

## Technical specifications

### Runtime and storage

The accepted package targets **Windows x64 fresh installation**. Its native shell uses **Rust 2021, Tauri 2 and Microsoft WebView2**; browser assets are JavaScript built with **Vite 8.1.6**. This describes the native desktop frontend; Station has a separate React operator, specified below or in its product manual. Canonical business workflows use bundled **CPython 3.13.5, FastAPI, Pydantic, SQLAlchemy and Alembic**, with **PostgreSQL 17 / PostGIS** and managed original files. The installed runtime tested here contains FastAPI 0.162.0. Package minimum Python requirements can differ from the bundled executable; the metadata reference preserves both. No stack rewrite is implied by the beta label.

The native transport is fixed to loopback `127.0.0.1:15480`; PostgreSQL uses the configured local runtime port (default `15432`). Optional local model service defaults to `127.0.0.1:15434`. Those are deployment defaults, not internet endpoints. The runtime has health, module and readiness endpoints; readiness is stronger than process existence. The task queue is the existing local Core task infrastructure, not an assertion that a separate Redis service is required for this desktop composition.

The default native profile is `%LOCALAPPDATA%\CivicSuite`; the historical directory name remains part of compatibility. Do not rename it to Townlight. A configured `TOWNLIGHT_PROFILE_ROOT` must be absolute. Local configuration and secrets live under that profile; protected managed files and database state must be backed up coherently. Source/runtime identity is distinct from a product’s display label.

### Data and consistency

Original evidence files and hashes; media analysis records; observations and voice summaries; Code citations; case revisions; review records; private packets and separately edited Records copies.

Versioned saves use expected prior revision identifiers where defined. Reopen and reconcile on conflict. Exact exports and handoffs use source IDs, current visibility, revision and SHA256. Review belongs to the saved revision and does not transfer silently to edited text. Database changes use the owning product’s migrations; a request or readiness check is not an authorization to mutate schema.

### Capacity and platform statements

This beta has synthetic single-profile workflow evidence. It does not have a published benchmark for concurrent staff capacity, minimum RAM/CPU, large-source limits or a field SLA. Do not turn a developer machine’s specification into a supported minimum. The signed MSI is 2,082,697,216 bytes; allow additional disk for extracted runtime, database, originals, exports, media and backups. Select equipment/storage after sizing those actual workloads.

The exact [runtime payload lock](https://townlight.github.io/reference/runtime-payload-lock.json) records pinned files, sizes and hashes. The [component metadata](https://townlight.github.io/reference/component-metadata.json) records shipped dependency declarations. These references are more precise than a manually copied dependency list. Third-party and historical license notices must accompany their matching payloads.

## Configuration and administration

### Native deployment configuration

Use Setup, Settings and System Health for supported staff operation. Administrators provision folders, backup storage, named accounts and the city profile. Select `inspections-preview` for the bounded desktop composition, including Access and Notice. Station remains a separate service boundary. Do not use a standalone product’s demo server as a substitute for the installed workspace.

Technical deployments use `TOWNLIGHT_PRODUCT_PROFILE`, `TOWNLIGHT_PROFILE_ROOT`, `DATABASE_URL`, `TOWNLIGHT_RUNTIME_PORT`, `PORTAL_MODE` and the runtime-managed secret files. Treat database URLs and native session proofs as secrets. The installed native domain runtime explicitly refuses non-loopback binding. `PORTAL_MODE=private` is the accepted posture; changing it does not by itself commission an internet portal, authentication provider or reverse proxy.

The isolated documentation exporter sets a fictional profile and unusable synthetic database origin only to read schemas; those values are not deployment configuration. Keep deployment values in the intended process/account scope. An already-running process does not automatically inherit later environment edits.

### Optional media analysis configuration

`TOWNLIGHT_INSPECTIONS_VISION_PROVIDER` accepts `ollama`, `openai` or `anthropic`. Select an actually image-capable model through `TOWNLIGHT_INSPECTIONS_VISION_MODEL`; an Ollama endpoint may use `TOWNLIGHT_INSPECTIONS_VISION_BASE_URL`. `TOWNLIGHT_INSPECTIONS_VISION_THINK` accepts true/false/low/medium/high where that configured adapter uses it. Keep provider credentials in protected deployment configuration, never in a source bundle. Missing vision configuration returns unavailable rather than invented observations.

`TOWNLIGHT_INSPECTIONS_TRANSCRIBER` selects `whistle` or `textflowkit`; the installed candidate provisions the bundled Whistle CPU path. The owning transcriber assets and retained notices must stay with it. A provider result remains an editable draft with original evidence retained. The separate TextFlowKit MCP adapter is not an automatically enabled Townlight server.

## API and integration examples

### Native command example

The following JavaScript belongs in the existing trusted Townlight frontend/development environment with `invoke` imported from `@tauri-apps/api/core`. It is not a command for an arbitrary web page or an instruction for nontechnical staff. IDs must come from records created in an isolated synthetic exercise.

``` javascript
import { invoke } from '@tauri-apps/api/core';
const result = await invoke('inspections_domain_request', {request: {operation: 'cases', offset: 0}});
console.log(result);
```

### Trusted local HTTP example

An administrator/developer can inspect an already-configured isolated runtime from a trusted local process. This PowerShell example reads the signed-in synthetic profile’s existing proof into memory; it does not create a user, seed a session, reveal the proof in output or bypass a permission check. Do not use real city data in development examples. A read response does not prove approval or publication.

``` powershell
$profilePath = Join-Path $env:LOCALAPPDATA 'CivicSuite'
$sessionPath = Join-Path $profilePath 'config\local-session.json'
$session = Get-Content -LiteralPath $sessionPath -Raw | ConvertFrom-Json
$headers = @{ 'X-Townlight-Session' = $session.session_hash }
Invoke-RestMethod -Uri 'http://127.0.0.1:15480/desktop/v1/inspections/evidence/supported-types' -Headers $headers
Remove-Variable session, headers
```

### A synthetic write with subsequent readback

This example demonstrates the existing Meetings HTTP contract in an isolated exercise. It is intentionally fictional. It does not start a service. Its authentication setup is included so it can be run independently under the signed-in synthetic account. If a write times out, inspect current records before repeating it.

``` powershell
$profilePath = Join-Path $env:LOCALAPPDATA 'CivicSuite'
$sessionPath = Join-Path $profilePath 'config/local-session.json'
$session = Get-Content -LiteralPath $sessionPath -Raw | ConvertFrom-Json
$headers = @{ 'X-Townlight-Session' = $session.session_hash }
$body = @{
  title = 'Synthetic documentation exercise'
  scheduled_start = '2026-11-05T18:00:00-07:00'
  location = 'Synthetic room'
  meeting_type = 'regular'
} | ConvertTo-Json
$meeting = Invoke-RestMethod -Method Post `
  -Uri 'http://127.0.0.1:15480/desktop/v1/meetings/meetings' `
  -Headers $headers -ContentType 'application/json' -Body $body
Invoke-RestMethod `
  -Uri ('http://127.0.0.1:15480/desktop/v1/meetings/meetings/' + $meeting.id) `
  -Headers $headers
Remove-Variable session, headers
```

This write requires Meetings to be enabled and the signed-in staff role to permit it. It is a cross-suite integration example; for this product’s request models, use the complete technical reference below.

### Complete technical contract

Read the [Inspections API reference](https://townlight.github.io/api/inspections.html) for every documented operation, request field, constraint, response declaration and source supplement. Download the [OpenAPI JSON](https://townlight.github.io/api/inspections-openapi.json) for tools. For Station this is the suite-side schema only; its separate service contract is documented in the API supplement. The [reference directory](https://townlight.github.io/reference/index.html) includes configuration/source inventories, dependency declarations, native command contracts, MCP signatures and candidate evidence.

## MCP and automation boundary

No direct product MCP server is exposed by the accepted Townlight desktop or Station boundary. Do not configure an invented `townlight mcp` command or assume an AI client has staff permissions. The integration surfaces for this beta are native IPC, the documented HTTP APIs, source bundle imports, exact exports and the existing Station CLI.

The bundled transcription code includes a **TextFlowKit MCP adapter** as a separate source capability. It offers job-based `transcribe_media`, `get_transcript`, `list_jobs`, `get_job_status` and `export_transcript`, and additional tools declared in that adapter. It uses stdio first and optional Streamable HTTP, with the MCP SDK as an optional extra. It is not automatically launched, authenticated as Townlight staff or accepted as a Townlight product MCP deployment. This documentation does not add such a service.

For a transcription client already provisioned separately, an illustrative tool call is:

``` json
{"name":"get_job_status","arguments":{"job_id":"synthetic-existing-job-id"}}
```

Use a job ID returned by that transcription service. This example does not create a Townlight record or bypass its review/Records handoff. The exact optional adapter tool signatures are supplied in the [MCP source reference](https://townlight.github.io/reference/mcp.html). Station meeting capture does not become live speech recognition because this optional donor adapter exists.

## Security and permissions

Use your own named account and save before leaving a screen. A saved draft is durable; unsaved form text may not be. If a write has an unknown result, reopen its record before repeating it.

Read source jurisdiction, dates, citation, version and visibility. A copied source hash identifies exact bytes, not their legal applicability. If a source changes or permission is removed, resolve the source problem rather than substituting stale cached content.

Keep originals and derivatives separate. Review the intended audience before export. A public summary excludes private fields only through the applicable copy contract and your review. A renamed private packet is still private content.

Drafting, review, approval, attachment, export, fulfillment and publication are separate operations. A Townlight workpaper does not itself adopt law, issue a permit, impose a fine or release a records response. The responsible staff member records the applicable decision.

The native session is validated and mapped to a persisted SQL identity. An editable actor/reviewer label is not authentication. Product/module permissions and source visibility apply at the server boundary. Revoked/unavailable authority fails closed for new Station operations; a previous permission result is not a perpetual authorization.

Use protected local folders, account permissions and credential storage. Never include the native session file, database passwords, provider keys or unredacted support bundles in a public issue or generated public documentation. A local public view is not automatically a secured internet deployment. Keep network exposure and real equipment acceptance specific to the chosen beta site.

## Backup recovery and maintenance

Save work and use Core’s canonical **Backup Now** before maintenance. That operation stops writers. Preserve the coherent profile/database/document backup and its receipt, then use **Start** to resume. A source export is not a full backup.

Use **Restore Latest Backup** through the supported controls. If the result says **Restore needs service start**, use **Start**, then **Check**, and reopen a known record. Do not repeat restore merely because services need to start. The fresh-profile acceptance verified that a fulfilled request survived restore and a post-backup marker did not.

Keep Station’s dedicated database and media evidence together in its own backup. Core’s native-profile backup must not be assumed to include an external Station data directory. Stop writers during a coordinated backup. Preserve failed media attempts and logs.

On failure, record the time, selected composition, component/installer versions and exact message. Check System Health for stopped, starting, ready or failed dependencies. Use the existing Retry control after readiness; do not create duplicate business records to refresh a stale view. Share only a redacted diagnostic bundle. Preserve secrets, original evidence, recovery material and unrelated installations.

## Troubleshooting

| Symptom | Likely meaning | Next action |
|----|----|----|
| Workspace absent | Wrong product composition or unavailable canonical runtime. | Check selected composition; activate through Finish Records Migration; wait for readiness. |
| Cannot sign in / 401 | Missing or expired named account session. | Sign in normally; reopen a Station launch ticket if applicable. |
| Permission denied / 403 | Account, module, source or browser-origin permission. | Ask the authorized administrator to inspect the intended permission; do not invent role headers. |
| Save conflict / 409 | The saved revision, expected source hash or lifecycle changed. | Keep edits, reopen current state and reconcile deliberately. |
| Invalid input / 422 | Required field, format, geometry, source envelope or state is invalid. | Read the field detail and correct the input/source; preserve originals. |
| Service unavailable / 503 | Database, schema, connected source or configuration unavailable. | Inspect System Health and the named dependency. Preserve work; retry only after readiness. |
| Export refused | Missing exact review, approval, audience or source authorization. | Read the refusal and complete the owning product’s explicit decision. |
| Restore needs service start | The snapshot was restored but services have not resumed. | Use Start, then Check and verify a saved record; do not blindly repeat restore. |
| Photo analysis unavailable | No configured image-capable vision service. | Use supplied observations or have an administrator configure the existing adapter. |
| Automatic text is incorrect | Model recognition is uncertain or wrong. | Compare original evidence, edit and record inspector review before any official use. |

## Verified workflows and limits

| Product | Recorded result | Precisely exercised |
|----|----|----|
| Inspections | PASS | Retained original/hash, supplied observations and voice summary, saved/reviewed case/readback, separate exact Records copy and private handoff; address exclusion; native workspace. |

These results come from the identified signed candidate’s fresh normal-profile Sandbox exercise: real native IPC/HTTP/PostgreSQL and selected headless controls. All accounts, source bundles and media were synthetic. The guest install/uninstall and recovery passed, and the owned Sandbox stopped. No host installed application or standalone CivicCast was changed. This documentation task reuses those receipts; it does not claim a new software acceptance run.

See the [Windows acceptance summary](https://github.com/townlight/townlight/releases/download/townlight-beta-1-windows-1.7.0.1/ACCEPTANCE-Windows-1.7.0.1.md) for this MSI. The historical [evidence index](https://townlight.github.io/reference/sandbox-evidence-index.json) applies to its original build.

The limits remain: actual city field acceptance and equipment/network commissioning; Station automatic provisioning/SCM commissioning; every UI/role combination; field recognition accuracy; and historical in-place upgrades are not certified. They are not five invented feature requirements. Fresh-install controlled beta handoff remains the accepted scope. This package makes no city-deployment, publication or general-availability claim.

## Terms of service and license

### Scope and status

These terms describe the Townlight Beta 1 software and this documentation package. This public Windows beta is for evaluation. No uptime commitment, support response time, indemnity, data-processing agreement or paid service is created by these documents. A separate signed agreement, if any, governs services it actually provides.

### Software license and rights

Current Townlight-owned distributions identified in this candidate use **AGPL-3.0-only**. The full license is supplied with this documentation and with the source companion. The license governs rights to run, copy, modify and convey the covered software; these operational terms do not add restrictions to those rights. Historical grants and dependency licenses retain their own terms. CivicCast remains a separate product and is not relicensed by this documentation work.

When conveying covered software, retain applicable notices and provide the corresponding source and installation/build information required by the license. For a modified version supporting remote network interaction, follow section 13’s source-offer requirement. The companion archive identifies the source for this candidate; a link to a different public branch is not a substitute for the matching source. Read the supplied license for the complete conditions. See the [GNU license reference](https://www.gnu.org/licenses/agpl-3.0.html) and [GNU licensing FAQ](https://www.gnu.org/licenses/gpl-faq.en.html).

### Data ownership and access

Importing a document does not transfer its ownership or grant permission to publish it. The operating organization controls its accounts, access decisions, lawful source use, retention and review/release policy. Keep resident information, credentials, private notes and restricted evidence in their authorized locations. Documentation examples contain fictional data. No real city account, credential or record is required to exercise these examples in an isolated test environment.

### Local operation and external processors

The accepted beta workflow is local and uses named staff accounts. Station has separate storage and credentials. Configure backup destinations and optional model/network providers deliberately. A configured external provider may receive submitted prompts, images or audio according to that configuration and provider’s terms; this documentation does not promise that every optional configuration is offline. An email outbox or local public view does not establish external delivery or an internet deployment. This static documentation site has no analytics, account collection or remote font dependency.

### Staff decisions and source applicability

Staff verify the jurisdiction, source currency, permissions, citations and proposed audience. Model output and generated guidance require review. No draft is automatically an official legal interpretation, zoning determination, permit approval, fee assessment, enforcement notice or records-release decision. Official permit fee authority remains with the adopted source and responsible organization; imported amounts do not become a new authoritative calculation.

### Beta operation and recovery

Use the identified candidate in its supported fresh-install scope. Preserve backups and original evidence. Test physical equipment and chosen network/service configuration before relying on them. The supplied acceptance describes selected synthetic workflows, not every screen, vendor, field condition or upgrade. Operators decide whether a particular deployment meets their own operational obligations.

### Warranty and liability

The covered software’s warranty and liability conditions are those in sections 15–17 of the supplied AGPL and any applicable separate written undertaking. This documentation creates no additional warranty or limitation beyond those terms. Third-party software is subject to its retained license notices. Nothing here removes rights that applicable law makes nonwaivable.

### Support and incident reporting

Use the project’s existing SUPPORT and SECURITY guidance for its matching repository. Report reproducible behavior with the version, operation and redacted logs. Do not put credentials, resident records or unredacted evidence in a public issue. Coordinate sensitive reports through the channel designated in SECURITY. No new support address or service commitment is invented here.

### Ending a beta exercise and document changes

When an organization ends testing, it controls retention/export and removes access according to its policy. Uninstall may retain data; back up and inspect the selected removal options. Ending an exercise does not revoke rights already granted by AGPL. Later software/documentation versions must identify their changed candidate and scope; historical receipts retain their original identities. These terms do not claim that a city has accepted a contract merely by reading a manual.

## Glossary

| Term | Meaning |
|----|----|
| Approval | An explicit authorized decision on the saved text/artifact. It is separate from saving or attachment. |
| Canonical record | The owning product’s retained identity and saved version, rather than an editable copied label. |
| Composition | The selected set of desktop modules; inspections-preview exposes the eight staff products. |
| Corresponding source | The source/build material matching the delivered covered program, subject to its license. |
| Derivative / Records copy | A separately prepared document with its own intended audience and hash. |
| Hash / SHA256 | A fingerprint of exact bytes. It detects change; it does not establish legal authority. |
| Idempotency | Repeating the same identified request has the same intended effect; changing its payload can be refused. |
| IPC | The native desktop command boundary between its browser interface and Rust host. |
| MCP | Model Context Protocol; no direct Townlight product server is enabled by this beta. |
| Original | Retained source bytes. A reviewed derivative does not replace them. |
| Provenance | Source, version, date, actor and relationship information retained with evidence. |
| Revision | An immutable saved version. Later edits do not inherit an earlier review automatically. |
| Snapshot | A fixed audience-specific copy tied to a source/reviewed revision. |
| Station | Townlight’s separate media boundary using a pinned CivicCast-derived engine; standalone CivicCast remains separate. |

## Alphabetical subject index

- **Accounts and authentication** — [Security and permissions](https://townlight.github.io/manuals/inspections.html#security-and-permissions).
- **AGPL and source** — [Terms of service and license](https://townlight.github.io/manuals/inspections.html#terms-of-service-and-license).
- **API contracts** — [API and integration examples](https://townlight.github.io/manuals/inspections.html#api-and-integration-examples).
- **Architecture** — [Architecture](https://townlight.github.io/manuals/inspections.html#architecture).
- **Backup** — [Backup recovery and maintenance](https://townlight.github.io/manuals/inspections.html#backup-recovery-and-maintenance).
- **Beta version** — [Beta identity](https://townlight.github.io/manuals/inspections.html#beta-identity).
- **Configuration** — [Configuration and administration](https://townlight.github.io/manuals/inspections.html#configuration-and-administration).
- **Evidence and acceptance** — [Verified workflows and limits](https://townlight.github.io/manuals/inspections.html#verified-workflows-and-limits).
- **Fees and official decisions** — [Terms of service and license](https://townlight.github.io/manuals/inspections.html#terms-of-service-and-license).
- **First run** — [First run](https://townlight.github.io/manuals/inspections.html#first-run).
- **Handoffs and audience** — [Connected workflows](https://townlight.github.io/manuals/inspections.html#connected-workflows).
- **MCP** — [MCP and automation boundary](https://townlight.github.io/manuals/inspections.html#mcp-and-automation-boundary).
- **Originals and provenance** — [Security and permissions](https://townlight.github.io/manuals/inspections.html#security-and-permissions).
- **Recovery** — [Backup recovery and maintenance](https://townlight.github.io/manuals/inspections.html#backup-recovery-and-maintenance).
- **Staff procedures** — [Daily workflow](https://townlight.github.io/manuals/inspections.html#daily-workflow).
- **Station configuration** — [Configuration and administration](https://townlight.github.io/manuals/inspections.html#configuration-and-administration).
- **Technical stack** — [Technical specifications](https://townlight.github.io/manuals/inspections.html#technical-specifications).
- **Troubleshooting** — [Troubleshooting](https://townlight.github.io/manuals/inspections.html#troubleshooting).

### Operating subject links

- **Evidence limits outlines and previous cases** — [Evidence limits outlines and previous cases](https://townlight.github.io/manuals/inspections.html#evidence-limits-outlines-and-previous-cases).
- **Find earlier retained cases** — [Find earlier retained cases](https://townlight.github.io/manuals/inspections.html#find-earlier-retained-cases).
- **Prepare an outline for review** — [Prepare an outline for review](https://townlight.github.io/manuals/inspections.html#prepare-an-outline-for-review).
- **Select supported original files** — [Select supported original files](https://townlight.github.io/manuals/inspections.html#select-supported-original-files).

## Source and document control

This edition is authored from the immutable corresponding-source companion, the generated installed-domain schema and the retained workflow receipts. The current software versions and signed artifacts are unchanged. Public historical pages are not synchronized or published by this local documentation task.

### Workflow subject index

- **Choose supplied or automatic text** — [Daily workflow, step 3](https://townlight.github.io/manuals/inspections.html#workflow-3).

- **Create the case** — [Daily workflow, step 1](https://townlight.github.io/manuals/inspections.html#workflow-1).

- **Hand off exact bytes** — [Daily workflow, step 7](https://townlight.github.io/manuals/inspections.html#workflow-7).

- **Prepare the Records copy** — [Daily workflow, step 6](https://townlight.github.io/manuals/inspections.html#workflow-6).

- **Retain originals** — [Daily workflow, step 2](https://townlight.github.io/manuals/inspections.html#workflow-2).

- **Review the analysis and citations** — [Daily workflow, step 4](https://townlight.github.io/manuals/inspections.html#workflow-4).

- **Save and record review** — [Daily workflow, step 5](https://townlight.github.io/manuals/inspections.html#workflow-5).

- [Source inventory and file hashes](https://townlight.github.io/reference/source-inventory.json)

- [All component metadata](https://townlight.github.io/reference/component-metadata.json)

- [Installed domain OpenAPI](https://townlight.github.io/reference/desktop-domain-openapi.json)

- [Workflow matrix](https://townlight.github.io/reference/workflow-matrix.json)

- [Full AGPL text](https://townlight.github.io/reference/AGPL-3.0.txt)


## Source package installation

Use locally built wheels from the exact component sources in the corresponding-source companion and verify their hashes. Do not relabel historical release assets. Installation of these Python packages is a developer/package check;
the signed Windows MSI and its installed acceptance remain separate.

In a new Windows virtual environment, replace the example wheel-directory path
with your locally built wheel directory from the matching pinned source and verify its SHA256 manifest:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
$candidateWheels = (Resolve-Path 'C:\path\to\candidate-wheels').Path
python -m pip install (Join-Path $candidateWheels 'townlight_core-1.3.0.dev2-py3-none-any.whl')
python -m pip install (Join-Path $candidateWheels 'townlight_inspections-0.3.0+dev.2-py3-none-any.whl')
python -c "import townlight_inspections; from importlib.metadata import version; print(version('townlight-inspections'))"
```

Expected principal import: `townlight_inspections`; expected distribution version:
`0.3.0+dev.2`. Use a fresh empty database/profile for workflow testing. Existing
city data and the previous release remain untouched; no in-place upgrade or
old-import compatibility shim is supplied.

## License and responsible use

Current owned code is AGPL-3.0-only. Preserve full license, matching corresponding source, dependency notices and historical grants. Terms of use do not remove license rights. Source imports do not confer permission to publish third-party material. Review all automatic drafts and use the separate owning-product decision before official action. CivicCast remains independent.

## Earlier documentation

Previous editions are retained under `docs/history/pre-townlight-beta-1/`. They describe their original software and license grants. Use the current Townlight Beta 1 manual for this candidate.
