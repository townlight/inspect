"""FastAPI runtime foundation for Townlight Inspections."""

import os

from civiccore import __version__ as CIVICCORE_VERSION
from civiccore.auth import staff_key_gate
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from civicinspect import __version__
from civicinspect.adapters import (
    PUBLIC_SOURCES_ENV,
    ConfigurationError,
    configured_analysis_providers,
    configured_transcription_provider,
    configured_vision_provider,
)
from civicinspect.case_lookup import lookup_repeat_cases
from civicinspect.integration_mocks import validate_inspection_context_mocks
from civicinspect.media_analysis import (
    EvidenceRejected,
    analyse_evidence,
    retain_evidence,
)
from civicinspect.notice_draft import draft_notice
from civicinspect.persistence import (
    InspectionCaseRepository,
    StaffReviewQueueItem,
    StaffReviewSummary,
    StoredInspectionReport,
)
from civicinspect.public_ui import render_public_lookup_page
from civicinspect.records_export import build_inspection_export
from civicinspect.report_draft import draft_inspection_report
from civicinspect.workflow_models import AnalysisRecord


app = FastAPI(
    title='Townlight Inspections',
    version=__version__,
    description='Inspection report, repeat-case, notice-drafting, and staff-review support for Townlight.',
)

_case_repository: InspectionCaseRepository | None = None
_case_db_url: str | None = None
_require_staff_key = staff_key_gate("CIVICINSPECT_STAFF_API_KEY", "X-CivicInspect-Staff-Key")


class RepeatCaseLookupRequest(BaseModel):
    property_reference: str
    violation_type: str = ""


class ReportDraftRequest(BaseModel):
    inspection_id: str
    property_reference: str
    inspector_notes: str
    photo_observations: list[str] = []
    voice_notes: str = ""
    analysis: AnalysisRecord | None = None


class NoticeDraftRequest(BaseModel):
    case_id: str
    property_reference: str
    violation_type: str
    observations: list[str]


class InspectionExportRequest(BaseModel):
    title: str
    case_id: str
    format: str = "markdown"


class InspectionContextRequest(BaseModel):
    inspection_id: str
    property_reference: str
    violation_type: str
    code_context_id: str = ""
    case_context_id: str = ""
    source_date_status: str = "current"


class IntegrationMockRequest(BaseModel):
    scenario: str = "inspection-context"
    role: str = "staff"
    code_context_id: str = ""
    case_context_id: str = ""
    official_finding: bool = False
    citation_issued: bool = False
    fine_amount: str | None = None
    photo_analysis_source: str = "inspector_observation"
    source_date_status: str = "current"


class EvidenceItemRequest(BaseModel):
    filename: str
    media_type: str
    description: str = ""
    content_base64: str
    sha256: str


class EvidenceRetainRequest(BaseModel):
    items: list[EvidenceItemRequest]


class MediaAnalysisRequest(BaseModel):
    items: list[EvidenceItemRequest]
    code_links: list[dict[str, str]] = []
    inspector_supplied_text: str = ""


class StaffReviewCreateRequest(BaseModel):
    inspection_id: str
    property_reference: str
    reason: str
    report_id: str | None = None


class StaffReviewUpdateRequest(BaseModel):
    status: str
    assigned_to: str | None = None
    resolution: str | None = None


@app.get("/")
def root() -> dict[str, str]:
    """Return current product state without overstating unshipped behavior."""

    return {
        "name": "CivicInspect",
        "version": __version__,
        "status": "inspection support product with staff review queues",
        "message": (
            "Townlight Inspections package, API foundation, sample repeat-case lookup, optional database-backed "
            "repeat-case and report-draft records, staff review queues, review-required Townlight Code "
            "context packets, adversarial local integration mocks, inspector-owned report draft "
            "helper, notice draft helper, records-ready export checklist, and public UI are online; "
            "official findings, citations, fines, inspection scheduling, live photo analysis, live "
            "LLM calls, and system-of-record integrations are not implemented."
        ),
        "next_step": "Configure CIVICINSPECT_CASE_DB_URL and CIVICINSPECT_STAFF_API_KEY before using staff queues.",
    }


