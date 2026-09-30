"""Demonstration trajectories.

Every task ships two: one success and one failure. They show what the goal looks
like, and they check that the task is well defined: replaying the success demo must
satisfy `is_success`, and replaying the failure demo must not.

A demonstration is an open-loop sequence of commands for one seed, recorded through
the task's command interface at its control period. States are recorded too, for
illustration and to spot replay drift. Replay relies on the simulation being
deterministic, which holds for CENIC at a fixed accuracy on the same Drake build.

Files: `<task demo_dir>/success.npz` and `failure.npz` (arrays) plus a `.json` beside
each (metadata), written by `Demonstration.save`.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Literal, Mapping

import numpy as np

if TYPE_CHECKING:
    from pydrake.geometry import Meshcat

    from robobench.config import EpisodeConfig
    from robobench.tasks.task import Task
    from robobench_sdk.controller import Controller

DemoKind = Literal["success", "failure"]


@dataclass
class Demonstration:
    kind: DemoKind
    seed: int
    """Reset seed the demo was recorded from."""
    command_interface: str
    control_period: float
    actions: Mapping[str, np.ndarray]
    """One array per action field, each shaped (num_steps, *field_shape)."""
    states: np.ndarray | None = None
    """(num_steps + 1, num_positions + num_velocities) plant state, including the initial state."""
    note: str = ""
    """What it shows, e.g. "Rotates the cube but drops it at t = 3 s"."""
    drake_version: str = ""
    sim_params: Mapping[str, float | str] = field(default_factory=dict)
    """CENIC settings at recording time; replay uses the same."""

    @property
    def num_steps(self) -> int:
        raise NotImplementedError

    def save(self, path: str | Path) -> None:
        """Write `<path>.npz` and `<path>.json`."""
        raise NotImplementedError

    @classmethod
    def load(cls, path: str | Path) -> "Demonstration":
        raise NotImplementedError


@dataclass(frozen=True)
class ReplayResult:
    success: bool
    """Whether `is_success` held (for `success_hold_time`) at any point during replay."""
    failure_reason: str | None
    """From `check_failure`, if it fired."""
    sim_duration: float
    max_state_deviation: float | None
    """Largest difference from the recorded states (None if the demo has no states). Large values mean replay drifted."""


def record_demonstration(
    task: "Task",
    controller: "Controller",
    seed: int,
    kind: DemoKind,
    note: str = "",
    config: "EpisodeConfig | None" = None,
) -> Demonstration:
    """Run `controller` in-process (no gRPC) for one episode and capture its commands and states.

    For task authors: use a scripted controller, a teleoperation controller, or a
    hand-tuned policy. Only the recorded commands matter, not how they were produced.
    """
    raise NotImplementedError


def replay_demonstration(task: "Task", demo: Demonstration, meshcat: "Meshcat | None" = None) -> ReplayResult:
    """Reset with `demo.seed`, apply the recorded commands open-loop, and evaluate success and failure."""
    raise NotImplementedError
