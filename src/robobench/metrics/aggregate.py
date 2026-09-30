"""Summaries across many episodes."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Mapping, Sequence

if TYPE_CHECKING:
    from robobench.results.records import EpisodeRecord


@dataclass(frozen=True)
class MetricSummary:
    n: int
    """Episodes with a finite value (e.g. time_to_completion is NaN for failures)."""
    mean: float
    std: float
    median: float
    min: float
    max: float
    ci95_low: float
    ci95_high: float


def summarize(values: Sequence[float]) -> MetricSummary:
    """Summary stats over finite values; CI by bootstrap."""
    raise NotImplementedError


def aggregate_episodes(episodes: Sequence["EpisodeRecord"]) -> Mapping[str, Mapping[str, MetricSummary]]:
    """{scenario name: {metric name: summary}}. Episodes that failed for controller reasons
    (crash, timeout, invalid command) count as failures, not as missing data."""
    raise NotImplementedError


def failure_breakdown(episodes: Sequence["EpisodeRecord"]) -> Mapping[str, Mapping[str, int]]:
    """{scenario name: {termination reason or failure kind: count}}."""
    raise NotImplementedError
