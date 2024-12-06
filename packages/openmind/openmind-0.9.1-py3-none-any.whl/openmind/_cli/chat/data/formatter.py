# Copyright 2024 the LlamaFactory team.
# Copyright (c) 2024 Huawei Technologies Co., Ltd.
#
# This code is inspired by the LLaMA-Factory.
# https://github.com/hiyouga/LLaMA-Factory/blob/main/src/llamafactory/data/formatter.py
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


import re
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional, Union, List, Tuple

from .data_utils import SLOTS
from .tool_utils import DefaultToolUtils, GLM4ToolUtils, FunctionCall
from ....utils import replace_invalid_characters

FORMATTER_CONTENT_REGEX = r"\{\{[a-zA-Z_][a-zA-Z0-9_]*\}\}"


@dataclass
class Formatter(ABC):
    slots: SLOTS = field(default_factory=list)
    tool_format: Optional[str] = None

    @abstractmethod
    def apply(self, **kwargs) -> SLOTS: ...

    def extract(self, content: str) -> Union[str, List["FunctionCall"]]:
        raise NotImplementedError


@dataclass
class EmptyFormatter(Formatter):
    def __post_init__(self):
        has_placeholder = False

        for slot in filter(lambda s: isinstance(s, str), self.slots):
            if re.search(FORMATTER_CONTENT_REGEX, slot):
                has_placeholder = True

        if has_placeholder:
            raise ValueError("Empty formatter should not contain any placeholder.")

    def apply(self, **kwargs) -> SLOTS:
        return self.slots


@dataclass
class StringFormatter(Formatter):
    def __post_init__(self):
        has_placeholder = False

        for slot in filter(lambda s: isinstance(s, str), self.slots):
            if re.search(FORMATTER_CONTENT_REGEX, slot):
                has_placeholder = True

        if not has_placeholder:
            raise ValueError("A placeholder is required in the string formatter.")

    def apply(self, **kwargs) -> SLOTS:
        elements = []

        for slot in self.slots:
            if isinstance(slot, str):
                for name, value in kwargs.items():
                    if not isinstance(value, str):
                        err_msg = f"Expected a string, got {value} with type {type(value)}."
                        raise TypeError(replace_invalid_characters(err_msg))

                    slot = slot.replace("{{" + name + "}}", value, 1)
                elements.append(slot)
            elif isinstance(slot, (dict, set)):
                elements.append(slot)
            else:
                err_msg = f"Input must be string, set[str] or dict[str, str], got {type(slot)}"
                raise TypeError(err_msg)

        return elements


@dataclass
class FunctionFormatter(Formatter):
    def __post_init__(self):
        if self.tool_format == "default":
            self.slots = DefaultToolUtils.get_function_slots() + self.slots
        elif self.tool_format == "glm4":
            self.slots = GLM4ToolUtils.get_function_slots() + self.slots
        else:
            err_msg = f"Tool format {self.tool_format} was not found."
            raise NotImplementedError(replace_invalid_characters(err_msg))

    def apply(self, **kwargs) -> SLOTS:
        content = kwargs.pop("content")
        functions: List[Tuple[str, str]] = []

        try:
            tool_calls = json.loads(content)
            if not isinstance(tool_calls, list):  # parallel function call
                tool_calls = [tool_calls]

            for tool_call in tool_calls:
                functions.append((tool_call["name"], json.dumps(tool_call["arguments"], ensure_ascii=False)))

        except json.JSONDecodeError:
            err_msg = f"Invalid JSON format in function message: {str([content])}"
            raise RuntimeError(replace_invalid_characters(err_msg))

        elements = []

        for name, arguments in functions:
            for slot in self.slots:
                if isinstance(slot, str):
                    slot = slot.replace("{{name}}", name).replace("{{arguments}}", arguments)
                    elements.append(slot)
                elif isinstance(slot, (dict, set)):
                    elements.append(slot)
                else:
                    err_msg = f"Input must be string, set[str] or dict[str, str], got {type(slot)}"
                    raise RuntimeError(err_msg)

        return elements


@dataclass
class ToolFormatter(Formatter):
    def __post_init__(self):
        if self.tool_format == "default":
            self._tool_formatter = DefaultToolUtils.tool_formatter
            self._tool_extractor = DefaultToolUtils.tool_extractor
        elif self.tool_format == "glm4":
            self._tool_formatter = GLM4ToolUtils.tool_formatter
            self._tool_extractor = GLM4ToolUtils.tool_extractor
        else:
            err_msg = f"Tool format {self.tool_format} was not found."
            raise NotImplementedError(err_msg)

    def apply(self, **kwargs) -> SLOTS:
        content = kwargs.pop("content")

        try:
            tools = json.loads(content)
            return [self._tool_formatter(tools) if len(tools) != 0 else ""]
        except json.JSONDecodeError:
            err_msg = f"Invalid JSON format in tool description: {str([content])}"
            raise RuntimeError(replace_invalid_characters(err_msg))

    def extract(self, content: str) -> Union[str, List["FunctionCall"]]:
        return self._tool_extractor(content)
