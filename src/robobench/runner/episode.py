"""The loop for a single episode."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from robobench.config import EpisodeConfig
    from robobench.controller_process.client import ControllerClient
    from robobench.results.recording import MeshcatRecorder
    from robobench.results.records import EpisodeRecord
    from robobench.scenarios.scenario import ScenarioInstance
    from robobench.sim.environment import SimulationEnvironment
    from robobench.sim.timing import ActionProcessor
    from robobench.validation.invalid import InvalidCommandHandler
    from robobench.validation.limits import CommandValidator


def run_episode(
    env: "SimulationEnvironment",
    client: "ControllerClient",
    instance: "ScenarioInstance",
    config: "EpisodeConfig",
    episode_id: str,
    recorder: "MeshcatRecorder | None" = None,
) -> "EpisodeRecord":
    """Run one episode and return its record. Never raises for controller problems.

    Steps:
        1. env.reset(instance); reset pipeline, validators, terminations, metrics, disturbances.
        2. client.reset(instance.task_info(episode_id)).
        3. Loop until a termination fires or the controller fails:
             raw obs -> pipeline -> timing.control_step (invalid check -> limit check -> apply -> advance)
             -> disturbances -> metrics.on_step -> terminations.
        4. Build the outcome (controller errors and InvalidCommandFailure become failure kinds),
           compute final metrics, send client.episode_end(summary).

    Args:
        env: Already built for `instance.scenario`.
        client: Connected and past the handshake.
        instance: The sampled episode.
        config: Timing/validation/invalid-command modes, recording flags.
        episode_id: Unique ID used in results and file names.
        recorder: Save a Meshcat replay if given.
    """
    raise NotImplementedError


def make_action_processor(
    invalid_handler: "InvalidCommandHandler",
    validator: "CommandValidator",
    get_step: Callable[[], int],
    get_time: Callable[[], float],
) -> "ActionProcessor":
    """Chain the two checks into the callable the timing strategy uses, collecting events for metrics."""
    raise NotImplementedError
