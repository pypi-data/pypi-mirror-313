# SPDX-FileCopyrightText: Copyright (c) 2023 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

"""Utility functions for loading CPP / CUDA extensions."""

import os
import warnings
from pathlib import Path
from types import ModuleType
from typing import Any, List, Optional, Union

import torch
from packaging.specifiers import SpecifierSet
from packaging.version import Version
from torch.utils.cpp_extension import load

__all__ = ["load_cpp_extension"]


def load_cpp_extension(
    name: str,
    sources: List[Union[str, Path]],
    cuda_version_specifiers: Optional[str],
    fail_msg: str = "",
    raise_if_failed: bool = False,
    **load_kwargs: Any,
) -> Optional[ModuleType]:
    """Load a C++ / CUDA extension using torch.utils.cpp_extension.load() if the current CUDA version satisfies it.

    Loading first time may take a few mins because of the compilation, but subsequent loads are instantaneous.

    Args:
        name: Name of the extension.
        sources: Source files to compile.
        cuda_version_specifiers: Specifier (e.g. ">=11.8,<12") for CUDA versions required to enable the extension.
        fail_msg: Additional message to display if the extension fails to load.
        raise_if_failed: Raise an exception if the extension fails to load.
        **load_kwargs: Keyword arguments to torch.utils.cpp_extension.load().
    """
    ext = None
    print(f"Loading extension {name}...")

    if not os.environ.get("TORCH_CUDA_ARCH_LIST"):
        try:
            device_capability = torch.cuda.get_device_capability()
            os.environ["TORCH_CUDA_ARCH_LIST"] = f"{device_capability[0]}.{device_capability[1]}"
        except Exception:
            warnings.warn("GPU not detected. Please unset `TORCH_CUDA_ARCH_LIST` env variable.")

    if torch.version.cuda is None:
        fail_msg = f"Skipping extension {name} because CUDA is not available."
    elif cuda_version_specifiers and Version(torch.version.cuda) not in SpecifierSet(
        cuda_version_specifiers
    ):
        fail_msg = (
            f"Skipping extension {name} because the current CUDA version {torch.version.cuda}"
            f" does not satisfy the specifiers {cuda_version_specifiers}."
        )
    else:
        try:
            ext = load(name, sources, **load_kwargs)
        except Exception as e:
            if not fail_msg:
                fail_msg = f"Unable to load extension {name} and falling back to CPU version."
            fail_msg = f"{e}\n{fail_msg}"
            # RuntimeError can be raised if there are any errors while compiling the extension.
            # OSError can be raised if CUDA_HOME path is not set correctly.
            # subprocess.CalledProcessError can be raised on `-runtime` images where c++ is not installed.

    if ext is None:
        if raise_if_failed:
            raise RuntimeError(fail_msg)
        else:
            warnings.warn(fail_msg)
    return ext
