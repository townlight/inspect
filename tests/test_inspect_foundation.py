from fastapi.testclient import TestClient

from townlight_inspections.case_lookup import lookup_repeat_cases
from townlight_inspections.main import app
from townlight_inspections.notice_draft import draft_notice
from townlight_inspections.records_export import build_inspection_export
from townlight_inspections.report_draft import draft_inspection_report


client = TestClient(app)


def test_repeat_case_lookup_returns_review_context() -> None:
    result = lookup_repeat_cases(property_reference="100 Main Street", violation_type="nuisance")
    assert result.repeat_case_count == 2
    assert result.related_case_ids == ("case-2025-014", "case-2025-088")
    assert "Inspectors own every decision" in result.disclaimer


def test_report_draft_preserves_inspector_ownership() -> None:
    result = draft_inspection_report(
        inspection_id="insp-100",
        property_reference="100 Main Street",
        inspector_notes="Overgrown vegetation visible from public alley.",
        photo_observations=("Photo shows weeds over fence line.",),
        voice_notes="Owner contact not confirmed.",
    )
    assert result.inspection_id == "insp-100"
    assert result.inspector_review_required is True
    assert result.observation_bullets[0].startswith("Overgrown vegetation")
    assert "related sample case" in result.summary


def test_notice_draft_requires_staff_actions() -> None:
    result = draft_notice(
        case_id="case-2026-001",
        property_reference="100 Main Street",
        violation_type="overgrown vegetation",
        observations=("Vegetation exceeds sample threshold.",),
    )
    assert result.heading == "Draft notice for overgrown vegetation"
    assert "Draft only for staff review" in result.draft_body
    assert any("Confirm the cited code section" in action for action in result.required_staff_actions)


def test_inspection_export_preserves_records_context() -> None:
    result = build_inspection_export(title="100 Main inspection draft", case_id="case-2026-001")
    assert result.title == "100 Main inspection draft"
    assert result.case_id == "case-2026-001"
    assert "Preserve inspector-entered notes and observation text." in result.checklist
    assert "municipal inspection case file" in result.retention_note


def test_repeat_case_lookup_api_success_shape() -> None:
    response = client.post(
        "/api/v1/townlight_inspections/cases/repeat-lookup",
        json={"property_reference": "100 Main Street", "violation_type": "nuisance"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["repeat_case_count"] == 2
    assert payload["related_case_ids"]
    assert payload["disclaimer"]


def test_report_notice_and_export_apis() -> None:
    report = client.post(
        "/api/v1/townlight_inspections/reports/draft",
        json={
            "inspection_id": "insp-100",
            "property_reference": "100 Main Street",
            "inspector_notes": "Overgrown vegetation observed.",
            "photo_observations": ["Photo shows rear alley condition."],
            "voice_notes": "Follow-up needed.",
        },
    )
    notice = client.post(
        "/api/v1/townlight_inspections/notices/draft",
        json={
            "case_id": "case-2026-001",
            "property_reference": "100 Main Street",
            "violation_type": "overgrown vegetation",
            "observations": ["Vegetation observed near alley."],
        },
    )
    export = client.post(
        "/api/v1/townlight_inspections/export",
        json={"title": "Inspection packet", "case_id": "case-2026-001"},
    )
    assert report.status_code == 200
    assert report.json()["inspector_review_required"] is True
    assert notice.status_code == 200
    assert notice.json()["required_staff_actions"]
    assert export.status_code == 200
    assert export.json()["case_id"] == "case-2026-001"


def test_public_ui_route_is_accessible_and_honest() -> None:
    response = client.get("/townlight_inspections")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    text = response.text
    assert '<a class="skip-link" href="#main">Skip to main content</a>' in text
    assert '<main id="main" tabindex="-1">' in text
    assert "v0.2.2 inspection support + staff review queues" in text
    assert "staff-only review queues" in text
    assert "does not issue official findings" in text
    assert "system-of-record updates" in text
