"""Unit checks for the inspection transcription adapter's fail-closed branches.

These are *unit* checks and are labelled as such: they prove the adapter refuses
or reports rather than inventing a transcript. The real engine run is the
acceptance receipt `media-analysis-receipt.json`.
"""
from __future__ import annotations

import pytest

from civicinspect.transcription import (
    TextFlowKitTranscriptionProvider,
    TranscriptionUnavailable,
)

WAV = b"RIFF" + b"\x00" * 60


def test_unavailable_when_runtime_missing(tmp_path) -> None:
    provider = TextFlowKitTranscriptionProvider(python=tmp_path / "missing.exe")
    assert provider.unavailable_reason()
    with pytest.raises(TranscriptionUnavailable):
        provider.transcribe_sync(raw=WAV, media_type="audio/wav")


def test_unavailable_when_decoder_missing_for_compressed_audio(tmp_path) -> None:
    provider = TextFlowKitTranscriptionProvider(ffmpeg="definitely-not-on-path-xyz")
    with pytest.raises(TranscriptionUnavailable) as excinfo:
        provider.transcribe_sync(raw=b"ID3" + b"\x00" * 40, media_type="audio/mpeg")
    assert "ffmpeg" in str(excinfo.value)


def test_adapter_names_itself() -> None:
    assert TextFlowKitTranscriptionProvider().name == "textflowkit.whistle"
