"""The asset manifest: what each model file is, where it came from, and whether it can be shipped."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pydrake.multibody.parsing import Parser
    from pydrake.multibody.plant import MultibodyPlant
    from pydrake.multibody.tree import ModelInstanceIndex

MANIFEST_PATH = Path(__file__).resolve().parent / "manifest.yaml"


class AssetKind(str, Enum):
    ROBOT = "robot"
    MANIPULAND = "manipuland"
    SCENE = "scene"


@dataclass(frozen=True)
class AssetInfo:
    name: str
    kind: AssetKind
    path: str
    """Model file, relative to the manifest (or absolute)."""
    source: str
    """Where it came from: a URL or a description."""
    license: str
    """SPDX identifier (e.g. "MIT", "BSD-3-Clause"), or "unknown" until checked."""
    redistributable: bool | None
    """Whether the project may ship it. None = not yet checked."""
    notes: str = ""


def list_assets(kind: AssetKind | None = None) -> list[AssetInfo]:
    raise NotImplementedError


def get_asset(name: str) -> AssetInfo:
    """Raises KeyError for assets missing from the manifest."""
    raise NotImplementedError


def asset_path(name: str) -> Path:
    """Absolute path to the asset's model file."""
    raise NotImplementedError


def add_manipuland(plant: "MultibodyPlant", parser: "Parser", name: str, instance_name: str | None = None) -> "ModelInstanceIndex":
    """Load a manipuland from the manifest into the plant (for use in `Task.build_scene`)."""
    raise NotImplementedError


def license_problems(names: list[str] | None = None) -> list[AssetInfo]:
    """Assets (all, or just `names`) whose license is unknown or that aren't cleared to redistribute.
    Used by validate-task and before making the repository public."""
    raise NotImplementedError
