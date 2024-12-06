# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

"""Medusa model to support medusa decoding."""

from modelopt.torch.opt.dynamic import DynamicModule


class MedusaModel(DynamicModule):
    """Base Medusa Model."""

    def _setup(self):
        self._register_temp_attribute("medusa_num_heads", 0)
        self._register_temp_attribute("medusa_num_layers", 0)
        self._register_temp_attribute("medusa_heads", None)

    def modify(self, medusa_num_heads=0, medusa_num_layers=0):
        """Base Medusa Model modify function. Child class should implement the details."""
        self.medusa_num_heads = medusa_num_heads
        self.medusa_num_layers = medusa_num_layers
