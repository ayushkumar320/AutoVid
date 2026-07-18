# Tech Stack

## Language

Python is the main language because the assignment asks for a Python script and because most AI audio/video tools have strong Python support.

## Core Tools

| Area | Tool | Why |
| --- | --- | --- |
| Video download | `yt-dlp` | Reliable YouTube downloading and metadata extraction |
| Audio/video processing | `ffmpeg` | Industry-standard tool for extracting and replacing audio |
| Transcription | `faster-whisper` | Faster Whisper inference with segment timestamps |
| Translation | Pluggable translator | Lets us switch between API and local model approaches |
| Text-to-speech | `edge-tts` | Free, natural-sounding English neural voices |
| Audio stitching | `pydub` | Simple silence insertion and audio composition |
| Terminal logs | `rich` | Clean progress messages and readable CLI output |

## Recommended Python Packages

```text
yt-dlp
faster-whisper
edge-tts
pydub
rich
```

Optional packages for local translation:

```text
transformers
sentencepiece
torch
indic-nlp-library
```

## System Dependencies

`ffmpeg` is required.

Check installation:

```bash
ffmpeg -version
```

On macOS, it can be installed with:

```bash
brew install ffmpeg
```

## Translation Options

### Option A: API-Based Translation

Use an LLM or translation API to convert transcript segments into English.

Pros:

- Usually better natural phrasing.
- Easier to set up.
- Good for submission quality.

Cons:

- May require API keys.
- Processing long videos can cost money.

### Option B: Local Translation Model

Use open-source models from Hugging Face, such as IndicTrans2 for Indian languages.

Pros:

- Free after setup.
- Works offline once models are downloaded.
- Strong fit for Indian languages.

Cons:

- Heavier installation.
- More GPU/CPU requirements.
- More setup risk before the deadline.

## TTS Voice Strategy

The assignment asks for "same voice, same energy." The MVP will not do true voice cloning. Instead, it will:

- Use natural English neural voices.
- Allow choosing male, female, and Indian English voices.
- Preserve segment timing and pacing as much as possible.

Possible `edge-tts` voices:

- `en-US-GuyNeural`
- `en-US-JennyNeural`
- `en-IN-PrabhatNeural`
- `en-IN-NeerjaNeural`

## Optional Advanced Stack

If the core pipeline is finished early, voice cloning can be explored.

Possible tools:

- Coqui XTTS
- RVC
- pyannote.audio for speaker diarization

These are stretch goals, not required for the first reliable submission.

