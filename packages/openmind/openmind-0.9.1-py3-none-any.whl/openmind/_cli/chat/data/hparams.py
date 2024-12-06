# Copyright 2024 the LlamaFactory team.
# Copyright (c) 2024 Huawei Technologies Co., Ltd.
#
# This code is inspired by the LLaMA-Factory.
# https://github.com/hiyouga/LLaMA-Factory/blob/main/src/llamafactory/hparams/model_args.py
# https://github.com/hiyouga/LLaMA-Factory/blob/main/src/llamafactory/hparams/generating_args.py
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
from typing import Dict, Any

from ..chat_utils import str2bool


def add_interactive_arguments(_parser):
    _parser.add_argument(
        "--template",
        type=str,
        default=None,
        help="Model template name for multi-turn conversation.",
    )
    _parser.add_argument(
        "--tool_format",
        type=str,
        default=None,
        help="Tool format used for constructing function calling.",
    )
    _parser.add_argument(
        "--framework",
        type=str,
        default=None,
        choices=["pt"],
        help="AI framework used for multi-turn conversation.",
    )
    _parser.add_argument(
        "--yaml_path",
        type=str,
        default=None,
        help="Local path for loading yaml configuration file.",
    )
    _parser.add_argument(
        "--docker",
        type=str,
        default=None,
        help="Whether to use docker or not.",
    )


def add_model_arguments(_parser):
    _parser.add_argument(
        "--model_revision",
        type=str,
        default="main",
        help="The specific model version to use (can be a branch name, tag name or commit id).",
    )
    _parser.add_argument(
        "--adapter_name_or_path",
        type=str,
        default=None,
        help="Path to the adapter weight or repo id  from openMind. " "Use commas to separate multiple adapters.",
    )
    _parser.add_argument(
        "--finetuning_type",
        type=str,
        default="lora",
        choices=["lora"],
        help="Fine-tuning method to use.",
    )
    _parser.add_argument(
        "--adapter_folder",
        type=str,
        default=None,
        help="The folder containing the adapter weights to load.",
    )
    _parser.add_argument(
        "--cache_dir",
        type=str,
        default=None,
        help="Where to store the pre-trained models downloaded from openMind.",
    )
    _parser.add_argument(
        "--use_fast_tokenizer",
        type=str2bool,
        default=True,
        help="Whether or not to use one of the fast tokenizer (backed by the tokenizers library).",
    )
    _parser.add_argument(
        "--resize_vocab",
        type=str2bool,
        default=False,
        help="Whether or not to resize the tokenizer vocab and the embedding layers.",
    )
    _parser.add_argument(
        "--split_special_tokens",
        type=str2bool,
        default=False,
        help="Whether or not the special tokens should be split during the tokenization process.",
    )
    _parser.add_argument(
        "--new_special_tokens",
        type=str,
        default=None,
        help="Special tokens to be added into the tokenizer. Use commas to separate multiple tokens.",
    )
    _parser.add_argument(
        "--low_cpu_mem_usage",
        type=str2bool,
        default=True,
        help="Whether or not to use memory-efficient model loading.",
    )
    _parser.add_argument(
        "--rope_scaling",
        type=str,
        default=None,
        choices=["linear", "dynamic"],
        help="Which scaling strategy should be adopted for the RoPE embeddings.",
    )
    _parser.add_argument(
        "--flash_attn",
        type=str,
        default="auto",
        choices=["auto", "disabled"],
        help="Enable FlashAttention for faster inference.",
    )
    _parser.add_argument(
        "--offload_folder",
        type=str,
        default="offload",
        help="Path to offload model weights.",
    )
    _parser.add_argument(
        "--use_cache",
        type=str2bool,
        default=True,
        help="Whether or not to use KV cache in generation.",
    )
    _parser.add_argument(
        "--infer_dtype",
        type=str,
        default="auto",
        choices=["auto", "float16", "bfloat16", "float32"],
        help="Data type for model weights and activations at inference.",
    )
    _parser.add_argument(
        "--hub_token",
        type=str,
        default=None,
        help="The hub token for accessing private model files.",
    )
    _parser.add_argument(
        "--print_param_status",
        type=str2bool,
        default=False,
        help="For debugging purposes, print the status of the parameters in the model.",
    )
    _parser.add_argument(
        "--device",
        type=str,
        default="npu:0",
        choices=["cpu", "npu:0", "npu:1", "npu:2", "npu:3", "npu:4", "npu:5", "npu:6", "npu:7"],
        help="Device used for chat, default is `npu:0`.",
    )


