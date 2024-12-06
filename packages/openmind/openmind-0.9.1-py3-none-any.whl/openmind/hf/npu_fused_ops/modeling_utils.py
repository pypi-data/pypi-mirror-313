# Copyright 2021 The HuggingFace Inc. team.
# 2024.09.02 - Adapt to openmind.
#              Huawei Technologies Co., Ltd.
# Copyright 2018 The Google AI Language Team Authors, Facebook AI Research authors and The HuggingFace Inc. team.
# Copyright (c) 2018, NVIDIA CORPORATION.  All rights reserved.
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
"""Utilities to dynamically load objects from the Hub."""

import os
import sys
import threading
import typing
import importlib
from typing import Optional, Union, Dict, List
from types import ModuleType
from pathlib import Path
import hashlib

import torch
import transformers
from transformers.dynamic_module_utils import get_relative_import_files
from transformers.utils.hub import HF_MODULES_CACHE

from .attenions.internlm2 import internlm2_forward
from .attenions.llama import LlamaNpuFusionAttention
from .attenions.qwen2 import Qwen2NPUAttention
from .attenions.mistral import MistralNpuFlashAttention
from ...utils import logging, replace_invalid_characters, is_torch_npu_available

from .rms_norm import om_rms_norm

logger = logging.get_logger()


_HF_REMOTE_CODE_LOCK = threading.Lock()


@classmethod
def _npu_fused_ops_imp(
    cls,
    config,
    use_flash_attention_2: bool = False,
    torch_dtype: Optional[torch.dtype] = None,
    device_map: Optional[Union[str, Dict[str, int]]] = None,
    check_device_map: bool = True,
):
    """
    Automatically checks and dispatches to a default attention implementation. In order of priority:
        1. An implementation specified in `config._attn_implementation` (due for example to the argument attn_implementation="sdpa" in from_pretrained).
        2. DEPRECATED: if use_flash_attention_2 is set to `True` and `flash_attn` is available, flash attention. (`LlamaFlashAttention` for example)
        3. SDPA implementation, if available and supported by the model type. (`LlamaSdpaAttention` for example)
        4. The default model's implementation otherwise (`LlamaAttention` for example) .
    """
    # Here we use config._attn_implementation_internal to check whether the attention implementation was explicitely set by the user.
    # The property `PretrainedConfig._attn_implementation` is never `None`, for backward compatibility (always fall back on "eager").
    # The `hasattr` here is used as some Transformers tests for some reason do not call PretrainedConfig __init__ (e.g. test_no_super_init_config_and_model)
    requested_attn_implementation = None
    if hasattr(config, "_attn_implementation_internal") and config._attn_implementation_internal is not None:
        if config._attn_implementation != "flash_attention_2" and use_flash_attention_2:
            error_msg = replace_invalid_characters(
                f'Both attn_implementation="{config._attn_implementation}" and `use_flash_attention_2=True` were used when loading the model, which are not compatible.'
                ' We recommend to just use `attn_implementation="flash_attention_2"` when loading the model.'
            )
            raise ValueError(error_msg)

        if config._attn_implementation not in ["eager", "sdpa", "flash_attention_2", "npu_fusion_attention"]:
            message = f'Specified `attn_implementation="{config._attn_implementation}"` is not supported. The only possible arguments are `attn_implementation="eager"` (manual attention implementation)'
            if cls._supports_flash_attn_2:
                message += ', `"attn_implementation=flash_attention_2"` (implementation using flash attention 2)'
            if cls._supports_sdpa:
                message += ', `"attn_implementation=sdpa"` (implementation using torch.nn.functional.scaled_dot_product_attention)'
            error_msg = replace_invalid_characters(message + ".")
            raise ValueError(error_msg)
        if config._attn_implementation_internal == "npu_fusion_attention":
            config.attn_implementation = "npu_fusion_attention"
        # If a config is passed with a preset attn_implementation, we skip the automatic dispatch and use the user-provided config, with hard checks that the requested attention implementation is available.
        requested_attn_implementation = config._attn_implementation_internal

    if use_flash_attention_2:
        logger.warning_once(
            'The model was loaded with use_flash_attention_2=True, which is deprecated and may be removed in a future release. Please use `attn_implementation="flash_attention_2"` instead.'
        )
        config._attn_implementation = "flash_attention_2"

    if config._attn_implementation == "flash_attention_2":
        cls._check_and_enable_flash_attn_2(
            config,
            torch_dtype=torch_dtype,
            device_map=device_map,
            hard_check_only=False,
            check_device_map=check_device_map,
        )
    elif requested_attn_implementation in [None, "sdpa"]:
        # use_flash_attention_2 takes priority over SDPA, hence SDPA treated in this elif.
        config = cls._check_and_enable_sdpa(
            config,
            hard_check_only=False if requested_attn_implementation is None else True,
        )

    elif is_torch_npu_available() and config._attn_implementation == "npu_fusion_attention":
        config._attn_implementation = "npu_fusion_attention"
        logger.warning_once("The model was loaded with npu_fusion_attention=True.")
    else:
        config._attn_implementation = "eager"

    if hasattr(config, "use_npu_rms_norm") and config.use_npu_rms_norm:
        logger.warning_once("The model was loaded with use_npu_rms_norm=True.")
        # use the npu_rms_norm when user choose to open this fusion operator and the npu is available
        transformers.models.llama.modeling_llama.LlamaRMSNorm = om_rms_norm.OmNpuRMSNorm
        transformers.models.qwen2.modeling_qwen2.Qwen2RMSNorm = om_rms_norm.OmNpuRMSNorm

    return config


