# SPDX-FileCopyrightText: Copyright (c) 2021 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Task solver classes and functions."""

# Standard Library
import pathlib
from abc import abstractmethod
from dataclasses import dataclass
from typing import Any, List, Optional, Tuple

# NVIDIA
from nvidia.srl.abc.distinctive import Distinctive
from nvidia.srl.abc.task import Task
from nvidia.srl.basics.types import WorldState
from nvidia.srl.tools.list import cumulative_sum


# TODO (roflaherty): Convert this to a child class of `srl.abc.trajectory.Trajectory`
@dataclass
class TaskSolution:
    """Data class that holds a solution for a task."""

    times: List[float]
    states: List[WorldState]

    def start_time(self) -> float:
        """Get the start time of the solution."""
        return self.times[0]

    def end_time(self) -> float:
        """Get the end time of the solution."""
        return self.times[-1]

    def start_state(self) -> WorldState:
        """Get the start state of the solution."""
        return self.states[0]

    def end_state(self) -> WorldState:
        """Get the end state of the solution."""
        return self.states[-1]

    def duration(self) -> float:
        """Get the time duration the solution."""
        return self.end_time() - self.start_time()

    def length(self) -> int:
        """Get the number of states in the solution."""
        return len(self.states)

    def time_steps(self) -> List[float]:
        """Get the time stepped between each pair of states."""
        return [t2 - t1 for t1, t2 in zip(self.times[:-1], self.times[1:])]

    def retime(self, start_time: float) -> "TaskSolution":
        """Retime the solution from a new start time."""
        new_times = cumulative_sum([start_time] + self.time_steps())
        return TaskSolution(times=new_times, states=self.states[:])

    def reverse(self, start_time: Optional[float] = None) -> "TaskSolution":
        """Reverse the states in the solution."""
        if start_time is None:
            start_time = self.times[0]
        new_times = cumulative_sum([start_time] + self.time_steps()[::-1])
        return TaskSolution(times=new_times, states=self.states[::-1])

    def __len__(self) -> int:
        """Get the number of states in the solution."""
        return self.length()

    def __iter__(self) -> "TaskSolution":
        """Return itself as an iterator."""
        self._current_index = 0
        return self

    def __next__(self) -> Tuple[float, WorldState]:
        """Return the next element in the iteration of itself."""
        if self._current_index < self.length():
            time = self.times[self._current_index]
            state = self.states[self._current_index]
            self._current_index += 1
            return (time, state)
        raise StopIteration


class SolverError(Exception):
    """An exception that occurs when solving a task."""

    pass


class TaskSolver(Distinctive):
    """Abstract base class for solving tasks."""

    def __init__(self, usd_path: str, task: Task, params: Optional[dict] = None, **kwargs: Any):
        """Initialize a new :class:`~srl.abc.task_solver.TaskSolver` object.

        Args:
            usd_path: Path to USD file that describes the scene.
            task: Task to be solved.
            params: Set of parameters that uniquely define the solver.
            kwargs: Additional keyword arguments are passed to the parent class,
                :class:`~srl.abc.srl.SRL`.
        """
        # Initialize parent class
        super().__init__(params=params, **kwargs)

        # Initialize instance attributes
        self._usd_path = pathlib.Path(usd_path).absolute()
        self._scene_dir_path = self._usd_path.parent
        self._task = task

    @abstractmethod
    def solve(self) -> Optional[TaskSolution]:
        """Solve the task.

        Return:
            A task solution data object or None if a solution for that task is not found.
        """
