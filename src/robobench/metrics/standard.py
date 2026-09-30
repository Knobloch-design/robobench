"""Standard metrics. `default_metrics()` is what every scenario gets unless it sets its own."""

from __future__ import annotations

from typing import Callable, Mapping, Sequence

import numpy as np

from robobench.metrics.base import EpisodeContext, Metric, StepContext


class Success(Metric):
    """"success": 1.0 or 0.0."""

    name = "success"

    def on_episode_end(self, ctx: EpisodeContext) -> Mapping[str, float]:
        raise NotImplementedError


class TimeToCompletion(Metric):
    """"time_to_completion": sim seconds until success (NaN on failure)."""

    name = "time_to_completion"

    def on_episode_end(self, ctx: EpisodeContext) -> Mapping[str, float]:
        raise NotImplementedError


class GoalError(Metric):
    """"final_goal_error" and "mean_goal_error" (time-averaged), using the scenario's Goal.error."""

    name = "goal_error"

    def on_step(self, ctx: StepContext) -> None:
        raise NotImplementedError

    def on_episode_end(self, ctx: EpisodeContext) -> Mapping[str, float]:
        raise NotImplementedError


class TrackingError(Metric):
    """RMS error between a measured quantity and a reference trajectory, for tracking-style tests."""

    name = "tracking_error"

    def __init__(
        self,
        measure: Callable[[StepContext], np.ndarray],
        reference: Callable[[float], np.ndarray],
        name: str = "tracking_error",
    ) -> None:
        raise NotImplementedError

    def on_step(self, ctx: StepContext) -> None:
        raise NotImplementedError

    def on_episode_end(self, ctx: EpisodeContext) -> Mapping[str, float]:
        raise NotImplementedError


class Effort(Metric):
    """"effort": integral of the sum of squared applied joint torques over time."""

    name = "effort"

    def on_step(self, ctx: StepContext) -> None:
        raise NotImplementedError

    def on_episode_end(self, ctx: EpisodeContext) -> Mapping[str, float]:
        raise NotImplementedError


class MechanicalEnergy(Metric):
    """"energy": integral of |tau * qdot| over time (J)."""

    name = "energy"

    def on_step(self, ctx: StepContext) -> None:
        raise NotImplementedError

    def on_episode_end(self, ctx: EpisodeContext) -> Mapping[str, float]:
        raise NotImplementedError


class CollisionCount(Metric):
    """"collisions": number of new contacts between body pairs that shouldn't touch.

    Allowed contacts (feet-ground, fingertips-cube) are listed per scenario.
    """

    name = "collisions"

    def __init__(self, allowed_pairs: Sequence[tuple[str, str]] = (), allow_robot_ground: bool = False) -> None:
        raise NotImplementedError

    def on_step(self, ctx: StepContext) -> None:
        raise NotImplementedError

    def on_episode_end(self, ctx: EpisodeContext) -> Mapping[str, float]:
        raise NotImplementedError


class JointLimitViolations(Metric):
    """"joint_limit_violation_steps": steps where the measured robot state exceeded its joint limits."""

    name = "joint_limit_violations"

    def on_step(self, ctx: StepContext) -> None:
        raise NotImplementedError

    def on_episode_end(self, ctx: EpisodeContext) -> Mapping[str, float]:
        raise NotImplementedError


class CommandViolationRate(Metric):
    """"command_violation_rate" (fraction of steps with any limit violation) and "command_violations" (total)."""

    name = "command_violations"

    def on_step(self, ctx: StepContext) -> None:
        raise NotImplementedError

    def on_episode_end(self, ctx: EpisodeContext) -> Mapping[str, float]:
        raise NotImplementedError


class InvalidCommandCount(Metric):
    """"invalid_commands": number of NaN/inf/shape problems (non-zero only in hold_last mode, or 1 on failure)."""

    name = "invalid_commands"

    def on_step(self, ctx: StepContext) -> None:
        raise NotImplementedError

    def on_episode_end(self, ctx: EpisodeContext) -> Mapping[str, float]:
        raise NotImplementedError


class ControllerLatency(Metric):
    """"latency_mean", "latency_p95", "latency_max" in wall-clock seconds."""

    name = "latency"

    def on_step(self, ctx: StepContext) -> None:
        raise NotImplementedError

    def on_episode_end(self, ctx: EpisodeContext) -> Mapping[str, float]:
        raise NotImplementedError


def default_metrics() -> list[Metric]:
    """Everything above except TrackingError, which needs a scenario-specific reference."""
    return [
        Success(),
        TimeToCompletion(),
        GoalError(),
        Effort(),
        MechanicalEnergy(),
        CollisionCount(),
        JointLimitViolations(),
        CommandViolationRate(),
        InvalidCommandCount(),
        ControllerLatency(),
    ]
