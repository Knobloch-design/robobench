"""Hardware-level command interfaces: the kinds of commands a real robot's driver accepts.

Each interface defines the action a controller sends, and wires Drake so that
the command acts the way the real motors would (e.g. a servo's internal PD loop
and current limit). The action spec's low/high bounds are what limit validation
checks against.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

import numpy as np

from robobench_sdk.specs import Action, ActionSpec

if TYPE_CHECKING:
    from pydrake.multibody.plant import MultibodyPlant
    from pydrake.multibody.tree import ModelInstanceIndex
    from pydrake.systems.framework import DiagramBuilder, InputPort

    from robobench.robots.base import JointLimits
    from robobench.sim.state import SimState


class CommandInterface(ABC):
    name: str

    @abstractmethod
    def action_spec(self, limits: "JointLimits") -> ActionSpec:
        """Fields, shapes, and bounds of the action this interface accepts."""

    @abstractmethod
    def add_to_diagram(
        self, builder: "DiagramBuilder", plant: "MultibodyPlant", instance: "ModelInstanceIndex"
    ) -> "InputPort":
        """Add whatever systems turn the command into plant actuation.

        Returns:
            The diagram input port the environment writes the command vector to each control step.
        """

    @abstractmethod
    def to_port_value(self, action: Action) -> np.ndarray:
        """Flatten a (validated) action into the vector for the input port."""

    @abstractmethod
    def hold_default(self, state: "SimState") -> Action:
        """A safe command for "hold where you are", used by hold_last before any valid command exists.

        Position-type interfaces return the current joint positions; torque-type return zeros.
        """


class JointTorqueInterface(CommandInterface):
    """Direct joint torques. Action: {"tau": (n,)}."""

    name = "joint_torque"

    def action_spec(self, limits: "JointLimits") -> ActionSpec:
        raise NotImplementedError

    def add_to_diagram(self, builder, plant, instance):
        raise NotImplementedError

    def to_port_value(self, action: Action) -> np.ndarray:
        raise NotImplementedError

    def hold_default(self, state: "SimState") -> Action:
        raise NotImplementedError


class JointPositionInterface(CommandInterface):
    """Joint position targets tracked by a simulated servo. Action: {"q": (n,)}.

    Models servos with an internal PD loop and effort limit (e.g. the LEAP hand's
    Dynamixels, the Trossen arms' position mode). Implemented with Drake's
    PD-controlled joint actuators (supported by CENIC), whose gains should match the real servo.
    """

    name = "joint_position"

    def __init__(self, kp: np.ndarray | float, kd: np.ndarray | float, joint_names: tuple[str, ...] | None = None) -> None:
        """
        Args:
            kp, kd: Servo gains, scalar or per joint.
            joint_names: Restrict to these joints (default: all actuated joints).
        """
        raise NotImplementedError

    def action_spec(self, limits: "JointLimits") -> ActionSpec:
        raise NotImplementedError

    def add_to_diagram(self, builder, plant, instance):
        raise NotImplementedError

    def to_port_value(self, action: Action) -> np.ndarray:
        raise NotImplementedError

    def hold_default(self, state: "SimState") -> Action:
        raise NotImplementedError


class MotorCommandInterface(CommandInterface):
    """Per-motor command with gains, like Unitree's low-level API.

    Action: {"q": (n,), "dq": (n,), "kp": (n,), "kd": (n,), "tau": (n,)}.
    Applied torque = kp * (q - q_meas) + kd * (dq - dq_meas) + tau, clamped to the motor limit.
    """

    name = "motor_command"

    def __init__(self, kp_max: np.ndarray | float, kd_max: np.ndarray | float) -> None:
        """Gain bounds used in the action spec (and therefore in limit validation)."""
        raise NotImplementedError

    def action_spec(self, limits: "JointLimits") -> ActionSpec:
        raise NotImplementedError

    def add_to_diagram(self, builder, plant, instance):
        raise NotImplementedError

    def to_port_value(self, action: Action) -> np.ndarray:
        raise NotImplementedError

    def hold_default(self, state: "SimState") -> Action:
        raise NotImplementedError
