from __future__ import annotations

import argparse
import sys

from config import AppConfig, STOP_STAGES
from logging_utils import Logger
from pipeline import DubbingPipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="autovid",
        description="Download a YouTube video and create an English-dubbed output.",
    )
    parser.add_argument("url", help="YouTube URL to dub into English.")
    parser.add_argument("--output-dir", default="outputs", help="Directory for generated job outputs.")
    parser.add_argument(
        "--translator",
        default=None,
        choices=["passthrough", "ollama", "groq"],
        help="Translation backend. Defaults to AUTOVID_TRANSLATOR or groq.",
    )
    parser.add_argument("--voice", default=None, help="edge-tts voice name.")
    parser.add_argument("--whisper-model", default=None, help="Faster Whisper model size or path.")
    parser.add_argument("--ollama-url", default=None, help="Ollama base URL.")
    parser.add_argument("--ollama-model", default=None, help="Ollama model name.")
    parser.add_argument("--groq-model", default=None, help="Groq model name.")
    parser.add_argument("--batch-size", type=int, default=20, help="Translation segment batch size.")
    parser.add_argument("--dry-run", action="store_true", help="Create job folder and print stages only.")
    parser.add_argument("--flat-tts", action="store_true", help="Disable energy-based TTS rate/pitch/volume tuning.")
    parser.add_argument(
        "--stop-after",
        choices=sorted(STOP_STAGES),
        default=None,
        help="Stop after a pipeline stage for incremental testing.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    logger = Logger()

    try:
        config = AppConfig.from_args(args)
        pipeline = DubbingPipeline(config=config, logger=logger)
        pipeline.run(args.url)
    except KeyboardInterrupt:
        logger.warning("Interrupted by user.")
        return 130
    except Exception as exc:
        logger.error(str(exc))
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
