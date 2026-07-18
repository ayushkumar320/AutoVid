# AutoVid

AutoVid is a local Python dubbing pipeline for the internship assignment. It accepts a YouTube URL, downloads the video, transcribes speech, translates it into English, generates English TTS audio, aligns the new audio to the original timing, and outputs a dubbed video.

## Requirements

- `uv`
- `ffmpeg`
- Ollama, optional but recommended for free local translation

Install `ffmpeg` on macOS:

```bash
brew install ffmpeg
```

Install dependencies:

```bash
uv sync
```

Optional Ollama model:

```bash
ollama pull qwen2.5:7b
```

## Usage

Dry run:

```bash
uv run autovid "https://www.youtube.com/watch?v=..." --dry-run
```

Run with local Ollama translation:

```bash
uv run autovid "https://www.youtube.com/watch?v=..." --translator ollama --ollama-model qwen2.5:7b
```

Run with passthrough translation for English test videos:

```bash
uv run autovid "https://www.youtube.com/watch?v=..." --translator passthrough
```

Stop after a stage:

```bash
uv run autovid "https://www.youtube.com/watch?v=..." --stop-after transcript
```

## Source Layout

The implementation uses a flat `src` layout:

```text
src/
  cli.py
  config.py
  pipeline.py
  downloader.py
  audio.py
  transcriber.py
  translator.py
  tts.py
  aligner.py
  muxer.py
  models.py
  storage.py
  process.py
```

This keeps the root folder focused on project files while the application code stays isolated under `src`.

## Output

Each run creates:

```text
outputs/<job_id>/
  source.mp4
  source.wav
  metadata.json
  transcript.json
  transcript.txt
  translated_segments.json
  tts_segments/
  tts_manifest.json
  dubbed.wav
  dubbed_output.mp4
  run_summary.json
```

## Translation Backends

- `passthrough`: testing only, returns original transcript text.
- `ollama`: recommended free local translation backend.
- `groq`: optional fast cloud backend using `GROQ_API_KEY`.

OpenAI is not required for the MVP.
