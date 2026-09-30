"""Ground-truth view of the simulation for goals, terminations, metrics, and disturbances.

This lives only on the benchmark side. It is never sent to the controller, which
only sees the observation.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from pydrake.math import RigidTransform
    from pydrake.multibody.math import SpatialVelocity
    from pydrake.multibody.plant import ContactResults, MultibodyPlant
    from pydrake.multibody.tree import ModelInstanceIndex
    from pydrake.systems.framework import Context


class SimState:
    def __init__(self, plant: "MultibodyPlant", plant_context: "Context", robot_instance: "ModelInstanceIndex") -> None:
        raise NotImplementedError

    @property
    def time(self) -> float:
        raise NotImplementedError

    @property
    def plant(self) -> "MultibodyPlant":
        """Escape hatch for anything the helpers don't cover. Treat as read-only."""
        raise NotImplementedError

    @property
    def plant_context(self) -> "Context":
        raise NotImplementedError

    def robot_positions(self) -> np.ndarray:
        raise NotImplementedError

    def robot_velocities(self) -> np.ndarray:
        raise NotImplementedError

    def applied_actuation(self) -> np.ndarray:
        """Actuator efforts actually applied this step (after any motor limits)."""
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
