"""Inspection report draft helpers for Townlight Inspections."""

from __future__ import annotations

from dataclasses import dataclass

from civicinspect.case_lookup import DISCLAIMER, lookup_repeat_cases


@dataclass(frozen=True)
class InspectionReportDraft:
    inspection_id: str
    property_reference: str
    summary: str
    observation_bullets: tuple[str, ...]
    inspector_review_required: bool
    disclaimer: str = DISCLAIMER


def draft_inspection_report(
    *,
    inspection_id: str,
    property_reference: str,
    inspector_notes: str,
    photo_observations: tuple[str, ...] = (),
    voice_notes: str = "",
    repeat_case_count: int | None = None,
) -> InspectionReportDraft:
    """Draft a report outline from inspector-provided text; no image analysis is performed."""

    count = (lookup_repeat_cases(property_reference=property_reference).repeat_case_count
             if repeat_case_count is None else repeat_case_count)
    observations = [note.strip() for note in photo_observations if note.strip()]
    if inspector_notes.strip():
        observations.insert(0, inspector_notes.strip())
    if voice_notes.strip():
        observations.append(f"Voice-note summary supplied by inspector: {voice_notes.strip()}")
    if not observations:
        observations.append("No observations supplied; inspector must enter field notes.")
    return InspectionReportDraft(
        inspection_id=inspection_id.strip() or "unassigned-inspection",
        property_reference=property_reference.strip() or "unknown property",
        summary=(
            f"Draft inspection report with {len(observations)} observation(s) and "
            f"{count} related {'sample ' if repeat_case_count is None else 'saved '}case(s)."
        ),
        observation_bullets=tuple(observations),
        inspector_review_required=True,
    )
