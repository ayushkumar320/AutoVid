# Walkthrough Talking Points

Use this doc to prepare the 2 minute submission walkthrough video.

## Suggested Structure

### 1. Problem Statement

"The goal of this project is to take a YouTube video in another language and generate an English-dubbed version while preserving the original video."

### 2. Architecture Summary

"I built the system as a staged Python pipeline. Each stage produces an output that the next stage consumes, which makes the system easier to debug and scale."

Mention the main stages:

- Download.
- Extract audio.
- Transcribe.
- Translate.
- Generate speech.
- Align audio.
- Replace original audio.

### 3. Why This Architecture

"I compared a few possible architectures, including a single monolithic script, a cloud API pipeline, a batch processing system, a streaming system, and a voice-cloning pipeline. I chose a modular local pipeline because it gives the best balance of reliability, code clarity, and deadline safety."

### 4. Tool Choices

"I used `yt-dlp` for reliable YouTube downloads, `ffmpeg` for audio and video processing, Whisper for transcription with timestamps, and `edge-tts` for natural English speech synthesis."

### 5. Timing Approach

"The important part of dubbing is timing. Whisper gives timestamps for every spoken segment, so I generate English TTS per segment and place each clip back at the original timestamp."

### 6. Quality Tradeoff

"The assignment mentions matching the same voice and energy. For the core version, I focused on stable natural TTS and timing alignment. The architecture keeps TTS separate, so a voice-cloning model like XTTS can be added later without rewriting the whole pipeline."

### 7. Demo Results

Show:

- Source video.
- Final dubbed video.
- Processing time.
- A short before and after comparison.

### 8. Closing

"The main design decision was to keep every stage modular, so failures are easy to isolate and improvements like better translation, speaker diarization, or voice cloning can be added later."

## One-Minute Architecture Script

```text
The system starts with a YouTube URL. I download the source video using yt-dlp, then use ffmpeg to extract the audio as a clean WAV file. That audio goes into Whisper, which produces timestamped transcript segments. Each segment is translated into natural English, then converted into speech using a neural English TTS voice. Instead of generating one huge audio file blindly, I generate audio per segment and place it back according to the original timestamps. Finally, I use ffmpeg to replace the original audio track with the generated English dub while keeping the original video stream unchanged.
```

## Strong Points To Emphasize

- Modular architecture.
- Timestamp-based alignment.
- Clear intermediate outputs.
- Practical MVP completed before advanced features.
- Future-ready design for voice cloning and multi-speaker support.

