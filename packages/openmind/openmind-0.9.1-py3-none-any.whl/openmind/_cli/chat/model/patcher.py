# Copyright 2024 the LlamaFactory team.
# Copyright (c) 2024 Huawei Technologies Co., Ltd.
#
# This code is inspired by the LLaMA-Factory.
# https://github.com/hiyouga/LLaMA-Factory/blob/main/src/llamafactory/model/patcher.py
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


import os
import argparse
from types import MethodType
from typing import Dict, Any

import torch
from transformers import PretrainedConfig, PreTrainedTokenizerBase, PreTrainedTokenizer, PreTrainedModel
from transformers.utils import is_torch_npu_available

from .rope import configure_rope
from ....utils import logging
from ..chat_utils import infer_optim_dtype
from .embedding import resize_embedding_layer
from .attention import configure_attn_implementation

logger = logging.get_logger()
logging.set_verbosity_info()


def patch_tokenizer(tokenizer):
    if "PreTrainedTokenizerBase" not in str(tokenizer._pad.__func__):
        tokenizer._pad = MethodType(PreTrainedTokenizerBase._pad, tokenizer)


def patch_config(
    config: "PretrainedConfig",
    args: argparse.Namespace,
    init_kwargs: Dict[str, Any],
) -> None:
    if args.compute_dtype is None:
        if args.infer_dtype != "auto":
            args.compute_dtype = getattr(torch, args.infer_dtype)
        else:
            args.compute_dtype = infer_optim_dtype(model_dtype=getattr(config, "torch_dtype", None))

    if is_torch_npu_available():
        use_jit_compile = os.environ.get("JIT_COMPILE", "0").lower() in ["true", "1"]
        torch.npu.set_compile_mode(jit_compile=use_jit_compile)

    configure_attn_implementation(config, args)
    configure_rope(config, args)

    if args.use_cache:
        setattr(config, "use_cache", True)
        logger.info("Using KV cache for faster generation.")

    init_kwargs["low_cpu_mem_usage"] = args.low_cpu_mem_usage
    init_kwargs["torch_dtype"] = args.compute_dtype

    if init_kwargs["low_cpu_mem_usage"] is True:
        if "device_map" not in init_kwargs and args.device:
            init_kwargs["device_map"] = args.device


def patch_model(model: "PreTrainedModel", tokenizer: "PreTrainedTokenizer", args: argparse.Namespace) -> None:
    gen_config = model.generation_config

    if not gen_config.do_sample and (
        (gen_config.temperature is not None and gen_config.temperature != 1.0)
        or (gen_config.top_p is not None and gen_config.top_p != 1.0)
        or (gen_config.typical_p is not None and gen_config.typical_p != 1.0)
    ):
        gen_config.do_sample = True

    if "GenerationMixin" not in str(model.generate.__func__):
        model.generate = MethodType(PreTrainedModel.generate, model)

    if args.resize_vocab:
        resize_embedding_layer(model, tokenizer)
