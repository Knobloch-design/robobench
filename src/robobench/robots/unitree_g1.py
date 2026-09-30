"""Unitree G1 humanoid."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Literal, Mapping

from robobench.robots.base import RobotDefinition

if TYPE_CHECKING:
    from robobench.robots.command_interfaces import CommandInterface
    from robobench.sensors.definitions import SensorDefinition


class UnitreeG1(RobotDefinition):
    """Floating-base humanoid.

    Default sensors: joint state, pelvis IMU, and optionally the head depth camera.
    Command interfaces: "motor_command" (default, matches Unitree's low-level API) and "joint_torque".
    """

    name = "unitree_g1"

    def __init__(
        self,
        model_path: str | Path | None = None,
        variant: Literal["23dof", "29dof"] = "29dof",
        with_hands: bool = False,
        head_camera: bool = False,
    ) -> None:
        """
        Args:
            model_path: URDF path. Default: bundled asset (Unitree's URDF, cleaned up for Drake).
            variant: Joint configuration of the G1 model.
            with_hands: Include the dexterous hands.
            head_camera: Add the head depth camera to the default sensors.
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
        return "motor_command"

    @property
    def floating_base(self) -> bool:
        return True
