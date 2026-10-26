"""Inspector-owned evidence and review; never official enforcement actions."""
import base64
import hashlib
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator

BOUNDARY = (
    "Inspector review workpaper only. Not an official finding, citation, fine, notice, "
    "inspection schedule, legal advice or system-of-record action. Photo observations "
    "and voice transcripts are supplied by staff; no automated image analysis or transcription."
)


class Model(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class Evidence(Model):
    filename: str = Field(pattern=r"^[a-zA-Z0-9][a-zA-Z0-9_.-]{0,150}$")
    description: str = Field(min_length=1, max_length=2000)
    media_type: Literal["text/plain", "image/jpeg", "image/png", "application/pdf"]
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
        if self.review_state == "reviewed" and not self.review_notes:
            raise ValueError("Record explicit inspector review notes.")
        return self
