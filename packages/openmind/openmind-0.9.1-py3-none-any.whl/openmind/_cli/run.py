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
import copy
import tempfile

from .subcommand import SubCommand
from .cli_utils import safe_load_yaml, try_to_trans_to_dict
from .cli_docker import CLIDocker
from ..utils.constants import DYNAMIC_ARG, SPECIFIED_ARGS
from ..pipelines import pipeline
from ..pipelines.pipeline_utils import SUPPORTED_TASK_MAPPING
from ..utils import is_vision_available, is_ms_available


class Run(SubCommand):
    """Holds all the logic for the `openmind-cli run` subcommand."""

    def __init__(self, subparsers: argparse._SubParsersAction):
        super().__init__()
        self._parser = subparsers.add_parser(
            "run",
            prog="openmind-cli run repo_id/task_type input/file_path ",
            help="Run models from openMind",
            description="run models from openMind",
            epilog=textwrap.dedent(
                """\
            examples:
                $ openmind-cli run PyTorch-NPU/bloom_1b1 --input "Give three tips for staying healthy"

                $ openmind-cli run PyTorch-NPU/bloom_1b1 --input "Give three tips for staying healthy" --task "text-generation"

                $ openmind-cli run text-generation --input "Give three tips for staying healthy" 
            """
            ),
            formatter_class=argparse.RawTextHelpFormatter,
        )
        self._add_arguments()
        self._parser.set_defaults(func=self._run_cmd)

    def _add_arguments(self) -> None:
        """Add arguments to the parser."""
        self._parser.add_argument(
            "--input",
            type=str,
            default=None,
            required=True,
            help="input content or file path",
        )
        self._parser.add_argument(
            "--task",
            type=str,
            default=None,
            help="task type",
        )
        self._parser.add_argument(
            "--framework",
            type=str,
            default=None,
            help="framework type, choosing from pt or ms",
        )
        self._parser.add_argument(
            "--backend",
            type=str,
            default=None,
            help="backend type, choosing the corresponding backend based on the framework",
        )
        self._parser.add_argument(
            "--cache_dir",
            type=str,
            default=None,
            help="cache directory of downloaded models",
        )
        self._parser.add_argument(
            "--yaml_path",
            type=str,
            default=None,
            help="path of yaml",
        )
        self._parser.add_argument(
            "--docker",
            type=str,
            default=None,
            help="whether to use docker or not",
        )

    def _init_pipeline(self, **kwargs):
        return pipeline(**kwargs)

    def _extract_params(self, args):
        if args.yaml_path:
            config_data = safe_load_yaml(args.yaml_path)
        else:
            config_data = dict()
        config_data["repo_or_task"] = vars(copy.deepcopy(args)).pop(DYNAMIC_ARG)
        vars(args).pop("func")
        vars(args).pop("yaml_path")

        specified_args = vars(args).pop(SPECIFIED_ARGS)

        for key, value in vars(args).items():
            if key not in config_data:
                config_data[key] = value
            # specified args has a higher priority than yaml
            elif key in config_data and key in specified_args:
                config_data[key] = specified_args[key]

        model_kwargs = config_data.get("model_kwargs", None)
        if model_kwargs:
            model_kwargs = try_to_trans_to_dict(model_kwargs)
            config_data["model_kwargs"] = model_kwargs

        input_or_path = config_data.pop("input")
        input_or_path = try_to_trans_to_dict(input_or_path)
        config_data["input"] = input_or_path

        return config_data

    def _run_cmd_without_docker(self, params) -> None:
        repo_or_task = params.pop("repo_or_task")
        input_or_path = params.pop("input")
        if repo_or_task in SUPPORTED_TASK_MAPPING:
            params["task"] = repo_or_task
        else:
            params["model"] = repo_or_task

        is_pt_framework = params.get("framework", None) is None or params.get("framework") == "pt"
        if is_pt_framework and params.get("device", None) is None and params.get("device_map", None) is None:
            params["device"] = "npu:0"
        elif (
            params.get("framework") == "ms"
            and params.get("device_id", None) is None
            and params.get("device_target", None) is None
        ):
            params["device_id"] = 0

        if is_ms_available():
            import mindspore as ms

            ms.set_context(
                mode=0,
                device_id=int(params.get("device_id", 0)),
                jit_level="o0",
                infer_boost="on",
                max_device_memory="59GB",
            )

        pipe = self._init_pipeline(**params)
        # input_or_path can be str or dict
        if isinstance(input_or_path, dict):
            output = pipe(**input_or_path)
        else:
            output = pipe(input_or_path)
        if is_vision_available():
            from PIL import Image

            if isinstance(output, Image.Image):
                with tempfile.NamedTemporaryFile(suffix=".jpg", dir="./", delete=False) as f:
                    output.save(f.name)
                    print(f"Image has been saved to {f.name}")
            else:
                print(output)
        else:
            print(output)

    def _run_cmd(self, args: argparse.Namespace) -> None:
        params = self._extract_params(args)
        if params.get("docker", None):
            CLIDocker.start_docker(args, params)
        else:
            params.pop("docker")
            params.pop(DYNAMIC_ARG)
            self._run_cmd_without_docker(params)
