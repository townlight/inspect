from fastapi.testclient import TestClient

import townlight_inspections.main as main_module
from townlight_inspections.main import app
from townlight_inspections.persistence import InspectionCaseRepository


client = TestClient(app)


def test_case_and_report_records_persist(tmp_path) -> None:
    db_path = tmp_path / "case-records.db"
    repository = InspectionCaseRepository(db_url=f"sqlite:///{db_path}")

    repeat = repository.lookup_repeat_cases(property_reference="100 Main Street", violation_type="nuisance")
    stored = repository.create_report(
        inspection_id="insp-100",
        property_reference="100 Main Street",
        inspector_notes="Overgrown vegetation observed.",
        photo_observations=("Photo shows rear alley condition.",),
        voice_notes="Follow-up needed.",
    )
    repository.engine.dispose()

    second_repository = InspectionCaseRepository(db_url=f"sqlite:///{db_path}", seed_defaults=False)
    try:
        reloaded_repeat = second_repository.lookup_repeat_cases(property_reference="100 Main Street")
        reloaded_report = second_repository.get_report(stored.report_id)
    finally:
        second_repository.engine.dispose()

    assert reloaded_repeat.related_case_ids == repeat.related_case_ids
    assert reloaded_report is not None
    assert reloaded_report.inspection_id == "insp-100"
    assert reloaded_report.inspector_review_required is True
    db_path.unlink(missing_ok=True)


def test_api_uses_configured_case_database(monkeypatch, tmp_path) -> None:
    db_path = tmp_path / "api-case-records.db"
    monkeypatch.setenv("TOWNLIGHT_INSPECTIONS_CASE_DB_URL", f"sqlite:///{db_path}")

    try:
        repeat_response = client.post(
            "/api/v1/townlight_inspections/cases/repeat-lookup",
            json={"property_reference": "100 Main Street", "violation_type": "nuisance"},
        )
        create_response = client.post(
            "/api/v1/townlight_inspections/reports/draft",
            json={
                "inspection_id": "insp-100",
                "property_reference": "100 Main Street",
                "inspector_notes": "Overgrown vegetation observed.",
                "photo_observations": ["Photo shows rear alley condition."],
                "voice_notes": "Follow-up needed.",
            },
        )
        report_id = create_response.json()["report_id"]
        get_response = client.get(f"/api/v1/townlight_inspections/reports/{report_id}")
    finally:
        main_module._dispose_case_repository()
        main_module._case_db_url = None

    assert repeat_response.status_code == 200
    assert repeat_response.json()["repeat_case_count"] == 2
    assert create_response.status_code == 200
    assert report_id
    assert get_response.status_code == 200
    assert get_response.json()["report_id"] == report_id
    assert create_response.json()["staff_review_id"]
    db_path.unlink(missing_ok=True)


def test_report_lookup_requires_configured_database() -> None:
    response = client.get("/api/v1/townlight_inspections/reports/not-configured")

    assert response.status_code == 503
    assert "Set TOWNLIGHT_INSPECTIONS_CASE_DB_URL" in response.json()["detail"]["fix"]


def test_staff_review_queue_lifecycle_is_staff_gated_and_persistent(monkeypatch, tmp_path) -> None:
    db_path = tmp_path / "staff-review-records.db"
    monkeypatch.setenv("TOWNLIGHT_INSPECTIONS_CASE_DB_URL", f"sqlite:///{db_path}")
    monkeypatch.setenv("TOWNLIGHT_INSPECTIONS_STAFF_API_KEY", "test-secret")
    headers = {
        "X-Townlight-Inspections-Role": "staff",
        "X-Townlight-Inspections-Staff-Key": "test-secret",
    }

    try:
        create_response = client.post(
            "/api/v1/townlight_inspections/staff/reviews",
            headers=headers,
            json={
                "inspection_id": "insp-200",
                "property_reference": "42 Oak Avenue",
                "reason": "Potential repeat case requires supervisor review.",
            },
        )
        review_id = create_response.json()["review_id"]
        list_response = client.get("/api/v1/townlight_inspections/staff/reviews", headers=headers)
        update_response = client.patch(
            f"/api/v1/townlight_inspections/staff/reviews/{review_id}",
            headers=headers,
            json={
                "status": "resolved",
                "assigned_to": "inspector@example.gov",
                "resolution": "Supervisor confirmed draft notice boundary.",
            },
        )
        summary_response = client.get("/api/v1/townlight_inspections/staff/reviews/summary", headers=headers)
    finally:
        main_module._dispose_case_repository()
        main_module._case_db_url = None

    assert create_response.status_code == 200
    assert create_response.json()["visibility"] == "staff_only"
    assert list_response.status_code == 200
    assert list_response.json()["items"][0]["review_id"] == review_id
    assert update_response.status_code == 200
    assert update_response.json()["status"] == "resolved"
    assert summary_response.status_code == 200
    assert summary_response.json()["total_items"] == 1
    db_path.unlink()


def test_staff_review_queue_rejects_missing_or_spoofed_staff_key(monkeypatch, tmp_path) -> None:
    db_path = tmp_path / "staff-review-auth.db"
    monkeypatch.setenv("TOWNLIGHT_INSPECTIONS_CASE_DB_URL", f"sqlite:///{db_path}")
    monkeypatch.setenv("TOWNLIGHT_INSPECTIONS_STAFF_API_KEY", "test-secret")

    try:
        missing_role = client.get("/api/v1/townlight_inspections/staff/reviews")
        spoofed_key = client.get(
            "/api/v1/townlight_inspections/staff/reviews",
            headers={
                "X-Townlight-Inspections-Role": "staff",
                "X-Townlight-Inspections-Staff-Key": "wrong",
            },
        )
    finally:
        main_module._dispose_case_repository()
        main_module._case_db_url = None

    assert missing_role.status_code == 403
    assert "X-Townlight-Inspections-Role" in missing_role.json()["detail"]["fix"]
    assert spoofed_key.status_code == 403
    assert "X-Townlight-Inspections-Staff-Key" in spoofed_key.json()["detail"]["fix"]
    db_path.unlink(missing_ok=True)
