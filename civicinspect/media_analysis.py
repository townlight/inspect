"""Draft-only media analysis for retained inspection evidence.

Scope (outputs/Townlight-Minimum-Beta-Scope-Audit-2026-10-27.md §2.4):

* raw evidence is retained as original bytes with a SHA-256 that is re-verified
  on retention, and audio MIME types are now accepted;
* a local adapter may turn a photo or a voice memo into *draft* observations
  that carry the required cited code sections;
* the draft is always inspector-review-required and never issues, files, fines,
  or enforces anything;
* whatever actually ran is named in the result (``runtime``), and a missing
  adapter is reported as unavailable rather than simulated.

Reuse note: the owned CivicCast/TownReporter/TextFlowKit code is not importable
from this workspace (the only local references are a docstring citation and a
docs page in Core), so nothing here claims to reuse it. The image/vision path
reuses the owned ``civiccore`` provider adapter, which already supports
multimodal input.
"""

from __future__ import annotations

import base64
import hashlib
from dataclasses import dataclass, field
from typing import Any, Mapping, Protocol, Sequence

from civicinspect.connections import SourceUnavailable, resolve
from civicinspect.transcription import TranscriptionUnavailable


BOUNDARY = (
    "Draft workpaper only. Inspector review is required before any notice, "
    "citation, fine, legal finding, inspection schedule or system-of-record "
    "action. Nothing is issued or enforced automatically."
)

MAX_EVIDENCE_BYTES = 10_000_000

#: Raw audio is retained as original bytes; the MIME set is what the container
#: browsers and phones actually record.
AUDIO_MEDIA_TYPES = ("audio/webm", "audio/ogg", "audio/wav", "audio/mpeg", "audio/mp4")
IMAGE_MEDIA_TYPES = ("image/jpeg", "image/png", "image/webp")
TEXT_MEDIA_TYPES = ("text/plain",)
DOCUMENT_MEDIA_TYPES = ("application/pdf",)
SUPPORTED_MEDIA_TYPES = (TEXT_MEDIA_TYPES + IMAGE_MEDIA_TYPES + AUDIO_MEDIA_TYPES
                         + DOCUMENT_MEDIA_TYPES)


class EvidenceRejected(ValueError):
    """The supplied evidence cannot be retained as-is."""


@dataclass(frozen=True)
class RetainedEvidence:
    """Original evidence bytes with their verified digest and provenance."""

    filename: str
    media_type: str
    description: str
    size_bytes: int
    sha256: str
    raw: bytes = field(repr=False)

    def as_record(self) -> dict[str, Any]:
        """Provenance record: bytes are not echoed back, the digest is."""

        return {"filename": self.filename, "media_type": self.media_type,
                "description": self.description, "size_bytes": self.size_bytes,
                "sha256": self.sha256, "kind": _kind(self.media_type),
                "original_bytes_retained": True}


def _kind(media_type: str) -> str:
    if media_type in AUDIO_MEDIA_TYPES:
        return "audio"
    if media_type in IMAGE_MEDIA_TYPES:
        return "image"
    if media_type in TEXT_MEDIA_TYPES:
        return "text"
    if media_type in DOCUMENT_MEDIA_TYPES:
        return "document"
    return "unknown"


def retain_evidence(*, filename: str, media_type: str, description: str,
                    content_base64: str, expected_sha256: str) -> RetainedEvidence:
    """Decode, bound-check and hash original bytes; reject any mismatch."""

    if media_type not in SUPPORTED_MEDIA_TYPES:
        raise EvidenceRejected(
            f"Unsupported media type '{media_type}'. Accepted: {', '.join(SUPPORTED_MEDIA_TYPES)}.")
    try:
        raw = base64.b64decode(content_base64, validate=True)
    except Exception:
        raise EvidenceRejected("Evidence must contain valid base64 original bytes.") from None
    if not raw:
        raise EvidenceRejected("Evidence original bytes are empty.")
    if len(raw) > MAX_EVIDENCE_BYTES:
        raise EvidenceRejected(
            f"Evidence original is {len(raw)} bytes; the limit is {MAX_EVIDENCE_BYTES}.")
    digest = hashlib.sha256(raw).hexdigest()
    if digest != expected_sha256:
        raise EvidenceRejected("Evidence original SHA256 does not match the supplied bytes.")
    return RetainedEvidence(filename=filename, media_type=media_type,
                            description=description, size_bytes=len(raw),
                            sha256=digest, raw=raw)


