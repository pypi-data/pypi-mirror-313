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
import ast
import json
import argparse
import inspect
import textwrap

import docker
from docker.errors import ContainerError, APIError

from ...utils.hub import OM_HUB_CACHE
from ..subcommand import SubCommand
from ..cli_utils import safe_load_yaml
from ...utils import logging
from ...utils.constants import (
    DEFAULT_FLAGS,
    DEFAULT_MODES,
    DYNAMIC_ARG,
)
from ...utils.hub import OpenMindHub

SPECIAL_PORTS_LIMIT = 1024

DEFAULT_YAML_CONFIG = {
    "ModelDeployParam": {
        "maxSeqLen": 2560,
        "npuDeviceIds": [[0, 1, 2, 3]],
        "ModelParam": {
            "modelInstanceType": "Standard",
            "modelName": "PyTorch-NPU/chatglm3_6b",
            "modelWeightPath": OM_HUB_CACHE,
            "worldSize": 4,
            "cpuMemSize": 5,
            "npuMemSize": 8,
            "backendType": "atb",
        },
    }
}

logger = logging.get_logger()
logging.set_verbosity_info()

# the docker default network segment
DOCKER_SUBNET_GATEWAY = "172.{}.0.0/16"
DOCKER_SUBNET_IP = "172.{}.0.2"
DOCKER_SUBNET_IP_SEGMENT_START = 18
DOCKER_SUBNET_IP_SEGMENT_END = 32
MINDIE_IMAGE_NAME = "mindie-image"