@app.get("/health")
def health() -> dict[str, str]:
    """Return dependency/version health for deployment smoke checks."""

    return {
        "status": "ok",
        "service": "civicinspect",
        "version": __version__,
        "civiccore_version": CIVICCORE_VERSION,
    }


@app.get("/civicinspect", response_class=HTMLResponse)
def public_civicinspect_page() -> str:
    """Return the public sample inspection support UI."""

    return render_public_lookup_page()


@app.post("/api/v1/civicinspect/cases/repeat-lookup")
def repeat_case_lookup(request: RepeatCaseLookupRequest) -> dict[str, object]:
    result = _lookup_repeat_cases(
        property_reference=request.property_reference,
        violation_type=request.violation_type,
    )
    return result.__dict__


@app.post("/api/v1/civicinspect/reports/draft")
def inspection_report_draft(request: ReportDraftRequest) -> dict[str, object]:
    if _case_database_url() is not None:
        stored = _get_case_repository().create_report(
            inspection_id=request.inspection_id,
            property_reference=request.property_reference,
            inspector_notes=request.inspector_notes,
            photo_observations=tuple(request.photo_observations),
            voice_notes=request.voice_notes,
            analysis=request.analysis,
        )
        staff_review = _get_case_repository().create_staff_review_queue_item(
            report_id=stored.report_id,
            inspection_id=stored.inspection_id,
            property_reference=stored.property_reference,
            reason="Inspection report draft requires staff review before any notice or enforcement action.",
            created_by="staff",
        )
        return _stored_report_response(stored, staff_review=staff_review)

    result = draft_inspection_report(
        inspection_id=request.inspection_id,
        property_reference=request.property_reference,
        inspector_notes=request.inspector_notes,
        photo_observations=tuple(request.photo_observations),
        voice_notes=request.voice_notes,
        analysis=request.analysis,
    )
    payload = result.__dict__
    payload["cited_sections"] = list(result.cited_sections)
    payload["analysis"] = (request.analysis.model_dump(mode="json")
                           if request.analysis is not None else None)
    payload["report_id"] = None
    payload["staff_review_id"] = None
    return payload


@app.get("/api/v1/civicinspect/reports/{report_id}")
def get_inspection_report(report_id: str) -> dict[str, object]:
    if _case_database_url() is None:
        raise HTTPException(
            status_code=503,
            detail={
                "message": "Townlight Inspections case persistence is not configured.",
                "fix": "Set CIVICINSPECT_CASE_DB_URL to retrieve persisted inspection report records.",
            },
        )
    stored = _get_case_repository().get_report(report_id)
    if stored is None:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "Inspection report record not found.",
                "fix": "Use a report_id returned by POST /api/v1/civicinspect/reports/draft.",
            },
        )
    return _stored_report_response(stored)


def _retain_all(items) -> list:
    retained = []
    for item in items:
        try:
            retained.append(retain_evidence(
                filename=item.filename,
                media_type=item.media_type,
                description=item.description,
                content_base64=item.content_base64,
                expected_sha256=item.sha256,
            ))
        except EvidenceRejected as exc:
            raise HTTPException(
                status_code=422,
                detail={"message": f"Evidence '{item.filename}' was not retained: {exc}",
                        "fix": "Send original unmodified bytes, their base64 encoding, the "
                               "matching SHA256, and a supported media type (text, image, "
                               "PDF or raw audio)."},
            ) from None
    return retained


def _analysis_providers() -> dict:
    """Code sources for cited sections, from the configured public source file."""

    try:
        return configured_analysis_providers()
    except ConfigurationError as exc:
        raise HTTPException(
            status_code=503,
            detail={"message": "Configured inspection Code sources could not be read.",
                    "detail": str(exc),
                    "fix": f"Check {PUBLIC_SOURCES_ENV} and restart the runtime."},
        ) from None


def _vision_provider():
    try:
        return configured_vision_provider()
    except ConfigurationError as exc:
        raise HTTPException(
            status_code=503,
            detail={"message": str(exc),
                    "fix": "Set CIVICINSPECT_VISION_PROVIDER to ollama, openai or "
                           "anthropic (and a supported think mode)."},
        ) from None


