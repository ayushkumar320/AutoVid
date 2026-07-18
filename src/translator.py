from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.request
from typing import Any, Protocol

from config import AppConfig
from logging_utils import Logger
from models import TranscriptSegment, TranslatedSegment


class Translator(Protocol):
    def translate_segments(self, segments: list[TranscriptSegment]) -> list[TranslatedSegment]:
        ...


class PassthroughTranslator:
    def translate_segments(self, segments: list[TranscriptSegment]) -> list[TranslatedSegment]:
        return [
            TranslatedSegment(
                index=segment.index,
                start=segment.start,
                end=segment.end,
                source_text=segment.text,
                english_text=segment.text,
                language=segment.language,
            )
            for segment in segments
        ]


class PromptBuilder:
    @staticmethod
    def translation_prompt(batch: list[TranscriptSegment]) -> str:
        data = [
            {"index": item.index, "start": item.start, "end": item.end, "text": item.text}
            for item in batch
        ]
        return (
            "You are translating video speech into natural spoken English for dubbing.\n\n"
            "Rules:\n"
            "- Preserve meaning.\n"
            "- Use natural conversational English.\n"
            "- Keep each translation concise so it can fit the original timing.\n"
            "- Do not add explanations.\n"
            "- Return valid JSON only.\n\n"
            f"Input segments:\n{json.dumps(data, ensure_ascii=False)}\n\n"
            'Return exactly this shape: [{"index": 0, "english_text": "..."}]'
        )


class OllamaTranslator:
    def __init__(self, base_url: str, model: str, batch_size: int, logger: Logger) -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.batch_size = batch_size
        self.logger = logger

    def translate_segments(self, segments: list[TranscriptSegment]) -> list[TranslatedSegment]:
        translated: list[TranslatedSegment] = []
        for offset in range(0, len(segments), self.batch_size):
            batch = segments[offset : offset + self.batch_size]
            self.logger.info(f"Translating batch {offset // self.batch_size + 1}")
            response = self._generate(PromptBuilder.translation_prompt(batch))
            translated.extend(build_translated_segments(batch, response, self.logger))
        return translated

    def _generate(self, prompt: str) -> str:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.1},
        }
        request = urllib.request.Request(
            f"{self.base_url}/api/generate",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=180) as response:
                data = json.loads(response.read().decode("utf-8"))
        except urllib.error.URLError as exc:
            raise RuntimeError(
                "Could not connect to Ollama. Start Ollama and pull a model, for example: "
                "ollama pull qwen2.5:7b"
            ) from exc
        return str(data.get("response", ""))


class GroqTranslator:
    def __init__(self, model: str, batch_size: int, logger: Logger) -> None:
        self.model = model
        self.batch_size = batch_size
        self.logger = logger
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise RuntimeError("GROQ_API_KEY is required when --translator groq is used.")

    def translate_segments(self, segments: list[TranscriptSegment]) -> list[TranslatedSegment]:
        translated: list[TranslatedSegment] = []
        for offset in range(0, len(segments), self.batch_size):
            batch = segments[offset : offset + self.batch_size]
            self.logger.info(f"Translating Groq batch {offset // self.batch_size + 1}")
            response = self._chat(PromptBuilder.translation_prompt(batch))
            translated.extend(build_translated_segments(batch, response, self.logger))
        return translated

    def _chat(self, prompt: str) -> str:
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.1,
        }
        request = urllib.request.Request(
            "https://api.groq.com/openai/v1/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=180) as response:
                data = json.loads(response.read().decode("utf-8"))
        except urllib.error.URLError as exc:
            raise RuntimeError("Groq translation request failed. Check your API key, model, and network.") from exc
        return str(data["choices"][0]["message"]["content"])


def build_translator(config: AppConfig, logger: Logger) -> Translator:
    if config.translator == "passthrough":
        logger.warning("Using passthrough translator; output will not be translated.")
        return PassthroughTranslator()
    if config.translator == "ollama":
        return OllamaTranslator(config.ollama_url, config.ollama_model, config.batch_size, logger)
    if config.translator == "groq":
        return GroqTranslator(config.groq_model, config.batch_size, logger)
    raise ValueError(f"Unknown translator backend: {config.translator}")


def build_translated_segments(
    batch: list[TranscriptSegment], response: str, logger: Logger
) -> list[TranslatedSegment]:
    items = parse_json_array(response)
    by_index = {int(item["index"]): str(item["english_text"]).strip() for item in items}
    output: list[TranslatedSegment] = []
    for segment in batch:
        english = by_index.get(segment.index)
        if not english:
            english = segment.text
            logger.warning(f"Missing translation for segment {segment.index}; using source text")
        output.append(
            TranslatedSegment(
                index=segment.index,
                start=segment.start,
                end=segment.end,
                source_text=segment.text,
                english_text=english,
                language=segment.language,
            )
        )
    return output


def parse_json_array(text: str) -> list[dict[str, Any]]:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?", "", cleaned).strip()
        cleaned = re.sub(r"```$", "", cleaned).strip()

    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"\[[\s\S]*\]", cleaned)
        if not match:
            raise RuntimeError(f"Translator did not return JSON: {text[:500]}")
        data = json.loads(match.group(0))

    if not isinstance(data, list):
        raise RuntimeError("Translator response must be a JSON array.")
    return data

