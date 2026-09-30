"""A suite: a named list of scenarios (with options) to run together."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class SuiteEntry:
    scenario: str
    """Registry name, e.g. "leap/cube_reorientation"."""
    overrides: dict[str, Any] = field(default_factory=dict)
    """Keyword arguments for the scenario factory."""
    episodes: int | None = None
    """None uses RunConfig.episodes_per_scenario."""
    label: str | None = None
    """Name in results when the same scenario appears with different overrides."""
    observation_pipeline: list[dict[str, Any]] | None = None
    """Pipeline config (see `ObservationPipeline.from_config`) replacing the scenario's for this entry."""


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
    def from_tags(cls, name: str, tags: tuple[str, ...]) -> "BenchmarkSuite":
        """Every registered scenario with all `tags`, default options."""
        raise NotImplementedError


def standard_suite(robot: str | None = None) -> BenchmarkSuite:
    """The shipped suite, optionally for one robot ("unitree_g1", "leap_hand", "trossen_stationary_ai")."""
    raise NotImplementedError
