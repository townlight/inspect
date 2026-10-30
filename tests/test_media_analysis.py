"""Raw audio retention and draft-only photo/audio analysis for Inspections.

Beta outcome (outputs/Townlight-Minimum-Beta-Scope-Audit-2026-10-27.md §2.4):
synthetic image and audio evidence is retained with original bytes and SHA-256;
a local adapter may produce a review-required draft with cited code sections; the
text path is unchanged; nothing is issued, filed, fined or enforced.

The adapters used here are explicit stubs; every test that needs a real adapter
labels it as such, and the analysis result always says what actually ran.
"""
from __future__ import annotations

import asyncio
import base64
import hashlib
import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from civicinspect import main as inspect_main
from civicinspect.media_analysis import (
    EvidenceRejected,
    analyse_evidence,
    retain_evidence,
)

FIXTURES = Path(__file__).parent / "fixtures"
DIGESTS = json.loads((FIXTURES / "media-digests.json").read_text(encoding="utf-8"))
PHOTO = (FIXTURES / "inspection-photo.png").read_bytes()
VOICE = (FIXTURES / "inspection-voice.wav").read_bytes()


def _b64(raw: bytes) -> str:
    return base64.b64encode(raw).decode("ascii")


def _code_provider():
    text = "Fictional Code 4.12: property owners must keep the right-of-way clear of obstructions."
    source = {"provider": "code", "source_id": "code:4.12",
              "version": "2026.1", "title": "Fictional Code 4.12",
              "citation": "Fictional Code 4.12", "text": text, "visibility": "public",
              "sha256": hashlib.sha256(text.encode()).hexdigest()}
    return {"code": lambda *, source_id=None, query=None: (
        [source] if source_id in (None, "code:4.12") else [])}, source


def _link():
    text = "Fictional Code 4.12: property owners must keep the right-of-way clear of obstructions."
    return {"provider": "code", "source_id": "code:4.12",
            "expected_sha256": hashlib.sha256(text.encode()).hexdigest()}


class StubVision:
    """Named stub: cannot be mistaken for a live model."""

    name = "test-stub-vision"
    supports_images = True

    def __init__(self, *, text="Draft: a pallet blocks part of the sidewalk.",
                 raises: Exception | None = None):
        self.text = text
        self.raises = raises
        self.calls: list[dict] = []

    async def generate(self, *, system_prompt, user_content, model=None, chunks=None,
                       images=None, **kwargs):
        self.calls.append({"model": model, "images": images, "user_content": user_content})
        if self.raises is not None:
            raise self.raises
        return self.text


class StubTranscriber:
    name = "test-stub-transcriber"

    def __init__(self, *, text="Draft: inspector said the pallet was still there.",
                 raises: Exception | None = None):
        self.text = text
        self.raises = raises
        self.calls: list[dict] = []

    async def transcribe(self, *, raw, media_type):
        self.calls.append({"bytes": len(raw), "media_type": media_type,
                           "sha256": hashlib.sha256(raw).hexdigest()})
        if self.raises is not None:
            raise self.raises
        return self.text


# --------------------------------------------------------------------------
# retention
# --------------------------------------------------------------------------

def test_raw_audio_is_retained_with_original_bytes_and_hash():
    retained = retain_evidence(filename="inspection-voice.wav", media_type="audio/wav",
                               description="Field voice memo",
                               content_base64=_b64(VOICE),
                               expected_sha256=DIGESTS["inspection-voice.wav"]["sha256"])
    assert retained.raw == VOICE
    assert retained.size_bytes == len(VOICE)
    assert retained.sha256 == DIGESTS["inspection-voice.wav"]["sha256"]
    record = retained.as_record()
    assert record["kind"] == "audio"
    assert record["original_bytes_retained"] is True
    assert "raw" not in record  # provenance record does not dump the bytes


def test_photo_retention_and_digest_mismatch_is_rejected():
    retained = retain_evidence(filename="inspection-photo.png", media_type="image/png",
                               description="Sidewalk photo",
                               content_base64=_b64(PHOTO),
                               expected_sha256=DIGESTS["inspection-photo.png"]["sha256"])
    assert retained.raw == PHOTO and retained.as_record()["kind"] == "image"

    with pytest.raises(EvidenceRejected) as error:
        retain_evidence(filename="inspection-photo.png", media_type="image/png",
                        description="Sidewalk photo", content_base64=_b64(PHOTO),
                        expected_sha256="0" * 64)
    assert "SHA256" in str(error.value)


