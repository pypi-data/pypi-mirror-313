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
"""Collection of general SRL Enum types."""
# Standard Library
import enum
from enum import auto  # noqa: F401


class Enum(enum.Enum):
    """Overload of the enum.Enum class to allow for easy printing of Enums."""

    def __str__(self) -> str:
        """Convert to string."""
        return f"{self.__class__.__name__}.{self.name}"

    def __repr__(self) -> str:
        """Convert to default representation."""
        return str(self)


class BodyType(Enum):
    """Enum to denote the body type of an object."""

    RIGID = auto()
    ARTICULATED = auto()


class PoseType(Enum):
    """Enum to denote the pose type of an object."""

    FIXED = auto()
    FLOATING = auto()
