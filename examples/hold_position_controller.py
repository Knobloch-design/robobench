"""The simplest possible controller: hold the joint positions from the first observation.

Shows the minimum a user writes. Works with any robot whose command interface is
"joint_position". Run against the benchmark with:

    robobench run --suite examples/suites/example.yaml \
        --controller examples.hold_position_controller:HoldPositionController
"""

from __future__ import annotations

import numpy as np

from robobench_sdk import Action, Controller, IncompatibleSpecError, Observation, SessionInfo, TaskInfo


class HoldPositionController(Controller):
    def on_connect(self, session: SessionInfo) -> None:
        if session.action_spec.interface != "joint_position":
            raise IncompatibleSpecError("HoldPositionController needs the joint_position interface")

    def reset(self, task: TaskInfo) -> None:
        self._target: np.ndarray | None = None

    def act(self, observation: Observation) -> Action:
        if self._target is None:
            self._target = np.array(observation["joint_position"], copy=True)
        return {"q": self._target}
