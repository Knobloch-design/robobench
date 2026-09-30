"""One Drake diagram for one scenario: plant + scene + robot + sensors + command interface.

Built once per scenario per worker, then reset for each episode. The controller
is not part of the diagram: each control step the environment writes the command
to an exported input port (held constant until the next command) and advances
the simulator.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Mapping

import numpy as np

from robobench_sdk.specs import Action, ActionSpec, Observation, ObservationSpec

if TYPE_CHECKING:
    from pydrake.geometry import Meshcat

    from robobench.robots.base import JointLimits
    from robobench.robots.command_interfaces import CommandInterface
    from robobench.scenarios.scenario import Scenario, ScenarioInstance
    from robobench.sim.state import SimState


class SimulationEnvironment:
    def __init__(self, scenario: "Scenario", meshcat: "Meshcat | None" = None) -> None:
        """
        Args:
            scenario: What to build (robot, scene, sensors, command interface, physics settings).
            meshcat: Attach a visualizer, needed for live viewing or recording.
        """
        raise NotImplementedError

    def build(self) -> None:
        """Create the plant/scene graph, add scene and robot, finalize, add sensors and the
        command interface, export the command input port, build the diagram and simulator."""
        raise NotImplementedError

    def reset(self, instance: "ScenarioInstance") -> None:
        """Restore the default context, apply the instance's randomizers, reset time to 0."""
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
        """Advance simulation time by `duration` seconds."""
        raise NotImplementedError

    def apply_external_wrench(self, body_name: str, wrench: np.ndarray, until_time: float) -> None:
        """Push a body with a world-frame [torque; force] until `until_time`. Used by disturbances."""
        raise NotImplementedError

    def state(self) -> "SimState":
        raise NotImplementedError

    def robot_constants(self) -> Mapping[str, Any]:
        """Robot facts for the handshake."""
        raise NotImplementedError

    def close(self) -> None:
        raise NotImplementedError
