"""LEAP hand (16-DoF, Dynamixel-driven)."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Literal, Mapping

from robobench.robots.base import RobotDefinition

if TYPE_CHECKING:
    from pydrake.math import RigidTransform

    from robobench.robots.command_interfaces import CommandInterface
    from robobench.sensors.definitions import SensorDefinition

DEFAULT_URDF_DIR = Path(__file__).resolve().parents[4] / "dex-urdf-main/robots/hands/leap_hand"
"""The dex-urdf checkout next to this project. Replace with a bundled asset later."""


class LeapHand(RobotDefinition):
    """Fixed-base dexterous hand, welded to the world at `mount_pose`.

    Default sensors: joint state (position, velocity, motor current as effort).
    Command interfaces: "joint_position" (default, Dynamixel current-limited position mode)
    and "joint_torque" (Dynamixel current mode).
    """

    name = "leap_hand"

    def __init__(
        self,
        side: Literal["left", "right"] = "right",
        model_path: str | Path | None = None,
        mount_pose: "RigidTransform | None" = None,
    ) -> None:
        """
        Args:
            side: Which hand. Picks leap_hand_{side}.urdf from DEFAULT_URDF_DIR.
            model_path: Explicit URDF path, overriding `side`.
            mount_pose: World pose of the hand base (e.g. palm-up for cube reorientation).
        """
        raise NotImplementedError

    def add_to_plant(self, plant, parser):
        raise NotImplementedError

    def default_sensors(self) -> list["SensorDefinition"]:
        raise NotImplementedError

    def command_interfaces(self) -> Mapping[str, "CommandInterface"]:
        raise NotImplementedError

    @property
    def default_command_interface(self) -> str:
        return "joint_position"

    @property
    def floating_base(self) -> bool:
        return False
