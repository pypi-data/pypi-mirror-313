# Copyright 2024 the LlamaFactory team.
# Copyright (c) 2024 Huawei Technologies Co., Ltd.
#
# This code is inspired by the LLaMA-Factory.
# https://github.com/hiyouga/LLaMA-Factory/blob/main/src/llamafactory/chat/chat_model.py
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


import gc
import copy
import argparse
import textwrap

from .chat_model import ChatModel
from ..subcommand import SubCommand
from ..cli_utils import safe_load_yaml
from ..cli_docker import CLIDocker
from ...utils.hub import OPENMIND_CACHE
from ...utils.constants import DYNAMIC_ARG, SPECIFIED_ARGS, CHAT_MODEL_TEMPLATE_MAPPINGS
from ...utils import get_framework, is_torch_available, replace_invalid_characters, logging
from .data.hparams import add_interactive_arguments, add_model_arguments, add_generating_arguments, postprocess_hparams

logger = logging.get_logger(allow_line_separator=True)
logging.set_verbosity_info()


class Chat(SubCommand):
    def __init__(self, subparsers: argparse._SubParsersAction):
        super().__init__()
        self._parser = subparsers.add_parser(
            "chat",
            prog="openmind-cli chat",
            help="Start a multi-turn conversation.",
            description="Start a multi-turn conversation.",
            formatter_class=argparse.RawTextHelpFormatter,
            epilog=textwrap.dedent(
                """\
                examples:
                    $ openmind-cli chat Baichuan/Baichuan2_7b_chat_pt
                    $ [User]>>> 你好
                    $ [Model]>>> 你好！很高兴为您提供帮助。请问有什么问题我可以帮您解答？
                """
            ),
        )
        self._add_arguments()
        self._parser.set_defaults(func=self._start_chat)

    def _add_arguments(self):
        add_interactive_arguments(self._parser)
        add_model_arguments(self._parser)
        add_generating_arguments(self._parser)

    def _prepare_arguments(self, args: argparse.Namespace) -> argparse.Namespace:
        args_dict = vars(copy.deepcopy(args))
        args_dict.pop("func")

        if args_dict.get(DYNAMIC_ARG) is None:
            raise ValueError("Task name or model repo id is required for `openmind-cli chat` CLI entrypoint.")

        if args_dict.get("yaml_path") is not None:
            yaml_content_dict = safe_load_yaml(args_dict.pop("yaml_path"))
            args_dict.update(yaml_content_dict)

        args_dict.update(args_dict.pop(SPECIFIED_ARGS))
        args_dict.pop("yaml_path", None)

        return argparse.Namespace(**args_dict)

    def _check_arguments(self, args: argparse.Namespace) -> argparse.Namespace:
        args_dict = vars(args)

        model_name_or_path = args_dict.pop(DYNAMIC_ARG)
        args_dict.update({"model_name_or_path": model_name_or_path})

        if args_dict.get("template") is None:
            try:
                default_template = CHAT_MODEL_TEMPLATE_MAPPINGS[model_name_or_path]
                logger.info(f"Param `--template` is not specified, use default template `{default_template}`")
            except KeyError as e:
                err_msg = (
                    f"Can not find default template for model `{model_name_or_path}`, "
                    f"check whether it is not in supported list, or it is a repo model name."
                )
                raise RuntimeError(replace_invalid_characters(err_msg)) from e

            args_dict.update({"template": default_template})

        if args_dict.get("framework") is None:
            args_dict.update({"framework": get_framework()})

        if args_dict.get("cache_dir") is None:
            args_dict.update({"cache_dir": OPENMIND_CACHE})

        if args_dict.get("adapter_name_or_path") is not None and args_dict.get("finetuning_type") != "lora":
            raise ValueError("Adapter is only valid for the LoRA method.")

        return argparse.Namespace(**args_dict)

    def _start_chat_without_docker(self, args: argparse.Namespace) -> None:
        parsed_args = self._check_arguments(args)

        chat_model = ChatModel(parsed_args)

        message_context = []
        logger.info("Welcome to use openMind chat, use `clear` to remove chat history, use `exit` to stop the chat.")

        while True:
            try:
                user_query = input("\n[USER]>>>")
            except UnicodeDecodeError:
                logger.info(
                    "Decoding error occurred when processing user input content, please set terminal coding" "to utf-8."
                )
                continue
            except Exception as ex:
                err_msg = f"Exception occurred when processing user input content, detail error message: {str(ex)}"
                raise RuntimeError(replace_invalid_characters(err_msg))

            if user_query.strip() == "":
                logger.info("No valid input detected, please confirm your input.")
                continue

            if user_query.strip() == "exit":
                break

            if user_query.strip() == "clear":
                message_context.clear()
                gc.collect()
                if is_torch_available():
                    import torch

                    torch.npu.empty_cache()
                logger.info("Chat history has been cleared.")
                continue

            message_context.append({"role": "user", "content": user_query})

            print("[MODEL]>>>", end="", flush=True)

            model_response = ""
            for rsp in chat_model.stream_chat(message_context):
                print(rsp, end="", flush=True)
                model_response += rsp
            print()
            message_context.append({"role": "assistant", "content": model_response})

    def _start_chat(self, args: argparse.Namespace) -> None:
        parsed_args = postprocess_hparams(self._prepare_arguments(args))
        if parsed_args.docker is not None:
            params = vars(parsed_args)
            CLIDocker.start_docker(args, params)
        else:
            del parsed_args.docker
            self._start_chat_without_docker(parsed_args)
