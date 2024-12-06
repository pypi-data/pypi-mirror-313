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

from typing import TYPE_CHECKING

from ...utils import _LazyModule

if TYPE_CHECKING:
    from .auto_factory import (
        AutoConfig,
        AutoFeatureExtractor,
        AutoImageProcessor,
        AutoModel,
        AutoModelForCausalLM,
        AutoModelForSequenceClassification,
        AutoProcessor,
        AutoTokenizer,
    )
else:
    import sys

    _import_structure = {
        "auto_factory": [
            "AutoConfig",
            "AutoFeatureExtractor",
            "AutoImageProcessor",
            "AutoModel",
            "AutoModelForCausalLM",
            "AutoModelForSequenceClassification",
            "AutoProcessor",
            "AutoTokenizer",
        ],
    }

    sys.modules[__name__] = _LazyModule(__name__, globals()["__file__"], _import_structure, module_spec=__spec__)
