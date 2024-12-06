# Copyright 2023 Mistral AI and the HuggingFace Inc. team. All rights reserved.
# 2024.09.27 - Adapt to openmind.
#              Huawei Technologies Co., Ltd.
# This code is based on EleutherAI's GPT-NeoX library and the GPT-NeoX
# and OPT implementations in this library. It has been modified from its
# original forms to accommodate minor architectural differences compared
# to GPT-NeoX and OPT used by the Meta AI team that trained the model.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import math
from typing import Optional, Tuple

import torch

# Remove the `try/catch` statement when CI is migrated to NPU devices
try:
    import torch_npu
except ImportError:
    pass

from transformers.cache_utils import Cache
from transformers.models.mistral.modeling_mistral import MistralAttention, apply_rotary_pos_emb


class MistralNpuFlashAttention(MistralAttention):
    """
    Mistral attention module using `torch_npu.npu_fusion_attention` This module inherits from
    `MistralAttention` as the weights of the module stays untouched. The only changes are on the
    forward pass to adapt to NPU FA API.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scale_value = 1.0 / math.sqrt(self.head_dim)

    # Adapted from MistralAttention.forward
    def forward(
        self,
        hidden_states: torch.Tensor,
        attention_mask: Optional[torch.Tensor] = None,
        position_ids: Optional[torch.LongTensor] = None,
        past_key_value: Optional[Cache] = None,
        output_attentions: bool = False,
        use_cache: bool = False,
        cache_position: Optional[torch.LongTensor] = None,
    ) -> Tuple[torch.Tensor, Optional[torch.Tensor], Optional[Tuple[torch.Tensor]]]:
        bsz, q_len, _ = hidden_states.size()

        query_states = self.q_proj(hidden_states)
        key_states = self.k_proj(hidden_states)
        value_states = self.v_proj(hidden_states)

        query_states = query_states.view(bsz, q_len, self.num_heads, self.head_dim).transpose(1, 2)
        key_states = key_states.view(bsz, q_len, self.num_key_value_heads, self.head_dim).transpose(1, 2)
        value_states = value_states.view(bsz, q_len, self.num_key_value_heads, self.head_dim).transpose(1, 2)

        cos, sin = self.rotary_emb(value_states, position_ids)
        query_states, key_states = apply_rotary_pos_emb(query_states, key_states, cos, sin)

        if past_key_value is not None:
            # sin and cos are specific to RoPE models; cache_position needed for the static cache
            cache_kwargs = {"sin": sin, "cos": cos, "cache_position": cache_position}
            key_states, value_states = past_key_value.update(key_states, value_states, self.layer_idx, cache_kwargs)

        # Note: Not need `repeat_kv` as in Eager or SPDA. NPU FA handles MQA/GQA operator simimlar to FlashAttention-2

        causal_mask = attention_mask
        if attention_mask is not None:
            causal_mask = causal_mask[:, :, :, : key_states.shape[-2]]

        query_states = query_states.contiguous()
        key_states = key_states.contiguous()
        value_states = value_states.contiguous()

        dropout_p = self.attention_dropout if self.training else 0.0
        attn_output = torch_npu.npu_fusion_attention(
            query_states,
            key_states,
            value_states,
            self.num_heads,
            input_layout="BNSD",
            pse=None,
            atten_mask=causal_mask.bool(),
            scale=self.scale_value,
            pre_tockens=2147483647,
            next_tockens=2147483647,
            keep_prob=1 - dropout_p,
            inner_precise=0,
        )[0]

        attn_output = attn_output.transpose(1, 2).contiguous()

        attn_output = attn_output.view(bsz, q_len, -1)
        attn_output = self.o_proj(attn_output)

        return attn_output, None, past_key_value
