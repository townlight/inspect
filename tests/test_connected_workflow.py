"""Affected invariants for installed inspection evidence and explicit review."""
import base64
import hashlib
import json

import pytest
from sqlalchemy import text

from civicinspect.connections import SourceUnavailable
from civicinspect.migrations import ready, source_engine, upgrade
from civicinspect.workflow_models import InspectionInput
from civicinspect.workflow_store import Conflict, InspectionRepository


@pytest.fixture
def repository(tmp_path):
    engine = source_engine("sqlite:///" + str(tmp_path / "inspections.db"))
    assert not ready(engine)
    upgrade(engine)
    upgrade(engine)
    assert ready(engine)
    source = {"source_id": "code:2", "title": "Fictional adopted Code", "version": "v2",
              "citation": "Fictional Code 2", "visibility": "public", "text": "Keep access clear."}
    source["sha256"] = hashlib.sha256(source["text"].encode()).hexdigest()
    available = [source]
    repo = InspectionRepository(engine, {"code": lambda **_kwargs: available})
    yield repo, source, available
    engine.dispose()


def draft(source, **changes):
    raw = b"PRIVATE original inspector observation"
    return InspectionInput.model_validate({"title": "Fictional access inspection",
        "property_reference": "PRIVATE fictional parcel", "inspection_reference": "fictional-1",
        "dataset_kind": "fictional", "inspector_notes": "PRIVATE notes",
        "photo_observations": ["PRIVATE inspector-entered photo description"],
        "voice_notes": "PRIVATE supplied transcript", "staff_notes": "PRIVATE staff note",
        "notice_draft": "PRIVATE notice draft, never issued",
        "evidence": [{"filename": "observation.txt", "description": "PRIVATE source",
            "media_type": "text/plain", "content_base64": base64.b64encode(raw).decode(),
            "sha256": hashlib.sha256(raw).hexdigest()}],
        "linked_sources": [{"source_id": source["source_id"], "expected_sha256": source["sha256"]}],
        **changes})


def test_durable_originals_review_repeat_lookup_and_exact_records_copy(repository):
    repo, source, _ = repository
    first = repo.save_case(draft(source), "inspector-1")
    case_id = first["entity_id"]
    reopened = InspectionRepository(repo.engine, repo.providers)
    current = reopened.get_case(case_id)
    assert current["payload"]["evidence"] == draft(source).model_dump()["evidence"]
    assert "0 related saved case(s)" in current["payload"]["report_draft"]["summary"]
    assert repo.repeat_cases(" private fictional parcel ")["items"][0]["entity_id"] == case_id
    assert repo.repeat_cases("unknown")["items"] == []
    with pytest.raises(ValueError, match="explicit staff review"):
        repo.packet(case_id, first["revision_id"], "records_copy", "inspector-1")
    reviewed = repo.save_case(draft(source, expected_revision=first["revision_id"],
        review_state="reviewed", review_notes="Inspected and reviewed, support only.",
        public_summary="Reviewed fictional access observation."), "reviewer-2", case_id)
    assert repo.get_case(case_id)["payload"]["reviewer_id"] == "reviewer-2"
    public = repo.packet(case_id, reviewed["revision_id"], "records_copy", "reviewer-2")
    private = repo.packet(case_id, reviewed["revision_id"], "staff_only", "reviewer-2")
    assert "PRIVATE" not in public["text"] and source["sha256"] in public["text"]
    assert "PRIVATE" in private["text"]
    assert repo.records_documents(source_id=private["source_id"]) == []
    assert repo.records_documents(source_id=public["source_id"])[0] == public
    assert hashlib.sha256(public["text"].encode()).hexdigest() == public["sha256"]
    assert len(repo.history(case_id)["revisions"]) == 2
    assert len(repo.history(case_id)["audit"]) == 4
    with pytest.raises(Conflict):
        repo.save_case(draft(source, expected_revision=first["revision_id"]), "inspector-1", case_id)
    edit = repo.save_case(draft(source, expected_revision=reviewed["revision_id"]), "inspector-1", case_id)
    assert edit["revision_id"] != reviewed["revision_id"]
    assert repo.get_case(case_id)["payload"]["reviewer_id"] is None
    assert repo.document(public["packet_id"])["sha256"] == public["sha256"]


def test_code_access_and_source_integrity_rechecked_without_cached_fallback(repository):
    repo, source, available = repository
    saved = repo.save_case(draft(source, review_state="reviewed", review_notes="Reviewed",
                                public_summary="Public"), "inspector")
    packet = repo.packet(saved["entity_id"], saved["revision_id"], "records_copy", "inspector")
    available.clear()
    assert repo.get_case(saved["entity_id"])["connection_error"]
    assert repo.records_documents(source_id=packet["source_id"]) == []
    with pytest.raises(SourceUnavailable):
        repo.document(packet["packet_id"])
    available.append({**source, "visibility": "restricted"})
    assert repo.records_documents(source_id=packet["source_id"]) == []
    available[0] = {**source, "text": "Changed without matching hash"}
    with pytest.raises(SourceUnavailable):
        repo.save_case(draft(source), "inspector")


def test_original_and_review_identity_validation_and_append_only_history(repository):
    repo, source, _ = repository
    bad = draft(source).model_dump()
    bad["evidence"][0]["sha256"] = "0" * 64
    with pytest.raises(ValueError, match="SHA256"):
        InspectionInput.model_validate(bad)
    with pytest.raises(ValueError):
        draft(source, reviewer_id="spoofed")
    with pytest.raises(ValueError):
        draft(source, review_state="reviewed", review_notes="")
    with pytest.raises(ValueError):
        draft(source, official_finding=True)
    repo.save_case(draft(source), "inspector")
    with pytest.raises(Exception, match="append-only"):
        with repo.engine.begin() as connection:
            connection.execute(text("UPDATE connected_revisions SET payload=:p"), {"p": json.dumps({})})
