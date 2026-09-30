# robobench

A Drake-based framework for testing how well any controller (a neural network, an LLM, a classical
controller, anything) makes a robot perform across many situations.

**Status:** skeleton. Interfaces, data types, and docstrings are defined; most bodies raise
`NotImplementedError`. The scenario registry is the only piece that works.

## Architecture

```
 ┌──────────────── benchmark process (robobench, has Drake) ────────────────┐      ┌─── controller process (robobench_sdk, no Drake) ───┐
 │                                                                          │      │                                                     │
 │  BenchmarkRunner ─► worker ─► run_episode                                │      │  serve(controller)                                  │
 │                                  │                                       │      │     │                                               │
 │   SimulationEnvironment (Drake)  │                                       │      │     ▼                                               │
 │     sensors ─► raw obs ─► ObservationPipeline ─► obs ───────────────────────────────►  Controller.act(obs)                            │
 │                                                                          │  ZMQ │     (NN / LLMController / anything)                 │
 │     command port ◄─ CommandValidator ◄─ InvalidCommandHandler ◄─ action ◄────────────  returns action                                 │
 │          │         (off/monitor/correct)  (fail/hold_last)               │      │                                                     │
 │          ▼                                                               │      └─────────────────────────────────────────────────────┘
 │     advance sim (LockstepTiming | RealTimeTiming)                        │
 │          │                                                               │
 │     disturbances ─► metrics.on_step ─► terminations                      │
 │                                                                          │
 └──────────────────────────────────────────────────────────────────────────┘
```

The controller only ever sees plain data (numpy arrays, strings), never the simulator. It runs in
its own process, with its own Python environment, so it can't conflict with Drake's dependencies,
can't read ground truth, and can't take the benchmark down when it crashes or hangs.

## Layout

```
sdk/robobench_sdk/          Install in the controller's environment. No Drake.
    specs.py                Observation/Action/Spec/Session/Task types that cross the process boundary
    controller.py           Controller base class: on_connect, reset, act, on_episode_end, close
    protocol.py, transport.py, server.py   Messages, ZMQ transport, controller-side loop
    llm/                    LLMController harness, Memory, ReferenceSheet

src/robobench/              The benchmark. Needs Drake.
    config.py               TimingMode, ValidationMode, InvalidCommandMode, SimParams, EpisodeConfig, RunConfig
    robots/                 UnitreeG1, LeapHand, TrossenStationaryAI + hardware-level command interfaces
    sensors/                Sensor definitions + configurable observation pipeline and stages
    scenes/                 Pre-generated scenes (terrain, buildings, tabletop) and their generators
    scenarios/              Test building blocks: Scenario, randomizers, goals, terminations, disturbances
      library/              Ready-made tests (G1 walking x2, LEAP cube reorientation, Trossen soft pick)
    validation/             Limit checks and NaN/shape handling
    metrics/                Standard metrics + aggregation
    controller_process/     Launching the controller process and the runner-side client
    sim/                    Drake diagram wrapper, ground-truth SimState, lockstep/real-time stepping
    runner/                 Episode loop, suites, parallel runner
    results/                Records, JSON/CSV writers, Meshcat recordings
    cli.py

examples/                   Minimal controller, LLM controller sketch, Python run script, example suite
```

## Decisions

| Area | Decision |
|---|---|
| Process model | Controller in a separate process; Drake-free SDK on the controller side |
| Observations | Robot's default sensors, through an optional pipeline (pass-through by default) |
| Timing | `lockstep` (default) or `real_time`; step timeout in both |
| Limit validation | `off` / `monitor` (default) / `correct`; violations always logged |
| Invalid commands | `fail` (default) / `hold_last`; covers NaN, inf, wrong shape, missing fields |
| Action interfaces | Hardware-level only (what each real robot's driver accepts); no shipped low-level controllers |
| Tests | Users compose `Scenario`s from building blocks; ready-made ones in `scenarios/library` |
| Results | Every record stores the modes it ran under, the seed, and all randomized values |

## Writing a controller

```python
from robobench_sdk import Controller

class MyController(Controller):
    def act(self, observation):
        return {"q": my_policy(observation["joint_position"])}
```

```bash
robobench run --suite examples/suites/example.yaml --controller my_pkg.my_module:MyController \
    --controller-python /path/to/my/env/bin/python
```
