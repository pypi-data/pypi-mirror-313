# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
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
"""Python language helper classes and functions."""

# Standard Library
import inspect
from types import FrameType
from typing import Any, Callable, Dict, List, Optional


def get_inner_classes(cls: type, parent_class: Optional[type] = None) -> List[type]:
    """Get the inner classes of the given class.

    Optional condition it that the inner classes are subclasses of the given parent class.

    Args:
        cls: Class to get subclasses for.
        parent_class: Class type that subclasses must be child classes to.
    """
    return [
        getattr(cls, name)
        for name in dir(cls)
        if isinstance(getattr(cls, name), type)
        and getattr(cls, name).__module__ == cls.__module__
        and (parent_class is None or issubclass(getattr(cls, name), parent_class))
    ]


def get_nested_dict(dict_obj: Dict[str, Any], key_list: List[str]) -> Dict[str, Any]:
    """Retrieve a nested dictionary by following a list of keys.

    Args:
        dict_obj: Dictionary to get the nested dict from.
        key_list: List of key values that specify the root of the nested dict to return.
    """
    current = dict_obj
    for key in key_list:
        # Use get to avoid KeyError if key is not present
        current = current.get(key)  # type: ignore
        if not isinstance(current, dict):
            raise ValueError(
                f"Value of final key is not a dictionary. Key: {key}, Value: {current}"
            )
    return current


def get_function_arg_names(func: Callable[..., Any]) -> List[str]:
    """Inspect the given function and return the argument names as a list."""
    arg_names = [
        param.name for param in inspect.signature(func).parameters.values() if param.name != "self"
    ]
    return arg_names


def what_file_called_me(depth: int = 2, frame: Optional[FrameType] = None) -> str:
    """Determine what file a function is called from.

    Example:
        foo.py

        def foo():
            bar()

        bar.py

        def bar():
            print(f"The file that called me is {what_file_called_me()}")

        $ python foo.py
        >  The file that called me is foo.py

    Args:
        depth: Number of frames to go back in the stack.

    Returns:
        The name of the file that called the current function at the given depth.
    """
    # Get the current frame
    if depth < 0:
        raise ValueError("Depth must be greater than or equal to 0.")
    current_frame = frame
    if current_frame is None:
        current_frame = inspect.currentframe()
    if current_frame is None:
        raise RuntimeError("Failed to retrieve the current frame.")
    if depth == 0:
        return current_frame.f_code.co_filename
    elif current_frame.f_back is None:
        raise ValueError("Frame stack does not have enough depth.")
    else:
        return what_file_called_me(depth - 1, current_frame.f_back)
