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
"""Task classes and functions."""

# Standard Library
from abc import abstractmethod
from typing import Any

# NVIDIA
from nvidia.srl.abc.distinctive import Distinctive


class Task(Distinctive):
    """Abstract base class for task objects."""

    def __init__(self, **kwargs: Any):
        """Initialize a new :class:`~srl.abc.task_solver.TaskSolver` object.

        Args:
            kwargs: Additional keyword arguments are passed to the parent class,
                :class:`~srl.abc.srl.SRL`.
        """
        # Initialize parent class
        super().__init__(**kwargs)

    @abstractmethod
    def serialize(self) -> str:
        """Serialize the task to a string."""

    @classmethod
    @abstractmethod
    def deserialize(cls, task_str: str) -> "Task":
        """De-serialize a task from a string."""
