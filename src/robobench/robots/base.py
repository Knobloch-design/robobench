"""What the benchmark needs to know about a robot."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, ClassVar, Mapping

import numpy as np

if TYPE_CHECKING:
    from pydrake.multibody.parsing import Parser
    from pydrake.multibody.plant import MultibodyPlant
    from pydrake.multibody.tree import ModelInstanceIndex

    from robobench.robots.command_interfaces import CommandInterface
    from robobench.sensors.definitions import SensorDefinition


@dataclass(frozen=True)
class JointLimits:
    """Per-actuated-joint limits, all arrays in the order of `names`."""

    names: tuple[str, ...]
    position_lower: np.ndarray
    position_upper: np.ndarray
    velocity: np.ndarray
    """Symmetric absolute velocity limit."""
    effort: np.ndarray
    """Symmetric absolute torque/force limit."""


class RobotDefinition(ABC):
    """A robot: its model files, sensors, and the command interfaces its real hardware accepts.

    Command interfaces are hardware-level only (what the real robot's driver takes).
    No walking, IK, or other higher-level controllers are provided.
    """

    name: ClassVar[str]
    """Stable identifier, e.g. "unitree_g1"."""

    @abstractmethod
    def add_to_plant(self, plant: "MultibodyPlant", parser: "Parser") -> "ModelInstanceIndex":
        """Load the model into the (not yet finalized) plant.

        Welds fixed-base robots to the world, adds actuators, and sets any
        actuator/PD properties that command interfaces rely on.

        Returns:
            The robot's model instance.
        """

    @abstractmethod
    def default_sensors(self) -> list["SensorDefinition"]:
        """The sensors the real robot has. These define the default (pass-through) observation."""

    @abstractmethod
    def command_interfaces(self) -> Mapping[str, "CommandInterface"]:
        """Every command interface this robot supports, keyed by interface name."""

    @property
    @abstractmethod
    def default_command_interface(self) -> str:
        """Key into `command_interfaces()` used when a scenario doesn't choose one."""

    @property
    @abstractmethod
    def floating_base(self) -> bool:
        """True for mobile robots (the G1), False for welded ones."""

    def joint_limits(self, plant: "MultibodyPlant", instance: "ModelInstanceIndex") -> JointLimits:
        """Read limits from the finalized plant. Override to add limits the model file lacks."""
        raise NotImplementedError

    def nominal_positions(self, plant: "MultibodyPlant", instance: "ModelInstanceIndex") -> np.ndarray:
        """A sensible starting configuration (standing pose, open hand, arms at home)."""
        raise NotImplementedError

    def reference_constants(self, plant: "MultibodyPlant", instance: "ModelInstanceIndex") -> Mapping[str, Any]:
        """Static facts sent to the controller in the handshake (limits, link lengths, masses...)."""
        raise NotImplementedError
