from __future__ import annotations

import json
import hashlib
from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from models import RunPaths


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")


def safe_job_id(url: str) -> str:
    suffix = hashlib.sha1(url.encode("utf-8")).hexdigest()[:8]
    return f"{utc_timestamp()}-{suffix}"


def create_run_paths(output_dir: Path, url: str) -> RunPaths:
    job_dir = output_dir / safe_job_id(url)
    tts_dir = job_dir / "tts_segments"
    job_dir.mkdir(parents=True, exist_ok=False)
    tts_dir.mkdir(parents=True, exist_ok=True)
    return RunPaths(
        job_dir=job_dir,
        source_video=job_dir / "source.mp4",
        source_audio=job_dir / "source.wav",
        metadata=job_dir / "metadata.json",
        transcript_json=job_dir / "transcript.json",
        transcript_txt=job_dir / "transcript.txt",
        translated_json=job_dir / "translated_segments.json",
        tts_dir=tts_dir,
        tts_manifest=job_dir / "tts_manifest.json",
        dubbed_audio=job_dir / "dubbed.wav",
        dubbed_video=job_dir / "dubbed_output.mp4",
        run_summary=job_dir / "run_summary.json",
    )


def to_jsonable(value: Any) -> Any:
    if isinstance(value, Path):
        return str(value)
    if is_dataclass(value):
        return to_jsonable(asdict(value))
    if isinstance(value, list):
        return [to_jsonable(item) for item in value]
    if isinstance(value, dict):
        return {key: to_jsonable(item) for key, item in value.items()}
    return value


def write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(to_jsonable(data), indent=2, ensure_ascii=False), encoding="utf-8")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))
