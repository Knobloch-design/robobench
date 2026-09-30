"""Controller-side message loop.

The benchmark launches controllers as:

    <controller python> -m robobench_sdk.server --controller my_pkg.my_module:MyController \
        --address tcp://127.0.0.1:5555 --kwargs '{"checkpoint": "model.pt"}'

Users can also run `serve(...)` themselves (e.g. on a GPU machine) and point the
benchmark at that address instead of letting it launch the process.
"""

from __future__ import annotations

from typing import Any, Mapping, Sequence

from robobench_sdk.controller import Controller
from robobench_sdk.transport import Transport


def serve(controller: Controller, address: str, transport: Transport | None = None) -> None:
    """Connect to the runner and answer its messages until SHUTDOWN.

    Handles the handshake (checks PROTOCOL_VERSION, calls `on_connect`), then
    dispatches RESET/OBSERVATION/EPISODE_END to the controller. If a controller
    method raises, replies with an ERROR message containing the traceback instead
    of crashing, so the runner can record it and continue.

    Args:
        controller: The user's controller instance.
        address: Runner address to connect to.
        transport: Override the default `ZmqTransport.connect(address)`.
    """
    raise NotImplementedError


def load_controller(target: str, kwargs: Mapping[str, Any] | None = None) -> Controller:
    """Import and instantiate a controller from a "package.module:ClassName" string."""
    raise NotImplementedError


def main(argv: Sequence[str] | None = None) -> None:
    """CLI entry point: parse --controller/--address/--kwargs, then `serve`."""
    raise NotImplementedError


if __name__ == "__main__":
    main()
