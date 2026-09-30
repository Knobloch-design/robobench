"""Meshcat replays of episodes, saved as standalone HTML files."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pydrake.geometry import Meshcat

    from robobench.sim.environment import SimulationEnvironment


class MeshcatRecorder:
    def __init__(self, meshcat: "Meshcat") -> None:
        raise NotImplementedError

    def start(self, env: "SimulationEnvironment") -> None:
        """Begin recording the environment's visualizer at episode start."""
        raise NotImplementedError

    def stop(self) -> None:
        raise NotImplementedError

    def save_html(self, path: str | Path) -> Path:
        """Write the replay. Opens in any browser without Drake installed."""
        raise NotImplementedError
