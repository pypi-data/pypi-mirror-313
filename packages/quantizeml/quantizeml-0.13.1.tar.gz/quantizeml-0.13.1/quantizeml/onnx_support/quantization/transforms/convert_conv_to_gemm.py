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

__all__ = ["convert_conv_to_gemm"]

import numpy as np
import onnx
import onnx.helper
import onnx.numpy_helper

from ...graph_tools import check_node_attributes, get_tensor_shape
from ..model import ONNXModel


def _find_conv_reshape_or_squeeze_patterns(model):
    # Finds and returns sublists of nodes in the model that match
    # (Conv, Reshape) or (Conv, Squeeze) patterns.
    node_patterns = []

    for node in model.nodes():
        node_outbounds = model.get_children(node)

        if node.op_type == "Conv" and len(node_outbounds) == 1:
            outbound = node_outbounds[0]
            if outbound.op_type in ("Reshape", "Squeeze"):
                node_patterns.append([node, outbound])

    return node_patterns


def _check_reshape_or_squeeze_output_shape_2D(model, squeeze_or_reshape_node):
    squeeze_or_reshape_output_shape = get_tensor_shape(
        model.find_value_info_by_name(squeeze_or_reshape_node.output[0]))

    if len(squeeze_or_reshape_output_shape) != 2:
        raise ValueError(
            f"Expected a 2D shape for the output of the node '{squeeze_or_reshape_node.name}', "
            f"but got a shape with {len(squeeze_or_reshape_output_shape)} dimensions: "
            f"{squeeze_or_reshape_output_shape}."
        )


def convert_conv_to_gemm(model):
    """
    Transforms Conv + (Reshape/Squeeze) into Flatten + Gemm if both operation chains are compatible.

    Args:
        model (ONNXModel): The ONNX model to be processed.
    """
    def _gemm_weight_from_conv(conv_node):
        # squeezes the conv weight to be compatible with dense weights
        # and updates the tensor proto
        conv_weight = model.get_variable(conv_node.input[1])
        conv_weight = np.reshape(conv_weight, (conv_weight.shape[0], -1))
        conv_weight_tp = model.get_initializer(conv_node.input[1])
        conv_weight_tp.CopyFrom(onnx.numpy_helper.from_array(conv_weight, conv_node.input[1]))

    def _update_conv_output_shape(conv_node):
        # Flatten node output will have the same channels as conv_input
        # but with conv output name
        conv_input_vi = model.find_value_info_by_name(conv_node.input[0])
        conv_output_vi = model.find_value_info_by_name(conv_node.output[0])
        channels, height, width = conv_input_vi.type.tensor_type.shape.dim[1:]

        conv_output_vi.type.tensor_type.shape.dim[1].dim_value = channels.dim_value * \
            height.dim_value * width.dim_value

        # Remove the last 2 dims of conv output
        conv_output_vi.type.tensor_type.shape.dim.pop()
        conv_output_vi.type.tensor_type.shape.dim.pop()

    assert isinstance(model, ONNXModel)

    nodes_to_add = []
    nodes_to_remove = []

    node_patterns = _find_conv_reshape_or_squeeze_patterns(model)

    if len(node_patterns) == 0:
        return

    supported_attributes = {'strides': [[1, 1]], 'group': [1]}

    for node_pattern in node_patterns:
        conv_node, squeeze_or_reshape_node = node_pattern

        conv_input_shape = get_tensor_shape(model.find_value_info_by_name(conv_node.input[0]))
        supported_attributes.update({'kernel_shape': [list(conv_input_shape[-2:])],
                                     'pads': [[0] * len(conv_input_shape)]})

        try:
            _check_reshape_or_squeeze_output_shape_2D(model, squeeze_or_reshape_node)
            check_node_attributes(conv_node, supported_attributes)

        except ValueError:
            # We don't change the model when the node attributes
            # do not match the required constraints
            continue

        _gemm_weight_from_conv(conv_node)
        _update_conv_output_shape(conv_node)

        flatten_node = onnx.helper.make_node("Flatten",
                                             inputs=[conv_node.input[0]],
                                             outputs=conv_node.output
                                             )
        gemm_node = onnx.helper.make_node("Gemm",
                                          inputs=[flatten_node.output[0]] + conv_node.input[1:],
                                          outputs=squeeze_or_reshape_node.output,
                                          transB=1
                                          )

        nodes_to_add.extend([flatten_node, gemm_node])
        nodes_to_remove.extend(node_pattern)

    model.add_nodes(nodes_to_add)
    model.remove_nodes(nodes_to_remove)
    model.clean_initializers()

    # As we add new nodes, we need to topologically sort the model graph
    model.topological_sort()
    model.check_model()
