#!/usr/bin/env python
# ******************************************************************************
# Copyright 2023 Brainchip Holdings Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ******************************************************************************
__all__ = ['sanitize']

import os
import tempfile
import onnx
from pathlib import Path

from onnxruntime.quantization.shape_inference import quant_pre_process

from .convert_avg_to_gap import convert_avg_to_gap
from .convert_conv_to_gemm import convert_conv_to_gemm
from .convert_even_to_odd_kernel import convert_even_to_odd_kernel
from .convert_matmul_to_gemm import convert_matmul_to_gemm
from .convert_min_max_to_clip import convert_min_max_to_clip
from .convert_resize_to_depthwise_transpose import convert_resize_to_depthwise_transpose
from .fuse_relu_clip_nodes import fuse_relu_clip_nodes
from .insert_rescaling import insert_rescaling
from .remove_pad_nodes import fold_pad_into_conv
from .remove_reshape import remove_reshape
from .squeeze_reshape_to_flatten import convert_squeeze_reshape_to_flatten
from .split_concat_nodes import split_concat_nodes
from .swap_pad_transpose import swap_pad_transpose
from .untranspose_gemm_weights import untranspose_gemm_weights
from ..model import ONNXModel


def sanitize(model):
    """Sanitize a model preparing it for quantization.

    This is a wrapping successive calls to several model transformations
    which aims at making the model quantization ready.

    Args:
        model: the input model

    Returns:
        the sanitized model
    """
    assert isinstance(model, ONNXModel)

    # Clone model to prevent modification of the original one
    model = model.clone()

    # Replace operations to match with current ONNX version
    model.update_model_version()

    # Clean inputs/outputs
    model.clean_graph_io()

    # Perform optimization only if model is not quantized
    if not any(node.domain == "com.brainchip" for node in model.nodes()):
        with tempfile.TemporaryDirectory(prefix="pre.quant.") as quant_tmp_dir:
            # To perfom ONNXRuntime optimization, we would like to use
            # onnxruntime.quantization.quant_pre_process, to optimize the model (when required)
            # and infer the intermediate shapes.
            # However, it always expects to read the model from a path. That is why we
            # save the input model if it is not a path.
            tmp_model_path = os.path.join(quant_tmp_dir, "model.onnx")
            model.save_model_to_file(tmp_model_path)

            # We employ onnxruntime preprocessing to deduce shapes and implement optimization.
            # There exists an issue in onnxruntime related to the Constant Node
            # when it comes to shape computation using symbolic_shape_inference.
            # The problem arises when attempting to access the value of the constant
            # node attribute, but this node possesses other distinct attribute values
            # (refer to https://onnx.ai/onnx/operators/onnx__Constant.html#constant-13).
            # To resolve this, we bypass the symbolic shape inference and apply first
            # an optimization that folds these constants, and then apply by shape inference.
            quant_pre_process(tmp_model_path, tmp_model_path, skip_symbolic_shape=True)
            quant_pre_process(tmp_model_path, tmp_model_path)

            # Load the model
            model = ONNXModel(onnx.load_model(Path(tmp_model_path)))

    # Swaps Pad and Transpose nodes when possible
    swap_pad_transpose(model)

    # Adds a Rescaling node to the model
    insert_rescaling(model)

    # Converts Resize nodes to DepthwiseConv2DTranpose when possible
    convert_resize_to_depthwise_transpose(model)

    # Retranspose Gemm weights if they are transposed
    untranspose_gemm_weights(model)

    # Convert Squeeze/Reshape into Flatten when possible
    convert_squeeze_reshape_to_flatten(model)

    # Convert Min/Max into Clip
    convert_min_max_to_clip(model)

    # Remove pointless reshape nodes
    remove_reshape(model)

    # Fold pad into conv when possible
    fold_pad_into_conv(model)

    # Convert even to odd kernel for convolutional nodes when possible
    convert_even_to_odd_kernel(model)

    # Convert AveragePool to GAP when possible
    convert_avg_to_gap(model)

    # Convert Matmul to Gemm
    convert_matmul_to_gemm(model)

    # Convert Conv to Gemm when possible
    convert_conv_to_gemm(model)

    # Fuses ReLU/Clip nodes
    fuse_relu_clip_nodes(model)

    # Split Concat nodes into multiple Concats with exactly two inputs when possible
    split_concat_nodes(model)

    return model
