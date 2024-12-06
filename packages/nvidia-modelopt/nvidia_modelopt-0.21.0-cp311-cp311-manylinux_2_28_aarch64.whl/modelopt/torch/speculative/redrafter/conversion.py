# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.
"""Redrafter conversion/restore utilities."""

from torch import nn

from modelopt.torch.opt.conversion import ModelLikeModule
from modelopt.torch.opt.dynamic import _DMRegistryCls
from modelopt.torch.opt.mode import ConvertReturnType, MetadataDict

from ..config import RedrafterConfig

RedrafterDMRegistry = _DMRegistryCls(prefix="Redrafter")  # global instance for the registry


def convert_to_redrafter_model(model: nn.Module, config: RedrafterConfig) -> ConvertReturnType:
    """Convert the model to a redrafter model as per `config`."""
    # initialize the true module if necessary
    model = model.init_modellike() if isinstance(model, ModelLikeModule) else model

    original_cls = type(model)
    if original_cls not in RedrafterDMRegistry:
        for cls in RedrafterDMRegistry._registry:
            if issubclass(original_cls, cls):
                RedrafterDMRegistry.register({original_cls: "base_model_class"})(
                    RedrafterDMRegistry[cls]
                )
                break

    redrafter_model = RedrafterDMRegistry.convert(model)
    redrafter_model.modify(
        redrafter_predict_n_tokens=config.redrafter_predict_n_tokens,
        redrafter_num_layers=config.redrafter_num_layers,
    )

    # no metadata, all specifed via config.
    metadata = {}

    return redrafter_model, metadata


def restore_redrafter_model(
    model: nn.Module, config: RedrafterConfig, metadata: MetadataDict
) -> nn.Module:
    """Function for restoring a previously convert model to a redrafter model."""
    # the metadata should be empty
    assert not metadata, "No metadata expected!"

    return convert_to_redrafter_model(model, config)[0]
