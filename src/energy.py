from __future__ import annotations

import math
from pathlib import Path

from logging_utils import Logger
from models import EnergyProfile, TranslatedSegment
from storage import write_json


class EnergyAnalyzer:
    def __init__(self, logger: Logger) -> None:
        self.logger = logger

    def analyze(
        self,
        source_audio: Path,
        segments: list[TranslatedSegment],
        output_path: Path | None = None,
    ) -> dict[int, EnergyProfile]:
        try:
            from pydub import AudioSegment
        except ImportError as exc:
            raise RuntimeError("Missing dependency 'pydub'. Run 'uv sync' first.") from exc

        self.logger.info("Analyzing original speech energy for expressive TTS")
        audio = AudioSegment.from_wav(source_audio)
        global_loudness = _finite_dbfs(audio.dBFS, fallback=-35.0)

        profiles: dict[int, EnergyProfile] = {}
        for segment in segments:
            start_ms = max(0, int(segment.start * 1000))
            end_ms = max(start_ms + 1, int(segment.end * 1000))
            snippet = audio[start_ms:end_ms]
            loudness = _finite_dbfs(snippet.dBFS, fallback=global_loudness)
            delta = loudness - global_loudness
            speech_rate = len(segment.source_text) / max(segment.duration, 0.1)
            profile = self._map_to_profile(segment.index, loudness, delta, speech_rate, segment.source_text)
            profiles[segment.index] = profile

        if output_path:
            write_json(output_path, [profile.to_dict() for profile in profiles.values()])

        self.logger.success(f"Created {len(profiles)} expressive TTS profiles")
        return profiles

    def _map_to_profile(
        self,
        index: int,
        loudness: float,
        delta: float,
        speech_rate: float,
        text: str,
    ) -> EnergyProfile:
        rate = 0
        pitch = 0
        volume = 0
        label = "neutral"

        if speech_rate >= 17:
            rate += 12
            pitch += 8
            label = "fast"
        elif speech_rate >= 13:
            rate += 6
            pitch += 4
            label = "active"
        elif speech_rate <= 7:
            rate -= 6
            pitch -= 3
            label = "calm"

        if delta >= 7:
            volume += 8
            rate += 5
            pitch += 8
            label = "high_energy"
        elif delta >= 3:
            volume += 4
            rate += 2
            pitch += 4
            label = "engaged"
        elif delta <= -8:
            volume -= 8
            rate -= 3
            pitch -= 6
            label = "soft"
        elif delta <= -4:
            volume -= 4
            pitch -= 3
            label = "relaxed"

        if any(mark in text for mark in ("!", "?", "?!")):
            pitch += 4
            rate += 2
            if label == "neutral":
                label = "expressive"

        return EnergyProfile(
            index=index,
            loudness_dbfs=round(loudness, 2),
            loudness_delta_db=round(delta, 2),
            speech_rate=round(speech_rate, 2),
            tts_rate=_percent(rate, -18, 18),
            tts_pitch=_pitch(pitch, -18, 18),
            tts_volume=_percent(volume, -16, 12),
            label=label,
        )


def _finite_dbfs(value: float, fallback: float) -> float:
    if math.isinf(value) or math.isnan(value):
        return fallback
    return float(value)


def _percent(value: int, minimum: int, maximum: int) -> str:
    clamped = min(maximum, max(minimum, value))
    return f"{clamped:+d}%"


def _pitch(value: int, minimum: int, maximum: int) -> str:
    clamped = min(maximum, max(minimum, value))
    return f"{clamped:+d}Hz"
