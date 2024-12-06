# SPDX-FileCopyrightText: Copyright (c) 2023 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

"""Module to load C++ / CUDA extensions."""

from pathlib import Path

from modelopt.torch.utils import load_cpp_extension

__all__ = ["get_cuda_ext", "get_cuda_ext_fp8", "precompile"]

path = Path(__file__).parent


def get_cuda_ext(raise_if_failed: bool = False):
    """Returns the cuda extention for tensor_quant."""
    if not hasattr(get_cuda_ext, "extension"):
        get_cuda_ext.extension = load_cpp_extension(  # type:ignore[attr-defined]
            name="modelopt_cuda_ext",
            sources=[path / "src/tensor_quant.cpp", path / "src/tensor_quant_gpu.cu"],
            cuda_version_specifiers=">=11",
            raise_if_failed=raise_if_failed,
        )
    return get_cuda_ext.extension  # type:ignore[attr-defined]


def get_cuda_ext_fp8(raise_if_failed: bool = False):
    """Returns the cuda extention for tensor_quant_fp8."""
    if not hasattr(get_cuda_ext_fp8, "extension"):
        get_cuda_ext_fp8.extension = load_cpp_extension(  # type:ignore[attr-defined]
            name="modelopt_cuda_ext_fp8",
            sources=[path / "src/tensor_quant_fp8.cpp", path / "src/tensor_quant_gpu_fp8.cu"],
            cuda_version_specifiers=">=11.8",
            fail_msg=(
                "CUDA extension for FP8 quantization could not be built and loaded, FP8 simulated"
                " quantization will not be available."
            ),
            raise_if_failed=raise_if_failed,
        )
    return get_cuda_ext_fp8.extension  # type:ignore[attr-defined]


def __getattr__(name):
    if name == "cuda_ext":
        return get_cuda_ext()
    elif name == "cuda_ext_fp8":
        return get_cuda_ext_fp8()
    else:
        raise AttributeError(f"module {__name__} has no attribute {name}")


def precompile():
    """Precompile the CUDA extensions."""
    print(get_cuda_ext())
    print(get_cuda_ext_fp8())
