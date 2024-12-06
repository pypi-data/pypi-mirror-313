# Copyright 2024 the LlamaFactory team.
# Copyright (c) 2024 Huawei Technologies Co., Ltd.
#
# This code is inspired by the LLaMA-Factory.
# https://github.com/hiyouga/LLaMA-Factory/blob/main/src/llamafactory/extras/misc.py
# https://github.com/hiyouga/LLaMA-Factory/blob/main/src/llamafactory/model/model_utils/misc.py
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


import argparse
from typing import Tuple

import torch
from transformers.utils import is_torch_npu_available, is_torch_bf16_gpu_available
from transformers import (
    PretrainedConfig,
    PreTrainedModel,
    PreTrainedTokenizer,
    LogitsProcessorList,
    InfNanRemoveLogitsProcessor,
)

from ...utils import replace_invalid_characters

IS_FP16_AVAILABLE = is_torch_npu_available()

try:
    IS_BF16_AVAILABLE = is_torch_bf16_gpu_available() or (is_torch_npu_available() and torch.npu.is_bf16_supported())
except Exception:
    IS_BF16_AVAILABLE = False


def infer_optim_dtype(model_dtype: "torch.dtype") -> "torch.dtype":
    r"""
    Infers the optimal dtype according to the model_dtype and device compatibility.
    """
    if IS_BF16_AVAILABLE and model_dtype == torch.bfloat16:
        return torch.bfloat16
    elif IS_FP16_AVAILABLE:
        return torch.float16
    else:
        return torch.float32


def register_autoclass(config: "PretrainedConfig", model: "PreTrainedModel", tokenizer: "PreTrainedTokenizer"):
    if "AutoConfig" in getattr(config, "auto_map", {}):
        config.__class__.register_for_auto_class()
    if "AutoModelForCausalLM" in getattr(config, "auto_map", {}):
        model.__class__.register_for_auto_class()
    if "AutoTokenizer" in tokenizer.init_kwargs.get("auto_map", {}):
        tokenizer.__class__.register_for_auto_class()


def count_parameters(model: "torch.nn.Module") -> Tuple[int, int]:
    r"""
    Returns the number of trainable parameters and number of all parameters in the model.
    """
    trainable_params, all_param = 0, 0

    for param in model.parameters():
        num_params = param.numel()

        # Due to the design of 4bit linear layers from bitsandbytes, multiply the number of parameters by itemsize
        if param.__class__.__name__ == "Params4bit":
            if hasattr(param, "quant_storage") and hasattr(param.quant_storage, "itemsize"):
                num_bytes = param.quant_storage.itemsize
            elif hasattr(param, "element_size"):  # for older pytorch version
                num_bytes = param.element_size()
            else:
                num_bytes = 1

            num_params = num_params * 2 * num_bytes

        all_param += num_params

        if param.requires_grad:
            trainable_params += num_params

    return trainable_params, all_param


def get_logits_processor() -> "LogitsProcessorList":
    r"""
    Gets logits processor that removes NaN and Inf logits.
    """
    logits_processor = LogitsProcessorList()
    logits_processor.append(InfNanRemoveLogitsProcessor())

    return logits_processor


def str2bool(value):
    if isinstance(value, bool):
        return value

    if isinstance(value, str) and value.lower() == "true":
        return True
    elif isinstance(value, str) and value.lower() == "false":
        return False
    else:
        err_msg = f"Boolean value expected, but got {type(value)}"
        raise argparse.ArgumentTypeError(replace_invalid_characters(err_msg))
