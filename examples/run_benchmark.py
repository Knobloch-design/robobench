"""Running a suite from Python instead of the CLI."""

from __future__ import annotations

from pathlib import Path

from robobench.config import EpisodeConfig, InvalidCommandMode, RunConfig, TimingMode, ValidationMode
from robobench.controller_process import ControllerLaunchConfig
from robobench.runner import BenchmarkRunner, BenchmarkSuite


def main() -> None:
    suite = BenchmarkSuite.from_yaml(Path(__file__).parent / "suites/example.yaml")

    controller = ControllerLaunchConfig(
        target="examples.hold_position_controller:HoldPositionController",
        # python_executable="/path/to/controller/env/bin/python",
    )

    config = RunConfig(
        output_dir=Path("results"),
        episodes_per_scenario=5,
        num_workers=2,
        episode=EpisodeConfig(
            timing=TimingMode.LOCKSTEP,
            validation=ValidationMode.MONITOR,
            invalid_command=InvalidCommandMode.FAIL,
        ),
    )

    run = BenchmarkRunner(suite, controller, config).run()
    print(f"Wrote {len(run.episodes)} episodes to {config.output_dir / run.metadata.run_id}")


if __name__ == "__main__":
    main()
