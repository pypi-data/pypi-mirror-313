# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

"""Handles plugins for third-party modules."""

from modelopt.torch.utils import import_plugin

from .huggingface import *

with import_plugin("megatron core dist checkpointing"):
    from .mcore_dist_checkpointing import *

with import_plugin("transformers"):
    from .transformers import *

with import_plugin("diffusers"):
    from .diffusers import *

with import_plugin("peft"):
    from .peft import *
