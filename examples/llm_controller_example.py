"""Sketch of an LLM controller for the LEAP cube task, using the SDK harness.

The user supplies the model adapter (`LLMClient`) and the two translation methods.
Memory, the reference sheet, and prompt assembly come from `LLMController`.
"""

from __future__ import annotations

from typing import Sequence

from robobench_sdk import Action, Observation
from robobench_sdk.llm import ChatMessage, LLMClient, LLMController


class MyModelClient(LLMClient):
    """Wrap whatever model/provider you use here."""

    def complete(self, messages: Sequence[ChatMessage]) -> str:
        raise NotImplementedError


class CubeLLMController(LLMController):
    def __init__(self) -> None:
        super().__init__(
            client=MyModelClient(),
            system_prompt=(
                "You control a 16-joint robot hand. Reply with a JSON list of 16 joint "
                "position targets in radians. Consult the reference sheet for joint limits."
            ),
            query_every_n_steps=5,
        )

    def format_observation(self, observation: Observation) -> ChatMessage:
        raise NotImplementedError

    def parse_response(self, text: str, observation: Observation) -> Action:
        raise NotImplementedError
