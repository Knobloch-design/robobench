"""Scenes: static geometry, movable objects, and named regions for spawning robots/goals/objects."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Mapping

import numpy as np

if TYPE_CHECKING:
    from pydrake.math import RigidTransform
    from pydrake.multibody.parsing import Parser
    from pydrake.multibody.plant import MultibodyPlant


@dataclass(frozen=True)
class Region:
    """An axis-aligned box in the world where something can be placed, with a yaw range.

    Scenes define named regions (e.g. "start_area", "goal_area", "object_spawn")
    that randomizers sample from.
    """

    name: str
    center: tuple[float, float, float]
    half_extents: tuple[float, float, float]
    yaw_range: tuple[float, float] = (-np.pi, np.pi)

    def sample(self, rng: np.random.Generator) -> "RigidTransform":
        """A uniformly random pose inside the region."""
        raise NotImplementedError

    def contains(self, position: np.ndarray) -> bool:
        raise NotImplementedError


class Scene(ABC):
    """Static geometry plus movable objects. Used by ComposedTask.build_scene; Task subclasses
    may use one or build their scene directly."""

    name: str

    @abstractmethod
    def add_to_plant(self, plant: "MultibodyPlant", parser: "Parser") -> None:
        """Add static geometry and movable objects. Called before the plant is finalized."""

    def regions(self) -> Mapping[str, Region]:
        """Named regions for spawning. Default: none."""
        return {}

    def object_bodies(self) -> tuple[str, ...]:
        """Body names of movable objects (cube, mug...), for randomizers, goals, and metrics."""
        return ()

    def description(self) -> str:
        """Natural-language description that can be passed to the controller."""
        return ""


class PregeneratedScene(Scene):
    """A scene loaded from a Drake model directives YAML (terrain meshes, building layouts...)."""

    def __init__(
        self,
        name: str,
        directives_path: str | Path,
        regions: Mapping[str, Region] | None = None,
        object_bodies: tuple[str, ...] = (),
        description: str = "",
    ) -> None:
        raise NotImplementedError

    def add_to_plant(self, plant, parser) -> None:
        raise NotImplementedError

    def regions(self) -> Mapping[str, Region]:
        raise NotImplementedError

    def object_bodies(self) -> tuple[str, ...]:
        raise NotImplementedError

    def description(self) -> str:
        raise NotImplementedError
