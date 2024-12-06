# Copyright 2024 the LlamaFactory team.
# Copyright (c) 2024 Huawei Technologies Co., Ltd.
#
# This code is inspired by the LLaMA-Factory.
# https://github.com/hiyouga/LLaMA-Factory/blob/main/src/llamafactory/chat/hf_engine.py
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
import asyncio
import concurrent.futures
from threading import Thread
from typing import Any, AsyncGenerator, List, Dict, Callable

import torch
import transformers
from transformers.dynamic_module_utils import get_relative_imports
from transformers import (
    PreTrainedModel,
    PreTrainedTokenizer,
    TextIteratorStreamer,
    AutoTokenizer,
    AutoConfig,
    AutoModelForCausalLM,
    GenerationConfig,
)

from .model.adapter import init_adapter
from .model.patcher import patch_tokenizer, patch_config, patch_model
from .data.hparams import trans_hparams_to_dict
from .data.formatter import ToolFormatter, FunctionFormatter
from .data.template import Template, TEMPLATES, add_or_replace_eos_token, get_jinja_template
from .chat_utils import register_autoclass, count_parameters, get_logits_processor
from ...utils.hub import snapshot_download
from ...utils import logging, replace_invalid_characters

logger = logging.get_logger()
logging.set_verbosity_info()


class ChatEngine:
    def __init__(self, args: argparse.Namespace) -> None:
        self.tokenizer = _init_tokenizer(args)
        self.tokenizer.padding_side = "left"

        self.template = _init_template(self.tokenizer, args)
        self.model = _init_model(self.tokenizer, args)

        self.generating_args = trans_hparams_to_dict(args)

        try:
            asyncio.get_event_loop()
        except RuntimeError:
            logger.warning("No current event loop found, creating a new one.")
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        self.semaphore = asyncio.Semaphore(int(os.environ.get("OPENMIND_MAX_CONCURRENT", "1")))

    async def stream_chat(self, messages_context: List[Dict[str, str]]) -> AsyncGenerator[str, None]:
        loop = asyncio.get_running_loop()

        input_args = (
            self.model,
            self.tokenizer,
            self.template,
            self.generating_args,
            messages_context,
        )

        async with self.semaphore:
            with concurrent.futures.ThreadPoolExecutor() as pool:
                stream = self._stream_chat(*input_args)
                while True:
                    try:
                        yield await loop.run_in_executor(pool, stream)
                    except StopAsyncIteration:
                        break

    def _stream_chat(
        self,
        model: "PreTrainedModel",
        tokenizer: "PreTrainedTokenizer",
        template: "Template",
        generating_args: Dict[str, Any],
        messages_context: List[Dict[str, str]],
    ) -> Callable[[], str]:
        gen_kwargs = process_generation_args(model, tokenizer, template, generating_args, messages_context)
        streamer = TextIteratorStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)
        gen_kwargs["streamer"] = streamer

        thread = Thread(target=model.generate, kwargs=gen_kwargs, daemon=True)
        thread.start()

        def stream():
            try:
                return streamer.__next__()
            except StopIteration:
                raise StopAsyncIteration()

        return stream


def get_init_kwargs(args: argparse.Namespace) -> Dict[str, Any]:
    if os.environ.get("FORCE_CHECK_IMPORTS", "0").lower() not in ["true", "1"]:
        transformers.dynamic_module_utils.check_imports = get_relative_imports

    if not os.path.exists(args.model_name_or_path):
        revision = "main" if args.model_revision == "main" else args.model_revision
        args.model_name_or_path = snapshot_download(
            args.model_name_or_path, revision=revision, cache_dir=args.cache_dir
        )

    return {
        "trust_remote_code": True,
        "cache_dir": args.cache_dir,
        "revision": args.model_revision,
        "token": args.hub_token,
    }


def _init_tokenizer(args: argparse.Namespace) -> "PreTrainedTokenizer":
    init_kwargs = get_init_kwargs(args)

    try:
        tokenizer = AutoTokenizer.from_pretrained(
            args.model_name_or_path,
            use_fast=args.use_fast_tokenizer,
            split_special_tokens=args.split_special_tokens,
            padding_side="right",
            **init_kwargs,
        )
    except ValueError:
        tokenizer = AutoTokenizer.from_pretrained(
            args.model_name_or_path,
            use_fast=True,
            padding_side="right",
            **init_kwargs,
        )

    if args.new_special_tokens is not None:
        num_added_tokens = tokenizer.add_special_tokens(
            dict(additional_special_tokens=args.new_special_tokens),
            replace_additional_special_tokens=False,
        )

        logger.info(f"Add {','.join(args.new_special_tokens)} to special tokens.")

        if num_added_tokens > 0 and not args.resize_vocab:
            args.resize_vocab = True
            logger.warning("New tokens have been added, set `resize_vocab` to True by force.")

    patch_tokenizer(tokenizer)

    return tokenizer


