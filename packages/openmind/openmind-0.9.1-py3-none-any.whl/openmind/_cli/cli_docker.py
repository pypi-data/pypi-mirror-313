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
import re
import ast
import sys
import stat
import shlex
import subprocess
import argparse
import importlib.metadata

from packaging.version import Version

from openmind.utils.hub import OpenMindHub
from .list import List
from ..utils import replace_invalid_characters
from ..utils.hub import OPENMIND_CACHE
from ..pipelines.pipeline_utils import SUPPORTED_TASK_MAPPING
from ..utils.logging import get_logger, set_verbosity_info
from ..utils.capability_check import (
    is_default_npu_openmind_version,
    is_default_cpu_openmind_version,
    is_openmind_version_below_minimum_requirement,
    is_openmind_version_mismatch,
)
from ..utils.constants import (
    GIT,
    GIT_LOGS_HEAD,
    OPENMIND_PREFIX,
    DOCKER_TAG_PARRETN,
    METADATA_EXTRA_INFO,
    OPENMIND_CACHE_IN_DOCKER,
    GE_CONFIG_IN_DOCKER,
    PYTORCH_IN_TAG,
    CHAT_MODEL_TEMPLATE_MAPPINGS,
)

logger = get_logger()

set_verbosity_info()


class CLIDocker:
    @staticmethod
    def trans_path_to_repo_id(model_name_or_path: str):
        if os.path.exists(model_name_or_path):
            git_head_path = os.path.join(model_name_or_path, GIT_LOGS_HEAD)
            # download model from git
            if os.path.exists(git_head_path):
                with open(git_head_path, "r") as f:
                    git_log_info = f.read().split()[-1]
                if OPENMIND_PREFIX in git_log_info:
                    repo_id = git_log_info.split(OPENMIND_PREFIX)[1].split(GIT)[0]

            # download model from snapshot_download
            # model_name_or_path: /xxx/xxx/models--organization--model/snapshots/xxx
            else:
                repo_id = "/".join(model_name_or_path.rstrip("/").split("/")[-3].split("--")[1:])
        else:
            repo_id = model_name_or_path

        return repo_id

    @staticmethod
    def choose_info_from_ci(ci_info: list, current_openmind_version: str):
        """
        Model CI info is defined as:
        ModelCiInfo(total=1, model_ci=[{'status': 'success', 'created_at': 'xxx', 'updated_at': 'xxx', 'stop_reason': 'model_ci_stop_by_user', \
            'result_url': '', 'hardware_version': 'NPU', 'framework': 'PyTorch', 'framework_version': '6.0.rc1-pytorch2.1.0', \
            'cann_version': '8.0.RC1.beta1', 'python_version': '3.8', 'openmind_version': '0.6.0', \
            'openeuler_version': 'openeuler-python3.8-cann8.0-pytorch2.1.0-openmind0.6.0'}])
        """

        # 'NPU' > 'CPU', 'python_version': '3.10' > '3.8'
        ci_info.sort(
            key=lambda x: (
                x["hardware_version"],
                Version(x["openmind_version"]),
                x["cann_version"],
                Version(x["python_version"]),
            ),
            reverse=True,
        )
        if ci_info[0]["framework"].lower() == "pytorch":
            ci_info.sort(key=lambda x: x["framework_version"], reverse=True)
        elif ci_info[0]["framework"].lower() == "mindspore":
            ci_info.sort(key=lambda x: Version(x["framework_version"]), reverse=True)
        latest_info = ci_info[0]

        docker_info_dict = {
            "hardware": latest_info["hardware_version"].lower(),
            "framework": latest_info["framework"].lower(),
            "openmind": latest_info["openmind_version"],
        }

        if is_openmind_version_below_minimum_requirement(latest_info["openmind_version"]):
            raise ValueError("openmind version is below the minimum requirement 0.8.0")
        elif is_openmind_version_mismatch(latest_info["openmind_version"], current_openmind_version):
            logger.info(f"openmind version mismatch and will be set to {latest_info['openmind_version']}")
        docker_tag = latest_info["openeuler_version"]

        return docker_tag, docker_info_dict

    @staticmethod
    def choose_info_from_metadata(extra_info: list, current_openmind_version: str):
        """
        Meta data extra info is defined as:
        extra='{"environment":["python:3.8 hardware:npu pytorch:2.1.0 cann:8.0 openmind:0.6.0", \
            "python:3.8 hardware:cpu pytorch:2.1.0 cann:8.0 openmind:0.6.0"]}' \
        has been converted into \
            [['python:3.8', 'hardware:npu', 'pytorch:2.1.0', 'cann:8.0', 'openmind:0.6.0'], \
                ['python:3.8', 'hardware:cpu', 'pytorch:2.1.0', 'cann:8.0', 'openmind:0.6.0']]
        """

        # convert str into dict
        extra_info_dict = []
        for each_info in extra_info:
            each_info_dict = dict()
            for each_ver in each_info:
                key, value = each_ver.split(":")
                each_info_dict[key] = value
            extra_info_dict.append(each_info_dict)

        valid_env_info = []
        docker_tag = "openeuler-"
        tag_info = []

        # select envs with correct keys
        for each_env in extra_info_dict:
            lower_each_env = {k.lower(): v.lower() for k, v in each_env.items()}
            key_set = set(lower_each_env.keys())
            key_set.add("pytorch")
            key_set.add("mindspore")
            if key_set == METADATA_EXTRA_INFO:
                valid_env_info.append(lower_each_env)

        valid_env_info.sort(
            key=lambda x: (x["hardware"], Version(x["openmind"]), x["cann"], Version(x["python"])),
            reverse=True,
        )

        if "pytorch" in valid_env_info[0]:
            framework = "pytorch"
            valid_env_info.sort(key=lambda x: x["pytorch"], reverse=True)
        else:
            framework = "mindspore"
            valid_env_info.sort(key=lambda x: Version(x["mindspore"]), reverse=True)
        latest_info = valid_env_info[0]

        docker_info_dict = {
            "hardware": latest_info["hardware"],
            "framework": framework,
            "openmind": latest_info["openmind"],
        }

        tag_info.append("python" + latest_info["python"])
        if latest_info["hardware"] == "npu":
            tag_info.append("cann" + latest_info["cann"])
        tag_info.append(framework + latest_info[framework])
        if is_openmind_version_below_minimum_requirement(latest_info["openmind"]):
            raise ValueError("openmind version is below the minimum requirement 0.8.0")
        elif is_openmind_version_mismatch(latest_info["openmind"], current_openmind_version):
            logger.info(f"openmind version mismatch and will be set to {latest_info['openmind']}")
        tag_info.append("openmind" + latest_info["openmind"])
        docker_tag += "-".join(tag_info)

        return docker_tag, docker_info_dict

    @staticmethod
    def choose_tag(tag: str, model_name_or_path: str):
        """Concatenate suitable tag from CI/Metadata info"""
        tag = tag.lower()
        repo_id = CLIDocker.trans_path_to_repo_id(model_name_or_path)
        current_openmind_version = importlib.metadata.version("openmind")
        docker_info_dict = {}

        model_metadata = OpenMindHub.get_model_info(repo_id=repo_id)
        framework = model_metadata.library_name.lower() if model_metadata.library_name else None
        try:
            # model_ci_info may not exist
            model_ci_info = OpenMindHub.get_model_ci_info(repo_id=repo_id)
            model_ci_info_list = model_ci_info.model_ci
            framework = model_ci_info_list[0]["framework"].lower()
            valid_model_ci_info_list = [x for x in model_ci_info_list if x["status"] == "success"]
        except Exception as ex:
            logger.info(f"Cannot obtain model CI information due to {str(ex)}.")
            valid_model_ci_info_list = []

        if tag != "default":
            # tag should be like openeuler-python3.8-pytorch2.1.0-openmind0.8.0 or \
            #     openeuler-python3.8-cann8.0-pytorch2.1.0-openmind0.8.0 or \
            #     openeuler-python3.8-cann8.0-mindspore2.3.0rc1-pytorch2.1.0-openmind0.8.0
            docker_tag = tag
            if tag == "latest-ms" or tag == "latest-pt":
                if framework is None:
                    raise ValueError(
                        "Please specify a framework from either MindSpore or PyTorch, dual frameworks are currently not supported."
                    )
                docker_info_dict["hardware"] = "npu"
                docker_info_dict["framework"] = framework
                docker_info_dict["openmind"] = "latest"
            else:
                if len(tag.split("-")) < 4 or len(tag.split("-")) > 6:
                    raise ValueError("The format of the tag is incorrect, please check it again.")

                if not re.match(DOCKER_TAG_PARRETN, tag):
                    raise ValueError("Invalid docker tag, please check it again.")

                if is_openmind_version_below_minimum_requirement(tag.split("openmind")[1]):
                    raise ValueError(
                        "Specified openmind version is below the minimum requirement, please upgrade it to >= 0.8.0"
                    )

                logger.info(f"Start specified docker version: {tag}, which may not be validated by CI.")

                docker_info_dict["hardware"] = "npu" if "cann" in tag else "cpu"
                if "mindspore" in tag and "pytorch" in tag:
                    docker_info_dict["framework"] = None
                elif "mindspore" in tag and "pytorch" not in tag:
                    docker_info_dict["framework"] = "mindspore"
                elif "pytorch" in tag and "mindspore" not in tag:
                    docker_info_dict["framework"] = "pytorch"
                docker_info_dict["openmind"] = tag.split("-")[-1].split("openmind")[1]

        else:
            try:
                # extra data may not exist
                extra_info_list = ast.literal_eval(model_metadata.extra)["environment"]
                valid_extra_info_list = [x.split() for x in extra_info_list if len(x.split()) == 5]
            except Exception as ex:
                logger.info(f"Cannot obtain extra environment information due to {str(ex)}.")
                valid_extra_info_list = []

            # CI info has a higher priority than extra environment info
            if valid_model_ci_info_list:
                docker_tag, docker_info_dict = CLIDocker.choose_info_from_ci(
                    valid_model_ci_info_list, current_openmind_version
                )
                logger.info(f"Start valid CI docker version: {docker_tag}")
            elif valid_extra_info_list:
                docker_tag, docker_info_dict = CLIDocker.choose_info_from_metadata(
                    valid_extra_info_list, current_openmind_version
                )
                logger.info(
                    f"Start valid extra environment docker version: {docker_tag}, which may not be validated by CI."
                )
            else:
                # set default version
                if framework is None:
                    raise ValueError(
                        "Please specify a framework from either MindSpore or PyTorch, dual frameworks are currently not supported."
                    )
                else:
                    docker_tag = "latest-pt" if framework == PYTORCH_IN_TAG else "latest-ms"
                logger.info(
                    f"No valid information found, start default docker version: {docker_tag}, which may not be validated by CI."
                )
                docker_info_dict["hardware"] = "npu"
                docker_info_dict["framework"] = framework
                docker_info_dict["openmind"] = "latest"

        return docker_tag, docker_info_dict

    @staticmethod
    def get_device_id(params: dict, tag_dict: dict) -> tuple:
        """
        Check the validity of parameters: "--device", "device_map", "device_id", "device_target" base on the inputs and
        tag infomation, and then get the devices which need to be mapped.

        Inputs:
            Two dicts of the parameters and tag infomation.
        Returns:
            A tuple includes a list of devices and a mindspore flag.
        """
        device = params.get("device", None)
        device_map = params.get("device_map", None)
        # the input of device_id should be an integer in range[0, 7].
        device_id = params.get("device_id", None)
        # the input of device_target could be CPU, GPU and Ascend.
        device_target = params.get("device_target", None)
        if device_target is not None:
            device_target = device_target.lower()
        device_list = [device, device_map, device_id, device_target]
        openmind_ver = tag_dict.get("openmind", None)

        # user specified hardware has higher priority than tag.
        if any(param == "cpu" for param in device_list):
            return [], False

        if all(var is None for var in device_list):
            if openmind_ver == "latest" or is_default_npu_openmind_version(openmind_ver):
                # default choice is use "npu:0" when openmind>=0.9.0
                return [0], False
            elif is_default_cpu_openmind_version(openmind_ver):
                # default choice is use "cpu" if openmind<0.9.0
                return [], False

        # can not specify npu when the hardware is cpu
        if tag_dict.get("hardware", None) == "cpu" and any(var is not None for var in device_list):
            raise ValueError("Device specification is not supported when using the CPU.")

        # Select the correct devices based on framework and hardware
        docker_device = []
        # Flag which represents mapping the device with MS framework
        ms_device = False
        if tag_dict.get("framework", None) == PYTORCH_IN_TAG:
            if device_id is not None or device_target is not None:
                raise ValueError("'--device_id' or '--device_target' are only used in MindSpore framework.")
            if device is not None:
                if device == "npu":
                    docker_device.append(0)
                else:
                    docker_device.append(int(device[-1]))
            if device_map is not None:
                if device_map == "npu":
                    docker_device.append(0)
                elif device_map[:3] == "npu":
                    docker_device.append(int(device_map[-1]))
                else:
                    # Map all eight devices under other circumstances
                    docker_device = [i for i in range(8)]
        else:
            # When framework is MindSpore
            if device is not None or device_map is not None:
                raise ValueError("'--device' or '--device_map' are only used in PyTorch framework.")

            if device_target is None and device_id is not None:
                docker_device.append(int(device_id))
                ms_device = True

            if device_target == "ascend" and device_id is not None:
                docker_device.append(int(device_id))
                ms_device = True

        return docker_device, ms_device

    @staticmethod
    def check_path(path):
        # Check if the path exists and whether it has read permission
        try:
            permissions = os.stat(path).st_mode
            is_readable_by_others = bool(permissions & stat.S_IROTH)
        except FileNotFoundError as e:
            msg = f"The file or directory '{path}' does not exist"
            raise FileNotFoundError(replace_invalid_characters(msg)) from e
        except PermissionError as e:
            msg = f"Permission denied when accessing '{path}'"
            raise PermissionError(replace_invalid_characters(msg)) from e
        except TypeError as e:
            msg = f"TypeError: {e}"
            raise TypeError(replace_invalid_characters(msg)) from e

        if not is_readable_by_others:
            msg = f"The file/folder '{path}' should be at least readable by others"
            raise PermissionError(replace_invalid_characters(msg))

    @staticmethod
    def get_model_path(args, cache_dir) -> str:
        _parser = argparse.ArgumentParser()
        subparsers = _parser.add_subparsers(title="subcommands")
        cli_list = List(subparsers)

        # Check if the model_path exists
        model_name_or_path = args._dynamic_arg
        model_path = None
        model_commit_id = None
        is_local_model = False

        if model_name_or_path in SUPPORTED_TASK_MAPPING:
            supported_models = SUPPORTED_TASK_MAPPING[model_name_or_path]["pt"]["transformers"]["supported_models"]
            model = supported_models[0]
            if "@" in model:
                model_name_or_path, model_commit_id = model.split("@")
            else:
                model_name_or_path = model

        if os.path.exists(model_name_or_path):
            # Map the directory
            model_path = model_name_or_path
        else:
            args.local_dir = None
            args.cache_dir = cache_dir
            os.makedirs(cache_dir, exist_ok=True)
            model_info = cli_list._get_model_info(args)
            for model in model_info:
                if model_name_or_path == model[0]:
                    model_path = model[1]
                    is_local_model = True

        # get the full path if the model was downloaded by snapshots
        if is_local_model and os.path.exists(os.path.join(model_path, "snapshots")):
            model_path = os.path.join(model_path, "snapshots")
            for item in os.listdir(model_path):
                # get commit id
                if os.path.exists(os.path.join(model_path, item, "config.json")):
                    model_path = os.path.join(model_path, item)

        # if don't find the model, download it.
        if model_path is None:
            model_path = OpenMindHub.snapshot_download(
                repo_id=model_name_or_path,
                cache_dir=cache_dir,
                revision=model_commit_id,
            )

        model_path = os.path.realpath(model_path)

        return model_path

    @staticmethod
    def generate_docker_command(docker_device, model_path, ge_config_path):
        """
        Init and concatenate the docker command.

        Inputs:
            docker_device: a list contains the NPU device ids that need to be mapped
            model_path: a str that represents the model path in host machine
            ge_config_path: a str that represents the ge_config path in host machine

        Returns:
            A concatenated docker_command and a path of the last two layers if the model is downloaded by snapshots

        Examples of snapshot_path:
            "/snapshots/a8c340dacb3bff5794a4925d39615e6c217ef7b3/"
        """
        docker_command = "docker run -it --user openmind "

        # map the npu
        for deviceid in set(docker_device):
            docker_command += f"--device=/dev/davinci{str(deviceid)} "

        docker_command += """
        --device=/dev/davinci_manager \
        --device=/dev/hisi_hdc \
        --device=/dev/devmm_svm \
        -v /usr/local/Ascend/driver:/usr/local/Ascend/driver \
        -v /usr/local/dcmi:/usr/local/dcmi \
        -v /usr/local/bin/npu-smi:/usr/local/bin/npu-smi \
        -v /usr/local/sbin:/usr/local/sbin \
        """

        # Map the paths with the Read Only mode
        CLIDocker.check_path(model_path)
        abs_model_path = os.path.abspath(model_path)
        splitted_str = abs_model_path.split("/")
        snapshot_path = ""
        if splitted_str[-2] == "snapshots":
            abs_model_path = "/".join(splitted_str[:-2])
            snapshot_path = "/".join(splitted_str[-2:])

        CLIDocker.check_path(abs_model_path)
        docker_command += f"-v {abs_model_path}:{OPENMIND_CACHE_IN_DOCKER}:ro "

        if ge_config_path is not None:
            CLIDocker.check_path(ge_config_path)
            abs_ge_config_path = os.path.abspath(os.path.realpath(ge_config_path))
            docker_command += f"-v {abs_ge_config_path}:{GE_CONFIG_IN_DOCKER}:ro "

        return docker_command, snapshot_path

    @staticmethod
    def start_docker(args, params):
        # Check if docker has been installed
        try:
            subprocess.run(["docker", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            raise subprocess.CalledProcessError(1, "Docker is not installed. Please install it first.") from e
        except FileNotFoundError as e:
            raise FileNotFoundError("Docker is not installed. Please install it first.") from e

        cache_dir = params.pop("cache_dir", None)
        if cache_dir is None:
            cache_dir = OPENMIND_CACHE
        model_path = CLIDocker.get_model_path(args, cache_dir)

        tag, tag_dict = CLIDocker.choose_tag(params.pop("docker"), model_path)
        params.pop("_dynamic_arg", None)
        params.pop("repo_or_task", None)
        docker_device, ms_device = CLIDocker.get_device_id(params, tag_dict)

        ge_config_path = params.get("ge_config_path", None)
        docker_command, snapshot_path = CLIDocker.generate_docker_command(docker_device, model_path, ge_config_path)

        # Need to specify a framework in docker to avoid errors.
        if tag_dict.get("framework", None) == PYTORCH_IN_TAG:
            docker_command += "-e OPENMIND_FRAMEWORK=pt "
        else:
            docker_command += "-e OPENMIND_FRAMEWORK=ms "

        input_msg = params.get("input", None)
        if isinstance(input_msg, dict):
            for key, value in input_msg.items():
                if isinstance(value, str) and os.path.exists(value):
                    CLIDocker.check_path(value)
                    file_name = value.split("/")[-1]
                    docker_command += f"-v {value}:/home/openmind/image/{key}/{file_name} "
                    input_msg[key] = f"/home/openmind/image/{key}/{file_name}"
        elif input_msg is not None and os.path.exists(input_msg):
            CLIDocker.check_path(input_msg)
            file_name = input_msg.split("/")[-1]
            docker_command += f"-v {input_msg}:/home/openmind/image/{file_name} "
            input_msg = f"/home/openmind/image/{file_name}"

        if input_msg:
            params["input"] = f'"{input_msg}"'

        # modify the cli command
        cmd = {"chat", "run"}

        if params.get("ge_config_path", None) is not None:
            params["ge_config_path"] = GE_CONFIG_IN_DOCKER

        if params.get("device", None) is not None and params.get("device")[:3] == "npu":
            params["device"] = "npu:0"
        if params.get("device_map", None) is not None and params.get("device_map")[:3] == "npu":
            params["device_map"] = "npu:0"
        if ms_device and params.get("device_id", None) is not None:
            params["device_id"] = 0

        cli_command = "openmind-cli "

        for idx in range(1, len(sys.argv)):
            # model has been downloaded and mapped as a path
            if sys.argv[idx] in cmd:
                model_path_in_container = os.path.join(OPENMIND_CACHE_IN_DOCKER, snapshot_path)
                cli_command = f"{cli_command} {sys.argv[idx]} {model_path_in_container} "
                break

        template = params.get("template", None)
        if sys.argv[1] == "chat" and args._dynamic_arg in CHAT_MODEL_TEMPLATE_MAPPINGS and template is None:
            openmind_ver = tag_dict.get("openmind", None)
            if openmind_ver == "latest" or is_default_npu_openmind_version(openmind_ver):
                params["template"] = CHAT_MODEL_TEMPLATE_MAPPINGS[args._dynamic_arg]

        for key, value in params.items():
            if value is not None:
                cli_command += f"--{key} {value} "

        # Stop and remove the container after finishing the inference task
        docker_command += f"--rm registry.modelers.cn/base_image/openmind-unprivileged:{tag} /bin/bash -c"
        docker_command = docker_command.replace("\n", "")

        # Prevent Command Injection
        black_symbol_list = {"|", ";", "$", "&", "<", ">", "`", "\n"}
        if any(char in cli_command for char in black_symbol_list):
            raise ValueError("Cli command should not contain any of '|', ';', '$', '&', '<', '>', '`', '\n'.")

        try:
            docker_cmd = shlex.split(docker_command)
            docker_cmd.append(cli_command)
            subprocess.run(docker_cmd, shell=False, check=True)
            logger.info("Docker run and container init success!")
        except subprocess.CalledProcessError as e:
            logger.error(f"Error during container initiation:{e}")

        return
