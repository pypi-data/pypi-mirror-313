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
import sys
import warnings

try:
    # This is populated by hatch_build.py
    from openmind.git_version_info import __version__
except ModuleNotFoundError:
    __version__ = "0.9.1"

if sys.version_info.major < 3 or (sys.version_info.major == 3 and sys.version_info.minor <= 8):
    warnings.warn(
        "Python 3.8 or lower versions have reached the end of their life cycles. openMind will "
        "no longer support Python 3.8 and lower versions in future releases.",
        FutureWarning,
    )
