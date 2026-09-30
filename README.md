# robobench

A robotics benchmark backed by error-controlled simulation: tasks run in Drake with CENIC, and
any controller (neural network, LLM, classical, anything) can be plugged in and scored on the
same tasks and seeds.

**Status:** early draft, meant for reading and discussion. Only the core classes are here; see
[NOTES.md](NOTES.md) for what's deferred.

## Two processes

The controller and the simulation run as separate programs and talk over gRPC. The controller
only ever receives sensor readings, so it can't use the simulator's true state; it can use its
own Python packages; and if it crashes or hangs, the benchmark keeps going.

```
 ┌───────────── simulation process ─────────────┐          ┌──────── controller process ────────┐
 │  run_episode                                  │          │                                     │
 │    Environment (Drake + CENIC)                │   gRPC   │  ControllerServer                   │
 │    RemoteController ──── Reset, Act ──────────┼─────────►│    your Controller                  │
 │                     ◄─── Action ──────────────┼──────────┤                                     │
 └───────────────────────────────────────────────┘          └─────────────────────────────────────┘
```

The messages will be defined in a gRPC schema (a `.proto` file). **TODO:** schema not written yet.

## The pieces

| File | Process | What it defines |
|---|---|---|
| [controller.py](src/robobench/controller.py) | controller | `Controller`: what users write. Observation in, action out |
| [controller_server.py](src/robobench/controller_server.py) | controller | `ControllerServer`: serves a Controller over gRPC |
| [remote_controller.py](src/robobench/remote_controller.py) | simulation | `RemoteController`, `launch_controller`: reach the controller over gRPC |
| [robot.py](src/robobench/robot.py) | simulation | `Robot`: loads the model, reads its sensors, applies its commands |
| [task.py](src/robobench/task.py) | simulation | `Task`: scene, reset, success condition, description, two demonstrations |
| [environment.py](src/robobench/environment.py) | simulation | `Environment`: the Drake/CENIC simulation for one task |
| [runner.py](src/robobench/runner.py) | simulation | `run_episode`, `run_benchmark`, `check_demonstrations` |
| [messages.py](src/robobench/messages.py) | both | numpy arrays to and from gRPC messages |

## One episode

```
env.reset(seed)                 task sets up the start, returns the goal
controller.reset(task info)     controller is told the objective
repeat every 0.02 s:
    observation = env.observe()           robot's sensors only
    action = controller.act(observation)  sent over gRPC; the simulation waits for the reply
    env.apply_action(action)
    env.step(0.02)                        CENIC advances the physics
    stop if task.is_success / is_failure, or time runs out
```

## Example

[examples/leap_cube_reorientation.py](examples/leap_cube_reorientation.py) is a filled-in
robot and task, and [examples/hold_still.py](examples/hold_still.py) is a minimal controller.
