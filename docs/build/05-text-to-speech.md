# Phase 5 - Text To Speech

## Goal

Generate natural English speech audio for translated segments.

## Implement

- `tts.py`.
- `edge-tts` backend.
- One audio file per segment.
- Voice selection.
- TTS manifest.

## Expected Files

```text
outputs/<job_id>/
  tts_segments/
    0000.mp3
    0001.mp3
    0002.mp3
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
python -m autovid "YOUTUBE_URL" --translator passthrough --stop-after tts
```

Expected:

- `tts_segments/` contains one file per translated segment.
- `tts_manifest.json` maps segment index to audio file path.
- Logs show TTS progress.

## Codex Prompt

```text
Implement Phase 5 from docs/build/05-text-to-speech.md.

Add edge-tts based speech synthesis in autovid/tts.py. Generate one MP3 file per translated segment, save a tts_manifest.json, and wire this into the pipeline. Add --voice with default en-IN-PrabhatNeural and --stop-after tts. Use async edge-tts cleanly from the synchronous pipeline.
```

