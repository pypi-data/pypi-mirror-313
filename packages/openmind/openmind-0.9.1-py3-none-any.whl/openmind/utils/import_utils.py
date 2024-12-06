# Copyright (c) Huawei Technologies Co., Ltd. 2023-2023, All rights reserved.
# Copyright 2022 The HuggingFace Inc. team.
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

# This code is borrowed and modified from
# https://github.com/huggingface/transformers/blob/v4.36.0/src/transformers/utils/import_utils.py

from collections import OrderedDict
from functools import lru_cache
import importlib
import importlib.metadata
from itertools import chain
import os
from types import ModuleType
from typing import Any

from .constants import MINDSPORE_INSTALL_URL, PYTORCH_INSTALL_URL
from .logging import get_logger
from ..utils.generic import replace_invalid_characters


logger = get_logger(__name__)


def _is_package_available(pkg_name: str) -> bool:
    # Check we're not importing a "pkg_name" directory somewhere but the actual library by trying to grab the version
    package_exists = importlib.util.find_spec(pkg_name) is not None
    if package_exists:
        try:
            _ = importlib.metadata.metadata(pkg_name)
            return True
        except importlib.metadata.PackageNotFoundError:
            return False
    return False


_torch_available = _is_package_available("torch")
_ms_available = _is_package_available("mindspore")
_tokenizers_available = _is_package_available("tokenizers")

_frameworks = []
if _torch_available:
    _frameworks.append("pt")
if _ms_available:
    _frameworks.append("ms")


def get_framework():
    if not _frameworks:
        return "N/A"
    elif len(_frameworks) == 1:
        return _frameworks[0]  # one of "pt", "ms" or "N/A"

    error_msg = f"Multiple frameworks detected, including: {', '.join(_frameworks)}. "
    raise RuntimeError(replace_invalid_characters(error_msg))


CURRENT_FRAMEWORK = get_framework()


@lru_cache
def is_torch_available():
    return _torch_available


@lru_cache
def is_tokenizers_available():
    return _tokenizers_available


@lru_cache
def is_vision_available():
    _pil_available = importlib.util.find_spec("PIL") is not None
    if _pil_available:
        try:
            package_version = importlib.metadata.version("Pillow")
        except importlib.metadata.PackageNotFoundError:
            try:
                package_version = importlib.metadata.version("Pillow-SIMD")
            except importlib.metadata.PackageNotFoundError:
                return False
        logger.debug(f"Detected PIL version {package_version}")
    return _pil_available


@lru_cache
def is_detectron2_available():
    return _is_package_available("detectron2")


@lru_cache
def is_lmeval_available():
    return _is_package_available("lm_eval")


@lru_cache
def is_pytesseract_available():
    return _is_package_available("pytesseract")


@lru_cache
def is_torch_npu_available():
    "Checks if `torch_npu` is installed and potentially if a NPU is in the environment"
    if not _torch_available or importlib.util.find_spec("torch_npu") is None:
        return False

    import torch
    import torch_npu  # noqa: F401

    return hasattr(torch, "npu") and torch.npu.is_available()


@lru_cache
def is_ms_available():
    return _ms_available


@lru_cache
def is_transformers_available():
    return _is_package_available("transformers")


@lru_cache
def is_mindformers_available():
    return _is_package_available("mindformers")


@lru_cache
def is_diffusers_available():
    return _is_package_available("diffusers")


@lru_cache
def is_mindone_available():
    return _is_package_available("mindone")


@lru_cache
def is_mindnlp_available():
    return _is_package_available("mindnlp")


@lru_cache
def is_sentencepiece_available():
    return _is_package_available("sentencepiece")


@lru_cache
def is_decord_available():
    return _is_package_available("decord")


@lru_cache
def is_timm_available():
    return _is_package_available("timm")


PYTORCH_IMPORT_ERROR = f"""
{0} requires the PyTorch library but it was not found in your environment. Checkout the instructions on the
installation page: {PYTORCH_INSTALL_URL} and follow the ones that match your environment.
Please note that you may need to restart your runtime after installation.
"""

TRANSFORMERS_IMPORT_ERROR = """
{0} requires the Transformers library but it was not found in your environment. You can install it with pip:
`pip install transformers`. Please note that you may need to restart your runtime after installation.
"""

