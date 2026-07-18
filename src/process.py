from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


class CommandError(RuntimeError):
    pass


def require_binary(name: str) -> str:
    path = shutil.which(name)
    if not path:
        raise CommandError(
            f"Required binary '{name}' was not found. Install it first, then rerun this command."
        )
    return path


def run_command(args: list[str], cwd: Path | None = None) -> None:
    try:
        subprocess.run(
            args,
            cwd=cwd,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except FileNotFoundError as exc:
        raise CommandError(f"Command not found: {args[0]}") from exc
    except subprocess.CalledProcessError as exc:
        detail = exc.stderr.strip() or exc.stdout.strip()
        raise CommandError(f"Command failed: {' '.join(args)}\n{detail}") from exc

