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
"""SRL object base class module."""

# Standard Library
from abc import ABC
from typing import Dict, Optional, Union

# NVIDIA
from nvidia.srl.tools.logger import Logger


class SRL(ABC):
    """Base class for all SRL classes."""

    # Count the number of initialized classes
    _initialized_count: Dict[str, int] = {}

    def __init__(
        self,
        logger_name: Optional[str] = None,
        log_level: Optional[Union[int, str]] = None,
        no_color: bool = False,
    ):
        """Initialize a new :class:`~srl.abc.srl.SRL` object.

        Args:
            logger_name: Set the name of the logger (default: "{class name}.{class count}").
            log_level: Set logging level for this class (default: logging.DEBUG).
            no_color: If true, disable logging text colors.
        """
        # Update class count
        class_name = self.__class__.__name__
        if class_name not in SRL._initialized_count:
            SRL._initialized_count[class_name] = 1
        else:
            SRL._initialized_count[class_name] += 1
        class_cnt = SRL._initialized_count[class_name]

        # Set default argument
        if logger_name is None:
            logger_name = f"{class_name}.{class_cnt-1}"

        # Initialize logger
        self.logger = Logger(name=logger_name, log_level=log_level, no_color=no_color)
