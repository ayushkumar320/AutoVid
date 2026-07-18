from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from logging_utils import Logger
from models import TTSClip

if TYPE_CHECKING:
    from pydub import AudioSegment


class AudioAligner:
    def __init__(self, logger: Logger) -> None:
        self.logger = logger

    def align(self, clips: list[TTSClip], output_wav: Path, total_duration: float | None = None) -> None:
        try:
            from pydub import AudioSegment
        except ImportError as exc:
            raise RuntimeError("Missing dependency 'pydub'. Run 'uv sync' first.") from exc

        if not clips:
            raise RuntimeError("Cannot align audio: no TTS clips were generated.")

        duration_ms = int(max((clip.end for clip in clips), default=0.0) * 1000)
        if total_duration:
            duration_ms = max(duration_ms, int(total_duration * 1000))

        timeline = AudioSegment.silent(duration=duration_ms + 1000)
        for clip in clips:
            segment_audio = AudioSegment.from_file(clip.path)
            target_ms = max(1, int((clip.end - clip.start) * 1000))
            segment_audio = self._fit_to_duration(segment_audio, target_ms)
            timeline = timeline.overlay(segment_audio, position=int(clip.start * 1000))

        timeline.export(output_wav, format="wav")
        self.logger.success(f"Created aligned dubbed audio: {output_wav}")

    def _fit_to_duration(self, audio: "AudioSegment", target_ms: int) -> "AudioSegment":
        actual_ms = len(audio)
        if actual_ms <= 0 or target_ms <= 0:
            return audio
        ratio = actual_ms / target_ms
        if ratio <= 1.15:
            return audio
        speed = min(1.15, max(0.90, ratio))
        return audio.speedup(playback_speed=speed)