class VisionProvider(Protocol):
    """The owned civiccore provider shape (multimodal generate)."""

    name: str
    supports_images: bool

    async def generate(self, *, system_prompt: str, user_content: str,
                       model: str | None = None, chunks: list[str] | None = None,
                       images: list[str] | None = None, **kwargs: Any) -> str: ...


class TranscriptionProvider(Protocol):
    """Adapter that turns retained audio bytes into text."""

    name: str

    async def transcribe(self, *, raw: bytes, media_type: str) -> str: ...


SYSTEM_PROMPT = (
    "You are assisting a municipal code inspector. Describe only what is visible "
    "in the attached photo in neutral, factual language suitable for a draft "
    "workpaper. Do not state a legal finding, do not say a violation occurred, do "
    "not mention fines or deadlines, and do not cite a code section that is not "
    "present in the supplied excerpts."
)


@dataclass
class MediaAnalysis:
    """Result of a draft-only analysis pass."""

    draft_observations: list[dict[str, Any]] = field(default_factory=list)
    cited_sections: list[dict[str, str]] = field(default_factory=list)
    unavailable: list[dict[str, str]] = field(default_factory=list)
    retained: list[dict[str, Any]] = field(default_factory=list)
    runtime: dict[str, Any] = field(default_factory=dict)
    review_required: bool = True
    determination_made: bool = False
    boundary: str = BOUNDARY

    def to_payload(self) -> dict[str, Any]:
        return {"draft_observations": self.draft_observations,
                "cited_sections": self.cited_sections,
                "unavailable": self.unavailable,
                "retained_evidence": self.retained,
                "runtime": self.runtime,
                "inspector_review_required": self.review_required,
                "determination_made": self.determination_made,
                "boundary": self.boundary}


def _resolve_citations(providers: Mapping[str, Any],
                       links: Sequence[Mapping[str, str]]) -> tuple[list[dict[str, str]],
                                                                     list[dict[str, str]]]:
    cited: list[dict[str, str]] = []
    missing: list[dict[str, str]] = []
    for link in links:
        try:
            source = resolve(providers, dict(link))
        except SourceUnavailable:
            missing.append({"source_id": str(link.get("source_id")),
                            "reason": "cited code source did not resolve, so no section "
                                      "is quoted in the draft"})
            continue
        cited.append({"source_id": source["source_id"], "citation": source["citation"],
                      "title": source["title"], "version": str(source["version"]),
                      "text": source["text"]})
    return cited, missing


