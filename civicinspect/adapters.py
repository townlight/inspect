# SPDX-License-Identifier: AGPL-3.0-only
"""Configured media/citation adapters shared by the product app and the host bridge.

Everything here reads *deployment* configuration and returns the adapter the
deployment actually configured, or a plain-Python error. It deliberately does
not import FastAPI: the product app (``civicinspect.main``) and the shared-shell
native transport (``civicsuite_runtime.inspections_bridge``) must resolve the
*same* adapters, so neither side may own a private copy.

Fail-closed rules kept from the original routes:

* no vision provider configured -> ``None`` (analysis reports ``unavailable``);
* no transcriber configured       -> ``None`` (audio is retained, never invented);
* a configured-but-invalid value  -> ``ConfigurationError``;
* no public Code source file      -> empty provider map, so no citation resolves.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path


class ConfigurationError(RuntimeError):
    """The deployment configured an adapter that cannot be used as configured."""


VISION_PROVIDER_ENV = "CIVICINSPECT_VISION_PROVIDER"
VISION_MODEL_ENV = "CIVICINSPECT_VISION_MODEL"
VISION_BASE_URL_ENV = "CIVICINSPECT_VISION_BASE_URL"
VISION_THINK_ENV = "CIVICINSPECT_VISION_THINK"
TRANSCRIBER_ENV = "CIVICINSPECT_TRANSCRIBER"
PUBLIC_SOURCES_ENV = "CIVICINSPECT_PUBLIC_SOURCES"
TRANSCRIBER_VALUES = {"whistle", "textflowkit"}


def configured_vision_provider():
    """Return ``(provider, model)`` for the configured vision adapter, or ``(None, None)``."""

    name = os.environ.get(VISION_PROVIDER_ENV, "").strip()
    if not name:
        return None, None
    try:
        from civiccore.llm.factory import build_provider
        from civiccore.llm.providers.config import AnthropicConfig, OllamaConfig, OpenAIConfig
    except Exception as exc:  # noqa: BLE001 - a broken Coherent Core must not invent an adapter
        raise ConfigurationError(
            f"the configured vision adapter library is unavailable ({type(exc).__name__})"
        ) from None
    schemas = {"ollama": OllamaConfig, "openai": OpenAIConfig, "anthropic": AnthropicConfig}
    schema = schemas.get(name)
    if schema is None:
        raise ConfigurationError(
            f"{VISION_PROVIDER_ENV} '{name}' is not supported; use ollama, openai or anthropic."
        )
    model = os.environ.get(VISION_MODEL_ENV) or None
    fields: dict[str, object] = {}
    if name == "ollama":
        for env_name, field_name in ((VISION_BASE_URL_ENV, "base_url"),
                                     (VISION_MODEL_ENV, "default_model")):
            raw = os.environ.get(env_name, "").strip()
            if raw:
                fields[field_name] = raw
        think = os.environ.get(VISION_THINK_ENV, "").strip()
        if think:
            lowered = think.lower()
            if lowered in {"true", "false"}:
                fields["think"] = lowered == "true"
            elif lowered in {"low", "medium", "high"}:
                fields["think"] = lowered
            else:
                raise ConfigurationError(
                    f"{VISION_THINK_ENV} '{think}' is not a valid think mode; "
                    "use true, false, low, medium or high."
                )
    return build_provider(name, schema(**fields)), model


def configured_transcription_provider():
    """The owned TextFlowKit transcriber, or ``None`` when it is not configured."""

    import sys
    bundled = Path(sys.executable).resolve().parent / 'inspections/whistle'
    default = 'whistle' if bundled.is_dir() else ''
    name = os.environ.get(TRANSCRIBER_ENV, default).strip().lower()
    if name not in TRANSCRIBER_VALUES:
        return None
    from civicinspect.transcription import TextFlowKitTranscriptionProvider

    return TextFlowKitTranscriptionProvider()


def configured_analysis_providers() -> dict:
    """Code sources for cited sections, from the configured public source file."""

    raw = os.environ.get(PUBLIC_SOURCES_ENV, "").strip()
    if not raw:
        return {}
    try:
        payload = json.loads(Path(raw).read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - unreadable configuration is not a citation
        raise ConfigurationError(
            f"configured inspection Code sources could not be read ({type(exc).__name__}); "
            f"check {PUBLIC_SOURCES_ENV}"
        ) from None
    rows = payload.get("sources", []) if isinstance(payload, dict) else payload
    sources = []
    for row in rows:
        text = str(row["text"])
        sources.append({"provider": "code", "source_id": str(row["source_id"]),
                        "version": row.get("version", "1"),
                        "title": str(row.get("title", row["source_id"])),
                        "citation": str(row.get("citation", row.get("title", row["source_id"]))),
                        "text": text, "visibility": str(row.get("visibility", "public")),
                        "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest()})
    return {"code": lambda *, source_id=None, query=None: (
        [dict(r) for r in sources if r["source_id"] == source_id] if source_id is not None
        else [])}