def _transcription_provider():
    """The owned TextFlowKit transcriber, or None when it is not configured."""

    return configured_transcription_provider()


@app.post("/api/v1/civicinspect/evidence/retain")
def retain_evidence_route(request: EvidenceRetainRequest) -> dict[str, object]:
    """Retain original evidence bytes (photos, documents and raw audio) with hashes."""

    retained = _retain_all(request.items)
    return {
        "retained_evidence": [item.as_record() for item in retained],
        "count": len(retained),
        "raw_audio_retained": any(item.media_type.startswith("audio/") for item in retained),
        "disclaimer": (
            "Original bytes retained with their SHA256. Retention is not a finding, "
            "citation, notice or enforcement action."
        ),
    }


@app.post("/api/v1/civicinspect/media/analyse")
async def media_analyse(request: MediaAnalysisRequest) -> dict[str, object]:
    """Draft-only analysis of retained media; inspector review always required."""

    retained = _retain_all(request.items)
    vision, model = _vision_provider()
    result = await analyse_evidence(
        evidence=retained,
        code_links=request.code_links,
        providers=_analysis_providers(),
        vision_provider=vision,
        transcription_provider=_transcription_provider(),
        model=model,
        inspector_supplied_text=request.inspector_supplied_text,
    )
    return result.to_payload()


@app.post("/api/v1/civicinspect/notices/draft")
def notice_draft(request: NoticeDraftRequest) -> dict[str, object]:
    result = draft_notice(
        case_id=request.case_id,
        property_reference=request.property_reference,
        violation_type=request.violation_type,
        observations=tuple(request.observations),
    )
    return result.__dict__


@app.post("/api/v1/civicinspect/context/inspection-review")
def inspection_review_context(request: InspectionContextRequest) -> dict[str, object]:
    repeat_context = _lookup_repeat_cases(
        property_reference=request.property_reference,
        violation_type=request.violation_type,
    )
    citations = [f"Repeat-case context: {case_id}" for case_id in repeat_context.related_case_ids]
    if request.code_context_id:
        citations.append(f"Townlight Code context: {request.code_context_id}")
    if request.case_context_id:
        citations.append(f"Inspection case context: {request.case_context_id}")
    return {
        "inspection_id": request.inspection_id.strip() or "unassigned-inspection",
        "property_reference": request.property_reference.strip() or "unknown property",
        "violation_type": request.violation_type.strip() or "general inspection",
        "code_context_id": request.code_context_id,
        "case_context_id": request.case_context_id,
        "source_date_status": request.source_date_status,
        "citations": citations,
        "repeat_case_count": repeat_context.repeat_case_count,
        "review_required": True,
        "boundary": (
            "Townlight Inspections provides inspection review context only; it is not an official finding, "
            "citation, fine, notice issuance, inspection schedule, photo-analysis result, or "
            "system-of-record action."
        ),
    }


@app.post("/api/v1/civicinspect/integrations/mock/inspection-context")
def integration_mock_inspection_context(request: IntegrationMockRequest) -> dict[str, object]:
    result = validate_inspection_context_mocks(request.model_dump())
    return {
        "scenario": result.scenario,
        "status": result.status,
        "review_required": result.review_required,
        "findings": list(result.findings),
        "boundary": result.boundary,
    }


@app.post("/api/v1/civicinspect/export")
def inspection_export(request: InspectionExportRequest) -> dict[str, object]:
    result = build_inspection_export(
        title=request.title,
        case_id=request.case_id,
        format=request.format,
    )
    return result.__dict__


@app.post("/api/v1/civicinspect/staff/reviews")
def create_staff_review(
    request: StaffReviewCreateRequest,
    _staff_principal: object = Depends(_require_staff_key),
) -> dict[str, object]:
    _require_persistence_configured()
    item = _get_case_repository().create_staff_review_queue_item(
        inspection_id=request.inspection_id,
        property_reference=request.property_reference,
        reason=request.reason,
        report_id=request.report_id,
        created_by="staff",
    )
    return _staff_review_payload(item)


@app.get("/api/v1/civicinspect/staff/reviews")
def list_staff_reviews(
    status: str | None = None,
    _staff_principal: object = Depends(_require_staff_key),
) -> dict[str, object]:
    _require_persistence_configured()
    return {
        "visibility": "staff_only",
        "items": [
            _staff_review_payload(item)
            for item in _get_case_repository().list_staff_review_queue_items(status=status)
        ],
    }


