# Phase 5 - Text To Speech

## Goal

Generate natural English speech audio for translated segments.

## Implement

- `tts.py`.
- `edge-tts` backend.
- One audio file per segment.
- Voice selection.
- Expressive rate, pitch, and volume tuning from original audio energy.
- TTS manifest.

## Expected Files

```text
outputs/<job_id>/
  tts_segments/
    0000.mp3
    0001.mp3
    0002.mp3
  energy_profiles.json
  tts_manifest.json
```

## Recommended Voices

```text
en-IN-PrabhatNeural
en-IN-NeerjaNeural
en-US-GuyNeural
en-US-JennyNeural
```

Default:

```text
en-IN-PrabhatNeural
```

## Acceptance Checks

Run:

```bash
uv run autovid "YOUTUBE_URL" --translator passthrough --stop-after tts
```

Expected:

- `tts_segments/` contains one file per translated segment.
- `energy_profiles.json` records the original energy-to-TTS settings.
- `tts_manifest.json` maps segment index to audio file path.
- Logs show TTS progress.

## Codex Prompt

```text
Implement Phase 5 from docs/build/05-text-to-speech.md.

Add edge-tts based speech synthesis in src/tts.py. Generate one MP3 file per translated segment, save a tts_manifest.json, and wire this into the pipeline. Add expressive TTS by analyzing original segment loudness and pace, then mapping that to edge-tts rate, pitch, and volume. Add --voice with default en-IN-PrabhatNeural, --flat-tts to disable expressive tuning, and --stop-after tts. Use async edge-tts cleanly from the synchronous pipeline.
```
