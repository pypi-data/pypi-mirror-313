# SPDX-FileCopyrightText: Copyright (c) 2023 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

"""Provides basic calibration utils."""

import struct
from typing import Dict, List, Union

import numpy as np
import onnx
from onnxruntime.quantization.calibrate import CalibrationDataReader

from modelopt.onnx.utils import (
    gen_random_inputs,
    get_input_names,
    get_input_shapes,
    parse_shapes_spec,
)

CalibrationDataType = Union[np.ndarray, Dict[str, np.ndarray]]


class CalibrationDataProvider(CalibrationDataReader):
    """Calibration data provider class."""

    def __init__(
        self, onnx_path: str, calibration_data: CalibrationDataType, calibration_shapes: str = None
    ):
        """Intializes the data provider class with the calibration data iterator.

        Args:
            onnx_path: Path to the ONNX model.
            calibration_data: Numpy data to calibrate the model.
                Ex. If a model has input shapes like {"sample": (2, 4, 64, 64), "timestep": (1,),
                "encoder_hidden_states": (2, 16, 768)}, the calibration data should have dictionary
                of tensors with shapes like {"sample": (1024, 4, 64, 64), "timestep": (512,),
                "encoder_hidden_states": (1024, 16, 768)} to calibrate with 512 samples.
        """
        onnx_model = onnx.load(onnx_path)
        input_names = get_input_names(onnx_model)
        if calibration_shapes:
            input_shapes = parse_shapes_spec(calibration_shapes)
        else:
            input_shapes = get_input_shapes(onnx_model)

        # Validate calibration data against expected inputs by the model
        if isinstance(calibration_data, np.ndarray):
            assert len(input_names) == 1, "Calibration data has only one tensor."
            calibration_data = {input_names[0]: calibration_data}
        elif isinstance(calibration_data, dict):
            assert len(input_names) == len(
                calibration_data
            ), "Model input count and calibration data doesn't match."
            for input_name in input_names:
                assert input_name in calibration_data
        else:
            raise ValueError(
                f"calibration data must be numpy array or dict, got {type(calibration_data)}"
            )

        # Create list of model inputs with appropriate batch size
        # So that we can create an input iterator
        n_itr = int(calibration_data[input_names[0]].shape[0] / input_shapes[input_names[0]][0])
        calibration_data_list = [{}] * n_itr
        for input_name in input_names:
            for idx, calib_data in enumerate(
                np.array_split(calibration_data[input_name], n_itr, axis=0)
            ):
                calibration_data_list[idx][input_name] = calib_data

        self.calibration_data_reader = iter(calibration_data_list)

    def get_next(self):
        """Returns the next available calibration input from the reader."""
        return next(self.calibration_data_reader, None)


class RandomDataProvider(CalibrationDataReader):
    """Calibration data reader class with random data provider."""

    def __init__(
        self, onnx_model: Union[str, onnx.onnx_pb.ModelProto], calibration_shapes: str = None
    ):
        """Initializes the data reader class with random calibration data."""
        if isinstance(onnx_model, str):
            onnx_path = onnx_model
            onnx_model = onnx.load(onnx_path)
        calibration_data_list: List[Dict[str, np.ndarray]] = [
            gen_random_inputs(onnx_model, calibration_shapes)
        ]
        self.calibration_data_reader = iter(calibration_data_list)

    def get_next(self):
        """Returns the next available calibration input from the reader."""
        return next(self.calibration_data_reader, None)


def import_scales_from_calib_cache(cache_path: str) -> Dict[str, float]:
    """Reads TensorRT calibration cache and returns as dictionary.

    Args:
        cache_path: Calibration cache path.

    Returns:
        Dictionary with scales in the format {tensor_name: float_scale}.
    """
    with open(cache_path, "r") as f:
        scales_dict = {}
        lines = f.readlines()
        for i, line in enumerate(lines):
            if i > 0:  # Skips the first line (i.e., TRT-8501-EntropyCalibration2)
                layer_name, hex_value = line.replace("\n", "").split(": ")
                try:
                    scale = struct.unpack("!f", bytes.fromhex(hex_value))[0]
                    scales_dict[layer_name + "_scale"] = scale
                except Exception:
                    raise ValueError(f"Scale value for tensor {layer_name} was not found!")

        return scales_dict
