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
import platform
import importlib
import importlib.metadata

from .. import __version__ as version
from .. import (
    is_ms_available,
    is_torch_available,
    is_torch_npu_available,
)
from .subcommand import SubCommand


class Env(SubCommand):
    """Holds all the logic for the `openmind-cli env` subcommand."""

    def __init__(self, subparsers: argparse._SubParsersAction):
        super().__init__()
        self._parser = subparsers.add_parser(
            "env",
            prog="openmind-cli env",
            help="Get current environment information.",
            description="Get current environment information.",
            epilog=textwrap.dedent(
                """\
            examples:
                $ openmind-cli env
                - `openmind` version: 0.9.1
                - `openmind_hub` version: 0.9.0
                - Platform: Linux-4.19.90-vhulk2111.1.0.h963.eulerosv2r10.aarch64-aarch64-with-glibc2.34
                - Python version: 3.10.13
                - PyTorch version (NPU?): 2.1.0 (2.1.0.post8)
                - MindSpore version: not installed
                - MindFormers version: not installed
                - Transformers version: 4.43.3
                - Accelerate version: 0.30.1
                - Datasets version: 2.20.0
                - Evaluate version: 0.4.2
                - DeepSpeed version: not installed
                - Lm-evaluation-harness version: 0.4.3
            """
            ),
            formatter_class=argparse.RawTextHelpFormatter,
        )
        self._add_arguments()
        self._parser.set_defaults(func=self._env_cmd)

    @staticmethod
    def _grab_package_version(pkg_name: str) -> str:
        try:
            return importlib.metadata.version(pkg_name)
        except importlib.metadata.PackageNotFoundError:
            return "not installed"

    @staticmethod
    def _format_dict(d):
        return "\n".join([f"- {prop}: {val}" for prop, val in d.items()]) + "\n"

    def _env_cmd(self, args: argparse.Namespace) -> None:
        """Get current environment information."""

        pt_version = "not installed"
        pt_npu_version = "not installed"
        pt_npu_available = False
        if is_torch_available():
            import torch

            pt_version = torch.__version__
            pt_npu_available = is_torch_npu_available()
            if pt_npu_available:
                import torch_npu

                pt_npu_version = torch_npu.__version__
        ms_version = "not installed"
        if is_ms_available():
            import mindspore

            ms_version = mindspore.__version__
        try:
            import openmind_hub

            om_hub_version = openmind_hub.__version__
        except Exception:
            om_hub_version = "not installed"
        info = {
            "`openmind` version": version,
            "`openmind_hub` version": om_hub_version,
            "Platform": platform.platform(),
            "Python version": platform.python_version(),
            "PyTorch version (NPU?)": f"{pt_version} ({pt_npu_version if pt_npu_available else pt_npu_available})",
            "Mindspore version": f"{ms_version}",
        }

        info["Mindformers version"] = self._grab_package_version("mindformers")
        info["Transformers version"] = self._grab_package_version("transformers")
        info["Accelerate version"] = self._grab_package_version("accelerate")
        info["Datasets version"] = self._grab_package_version("datasets")
        info["Evaluate version"] = self._grab_package_version("evaluate")
        info["DeepSpeed version"] = self._grab_package_version("deepspeed")
        info["Lm-evaluation-harness version"] = self._grab_package_version("lm_eval")

        print(self._format_dict(info))
