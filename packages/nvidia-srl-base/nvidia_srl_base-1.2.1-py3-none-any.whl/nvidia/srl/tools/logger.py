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
"""Logger utility module."""

# Standard Library
import argparse
import logging
from typing import Any, Dict, Optional, Union

CRITICAL = logging.CRITICAL
ERROR = logging.ERROR
WARNING = logging.WARNING
INFO = logging.INFO
DEBUG = logging.DEBUG
NOTSET = logging.NOTSET


def name_from_level(level: int) -> str:
    """Get the log level name from the log level numerical value."""
    if level < 5:
        return "NOTSET"
    elif level < 15:
        return "DEBUG"
    elif level < 25:
        return "INFO"
    elif level < 35:
        return "WARNING"
    elif level < 45:
        return "ERROR"
    else:
        return "CRITICAL"


def level_from_name(name: str) -> int:
    """Get the log level numerical value from the log level name."""
    name_to_level_map = {
        "CRITICAL": CRITICAL,
        "ERROR": ERROR,
        "WARNING": WARNING,
        "INFO": INFO,
        "DEBUG": DEBUG,
        "NOTSET": NOTSET,
    }
    return name_to_level_map[name.upper()]


LIST_LEVELS = [
    NOTSET,
    DEBUG,
    INFO,
    WARNING,
    ERROR,
    CRITICAL,
]


LIST_NAMES = list(map(name_from_level, LIST_LEVELS))


class Logger:
    """Wrapper class around the `logging.getLogger` function."""

    def __init__(
        self,
        name: str,
        log_level: Optional[Union[int, str]] = None,
        no_color: bool = False,
    ):
        """Initialize a new :class:`~srl.util.logger.Logger` object.

        Args:
            name: Set the name of the logger.
            log_level: Set logging level for this class (default: logging.DEBUG).
            no_color: If true, disable logging text colors.
        """
        # Convert log level from string
        if isinstance(log_level, str):
            log_level = level_from_name(log_level)
        # Set default arguments
        if log_level is None:
            log_level = logging.DEBUG

        # Configure logger
        self._name = name
        self._logger = logging.getLogger(self._name)
        self._logger.setLevel(log_level)

        format = "[%(levelname)s] [%(name)s] - %(message)s"
        if no_color:
            stdout_formatter = logging.Formatter(format)
        else:
            stdout_formatter = _LoggingColoredFormatter(format)
        stdout_handler = logging.StreamHandler()
        stdout_handler.setLevel(logging.NOTSET)
        stdout_handler.setFormatter(stdout_formatter)

        self._logger.addHandler(stdout_handler)
        self._logger.propagate = False

    def get_level(self) -> int:
        """Return the current logging level."""
        return self._logger.level

    def get_level_name(self) -> str:
        """Return the name the current logging level."""
        return logging.getLevelName(self.get_level())

    def set_level(self, level: Union[int, str]) -> None:
        """Set the logging level."""
        level_int: int
        if isinstance(level, int):
            level_int = level
        elif isinstance(level, str):
            level_int = level_from_name(level)
        self._logger.setLevel(level_int)

    def debug(self, msg: str, *args: Any, **kwargs: Dict[Any, Any]) -> None:
        """Log a message with severity level "DEBUG"."""
        self._logger.debug(msg, *args, **kwargs)  # type: ignore

    def info(self, msg: str, *args: Any, **kwargs: Dict[Any, Any]) -> None:
        """Log a message with severity level "INFO"."""
        self._logger.info(msg, *args, **kwargs)  # type: ignore

    def warning(self, msg: str, *args: Any, **kwargs: Dict[Any, Any]) -> None:
        """Log a message with severity level "WARNING"."""
        self._logger.warning(msg, *args, **kwargs)  # type: ignore

    def error(self, msg: str, *args: Any, **kwargs: Dict[Any, Any]) -> None:
        """Log a message with severity level "ERROR"."""
        self._logger.error(msg, *args, **kwargs)  # type: ignore

    def critical(self, msg: str, *args: Any, **kwargs: Dict[Any, Any]) -> None:
        """Log a message with severity level "CRITICAL"."""
        self._logger.critical(msg, *args, **kwargs)  # type: ignore

    def log(self, level: int, msg: str, *args: Any, **kwargs: Dict[Any, Any]) -> None:
        """Log a message with the given severity level."""
        self._logger.log(level, msg, *args, **kwargs)  # type: ignore

    def exception(self, msg: str, *args: Any, **kwargs: Dict[Any, Any]) -> None:
        """Log a message with severity level "ERROR" with exception information."""
        self._logger.exception(msg, *args, **kwargs)  # type: ignore


class _LoggingColoredFormatter(logging.Formatter):
    """This class is used to add color to logging output."""

    GRAY = "\x1b[38;5;247m"
    GREEN = "\x1b[38;5;2m"
    BLUE = "\x1b[38;5;27m"
    YELLOW = "\x1b[38;5;11m"
    RED = "\x1b[38;5;1m"
    BOLD_RED = "\x1b[31;1m"
    RESET = "\x1b[0m"

    def __init__(self, fmt: str):
        """Initialize a new `_ColoredFormatter` object."""
        super().__init__()
        self.fmt = fmt
        self.FORMATS = {
            logging.DEBUG: self.GRAY + self.fmt + self.RESET,
            logging.INFO: self.GREEN + self.fmt + self.RESET,
            logging.WARNING: self.YELLOW + self.fmt + self.RESET,
            logging.ERROR: self.RED + self.fmt + self.RESET,
            logging.CRITICAL: self.BOLD_RED + self.fmt + self.RESET,
        }

    def format(self, record: logging.LogRecord) -> str:
        """Override the standard `logging.Formatter.format` method."""
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def add_logger_args(parser: argparse.ArgumentParser, default_level: str = "info") -> None:
    """Add logger argparse arguments to the parser object.

    Args:
        parser: Argparse object to add the logger command to.
        default_level: Default logger level to use.
    """
    parser.add_argument(
        "--log-level",
        default=default_level,
        choices=list(map(str.lower, LIST_NAMES)),
        help="Set the logger level.",
    )
