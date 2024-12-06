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

from ..utils.import_utils import is_transformers_available
from ..utils.patch_utils import _apply_patches


# NOTE: If the module need to monkey patch has already been imported and was being
# used by other code, that it could have created a local reference to a target
# function it wishes to wrap, in its own namespace. So although the monkey patch
# would work fine where the original function was used direct from the module, it
# would not cover where it was used via a local reference.
#
# The import and monkey patch order should be hard coded and limited. The most base
# modules should be imported and patched first.
#
# Please Do not import other modules before hub patch!!!

if is_transformers_available():
    # logger patch
    from transformers.utils import logging as hf_logging

    from ..utils import logging

    patch_list = [
        ("get_logger", logging.get_logger),
        ("set_verbosity_info", logging.set_verbosity_info),
        ("set_verbosity_critical", logging.set_verbosity_critical),
        ("set_verbosity_error", logging.set_verbosity_error),
        ("set_verbosity_debug", logging.set_verbosity_debug),
        ("set_verbosity_warning", logging.set_verbosity_warning),
        ("set_verbosity", logging.set_verbosity),
    ]
    _apply_patches(patch_list, hf_logging)
