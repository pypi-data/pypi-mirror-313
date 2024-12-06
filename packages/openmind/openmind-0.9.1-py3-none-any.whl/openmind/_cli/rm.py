# Copyright (c) 2024 Huawei Technologies Co., Ltd.
#
# openMind is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#
#          http://license.coscl.org.cn/MulanPSL2
#
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
# EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
# MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.

import argparse
import textwrap
import shutil
from ..utils import replace_invalid_characters
from .subcommand import SubCommand
from .list import List


class Rm(SubCommand):
    """Holds all the logic for the `openmind-cli rm` subcommand."""

    def __init__(self, subparsers: argparse._SubParsersAction):
        super().__init__()
        self._parser = subparsers.add_parser(
            "rm",
            prog="openmind-cli rm",
            help="Remove the specified model from the given or default path.",
            description="Remove the specified model from the given or default path.",
            epilog=textwrap.dedent(
                """\
            examples:
                $ openmind-cli rm PyTorch-NPU/bluelm_7b_chat
                Deleted file path: /root/.cache/openmind/hub/models--PyTorch-NPU-bluelm_7b_chat
                File deleted successfully.
                
                $ openmind-cli rm PyTorch-NPU/convnextv2_tiny_1k_224 --local_dir /your/local/path/
                Deleted file path: /your/local/path/models--PyTorch-NPU--convnextv2_tiny_1k_224
                File deleted successfully.

                $ openmind-cli rm PyTorch-NPU/convnextv2_tiny_1k_224 --cache_dir /root/.cache/openmind/hub/
                Deleted file path: /root/.cache/openmind/hub/models--PyTorch-NPU--convnextv2_tiny_1k_224
                File deleted successfully.

                $ openmind-cli rm PyTorch-NPU/convnextv2_tiny_1k_224 --local_dir /your/local/path/ --cache_dir /root/.cache/opnemind/
                Deleted file path: /your/local/path/models--PyTorch-NPU--convnextv2_tiny_1k_224
                Deleted file path: /root/.cache/opnemind/models--PyTorch-NPU--convnextv2_tiny_1k_224
                Files deleted successfully.
            """
            ),
            formatter_class=argparse.RawTextHelpFormatter,
        )
        self._add_arguments()
        _parser = argparse.ArgumentParser()

        subparsers = _parser.add_subparsers(title="subcommands")
        self._list = List(subparsers)
        self._parser.set_defaults(func=self._rm_cmd)

    def _add_arguments(self) -> None:
        """Add arguments to the parser."""
        self._parser.add_argument(
            "--cache_dir",
            type=str,
            default=None,
            help="cache directory of downloaded models",
        )
        self._parser.add_argument(
            "--local_dir",
            type=str,
            default=None,
            help="local directory of downloaded models",
        )

    def _rm_cmd(self, args: argparse.Namespace) -> None:
        """Remove the specified model from the given or default path."""
        model_info = self._list._get_model_info(args)
        delete_num = 0
        for model in model_info:
            if args._dynamic_arg == model[0]:
                print(replace_invalid_characters(f"Deleted file path: {model[1]}"))
                shutil.rmtree(model[1])
                delete_num += 1
        if delete_num > 1:
            print("Files deleted successfully.")
        elif delete_num == 1:
            print("File deleted successfully.")
        else:
            err_msg = f"model `{args._dynamic_arg}` does not exist in the given or default path."
            raise ValueError(replace_invalid_characters(err_msg))
