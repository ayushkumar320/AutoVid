# AutoVid Documentation

This folder explains the internship assignment, the proposed solution, and the implementation plan for the automated video dubbing system.

Read the docs in this order:

1. [Assignment Understanding](./01-assignment-understanding.md)
2. [Core Architecture](./02-core-architecture.md)
3. [Tech Stack](./03-tech-stack.md)
4. [Build Plan](./04-build-plan.md)
5. [Quality Strategy](./05-quality-strategy.md)
6. [Architecture Alternatives](./06-architecture-alternatives.md)
7. [Walkthrough Talking Points](./07-walkthrough-talking-points.md)

For implementation, use the phase-wise build playbook:

- [Build Playbook](./build/README.md)
- [LLM and Translation Strategy](./build/00-llm-and-translation-strategy.md)
- [Phase 1 - Project Scaffold](./build/01-project-scaffold.md)
- [Phase 2 - Download and Audio Extraction](./build/02-download-and-audio-extraction.md)
- [Phase 3 - Transcription](./build/03-transcription.md)
- [Phase 4 - Translation](./build/04-translation.md)
- [Phase 5 - Text To Speech](./build/05-text-to-speech.md)
- [Phase 6 - Alignment and Muxing](./build/06-alignment-and-muxing.md)
- [Phase 7 - Validation and Submission](./build/07-validation-and-submission.md)

The main idea is to build a local Python pipeline that takes a YouTube URL, downloads the video, transcribes and translates the speech into English, generates English speech, aligns the new audio to the original timing, and outputs a dubbed video.
