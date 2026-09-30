"""Harness that turns a chat-style LLM into a `Controller`.

The harness assembles prompts from the system prompt, reference sheet, memory,
and the current observation, calls the model, and parses its reply into an
action. It deliberately does no motion control of its own: the parsed action
goes to the robot exactly as the model produced it.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence

from robobench_sdk.controller import Controller
from robobench_sdk.llm.memory import Memory
from robobench_sdk.llm.messages import ChatMessage
from robobench_sdk.llm.reference import ReferenceSheet
from robobench_sdk.specs import Action, EpisodeSummary, Observation, SessionInfo, TaskInfo


class ResponseParseError(Exception):
    """The model's reply couldn't be turned into an action."""


class LLMClient(ABC):
    """Adapter for a specific model provider. Users implement this; none are shipped."""

    @abstractmethod
    def complete(self, messages: Sequence[ChatMessage]) -> str:
        """Send the conversation and return the model's reply text."""


class LLMController(Controller):
    """Base class for LLM controllers. Subclasses implement `format_observation` and `parse_response`.

    If `parse_response` raises `ResponseParseError`, the harness returns an all-NaN
    action, so the benchmark's invalid-command handling (fail / hold_last) applies
    and the failure is logged the same way as for any other controller.
    """

    def __init__(
        self,
        client: LLMClient,
        system_prompt: str = "",
        memory: Memory | None = None,
        reference: ReferenceSheet | None = None,
        query_every_n_steps: int = 1,
    ) -> None:
        """
        Args:
            client: The model adapter.
            system_prompt: Fixed instructions prepended to every query.
            memory: Conversation/episode memory. Defaults to `RollingMemory()`.
            reference: Constants the model can consult. Filled from the session in `on_connect`.
            query_every_n_steps: Call the model only every N control steps and repeat the
                previous action in between. Doesn't matter for results in lockstep mode;
                in real-time mode, slow models may want N > 1.
        """
        raise NotImplementedError

    def on_connect(self, session: SessionInfo) -> None:
        """Store the specs and load `session.robot_constants` into the reference sheet."""
        raise NotImplementedError

    def reset(self, task: TaskInfo) -> None:
        """Clear episode-scoped memory and store the task description."""
        raise NotImplementedError

    def act(self, observation: Observation) -> Action:
        """Query the model (every `query_every_n_steps`), parse, record to memory, return the action."""
        raise NotImplementedError

    def on_episode_end(self, summary: EpisodeSummary) -> None:
        """Record the outcome in persistent memory, if the memory keeps anything across episodes."""
        raise NotImplementedError

    def build_prompt(self, observation: Observation) -> list[ChatMessage]:
        """Assemble system prompt + reference sheet + task + memory + current observation.

        Override to change the prompt layout.
        """
        raise NotImplementedError

    @abstractmethod
    def format_observation(self, observation: Observation) -> ChatMessage:
        """Turn the numeric/image observation into a user message the model can read."""

    @abstractmethod
    def parse_response(self, text: str, observation: Observation) -> Action:
        """Turn the model's reply into an action matching the session's action spec.

        Raise `ResponseParseError` if the reply is unusable.
        """
