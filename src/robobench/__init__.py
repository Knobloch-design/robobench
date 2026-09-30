"""robobench: a robotics benchmark backed by error-controlled simulation (Drake + CENIC).

Controller process:
    controller.py          Controller: what users write (observation -> action)
    controller_server.py   serves a Controller over gRPC

Simulation process:
    remote_controller.py   RemoteController: reaches the controller over gRPC; launch_controller
    robot.py               Robot: model, sensors, accepted commands
    task.py                Task: scene, reset, success, description, demonstrations
    environment.py         Environment: the Drake/CENIC simulation for one task
    runner.py              run_episode, run_benchmark, check_demonstrations

Both:
    messages.py            numpy arrays <-> gRPC messages (schema TODO)
"""
