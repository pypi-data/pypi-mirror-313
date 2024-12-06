# Copyright 2024 the LlamaFactory team.
# Copyright (c) 2024 Huawei Technologies Co., Ltd.
#
# This code is inspired by the LLaMA-Factory.
# https://github.com/hiyouga/LLaMA-Factory/blob/main/src/llamafactory/model/adapter.py
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

from peft import PeftModel
from transformers import PreTrainedModel

from ....utils import logging

logger = logging.get_logger()
logging.set_verbosity_info()


def init_adapter(model: "PreTrainedModel", args: argparse.Namespace) -> PeftModel:
    r"""
    Initializes the adapters, support LoRA trained model.
    """
    if args.finetuning_type == "lora":
        model = setup_lora_tuning(model, args)
    else:
        raise NotImplementedError(f"Unknown fine-tuning type: {args.finetuning_type}.")

    return model


def setup_lora_tuning(
    model: "PreTrainedModel",
    args: argparse.Namespace,
) -> "PeftModel":
    adapter_to_resume = None

    if args.adapter_name_or_path is not None:
        is_mergeable = True

        if getattr(model, "quantization_method", None):  # merge lora in quantized model is unstable
            if len(args.adapter_name_or_path) != 1:
                raise RuntimeError("Quantized model only accepts a single adapter.")
            is_mergeable = False

        if not is_mergeable:
            adapter_to_merge = args.adapter_name_or_path[:-1]
            adapter_to_resume = args.adapter_name_or_path[-1]
        else:
            adapter_to_merge = args.adapter_name_or_path

        init_kwargs = {
            "subfolder": args.adapter_folder,
            "offload_folder": args.offload_folder,
            "cache_dir": args.cache_dir,
            "revision": args.model_revision,
            "token": args.hub_token,
        }

        for adapter in adapter_to_merge:
            model: "PeftModel" = PeftModel.from_pretrained(model, adapter, **init_kwargs)
            model = model.merge_and_unload()

        if len(adapter_to_merge) > 0:
            logger.info(f"Merged {len(adapter_to_merge)} adapter(s).")

        if adapter_to_resume is not None:  # resume lora training
            model = PeftModel.from_pretrained(model, adapter_to_resume, is_trainable=False, **init_kwargs)

        logger.info(f"Loaded adapter(s): {','.join(args.adapter_name_or_path)}")

    return model
