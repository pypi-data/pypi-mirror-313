#!/usr/bin/env python
# ******************************************************************************
# Copyright 2024 Brainchip Holdings Ltd.
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

__all__ = ["untranspose_gemm_weights"]

import onnx
import onnx.numpy_helper

from ...graph_tools import get_field, replace_field
from ..model import ONNXModel


def untranspose_gemm_weights(model):
    """Retransposes gemm weights if they are transposed.

    Args:
        model (ONNXModel): The ONNX model to be processed.
    """
    assert isinstance(model, ONNXModel)

    for node in model.nodes():
        if node.op_type == "Gemm":
            transB = get_field(node, "transB", -1)
            if transB in (-1, 0):
                # Transpose weights
                weights = model.get_variable(node.input[1])
                weights = weights.T

                # Update Tensor proto
                weights_tp = model.get_initializer(node.input[1])
                weights_tp.CopyFrom(onnx.numpy_helper.from_array(weights, node.input[1]))

                # Update or create attribute value
                if transB == -1:
                    node.attribute.append(onnx.helper.make_attribute(key="transB", value=1))
                else:
                    replace_field(node, "transB", 1)
    model.check_model()
