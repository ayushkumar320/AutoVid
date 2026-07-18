from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class TranscriptSegment:
    index: int
    start: float
    end: float
    text: str
    language: str | None = None

    @property
    def duration(self) -> float:
        return max(0.0, self.end - self.start)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class TranslatedSegment:
    index: int
    start: float
    end: float
    source_text: str
    english_text: str
    language: str | None = None

    @property
    def duration(self) -> float:
        return max(0.0, self.end - self.start)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class EnergyProfile:
    index: int
    loudness_dbfs: float | None
    loudness_delta_db: float
    speech_rate: float
    tts_rate: str
    tts_pitch: str
    tts_volume: str
    label: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class TTSClip:
    index: int
    path: Path
    start: float
    end: float
    english_text: str
    rate: str = "+0%"
    pitch: str = "+0Hz"
    volume: str = "+0%"
    energy_label: str = "neutral"

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["path"] = str(self.path)
        return data


@dataclass(frozen=True)
class RunPaths:
    job_dir: Path
    source_video: Path
    source_audio: Path
    metadata: Path
    transcript_json: Path
    transcript_txt: Path
    translated_json: Path
    tts_dir: Path
    tts_manifest: Path
    dubbed_audio: Path
    dubbed_video: Path
    run_summary: Path