@app.patch("/api/v1/civicinspect/staff/reviews/{review_id}")
def update_staff_review(
    review_id: str,
    request: StaffReviewUpdateRequest,
    _staff_principal: object = Depends(_require_staff_key),
) -> dict[str, object]:
    _require_persistence_configured()
    try:
        item = _get_case_repository().update_staff_review_queue_item(
            review_id=review_id,
            status=request.status,
            assigned_to=request.assigned_to,
            resolution=request.resolution,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail={"message": "Staff review update is invalid.", "fix": str(exc)},
        ) from exc
    if item is None:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "Townlight Inspections staff review item was not found.",
                "fix": "List staff reviews and retry with an existing review_id.",
            },
        )
    return _staff_review_payload(item)


@app.get("/api/v1/civicinspect/staff/reviews/summary")
def staff_review_summary(
    _staff_principal: object = Depends(_require_staff_key),
) -> dict[str, object]:
    _require_persistence_configured()
    return _staff_review_summary_payload(_get_case_repository().staff_review_summary())


def _case_database_url() -> str | None:
    return os.environ.get("CIVICINSPECT_CASE_DB_URL")


def _get_case_repository() -> InspectionCaseRepository:
    global _case_db_url, _case_repository
    db_url = _case_database_url()
    if db_url is None:
        raise RuntimeError("CIVICINSPECT_CASE_DB_URL is not configured.")
    if _case_repository is None or db_url != _case_db_url:
        _dispose_case_repository()
        _case_db_url = db_url
        _case_repository = InspectionCaseRepository(db_url=db_url)
    return _case_repository


def _dispose_case_repository() -> None:
    global _case_repository
    if _case_repository is not None:
        _case_repository.engine.dispose()
        _case_repository = None


def _lookup_repeat_cases(*, property_reference: str, violation_type: str = ""):
    if _case_database_url() is None:
        return lookup_repeat_cases(property_reference=property_reference, violation_type=violation_type)
    return _get_case_repository().lookup_repeat_cases(
        property_reference=property_reference,
        violation_type=violation_type,
    )


def _stored_report_response(
    stored: StoredInspectionReport, *, staff_review: StaffReviewQueueItem | None = None
) -> dict[str, object]:
    return {
        "report_id": stored.report_id,
        "inspection_id": stored.inspection_id,
        "property_reference": stored.property_reference,
        "summary": stored.summary,
        "observation_bullets": list(stored.observation_bullets),
        "inspector_review_required": stored.inspector_review_required,
        "staff_review_id": staff_review.review_id if staff_review is not None else None,
        "disclaimer": stored.disclaimer,
        "created_at": stored.created_at.isoformat(),
    }


def _require_persistence_configured() -> None:
    if _case_database_url() is None:
        raise HTTPException(
            status_code=503,
            detail={
                "message": "Townlight Inspections staff review persistence is not configured.",
                "fix": "Set CIVICINSPECT_CASE_DB_URL before using staff review queue routes.",
            },
        )


def _staff_review_payload(item: StaffReviewQueueItem) -> dict[str, object]:
    return {
        "review_id": item.review_id,
        "report_id": item.report_id,
        "inspection_id": item.inspection_id,
        "property_reference": item.property_reference,
        "status": item.status,
        "reason": item.reason,
        "assigned_to": item.assigned_to,
        "resolution": item.resolution,
        "created_by": item.created_by,
        "created_at": item.created_at.isoformat(),
        "updated_at": item.updated_at.isoformat(),
        "visibility": item.visibility,
        "boundary": (
            "Staff review queues support inspection triage only; they do not issue findings, "
            "citations, fines, notices, schedules, or system-of-record updates."
        ),
    }


def _staff_review_summary_payload(summary: StaffReviewSummary) -> dict[str, object]:
    return {
        "total_items": summary.total_items,
        "by_status": summary.by_status,
        "open_items": summary.open_items,
        "generated_at": summary.generated_at.isoformat(),
        "visibility": summary.visibility,
    }
