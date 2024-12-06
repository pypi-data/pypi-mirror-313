# SPDX-FileCopyrightText: Copyright (c) 2023 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

"""Nvidia TensorRT Model Optimizer (modelopt)."""

import sys as _sys
import warnings as _warnings
from importlib.metadata import version as _version

if _sys.version_info < (3, 9):
    _warnings.warn(
        "nvidia-modelopt will drop Python 3.8 support in next release.", DeprecationWarning
    )

__version__ = _version("nvidia-modelopt")
