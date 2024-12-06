# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

"""This module contains TensorRT utils."""

import ctypes
import platform
from typing import List, Optional, Tuple

import numpy as np
import onnx
import onnx_graphsurgeon as gs

try:
    import tensorrt as trt

    TRT_PYTHON_AVAILABLE = True
except ImportError:
    TRT_PYTHON_AVAILABLE = False


def get_custom_layers(onnx_path: str, trt_plugins: Optional[str]) -> List[str]:
    """Gets custom layers in ONNX model.

    Args:
        onnx_path: Path to the input ONNX model.
        trt_plugins: Paths to custom TensorRT plugins.

    Returns:
        List of custom layers.
    """
    # Initialize TensorRT plugins
    if trt_plugins is not None:
        trt_plugins = trt_plugins.split(";")
        for plugin in trt_plugins:
            ctypes.CDLL(plugin)

    # Create builder and network
    trt_logger = trt.Logger(trt.Logger.WARNING)
    trt.init_libnvinfer_plugins(trt_logger, "")
    builder = trt.Builder(trt_logger)
    network = builder.create_network()

    # Parse ONNX file
    parser = trt.OnnxParser(network, trt_logger)
    with open(onnx_path, "rb") as model:
        if not parser.parse(model.read()):
            error_str = [str(parser.get_error(error)) for error in range(parser.num_errors)]
            raise Exception(f"Failed to parse ONNX file: {''.join(error_str)}")

    # Obtain plugin layer names
    custom_layers = []
    for layer_idx in range(network.num_layers):
        layer = network.get_layer(layer_idx)
        if "PLUGIN" in str(layer.type):
            custom_layers.append(layer.name)

    return custom_layers


def load_onnx_model(
    onnx_path: str, trt_plugins: Optional[str] = None, use_external_data_format: bool = False
) -> Tuple[onnx.onnx_pb.ModelProto, bool, List[str]]:
    """Load ONNX model. If 'tensorrt' is installed, check if the model has custom ops and ensure it's supported by ORT.

    Args:
        onnx_path: Path to the input ONNX model.
        trt_plugins: Paths to custom TensorRT plugins.
        use_external_data_format: If True, separate data path will be used to store the weights of the quantized model.

    Returns:
        Loaded ONNX model supported by ORT.
        Boolean indicating whether the model has custom ops or not.
        List of custom ops in the ONNX model.
    """
    custom_ops = []
    has_custom_op = False

    # Load the model and weights
    onnx_model = onnx.load(onnx_path, load_external_data=use_external_data_format)

    if TRT_PYTHON_AVAILABLE and platform.system() != "Windows":
        # Check if there's a custom TensorRT op in the ONNX model. If so, make it ORT compatible by adding
        #   `trt.plugins to the ONNX graph.
        trt_plugin_domain = "trt.plugins"
        trt_plugin_version = 1

        custom_layers = get_custom_layers(onnx_path, trt_plugins)
        has_custom_op = True if custom_layers else False

        if has_custom_op:
            graph = gs.import_onnx(onnx_model)
            for node in graph.nodes:
                if node.name in custom_layers:
                    custom_ops.append(node.op)
                    node.domain = trt_plugin_domain
            custom_ops = np.unique(custom_ops)

            # TODO: Add type and shape inference.
            onnx_model = gs.export_onnx(graph)
            onnx_model.opset_import.append(
                onnx.helper.make_opsetid(trt_plugin_domain, trt_plugin_version)
            )

    return onnx_model, has_custom_op, custom_ops
