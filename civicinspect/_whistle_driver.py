"""Driver executed inside the TextFlowKit runtime: WAV in, transcript JSON out.

Uses only TextFlowKit's public engine-selection API and prints one JSON line.
"""
from __future__ import annotations

import json
import sys
import os
from pathlib import Path


def main() -> int:
    path, engine_name = sys.argv[1], (sys.argv[2] if len(sys.argv) > 2 else "whistle")
    # The suite deploys verified assets alongside its interpreter. An explicit
    # independently provisioned TextFlowKit configuration remains supported.
    bundled = Path(sys.executable).resolve().parent / "inspections" / "whistle"
    if bundled.is_dir():
        os.environ.setdefault("TEXTFLOWKIT_MODELS_DIR", str(bundled))
        os.environ.setdefault("TEXTFLOWKIT_OFFLINE", "1")
    from textflowkit.core.engine import get_engine

    engine = get_engine(engine_name)
    transcript = engine.transcribe(path)
    payload = {
        "engine": engine_name,
        "engine_class": type(engine).__name__,
        "model": getattr(engine, "model_name", None),
        "device": getattr(engine, "device", None),
        "text": transcript.text,
        "segments": [
            {"start": float(seg.start), "end": float(seg.end), "text": seg.text}
            for seg in (getattr(transcript, "segments", None) or [])
        ],
    }
    print(json.dumps(payload, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