MINDSPORE_IMPORT_ERROR = f"""
{{0}} requires the MindSpore library but it was not found in your environment. Checkout the instructions on the
installation page: {MINDSPORE_INSTALL_URL} and follow the ones that match your environment.
Please note that you may need to restart your runtime after installation.
"""

MINDFORMERS_IMPORT_ERROR = """
{0} requires the Mindformers library but it was not found in your environment. You can install it with pip:
`pip install mindformers`. Please note that you may need to restart your runtime after installation.
"""

FRAMEWORK_NOT_FOUND_ERROR = """
{0} requires PyTorch or MindSpore, but the framework was not found in your environment. Please install one
framework you want to use and note that you may need to restart your runtime after installation.
"""

BACKENDS_MAPPING = OrderedDict(
    [
        ("torch", (is_torch_available, PYTORCH_IMPORT_ERROR)),
        ("transformers", (is_transformers_available, TRANSFORMERS_IMPORT_ERROR)),
        ("mindspore", (is_ms_available, MINDSPORE_IMPORT_ERROR)),
        ("mindformers", (is_mindformers_available, MINDFORMERS_IMPORT_ERROR)),
    ]
)


def requires_backends(obj, backends):
    if not isinstance(backends, (list, tuple)):
        backends = [backends]

    name = obj.__name__ if hasattr(obj, "__name__") else obj.__class__.__name__

    # Raise an error for users who might not realize that classes require a framework, either PyTorch
    # or MindSpore.
    if "torch" in backends and "mindspore" in backends:
        if not is_torch_available() and not is_ms_available():
            error_msg = FRAMEWORK_NOT_FOUND_ERROR.format(name)
            raise ImportError(replace_invalid_characters(error_msg))

    checks = (BACKENDS_MAPPING[backend] for backend in backends)
    failed = [msg.format(name) for available, msg in checks if not available()]
    if failed:
        error_msg = "".join(failed)
        raise ImportError(replace_invalid_characters(error_msg))


class DummyObject(type):
    """
    Metaclass for the dummy objects. Any class inheriting from it will return the ImportError generated by
    `requires_backend` each time a user tries to access any method of that class.
    """

    def __getattribute__(cls, key):
        if key.startswith("_") and key != "_from_config":
            return super().__getattribute__(key)
        requires_backends(cls, cls._backends)


class _LazyModule(ModuleType):
    """
    Module class that surfaces all objects but only performs associated imports when the objects are requested.
    """

    # Very heavily inspired by optuna.integration._IntegrationModule
    # https://github.com/optuna/optuna/blob/master/optuna/integration/__init__.py
    def __init__(self, name, module_file, import_structure, module_spec=None, extra_objects=None):
        super().__init__(name)
        self._modules = set(import_structure.keys())
        self._class_to_module = {}
        for key, values in import_structure.items():
            for value in values:
                self._class_to_module[value] = key
        # Needed for autocompletion in an IDE
        self.__all__ = list(import_structure.keys()) + list(chain(*import_structure.values()))
        self.__file__ = module_file
        self.__spec__ = module_spec
        self.__path__ = [os.path.dirname(module_file)]
        self._objects = {} if extra_objects is None else extra_objects
        self._name = name
        self._import_structure = import_structure

    # Needed for autocompletion in an IDE
    def __dir__(self):
        result = super().__dir__()
        # The elements of self.__all__ that are submodules may or may not be in the dir already, depending on whether
        # they have been accessed or not. So we only add the elements of self.__all__ that are not already in the dir.
        for attr in self.__all__:
            if attr not in result:
                result.append(attr)
        return result

    def __getattr__(self, name: str) -> Any:
        if name in self._objects:
            return self._objects[name]
        if name in self._modules:
            value = self._get_module(name)
        elif name in self._class_to_module.keys():
            module = self._get_module(self._class_to_module[name])
            value = getattr(module, name)
        else:
            error_msg = f"module {self.__name__} has no attribute {name}"
            raise AttributeError(replace_invalid_characters(error_msg))

        setattr(self, name, value)
        return value

    def __reduce__(self):
        return (self.__class__, (self._name, self.__file__, self._import_structure))

    def _get_module(self, module_name: str):
        try:
            return importlib.import_module("." + module_name, self.__name__)
        except Exception as e:
            error_msg = (
                f"Failed to import {self.__name__}.{module_name} because of the following error "
                f"(look up to see its traceback):{e}"
            )
            raise RuntimeError(replace_invalid_characters(error_msg)) from e
