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
"""Scene generator classes and functions."""


# Standard Library
from abc import abstractmethod
from typing import Any, Optional

# Third Party
from pxr import Usd

# NVIDIA
from nvidia.srl.abc.distinctive import Distinctive


class SceneGenerator(Distinctive):
    """An abstract base class for generating scenes."""

    def __init__(
        self,
        name: str,
        params: Optional[dict] = None,
        **kwargs: Any,
    ):
        """Initialize a new :class:`~srl.abc.scene_generator.SceneGenerator` object.

        Args:
            name: Name given to the scene.
            params: Set of parameters that uniquely define the scene.
            kwargs: Additional keyword arguments are passed to the parent class,
                :class:`~srl.abc.srl.SRL`.
        """
        # Initialize parent class
        super().__init__(params=params, **kwargs)

        # Initialize instance attributes
        self._name = name

    def name(self) -> str:
        """Get name attribute."""
        return self._name

    def __str__(self) -> str:
        """Return the readable string representation of the object."""
        return f"{self.__class__.__name__} ({self._name}): {self.__repr__()}"

    @abstractmethod
    def generate(self) -> Usd.Stage:
        """Generate the USD scene.

        Returns:
            Generated USD stage.
        """
