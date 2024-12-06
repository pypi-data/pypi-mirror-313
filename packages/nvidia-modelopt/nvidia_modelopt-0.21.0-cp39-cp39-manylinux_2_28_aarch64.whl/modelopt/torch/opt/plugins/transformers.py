# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.
"""ModelOpt plugin for enabling automatic save/restore of ModelOpt state for HuggingFace models."""

from transformers import PreTrainedModel

from .huggingface import patch_pretrained_methods

__all__ = []

patch_pretrained_methods(PreTrainedModel, "transformers")
