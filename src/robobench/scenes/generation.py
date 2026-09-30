"""Offline generators for pre-generated scenes. Run once; the outputs are shipped as assets."""

from __future__ import annotations

from pathlib import Path


def generate_rocky_terrain(
    seed: int,
    out_dir: str | Path,
    size: tuple[float, float] = (20.0, 20.0),
    rock_density: float = 0.3,
    max_rock_height: float = 0.15,
) -> Path:
    """Write a rocky terrain (collision + visual meshes, model directives YAML).

    Returns:
        Path to the directives YAML, loadable by `PregeneratedScene`.
    """
    raise NotImplementedError


def generate_building(seed: int, out_dir: str | Path, num_rooms: int = 4) -> Path:
    """Write a building layout (walls, doorways, named room regions). Returns the directives YAML path."""
    raise NotImplementedError
