# Phase 1 - Project Scaffold

## Goal

Create a clean uv-based Python project structure for the dubbing pipeline.

## Implement

- Flat source modules under `src/`.
- CLI entrypoint.
- Shared data models.
- Configuration loading.
- Output directory structure.
- Basic logging.

## Expected Files

```text
src/
  __init__.py
  __main__.py
  cli.py
  config.py
  models.py
  pipeline.py
  logging_utils.py
pyproject.toml
README.md
outputs/
```

## Acceptance Checks

Run:

```bash
uv run autovid --help
```

Expected:

- CLI help is printed.
- No import errors.

Run:

```bash
uv run autovid "https://example.com/video"
```

Expected:

- The script prints planned stages.
- It creates an output job folder.
- It can run in dry-run mode before real processing is implemented.

## Codex Prompt

```text
Implement Phase 1 from docs/build/01-project-scaffold.md.

Create a clean uv Python project using a flat src layout. Put application modules directly under src with CLI support, config loading, shared dataclasses, logging helpers, and a placeholder pipeline. The command should support a YouTube URL argument, --output-dir, --translator, --voice, and --dry-run. Add pyproject.toml and a root README.md with setup and usage instructions. Keep the code modular and ready for later phases.
```
