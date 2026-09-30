"""Benchmark-side gRPC client for the controller: one method per RPC in controller.proto.

gRPC failures are translated into the exceptions below, which the episode loop turns
into failure kinds in the results.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from robobench_sdk.protocol import DEFAULT_MAX_MESSAGE_BYTES
from robobench_sdk.specs import Action, EpisodeSummary, Observation, SessionInfo, TaskInfo

if TYPE_CHECKING:
    from robobench.controller_process.launcher import ControllerProcess


class ControllerError(Exception):
    """Base class."""


class ControllerTimeout(ControllerError):
    """No reply within the step timeout (gRPC DEADLINE_EXCEEDED)."""


class ControllerCrashed(ControllerError):
    """The process exited or the connection dropped (gRPC UNAVAILABLE, or the process is gone)."""


class ControllerRaised(ControllerError):
    """The controller's own code raised (gRPC INTERNAL). Carries the remote traceback."""

    def __init__(self, remote_traceback: str) -> None:
        super().__init__(remote_traceback)
        self.remote_traceback = remote_traceback


class ControllerRejected(ControllerError):
    """Connect was refused: incompatible specs or protocol version (gRPC FAILED_PRECONDITION)."""


class PendingAction:
    """An in-flight Act call (real-time mode). Wraps a gRPC future."""

    @property
    def seq(self) -> int:
        raise NotImplementedError

    def done(self) -> bool:
        raise NotImplementedError

    def result(self, timeout: float | None = None) -> tuple[Action, float]:
        """(action, wall-clock latency). Raises the ControllerError the call failed with."""
        raise NotImplementedError

    def cancel(self) -> None:
        raise NotImplementedError


class ControllerClient:
    def __init__(
        self,
        address: str,
        process: "ControllerProcess | None",
        step_timeout: float,
        max_message_bytes: int = DEFAULT_MAX_MESSAGE_BYTES,
    ) -> None:
        """
        Args:
            address: host:port of the controller's gRPC server.
            process: Used to tell a crash from a slow reply. None for external controllers.
            step_timeout: Deadline (wall-clock seconds) for each Act call.
            max_message_bytes: Must match the controller side (large enough for images).
        """
        raise NotImplementedError

    def wait_until_ready(self, timeout: float) -> None:
        """Block until the channel connects (model loading can make startup slow)."""
        raise NotImplementedError

    def connect(self, session: SessionInfo) -> str:
        """Handshake. Returns the controller's reported name.

        Raises:
            ControllerRejected: specs or protocol version refused.
        """
        raise NotImplementedError

    def reset(self, task: TaskInfo) -> None:
        raise NotImplementedError

    def act(self, observation: Observation) -> tuple[Action, float]:
        """Lockstep: blocking Act call with the step-timeout deadline.

        Returns:
            (action exactly as received, wall-clock latency in seconds).
        """
        raise NotImplementedError

    def act_async(self, observation: Observation) -> PendingAction:
        """Real-time: start an Act call without waiting."""
        raise NotImplementedError

    def end_episode(self, summary: EpisodeSummary) -> None:
        raise NotImplementedError

    def shutdown(self) -> None:
        """Send Shutdown and close the channel. Never raises."""
        raise NotImplementedError
