# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.
"""Implements NVFP4 quantization for efficient tensor storage and computation."""

from typing import List, Optional

import torch

from modelopt.torch.quantization.qtensor.base_qtensor import BaseQuantizedTensor

__all__ = ["NVFP4QTensor"]


class NVFP4QTensor(BaseQuantizedTensor):
    """Not implemented."""

    @classmethod
    def resmooth_weights_and_get_scales(
        cls,
        merged_weights: torch.Tensor,
        pre_quant_scales: List[torch.Tensor],
        ranks: int,
        group_size: int,
        avg_pre_quant_scale: torch.Tensor = None,
    ):
        """Not implemented."""
        raise NotImplementedError()

    @classmethod
    def get_weights_scaling_factor(
        cls,
        input: torch.Tensor,
        block_size: int,
        weights_scaling_factor_2: Optional[torch.Tensor] = None,
        keep_high_precision: bool = False,
    ):
        """Not implemented."""
        raise NotImplementedError()

    @classmethod
    def get_weights_scaling_factor_2(cls, input: torch.Tensor):
        """Not implemented."""
        raise NotImplementedError()

    @classmethod
    def get_activation_scaling_factor(cls, quantizer):
        """Not implemented."""
        raise NotImplementedError()

    @staticmethod
    def _cast_fp4(weight: torch.Tensor):
        """Not implemented."""
        raise NotImplementedError()

    @classmethod
    def quantize(
        cls,
        input: torch.Tensor,
        block_size: int,
        weights_scaling_factor: Optional[torch.Tensor] = None,
        weights_scaling_factor_2: Optional[torch.Tensor] = None,
        keep_high_precision: bool = False,
    ):
        """Not implemented."""
        raise NotImplementedError()

    def dequantize(self, dtype: torch.dtype = torch.float16, **kwarg):
        """Not implemented."""
        raise NotImplementedError()
