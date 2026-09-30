"""Plain-data types shared by the benchmark and controllers.

Everything that crosses the process boundary is defined here. These types only
hold numpy arrays, strings, numbers, and containers of those, never Drake
objects, so a controller can run in an environment without Drake installed and
can only ever see what the benchmark deliberately sends it.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, TypeAlias

import numpy as np

Observation: TypeAlias = dict[str, np.ndarray | str | float]
"""One control step's observation, keyed by the field names in `ObservationSpec`.

Always contains "time" (simulation seconds). Numeric fields are numpy arrays,
text fields are strings.
"""

Action: TypeAlias = dict[str, np.ndarray]
"""One command, keyed by the field names in `ActionSpec` (e.g. {"q": ...})."""


@dataclass(frozen=True)
class ArraySpec:
    """Shape, dtype, and optional bounds of one numeric field."""

    name: str
    shape: tuple[int, ...]
    dtype: str = "float64"
    low: np.ndarray | None = None
    """Elementwise lower bound. For actions, this is what limit validation checks."""
    high: np.ndarray | None = None
    units: str | None = None
    element_names: tuple[str, ...] | None = None
    """Names of each element in order, e.g. joint names for a joint-position field."""
    description: str = ""


@dataclass(frozen=True)
class TextSpec:
    """A free-text observation field, e.g. a task instruction."""

    name: str
    description: str = ""


@dataclass(frozen=True)
class ObservationSpec:
    """Every field the controller will receive each step (after the observation pipeline)."""

    arrays: Mapping[str, ArraySpec]
    texts: Mapping[str, TextSpec] = field(default_factory=dict)


@dataclass(frozen=True)
class ActionSpec:
    """Every field the controller must return from `act()`."""

    interface: str
    """Command interface name, e.g. "joint_position", "joint_torque", "motor_command"."""
    arrays: Mapping[str, ArraySpec]


@dataclass(frozen=True)
class SessionInfo:
    """Sent once, during the handshake, before any episode starts."""

    protocol_version: int
    robot: str
    observation_spec: ObservationSpec
    action_spec: ActionSpec
    control_period: float
    """Simulation seconds between consecutive `act()` calls."""
    timing_mode: str
    """"lockstep" or "real_time"."""
    robot_constants: Mapping[str, Any]
    """Static robot facts (joint limits, link lengths, masses...). Feeds the LLM ReferenceSheet."""


@dataclass(frozen=True)
class TaskInfo:
    """Sent at the start of every episode."""

    scenario: str
    episode_id: str
    description: str
    """Natural-language task description, e.g. "Walk to the marked doorway"."""
    goal: Mapping[str, Any]
    """Structured goal, e.g. {"target_position": [x, y, z]} or {"target_face": "+z"}."""
    max_duration: float
    controller_seed: int
    """Seed the controller may use for its own randomness. Derived from, but not equal to,
    the scenario seed, so it cannot be used to reproduce the hidden randomization."""
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class EpisodeSummary:
    """Sent to the controller when an episode ends."""

    episode_id: str
    success: bool
    termination_reason: str
    metrics: Mapping[str, float]
