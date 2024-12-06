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
"""Task generator classes and functions."""

# Standard Library
from abc import abstractmethod
from typing import Any, Optional

# Third Party
from pxr import Usd

# NVIDIA
from nvidia.srl.abc.distinctive import Distinctive
from nvidia.srl.abc.task import Task
from nvidia.srl.basics.types import PathLike


class TaskGenerator(Distinctive):
    """Abstract base class for generating tasks."""

    def __init__(self, stage: Usd.Stage, params: Optional[dict] = None, **kwargs: Any):
        """Initialize a new :class:`~srl.abc.task_generator.TaskGenerator` object.

        Args:
            stage: USD stage that describes the world scene.
            params: Set of parameters that uniquely define the scene.
            kwargs: Additional keyword arguments are passed to the parent class,
                :class:`~srl.abc.srl.SRL`.
        """
        # Initialize parent class
        super().__init__(params=params, **kwargs)

        # Initialize instance attributes
        self._stage = stage

    @classmethod
    def init_from_usd_path(cls, usd_path: PathLike, **kwargs: Any) -> "TaskGenerator":
        """Create new `WorldStructure` object from USD path.

        Args:
            usd_path: File path to load the USD from.

        Returns:
            WorldStructure: New `WorldStructure` object initialized from USD path.
        """
        if not isinstance(usd_path, str):
            usd_path = str(usd_path)
        stage = Usd.Stage.Open(usd_path)
        return cls(stage, **kwargs)

    @abstractmethod
    def generate(self) -> Task:
        """Generate the task.

        Returns:
            A newly generated task.
        """
