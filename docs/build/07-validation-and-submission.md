# Phase 7 - Validation and Submission

## Goal

Validate the pipeline and prepare submission artifacts.

## Implement

- `run_summary.json`.
- Processing time tracking.
- Basic validation checks.
- README usage examples.
- Walkthrough notes.

## Expected Files

```text
outputs/<job_id>/
  run_summary.json
```

## Run Summary Fields

```json
{
  "source_url": "...",
  "job_id": "...",
  "translator": "groq",
  "voice": "en-US-JennyNeural",
  "duration_seconds": 1800,
  "segment_count": 320,
  "processing_time_seconds": 4200,
  "outputs": {
    "source_video": "source.mp4",
    "dubbed_audio": "dubbed.wav",
    "dubbed_video": "dubbed_output.mp4"
  }
}
```

## Validation Checklist

- Video downloads correctly.
- Audio extraction succeeds.
- Transcript has meaningful segments.
- Translation output is English and natural.
- TTS files are generated for all segments.
- Dubbed audio duration is close to video duration.
- Final video plays correctly.
- Processing time is recorded.

## Submission Checklist

For each of the two final videos:

- Source video URL.
- Source video file or source link.
- Dubbed output video.
- Processing time.
- Notes on translation/TTS backend used.

Also prepare:

- 2 minute walkthrough video.
- Short architecture explanation.
- Mention chosen architecture and tradeoffs.

## Codex Prompt

```text
Implement Phase 7 from docs/build/07-validation-and-submission.md.

Add run summary tracking, processing time measurements, validation checks, and final CLI summary output. Update README.md with setup, usage, output folder structure, backend options, and submission notes. Make sure the project clearly records source URL, translator, voice, segment count, output paths, and total processing time.
```
