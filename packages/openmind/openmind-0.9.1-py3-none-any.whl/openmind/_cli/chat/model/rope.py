# Copyright 2024 the LlamaFactory team.
# Copyright (c) 2024 Huawei Technologies Co., Ltd.
#
# This code is inspired by the LLaMA-Factory.
# https://github.com/hiyouga/LLaMA-Factory/blob/main/src/llamafactory/model/model_utils/rope.py
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

from transformers import PretrainedConfig

from ....utils import logging

logger = logging.get_logger()
logging.set_verbosity_info()


def configure_rope(config: "PretrainedConfig", args: argparse.Namespace) -> None:
    if args.rope_scaling is None:
        return

    if not hasattr(config, "rope_scaling"):
        logger.warning("Current model does not support RoPE scaling.")
        return

    scaling_factor = 2.0

    setattr(config, "rope_scaling", {"type": args.rope_scaling, "factor": scaling_factor})
    logger.info(f"Using {args.rope_scaling} scaling strategy and setting scaling factor to {scaling_factor}")
