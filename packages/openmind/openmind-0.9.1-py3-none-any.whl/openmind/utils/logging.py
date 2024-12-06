# Copyright (c) Huawei Technologies Co., Ltd. 2023-2023, All rights reserved.
# Copyright 2023 The HuggingFace Inc. team.
# 2024.05.25 - Redirect logs to standard output for StreamHandler
#              Huawei Technologies Co., Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Note: This file is mainly copied from transformers.logger
# https://github.com/huggingface/transformers/blob/v4.35.2/src/transformers/utils/logging.py
from collections import OrderedDict
import logging
import re
import sys
import threading

from tqdm import auto as tqdm_lib

from .generic import replace_invalid_characters
from .constants import OPENMIND_MODEL_URL, HUGGINGFACE_MODEL_URL

_lock = threading.Lock()
_global_handler = None
TQDM_ACTIVE = True

log_levels = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
}

_default_log_level = logging.WARNING


def set_verbosity(verbosity: int) -> None:
    """Set the verbosity level for root logger"""

    _configure_library_root_logger()
    get_logger().setLevel(verbosity)


def set_verbosity_info():
    """Set the verbosity to the `INFO` level."""
    return set_verbosity(log_levels.get("info", _default_log_level))


def set_verbosity_warning():
    """Set the verbosity to the `WARNING` level."""
    return set_verbosity(log_levels.get("warning", _default_log_level))


def set_verbosity_debug():
    """Set the verbosity to the `DEBUG` level."""
    return set_verbosity(log_levels.get("debug", _default_log_level))


def set_verbosity_error():
    """Set the verbosity to the `ERROR` level."""
    return set_verbosity(log_levels.get("error", _default_log_level))


def set_verbosity_critical():
    """Set the verbosity to the `CRITICAL` level."""
    return set_verbosity(log_levels.get("critical", _default_log_level))


def _get_library_name() -> str:
    return __name__.split(".")[0]


class EmptyTqdm:
    """Dummy tqdm which doesn't do anything."""

    def __init__(self, *args, **kwargs):  # pylint: disable=unused-argument
        self._iterator = args[0] if args else None

    def __iter__(self):
        return iter(self._iterator)

    def __getattr__(self, _):
        """Return empty function."""

        def empty_fn(*args, **kwargs):  # pylint: disable=unused-argument
            return

        return empty_fn

    def __enter__(self):
        return self

    def __exit__(self, type_, value, traceback):
        return


class TqdmCls:
    def __init__(self):
        self._lock = None

    def __call__(self, *args, **kwargs):
        if TQDM_ACTIVE:
            return tqdm_lib.tqdm(*args, **kwargs)
        else:
            return EmptyTqdm(*args, **kwargs)

    def set_lock(self, *args, **kwargs):
        if TQDM_ACTIVE:
            return tqdm_lib.tqdm.set_lock(*args, **kwargs)

    def get_lock(self):
        if TQDM_ACTIVE:
            return tqdm_lib.tqdm.get_lock()


tqdm = TqdmCls()


def _configure_library_root_logger():
    global _global_handler
    with _lock:
        if _global_handler:
            return
        _global_handler = logging.StreamHandler(sys.stdout)
        _global_handler.setFormatter(logging.Formatter("[%(levelname)s][%(asctime)s]: %(message)s"))
        # Apply our default configuration to the library root logger.
        library_root_logger = logging.getLogger(_get_library_name())
        library_root_logger.addHandler(_global_handler)
        library_root_logger.setLevel(_default_log_level)
        library_root_logger.propagate = False


class StringFilter(logging.Filter):
    """
    replace some keywords for logger
    """

    def __init__(self, allow_line_separator=False):
        super().__init__()
        self.allow_line_separator = allow_line_separator

    def filter(self, record):
        # Cannot perform global keyword replacement, can only replace one sentence at a time.
        # In some cases, not replacing may be correct.
        if isinstance(record.msg, str):
            replace_dict = OrderedDict(
                {
                    f"on {HUGGINGFACE_MODEL_URL}": f"on {OPENMIND_MODEL_URL.lstrip('https://')}",
                }
            )
            replace_dict = dict((re.escape(k), v) for k, v in replace_dict.items())
            pattern = re.compile("|".join(replace_dict.keys()))
            record.msg = pattern.sub(lambda m: replace_dict[re.escape(m.group(0))], record.msg)
            record.msg = replace_invalid_characters(record.msg, allow_line_separator=self.allow_line_separator)
        return True


def get_logger(name=None, allow_line_separator=False) -> logging.Logger:
    """
    Return a logger with the specified name. If name is not specified, return the root
    logger
    """
    if name is None:
        name = _get_library_name()

    _configure_library_root_logger()
    logger = logging.getLogger(name)
    logger.addFilter(StringFilter(allow_line_separator=allow_line_separator))
    return logger


__all__ = [
    "get_logger",
    "set_verbosity",
    "set_verbosity_info",
    "set_verbosity_warning",
    "set_verbosity_debug",
    "set_verbosity_error",
    "set_verbosity_critical",
]
