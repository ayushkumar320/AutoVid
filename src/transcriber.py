from __future__ import annotations

from pathlib import Path

from logging_utils import Logger
from models import TranscriptSegment
from storage import write_json


class FasterWhisperTranscriber:
    def __init__(self, model_name: str, logger: Logger) -> None:
        self.model_name = model_name
        self.logger = logger

    def transcribe(self, audio_path: Path, json_path: Path, text_path: Path) -> list[TranscriptSegment]:
        try:
            from faster_whisper import WhisperModel
        except ImportError as exc:
            raise RuntimeError("Missing dependency 'faster-whisper'. Run 'uv sync' first.") from exc

        self.logger.info(f"Loading Faster Whisper model: {self.model_name}")
        model = WhisperModel(self.model_name, device="auto", compute_type="auto")
        self.logger.info("Transcribing audio into timestamped segments")
        raw_segments, info = model.transcribe(str(audio_path), vad_filter=True)

        language = getattr(info, "language", None)
        segments: list[TranscriptSegment] = []
        transcript_lines: list[str] = []

        for index, segment in enumerate(raw_segments):
            text = segment.text.strip()
            if not text:
                continue
            item = TranscriptSegment(
                index=index,
                start=float(segment.start),
                end=float(segment.end),
                text=text,
                language=language,
            )
            segments.append(item)
            transcript_lines.append(f"[{item.start:.2f} - {item.end:.2f}] {item.text}")

        write_json(json_path, [segment.to_dict() for segment in segments])
        text_path.write_text("\n".join(transcript_lines) + "\n", encoding="utf-8")
        self.logger.success(f"Transcribed {len(segments)} segments; language={language or 'unknown'}")
        return segments

