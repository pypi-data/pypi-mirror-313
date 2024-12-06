# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.
"""Eagle conversion/restore utilities."""

from torch import nn

from modelopt.torch.opt.conversion import ModelLikeModule
from modelopt.torch.opt.dynamic import _DMRegistryCls
from modelopt.torch.opt.mode import ConvertReturnType, MetadataDict

from ..config import EagleConfig

EagleDMRegistry = _DMRegistryCls(prefix="Eagle")  # global instance for the registry


def convert_to_eagle_model(model: nn.Module, config: EagleConfig) -> ConvertReturnType:
    """Convert the model to a eagle model as per `config`."""
    # initialize the true module if necessary
    model = model.init_modellike() if isinstance(model, ModelLikeModule) else model

    original_cls = type(model)
    if original_cls not in EagleDMRegistry:
        for cls in EagleDMRegistry._registry:
            if issubclass(original_cls, cls):
                EagleDMRegistry.register({original_cls: "base_model_class"})(EagleDMRegistry[cls])
                break

    eagle_model = EagleDMRegistry.convert(model)
    eagle_model.modify(eagle_num_layers=config.eagle_num_layers)

    # no metadata, all specifed via config.
    metadata = {}

    return eagle_model, metadata


def restore_eagle_model(model: nn.Module, config: EagleConfig, metadata: MetadataDict) -> nn.Module:
    """Function for restoring a previously convert model to a eagle model."""
    # the metadata should be empty
    assert not metadata, "No metadata expected!"

    return convert_to_eagle_model(model, config)[0]
