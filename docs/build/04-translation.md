# Phase 4 - Translation

## Goal

Translate transcript segments into natural English.

## Implement

- `translator.py`.
- Provider interface.
- Ollama backend.
- Passthrough backend for testing English videos.
- Optional Groq/OpenAI backend later.
- Batch translation to reduce calls.

## Expected Files

```text
outputs/<job_id>/
  translated_segments.json
```

## Recommended Backends

```text
passthrough
ollama
groq
openai
```

Implement in this order:

1. `passthrough`
2. `ollama`
3. `groq` if needed
4. `openai` only if you choose to use a paid/high quality API

## Ollama Integration

Ollama usually runs locally at:

```text
http://localhost:11434
```

Recommended model:

```text
qwen2.5:7b
```

## Acceptance Checks

Run with passthrough:

```bash
python -m autovid "YOUTUBE_URL" --translator passthrough --stop-after translation
```

Run with Ollama:

```bash
python -m autovid "YOUTUBE_URL" --translator ollama --ollama-model qwen2.5:7b --stop-after translation
```

Expected:

- `translated_segments.json` exists.
- Each segment has `english_text`.
- Translation preserves segment indexes.
- If Ollama is not running, the error message explains how to start it.

## Codex Prompt

```text
Implement Phase 4 from docs/build/04-translation.md.

Add a translator interface with passthrough and Ollama backends. The Ollama backend should call the local Ollama HTTP API, batch transcript segments, ask for valid JSON only, parse responses robustly, and save translated_segments.json. Add CLI options --translator, --ollama-url, --ollama-model, and --stop-after translation. Keep Groq/OpenAI as clean future extension points, but do not require paid APIs.
```

