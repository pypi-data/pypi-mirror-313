# SPDX-FileCopyrightText: Copyright (c) 2023 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

"""Plugins for pruning for Megatron-Core / NeMo modules using Minitron algorithm."""

# import nas plugin to check if it is enabled else raises an Exception
from modelopt.core.torch.nas.plugins.megatron import *  # noqa: F403

from ..config import MCoreGPTMinitronConfig

MCoreGPTMinitronConfig.register_default(
    {
        "megatron.core.models.gpt.GPTModel": {
            "hidden_size_divisor": 64,
            "num_heads_per_group_divisor": 1,
            "num_query_groups_divisor": 1,
            "ffn_hidden_size_divisor": 64,
        },
    }
)
