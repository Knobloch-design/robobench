"""Trossen "Stationary AI" bimanual manipulator."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Mapping

from robobench.robots.base import RobotDefinition

if TYPE_CHECKING:
    from robobench.robots.command_interfaces import CommandInterface
    from robobench.sensors.definitions import SensorDefinition


class TrossenStationaryAI(RobotDefinition):
    """Two follower arms with parallel grippers on a fixed frame, plus fixed and wrist cameras.

    Only the follower arms are simulated (the leader arms are for teleoperation).
    Action fields cover both arms and both grippers in one vector, left then right.

    Default sensors: joint state for both arms/grippers and the kit's cameras.
    Command interfaces: "joint_position" (default) and "joint_torque".
    Confirm joint counts, camera placement, and supported driver modes against Trossen's docs.
    """

    name = "trossen_stationary_ai"

    def __init__(self, model_path: str | Path | None = None, cameras: bool = True) -> None:
        """
        Args:
            model_path: Model directives/URDF for the full cell. Default: bundled asset.
            cameras: Include the cameras in the default sensors (disable for faster runs).
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
