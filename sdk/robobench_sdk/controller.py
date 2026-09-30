"""The interface every controller implements."""

from __future__ import annotations

from abc import ABC, abstractmethod

from robobench_sdk.specs import Action, EpisodeSummary, Observation, SessionInfo, TaskInfo


class IncompatibleSpecError(Exception):
    """Raised from `on_connect` when a controller can't handle the offered specs."""


class Controller(ABC):
    """Base class for anything that controls a robot in the benchmark.

    Runs in its own process. The call sequence is:

        on_connect(session)
        repeat per episode:
            reset(task)
            act(observation) ... act(observation)
            on_episode_end(summary)
        close()

    Only `act` is required. Controllers may keep any internal state they like.
    Exceptions raised here are reported to the benchmark and end the episode
    as a controller failure.
    """

    def on_connect(self, session: SessionInfo) -> None:
        """Called once after the handshake, with the robot, specs, and timing for this session.

        Raise `IncompatibleSpecError` if this controller can't work with them
        (e.g. it expects a camera the observation spec doesn't include).
        """

    def reset(self, task: TaskInfo) -> None:
        """Called at the start of every episode with the task to perform."""

    @abstractmethod
    def act(self, observation: Observation) -> Action:
        """Return the next command for the robot.

        Args:
            observation: Fields described by `session.observation_spec`.

        Returns:
            A dict matching `session.action_spec`. Values outside the robot's limits,
            NaNs, or wrong shapes are handled and logged by the benchmark according
            to its validation settings.
        """

    def on_episode_end(self, summary: EpisodeSummary) -> None:
        """Called when an episode ends, with its outcome."""

    def close(self) -> None:
        """Called once before the controller process shuts down."""
