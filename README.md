# robobench

A robotics benchmark backed by error-controlled simulation. Tasks run in Drake on CENIC,
Drake's error-controlled convex integrator for contact, and any controller (a neural network,
an LLM, a classical controller, anything) can be plugged in and scored on the same tasks,
seeds, and metrics.

**Status:** skeleton. Interfaces, data types, the gRPC schema, and docstrings are defined; most
bodies raise `NotImplementedError`. The task registry and the generated gRPC code work.

## Architecture

```
 ┌──────────── benchmark process (robobench, has Drake) ─────────────┐          ┌── controller process (robobench_sdk, no Drake) ──┐
 │                                                                   │          │                                                  │
 │  BenchmarkRunner ─► worker ─► run_episode                         │          │  gRPC server (robobench_sdk.serve)               │
 │                                                                   │          │     │                                            │
 │   SimulationEnvironment (Drake + CENIC)                           │   gRPC   │     ▼                                            │
 │     sensors ─► raw obs ─► ObservationPipeline ─► obs ───── Act(Observation) ────►  Controller.act(obs)                          │
 │                                                                   │          │     (NN / LLMController / anything)              │
 │     command port ◄─ CommandValidator ◄─ InvalidCommandHandler ◄──── Action ◄───────  returns action                              │
 │          │        (off/monitor/correct)   (fail/hold_last)        │          │                                                  │
 │          ▼                                                        │          └──────────────────────────────────────────────────┘
 │     CENIC advances one control period (lockstep or real-time)     │
 │          ▼                                                        │
 │     disturbances ─► metrics ─► task.is_success / check_failure    │
 └───────────────────────────────────────────────────────────────────┘
```

The controller only ever sees its observation (camera images, IMU readings, joint encoders),
never the simulator, so it can't use privileged state. It runs in its own process and Python
environment, so it can't conflict with Drake's dependencies or take the benchmark down when it
crashes or hangs. The protocol is defined in
[`sdk/robobench_sdk/proto/controller.proto`](sdk/robobench_sdk/proto/controller.proto); any
language with gRPC can implement a controller from it.

## Using it

```bash
pip install ./sdk .          # benchmark side
pip install ./sdk            # controller side (its own environment)
```

```python
from robobench_sdk import Controller

class MyController(Controller):
    def act(self, observation):
        return {"q": my_policy(observation["joint_position"])}
```

```bash
robobench run --controller my_pkg.my_module:MyController --controller-python /path/to/env/bin/python
robobench run --robot leap_hand --controller ...        # just one robot's tasks
robobench run --task leap/cube_reorientation --controller ...
```

## Tasks

A task subclasses [`Task`](src/robobench/tasks/task.py) and defines:

| Method | What it is |
|---|---|
| `build_scene` | The scene to simulate: models and systems added to the Drake diagram |
| `reset` | The reset map: random seed → valid initial conditions in the Drake context |
| `is_success` | The success condition, read from the system state |
| `description` | A natural-language description of the objective |

plus its `robot`, and two demonstration trajectories, one success and one failure, which
`robobench validate-task` replays to check the task is well defined. Optional hooks cover early
failure, goal error, CENIC accuracy, sensors, and more. `ComposedTask` builds a task from
reusable helpers (randomizers, goals, failure conditions). See [CONTRIBUTING.md](CONTRIBUTING.md).

Starting robots: Unitree G1, LEAP hand, Trossen Stationary AI. Built-in tasks:
`g1/walk_rocky_terrain`, `g1/walk_building`, `leap/cube_reorientation`.

## Layout

```
sdk/robobench_sdk/          Installed in the controller's environment. No Drake.
    proto/controller.proto  The protocol (gRPC). Generated code beside it; regenerate with sdk/scripts/generate_protos.py
    specs.py                Observation/Action/Spec/Session/Task types user code sees
    protocol.py             Protocol version; conversion between specs and protobuf messages
    controller.py           Controller base class: on_connect, reset, act, on_episode_end, close
    server.py               gRPC server wrapping a Controller
    llm/                    LLMController harness, Memory, ReferenceSheet

src/robobench/              The benchmark. Needs Drake >= 1.57.
    config.py               Timing/validation/invalid-command modes, CENIC SimParams, run config
    assets/                 Asset manifest with source and license per model
    robots/                 UnitreeG1, LeapHand, TrossenStationaryAI + hardware-level command interfaces
    sensors/                Sensor definitions + configurable observation pipeline
    scenes/                 Pre-generated scenes (terrain, buildings, tabletop) and generators
    tasks/                  Task base class, ComposedTask, helpers, demonstrations, validate_task, registry
      library/              Built-in tasks and their demos/
    validation/             Command limit checks and NaN/shape handling
    metrics/                Standard metrics + aggregation
    controller_process/     Launching the controller process; gRPC client
    sim/                    Drake/CENIC diagram wrapper, SimState, lockstep/real-time stepping
    runner/                 Episode loop, suites, parallel runner
    results/                Records, JSON/CSV writers, Meshcat recordings
    cli.py

examples/                   Minimal controller, LLM sketch, run script, demo recording, example suite
```

## Decisions

| Area | Decision |
|---|---|
| Simulation | Drake with CENIC only (continuous-time plant, error-controlled). No deformable bodies |
| Process model | Controller in a separate process, serving gRPC; Drake-free SDK on the controller side |
| Tasks | `Task` base class (scene, reset map, success, description) + success/failure demonstrations |
| Observations | Robot's default sensors, through an optional pipeline (pass-through by default) |
| Timing | `lockstep` (default, deterministic) or `real_time`; step timeout in both |
| Limit validation | `off` / `monitor` (default) / `correct`; violations always logged |
| Invalid commands | `fail` (default) / `hold_last`; covers NaN, inf, wrong shape, missing fields |
| Action interfaces | Hardware-level only; no shipped low-level controllers |
| Results | Every record stores its modes, seed, episode setup, CENIC settings, and simulation speed |
| License | To be decided before the repository goes public |
