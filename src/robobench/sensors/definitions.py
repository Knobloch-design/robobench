"""Sensors that produce raw observation fields from the simulation."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Mapping

import numpy as np

from robobench_sdk.specs import ArraySpec

if TYPE_CHECKING:
    from pydrake.geometry import SceneGraph
    from pydrake.math import RigidTransform
    from pydrake.multibody.plant import MultibodyPlant
    from pydrake.multibody.tree import ModelInstanceIndex
    from pydrake.systems.framework import Context, DiagramBuilder


class SensorDefinition(ABC):
    """One sensor. May produce several observation fields (e.g. "joint_position", "joint_velocity")."""

    name: str

    @abstractmethod
    def add_to_diagram(
        self,
        builder: "DiagramBuilder",
        plant: "MultibodyPlant",
        scene_graph: "SceneGraph",
        instance: "ModelInstanceIndex",
    ) -> None:
        """Add the Drake systems for this sensor. Called before the diagram is built."""

    @abstractmethod
    def specs(self) -> Mapping[str, ArraySpec]:
        """The raw fields this sensor produces. Valid after `add_to_diagram`."""

    @abstractmethod
    def read(self, root_context: "Context") -> Mapping[str, np.ndarray]:
        """Evaluate the sensor at the current simulation state."""


class JointStateSensor(SensorDefinition):
    """Joint encoders. Fields: "joint_position", "joint_velocity", and optionally "joint_effort"."""

    def __init__(self, name: str = "joints", include_effort: bool = True, joint_names: tuple[str, ...] | None = None) -> None:
        raise NotImplementedError

    def add_to_diagram(self, builder, plant, scene_graph, instance) -> None:
        raise NotImplementedError

    def specs(self) -> Mapping[str, ArraySpec]:
        raise NotImplementedError

    def read(self, root_context) -> Mapping[str, np.ndarray]:
        raise NotImplementedError


class ImuSensor(SensorDefinition):
    """IMU on a body. Fields: "{name}_angular_velocity", "{name}_linear_acceleration", "{name}_orientation"."""

    def __init__(self, name: str, body_name: str, X_BS: "RigidTransform | None" = None) -> None:
        raise NotImplementedError

    def add_to_diagram(self, builder, plant, scene_graph, instance) -> None:
        raise NotImplementedError

    def specs(self) -> Mapping[str, ArraySpec]:
        raise NotImplementedError

    def read(self, root_context) -> Mapping[str, np.ndarray]:
        raise NotImplementedError


class CameraSensor(SensorDefinition):
    """RGB(-D) camera attached to a frame. Fields: "{name}_rgb" (H, W, 3) and optionally "{name}_depth" (H, W)."""

    def __init__(
        self,
        name: str,
        parent_frame: str,
        X_PC: "RigidTransform",
        width: int = 640,
        height: int = 480,
        fov_y: float = 0.9,
        depth: bool = False,
    ) -> None:
        """`parent_frame` is a frame name in the plant ("world" for fixed cameras)."""
        raise NotImplementedError

    def add_to_diagram(self, builder, plant, scene_graph, instance) -> None:
        raise NotImplementedError

    def specs(self) -> Mapping[str, ArraySpec]:
        raise NotImplementedError

    def read(self, root_context) -> Mapping[str, np.ndarray]:
        raise NotImplementedError


class ContactForceSensor(SensorDefinition):
    """Net contact force on selected bodies (fingertips, feet). Field: "{name}_force" (n_bodies, 3)."""

    def __init__(self, name: str, body_names: tuple[str, ...]) -> None:
        raise NotImplementedError

    def add_to_diagram(self, builder, plant, scene_graph, instance) -> None:
        raise NotImplementedError

    def specs(self) -> Mapping[str, ArraySpec]:
        raise NotImplementedError

    def read(self, root_context) -> Mapping[str, np.ndarray]:
        raise NotImplementedError
