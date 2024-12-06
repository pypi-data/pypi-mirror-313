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
from typing import List

from .subcommand import SubCommand
from ..utils.constants import DYNAMIC_ARG, SPECIFIED_ARGS
from ..utils.hub import OpenMindHub
from .cli_utils import safe_load_yaml, try_to_trans_to_list
from ..utils.logging import get_logger, set_verbosity_info
from ..utils import replace_invalid_characters

logger = get_logger()

set_verbosity_info()


class Push(SubCommand):
    """Holds all the logic for the `openmind-cli push` subcommand."""

    def __init__(self, subparsers: argparse._SubParsersAction):
        super().__init__()
        self._parser = subparsers.add_parser(
            "push",
            prog="openmind-cli push repo_id",
            help="Push models or datasets or spaces to openMind",
            description="Push models or datasets or spaces to openMind",
            epilog=textwrap.dedent(
                """\
            examples:
                $ openmind-cli push your_organization/your_repo --token xxx
                Push to your_organization/your_repo finished
                
                $ openmind-cli push your_organization/your_repo --yaml_path ./config.yaml
                Push to your_organization/your_repo finished

                $ openmind-cli push your_organization/your_repo --folder_path ~/.cache2/openmind/hub --yaml_path ./config.yaml
                Push to your_organization/your_repo finished
            """
            ),
            formatter_class=argparse.RawTextHelpFormatter,
        )
        self._add_arguments()
        self._parser.set_defaults(func=self._push_cmd)

    def _add_arguments(self) -> None:
        self._parser.add_argument(
            "--folder_path",
            type=str,
            default="./",
            help="path to be uploaded, not include the folder itself",
        )
        self._parser.add_argument(
            "--path_in_repo",
            type=str,
            default=None,
            help="path to be uploaded to the hub",
        )
        self._parser.add_argument(
            "--commit_message",
            type=str,
            default="Upload folder using openMind hub",
            help="the submission message of this commit",
        )
        self._parser.add_argument(
            "--commit_description",
            type=str,
            default=None,
            help="the description of this commit",
        )
        self._parser.add_argument(
            "--token",
            type=str,
            default=None,
            help="token with writable access to the target hub",
        )
        self._parser.add_argument(
            "--revision",
            type=str,
            default="main",
            help="upload to the specified branch of the hub",
        )
        self._parser.add_argument(
            "--allow_patterns",
            type=str or List[str],
            default=None,
            help="only certain types of files are allowed to be downloaded, like *.py,*.bin",
        )
        self._parser.add_argument(
            "--ignore_patterns",
            type=str or List[str],
            default=None,
            help="ignore the download of certain types of files",
        )
        self._parser.add_argument(
            "--num_threads",
            type=int,
            default=5,
            help="number of concurrent upload threads",
        )
        self._parser.add_argument(
            "--yaml_path",
            type=str,
            default=None,
            help="path of yaml",
        )

    def _upload_model(self, repo_id, args):
        if args.yaml_path:
            config_data = safe_load_yaml(args.yaml_path)
        else:
            config_data = dict()
        config_data["repo_id"] = repo_id
        vars(args).pop("func")
        vars(args).pop("yaml_path")

        specified_args = vars(args).pop(SPECIFIED_ARGS)

        for key, value in vars(args).items():
            if key not in config_data:
                config_data[key] = value
            # specified args has a higher priority than yaml
            elif key in config_data and key in specified_args:
                config_data[key] = specified_args[key]

        if not config_data["token"]:
            err_msg = "Please specify your token"
            raise ValueError(replace_invalid_characters(err_msg))

        # convert str to the corresponding type
        config_data["num_threads"] = int(config_data["num_threads"])
        config_data["allow_patterns"] = try_to_trans_to_list(config_data["allow_patterns"])
        config_data["ignore_patterns"] = try_to_trans_to_list(config_data["ignore_patterns"])

        OpenMindHub.upload_folder(**config_data)

    def _push_cmd(self, args: argparse.Namespace) -> None:
        """Push models or datasets or spaces to openMind"""
        repo_id = vars(args).pop(DYNAMIC_ARG)
        self._upload_model(repo_id, args)
        msg = f"Push to {repo_id} finished"
        logger.info(msg)
