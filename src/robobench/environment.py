"""The simulation for one task: a Drake diagram with the robot and scene, run with CENIC.

Lives in the simulation process. The controller is never part of this diagram; it gets
observations and sends actions over gRPC.

CENIC is Drake's error-controlled integrator for contact. It needs a continuous-time
plant (time_step=0) and chooses its own step sizes to stay within `accuracy`.
"""

from pydrake.multibody.parsing import Parser
from pydrake.multibody.plant import AddMultibodyPlant, MultibodyPlantConfig
from pydrake.systems.analysis import ApplySimulatorConfig, Simulator, SimulatorConfig
from pydrake.systems.framework import DiagramBuilder

from robobench.controller import Action, Observation
from robobench.task import Task


class Environment:
    """Builds and steps the simulation for one task."""

    def __init__(self, task: Task, accuracy: float = 1e-3):
        """Build the task's diagram (robot + scene) on a continuous-time plant, and a CENIC simulator for it."""
        self.task = task

        builder = DiagramBuilder()
        self.plant, self.scene_graph = AddMultibodyPlant(MultibodyPlantConfig(time_step=0.0), builder)
        parser = Parser(self.plant)
        task.robot.add_to_diagram(builder, self.plant, parser)
        task.build_scene(builder, self.plant, parser)
        self.plant.Finalize()
        self.diagram = builder.Build()

        self.simulator = Simulator(self.diagram)
        ApplySimulatorConfig(SimulatorConfig(integration_scheme="cenic", accuracy=accuracy), self.simulator)

    @property
    def context(self):
        """The plant's context: the true state of the simulation."""
        return self.plant.GetMyMutableContextFromRoot(self.simulator.get_mutable_context())

    @property
    def time(self) -> float:
        """Seconds of simulated time since the episode started."""
        return self.simulator.get_context().get_time()

    def reset(self, seed: int) -> dict:
        """Start a new episode. Returns the goal."""
        self.diagram.SetDefaultContext(self.simulator.get_mutable_context())
        self.simulator.get_mutable_context().SetTime(0.0)
        goal = self.task.reset(seed, self.plant, self.context)
        self.simulator.Initialize()
        return goal

    def observe(self) -> Observation:
        """The robot's current sensor readings: what gets sent to the controller."""
        return self.task.robot.observe(self.plant, self.context)

    def apply_action(self, action: Action) -> None:
        """Send the controller's command to the robot's actuators. It holds until the next command."""
        self.task.robot.apply_action(action, self.plant, self.context)

    def step(self, duration: float) -> None:
        """Advance the simulation by `duration` seconds."""
        self.simulator.AdvanceTo(self.time + duration)
