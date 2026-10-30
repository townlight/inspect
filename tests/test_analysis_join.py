# SPDX-License-Identifier: AGPL-3.0-only
"""F-01: analysed observations and resolved citations reach the SAME saved draft.

The audit finding was that ``media/analyse`` returned real observations and
citations while the saved case's ``report_draft`` carried neither. These checks
join those halves without adding a parallel case system: the analysis is a field
of the existing ``InspectionInput`` payload and travels the existing
revision/packet path.
"""
import base64
import hashlib
import json

import pytest

from civicinspect.media_analysis import analyse_evidence, retain_evidence
from civicinspect.migrations import ready, source_engine, upgrade
from civicinspect.workflow_models import AnalysisRecord, InspectionInput
from civicinspect.workflow_store import InspectionRepository

TEXT = "Synthetic Code 4.2: pallets must not block the sidewalk."
SOURCE = {"source_id": "code:4.2", "title": "Synthetic sidewalk section",
          "version": "v3", "citation": "Synthetic Code 4.2", "visibility": "public",
          "text": TEXT, "sha256": hashlib.sha256(TEXT.encode()).hexdigest()}
PROVIDERS = {"code": lambda *, source_id=None, query=None: (
    [dict(SOURCE)] if source_id == "code:4.2" else [])}
PHOTO = b"\x89PNG\r\n\x1a\n" + b"synthetic-photo-bytes" * 4
AUDIO = b"RIFF\x00\x00\x00\x00WAVEfmt " + b"synthetic-voice-bytes" * 4


class Vision:
    name = "synthetic-vision"
    supports_images = True

    async def generate(self, *, system_prompt, user_content, model=None, chunks=None,
                       images=None, **kwargs):
        return "A pallet stands across the sidewalk edge."


class Transcriber:
    name = "synthetic-transcriber"

    async def transcribe(self, *, raw, media_type):
        return "Pallet has been there since Tuesday."


def retained():
    return [retain_evidence(filename="photo.png", media_type="image/png",
                            description="sidewalk", content_base64=base64.b64encode(PHOTO).decode(),
                            expected_sha256=hashlib.sha256(PHOTO).hexdigest()),
            retain_evidence(filename="voice.wav", media_type="audio/wav",
                            description="voice memo", content_base64=base64.b64encode(AUDIO).decode(),
                            expected_sha256=hashlib.sha256(AUDIO).hexdigest())]


@pytest.fixture
def repository(tmp_path):
    engine = source_engine("sqlite:///" + str(tmp_path / "inspections.db"))
    assert not ready(engine)
    upgrade(engine)
    assert ready(engine)
    available = [dict(SOURCE)]
    repo = InspectionRepository(engine, {"code": lambda **kwargs: (
        [dict(r) for r in available if kwargs.get("source_id") == r["source_id"]])})
    yield repo, available
    engine.dispose()


async def analysis_record():
    result = await analyse_evidence(evidence=retained(), providers=PROVIDERS,
                                    code_links=[{"provider": "code", "source_id": "code:4.2",
                                                 "expected_sha256": SOURCE["sha256"]}],
                                    vision_provider=Vision(), transcription_provider=Transcriber(),
                                    inspector_supplied_text="Pallet on sidewalk.")
    return result


def case_payload(analysis, **changes):
    return InspectionInput.model_validate({
        "title": "Synthetic access inspection", "property_reference": "synthetic parcel",
        "inspection_reference": "syn-1", "dataset_kind": "fictional",
        "inspector_notes": "Observed from the sidewalk.",
        "photo_observations": [], "voice_notes": "",
        "evidence": [{"filename": item.filename, "description": item.description,
                      "media_type": item.media_type,
                      "content_base64": base64.b64encode(item.raw).decode(),
                      "sha256": item.sha256} for item in retained()],
        "linked_sources": [{"source_id": SOURCE["source_id"],
                            "expected_sha256": SOURCE["sha256"]}],
        "analysis": AnalysisRecord.from_media_analysis(analysis.to_payload()).model_dump(mode="json"),
        **changes})


def test_analysis_survives_into_the_same_saved_draft_and_staff_packet(repository):
    repo, available = repository
    import asyncio
    result = asyncio.run(analysis_record())
    assert result.runtime["executed"] is True
    assert [o["source"] for o in result.draft_observations] == [
        "inspector_supplied_text", "vision_adapter", "transcription_adapter"]

    payload = case_payload(result)
    assert payload.analysis is not None
    first = repo.save_case(payload, "inspector-1")

    # Read back from a fresh repository instance (restart equivalence).
    reopened = InspectionRepository(repo.engine, repo.providers).get_case(first["entity_id"])
    saved = reopened["payload"]
    assert saved["analysis"]["cited_sections"][0]["source_id"] == "code:4.2"
    assert "Synthetic Code 4.2 (code:4.2)" in saved["report_draft"]["cited_sections"]
    joined = " ".join(saved["report_draft"]["observations"])
    assert "A pallet stands across the sidewalk edge." in joined
    assert "Pallet has been there since Tuesday." in joined
    for item in retained():
        assert item.sha256 in {e["sha256"] for e in saved["evidence"]}

    reviewed = repo.save_case(case_payload(result, expected_revision=first["revision_id"],
        review_state="reviewed", review_notes="Reviewed the photo and voice memo.",
        public_summary="Reviewed synthetic sidewalk observation."), "reviewer-2",
        first["entity_id"])
    packet = repo.packet(first["entity_id"], reviewed["revision_id"], "staff_only", "reviewer-2")
    body = json.loads(packet["text"])
    verified = body["staff_inspection"]["analysis"]
    assert verified["cited_sections"][0]["text"] == TEXT
    assert verified["observations"] and verified["review_required"] is True
    assert body["staff_inspection"]["report_draft"]["analysis"] == verified
    assert "A pallet stands across the sidewalk edge." in json.dumps(body)
    records = repo.packet(first["entity_id"], reviewed["revision_id"], "records_copy",
                          "reviewer-2")
    body_records = json.loads(records["text"])
    assert "analysis" not in body_records and "staff_inspection" not in body_records
    assert "A pallet stands across the sidewalk edge." not in records["text"]
    assert "since Tuesday" not in records["text"]
    for item in retained():
        assert item.sha256 not in records["text"]
    assert body_records["public_summary"] == "Reviewed synthetic sidewalk observation."

    # A restricted source cannot be cited in an exported packet.
    available.clear()
    with pytest.raises(Exception):
        repo.packet(first["entity_id"], reviewed["revision_id"], "staff_only", "reviewer-2")


def test_analysis_cannot_cite_a_section_the_case_did_not_select():
    import asyncio
    result = asyncio.run(analysis_record())
    data = case_payload(result).model_dump(mode="json")
    data["linked_sources"] = []
    with pytest.raises(ValueError, match="Cite only the Code sources selected"):
        InspectionInput.model_validate(data)


def test_analysis_observation_must_cite_a_resolved_section():
    with pytest.raises(ValueError, match="cites a section that was not resolved"):
        AnalysisRecord.model_validate({"observations": [
            {"source": "vision_adapter", "text": "Pallet on the walk.",
             "citation_source_ids": ["code:9.9"]}], "cited_sections": []})
    with pytest.raises(ValueError, match="always review-required"):
        AnalysisRecord.model_validate({"review_required": False})
