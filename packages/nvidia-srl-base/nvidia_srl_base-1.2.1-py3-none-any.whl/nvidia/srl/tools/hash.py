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
"""Hash related functions."""

# Standard Library
import hashlib
from typing import Any, Optional


def hash_from_str(input_str: str, hash_len: Optional[int] = None) -> str:
    """Create a hash string from a string.

    Args:
        input_str: Input string.
        hash_len: Number of characters in hash output. Defaults to complete hash string.
    """
    input_utf8 = input_str.encode("utf-8")
    hash_alg = hashlib.sha1()
    hash_alg.update(input_utf8)
    hash_str = hash_alg.hexdigest()
    if hash_len is not None:
        hash_str = hash_str[0:hash_len]
    return hash_str


def hash_from_dict(input_dict: dict, **kwargs: Any) -> str:
    """Create a hash string from a dictionary.

    Args:
        input_dict: Input dictionary.
        kwargs: Additional keyword arguments are passed to
            :func:`~srl.util.hash.hash_from_str`.
    """
    input_str = str(sorted(input_dict.items()))
    return hash_from_str(input_str, **kwargs)
