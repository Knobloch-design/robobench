"""Writing results to disk.

Layout of one run directory:
    <output_dir>/<run_id>/
        metadata.json
        episodes.jsonl        one EpisodeRecord per line, appended as episodes finish
        episodes.csv          one row per episode: ids, modes, outcome, every metric
        violations.csv        one row per limit violation
        invalid_commands.csv  one row per invalid-command event
        summary.json          aggregates and failure breakdown
        recordings/           Meshcat HTML replays
        controller_logs/      controller stdout/stderr per worker
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING, Sequence

if TYPE_CHECKING:
    from robobench.results.records import EpisodeRecord, RunMetadata, RunRecord


class ResultWriter(ABC):
    def __init__(self, run_dir: Path) -> None:
        self.run_dir = run_dir

    @abstractmethod
    def write_metadata(self, metadata: "RunMetadata") -> None: ...

    @abstractmethod
    def append_episode(self, record: "EpisodeRecord") -> None:
        """Called as each episode finishes."""

    @abstractmethod
    def finalize(self, run: "RunRecord") -> None:
        """Write summaries once the run is done."""


class JsonWriter(ResultWriter):
    def write_metadata(self, metadata) -> None:
        raise NotImplementedError

    def append_episode(self, record) -> None:
        raise NotImplementedError

    def finalize(self, run) -> None:
        raise NotImplementedError


class CsvWriter(ResultWriter):
    def write_metadata(self, metadata) -> None:
        raise NotImplementedError

    def append_episode(self, record) -> None:
        raise NotImplementedError

    def finalize(self, run) -> None:
        raise NotImplementedError


def make_writers(run_dir: Path, formats: Sequence[str] = ("json", "csv")) -> list[ResultWriter]:
    raise NotImplementedError


def load_run(run_dir: str | Path) -> "RunRecord":
    """Read a run back (for comparison, plotting, or `BenchmarkRunner.resume`)."""
    raise NotImplementedError
