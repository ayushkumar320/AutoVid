from __future__ import annotations

import asyncio
from pathlib import Path

from logging_utils import Logger
from models import TTSClip, TranslatedSegment
from storage import write_json


class EdgeTTSGenerator:
    def __init__(self, voice: str, logger: Logger) -> None:
        self.voice = voice
        self.logger = logger

    def synthesize(
        self,
        segments: list[TranslatedSegment],
        output_dir: Path,
        manifest_path: Path,
    ) -> list[TTSClip]:
        clips = asyncio.run(self._synthesize_async(segments, output_dir))
        write_json(manifest_path, [clip.to_dict() for clip in clips])
        self.logger.success(f"Generated {len(clips)} TTS clips")
        return clips

    async def _synthesize_async(
        self,
        segments: list[TranslatedSegment],
        output_dir: Path,
    ) -> list[TTSClip]:
        try:
            import edge_tts
        except ImportError as exc:
            raise RuntimeError("Missing dependency 'edge-tts'. Run 'uv sync' first.") from exc

        clips: list[TTSClip] = []
        for segment in segments:
            path = output_dir / f"{segment.index:04d}.mp3"
            text = segment.english_text.strip() or segment.source_text
            self.logger.info(f"Generating TTS segment {segment.index}")
            communicate = edge_tts.Communicate(text=text, voice=self.voice)
            await communicate.save(str(path))
            clips.append(
                TTSClip(
                    index=segment.index,
                    path=path,
                    start=segment.start,
                    end=segment.end,
                    english_text=text,
                )
            )
        return clips

