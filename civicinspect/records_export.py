"""Records-ready export helpers for Townlight Inspections."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class InspectionExport:
    title: str
    case_id: str
    format: str
    checklist: tuple[str, ...]
    retention_note: str


def build_inspection_export(*, title: str, case_id: str, format: str = "markdown") -> InspectionExport:
    """Build a deterministic records-ready inspection export checklist."""

    return InspectionExport(
        title=title.strip() or "Untitled inspection export",
        case_id=case_id.strip() or "unassigned-case",
        format=format,
        checklist=(
            "Preserve inspector-entered notes and observation text.",
            "Preserve any draft notice text exactly as reviewed by staff.",
            "Record inspector, reviewer, review date, and final disposition.",
            "Include the non-decision disclaimer with any public-facing export.",
        ),
        retention_note=(
            "Keep observations, draft report, notice draft, staff edits, and final system-of-record "
            "links with the municipal inspection case file."
        ),
    )
