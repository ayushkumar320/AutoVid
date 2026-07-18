from __future__ import annotations

from pathlib import Path
from typing import Any

from logging_utils import Logger
from storage import write_json


class VideoDownloader:
    def __init__(self, logger: Logger) -> None:
        self.logger = logger

    def download(self, url: str, output_video: Path, metadata_path: Path) -> dict[str, Any]:
        try:
            import yt_dlp
        except ImportError as exc:
            raise RuntimeError("Missing dependency 'yt-dlp'. Run 'uv sync' first.") from exc

        self.logger.info("Downloading source video with yt-dlp")
        options: dict[str, Any] = {
            "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            "outtmpl": str(output_video),
            "merge_output_format": "mp4",
            "noplaylist": True,
            "quiet": True,
            "no_warnings": True,
        }

        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=True)

        metadata = {
            "source_url": url,
            "title": info.get("title"),
            "duration_seconds": info.get("duration"),
            "uploader": info.get("uploader"),
            "webpage_url": info.get("webpage_url", url),
            "source_video": str(output_video),
        }
        write_json(metadata_path, metadata)
        self.logger.success(f"Downloaded video: {output_video}")
        return metadata

