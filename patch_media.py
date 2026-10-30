"""Patch Inspections so raw audio evidence is accepted and retained with provenance.

Two additive edits:

1. `workflow_models.py` — `Evidence.media_type` gains the raw-audio MIME types
   (the beta gap: evidence permits text/plain, image/jpeg, image/png,
   application/pdf only, so raw audio could not be preserved). The existing
   base64/size/SHA256 validation is unchanged, so audio originals get the same
   original-byte + hash retention that photos already had.
2. `main.py` — new routes for retained evidence + draft-only analysis.

Idempotent.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
models = ROOT / "civicinspect" / "workflow_models.py"
main = ROOT / "civicinspect" / "main.py"

# ---- 1. workflow_models.py: accept raw audio -------------------------------
text = models.read_text(encoding="utf-8")
OLD_MEDIA = '''    media_type: Literal["text/plain", "image/jpeg", "image/png", "application/pdf"]'''
NEW_MEDIA = '''    media_type: Literal["text/plain", "image/jpeg", "image/png", "image/webp",
                        "application/pdf", "audio/webm", "audio/ogg", "audio/wav",
                        "audio/mpeg", "audio/mp4"]'''
if NEW_MEDIA in text:
    print("workflow_models.py already patched")
else:
    assert OLD_MEDIA in text, "expected evidence media_type literal not found"
    text = text.replace(OLD_MEDIA, NEW_MEDIA, 1)
    OLD_BOUNDARY = '''    "inspection schedule, legal advice or system-of-record action. Photo observations "
    "and voice transcripts are supplied by staff; no automated image analysis or transcription."'''
    NEW_BOUNDARY = '''    "inspection schedule, legal advice or system-of-record action. Photo observations "
    "and voice transcripts supplied by staff remain authoritative; any automated "
    "description or transcript produced by a configured adapter is a review-required "
    "draft, and nothing is issued or enforced automatically."'''
    assert OLD_BOUNDARY in text, "expected boundary text not found"
    text = text.replace(OLD_BOUNDARY, NEW_BOUNDARY, 1)
    models.write_text(text, encoding="utf-8")
    print("workflow_models.py patched: raw audio evidence accepted")

# ---- 2. main.py: evidence + analysis routes --------------------------------
text = main.read_text(encoding="utf-8")
if "/evidence/retain" in text:
    print("main.py already patched")
    raise SystemExit(0)

OLD_IMPORTS = '''from civicinspect.integration_mocks import validate_inspection_context_mocks'''
NEW_IMPORTS = '''from civicinspect.integration_mocks import validate_inspection_context_mocks
from civicinspect.media_analysis import (
    EvidenceRejected,
    analyse_evidence,
    retain_evidence,
)'''
assert OLD_IMPORTS in text
text = text.replace(OLD_IMPORTS, NEW_IMPORTS, 1)

OLD_MODELS = '''class StaffReviewCreateRequest(BaseModel):'''
NEW_MODELS = '''class EvidenceItemRequest(BaseModel):
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


class StaffReviewCreateRequest(BaseModel):'''
assert OLD_MODELS in text
text = text.replace(OLD_MODELS, NEW_MODELS, 1)

OLD_ROUTES = '''@app.post("/api/v1/civicinspect/notices/draft")'''
NEW_ROUTES = '''def _retain_all(items) -> list:
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

    raw = os.environ.get("CIVICINSPECT_PUBLIC_SOURCES", "").strip()
    if not raw:
        return {}
    import json
    import hashlib
    from pathlib import Path as _Path
    try:
        payload = json.loads(_Path(raw).read_text(encoding="utf-8"))
    except Exception:
        raise HTTPException(
            status_code=503,
            detail={"message": "Configured inspection Code sources could not be read.",
                    "fix": "Check CIVICINSPECT_PUBLIC_SOURCES."},
        ) from None
    rows = payload.get("sources", []) if isinstance(payload, dict) else payload
    sources = []
    for row in rows:
        text = str(row["text"])
        sources.append({"provider": "code", "source_id": str(row["source_id"]),
                        "version": row.get("version", "1"),
                        "title": str(row.get("title", row["source_id"])),
                        "citation": str(row.get("citation", row.get("title", row["source_id"]))),
                        "text": text, "visibility": str(row.get("visibility", "public")),
                        "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest()})
    return {"code": lambda *, source_id=None, query=None: (
        [dict(r) for r in sources if r["source_id"] == source_id] if source_id is not None
        else [])}


def _vision_provider():
    name = os.environ.get("CIVICINSPECT_VISION_PROVIDER", "").strip()
    if not name:
        return None, None
    from civiccore.llm.factory import build_provider
    from civiccore.llm.providers.config import AnthropicConfig, OllamaConfig, OpenAIConfig
    schemas = {"ollama": OllamaConfig, "openai": OpenAIConfig, "anthropic": AnthropicConfig}
    schema = schemas.get(name)
    if schema is None:
        raise HTTPException(
            status_code=503,
            detail={"message": f"Configured inspection vision provider '{name}' is not supported.",
                    "fix": "Set CIVICINSPECT_VISION_PROVIDER to ollama, openai or anthropic."},
        )
    model = os.environ.get("CIVICINSPECT_VISION_MODEL") or None
    return build_provider(name, schema()), model


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
        model=model,
        inspector_supplied_text=request.inspector_supplied_text,
    )
    return result.to_payload()


@app.post("/api/v1/civicinspect/notices/draft")'''
assert OLD_ROUTES in text
text = text.replace(OLD_ROUTES, NEW_ROUTES, 1)

main.write_text(text, encoding="utf-8")
print("main.py patched: evidence retention + draft media analysis routes")
