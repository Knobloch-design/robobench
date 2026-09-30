"""Name -> scenario factory registry, so suites and the CLI can refer to tests by name."""

from __future__ import annotations

import importlib
from typing import TYPE_CHECKING, Any, Callable

if TYPE_CHECKING:
    from robobench.scenarios.scenario import Scenario

ScenarioFactory = Callable[..., "Scenario"]

_REGISTRY: dict[str, ScenarioFactory] = {}
_TAGS: dict[str, tuple[str, ...]] = {}


def register_scenario(name: str, tags: tuple[str, ...] = ()) -> Callable[[ScenarioFactory], ScenarioFactory]:
    """Decorator: `@register_scenario("g1/walk_rocky_terrain")` on a function returning a Scenario.

    Factory keyword arguments become overridable options (e.g. terrain variant, tolerance).
    """

    def decorator(factory: ScenarioFactory) -> ScenarioFactory:
        if name in _REGISTRY:
            raise ValueError(f"Scenario {name!r} is already registered")
        _REGISTRY[name] = factory
        _TAGS[name] = tags
        return factory

    return decorator


def _load_builtin_library() -> None:
    importlib.import_module("robobench.scenarios.library")


def get_scenario(name: str, **overrides: Any) -> "Scenario":
    """Build a registered scenario. Loads the built-in library on first use."""
    _load_builtin_library()
    try:
        factory = _REGISTRY[name]
    except KeyError:
        raise KeyError(f"Unknown scenario {name!r}. Known: {sorted(_REGISTRY)}") from None
    return factory(**overrides)


def list_scenarios(tags: tuple[str, ...] = ()) -> list[str]:
    """Registered names, optionally only those with all of `tags`."""
    _load_builtin_library()
    return sorted(name for name in _REGISTRY if set(tags) <= set(_TAGS[name]))
