"""robobench: run arbitrary controllers through Drake-simulated robot tasks, on CENIC.

Layout:
    config              run/episode settings, CENIC physics settings, timing/validation mode enums
    assets              asset manifest (robots, manipulands, scenes) with source and license
    robots              robot definitions and their hardware-level command interfaces
    sensors             sensor definitions and the configurable observation pipeline
    scenes              pre-generated environments (terrain, buildings, tabletops)
    tasks               Task base class, helpers, demonstrations, validation, registry, library
    validation          command limit checking and invalid-command (NaN/shape) handling
    metrics             per-step / per-episode metrics and aggregation
    controller_process  launching the controller's separate process and its gRPC client
    sim                 the Drake/CENIC diagram wrapper and the lockstep / real-time stepping
    runner              episode loop, suites, and the parallel benchmark runner
    results             records, writers, and Meshcat recordings
"""

__version__ = "0.0.1"
