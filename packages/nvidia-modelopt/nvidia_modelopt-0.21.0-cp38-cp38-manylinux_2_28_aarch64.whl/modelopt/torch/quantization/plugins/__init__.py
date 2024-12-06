# SPDX-FileCopyrightText: Copyright (c) 2023 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

"""Handles quantization plugins to correctly quantize third-party modules.

Please check out the source code of this module for examples of how plugins work and how you can
write your own one. Currently, we support plugins for

- :meth:`apex<modelopt.torch.quantization.plugins.apex>`
- :meth:`diffusers<modelopt.torch.quantization.plugins.diffusers>`
- :meth:`huggingface<modelopt.torch.quantization.plugins.huggingface>`
- :meth:`megatron<modelopt.torch.quantization.plugins.megatron>`
- :meth:`nemo<modelopt.torch.quantization.plugins.nemo>`
- :meth:`fairscale<modelopt.torch.quantization.plugins.fairscale>`
- :meth:`peft<modelopt.torch.quantization.plugins.peft>`
"""

from modelopt.torch.utils import import_plugin

with import_plugin("apex"):
    from .apex import *

with import_plugin("diffusers"):
    from .diffusers import *

with import_plugin("huggingface"):
    from .huggingface import *

with import_plugin("megatron"):
    from .megatron import *

with import_plugin("nemo"):
    from .nemo import *

with import_plugin("fairscale"):
    from .fairscale import *

with import_plugin("peft"):
    from .peft import *
