"""Command-line interface.

Running:
    robobench run --controller my_pkg.ctrl:MyController --controller-python /path/to/env/bin/python
                                                     # the full suite
    robobench run --robot leap_hand --controller ... # only one robot's tasks
    robobench run --tags locomotion --controller ...
    robobench run --task leap/cube_reorientation --controller ...
    robobench run --suite my_suite.yaml --controller ...
    robobench run ... --connect gpu-box:50051        # controller already serving elsewhere
    robobench run ... --config run.yaml --workers 4

Exploring:
    robobench list [--robot leap_hand] [--tags manipulation]
    robobench describe leap/cube_reorientation
    robobench summarize results/<run_id>

Contributing:
    robobench validate-task leap/cube_reorientation  # all checks, including demo replay
    robobench replay-demo leap/cube_reorientation success   # watch it in Meshcat
    robobench check-licenses                          # assets with unknown licenses
"""

from __future__ import annotations

from typing import Sequence


def main(argv: Sequence[str] | None = None) -> int:
    raise NotImplementedError


if __name__ == "__main__":
    raise SystemExit(main())
