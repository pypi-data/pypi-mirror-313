# SPDX-FileCopyrightText: Copyright (c) 2023 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

"""Model optimization and deployment subpackage for torch."""

import warnings as _warnings

import torch
from packaging.version import Version

try:
    from . import distill, nas, opt, prune, quantization, sparsity, speculative, utils  # noqa: E402
except ImportError as e:
    raise ImportError("Please install optional ``[torch]`` dependencies.") from e

if Version(torch.__version__) < Version("2.1"):
    _warnings.warn(
        "nvidia-modelopt will drop torch 2.0 support in next release.", DeprecationWarning
    )

if torch.version.cuda and Version(torch.version.cuda) < Version("12.0"):
    _warnings.warn(
        "nvidia-modelopt will drop CUDA 11.x support in next release.", DeprecationWarning
    )
