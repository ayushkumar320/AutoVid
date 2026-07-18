from __future__ import annotations

from pathlib import Path

from logging_utils import Logger
from process import require_binary, run_command


class VideoMuxer:
    def __init__(self, logger: Logger) -> None:
        self.logger = logger

    def mux(self, source_video: Path, dubbed_audio: Path, output_video: Path) -> None:
        require_binary("ffmpeg")
        self.logger.info("Replacing original audio with dubbed English audio")
        run_command(
            [
                "ffmpeg",
                "-y",
                "-i",
                str(source_video),
                "-i",
                str(dubbed_audio),
                "-map",
                "0:v:0",
                "-map",
                "1:a:0",
                "-c:v",
                "copy",
                "-c:a",
                "aac",
                "-shortest",
                str(output_video),
            ]
        )
        self.logger.success(f"Created final dubbed video: {output_video}")

