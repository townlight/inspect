"""Inspector-owned evidence and review; never official enforcement actions."""
import base64
import hashlib
import json
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator

BOUNDARY = (
    "Inspector review workpaper only. Not an official finding, citation, fine, notice, "
    "inspection schedule, legal advice or system-of-record action. Photo observations "
    "and voice transcripts supplied by staff remain authoritative; any automated "
    "description or transcript produced by a configured adapter is a review-required "
    "draft, and nothing is issued or enforced automatically."
)


class Model(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class AnalysisObservation(Model):
    """One draft observation, named with the adapter that actually produced it."""

    source: str = Field(min_length=1, max_length=64)
    filename: str = Field(default="", max_length=160)
    media_type: str = Field(default="", max_length=80)
    text: str = Field(min_length=1, max_length=4000)
    adapter: str = Field(default="", max_length=120)
    citation_source_ids: list[str] = Field(default_factory=list, max_length=30)

    @model_validator(mode="after")
    def cites(self):
        if len(self.citation_source_ids) != len(set(self.citation_source_ids)):
            raise ValueError("Each draft observation cites a source once.")
        return self


class CitedSection(Model):
    """One resolved public Code section; never a caller-supplied quotation."""

    source_id: str = Field(min_length=1, max_length=500)
    citation: str = Field(min_length=1, max_length=500)
    title: str = Field(default="", max_length=500)
    version: str = Field(default="", max_length=80)


class AnalysisRecord(Model):
    """The adapter output that accompanies a saved inspection draft."""

    observations: list[AnalysisObservation] = Field(default_factory=list, max_length=30)
    cited_sections: list[CitedSection] = Field(default_factory=list, max_length=30)
    unavailable: list[str] = Field(default_factory=list, max_length=30)
    runtime: dict = Field(default_factory=dict)
    review_required: bool = True

    @model_validator(mode="after")
    def consistent(self):
        if not self.review_required:
            raise ValueError("Analysed observations are always review-required draft text.")
        cited = {section.source_id for section in self.cited_sections}
        for item in self.observations:
            if not set(item.citation_source_ids) <= cited:
                raise ValueError("A draft observation cites a section that was not resolved.")
        if len(self.cited_sections) > len({s.source_id for s in self.cited_sections}):
            raise ValueError("Each cited section appears once.")
        if len(json.dumps(self.runtime, sort_keys=True, default=str)) > 8000:
            raise ValueError("Adapter runtime details must stay small.")
        return self

    @classmethod
    def from_media_analysis(cls, payload) -> "AnalysisRecord":
        """Build the record from ``MediaAnalysis.to_payload()`` (or an equal dict)."""

        return cls.model_validate({
            "observations": [
                {"source": item["source"], "filename": item.get("filename", ""),
                 "media_type": item.get("media_type", ""), "text": item["text"],
                 "adapter": item.get("adapter", ""),
                 "citation_source_ids": list(item.get("citation_source_ids") or [])}
                for item in payload.get("draft_observations", [])],
            "cited_sections": [
                {"source_id": section["source_id"], "citation": section["citation"],
                 "title": section.get("title", ""), "version": str(section.get("version", ""))}
                for section in payload.get("cited_sections", [])],
            "unavailable": [str(item.get("reason", item)) for item in payload.get("unavailable", [])],
            "runtime": payload.get("runtime") or {},
            "review_required": True,
        })


class Evidence(Model):
    filename: str = Field(pattern=r"^[a-zA-Z0-9][a-zA-Z0-9_.-]{0,150}$")
    description: str = Field(min_length=1, max_length=2000)
    media_type: Literal["text/plain", "image/jpeg", "image/png", "image/webp",
                        "application/pdf", "audio/webm", "audio/ogg", "audio/wav",
                        "audio/mpeg", "audio/mp4"]
    content_base64: str = Field(min_length=1, max_length=14_000_000)
    sha256: str = Field(pattern=r"^[a-f0-9]{64}$")

    @model_validator(mode="after")
    def original(self):
        try:
            raw = base64.b64decode(self.content_base64, validate=True)
        except ValueError:
            raise ValueError("Evidence must contain valid base64 original bytes.") from None
        if not raw or len(raw) > 10_000_000 or hashlib.sha256(raw).hexdigest() != self.sha256:
            raise ValueError("Evidence original SHA256 or size does not match.")
        return self


class SourceLink(Model):
    provider: Literal["code"] = "code"
    source_id: str = Field(min_length=1, max_length=500)
    expected_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")


class InspectionInput(Model):
    expected_revision: UUID | None = None
    title: str = Field(min_length=1, max_length=500)
    property_reference: str = Field(min_length=1, max_length=1000)
    inspection_reference: str = Field(min_length=1, max_length=160)
    dataset_kind: Literal["municipal", "fictional"]
    inspector_notes: str = Field(min_length=1, max_length=10000)
    photo_observations: list[str] = Field(default_factory=list, max_length=30)
    voice_notes: str = Field(default="", max_length=10000)
    evidence: list[Evidence] = Field(default_factory=list, max_length=10)
    linked_sources: list[SourceLink] = Field(default_factory=list, max_length=30)
    assigned_to: str = Field(default="", max_length=255)
    staff_notes: str = Field(default="", max_length=10000)
    notice_draft: str = Field(default="", max_length=10000)
    review_state: Literal["draft", "follow_up", "reviewed"] = "draft"
    review_notes: str = Field(default="", max_length=4000)
    public_summary: str = Field(default="", max_length=10000)
    analysis: AnalysisRecord | None = None

    @model_validator(mode="after")
    def review(self):
        if any(not s.strip() or len(s) > 2000 for s in self.photo_observations):
            raise ValueError("Provide bounded, inspector-entered photo observations.")
        names = [e.filename.casefold() for e in self.evidence]
        if len(names) != len(set(names)) or sum(len(e.content_base64) for e in self.evidence) > 14_000_000:
            raise ValueError("Use unique evidence filenames and at most 10MB of original evidence.")
        ids = [s.source_id for s in self.linked_sources]
        if len(ids) != len(set(ids)):
            raise ValueError("Select each Code source once.")
        if self.analysis is not None:
            selected = {link.source_id for link in self.linked_sources}
            cited = {section.source_id for section in self.analysis.cited_sections}
            if not cited <= selected:
                raise ValueError("Cite only the Code sources selected for this case.")
        if self.review_state == "reviewed" and not self.review_notes:
            raise ValueError("Record explicit inspector review notes.")
        return self
