"""The loop for a single episode."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from robobench.config import EpisodeConfig
    from robobench.controller_process.client import ControllerClient
    from robobench.results.recording import MeshcatRecorder
    from robobench.results.records import EpisodeRecord
    from robobench.sim.environment import SimulationEnvironment
    from robobench.sim.timing import ActionProcessor
    from robobench.tasks.task import Task
    from robobench.validation.invalid import InvalidCommandHandler
    from robobench.validation.limits import CommandValidator


def run_episode(
    env: "SimulationEnvironment",
    client: "ControllerClient",
    task: "Task",
    seed: int,
    config: "EpisodeConfig",
    episode_id: str,
    recorder: "MeshcatRecorder | None" = None,
) -> "EpisodeRecord":
    """Run one episode and return its record. Never raises for controller problems.

    Steps:
        1. setup = env.reset(seed) (the task's reset map); reset pipeline, validators, metrics,
           disturbances, and the success-hold timer.
        2. client.reset(task.task_info(setup, episode_id, controller_seed)).
        3. Loop until the episode ends:
             raw obs -> pipeline -> timing.control_step (invalid check -> limit check -> apply -> advance)
             -> disturbances -> metrics.on_step
             -> task.is_success held for task.success_hold_time?  success
             -> task.check_failure?                               failure with its reason
             -> sim time >= task.max_duration?                    timeout
        4. Build the outcome (controller errors and InvalidCommandFailure become failure kinds),
           compute final metrics, attach env.stats(), send client.end_episode(summary).

    Args:
        env: Already built for `task`.
        client: Connected and past the handshake.
        task: The task being run.
        seed: Reset seed for this episode.
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