async def analyse_evidence(
    *,
    evidence: Sequence[RetainedEvidence],
    code_links: Sequence[Mapping[str, str]] = (),
    providers: Mapping[str, Any] | None = None,
    vision_provider: VisionProvider | None = None,
    transcription_provider: TranscriptionProvider | None = None,
    model: str | None = None,
    inspector_supplied_text: str = "",
) -> MediaAnalysis:
    """Analyse retained evidence into draft observations; never decides anything."""

    result = MediaAnalysis()
    result.retained = [item.as_record() for item in evidence]
    cited, missing = _resolve_citations(providers or {}, code_links)
    result.cited_sections = cited
    result.unavailable.extend(missing)

    if inspector_supplied_text.strip():
        result.draft_observations.append(
            {"source": "inspector_supplied_text",
             "text": inspector_supplied_text.strip(),
             "citation_source_ids": [item["source_id"] for item in cited]})

    ran: list[dict[str, Any]] = []
    for item in evidence:
        kind = _kind(item.media_type)
        if kind == "image":
            if vision_provider is None:
                result.unavailable.append(
                    {"item": item.filename,
                     "reason": "no vision adapter is configured, so no automatic "
                               "description was produced; the photo is retained for "
                               "inspector review"})
                continue
            if not getattr(vision_provider, "supports_images", False):
                result.unavailable.append(
                    {"item": item.filename,
                     "reason": f"configured adapter '{getattr(vision_provider, 'name', 'unknown')}' "
                               "does not support images; no description was produced"})
                continue
            image_b64 = base64.b64encode(item.raw).decode("ascii")
            payload = (f"Photo description supplied by staff: {item.description}\n"
                       f"Cited code excerpts:\n" +
                       "\n".join(f"[{i}] {c['citation']}: {c['text']}"
                                 for i, c in enumerate(cited, start=1)))
            try:
                text = await vision_provider.generate(
                    system_prompt=SYSTEM_PROMPT, user_content=payload,
                    model=model, images=[image_b64])
            except Exception as exc:
                result.unavailable.append(
                    {"item": item.filename,
                     "reason": f"vision adapter failed ({type(exc).__name__}); the photo is "
                               "retained and no description is invented"})
                continue
            if not text or not text.strip():
                result.unavailable.append(
                    {"item": item.filename,
                     "reason": "vision adapter returned no text; nothing is invented"})
                continue
            ran.append({"adapter": getattr(vision_provider, "name", "unknown"),
                        "model": model, "media_type": item.media_type,
                        "filename": item.filename, "mode": "image-description"})
            result.draft_observations.append(
                {"source": "vision_adapter", "filename": item.filename,
                 "media_type": item.media_type, "text": text.strip(),
                 "citation_source_ids": [c["source_id"] for c in cited],
                 "adapter": getattr(vision_provider, "name", "unknown")})
        elif kind == "audio":
            if transcription_provider is None:
                result.unavailable.append(
                    {"item": item.filename,
                     "reason": "the audio original is retained with its SHA-256 but no "
                               "transcription adapter is configured, so no transcript "
                               "was produced and none is invented"})
                continue
            try:
                text = await transcription_provider.transcribe(raw=item.raw,
                                                               media_type=item.media_type)
            except TranscriptionUnavailable as exc:
                result.unavailable.append(
                    {"item": item.filename,
                     "reason": f"no transcription runtime is usable here ({exc}); the "
                               "audio original is retained with its SHA-256 and no "
                               "transcript is invented"})
                continue
            except Exception as exc:
                result.unavailable.append(
                    {"item": item.filename,
                     "reason": f"transcription adapter failed ({type(exc).__name__}); the "
                               "audio original is retained"})
                continue
            if not text or not text.strip():
                result.unavailable.append(
                    {"item": item.filename,
                     "reason": "transcription adapter returned no text; nothing is invented"})
                continue
            detail = getattr(transcription_provider, "last_result", None) or {}
            ran.append({"adapter": getattr(transcription_provider, "name", "unknown"),
                        "model": detail.get("model"),
                        "engine": detail.get("engine") or detail.get("engine_class"),
                        "device": detail.get("device"),
                        "decoded_by": detail.get("decoded_by"),
                        "segments": len(detail.get("segments") or []),
                        "media_type": item.media_type,
                        "filename": item.filename, "mode": "audio-transcription"})
            result.draft_observations.append(
                {"source": "transcription_adapter", "filename": item.filename,
                 "media_type": item.media_type, "text": text.strip(),
                 "citation_source_ids": [c["source_id"] for c in cited],
                 "adapter": getattr(transcription_provider, "name", "unknown")})

    if ran:
        result.runtime = {"executed": True, "runs": ran,
                          "note": "text produced by the named adapter; inspector review "
                                  "is still required before any notice or action"}
    else:
        result.runtime = {"executed": False,
                          "runs": [],
                          "note": "no media adapter executed; evidence is retained and "
                                  "the draft contains only staff-supplied text"}
    return result