class Api(SubCommand):
    """Holds all the logic for the 'openmind-cli _api' subcommand."""

    def __init__(self, subparsers: argparse._SubParsersAction):
        super().__init__()
        self.host_model_path = None
        self._parser = subparsers.add_parser(
            "_api",
            prog="openmind-cli _api",
            help="Using mindie-service to Perform Inference via curl",
            description="Using mindie-service to Perform Inference via curl",
            epilog=textwrap.dedent(
                """\
            examples:
                $ openmind-cli _api PyTorch-NPU/chatglm3_6b

                $ openmind-cli _api PyTorch-NPU/chatglm3_6b --model_path /path/to/your/chatglm3_6b --npu_device_ids [[0,1,2,3]]

                $ openmind-cli _api PyTorch-NPU/chatglm3_6b --yaml_path config.yaml
                ...
            """
            ),
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )
        self._add_arguments()
        self._parser.set_defaults(func=self._api_cmd)

    @property
    def config_path(self):
        dir_name = os.path.dirname(inspect.getfile(self.__class__))
        return os.path.join(dir_name, "config.json")

    @property
    def npu_device_ids(self):
        npu_device_ids = None
        if isinstance(self.args.npu_device_ids, str):
            npu_device_ids = ast.literal_eval(self.args.npu_device_ids)
            if not all(0 <= num <= 7 for num in npu_device_ids[0]):
                raise ValueError("Device id must be in range 0 ~ 7 .")
        elif self.args.npu_device_ids is None:
            logger.info("Use default npu_device_ids [[0, 1, 2, 3]]")
        else:
            raise TypeError("npu_device_ids data type error, please check data type!")
        return npu_device_ids

    @property
    def max_seq_len(self):
        max_seq_len = None
        if isinstance(self.args.max_seq_len, int):
            max_seq_len = self.args.max_seq_len
        elif self.args.max_seq_len is None:
            logger.info("Use default max_seq_len 2560")
        else:
            raise TypeError("max_seq_len data type error, please check data type!")
        return max_seq_len

    def _add_arguments(self) -> None:
        """Add arguments to the parser."""
        self._parser.add_argument(
            "--model_path",
            type=str,
            help="path of the model",
        )
        self._parser.add_argument(
            "--port",
            type=int,
            default=1025,
            help="port for the service-oriented deployment",
        )
        self._parser.add_argument(
            "--max_seq_len",
            type=int,
            help="maximum length of the sequence",
        )
        self._parser.add_argument(
            "--npu_device_ids",
            type=str,
            help="npu ids allocated to the model instance",
        )
        self._parser.add_argument(
            "--yaml_path",
            type=str,
            default=None,
            help="Path to the YAML configuration file",
        )

    def _init_param(self, args: argparse.Namespace):
        args_dict = vars(args)
        args_dict.pop("func")
        self.model_id = args_dict.pop(DYNAMIC_ARG)

        self.use_default_model_path = False
        if args_dict.get("yaml_path") is not None:
            yaml_content_dict = safe_load_yaml(args_dict.pop("yaml_path"))
            yaml_device_ids = yaml_content_dict["ModelDeployParam"]["npuDeviceIds"]
            yaml_world_size = yaml_content_dict["ModelDeployParam"]["ModelParam"]["worldSize"]
            self.host_model_path = yaml_content_dict["ModelDeployParam"]["ModelParam"]["modelWeightPath"]

            if len(yaml_device_ids[0]) != yaml_world_size:
                raise ValueError("WorldSize must be consistent with npuDeviceIds!")
        else:
            yaml_content_dict = DEFAULT_YAML_CONFIG

        if self.args.model_path:
            self.host_model_path = self.args.model_path
        if not self.host_model_path:
            self.host_model_path = os.path.join(OM_HUB_CACHE, "--".join(self.model_id.split("/")))
            self.use_default_model_path = True
        self.host_model_path = os.path.abspath(self.host_model_path)

        yaml_content_dict["ModelDeployParam"]["ModelParam"]["modelName"] = self.model_id
        yaml_content_dict["ModelDeployParam"]["ModelParam"] = [yaml_content_dict["ModelDeployParam"].pop("ModelParam")]
        yaml_content_dict["ModelDeployParam"]["ModelParam"][0]["modelWeightPath"] = self.host_model_path

        if self.npu_device_ids:
            self.host_npu_ids = self.npu_device_ids
            yaml_content_dict["ModelDeployParam"]["ModelParam"][0]["worldSize"] = len(self.npu_device_ids[0])
        else:
            self.host_npu_ids = yaml_content_dict["ModelDeployParam"]["npuDeviceIds"]
        if self.max_seq_len:
            yaml_content_dict["ModelDeployParam"]["maxSeqLen"] = self.max_seq_len
        return yaml_content_dict

    def _pull_model(self):
        OpenMindHub.snapshot_download(self.model_id, cache_dir=self.host_model_path)

    def _update_config(self, yaml_content_dict):
        with open(self.config_path, "r") as f:
            config_content = json.load(f)

        world_size = yaml_content_dict["ModelDeployParam"]["ModelParam"][0]["worldSize"]
        yaml_content_dict["ModelDeployParam"]["npuDeviceIds"] = [[i for i in range(world_size)]]

        config_content["OtherParam"]["ServeParam"]["httpsEnabled"] = False
        config_content["ModelDeployParam"] = yaml_content_dict["ModelDeployParam"]

        # ipAddress must be set as current container's ip, or else we can not curl from host device
        config_content["OtherParam"]["ServeParam"]["ipAddress"] = self.addr

        if self.args.port:
            if self.args.port <= SPECIAL_PORTS_LIMIT:
                raise ValueError(f"Port must be greater than {SPECIAL_PORTS_LIMIT}.")
            config_content["OtherParam"]["ServeParam"]["port"] = self.args.port
        if os.path.exists(self.config_path):
            os.remove(self.config_path)
        with os.fdopen(os.open(self.config_path, DEFAULT_FLAGS, DEFAULT_MODES), "w", encoding="utf-8") as f:
            json.dump(config_content, f, ensure_ascii=False, indent=4)

    def _start_container(self):
        devices = [f"/dev/davinci{i}" for i in self.host_npu_ids[0]]
        devices.extend(["/dev/davinci_manager", "/dev/hisi_hdc", "/dev/devmm_svm"])
        volumes = [
            "/usr/local/Ascend/driver:/usr/local/Ascend/driver",
            "/usr/local/dcmi:/usr/local/dcmi",
            "/usr/local/bin/npu-smi:/usr/local/bin/npu-smi",
            "/usr/local/sbin:/usr/local/sbin",
            "/tmp:/tmp",
            "/usr/share/zoneinfo/Asia/Shanghai:/etc/localtime",
            f"{self.host_model_path}:{self.host_model_path}",
            f"{self.config_path}:/usr/local/Ascend/mindie/latest/mindie-service/conf/config.json",
        ]

        try:
            self.client.containers.run(
                image=MINDIE_IMAGE_NAME,
                command="/bin/bash",
                name=self.container_name,
                volumes=volumes,
                ports={f"{self.args.port}": f"{self.args.port}"},
                devices=devices,
                detach=True,
                network=self.network_name,
            )
            logger.info(f"Docker run and container init success! The container ip is {self.addr}")

        except (ContainerError, APIError) as err:
            logger.error(f"There is an error during container initialization:{err}")
            if self.client.networks.get(self.network_name) is not None:
                self.client.networks.get(self.network_name).remove()

    def _api_cmd(self, args: argparse.Namespace) -> None:
        """Using mindieservice to perform inference via curl"""
        self.args = args
        self.container_name = "mindie-service"
        self.network_name = "mindie-network"
        self.client = docker.from_env()
        if vars(args).get(DYNAMIC_ARG) == "stop":
            self._stop_service(remind=True)
            return
        yaml_content_dict = self._init_param(args)
        self._pull_model()
        self._create_network()
        self._update_config(yaml_content_dict)
        self._start_container()

    def _create_network(self):
        """create network for mindie service container"""
        self._stop_service()
        self.addr = None
        for ip in range(DOCKER_SUBNET_IP_SEGMENT_START, DOCKER_SUBNET_IP_SEGMENT_END):
            # find available ip network segment
            try:
                self.client.networks.create(
                    self.network_name,
                    driver="bridge",
                    ipam=docker.types.IPAMConfig(
                        pool_configs=[docker.types.IPAMPool(subnet=DOCKER_SUBNET_GATEWAY.format(ip))]
                    ),
                )
                self.addr = DOCKER_SUBNET_IP.format(ip)
                break
            except APIError:
                continue

        if self.addr is None:
            raise EnvironmentError("No avaliable network for docker daemon service, please check your network config.")

    def _stop_service(self, remind=False):
        containers = self.client.containers.list(all=True)
        if any(self.container_name == container.name for container in containers):
            container = self.client.containers.get(self.container_name)
            container.remove(force=True)
            if remind:
                logger.info("Stop mindie service success.")
        elif remind:
            logger.info("There is no mindie daemon service to stop.")
        if (
            any(self.network_name == network.name for network in self.client.networks.list())
            and self.client.networks.get(self.network_name) is not None
        ):
            self.client.networks.get(self.network_name).remove()
