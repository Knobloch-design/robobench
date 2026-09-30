"""How controller calls interleave with simulation time.

Lockstep (default):
    send observation -> simulation frozen until the action arrives -> apply -> advance one control period.
    Controller latency affects only how long the run takes, not the results.

Real-time:
    send observation (asynchronous gRPC call) -> simulation keeps advancing, paced to the wall
    clock, with the previous command held -> the reply is applied at whatever sim time it arrives
    -> the next observation is sent at the next control-period boundary. Slow controllers act on
    stale information, just as they would on hardware. If CENIC itself can't keep up with the
    wall clock during hard contact, the achieved rate is recorded (SimStats).

Both modes give up after `step_timeout` wall-clock seconds with no reply.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, Callable

from robobench_sdk.specs import Action, Observation

if TYPE_CHECKING:
    from robobench.config import EpisodeConfig
    from robobench.controller_process.client import ControllerClient
    from robobench.sim.environment import SimulationEnvironment

ActionProcessor = Callable[[Action], Action]
"""Turns the controller's raw action into the action to apply (invalid-command handling, then limit
validation). May raise `InvalidCommandFailure`. Provided by the episode loop."""


@dataclass(frozen=True)
class ControlStepResult:
    raw_action: Action | None
    """What the controller sent, or None if no reply arrived this step (real-time only)."""
    applied_action: Action | None
    """What was sent to the robot after processing."""
    latency_wall: float | None
    """Wall-clock seconds from sending the observation to receiving the reply."""
    latency_sim: float | None
    """Sim seconds that passed during that wait (always 0 in lockstep)."""


class TimingStrategy(ABC):
    def __init__(self, config: "EpisodeConfig") -> None:
        raise NotImplementedError

    def reset(self) -> None:
        """Clear in-flight requests at episode start."""

    @abstractmethod
    def control_step(
        self,
        env: "SimulationEnvironment",
        client: "ControllerClient",
        observation: Observation,
        process: ActionProcessor,
    ) -> ControlStepResult:
        """Deliver `observation`, get and apply an action, and advance the sim one control period.

        Raises:
            ControllerError subclasses: from the client.
            InvalidCommandFailure: from `process`, in FAIL mode.
        """


class LockstepTiming(TimingStrategy):
    def control_step(self, env, client, observation, process) -> ControlStepResult:
        raise NotImplementedError


class RealTimeTiming(TimingStrategy):
    def control_step(self, env, client, observation, process) -> ControlStepResult:
        raise NotImplementedError


def make_timing(config: "EpisodeConfig") -> TimingStrategy:
    """Pick the strategy for `config.timing`."""
    raise NotImplementedError
