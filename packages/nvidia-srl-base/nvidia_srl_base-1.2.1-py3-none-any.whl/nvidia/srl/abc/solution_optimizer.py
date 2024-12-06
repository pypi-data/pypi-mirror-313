# SPDX-FileCopyrightText: Copyright (c) 2023 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
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
"""Solution optimizer classes and functions."""

# Standard Library
import pathlib
from abc import abstractmethod
from typing import Any, Optional

# NVIDIA
from nvidia.srl.abc.distinctive import Distinctive
from nvidia.srl.abc.task import Task
from nvidia.srl.abc.task_solver import TaskSolution


class SolutionOptimizer(Distinctive):
    """Abstract base class for optimizing task solutions."""

    def __init__(self, usd_path: str, task: Task, params: Optional[dict] = None, **kwargs: Any):
        """Initialize a new :class:`~srl.abc.solution_optimizer.SolutionOptimizer` object.

        Args:
            usd_path: Path to USD file that describes the scene.
            task: Task to be solved.
            params: Set of parameters that uniquely define the optimizer.
            kwargs: Additional keyword arguments are passed to the parent class,
                :class:`~srl.abc.distinctive.Distinctive`.
        """
        # Initialize parent class
        super().__init__(params=params, **kwargs)

        # Initialize instance attributes
        self._usd_path = pathlib.Path(usd_path).absolute()
        self._scene_dir_path = self._usd_path.parent
        self._task = task

    @abstractmethod
    def optimize(self, solution: TaskSolution) -> Optional[TaskSolution]:
        """Optimize the task solution.

        Args:
            solution: Solution to be optimized.

        Return:
            A task solution data object or None if an improved solution for that task is not found.
        """
