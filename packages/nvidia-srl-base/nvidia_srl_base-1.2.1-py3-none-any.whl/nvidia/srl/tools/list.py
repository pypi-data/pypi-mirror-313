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
"""Helper functions for lists."""

# Standard Library
from typing import Any, Iterable, List, Union


def to_pretty_str(
    input_list: Iterable[Any], prefix: str = "", separator: str = "\n", suffix: str = ""
) -> str:
    r"""Transform a list into a pretty string.

    Args:
        input_list: The list to be transformed.
        prefix: The string that is prepended to each list element.
        separator: The string separator between each element in the list. Defaults to "\\n".
        suffix: The string that is appended to each list element.

    Returns:
        The input list as a pretty string.
    """
    return separator.join(f"{prefix}{elem}{suffix}" for elem in input_list)


def cumulative_sum(sequence: List[Union[int, float]]) -> List[Union[int, float]]:
    """Compute the cumulative sum of a list."""
    if not sequence:
        return []
    new_sequence = sequence[:1]
    for value in sequence[1:]:
        new_sequence.append(new_sequence[-1] + value)
    return new_sequence
