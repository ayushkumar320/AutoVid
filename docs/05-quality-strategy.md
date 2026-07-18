# Quality Strategy

## What Quality Means Here

The assignment will be judged on:

- Translation accuracy.
- Naturalness of the English speech.
- Timing match between video and dubbed audio.
- Code readability.
- Clarity of explanation.

## Accuracy Strategy

Use segment-level timestamps from Whisper so that each translated line remains connected to its original timing.

For translation:

- Preserve meaning, not exact word order.
- Keep translations concise enough to fit the original speaking time.
- Avoid overly formal English unless the original tone is formal.

## Timing Strategy

Each segment has:

- Start time.
- End time.
- Original duration.
- Generated TTS duration.

The aligner should place the generated segment at the original start time. If the generated speech is too long, we can apply a small speed adjustment.

Safe speed adjustment range:

```text
0.90x to 1.15x
```

Avoid aggressive speed changes because they make the voice sound unnatural.

## Voice Strategy

For the MVP:

- Use natural neural English voices from `edge-tts`.
- Let the user choose the voice.
- Use Indian English voices for Indian source videos when appropriate.

Suggested defaults:

- Male Indian English: `en-IN-PrabhatNeural`
- Female Indian English: `en-IN-NeerjaNeural`
- Male US English: `en-US-GuyNeural`
- Female US English: `en-US-JennyNeural`

## Code Quality Strategy

Keep modules small and focused:

- `downloader.py` only downloads.
- `transcriber.py` only transcribes.
- `translator.py` only translates.
- `tts.py` only generates speech.
- `aligner.py` only builds the dubbed track.
- `muxer.py` only creates the final video.

Use structured data instead of passing loose dictionaries everywhere.

Recommended data models:

```python
@dataclass
class TranscriptSegment:
    index: int
    start: float
    end: float
    text: str

@dataclass
class TranslatedSegment:
    index: int
    start: float
    end: float
    source_text: str
    english_text: str
```

## Logging Strategy

The CLI should clearly print:

- Current stage.
- Input URL.
- Download progress.
- Transcription progress.
- Number of segments translated.
- TTS progress.
- Final output path.
- Total processing time.

Good logs make the project easier to debug and also look more professional during the walkthrough.

## Risk Management

| Risk | Mitigation |
| --- | --- |
| Long videos take too much time | Test on short clips first, then run final long videos overnight |
| Translation model setup is heavy | Keep translation backend pluggable |
| TTS segments do not match timing | Use timestamp-based stitching and mild speed adjustment |
| YouTube download fails | Use `yt-dlp`, show clear error messages |
| Voice does not match original perfectly | Explain MVP uses natural voice matching, with voice cloning as future work |

