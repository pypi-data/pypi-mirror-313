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

__all__ = ["convert_matmul_to_gemm"]

import onnx.helper
import onnx.numpy_helper

from ..model import ONNXModel


def convert_matmul_to_gemm(model):
    """Converts Matmul node to a Gemm node.

    Args:
        model (ONNXModel): The ONNX model to be processed.
    """
    def _gemm_weight_from_matmul(matmul_node):
        # MatMul weights need to be transposed as in Gemm node we always
        # use transB=1
        matmul_weight = model.get_variable(matmul_node.input[1])
        matmul_weight = matmul_weight.T
        matmul_weight_tp = model.get_initializer(matmul_node.input[1])
        matmul_weight_tp.CopyFrom(onnx.numpy_helper.from_array(matmul_weight, matmul_node.input[1]))

    assert isinstance(model, ONNXModel)

    for node in model.nodes():
        if node.op_type == "MatMul":
            _gemm_weight_from_matmul(node)
            node.op_type = "Gemm"
            node.attribute.append(onnx.helper.make_attribute(key="transB", value=1))
    model.check_model()
