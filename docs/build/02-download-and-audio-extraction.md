# Phase 2 - Download and Audio Extraction

## Goal

Download the YouTube video and extract clean audio for transcription.

## Implement

- `downloader.py` using `yt-dlp`.
- `audio.py` using `ffmpeg`.
- Save metadata.
- Add progress logs.

## Expected Files

```text
src/
  downloader.py
  audio.py
outputs/<job_id>/
  source.mp4
  source.wav
  metadata.json
```

## Download Rules

Use `yt-dlp` to download a video format compatible with `ffmpeg`.

Prefer:

```text
bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best
```

## Audio Rules

Extract WAV audio:

```text
mono, 16 kHz, PCM WAV
```

This is friendly for Whisper.

## Acceptance Checks

Run with a short video:

```bash
uv run autovid "YOUTUBE_URL" --stop-after audio
```

Expected:

- `source.mp4` exists.
- `source.wav` exists.
- `metadata.json` contains URL, title, duration, and download time if available.
- Logs clearly show download and extraction stages.

## Codex Prompt

```text
Implement Phase 2 from docs/build/02-download-and-audio-extraction.md.

Add yt-dlp based video downloading and ffmpeg based audio extraction. Create src/downloader.py and src/audio.py, wire them into the pipeline, and add a --stop-after audio option so the pipeline can stop after source.wav is produced. Save metadata.json in the job output folder. Use subprocess safely and print clear progress logs.
```
