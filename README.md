# AutoVid

AutoVid is a local Python dubbing pipeline for the internship assignment. It accepts a YouTube URL, downloads the video, transcribes speech, translates it into English, generates English TTS audio, aligns the new audio to the original timing, and outputs a dubbed video.

## Requirements

- `uv`
- `ffmpeg`
- Groq API key for default translation
- Ollama, optional local fallback

Install `ffmpeg` on macOS:

```bash
brew install ffmpeg
```

Install dependencies:

```bash
uv sync
```

Default Groq setup:

```bash
export GROQ_API_KEY="your_groq_api_key"
```

Or create a local `.env` file:

```text
GROQ_API_KEY=your_groq_api_key
```

Optional Ollama fallback model:

```bash
ollama pull qwen2.5:7b
```

## Usage

Dry run:

```bash
uv run autovid "https://www.youtube.com/watch?v=..." --dry-run
```

Run with default Groq translation:

```bash
uv run autovid "https://www.youtube.com/watch?v=..."
```

Run with a specific Groq model:

```bash
uv run autovid "https://www.youtube.com/watch?v=..." --groq-model qwen/qwen3.6-27b
```

Run with local Ollama translation:

```bash
uv run autovid "https://www.youtube.com/watch?v=..." --translator ollama --ollama-model qwen2.5:7b
```

Run with passthrough translation for English test videos:

```bash
uv run autovid "https://www.youtube.com/watch?v=..." --translator passthrough
```

Expressive TTS is enabled by default. It analyzes original segment energy and adjusts TTS rate, pitch, and volume. Disable it with:

```bash
uv run autovid "https://www.youtube.com/watch?v=..." --flat-tts
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
  energy_profiles.json
  tts_segments/
  tts_manifest.json
  dubbed.wav
  dubbed_output.mp4
  run_summary.json
```

## Translation Backends

- `passthrough`: testing only, returns original transcript text.
- `groq`: default fast cloud backend using `GROQ_API_KEY`.
- `ollama`: optional free local translation backend.

OpenAI is not required for the MVP.
