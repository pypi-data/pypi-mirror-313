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
import torch
import logging

from ..utils.logging import get_logger

openmind_logger = get_logger(__name__)
openmind_logger.setLevel(logging.INFO)


def print_in_main_process(msg):
    local_rank = int(os.environ.get("LOCAL_RANK", -1))
    if local_rank in [0, -1]:
        openmind_logger.info(msg)


def is_last_rank():
    return torch.distributed.get_rank() == (torch.distributed.get_world_size() - 1)


def print_in_last_rank(msg):
    if torch.distributed.is_initialized():
        if is_last_rank():
            openmind_logger.info(msg)
    else:
        openmind_logger.info(msg)
