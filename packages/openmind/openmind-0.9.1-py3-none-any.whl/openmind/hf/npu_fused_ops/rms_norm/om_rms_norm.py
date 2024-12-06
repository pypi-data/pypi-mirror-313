#  Copyright (c) Huawei Technologies Co., Ltd. 2024-2024. All rights reserved.
#
# 2024.11.05 - Adapt to openmind.
#              Huawei Technologies Co., Ltd.
# Copyright (c) 2023 toshiaki1729
# copyright (C) 2007 Free Software Foundation; Inc. <https: fsf.org >
# Licensed under the MIT License
# some modules/classes are copied and modified from https://github.com/mcmonkey4eva/sd3-ref
# the original code is licensed under the MIT License

# and some module/classes are contributed from KohakuBlueleaf. Thanks for the contribution!


import torch

from torch import nn

try:
    import torch_npu
except ImportError:
    pass


from ....utils import is_torch_npu_available, logging

logger = logging.get_logger()

NPU_AVAILABLE = is_torch_npu_available()


class OmNpuRMSNorm(nn.Module):
    """
    RMSNorm operator adapted for NPU. When NPU is available and the user chooses to enable OmNpuRMSNorm, it will be opened.
    Otherwise, the native implementation will still be used
    """

    def __init__(self, hidden_size, eps=1e-6):
        """

        Initialize the RMSNorm normalization layer.

        Args:
            dim (int): The dimension of the input tensor.
            eps (float, optional): A small value added to the denominator for numerical stability. Default is 1e-6.

        Attributes:
            eps (float): A small value added to the denominator for numerical stability.
            weight (nn.Parameter): Learnable scaling parameter.

        """

        logger.warning_once(
            "If torch_npu is available, this model will using torch npu fused RMSNorm, "
            "instead of the built-in RMSNorm."
        )
        super().__init__()
        self.weight = nn.Parameter(torch.ones(hidden_size))
        self.variance_epsilon = eps

    def forward(self, hidden_states):
        """
        Forward pass through the RMSNorm layer.

        Args:
            x (torch.Tensor): The input tensor.

        Returns:
            torch.Tensor: The output tensor after applying RMSNorm.

        """
        if NPU_AVAILABLE:
            logger.warning_once("The model is using  torch npu fused RMSNorm.")
            return torch_npu.npu_rms_norm(hidden_states, self.weight, epsilon=self.variance_epsilon)[0]
        else:
            input_dtype = hidden_states.dtype
            hidden_states = hidden_states.to(torch.float32)
            variance = hidden_states.pow(2).mean(-1, keepdim=True)
            hidden_states = hidden_states * torch.rsqrt(variance + self.variance_epsilon)
            return self.weight * hidden_states.to(input_dtype)

    def extra_repr(self):
        return f"{tuple(self.weight.shape)}, eps={self.variance_epsilon}"
