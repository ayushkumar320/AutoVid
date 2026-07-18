from __future__ import annotations

from pathlib import Path

from logging_utils import Logger
from process import require_binary, run_command


class AudioProcessor:
    def __init__(self, logger: Logger) -> None:
        self.logger = logger

    def extract_wav(self, source_video: Path, output_wav: Path) -> None:
        require_binary("ffmpeg")
        self.logger.info("Extracting mono 16 kHz WAV audio for transcription")
        run_command(
            [
                "ffmpeg",
                "-y",
                "-i",
                str(source_video),
                "-vn",
                "-ac",
                "1",
                "-ar",
                "16000",
                "-c:a",
                "pcm_s16le",
                str(output_wav),
            ]
        )
        self.logger.success(f"Extracted audio: {output_wav}")

