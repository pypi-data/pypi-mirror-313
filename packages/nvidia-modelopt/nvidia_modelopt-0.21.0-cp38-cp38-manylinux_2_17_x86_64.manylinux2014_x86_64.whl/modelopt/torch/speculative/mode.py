# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

"""This module contains the mode descriptor for the quantization mode."""

from typing import Type

from modelopt.torch.opt.config import ModeloptBaseConfig
from modelopt.torch.opt.mode import (
    ConvertEntrypoint,
    RestoreEntrypoint,
    _ModeDescriptor,
    _ModeRegistryCls,
)

from .config import EagleConfig, MedusaConfig, RedrafterConfig
from .eagle.conversion import convert_to_eagle_model, restore_eagle_model
from .medusa.conversion import convert_to_medusa_model, restore_medusa_model
from .redrafter.conversion import convert_to_redrafter_model, restore_redrafter_model

SpeculativeDecodingModeRegistry = _ModeRegistryCls()


@SpeculativeDecodingModeRegistry.register_mode
class MedusaModeDescriptor(_ModeDescriptor):
    """Class to describe the ``"medusa"`` mode.

    The properties of this mode can be inspected via the source code.
    """

    @property
    def name(self) -> str:
        """Returns the value (str representation) of the mode."""
        return "medusa"

    @property
    def config_class(self) -> Type[ModeloptBaseConfig]:
        """Specifies the config class for the mode."""
        return MedusaConfig

    @property
    def convert(self) -> ConvertEntrypoint:
        """The mode's entrypoint for converting a model."""
        return convert_to_medusa_model

    @property
    def restore(self) -> RestoreEntrypoint:
        """The mode's entrypoint for restoring a model."""
        return restore_medusa_model


@SpeculativeDecodingModeRegistry.register_mode
class EagleModeDescriptor(_ModeDescriptor):
    """Class to describe the ``"eagle"`` mode.

    The properties of this mode can be inspected via the source code.
    """

    @property
    def name(self) -> str:
        """Returns the value (str representation) of the mode."""
        return "eagle"

    @property
    def config_class(self) -> Type[ModeloptBaseConfig]:
        """Specifies the config class for the mode."""
        return EagleConfig

    @property
    def convert(self) -> ConvertEntrypoint:
        """The mode's entrypoint for converting a model."""
        return convert_to_eagle_model

    @property
    def restore(self) -> RestoreEntrypoint:
        """The mode's entrypoint for restoring a model."""
        return restore_eagle_model


@SpeculativeDecodingModeRegistry.register_mode
class RedrafterModeDescriptor(_ModeDescriptor):
    """Class to describe the ``"redrafter"`` mode.

    The properties of this mode can be inspected via the source code.
    """

    @property
    def name(self) -> str:
        """Returns the value (str representation) of the mode."""
        return "redrafter"

    @property
    def config_class(self) -> Type[ModeloptBaseConfig]:
        """Specifies the config class for the mode."""
        return RedrafterConfig

    @property
    def convert(self) -> ConvertEntrypoint:
        """The mode's entrypoint for converting a model."""
        return convert_to_redrafter_model

    @property
    def restore(self) -> RestoreEntrypoint:
        """The mode's entrypoint for restoring a model."""
        return restore_redrafter_model
