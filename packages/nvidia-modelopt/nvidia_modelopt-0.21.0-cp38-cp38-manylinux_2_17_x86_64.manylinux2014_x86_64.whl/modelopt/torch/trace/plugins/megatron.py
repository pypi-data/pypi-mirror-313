# SPDX-FileCopyrightText: Copyright (c) 2023 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

"""Plugins for tracing Megatron modules."""

from megatron.core.models.gpt import GPTModel

from ..symbols import Symbol, SymInfo, SymMap


# NOTE: No need to register symbols for VocabParallelEmbedding, SelfAttention, MLP, LayerNorm, Row/Col Parallel Linear,
# etc. as they are not traced and manually handled in the _DynamicGPTModel class
@SymMap.register(GPTModel)
def get_megatron_gpt_model_sym_info(mod: GPTModel) -> SymInfo:
    """Get symbol information for ``GPTModel`` layers."""
    hidden_size = Symbol(is_searchable=True)
    return SymInfo(is_shape_preserving=True, hidden_size=hidden_size)
