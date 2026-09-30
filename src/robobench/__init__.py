"""robobench: run arbitrary controllers through Drake-simulated robot scenarios.

Layout:
    config              run/episode/sim settings and the timing/validation mode enums
    robots              robot definitions and their hardware-level command interfaces
    sensors             sensor definitions and the configurable observation pipeline
    scenes              pre-generated environments (terrain, buildings, tabletops)
    scenarios           building blocks for tests + registry + ready-made test library
    validation          command limit checking and invalid-command (NaN/shape) handling
    metrics             per-step / per-episode metrics and aggregation
    controller_process  launching and talking to the controller's separate process
    sim                 the Drake diagram wrapper and the lockstep / real-time stepping
    runner              episode loop, suites, and the parallel benchmark runner
    results             records, writers, and Meshcat recordings
"""

__version__ = "0.0.1"
