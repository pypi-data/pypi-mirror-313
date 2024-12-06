# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

"""Redrafter model to support redrafter decoding."""

from modelopt.torch.opt.dynamic import DynamicModule


class RedrafterModel(DynamicModule):
    """Base Redrafter Model."""

    def _setup(self):
        self._register_temp_attribute("redrafter_predict_n_tokens", 0)
        self._register_temp_attribute("redrafter_num_layers", 0)
        self._register_temp_attribute("drafter", None)

    def modify(self, redrafter_predict_n_tokens=0, redrafter_num_layers=0):
        """Base Redrafter Model modify function. Child class should implement the details."""
        self.redrafter_predict_n_tokens = redrafter_predict_n_tokens
        self.redrafter_num_layers = redrafter_num_layers
