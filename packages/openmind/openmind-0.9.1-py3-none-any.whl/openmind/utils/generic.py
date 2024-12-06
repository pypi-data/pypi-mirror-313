# Copyright 2022 The HuggingFace Team. All rights reserved.
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
import copy
from contextlib import contextmanager
from enum import Enum
import os
import tempfile

from .constants import LOG_CONTENT_BLACK_LIST, BLANKS


@contextmanager
def working_or_temp_dir(working_dir, use_temp_dir: bool = False):
    if use_temp_dir:
        with tempfile.TemporaryDirectory(dir=os.path.expanduser("~")) as tmp_dir:
            yield tmp_dir
    else:
        yield working_dir


class ExplicitEnum(str, Enum):
    """
    Enum with more explicit error message for missing values.
    """

    @classmethod
    def _missing_(cls, value):
        error_msg = f"{value} is not a valid {cls.__name__}, please select one of {list(cls._value2member_map_.keys())}"
        raise ValueError(replace_invalid_characters(error_msg))


# vendored from distutils.util
def strtobool(val: str):
    """Convert a string representation of truth to true (1) or false (0).

    True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values are 'n', 'no', 'f', 'false', 'off', and '0'.
    Raises ValueError if 'val' is anything else.
    """
    val = val.lower()
    if val in {"y", "yes", "t", "true", "on", "1"}:
        return True
    if val in {"n", "no", "f", "false", "off", "0"}:
        return False
    error_msg = f"invalid truth value {val!r}"
    raise ValueError(replace_invalid_characters(error_msg))


def replace_invalid_characters(content: str, allow_line_separator=False) -> str:
    """Find and replace invalid characters in input content"""
    if not isinstance(content, str):
        raise TypeError("Input content for replacing invalid characters should be string format.")

    black_list_bak = copy.deepcopy(LOG_CONTENT_BLACK_LIST)

    if allow_line_separator:
        black_list_bak.remove("\n")

    for forbidden_str in black_list_bak:
        if forbidden_str in content:
            content = content.replace(forbidden_str, "")

    while BLANKS in content:
        content = content.replace(BLANKS, " ")

    return content
