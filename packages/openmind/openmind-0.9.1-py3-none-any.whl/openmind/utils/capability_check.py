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

from packaging.version import Version


def is_default_npu_openmind_version(openmind_ver):
    return Version(openmind_ver) >= Version("0.9.0")


def is_default_cpu_openmind_version(openmind_ver):
    return Version(openmind_ver) < Version("0.9.0")


def is_openmind_version_below_minimum_requirement(openmind_ver):
    return Version(openmind_ver) < Version("0.8.0")


def is_openmind_version_mismatch(target_version, current_version):
    return Version(target_version) != Version(current_version)
