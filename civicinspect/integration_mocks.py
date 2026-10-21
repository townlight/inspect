"""Adversarial local integration contracts for Townlight Inspections."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class IntegrationMockResult:
    scenario: str
    status: str
    review_required: bool
    findings: tuple[str, ...]
    boundary: str


def validate_inspection_context_mocks(payload: dict[str, Any]) -> IntegrationMockResult:
    """Validate local CivicCode/case context payloads without external calls."""

    findings: list[str] = []
    scenario = str(payload.get("scenario", "inspection-context"))

    if payload.get("role") not in {"staff", "service"}:
        findings.append("Rejected inspection context without trusted staff or service role.")
    if not payload.get("code_context_id"):
        findings.append("Missing Townlight Code context ID; cite code context before notice drafting.")
    if not payload.get("case_context_id"):
        findings.append("Missing inspection case context ID; confirm the system-of-record case first.")
    if payload.get("official_finding") is True:
        findings.append("Rejected attempted official finding in integration context.")
    if payload.get("citation_issued") is True:
        findings.append("Rejected attempted citation issuance in integration context.")
    if payload.get("fine_amount") is not None:
        findings.append("Rejected attempted fine assessment in integration context.")
    if payload.get("photo_analysis_source") == "live":
        findings.append("Rejected live photo-analysis claim; only inspector-provided observations are allowed.")
    if payload.get("source_date_status") == "stale":
        findings.append("Stale code/case context requires staff refresh before notice drafting.")

    status = "ready-for-staff-review" if not findings else "blocked-for-staff-review"
    return IntegrationMockResult(
        scenario=scenario,
        status=status,
        review_required=True,
        findings=tuple(findings),
        boundary=(
            "Townlight Inspections validates local integration context only; it does not call live "
            "Townlight Code, inspection scheduling, photo-analysis, LLM, or system-of-record "
            "services in this recovery release."
        ),
    )
