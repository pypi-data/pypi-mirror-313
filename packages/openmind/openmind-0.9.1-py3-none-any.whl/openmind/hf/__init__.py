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


from ..utils import is_transformers_available, is_torch_available

if is_transformers_available() and is_torch_available():
    import transformers

    from .npu_fused_ops.modeling_utils import (
        built_in_model_patchs,
        remote_model_patchs,
        _npu_fused_ops_imp,
    )

    transformers.modeling_utils.PreTrainedModel._autoset_attn_implementation = _npu_fused_ops_imp
    built_in_model_patchs()
    remote_model_patchs()
