# Phase 1 - Project Scaffold

## Goal

Create a clean Python project structure for the dubbing pipeline.

## Implement

- Python package named `autovid`.
- CLI entrypoint.
- Shared data models.
- Configuration loading.
- Output directory structure.
- Basic logging.

## Expected Files

```text
autovid/
  __init__.py
  __main__.py
  cli.py
  config.py
  models.py
  pipeline.py
  logging_utils.py
requirements.txt
README.md
outputs/
```

## Acceptance Checks

Run:

```bash
python -m autovid --help
```

Expected:

- CLI help is printed.
- No import errors.

Run:

```bash
python -m autovid "https://example.com/video"
```

Expected:

- The script prints planned stages.
- It creates an output job folder.
- It can run in dry-run mode before real processing is implemented.

## Codex Prompt

```text
Implement Phase 1 from docs/build/01-project-scaffold.md.

Create a clean Python package named autovid with CLI support, config loading, shared dataclasses, logging helpers, and a placeholder pipeline. The command should support a YouTube URL argument, --output-dir, --translator, --voice, and --dry-run. Add requirements.txt and a root README.md with setup and usage instructions. Keep the code modular and ready for later phases.
```

