from fastapi.testclient import TestClient

from civicinspect.integration_mocks import validate_inspection_context_mocks
from civicinspect.main import app


client = TestClient(app)


def test_adversarial_mock_rejects_spoofed_enforcement_and_live_photo_claims() -> None:
    result = validate_inspection_context_mocks(
        {
            "scenario": "spoofed-citation",
            "role": "resident",
            "official_finding": True,
            "citation_issued": True,
            "fine_amount": "$500",
            "photo_analysis_source": "live",
            "source_date_status": "stale",
        }
    )

    assert result.status == "blocked-for-staff-review"
    assert result.review_required is True
    assert "Rejected inspection context without trusted staff or service role." in result.findings
    assert "Rejected attempted official finding in integration context." in result.findings
    assert "Rejected attempted citation issuance in integration context." in result.findings
    assert "does not call live Townlight Code" in result.boundary


def test_integration_mock_api_accepts_complete_staff_context_for_review() -> None:
    response = client.post(
        "/api/v1/civicinspect/integrations/mock/inspection-context",
        json={
            "scenario": "complete-local-context",
            "role": "staff",
            "code_context_id": "code-context-456",
            "case_context_id": "case-context-123",
            "source_date_status": "current",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ready-for-staff-review"
    assert payload["findings"] == []
    assert payload["review_required"] is True


def test_integration_mock_api_blocks_stale_or_partial_context() -> None:
    response = client.post(
        "/api/v1/civicinspect/integrations/mock/inspection-context",
        json={
            "scenario": "stale-code-context",
            "role": "service",
            "case_context_id": "case-context-123",
            "source_date_status": "stale",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "blocked-for-staff-review"
    assert "Missing Townlight Code context ID" in " ".join(payload["findings"])
    assert "Stale code/case context" in " ".join(payload["findings"])


def test_inspection_review_context_carries_code_and_case_references() -> None:
    response = client.post(
        "/api/v1/civicinspect/context/inspection-review",
        json={
            "inspection_id": "insp-100",
            "property_reference": "100 Main Street",
            "violation_type": "nuisance",
            "code_context_id": "code-section-1",
            "case_context_id": "case-2026-001",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["review_required"] is True
    assert "Townlight Code context: code-section-1" in payload["citations"]
    assert "Inspection case context: case-2026-001" in payload["citations"]
    assert "official finding" in payload["boundary"]
