from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path


STOP_STAGES = {
    "download",
    "audio",
    "transcript",
    "translation",
    "tts",
    "alignment",
    "mux",
}


@dataclass(frozen=True)
class AppConfig:
    output_dir: Path
    translator: str
    voice: str
    whisper_model: str
    ollama_url: str
    ollama_model: str
    groq_model: str
    stop_after: str | None
    dry_run: bool
    batch_size: int

    @classmethod
    def from_args(cls, args: object) -> "AppConfig":
        load_dotenv(Path.cwd() / ".env")
        translator = getattr(args, "translator", None) or os.getenv("AUTOVID_TRANSLATOR", "groq")
        voice = getattr(args, "voice", None) or os.getenv("AUTOVID_VOICE", "en-IN-PrabhatNeural")
        whisper_model = getattr(args, "whisper_model", None) or os.getenv("AUTOVID_WHISPER_MODEL", "small")
        ollama_url = getattr(args, "ollama_url", None) or os.getenv("OLLAMA_URL", "http://localhost:11434")
        ollama_model = getattr(args, "ollama_model", None) or os.getenv("OLLAMA_MODEL", "qwen2.5:7b")
        groq_model = getattr(args, "groq_model", None) or os.getenv("GROQ_MODEL", "qwen/qwen3.6-27b")
        output_dir = Path(getattr(args, "output_dir", "outputs")).expanduser().resolve()
        stop_after = getattr(args, "stop_after", None)
        batch_size = int(getattr(args, "batch_size", 20))

        if stop_after and stop_after not in STOP_STAGES:
            allowed = ", ".join(sorted(STOP_STAGES))
            raise ValueError(f"Invalid --stop-after '{stop_after}'. Choose one of: {allowed}")

        return cls(
            output_dir=output_dir,
            translator=translator,
            voice=voice,
            whisper_model=whisper_model,
            ollama_url=ollama_url.rstrip("/"),
            ollama_model=ollama_model,
            groq_model=groq_model,
            stop_after=stop_after,
            dry_run=bool(getattr(args, "dry_run", False)),
            batch_size=batch_size,
        )


def load_dotenv(path: Path) -> None:
    if not path.exists():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")

        if key:
            os.environ.setdefault(key, value)