def _init_template(tokenizer, args: argparse.Namespace) -> "Template":
    template = TEMPLATES.get(args.template, None)

    if template is None:
        err_msg = f"Template `{args.template}` has not been registered yet."
        raise RuntimeError(replace_invalid_characters(err_msg))

    tool_format = args.tool_format

    if tool_format is not None:
        logger.info(f"Using tool format: {tool_format}")
        eos_slots = [] if template.efficient_eos else [{"eos_token"}]
        template.format_tools = ToolFormatter(tool_format=tool_format)
        template.format_function = FunctionFormatter(slots=eos_slots, tool_format=tool_format)

    stop_words = template.stop_words
    if template.replace_eos:
        if not stop_words:
            raise ValueError("Stop words are required to replace the EOS token.")

        add_or_replace_eos_token(tokenizer, eos_token=stop_words[0])
        stop_words = stop_words[1:]

    if tokenizer.eos_token_id is None:
        add_or_replace_eos_token(tokenizer, eos_token="<|endoftext|>")

    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token
        logger.info(f"Add pad token: {tokenizer.pad_token}")

    if stop_words:
        num_added_tokens = tokenizer.add_special_tokens(
            dict(additional_special_tokens=stop_words), replace_additional_special_tokens=False
        )
        logger.info(f"Add {','.join(stop_words)} to stop words.")

        if num_added_tokens > 0:
            logger.warning("New tokens have been added, make sure `resize_vocab` is True.")

    if template.replace_jinja_template:
        try:
            tokenizer.chat_template = get_jinja_template(template, tokenizer)
        except ValueError:
            logger.info("Cannot add this chat template to tokenizer.")

    return template


def _init_model(tokenizer, args: argparse.Namespace) -> "PreTrainedModel":
    init_kwargs = get_init_kwargs(args)

    config = AutoConfig.from_pretrained(args.model_name_or_path, **init_kwargs)
    patch_config(config, args, init_kwargs)

    init_kwargs["config"] = config
    init_kwargs["pretrained_model_name_or_path"] = args.model_name_or_path

    model = AutoModelForCausalLM.from_pretrained(**init_kwargs)
    patch_model(model, tokenizer, args)
    register_autoclass(config, model, tokenizer)

    init_adapter(model, args)

    model.requires_grad_(False)

    for param in model.parameters():
        if param.data.dtype == torch.float32 and args.compute_dtype != torch.float32:
            param.data = param.data.to(args.compute_dtype)

    model.eval()

    _, all_param = count_parameters(model)
    logger.info(f"all params: {all_param}")

    if args.print_param_status:
        for name, param in model.named_parameters():
            logger.info(f"name: {name}, dtype: {param.dtype}, device: {param.device}, trainable: {param.requires_grad}")

    return model


def process_generation_args(
    model: "PreTrainedModel",
    tokenizer: "PreTrainedTokenizer",
    template: "Template",
    generating_args: Dict[str, Any],
    messages_context: List[Dict[str, str]],
) -> Dict[str, Any]:
    paired_messages_context = messages_context + [{"role": "assistant", "content": ""}]

    prompt_ids, _ = template.encode(tokenizer, paired_messages_context)

    inputs = torch.tensor([prompt_ids], device=model.device)
    attention_mask = torch.ones_like(inputs, dtype=torch.bool)

    generating_args = generating_args.copy()
    generating_args.update(
        dict(
            num_return_sequences=1,
            eos_token_id=[tokenizer.eos_token_id] + tokenizer.additional_special_tokens_ids,
            pad_token_id=tokenizer.pad_token_id,
        )
    )

    if not generating_args["temperature"]:
        generating_args["do_sample"] = False

    if not generating_args["do_sample"]:
        generating_args.pop("temperature", None)
        generating_args.pop("top_p", None)

    gen_kwargs = dict(
        inputs=inputs,
        attention_mask=attention_mask,
        generation_config=GenerationConfig(**generating_args),
        logits_processor=get_logits_processor(),
    )

    return gen_kwargs
