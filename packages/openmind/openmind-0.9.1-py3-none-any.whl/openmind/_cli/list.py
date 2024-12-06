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

import os
import argparse
import math
import textwrap
from pathlib import Path
from tabulate import tabulate

from ..utils.hub import OM_HUB_CACHE
from .subcommand import SubCommand
from ..utils.constants import (
    GB,
    GIT,
    GIT_LOGS_HEAD,
    OPENMIND_PREFIX,
    SNAPSHOTS,
    MODEL_CONFIG,
)


class List(SubCommand):
    """Holds all the logic for the `openmind-cli list` subcommand."""

    def __init__(self, subparsers: argparse._SubParsersAction):
        super().__init__()
        self._parser = subparsers.add_parser(
            "list",
            prog="openmind-cli list",
            help="List all models downloaded to the local",
            description="List all models downloaded to the local",
            epilog=textwrap.dedent(
                """\
            examples:
                $ openmind-cli list
                Model Nmae                      Model Path                                                              Model Size(GB)
                PyTorch-NPU/bluelm_7b_chat      /root/.cache/openmind/hub/models--PyTorch-NPU-bluelm_7b_chat            27.2       
                
                $ openmind-cli list --local_dir ./
                Model Name                          Model Path                                                     Model Size(GB)
                PyTorch-NPU/convnextv2_tiny_1k_224  /home/demo/models--PyTorch-NPU--convnextv2_tiny_1k_224         0.6

                $ openmind-cli list --cache_dir ./
                Model Name                          Model Path                                                     Model Size(GB)
                PyTorch-NPU/convnextv2_tiny_1k_224  /home/demo/models--PyTorch-NPU--convnextv2_tiny_1k_224         0.6
            """
            ),
            formatter_class=argparse.RawTextHelpFormatter,
        )
        self._add_arguments()
        self._parser.set_defaults(func=self._list_cmd)

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

    def _get_folder_size(self, folder_path):
        total_size = 0

        for root, _, files in os.walk(folder_path):
            for file in files:
                fp = os.path.join(root, file)
                # size of the soft link file is not calculated
                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)

        return math.ceil(total_size / GB * 10) / 10

    def _get_local_folder_size(self, folder_path):
        total_size = 0

        for root, _, files in os.walk(folder_path):
            for file in files:
                fp = os.path.join(root, file)
                total_size += os.path.getsize(fp)

        return math.ceil(total_size / GB * 10) / 10

    def _check_file_exists(self, directory, filename):
        for root, _, files in os.walk(directory):
            target_file = os.path.join(root, filename)
            # Check whether the target file is a soft link
            if os.path.islink(target_file):
                target_path = os.readlink(target_file)
                absolute_target_path = os.path.realpath(os.path.join(os.path.dirname(target_file), target_path))
                if os.path.exists(absolute_target_path):
                    return True
            elif filename in files:
                return True

        return False

    def _check_git_om_model(self, model_path):
        model_name = ""
        model_size = 0

        git_head_path = os.path.join(model_path, GIT_LOGS_HEAD)
        if os.path.exists(git_head_path):
            with open(git_head_path, "r") as f:
                git_log_info = f.read().split()[-1]
            if OPENMIND_PREFIX in git_log_info:
                model_name = git_log_info.split(OPENMIND_PREFIX)[1].split(GIT)[0]
                model_size = self._get_folder_size(model_path)

        return model_name, model_size

    def _check_cache_om_model(self, model_path):
        model_name = ""
        model_size = 0
        git_head_path = os.path.join(model_path, GIT_LOGS_HEAD)

        if os.path.isdir(model_path):
            for file in os.listdir(model_path):
                if file == SNAPSHOTS:
                    model_cache_path = os.path.join(model_path, file)
                    if self._check_file_exists(model_cache_path, MODEL_CONFIG):
                        model_name = "/".join(model_path.split("/")[-1].split("--")[1:])
                        model_size = self._get_folder_size(model_path)
                        return model_name, model_size

                elif file == MODEL_CONFIG and not os.path.exists(git_head_path):
                    model_name = model_path.split("/")[-1]
                    model_size = self._get_local_folder_size(model_path)
                    return model_name, model_size

        return model_name, model_size

    def _add_model_info(self, base_path, model_info):
        for file in os.listdir(base_path):
            model_path = os.path.join(base_path, file)
            git_model_name, git_model_size = self._check_git_om_model(model_path)
            if git_model_name and git_model_size:
                model_info.add((git_model_name, model_path, git_model_size))

            cache_model_name, cache_model_size = self._check_cache_om_model(model_path)
            if cache_model_name and cache_model_size:
                model_info.add((cache_model_name, model_path, cache_model_size))

    def _get_model_info(self, args: argparse.Namespace) -> set:
        model_info = set()

        if args.local_dir:
            local_path = Path(args.local_dir).absolute()
            self._add_model_info(local_path, model_info)

        if args.cache_dir:
            cache_path = Path(args.cache_dir).absolute()
            self._add_model_info(cache_path, model_info)

        if not args.local_dir and not args.cache_dir:
            self._add_model_info(OM_HUB_CACHE, model_info)

        return model_info

    def _list_cmd(self, args: argparse.Namespace) -> None:
        """List all models downloaded to the local."""
        model_info = self._get_model_info(args)
        headers = ["Model Name", "Model Path", "Model Size(GB)"]
        table = tabulate(sorted(model_info), headers=headers, tablefmt="plain", numalign="left")
        print(table)
