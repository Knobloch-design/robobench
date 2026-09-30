"""Command-line interface.

    robobench list [--tags g1,locomotion]
    robobench describe leap/cube_reorientation
    robobench run --suite suites/example.yaml --controller my_pkg.ctrl:MyController \
        --controller-python /path/to/controller/env/bin/python [--config run.yaml] [--workers 4]
    robobench run --suite ... --connect tcp://gpu-box:5555     # controller started elsewhere
    robobench summarize results/<run_id>
"""

from __future__ import annotations

from typing import Sequence


def main(argv: Sequence[str] | None = None) -> int:
    raise NotImplementedError


if __name__ == "__main__":
    raise SystemExit(main())
