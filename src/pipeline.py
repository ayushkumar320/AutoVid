from __future__ import annotations

from time import perf_counter
from typing import Any

from aligner import AudioAligner
from audio import AudioProcessor
from config import AppConfig
from downloader import VideoDownloader
from logging_utils import Logger
from muxer import VideoMuxer
from storage import create_run_paths, write_json
from transcriber import FasterWhisperTranscriber
from translator import build_translator
from tts import EdgeTTSGenerator


class DubbingPipeline:
    def __init__(self, config: AppConfig, logger: Logger) -> None:
        self.config = config
        self.logger = logger

    def run(self, url: str) -> None:
        started_at = perf_counter()
        paths = create_run_paths(self.config.output_dir, url)
        self.logger.stage("AutoVid Dubbing Pipeline")
        self.logger.info(f"Job directory: {paths.job_dir}")
        self.logger.info(f"Translator: {self.config.translator}")
        if self.config.translator == "groq":
            self.logger.info(f"Groq model: {self.config.groq_model}")
        if self.config.translator == "ollama":
            self.logger.info(f"Ollama model: {self.config.ollama_model}")
        self.logger.info(f"Voice: {self.config.voice}")

        if self.config.dry_run:
            self._write_summary(paths, url, started_at, status="dry_run")
            self._print_dry_run()
            return

        metadata: dict[str, Any] = {}

        self.logger.stage("1. Download")
        metadata = VideoDownloader(self.logger).download(url, paths.source_video, paths.metadata)
        if self._should_stop("download", paths, url, started_at, metadata):
            return

        self.logger.stage("2. Audio Extraction")
        AudioProcessor(self.logger).extract_wav(paths.source_video, paths.source_audio)
        if self._should_stop("audio", paths, url, started_at, metadata):
            return

        self.logger.stage("3. Transcription")
        segments = FasterWhisperTranscriber(self.config.whisper_model, self.logger).transcribe(
            paths.source_audio,
            paths.transcript_json,
            paths.transcript_txt,
        )
        if self._should_stop("transcript", paths, url, started_at, metadata, len(segments)):
            return

        self.logger.stage("4. Translation")
        translator = build_translator(self.config, self.logger)
        translated_segments = translator.translate_segments(segments)
        write_json(paths.translated_json, [segment.to_dict() for segment in translated_segments])
        self.logger.success(f"Translated {len(translated_segments)} segments")
        if self._should_stop("translation", paths, url, started_at, metadata, len(segments)):
            return

        self.logger.stage("5. Text To Speech")
        clips = EdgeTTSGenerator(self.config.voice, self.logger).synthesize(
            translated_segments,
            paths.tts_dir,
            paths.tts_manifest,
        )
        if self._should_stop("tts", paths, url, started_at, metadata, len(segments)):
            return

        self.logger.stage("6. Alignment")
        duration = metadata.get("duration_seconds")
        AudioAligner(self.logger).align(clips, paths.dubbed_audio, duration)
        if self._should_stop("alignment", paths, url, started_at, metadata, len(segments)):
            return

        self.logger.stage("7. Final Video")
        VideoMuxer(self.logger).mux(paths.source_video, paths.dubbed_audio, paths.dubbed_video)
        self._write_summary(paths, url, started_at, metadata, len(segments), status="completed")
        self.logger.success(f"Done: {paths.dubbed_video}")

    def _should_stop(
        self,
        stage: str,
        paths: Any,
        url: str,
        started_at: float,
        metadata: dict[str, Any] | None = None,
        segment_count: int = 0,
    ) -> bool:
        if self.config.stop_after != stage:
            return False
        self._write_summary(paths, url, started_at, metadata or {}, segment_count, status=f"stopped_after_{stage}")
        self.logger.warning(f"Stopped after stage: {stage}")
        return True

    def _write_summary(
        self,
        paths: Any,
        url: str,
        started_at: float,
        metadata: dict[str, Any] | None = None,
        segment_count: int = 0,
        status: str = "completed",
    ) -> None:
        elapsed = perf_counter() - started_at
        summary = {
            "status": status,
            "source_url": url,
            "job_dir": str(paths.job_dir),
            "translator": self.config.translator,
            "groq_model": self.config.groq_model if self.config.translator == "groq" else None,
            "ollama_model": self.config.ollama_model if self.config.translator == "ollama" else None,
            "voice": self.config.voice,
            "whisper_model": self.config.whisper_model,
            "duration_seconds": (metadata or {}).get("duration_seconds"),
            "segment_count": segment_count,
            "processing_time_seconds": round(elapsed, 2),
            "outputs": {
                "source_video": str(paths.source_video),
                "source_audio": str(paths.source_audio),
                "transcript_json": str(paths.transcript_json),
                "translated_json": str(paths.translated_json),
                "dubbed_audio": str(paths.dubbed_audio),
                "dubbed_video": str(paths.dubbed_video),
            },
        }
        write_json(paths.run_summary, summary)

    def _print_dry_run(self) -> None:
        stages = [
            "download video",
            "extract audio",
            "transcribe speech",
            "translate to English",
            "generate TTS",
            "align dubbed audio",
            "mux final video",
        ]
        for stage in stages:
            self.logger.info(f"Would run: {stage}")