def test_unsupported_media_type_is_rejected():
    with pytest.raises(EvidenceRejected) as error:
        retain_evidence(filename="clip.mp4", media_type="video/mp4", description="",
                        content_base64=_b64(b"nope"), expected_sha256="0" * 64)
    assert "Unsupported media type" in str(error.value)


def test_workflow_evidence_model_accepts_raw_audio_and_rejects_bad_hash():
    from civicinspect.workflow_models import Evidence

    valid = Evidence.model_validate({
        "filename": "voice.wav", "description": "Raw audio", "media_type": "audio/wav",
        "content_base64": _b64(VOICE),
        "sha256": DIGESTS["inspection-voice.wav"]["sha256"]})
    assert valid.media_type == "audio/wav"

    with pytest.raises(Exception):
        Evidence.model_validate({
            "filename": "voice.wav", "description": "Raw audio", "media_type": "audio/wav",
            "content_base64": _b64(VOICE), "sha256": "0" * 64})


# --------------------------------------------------------------------------
# analysis
# --------------------------------------------------------------------------

def _evidence_bundle():
    return [
        retain_evidence(filename="inspection-photo.png", media_type="image/png",
                        description="Sidewalk obstruction",
                        content_base64=_b64(PHOTO),
                        expected_sha256=DIGESTS["inspection-photo.png"]["sha256"]),
        retain_evidence(filename="inspection-voice.wav", media_type="audio/wav",
                        description="Field voice memo",
                        content_base64=_b64(VOICE),
                        expected_sha256=DIGESTS["inspection-voice.wav"]["sha256"]),
    ]


def test_no_adapters_means_evidence_retained_and_nothing_invented():
    providers, _ = _code_provider()
    result = asyncio.run(analyse_evidence(evidence=_evidence_bundle(),
                                          code_links=[_link()], providers=providers))
    payload = result.to_payload()
    assert payload["inspector_review_required"] is True
    assert payload["determination_made"] is False
    assert payload["runtime"]["executed"] is False
    assert len(payload["retained_evidence"]) == 2
    assert {item["kind"] for item in payload["retained_evidence"]} == {"image", "audio"}
    assert [item["citation"] for item in payload["cited_sections"]] == ["Fictional Code 4.12"]
    reasons = " ".join(item["reason"] for item in payload["unavailable"])
    assert "no vision adapter" in reasons
    assert "no transcription adapter" in reasons
    assert payload["draft_observations"] == []


def test_stub_adapters_execute_and_are_named_with_citations():
    providers, _ = _code_provider()
    vision, transcriber = StubVision(), StubTranscriber()
    result = asyncio.run(analyse_evidence(
        evidence=_evidence_bundle(), code_links=[_link()], providers=providers,
        vision_provider=vision, transcription_provider=transcriber, model="stub-vision-1"))
    payload = result.to_payload()
    assert payload["runtime"]["executed"] is True
    adapters = {run["adapter"] for run in payload["runtime"]["runs"]}
    assert adapters == {"test-stub-vision", "test-stub-transcriber"}
    # the real image bytes and the real audio bytes reached the adapters
    assert vision.calls and vision.calls[0]["images"] == [_b64(PHOTO)]
    assert transcriber.calls[0]["sha256"] == DIGESTS["inspection-voice.wav"]["sha256"]
    assert transcriber.calls[0]["media_type"] == "audio/wav"
    # each draft observation points at the cited section, and stays review-required
    for observation in payload["draft_observations"]:
        assert observation["citation_source_ids"] == ["code:4.12"]
    assert payload["inspector_review_required"] is True
    assert payload["determination_made"] is False
    for observation in payload["draft_observations"]:
        text = observation["text"].casefold()
        for forbidden in ("violation occurred", "fine", "penalty", "must comply within"):
            assert forbidden not in text


def test_adapter_failures_are_reported_not_hidden():
    providers, _ = _code_provider()
    result = asyncio.run(analyse_evidence(
        evidence=_evidence_bundle(), code_links=[_link()], providers=providers,
        vision_provider=StubVision(raises=RuntimeError("daemon down")),
        transcription_provider=StubTranscriber(text="  ")))
    payload = result.to_payload()
    assert payload["runtime"]["executed"] is False
    reasons = " ".join(item["reason"] for item in payload["unavailable"])
    assert "RuntimeError" in reasons
    assert "returned no text" in reasons
    assert payload["draft_observations"] == []
    assert len(payload["retained_evidence"]) == 2


