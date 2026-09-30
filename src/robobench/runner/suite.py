"""A suite: a named list of tasks (with options) to run together.

The three ways the benchmark is meant to be used map onto suites:
    run everything             standard_suite()
    run a subset               BenchmarkSuite.from_filter(robot="leap_hand"), or tags, or names
    run a custom mix           a suite YAML file
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Sequence


@dataclass
class SuiteEntry:
    task: str
    """Registry name, e.g. "leap/cube_reorientation"."""
    overrides: dict[str, Any] = field(default_factory=dict)
    """Keyword arguments for the task factory."""
    episodes: int | None = None
    """None uses RunConfig.episodes_per_task."""
    label: str | None = None
    """Name in results when the same task appears with different overrides."""
    observation_pipeline: list[dict[str, Any]] | None = None
    """Pipeline config (see `ObservationPipeline.from_config`) replacing the task's for this entry."""


@dataclass
class BenchmarkSuite:
    name: str
    entries: list[SuiteEntry]
    description: str = ""

    @classmethod
    def from_yaml(cls, path: str | Path) -> "BenchmarkSuite":
        raise NotImplementedError

    def to_yaml(self, path: str | Path) -> None:
        raise NotImplementedError

    @classmethod
    def from_filter(
        cls,
        name: str = "filtered",
        robot: str | None = None,
        tags: tuple[str, ...] = (),
        tasks: Sequence[str] | None = None,
    ) -> "BenchmarkSuite":
        """Every registered task matching the filters, with default options.

        e.g. from_filter(robot="leap_hand"), from_filter(tags=("locomotion",)).
        """
        raise NotImplementedError


def standard_suite() -> BenchmarkSuite:
    """The full benchmark: every task in the built-in library, default options."""
    raise NotImplementedError
