"""Settings for simulations, episodes, and whole benchmark runs."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pydrake.multibody.plant import MultibodyPlantConfig

    from robobench.sensors.pipeline import ObservationPipeline


class TimingMode(str, Enum):
    LOCKSTEP = "lockstep"
    """Simulation pauses while the controller computes. Latency doesn't affect results."""
    REAL_TIME = "real_time"
    """Simulation keeps running while the controller computes; the previous command is held."""


class ValidationMode(str, Enum):
    OFF = "off"
    """Commands pass through untouched (violations are still counted)."""
    MONITOR = "monitor"
    """Commands pass through; every limit violation is logged."""
    CORRECT = "correct"
    """Out-of-limit values are clipped to the limit; every violation is logged."""


class InvalidCommandMode(str, Enum):
    """What to do with commands that can't be simulated at all (NaN, inf, wrong shape, missing field)."""

    FAIL = "fail"
    """End the episode as a failure."""
    HOLD_LAST = "hold_last"
    """Reuse the last valid command (or the interface's hold default on the first step)."""


@dataclass
class SimParams:
    """Physics settings. Scenarios set their own, since contact-heavy tasks need different values."""

    time_step: float = 0.001
    """Discrete plant time step (s)."""
    discrete_contact_approximation: str = "sap"
    """"tamsi", "sap", "similar", or "lagged". Deformable bodies require "sap"."""
    contact_model: str = "hydroelastic_with_fallback"
    """"point", "hydroelastic", or "hydroelastic_with_fallback"."""
    penetration_allowance: float | None = None
    extra: dict[str, Any] = field(default_factory=dict)
    """Any other MultibodyPlantConfig fields."""

    def to_plant_config(self) -> "MultibodyPlantConfig":
        raise NotImplementedError


@dataclass
class EpisodeConfig:
    """How each episode is run. Recorded in every result so runs with different modes can't be confused."""

    timing: TimingMode = TimingMode.LOCKSTEP
    control_period: float = 0.02
    """Simulation seconds between controller calls (50 Hz default)."""
    real_time_rate: float = 1.0
    """Real-time mode only: sim seconds per wall-clock second."""
    validation: ValidationMode = ValidationMode.MONITOR
    invalid_command: InvalidCommandMode = InvalidCommandMode.FAIL
    step_timeout: float = 120.0
    """Wall-clock seconds to wait for one action before declaring the controller hung. Applies in both modes."""
    observation_pipeline: "ObservationPipeline | None" = None
    """Overrides the scenario's pipeline if set. None keeps the scenario's (pass-through by default)."""
    record_steps: bool = False
    """Store per-step records (large)."""
    record_video: bool = False
    """Save a Meshcat HTML replay per episode."""


@dataclass
class RunConfig:
    """Settings for a whole benchmark run."""

    output_dir: Path = Path("results")
    episodes_per_scenario: int = 10
    base_seed: int = 0
    num_workers: int = 1
    """Parallel worker processes. Each gets its own simulator and its own controller process."""
    fresh_controller_per_episode: bool = False
    """Restart the controller process before every episode, guaranteeing no carried-over state."""
    episode: EpisodeConfig = field(default_factory=EpisodeConfig)

    @classmethod
    def from_yaml(cls, path: str | Path) -> "RunConfig":
        raise NotImplementedError

    def to_dict(self) -> dict[str, Any]:
        """Plain-data snapshot stored in the run's results."""
        raise NotImplementedError
