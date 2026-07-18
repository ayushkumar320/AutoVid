# Assignment Understanding

## Goal

Build a Python script that converts a YouTube video in any supported spoken language into an English-dubbed video.

The final output should preserve the original video while replacing the original audio with English speech.

## Required Features

The script must:

- Accept a YouTube URL as input.
- Download the video.
- Transcribe the original speech.
- Translate the speech into English.
- Synthesize natural-sounding English speech.
- Replace the original audio with dubbed English audio.
- Save the final dubbed video to disk.
- Print progress to the terminal during processing.

## Submission Requirements

The final email submission should include:

- A dubbed output for one video around 30 minutes long.
- A dubbed output for one video around 2 hours long.
- The source video details for both runs.
- The final dubbed video files.
- The processing time for each video.
- A 2 minute walkthrough video explaining the architecture and decisions.

## Evaluation Criteria

The assignment will be judged on only two major areas:

- Accuracy: translation quality, naturalness of the English voice, and timing alignment.
- Code quality and clarity: readable code, clean architecture, and a clear explanation.

## Practical Interpretation

The most important thing is to ship a reliable end-to-end pipeline before improving advanced features. A working system with clear structure is better than an ambitious voice-cloning system that is unstable.

The core project should focus on:

- Reliable video download.
- Segment-level transcription with timestamps.
- Meaning-preserving English translation.
- Natural TTS voice generation.
- Good enough timing alignment.
- Clear logs and outputs.

