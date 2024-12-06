# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

"""Eagle model to support eagle decoding."""

from modelopt.torch.opt.dynamic import DynamicModule


class EagleModel(DynamicModule):
    """Base Eagle Model."""

    def _setup(self):
        self._register_temp_attribute("eagle_num_layers", 0)
        self._register_temp_attribute("eagle_module", None)

    def modify(self, eagle_num_layers):
        """Base Eagle Model modify function. Child class should implement the details."""
        self.eagle_num_layers = eagle_num_layers
