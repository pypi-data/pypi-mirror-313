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

from .import_utils import (
    DummyObject,
    _LazyModule,
    get_framework,
    is_decord_available,
    is_torch_available,
    is_torch_npu_available,
    is_ms_available,
    is_transformers_available,
    is_mindformers_available,
    is_diffusers_available,
    is_mindone_available,
    is_mindnlp_available,
    is_sentencepiece_available,
    is_timm_available,
    is_vision_available,
    is_tokenizers_available,
    is_lmeval_available,
    requires_backends,
)

from .generic import replace_invalid_characters

__all__ = [
    "get_framework",
    "is_ms_available",
    "is_torch_available",
    "is_torch_npu_available",
    "is_mindformers_available",
    "is_transformers_available",
    "is_diffusers_available",
    "is_mindone_available",
    "is_mindnlp_available",
    "is_tokenizers_available",
    "is_lmeval_available",
    "logging",
    "replace_invalid_characters",
]
