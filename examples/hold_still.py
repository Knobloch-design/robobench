"""The simplest controller: keep every joint where it started. A baseline, and a failure demo.

This file is all a user writes. The benchmark runs it in its own process and talks to
it over gRPC.
"""

from robobench.controller import Controller


class HoldStill(Controller):
    """Commands the starting joint positions forever."""

    def reset(self, task):
        """Forget the previous episode's starting pose."""
        self.target = None

    def act(self, observation):
        """Remember the first joint positions seen, and keep commanding them."""
        if self.target is None:
            self.target = observation["joint_position"].copy()
        return {"joint_position_target": self.target}


if __name__ == "__main__":
    # Run the cube task three times with this controller in a separate process.
    from examples.leap_cube_reorientation import CubeReorientation
    from robobench.remote_controller import launch_controller
    from robobench.runner import run_benchmark

    controller = launch_controller("examples.hold_still:HoldStill")
    for result in run_benchmark([CubeReorientation()], controller, seeds=[0, 1, 2]):
        print(result)
    controller.close()