def om_get_class_in_module(
    class_name: str,
    module_path: Union[str, os.PathLike],
    *,
    force_reload: bool = False,
) -> typing.Type:
    """
    Import a module on the cache directory for modules and extract a class from it.

    Args:
        class_name (`str`): The name of the class to import.
        module_path (`str` or `os.PathLike`): The path to the module to import.
        force_reload (`bool`, *optional*, defaults to `False`):
            Whether to reload the dynamic module from file if it already exists in `sys.modules`.
            Otherwise, the module is only reloaded if the file has changed.

    Returns:
        `typing.Type`: The class looked for.
    """
    name = os.path.normpath(module_path)
    if name.endswith(".py"):
        name = name[:-3]
    name = name.replace(os.path.sep, ".")
    module_file: Path = Path(HF_MODULES_CACHE) / module_path
    with _HF_REMOTE_CODE_LOCK:
        if force_reload:
            sys.modules.pop(name, None)
            importlib.invalidate_caches()
        cached_module: Optional[ModuleType] = sys.modules.get(name)
        module_spec = importlib.util.spec_from_file_location(name, location=module_file)

        # Hash the module file and all its relative imports to check if we need to reload it
        module_files: List[Path] = [module_file] + sorted(map(Path, get_relative_import_files(module_file)))
        module_hash: str = hashlib.sha256(b"".join(bytes(f) + f.read_bytes() for f in module_files)).hexdigest()

        module: ModuleType
        if cached_module is None:
            module = importlib.util.module_from_spec(module_spec)
            # insert it into sys.modules before any loading begins
            sys.modules[name] = module
        else:
            module = cached_module
        # reload in both cases, unless the module is already imported and the hash hits
        if getattr(module, "__transformers_module_hash__", "") != module_hash:
            module_spec.loader.exec_module(module)
            module.__transformers_module_hash__ = module_hash

        if class_name == "InternLM2ForCausalLM":
            npu_attention_class = type(
                "NPUFusionAttention", (module.INTERNLM2_ATTENTION_CLASSES["eager"],), {"forward": internlm2_forward}
            )
            module.INTERNLM2_ATTENTION_CLASSES.update({"npu_fusion_attention": npu_attention_class})
        return getattr(module, class_name)


def remote_model_patchs():
    transformers.dynamic_module_utils.get_class_in_module = om_get_class_in_module


def built_in_model_patchs():
    transformers.models.llama.modeling_llama.LLAMA_ATTENTION_CLASSES.update(
        {"npu_fusion_attention": LlamaNpuFusionAttention}
    )
    transformers.models.qwen2.modeling_qwen2.QWEN2_ATTENTION_CLASSES.update({"npu_fusion_attention": Qwen2NPUAttention})
    transformers.models.mistral.modeling_mistral.MISTRAL_ATTENTION_CLASSES.update(
        {"npu_fusion_attention": MistralNpuFlashAttention}
    )
