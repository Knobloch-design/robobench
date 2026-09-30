"""Runs a suite: plans episodes, farms them out to workers, collects and writes results.

Each worker process owns its own simulation environments and its own controller
process. Drake simulators are single-threaded, so parallelism comes from workers.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Sequence

if TYPE_CHECKING:
    from multiprocessing.queues import Queue

    from robobench.config import RunConfig
    from robobench.controller_process.launcher import ControllerLaunchConfig
    from robobench.results.records import RunRecord
    from robobench.runner.suite import BenchmarkSuite


@dataclass(frozen=True)
class EpisodeJob:
    episode_id: str
    task: str
    overrides: dict[str, Any] = field(default_factory=dict)
    seed: int = 0
    label: str | None = None
    observation_pipeline: list[dict[str, Any]] | None = None


def derive_seed(base_seed: int, task_label: str, index: int) -> int:
    """Stable per-episode seed: the same (base_seed, task, index) always gives the same episode,
    regardless of worker count or order."""
    raise NotImplementedError


class BenchmarkRunner:
    def __init__(self, suite: "BenchmarkSuite", controller: "ControllerLaunchConfig", config: "RunConfig") -> None:
        raise NotImplementedError

    def plan(self) -> list[EpisodeJob]:
        """All episodes to run, in a deterministic order."""
        raise NotImplementedError

    def run(self) -> "RunRecord":
        """Run every planned episode, writing each record as it finishes (so a crash loses nothing),
        then aggregate and write the summary."""
        raise NotImplementedError

    def resume(self, run_dir: str) -> "RunRecord":
        """Finish an interrupted run, skipping episodes already recorded there."""
        raise NotImplementedError


def worker_main(
    worker_id: int,
    jobs: Sequence[EpisodeJob],
    controller: "ControllerLaunchConfig",
    config: "RunConfig",
    results: "Queue",
) -> None:
    """Worker process entry point.

    Starts one controller process, builds (and caches) one CENIC environment per task,
    handshakes with the controller whenever the task (robot/specs) changes, and runs jobs.
    On controller crash: record the episode as failed, restart, continue. Once restarts run
    out, report the remaining jobs as not run.
    """
    raise NotImplementedError
