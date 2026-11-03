"""Deterministic repeat-case lookup helpers for Townlight Inspections."""

from __future__ import annotations

from dataclasses import dataclass


DISCLAIMER = (
    "Townlight Inspections provides inspection-support drafts only. Inspectors own every decision; "
    "the module does not issue official findings, citations, fines, or notices."
)


@dataclass(frozen=True)
class RepeatCaseResult:
    property_reference: str
    violation_type: str
    repeat_case_count: int
    related_case_ids: tuple[str, ...]
    staff_note: str
    disclaimer: str = DISCLAIMER


SAMPLE_CASES = {
    "100 main": ("case-2025-014", "case-2025-088"),
    "42 oak": ("case-2024-219",),
}


def lookup_repeat_cases(*, property_reference: str, violation_type: str = "") -> RepeatCaseResult:
    """Return sample repeat-case context without querying a production case system."""

    clean_property = property_reference.strip() or "unknown property"
    normalized = clean_property.casefold()
    related = tuple(ids for key, ids in SAMPLE_CASES.items() if key in normalized for ids in ids)
    clean_violation = violation_type.strip() or "general inspection"
    return RepeatCaseResult(
        property_reference=clean_property,
        violation_type=clean_violation,
        repeat_case_count=len(related),
        related_case_ids=related,
        staff_note=(
            "Review related case history before drafting any notice. Confirm ownership, "
            "jurisdiction, and current field conditions in the system of record."
        ),
    )
