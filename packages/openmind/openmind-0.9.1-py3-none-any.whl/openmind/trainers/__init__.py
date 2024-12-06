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

from ..utils import _LazyModule

if TYPE_CHECKING:
    from .trainer import Trainer
    from .training_args import TrainingArguments
    from .pretrainer import PreTrainer
    from .pretraining_args import PreTrainingArguments
else:
    import sys

    _import_structure = {
        "trainer": ["Trainer"],
        "training_args": ["TrainingArguments"],
        "pretrainer": ["PreTrainer"],
        "pretraining_args": ["PreTrainingArguments"],
    }

    sys.modules[__name__] = _LazyModule(__name__, globals()["__file__"], _import_structure, module_spec=__spec__)