def test_unresolvable_code_citation_is_reported_and_not_quoted():
    providers, _ = _code_provider()
    bad = dict(_link())
    bad["expected_sha256"] = "1" * 64
    result = asyncio.run(analyse_evidence(
        evidence=_evidence_bundle()[:1], code_links=[bad], providers=providers,
        vision_provider=StubVision()))
    payload = result.to_payload()
    assert payload["cited_sections"] == []
    assert any("did not resolve" in item["reason"] for item in payload["unavailable"])
    assert payload["draft_observations"][0]["citation_source_ids"] == []


def test_inspector_supplied_text_path_is_preserved():
    providers, _ = _code_provider()
    result = asyncio.run(analyse_evidence(
        evidence=[], code_links=[_link()], providers=providers,
        inspector_supplied_text="Pallet on sidewalk, still present."))
    payload = result.to_payload()
    assert payload["draft_observations"][0]["source"] == "inspector_supplied_text"
    assert payload["runtime"]["executed"] is False


# --------------------------------------------------------------------------
# API routes
# --------------------------------------------------------------------------

@pytest.fixture
def client(monkeypatch):
    monkeypatch.delenv("CIVICINSPECT_CASE_DB_URL", raising=False)
    monkeypatch.delenv("CIVICINSPECT_VISION_PROVIDER", raising=False)
    monkeypatch.delenv("CIVICINSPECT_PUBLIC_SOURCES", raising=False)
    with TestClient(inspect_main.app) as test_client:
        yield test_client


def test_api_retains_raw_audio_and_photo_with_hashes(client):
    response = client.post("/api/v1/civicinspect/evidence/retain", json={"items": [
        {"filename": "inspection-voice.wav", "media_type": "audio/wav",
         "description": "Field voice memo", "content_base64": _b64(VOICE),
         "sha256": DIGESTS["inspection-voice.wav"]["sha256"]},
        {"filename": "inspection-photo.png", "media_type": "image/png",
         "description": "Sidewalk", "content_base64": _b64(PHOTO),
         "sha256": DIGESTS["inspection-photo.png"]["sha256"]},
    ]})
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["count"] == 2 and body["raw_audio_retained"] is True
    hashes = {item["filename"]: item["sha256"] for item in body["retained_evidence"]}
    assert hashes["inspection-voice.wav"] == DIGESTS["inspection-voice.wav"]["sha256"]
    assert "not a finding" in body["disclaimer"]


def test_api_rejects_tampered_evidence_actionably(client):
    response = client.post("/api/v1/civicinspect/evidence/retain", json={"items": [
        {"filename": "inspection-voice.wav", "media_type": "audio/wav",
         "description": "Field voice memo", "content_base64": _b64(VOICE),
         "sha256": "0" * 64}]})
    assert response.status_code == 422
    detail = response.json()["detail"]
    assert "was not retained" in detail["message"]
    assert "SHA256" in detail["fix"]


def test_api_analysis_without_adapters_is_explicitly_review_required(client):
    response = client.post("/api/v1/civicinspect/media/analyse", json={"items": [
        {"filename": "inspection-photo.png", "media_type": "image/png",
         "description": "Sidewalk", "content_base64": _b64(PHOTO),
         "sha256": DIGESTS["inspection-photo.png"]["sha256"]},
        {"filename": "inspection-voice.wav", "media_type": "audio/wav",
         "description": "Voice memo", "content_base64": _b64(VOICE),
         "sha256": DIGESTS["inspection-voice.wav"]["sha256"]},
    ]})
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["inspector_review_required"] is True
    assert body["determination_made"] is False
    assert body["runtime"]["executed"] is False
    assert len(body["retained_evidence"]) == 2
    assert body["boundary"].startswith("Draft workpaper only")


def test_api_rejects_unsupported_vision_provider(monkeypatch):
    monkeypatch.setenv("CIVICINSPECT_VISION_PROVIDER", "not-a-provider")
    with TestClient(inspect_main.app) as test_client:
        response = test_client.post("/api/v1/civicinspect/media/analyse", json={"items": [
            {"filename": "inspection-photo.png", "media_type": "image/png",
             "description": "Sidewalk", "content_base64": _b64(PHOTO),
             "sha256": DIGESTS["inspection-photo.png"]["sha256"]}]})
    assert response.status_code == 503
    assert "not supported" in response.json()["detail"]["message"]


def test_existing_reports_draft_route_still_works_with_supplied_text(client):
    response = client.post("/api/v1/civicinspect/reports/draft", json={
        "inspection_id": "fictional-1", "property_reference": "fictional parcel",
        "inspector_notes": "Observed a pallet on the sidewalk.",
        "photo_observations": ["Pallet blocking half the walkway."],
        "voice_notes": "Inspector says it was present last week too."})
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["inspector_review_required"] is True
    assert body["observation_bullets"]
