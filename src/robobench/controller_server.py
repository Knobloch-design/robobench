"""The controller's side of the connection. Runs in the controller's own process.

    ┌──── simulation process ────┐         ┌──── controller process ────┐
    │  run_episode               │  gRPC   │  ControllerServer          │
    │    RemoteController ───────┼────────►│    your Controller         │
    │    (remote_controller.py)  │◄────────┼─── (this file)             │
    └────────────────────────────┘         └────────────────────────────┘

The user's Controller is wrapped in a gRPC server. The simulation process connects to
it and calls Reset and Act (defined in proto/controller.proto). Keeping the controller
in its own process means it can't read the simulator's true state, can use its own
Python packages without clashing with Drake's, and can't take the benchmark down if
it crashes or hangs.

Started by `launch_controller` in remote_controller.py, as:
    python -m robobench.controller_server my_package.my_module:MyController <port>
"""

from robobench.controller import Controller


class ControllerServer:
    """Answers the simulation's gRPC calls by calling the user's Controller.

    Will subclass the ControllerServicer class generated from proto/controller.proto.
    """

    def __init__(self, controller: Controller):
        """Wrap the user's controller."""
        self.controller = controller

    def Reset(self, request, context):
        """gRPC call at the start of an episode: unpack the TaskInfo and pass it to controller.reset."""
        raise NotImplementedError

    def Act(self, request, context):
        """gRPC call every control step: unpack the observation, call controller.act, pack the action."""
        raise NotImplementedError

    def Shutdown(self, request, context):
        """gRPC call at the end of the benchmark: stop the server so the process exits."""
        raise NotImplementedError


def serve(controller: Controller, port: int) -> None:
    """Start a gRPC server for `controller` on `port` and wait until Shutdown is called."""
    raise NotImplementedError


def load_controller(target: str) -> Controller:
    """Import and create a controller from a "package.module:ClassName" string."""
    raise NotImplementedError


if __name__ == "__main__":
    # Entry point for the controller process: load the named controller and serve it.
    import sys

    serve(load_controller(sys.argv[1]), port=int(sys.argv[2]))
