"""Ready-made scenes."""

from __future__ import annotations

from pathlib import Path

from robobench.scenes.base import PregeneratedScene, Scene

ASSET_DIR = Path(__file__).resolve().parent / "assets"


def flat_ground() -> Scene:
    """A ground plane. Useful for debugging a robot before harder scenes."""
    raise NotImplementedError


def rocky_terrain(variant: int = 0) -> PregeneratedScene:
    """One of the pre-generated rocky terrains, with "start_area" and "goal_area" regions."""
    raise NotImplementedError


def building(variant: int = 0) -> PregeneratedScene:
    """One of the pre-generated building layouts (rooms, doorways), with named room regions."""
    raise NotImplementedError


def hand_workspace(object_name: str = "cube") -> Scene:
    """Space above a palm-up LEAP hand with one object ("cube", ...) and an "object_spawn" region."""
    raise NotImplementedError


def tabletop(objects: tuple[str, ...] = (), deformable: tuple[str, ...] = ()) -> Scene:
    """Table in front of the Trossen cell. `deformable` objects are simulated as FEM soft bodies."""
    raise NotImplementedError
