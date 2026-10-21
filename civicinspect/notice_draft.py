"""Notice draft helpers for Townlight Inspections."""

from __future__ import annotations

from dataclasses import dataclass

from civicinspect.case_lookup import DISCLAIMER, lookup_repeat_cases


@dataclass(frozen=True)
class NoticeDraft:
    case_id: str
    property_reference: str
    heading: str
    draft_body: str
    required_staff_actions: tuple[str, ...]
    disclaimer: str = DISCLAIMER


def draft_notice(
    *,
    case_id: str,
    property_reference: str,
    violation_type: str,
    observations: tuple[str, ...],
) -> NoticeDraft:
    """Create a deterministic notice draft that remains subordinate to inspector review."""

    repeat_context = lookup_repeat_cases(
        property_reference=property_reference,
        violation_type=violation_type,
    )
    clean_case = case_id.strip() or "unassigned-case"
    clean_type = violation_type.strip() or "inspection matter"
    clean_observations = tuple(item.strip() for item in observations if item.strip())
    observation_text = "; ".join(clean_observations) if clean_observations else "No observations supplied."
    return NoticeDraft(
        case_id=clean_case,
        property_reference=property_reference.strip() or "unknown property",
        heading=f"Draft notice for {clean_type}",
        draft_body=(
            f"Draft only for staff review. Case {clean_case} concerns {clean_type}. "
            f"Inspector observations: {observation_text}"
        ),
        required_staff_actions=(
            "Confirm the cited code section in Townlight Code before issuing any notice.",
            "Confirm property ownership and mailing address in the system of record.",
            f"Review {repeat_context.repeat_case_count} related sample case(s) before finalizing.",
        ),
    )
