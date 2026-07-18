# Phase 3 - Transcription

## Goal

Transcribe extracted audio into timestamped segments.

## Implement

- `transcriber.py`.
- Faster Whisper backend.
- Transcript JSON output.
- Human-readable transcript text output.

## Expected Files

```text
outputs/<job_id>/
  transcript.json
  transcript.txt
```

## Model Recommendation

Start with:

```text
small
```

Use `medium` if quality is poor and processing time is acceptable.

## Transcript Segment Format

```json
{
  "index": 0,
  "start": 1.25,
  "end": 4.80,
  "text": "Detected source speech",
  "language": "hi"
}
```

## Acceptance Checks

Run:

```bash
python -m autovid "YOUTUBE_URL" --stop-after transcript
```

Expected:

- `transcript.json` exists.
- `transcript.txt` exists.
- Segments contain start time, end time, and text.
- Logs show detected language and segment count.

## Codex Prompt

```text
Implement Phase 3 from docs/build/03-transcription.md.

Add a Faster Whisper transcription backend in autovid/transcriber.py. Wire it into the pipeline after audio extraction. Save transcript.json and transcript.txt. Add --whisper-model with default small and --stop-after transcript. Use the existing dataclasses or add clean dataclasses if needed. Print detected language, segment count, and output paths.
```

