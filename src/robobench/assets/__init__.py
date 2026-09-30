"""Simulatable assets (robot models, manipulands, scenes) and where they came from.

Every asset a task loads must be in `manifest.yaml` with its source and license, so
the project knows what it may redistribute when it's open-sourced.
"""

from robobench.assets.registry import AssetInfo, AssetKind, asset_path, get_asset, license_problems, list_assets

__all__ = ["AssetInfo", "AssetKind", "asset_path", "get_asset", "license_problems", "list_assets"]
