# SPDX-FileCopyrightText: Copyright (c) 2022 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
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
"""Distinctive based class."""

# Standard Library
from typing import Any, Optional

# NVIDIA
from nvidia.srl.abc.srl import SRL
from nvidia.srl.tools.hash import hash_from_dict


class Distinctive(SRL):
    """A base class to use a parameter dictionary to uniquely define class instances."""

    HASH_LEN = 7

    def __init__(
        self,
        params: Optional[dict] = None,
        **kwargs: Any,
    ):
        """Initialize a new :class:`~srl.abc.param_class.ParamClass` object.

        Args:
            params: Set of parameters that uniquely define the class. Used to create hash string.
            kwargs: Additional keyword arguments are passed to the parent class,
                :class:`~srl.abc.srl.SRL`.
        """
        # Initialize parent class
        super().__init__(**kwargs)

        # Initialize instance attributes
        if params is None:
            params = dict()
        self._params = params

    def param(self, key: str) -> Any:
        """Get value from the params associated with the given key."""
        return self._params[key]

    def params(self) -> dict:
        """Get params attribute."""
        return self._params

    def hash_str(self) -> str:
        """Generate unique hash string for this object."""
        return hash_from_dict(self._params, hash_len=self.HASH_LEN)

    def __repr__(self) -> str:
        """Return the unambiguous string representation of the object."""
        return f"({self.hash_str()}) {self._params}"

    def __str__(self) -> str:
        """Return the readable string representation of the object."""
        return f"{self.__class__.__name__}: {repr(self)}"
