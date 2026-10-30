"""Reuse the owned TextFlowKit transcriber as an inspection adapter.

Why a subprocess
----------------
The candidate includes an owned copy of TextFlowKit's Whistle engine and its
pinned native assets. The driver runs in the deployed Python interpreter;
an explicitly configured independent interpreter remains supported. The
adapter accepts bytes and returns text or an explicit failure.

What is real
------------
* the engine is TextFlowKit's own `get_engine("whistle")` -> `WhistleEngine`,
  which runs the pinned native `needle.exe` against `whistle.cact`;
* audio of any container is decoded with ffmpeg to the 16 kHz mono PCM WAV the
  engine requires; if ffmpeg is missing the adapter says so instead of guessing.
"""
from __future__ import annotations

import asyncio
import json
import os
import shutil
import subprocess
import tempfile
import wave
import sys
from pathlib import Path

DEFAULT_PYTHON = Path(sys.executable)
DRIVER = Path(__file__).resolve().parent / "_whistle_driver.py"


class TranscriptionUnavailable(RuntimeError):
    """The adapter cannot run in this deployment (no runtime, no ffmpeg...)."""


class TranscriptionFailed(RuntimeError):
    """The adapter ran and failed."""


class TextFlowKitTranscriptionProvider:
    """Runs the owned TextFlowKit transcription engine over a subprocess."""

    name = "textflowkit.whistle"

    def __init__(self, *, python: str | os.PathLike[str] | None = None,
                 engine: str = "whistle", ffmpeg: str | None = None,
                 timeout: float = 100.0) -> None:
        self.python = Path(python or os.environ.get("CIVICINSPECT_TEXTFLOWKIT_PYTHON")
                           or DEFAULT_PYTHON)
        self.engine = engine
        bundled_ffmpeg = Path(sys.executable).resolve().parent.parent / 'station/bin/ffmpeg.exe'
        self.ffmpeg = ffmpeg or os.environ.get('CIVICINSPECT_FFMPEG') or (str(bundled_ffmpeg) if bundled_ffmpeg.is_file() else 'ffmpeg')
        self.timeout = timeout

    # -- what the engine accepts --------------------------------------------
    @staticmethod
    def _is_engine_wav(path: Path) -> bool:
        """True only for a WAV the engine takes as-is: 16 kHz mono 16-bit PCM.

        The product fixture and many phone recorders are 8 kHz, and the engine
        rejects that (``WhistleError``), so a WAV is conformed like any other
        container when it is not already in the engine's format.
        """

        try:
            with wave.open(str(path), "rb") as handle:
                return (handle.getframerate() == 16000 and handle.getnchannels() == 1
                        and handle.getsampwidth() == 2)
        except Exception:  # noqa: BLE001 - an unreadable header is "not conforming"
            return False

    # -- availability -------------------------------------------------------
    def unavailable_reason(self) -> str | None:
        if not self.python.is_file():
            return (f"TextFlowKit runtime not found at {self.python}; set "
                    "CIVICINSPECT_TEXTFLOWKIT_PYTHON to its interpreter")
        if not DRIVER.is_file():
            return f"transcription driver missing at {DRIVER}"
        return None

    # -- the adapter surface ------------------------------------------------
    def transcribe_sync(self, *, raw: bytes, media_type: str) -> dict:
        reason = self.unavailable_reason()
        if reason:
            raise TranscriptionUnavailable(reason)

        workdir = Path(tempfile.mkdtemp(prefix="civicinspect-stt-"))
        try:
            suffix = {"audio/webm": ".webm", "audio/ogg": ".ogg", "audio/mpeg": ".mp3",
                      "audio/mp4": ".m4a", "audio/wav": ".wav"}.get(media_type, ".bin")
            source = workdir / f"evidence{suffix}"
            source.write_bytes(raw)
            wav = workdir / "evidence-16k.wav"

            if suffix == ".wav" and self._is_engine_wav(source):
                wav = source
                converted_by = None
            else:
                ffmpeg = shutil.which(self.ffmpeg or "ffmpeg")
                if not ffmpeg:
                    raise TranscriptionUnavailable(
                        f"ffmpeg is not available to decode {media_type} audio for "
                        "transcription")
                convert = subprocess.run(
                    [ffmpeg, "-nostdin", "-v", "error", "-y", "-i", str(source),
                     "-ac", "1", "-ar", "16000", "-sample_fmt", "s16", str(wav)],
                    capture_output=True, text=True, timeout=self.timeout,
                    creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
                if convert.returncode != 0 or not wav.is_file():
                    raise TranscriptionFailed(
                        "ffmpeg could not decode the audio: "
                        + (convert.stderr or "")[-300:])
                converted_by = "ffmpeg"

            run = subprocess.run(
                [str(self.python), str(DRIVER), str(wav), self.engine],
                capture_output=True, text=True, timeout=self.timeout,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
            if run.returncode != 0:
                raise TranscriptionFailed(
                    f"TextFlowKit {self.engine} exited {run.returncode}: "
                    + (run.stderr or run.stdout or "").strip()[-400:])
            try:
                payload = json.loads((run.stdout or "").strip().splitlines()[-1])
            except Exception as exc:
                raise TranscriptionFailed(
                    f"could not read the transcribe result ({type(exc).__name__})") from exc
            payload["decoded_by"] = converted_by or "already 16 kHz mono PCM WAV"
            payload["source_media_type"] = media_type
            return payload
        finally:
            shutil.rmtree(workdir, ignore_errors=True)

    async def transcribe(self, *, raw: bytes, media_type: str) -> str:
        payload = await asyncio.to_thread(self.transcribe_sync, raw=raw,
                                         media_type=media_type)
        text = (payload.get("text") or "").strip()
        if not text:
            raise TranscriptionFailed("engine produced an empty transcript")
        self.last_result = payload
        return text
