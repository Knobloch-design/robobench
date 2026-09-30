"""Example task: the LEAP hand rotates a cube so a randomly chosen face ends up on top.

Shows what a filled-in Robot and Task look like. The bodies are still stubs.
"""

from robobench.robot import Robot
from robobench.task import Task

LEAP_URDF = "dex-urdf-main/robots/hands/leap_hand/leap_hand_right.urdf"

CUBE_FACES = ["+x", "-x", "+y", "-y", "+z", "-z"]


class LeapHand(Robot):
    """16-joint hand. Senses joint positions and velocities; accepts joint position targets."""

    name = "leap_hand"

    def add_to_diagram(self, builder, plant, parser):
        """Load LEAP_URDF, weld it palm-up, and add a position-controlled actuator per joint
        (the URDF has none)."""
        raise NotImplementedError

    def observe(self, plant, context):
        """{"joint_position": (16,), "joint_velocity": (16,)}"""
        raise NotImplementedError

    def apply_action(self, action, plant, context):
        """Expects {"joint_position_target": (16,)}."""
        raise NotImplementedError


class CubeReorientation(Task):
    """Bring a random target face of the cube to the top and keep it there."""

    name = "leap/cube_reorientation"
    robot = LeapHand()
    max_duration = 20.0

    def build_scene(self, builder, plant, parser):
        """A 6 cm cube with differently colored faces, resting in the palm."""
        raise NotImplementedError

    def reset(self, seed, plant, context):
        """Randomly tilt the cube in the palm, and pick a target face that isn't already on top.
        Returns {"target_face": ...}."""
        raise NotImplementedError

    def is_success(self, plant, context, goal):
        """The target face points up, within about 10 degrees."""
        raise NotImplementedError

    def description(self, goal):
        """Tell the controller which face to bring to the top."""
        return f"Rotate the cube in your hand until its {goal['target_face']} face points up."

    def is_failure(self, plant, context, goal):
        """The cube fell below the palm."""
        raise NotImplementedError
