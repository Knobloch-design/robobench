"""One Drake diagram for one task: robot + task scene + sensors + command interface, on CENIC.

Built once per task per worker, then reset for each episode. The controller is not
part of the diagram: each control step the environment writes the command to an
exported input port (held constant until the next command) and advances the simulator.

Build order:
    1. DiagramBuilder + continuous-time MultibodyPlant/SceneGraph (task.sim_params().plant_config())
    2. robot.add_to_plant
    3. task.build_scene
    4. plant.Finalize(); task.finalize_scene
    5. sensors and command interface; export the command port
    6. Build; Simulator with ApplySimulatorConfig(task.sim_params().simulator_config()) -> CENIC
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Mapping

import numpy as np

from robobench_sdk.specs import Action, ActionSpec, Observation, ObservationSpec

if TYPE_CHECKING:
    from pydrake.geometry import Meshcat

    from robobench.robots.base import JointLimits
    from robobench.robots.command_interfaces import CommandInterface
    from robobench.sim.state import SceneHandles, SimState
    from robobench.tasks.task import EpisodeSetup, Task


@dataclass(frozen=True)
class SimStats:
    """Simulation cost for one episode. Reported with results, so speed can be weighed alongside performance."""

    sim_time: float
    """Simulated seconds."""
    wall_time_simulating: float
    """Wall-clock seconds spent inside the simulator (excludes waiting on the controller)."""
    realtime_rate: float
    """sim_time / wall_time_simulating."""
    integrator_steps: int
    smallest_step: float
    largest_step: float


class SimulationEnvironment:
    def __init__(self, task: "Task", meshcat: "Meshcat | None" = None) -> None:
        """
        Args:
            task: What to build.
            meshcat: Attach a visualizer, needed for live viewing or recording.
        """
        raise NotImplementedError

    def build(self) -> None:
        """Build the diagram and CENIC simulator (see the module docstring for the order)."""
        raise NotImplementedError

    def reset(self, seed: int) -> "EpisodeSetup":
        """Default the context, run `task.reset(seed, state)`, reset time and integrator stats."""
        raise NotImplementedError

    @property
    def scene(self) -> "SceneHandles":
        raise NotImplementedError

    @property
    def raw_observation_spec(self) -> ObservationSpec:
        """Sensor fields before the observation pipeline."""
        raise NotImplementedError

    @property
    def action_spec(self) -> ActionSpec:
        raise NotImplementedError

    @property
    def command_interface(self) -> "CommandInterface":
        raise NotImplementedError

    @property
    def joint_limits(self) -> "JointLimits":
        raise NotImplementedError

    @property
    def time(self) -> float:
        raise NotImplementedError

    def read_observation(self) -> Observation:
        """Raw sensor readings at the current time, plus "time"."""
        raise NotImplementedError

    def apply_action(self, action: Action) -> None:
        """Write a validated action to the command port. It's held until the next call."""
        raise NotImplementedError

    def advance(self, duration: float) -> None:
        """Advance simulation time by `duration` seconds (CENIC chooses the internal steps)."""
        raise NotImplementedError

    def apply_external_wrench(self, body_name: str, wrench: np.ndarray, until_time: float) -> None:
        """Push a body with a world-frame [torque; force] until `until_time`. Used by disturbances."""
        raise NotImplementedError

    def state(self) -> "SimState":
        raise NotImplementedError

    def stats(self) -> SimStats:
        """Integrator statistics since the last reset."""
        raise NotImplementedError

    def robot_constants(self) -> Mapping[str, Any]:
        """Robot facts for the handshake."""
        raise NotImplementedError

    def close(self) -> None:
        raise NotImplementedError
