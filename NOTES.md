# Deferred

This draft keeps only the core classes. Everything below was designed earlier and is left
out for now, to be added back as the core settles. The fuller version is on the
`full-skeleton` branch.

**Controller connection** (the separate process and gRPC are outlined in the draft; these details aren't)
- A small Drake-free package for controller authors (the "SDK"), so their environment needs no Drake.
- Handshake at connect time: the robot, the observation and action formats, and a protocol version.
- Timeouts, crash detection and restarts for the controller process; choosing a free port automatically.

**Command checking**
- Limit checks on commands: off / monitor (default) / correct, with every violation logged.
- NaN, inf and wrong-shape commands: fail the episode (default) or reuse the last valid command.

**Observations and timing**
- Optional sensor noise, delay, dropout, and downsampling between the sensors and the controller.
- Real-time mode, where the simulation keeps running while the controller thinks (lockstep is the default and the only mode here).

**Tasks**
- Robot and task stubs for the Unitree G1 and the Trossen Stationary AI.
- Other tasks: G1 walking over rocky terrain and through a building.
- Reusable helpers for writing tasks (randomizers, goals, failure conditions).
- A task registry, and suites for running the full benchmark or a subset (e.g. one robot's tasks).
- Stronger task checks: reset is deterministic, not solved at the start, no initial overlaps.
- Asset manifest with the source and license of every model, before open-sourcing.

**Results**
- Metrics beyond success (time, effort, energy, collisions, violation rates, latency, simulation speed).
- Aggregates across seeds, saved results (JSON/CSV), and Meshcat replays.

**Other**
- LLM controller harness (memory, a reference sheet of robot constants).
- Command line, config files, parallel workers, controller crash handling.
- License choice.
