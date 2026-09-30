"""The controller-side gRPC server.

The benchmark launches controllers as:

    <controller python> -m robobench_sdk.server --controller my_pkg.my_module:MyController \
        --port-file /tmp/.../port --kwargs '{"checkpoint": "model.pt"}'

The server binds a free port and writes it to `--port-file`, which is how the
benchmark learns where to connect. Users can also run `serve(...)` themselves
(e.g. on a GPU machine) with a fixed address and point the benchmark at it.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, Sequence

import grpc

from robobench_sdk.controller import Controller
from robobench_sdk.proto import controller_pb2 as pb
from robobench_sdk.proto import controller_pb2_grpc as pb_grpc
from robobench_sdk.protocol import DEFAULT_MAX_MESSAGE_BYTES


class ControllerServicer(pb_grpc.ControllerServicer):
    """Adapts a user's `Controller` to the gRPC service.

    Converts messages with `protocol`, and maps exceptions to status codes:
    `IncompatibleSpecError` or a version mismatch in Connect -> FAILED_PRECONDITION;
    anything raised by the controller -> INTERNAL with the traceback as details.
    """

    def __init__(self, controller: Controller) -> None:
        raise NotImplementedError

    def Connect(self, request: pb.SessionInfo, context: grpc.ServicerContext) -> pb.ConnectReply:
        raise NotImplementedError

    def Reset(self, request: pb.TaskInfo, context: grpc.ServicerContext) -> pb.Empty:
        raise NotImplementedError

    def Act(self, request: pb.Observation, context: grpc.ServicerContext) -> pb.Action:
        """Calls `controller.act` and echoes the observation's `seq` in the reply."""
        raise NotImplementedError

    def EndEpisode(self, request: pb.EpisodeSummary, context: grpc.ServicerContext) -> pb.Empty:
        raise NotImplementedError

    def Shutdown(self, request: pb.Empty, context: grpc.ServicerContext) -> pb.Empty:
        """Calls `controller.close` and stops the server after replying."""
        raise NotImplementedError


def serve(
    controller: Controller,
    address: str = "127.0.0.1:0",
    port_file: str | Path | None = None,
    max_message_bytes: int = DEFAULT_MAX_MESSAGE_BYTES,
) -> None:
    """Serve `controller` until the benchmark calls Shutdown.

    Uses a single worker thread, so controller methods are never called concurrently
    and controllers don't need to be thread-safe.

    Args:
        controller: The user's controller instance.
        address: host:port to bind. Port 0 picks a free port.
        port_file: If given, the bound port is written here once the server is ready.
        max_message_bytes: Must match the benchmark's setting (large enough for images).
    """
    raise NotImplementedError


def load_controller(target: str, kwargs: Mapping[str, Any] | None = None) -> Controller:
    """Import and instantiate a controller from a "package.module:ClassName" string."""
    raise NotImplementedError


def main(argv: Sequence[str] | None = None) -> None:
    """CLI entry point: parse --controller/--address/--port-file/--kwargs, then `serve`."""
    raise NotImplementedError


if __name__ == "__main__":
    main()
