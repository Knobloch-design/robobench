"""The metric interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, Mapping

from robobench_sdk.specs import Action, Observation

if TYPE_CHECKING:
    from robobench.results.records import EpisodeOutcome
    from robobench.sim.state import SimState
    from robobench.tasks.task import EpisodeSetup, Task
    from robobench.validation.invalid import InvalidCommandEvent
    from robobench.validation.limits import Violation


@dataclass(frozen=True)
class StepContext:
    """Everything that happened in one control step."""

    step: int
    state: "SimState"
    """Ground truth after the step."""
    observation: Observation
    """What the controller was sent (after the pipeline)."""
    raw_action: Action | None
    """What the controller returned (None if no reply arrived this step, real-time only)."""
    applied_action: Action | None
    """What reached the robot after invalid-command handling and limit validation."""
    violations: list["Violation"]
    invalid_events: list["InvalidCommandEvent"]
    latency_wall: float | None
    latency_sim: float | None


@dataclass(frozen=True)
class EpisodeContext:
    task: "Task"
    setup: "EpisodeSetup"
    outcome: "EpisodeOutcome"
    final_state: "SimState"
    steps: int


class Metric(ABC):
    """Metrics accumulate over steps and report named values at the end.

    A metric may report several values (e.g. "latency_mean", "latency_max").
    """

    name: str

    def reset(self, task: "Task", setup: "EpisodeSetup") -> None:
        """Clear accumulated values at episode start."""

    def on_step(self, ctx: StepContext) -> None:
        """Called after every control step."""

    @abstractmethod
    def on_episode_end(self, ctx: EpisodeContext) -> Mapping[str, float]:
        """Final values for this episode."""
