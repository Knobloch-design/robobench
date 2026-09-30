"""What gets saved. All plain data so it serializes directly to JSON/CSV."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING, Any, Mapping

if TYPE_CHECKING:
    from robobench.metrics.aggregate import MetricSummary
    from robobench.validation.invalid import InvalidCommandEvent
    from robobench.validation.limits import Violation


class FailureKind(str, Enum):
    """Why an episode ended for reasons other than the scenario's own terminations."""

    CONTROLLER_CRASHED = "controller_crashed"
    CONTROLLER_TIMEOUT = "controller_timeout"
    CONTROLLER_RAISED = "controller_raised"
    INVALID_COMMAND = "invalid_command"
    SIMULATION_ERROR = "simulation_error"
    NOT_RUN = "not_run"
    """The worker ran out of controller restarts before reaching this episode."""


@dataclass(frozen=True)
class EpisodeOutcome:
    success: bool
    termination_reason: str
    """Termination reason ("goal_reached", "fell", "timeout") or the failure kind's value."""
    failure_kind: FailureKind | None
    sim_duration: float
    wall_duration: float
    steps: int
    error_detail: str | None = None
    """Traceback or invalid-command detail, when there is one."""


@dataclass(frozen=True)
class StepRecord:
    """Optional per-step log (EpisodeConfig.record_steps). Images are not stored."""

    step: int
    time: float
    raw_action: Mapping[str, list[float]] | None
    applied_action: Mapping[str, list[float]] | None
    num_violations: int
    invalid_kinds: list[str]
    latency_wall: float | None


@dataclass
class EpisodeRecord:
    episode_id: str
    scenario: str
    label: str | None
    seed: int
    samples: Mapping[str, Any]
    """Randomizer outputs, to replay the exact episode."""
    episode_config: Mapping[str, Any]
    """Timing, validation, and invalid-command modes used, so results with different modes can't be mixed up."""
    outcome: EpisodeOutcome
    metrics: Mapping[str, float]
    violations: list["Violation"] = field(default_factory=list)
    invalid_events: list["InvalidCommandEvent"] = field(default_factory=list)
    steps: list[StepRecord] | None = None
    recording_path: str | None = None


@dataclass(frozen=True)
class RunMetadata:
    run_id: str
    started_at: str
    """ISO 8601."""
    robobench_version: str
    drake_version: str
    protocol_version: int
    controller_target: str | None
    controller_kwargs: Mapping[str, Any]
    suite: str
    run_config: Mapping[str, Any]
    host: str


@dataclass
class RunRecord:
    metadata: RunMetadata
    episodes: list[EpisodeRecord]
    aggregates: Mapping[str, Mapping[str, "MetricSummary"]] = field(default_factory=dict)
    failure_breakdown: Mapping[str, Mapping[str, int]] = field(default_factory=dict)
