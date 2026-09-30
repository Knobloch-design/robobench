# Contributing

Most contributions are new tasks or new models. Neither needs deep robotics experience.

## Adding a task

1. **Write the task.** Subclass `robobench.tasks.Task`, or build a `ComposedTask` from the
   helpers in `robobench.tasks.helpers`. You must provide:
   - `robot`: which robot the task uses
   - `build_scene`: what's in the world
   - `reset(seed, state)`: seed → valid initial conditions. Must be deterministic; use
     `numpy.random.default_rng(seed)`
   - `is_success(state, setup)`: whether the task is done, from ground-truth state
   - `description(setup)`: the objective in plain language, as the controller will read it
2. **Register it** in `src/robobench/tasks/library/` with
   `@register_task("robot/task_name", robot="leap_hand", tags=(...))`.
3. **Record two demonstrations**, one success and one failure, with
   `robobench.tasks.demonstrations.record_demonstration` (see `examples/record_demonstrations.py`).
   They don't need to cover every way to succeed or fail. They show what the goal is and check
   that the success condition judges both correctly.
4. **Check it:** `robobench validate-task robot/task_name` must pass. It checks that the scene
   builds on CENIC, reset is deterministic and varies across seeds, the task isn't solved at
   reset, both demos replay with the right outcome, and every asset has a known license.

## Adding a model (robot, manipuland, or scene)

1. Add the files, and an entry in `src/robobench/assets/manifest.yaml` with where they came
   from and their license. Assets with unknown licenses can't be shipped when the project
   goes public.
2. For a robot, subclass `RobotDefinition` with its default sensors and the command
   interfaces its real driver accepts. No higher-level controllers.
