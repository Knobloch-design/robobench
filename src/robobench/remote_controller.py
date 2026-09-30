"""The simulation's side of the connection. Runs in the simulation process.

`RemoteController` looks like any other Controller to the episode loop, but each call
is sent over gRPC to the real controller running in its own process
(see controller_server.py for the other side).
"""

import subprocess

from robobench.controller import Action, Controller, Observation, TaskInfo


class RemoteController(Controller):
    """Stand-in for a controller running in another process, reached over gRPC."""

    def __init__(self, address: str, process: subprocess.Popen | None = None):
        """Connect to the controller's gRPC server at `address` (host:port).

        `process` is the controller's process if we launched it, so `close` can stop it.
        """
        self.address = address
        self.process = process

    def reset(self, task: TaskInfo) -> None:
        """Send the task to the controller with the Reset call."""
        raise NotImplementedError

    def act(self, observation: Observation) -> Action:
        """Send the observation with the Act call and wait for the controller's action."""
        raise NotImplementedError

    def close(self) -> None:
        """Send Shutdown and wait for the controller's process to exit."""
        raise NotImplementedError


def launch_controller(target: str, python: str = "python", port: int = 50051) -> RemoteController:
    """Start a controller in its own process and connect to it.

    Args:
        target: The controller class, as "package.module:ClassName".
        python: The Python to run it with, so it can live in its own environment
            (for example one with PyTorch installed, without Drake).
        port: The port its gRPC server listens on.
    """
    raise NotImplementedError
