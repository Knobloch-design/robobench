"""Ready-made tasks. Importing this package registers them.

Each task's demonstrations live in `demos/<task name with "/" replaced by "__">/`.
"""

from robobench.tasks.library import (  # noqa: F401
    g1_walk_building,
    g1_walk_rocky_terrain,
    leap_cube_reorientation,
)
