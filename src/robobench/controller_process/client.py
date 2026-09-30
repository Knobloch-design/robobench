"""Runner-side stub for the remote controller: one method per protocol exchange."""

from __future__ import annotations

from typing import TYPE_CHECKING

from robobench_sdk.specs import Action, EpisodeSummary, Observation, SessionInfo, TaskInfo

if TYPE_CHECKING:
    from robobench.controller_process.launcher import ControllerProcess
    from robobench_sdk.transport import Transport


class ControllerError(Exception):
    """Base class. The episode loop turns these into failure kinds in the results."""


class ControllerTimeout(ControllerError):
    """No reply within the step timeout (or the startup timeout for the handshake)."""


class ControllerCrashed(ControllerError):
    """The process exited or the connection dropped."""


class ControllerRaised(ControllerError):
    """The controller's own code raised. Carries the remote traceback."""

    def __init__(self, remote_traceback: str) -> None:
        super().__init__(remote_traceback)
        self.remote_traceback = remote_traceback


class ControllerClient:
    def __init__(self, transport: "Transport", process: "ControllerProcess | None", step_timeout: float) -> None:
        """
        Args:
            transport: Bound transport the controller connects to.
            process: Used to tell a crash apart from a slow reply. None for external controllers.
            step_timeout: Wall-clock seconds to wait for each action.
        """
        raise NotImplementedError

    def handshake(self, session: SessionInfo, timeout: float) -> None:
        """Send HELLO and wait for HELLO_ACK.

        Raises:
            ControllerRaised: the controller rejected the specs (IncompatibleSpecError) or the protocol version.
        """
        raise NotImplementedError

    def reset(self, task: TaskInfo) -> None:
        raise NotImplementedError

    def act(self, observation: Observation) -> tuple[Action, float]:
        """Lockstep: send the observation and block for the action.

        Returns:
            (action, wall-clock latency in seconds). The action is returned exactly as received.
        """
        raise NotImplementedError

    def send_observation(self, observation: Observation) -> int:
        """Real-time: send without waiting. Returns the sequence number."""
        raise NotImplementedError

    def poll_action(self, timeout: float = 0.0) -> tuple[int, Action, float] | None:
        """Real-time: (seq, action, latency) if a reply has arrived, else None."""
        raise NotImplementedError

    def episode_end(self, summary: EpisodeSummary) -> None:
        raise NotImplementedError

    def shutdown(self) -> None:
        raise NotImplementedError
