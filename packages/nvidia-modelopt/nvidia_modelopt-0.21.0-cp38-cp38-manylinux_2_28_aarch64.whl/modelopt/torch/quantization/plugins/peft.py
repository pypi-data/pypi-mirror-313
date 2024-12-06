# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

"""Support quantization for peft LoRA linear layers."""

import torch.nn.functional as F
from peft.tuners.lora.layer import Linear as LoraLinear

from modelopt.torch.opt.dynamic import DynamicModule

from ..nn import QuantModuleRegistry, TensorQuantizer

__all__ = []


@QuantModuleRegistry.register({LoraLinear: "LoraLinear"})
class _QuantLoraLinear(DynamicModule):
    def _setup(self):
        self.input_quantizer = TensorQuantizer()
        self.weight_quantizer = TensorQuantizer()
        self.output_quantizer = TensorQuantizer()

    def forward(self, x, *args, **kwargs):
        adapter_names = kwargs.pop("adapter_names", None)
        if self.disable_adapters or adapter_names is not None or self.merged:
            return super().forward(x, args, kwargs)

        weight = self.base_layer.weight
        for active_adapter in self.active_adapters:
            if active_adapter not in self.lora_A.keys():
                continue
            lora_a = self.lora_A[active_adapter]
            lora_b = self.lora_B[active_adapter]
            scaling = self.scaling[active_adapter]

            if not self.use_dora[active_adapter]:
                weight = weight + scaling * lora_b.weight @ lora_a.weight
            else:
                raise NotImplementedError("dora not implemented")

        x = self.input_quantizer(x)
        weight = self.weight_quantizer(weight)
        output = self.output_quantizer(F.linear(x, weight, self.base_layer.bias))
        return output
