"""Running controllers on tasks and collecting results. Runs in the simulation process.

The `controller` passed in here is normally a RemoteController: the real controller runs
in its own process, and each reset/act call goes over gRPC. The loop doesn't need to know.
"""

from dataclasses import dataclass

from robobench.controller import Controller, TaskInfo
from robobench.environment import Environment
from robobench.task import Demonstration, Task

CONTROL_PERIOD = 0.02
"""Seconds of simulated time between controller calls (50 Hz)."""


@dataclass
class EpisodeResult:
    """What one episode produced."""

    task: str
    seed: int
    outcome: str
    """"success", "failure", or "timeout"."""
    duration: float
    """Seconds of simulated time the episode lasted."""


def run_episode(task: Task, controller: Controller, seed: int) -> EpisodeResult:
    """One attempt at a task, from reset until success, failure, or timeout.

    The simulation pauses while it waits for each action from the controller.
    """
    env = Environment(task)
    goal = env.reset(seed)
    controller.reset(TaskInfo(description=task.description(goal), goal=goal))

    while env.time < task.max_duration:
        action = controller.act(env.observe())
        env.apply_action(action)
        env.step(CONTROL_PERIOD)

        if task.is_success(env.plant, env.context, goal):
            return EpisodeResult(task.name, seed, "success", env.time)
        if task.is_failure(env.plant, env.context, goal):
            return EpisodeResult(task.name, seed, "failure", env.time)

    return EpisodeResult(task.name, seed, "timeout", env.time)


def run_benchmark(tasks: list[Task], controller: Controller, seeds: list[int]) -> list[EpisodeResult]:
    """Every task, once per seed. Every controller gets the same seeds, so results are comparable."""
    return [run_episode(task, controller, seed) for task in tasks for seed in seeds]


class DemonstrationController(Controller):
    """Plays back a demonstration's recorded commands, one per step.

    The benchmark's own tool for checking demos, so it runs in the simulation process
    without gRPC.
    """

    def __init__(self, demo: Demonstration):
        """Queue up the demonstration's recorded commands."""
        self.actions = iter(demo.actions)

    def act(self, observation):
        """Ignore the observation and return the next recorded command."""
        return next(self.actions)


def check_demonstrations(task: Task) -> bool:
    """The task's success demo must succeed, and its failure demo must not."""
    demos = task.demonstrations()
    success = run_episode(task, DemonstrationController(demos["success"]), demos["success"].seed)
    failure = run_episode(task, DemonstrationController(demos["failure"]), demos["failure"].seed)
    return success.outcome == "success" and failure.outcome != "success"
