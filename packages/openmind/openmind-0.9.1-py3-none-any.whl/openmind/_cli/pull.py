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

from .subcommand import SubCommand
from ..utils.constants import DYNAMIC_ARG, SPECIFIED_ARGS
from ..utils.hub import OpenMindHub
from .cli_utils import safe_load_yaml, try_to_trans_to_bool, try_to_trans_to_list
from ..utils.logging import get_logger, set_verbosity_info

logger = get_logger()

set_verbosity_info()


class Pull(SubCommand):
    """Holds all the logic for the `openmind-cli pull` subcommand."""

    def __init__(self, subparsers: argparse._SubParsersAction):
        super().__init__()
        self._parser = subparsers.add_parser(
            "pull",
            prog="openmind-cli pull repo_id",
            help="Pull models or datasets or spaces from openMind",
            description="Pull models or datasets or spaces from openMind",
            epilog=textwrap.dedent(
                """\
            examples:
                $ openmind-cli pull PyTorch-NPU/bert_base_cased
                Pull PyTorch-NPU/bert_base_cased finished
                
                $ openmind-cli pull PyTorch-NPU/bert_base_cased --yaml_path ./config.yaml
                Pull PyTorch-NPU/bert_base_cased finished

                $ openmind-cli pull PyTorch-NPU/bert_base_cased --cache_dir ~/.cache2/openmind/hub --yaml_path ./config.yaml
                Pull PyTorch-NPU/bert_base_cased finished
            """
            ),
            formatter_class=argparse.RawTextHelpFormatter,
        )
        self._add_arguments()
        self._parser.set_defaults(func=self._pull_cmd)

    def _add_arguments(self) -> None:
        """Add arguments to the parser."""
        self._parser.add_argument(
            "--repo_type",
            type=str,
            default="model",
            help="choose from model/dataset/space",
        )
        self._parser.add_argument(
            "--revision",
            type=str,
            default=None,
            help="branch name",
        )
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
        self._parser.add_argument(
            "--local_dir_use_symlinks",
            type=str,
            default="auto",
            help="used with local_dir, whether to create .symlink files",
        )
        self._parser.add_argument(
            "--resume_download",
            type=str,
            default=True,
            help="resume previously interrupted downloads",
        )
        self._parser.add_argument(
            "--force_download",
            type=str,
            default=False,
            help="whether to force to download files",
        )
        self._parser.add_argument(
            "--token",
            type=str,
            default=None,
            help="token with readable access to the private hub",
        )
        self._parser.add_argument(
            "--local_files_only",
            type=str,
            default=False,
            help="only check whether local files have been downloaded",
        )
        self._parser.add_argument(
            "--allow_patterns",
            type=str,
            default=None,
            help="only certain types of files are allowed to be downloaded, like *.py,*.bin",
        )
        self._parser.add_argument(
            "--ignore_patterns",
            type=str,
            default=None,
            help="ignore the download of certain types of files",
        )
        self._parser.add_argument(
            "--max_workers",
            type=int,
            default=8,
            help="number of concurrent download threads",
        )
        self._parser.add_argument(
            "--yaml_path",
            type=str,
            default=None,
            help="path of yaml",
        )

    def _download_model(self, repo_id, args):
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

        # convert str to the corresponding type
        config_data["max_workers"] = int(config_data["max_workers"])
        config_data["local_dir_use_symlinks"] = try_to_trans_to_bool(config_data["local_dir_use_symlinks"])
        config_data["resume_download"] = try_to_trans_to_bool(config_data["resume_download"])
        config_data["force_download"] = try_to_trans_to_bool(config_data["force_download"])
        config_data["local_files_only"] = try_to_trans_to_bool(config_data["local_files_only"])
        config_data["allow_patterns"] = try_to_trans_to_list(config_data["allow_patterns"])
        config_data["ignore_patterns"] = try_to_trans_to_list(config_data["ignore_patterns"])

        download_folder = OpenMindHub.snapshot_download(**config_data)

        return download_folder

    def _pull_cmd(self, args: argparse.Namespace) -> None:
        """Pull models or datasets or spaces from openMind"""
        repo_id = vars(args).pop(DYNAMIC_ARG)
        download_folder = self._download_model(repo_id, args)
        msg = f"Pull {repo_id} finished, saved in {download_folder}"
        logger.info(msg)
