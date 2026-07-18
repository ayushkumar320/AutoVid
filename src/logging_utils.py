from __future__ import annotations

from contextlib import contextmanager
from time import perf_counter
from typing import Iterator


try:
    from rich.console import Console
except ImportError:  # pragma: no cover - fallback for partial environments
    Console = None


class Logger:
    def __init__(self) -> None:
        self._console = Console() if Console else None

    def info(self, message: str) -> None:
        self._print(f"[info] {message}")

    def success(self, message: str) -> None:
        self._print(f"[ok] {message}")

    def warning(self, message: str) -> None:
        self._print(f"[warn] {message}")

    def error(self, message: str) -> None:
        self._print(f"[error] {message}")

    def stage(self, name: str) -> None:
        self._print(f"\n=== {name} ===")

    def _print(self, message: str) -> None:
        if self._console:
            self._console.print(message, markup=False)
        else:
            print(message)


@contextmanager
def timed(label: str, logger: Logger) -> Iterator[dict[str, float]]:
    start = perf_counter()
    data: dict[str, float] = {"seconds": 0.0}
    logger.info(f"Starting {label}")
    try:
        yield data
    finally:
        data["seconds"] = perf_counter() - start
        logger.success(f"Finished {label} in {data['seconds']:.1f}s")
