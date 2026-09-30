"""Starting, watching, and restarting the controller process."""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping


@dataclass
class ControllerLaunchConfig:
    """How to get a controller.

    Either the benchmark launches it (`target` set), or the user started it already
    with `robobench_sdk.serve` and the benchmark only connects (`target` None, `address` set).
    """

    target: str | None = None
    """"package.module:ClassName", importable by `python_executable`."""
    kwargs: Mapping[str, Any] = field(default_factory=dict)
    """Passed to the controller's constructor. Must be JSON-serializable."""
    python_executable: str = sys.executable
    """Python of the controller's own environment (which needs robobench-sdk, not Drake)."""
    cwd: Path | None = None
    env: Mapping[str, str] = field(default_factory=dict)
    """Extra environment variables (e.g. CUDA_VISIBLE_DEVICES, API keys)."""
    address: str | None = None
    """Address to bind for launched controllers (None picks a free local port),
    or the address of an already-running controller."""
    startup_timeout: float = 120.0
    """Seconds to wait for the handshake (model loading can be slow)."""
    max_restarts: int = 3
    """Per worker. After this many crashes the worker's remaining episodes are marked not run."""
    log_dir: Path | None = None
    """Where the controller's stdout/stderr go. None: inside the run's output directory."""

    @property
    def launches_process(self) -> bool:
        return self.target is not None


class ControllerProcess:
    """One controller process (or a connection to an externally started one)."""

    def __init__(self, config: ControllerLaunchConfig) -> None:
        raise NotImplementedError

    def start(self) -> str:
        """Launch `python -m robobench_sdk.server ...` (if launching) and return the address to talk on."""
        raise NotImplementedError

    def is_alive(self) -> bool:
        """For external controllers, whether the connection is still up."""
        raise NotImplementedError

    def stop(self, grace_period: float = 5.0) -> None:
        """Ask it to shut down; kill after `grace_period`."""
        raise NotImplementedError

    def restart(self) -> str:
        """Kill and relaunch. Raises RuntimeError once `max_restarts` is used up, or for external controllers."""
        raise NotImplementedError

    @property
    def restarts_used(self) -> int:
        raise NotImplementedError

    def __enter__(self) -> "ControllerProcess":
        self.start()
        return self

    def __exit__(self, *exc: object) -> None:
        self.stop()
