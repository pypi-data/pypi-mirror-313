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
"""Functions to compare different types of quantities."""

# Third Party
import numpy as np

# NVIDIA
from nvidia.srl.basics.types import Vector


def vector_eq(vec0: Vector, vec1: Vector) -> bool:
    """Compare two vectors for equality."""
    if isinstance(vec0, np.ndarray) and isinstance(vec1, np.ndarray):
        return vec0.shape == vec1.shape and bool(np.all(vec0 == vec1))
    else:
        return type(vec0) == type(vec1) and vec0 == vec1  # noqa: E721