def add_generating_arguments(_parser):
    _parser.add_argument(
        "--do_sample",
        type=str2bool,
        default=True,
        help="Whether or not to use sampling, use greedy decoding otherwise.",
    )
    _parser.add_argument(
        "--temperature",
        type=float,
        default=0.95,
        help="The value used to modulate the next token probabilities.",
    )
    _parser.add_argument(
        "--top_p",
        type=float,
        default=0.7,
        help="The smallest set of most probable tokens with probabilities that add up to top_p or higher are kept.",
    )
    _parser.add_argument(
        "--top_k",
        type=int,
        default=50,
        help="The number of highest probability vocabulary tokens to keep for top-k filtering.",
    )
    _parser.add_argument(
        "--num_beams",
        type=int,
        default=1,
        help="Number of beams for beam search. 1 means no beam search.",
    )
    _parser.add_argument(
        "--max_length",
        type=int,
        default=1024,
        help="The maximum length the generated tokens can have. It can be overridden by max_new_tokens.",
    )
    _parser.add_argument(
        "--max_new_tokens",
        type=int,
        default=1024,
        help="The maximum numbers of tokens to generate, ignoring the number of tokens in the prompt.",
    )
    _parser.add_argument(
        "--repetition_penalty",
        type=float,
        default=1.0,
        help="The parameter for repetition penalty. 1.0 means no penalty.",
    )
    _parser.add_argument(
        "--length_penalty",
        type=float,
        default=1.0,
        help="Exponential penalty to the length that is used with beam-based generation.",
    )
    _parser.add_argument(
        "--default_system",
        type=str,
        default=None,
        help="Default system message to use in chat completion.",
    )


def postprocess_hparams(args: argparse.Namespace) -> argparse.Namespace:
    args_dict = vars(args)

    cast_hparams_type(args_dict)

    if args_dict.get("split_special_tokens") and args_dict.get("use_fast_tokenizer"):
        raise ValueError("Param `split_special_tokens` is only supported for slow tokenizers.")

    if args_dict.get("adapter_name_or_path") is not None:  # support merging multiple lora weights
        args_dict["adapter_name_or_path"] = [path.strip() for path in args_dict.get("adapter_name_or_path").split(",")]

    if args_dict.get("new_special_tokens") is not None:  # support multiple special tokens
        args_dict["new_special_tokens"] = [token.strip() for token in args_dict.get("new_special_tokens").split(",")]

    args_dict["compute_dtype"] = None

    return argparse.Namespace(**args_dict)


def trans_hparams_to_dict(args: argparse.Namespace) -> Dict[str, Any]:
    args_dict = vars(args)

    if args_dict.get("max_new_tokens", -1) > 0:
        args_dict.pop("max_length", None)
    else:
        args_dict.pop("max_new_tokens", None)

    return args_dict


def cast_hparams_type(args_dict):
    # cast hparams' type by force when specified from CLI
    if "use_fast_tokenizer" in args_dict and isinstance(args_dict["use_fast_tokenizer"], str):
        args_dict["use_fast_tokenizer"] = str2bool(args_dict["use_fast_tokenizer"])
    if "resize_vocab" in args_dict and isinstance(args_dict["resize_vocab"], str):
        args_dict["resize_vocab"] = str2bool(args_dict["resize_vocab"])
    if "split_special_tokens" in args_dict and isinstance(args_dict["split_special_tokens"], str):
        args_dict["split_special_tokens"] = str2bool(args_dict["split_special_tokens"])
    if "low_cpu_mem_usage" in args_dict and isinstance(args_dict["low_cpu_mem_usage"], str):
        args_dict["low_cpu_mem_usage"] = str2bool(args_dict["low_cpu_mem_usage"])
    if "use_cache" in args_dict and isinstance(args_dict["use_cache"], str):
        args_dict["use_cache"] = str2bool(args_dict["use_cache"])
    if "print_param_status" in args_dict and isinstance(args_dict["print_param_status"], str):
        args_dict["print_param_status"] = str2bool(args_dict["print_param_status"])
    if "do_sample" in args_dict and isinstance(args_dict["do_sample"], str):
        args_dict["do_sample"] = str2bool(args_dict["do_sample"])
    if "temperature" in args_dict and isinstance(args_dict["temperature"], str):
        args_dict["temperature"] = float(args_dict["temperature"])
    if "top_p" in args_dict and isinstance(args_dict["top_p"], str):
        args_dict["top_p"] = float(args_dict["top_p"])
    if "top_k" in args_dict and isinstance(args_dict["top_k"], str):
        args_dict["top_k"] = int(args_dict["top_k"])
    if "num_beams" in args_dict and isinstance(args_dict["num_beams"], str):
        args_dict["num_beams"] = int(args_dict["num_beams"])
    if "max_length" in args_dict and isinstance(args_dict["max_length"], str):
        args_dict["max_length"] = int(args_dict["max_length"])
    if "max_new_tokens" in args_dict and isinstance(args_dict["max_new_tokens"], str):
        args_dict["max_new_tokens"] = int(args_dict["max_new_tokens"])
    if "repetition_penalty" in args_dict and isinstance(args_dict["repetition_penalty"], str):
        args_dict["repetition_penalty"] = float(args_dict["repetition_penalty"])
    if "length_penalty" in args_dict and isinstance(args_dict["length_penalty"], str):
        args_dict["length_penalty"] = float(args_dict["length_penalty"])
