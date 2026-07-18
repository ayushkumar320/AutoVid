# Phase 6 - Alignment and Muxing

## Goal

Create one full dubbed audio track and combine it with the original video.

## Implement

- `aligner.py`.
- `muxer.py`.
- Silence insertion based on timestamps.
- Optional mild speed adjustment.
- Final video output.

## Expected Files

```text
outputs/<job_id>/
  dubbed.wav
  dubbed_output.mp4
```

## Alignment Method

For each translated segment:

1. Read original `start` and `end`.
2. Place TTS audio at `start`.
3. Add silence between segments.
4. Keep total audio duration close to the video duration.

## Speed Adjustment

If a TTS clip is much longer than the original segment, adjust speed gently.

Recommended range:

```text
0.90x to 1.15x
```

Avoid extreme speed changes because they make speech unnatural.

## Final Mux Command

Use `ffmpeg` to copy video and replace audio:

```bash
ffmpeg -i source.mp4 -i dubbed.wav -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -shortest dubbed_output.mp4
```

## Acceptance Checks

Run:

```bash
python -m autovid "YOUTUBE_URL" --translator passthrough
```

Expected:

- `dubbed.wav` exists.
- `dubbed_output.mp4` exists.
- Final video is playable.
- Original visuals are preserved.
- Audio starts at the expected time.

## Codex Prompt

```text
Implement Phase 6 from docs/build/06-alignment-and-muxing.md.

Add aligner.py to stitch per-segment TTS audio into dubbed.wav using original timestamps and silence insertion. Add muxer.py to replace the source video audio with dubbed.wav using ffmpeg while copying the video stream. Wire both into the pipeline and save dubbed_output.mp4. Add clear logs and include output paths in the final summary.
```

