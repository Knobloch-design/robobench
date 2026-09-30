"""Ground-truth access to the simulation, for tasks, metrics, and disturbances.

This lives only on the benchmark side and is never sent to the controller, which only
sees its observation. `SimState` is a thin wrapper around the Drake root context:
`state.plant_context` is the real thing, and the helpers are shortcuts.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Mapping

import numpy as np

if TYPE_CHECKING:
    from pydrake.geometry import SceneGraph
    from pydrake.math import RigidTransform
    from pydrake.multibody.math import SpatialVelocity
    from pydrake.multibody.plant import ContactResults, MultibodyPlant
    from pydrake.multibody.tree import ModelInstanceIndex
    from pydrake.systems.framework import Context


@dataclass(frozen=True)
class SceneHandles:
    """Handles to the built diagram, fixed for the environment's lifetime."""

    plant: "MultibodyPlant"
    scene_graph: "SceneGraph"
    robot_instance: "ModelInstanceIndex"
    extras: Mapping[str, Any] = field(default_factory=dict)
    """Whatever `Task.build_scene` returned."""


class SimState:
    def __init__(self, scene: SceneHandles, root_context: "Context") -> None:
        raise NotImplementedError

    @property
    def scene(self) -> SceneHandles:
        raise NotImplementedError

    @property
    def plant(self) -> "MultibodyPlant":
        raise NotImplementedError

    @property
    def root_context(self) -> "Context":
        raise NotImplementedError

    @property
    def plant_context(self) -> "Context":
        """Writable during `Task.reset`; treat as read-only everywhere else."""
        raise NotImplementedError

    @property
    def time(self) -> float:
        raise NotImplementedError

    def robot_positions(self) -> np.ndarray:
        raise NotImplementedError

    def robot_velocities(self) -> np.ndarray:
        raise NotImplementedError

    def applied_actuation(self) -> np.ndarray:
        """Actuator efforts actually applied (after any motor limits)."""
        raise NotImplementedError

    def body_pose(self, body_name: str, model_instance: "ModelInstanceIndex | None" = None) -> "RigidTransform":
        raise NotImplementedError

    def body_velocity(self, body_name: str, model_instance: "ModelInstanceIndex | None" = None) -> "SpatialVelocity":
        raise NotImplementedError

    def robot_base_pose(self) -> "RigidTransform":
        raise NotImplementedError

    def contact_results(self) -> "ContactResults":
        raise NotImplementedError

    def contact_body_pairs(self) -> list[tuple[str, str]]:
        """Pairs of body names currently in contact."""
        raise NotImplementedError

    # Reset-time helpers.

    def set_robot_positions(self, q: np.ndarray) -> None:
        raise NotImplementedError

    def set_free_body_pose(self, body_name: str, X_WB: "RigidTransform") -> None:
        """Place a floating body (a manipuland, or the G1 pelvis)."""
        raise NotImplementedError
