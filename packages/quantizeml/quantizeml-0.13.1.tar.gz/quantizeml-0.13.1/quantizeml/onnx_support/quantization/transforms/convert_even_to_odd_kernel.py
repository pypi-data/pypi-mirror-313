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
"""
Sanitize to convert kernel shapes from even to odd in convolutional nodes.
"""

__all__ = ['convert_even_to_odd_kernel']


import numpy as np
import onnx

from ...graph_tools import get_field, get_tensor_shape, has_field, replace_field
from ...layers import check_conv_depthwise_compatibility
from ..model import ONNXModel
from .utils import compute_conv_same_pads


def convert_even_to_odd_kernel(model):
    """Adjusts kernel shapes from even to odd for convolutional nodes.

    Args:
        model (ONNXModel): The ONNX model to be processed.
    """
    assert isinstance(model, ONNXModel)

    target_nodes_data = _find_target_nodes(model)

    # When there are no valid candidates, return the original model
    if len(target_nodes_data) == 0:
        return

    for node_data in target_nodes_data:
        _update_node_data(model, node_data)


def _find_target_nodes(model):
    def is_same_padding(input_shape, kernel_shape, strides, pads):
        return pads == compute_conv_same_pads(input_shape, kernel_shape, strides)

    def is_valid_attributes(input_shape, kernel_shape, strides, pads):
        stride_1_cond = strides[0] == 1 and kernel_shape[0] in (2, 4, 6)
        stride_2_cond = strides[0] == 2 and kernel_shape[0] == 2

        return (stride_1_cond or stride_2_cond) and is_same_padding(input_shape[2:], kernel_shape,
                                                                    strides, pads)

    skippable_nodes = ("Mul", "Add", "Transpose")
    target_nodes_data = []

    for node in model.nodes():
        if node.op_type == "Conv":
            supported = False
            try:
                check_conv_depthwise_compatibility(node, model.graph())
                # No constraints on Depthwise nodes
                supported = True
            except RuntimeError:
                # For Conv nodes, we skip the first Conv that is attached to
                # ("Transpose", Mul, "Add")
                inbound = model.get_parent(node, idx=0)
                # Inbound is None means that Conv is the first node
                while inbound is not None:
                    if inbound.op_type not in skippable_nodes:
                        supported = True
                        break
                    inbound = model.get_parent(inbound, idx=0)
            except Exception:
                # Continue if the node is not a depthwiseConv or a standard convolution with group=1
                continue

            if supported:
                input_shape = get_tensor_shape(model.find_value_info_by_name(node.input[0]))
                weights = model.get_variable(node.input[1])
                kernel_shape = get_field(node, "kernel_shape", weights.shape[2:])
                strides = get_field(node, "strides", [1, 1])
                pads = get_field(node, "pads", [0, 0, 0, 0])

                if is_valid_attributes(input_shape, kernel_shape, strides, pads):
                    target_nodes_data.append({
                        "node": node,
                        "input_shape": input_shape,
                        "kernel_shape": kernel_shape,
                        "strides": strides,
                        "pads": pads,
                    })

    return target_nodes_data


def _compute_slice_offsets(node_data):
    stride = node_data["strides"][0]
    height, width = node_data["input_shape"][2:]
    kernel_shape = node_data["kernel_shape"][0]

    if stride == 1:
        col_start = 1
        row_start = 1
    elif stride == 2:
        col_start = height % 2
        row_start = width % 2

    col_end = col_start + kernel_shape
    row_end = row_start + kernel_shape

    return col_start, row_start, col_end, row_end


def _update_node_data(model, node_data):
    # Get weights variables and tensor proto
    weights = model.get_variable(node_data["node"].input[1])
    weights_tp = model.get_initializer(node_data["node"].input[1])

    # Increase kernel shape by 1 and construct new_weigths
    kernel_shape = node_data["kernel_shape"][0]
    updated_shape = (*weights.shape[:2], kernel_shape + 1, kernel_shape + 1)
    updated_kernel = np.zeros(updated_shape, dtype=weights.dtype)

    # Compute placement of the original kernel in the new kernel
    col_start, row_start, col_end, row_end = _compute_slice_offsets(node_data)
    # Shape of kernel is (F, C, Kh, Kw)
    updated_kernel[:, :, col_start:col_end, row_start:row_end] = weights

    # Update weights
    weights_tp.CopyFrom(onnx.numpy_helper.from_array(updated_kernel, node_data["node"].input[1]))

    # Update kernel_shape attribute if it exists
    if has_field(node_data["node"], "kernel_shape"):
        replace_field(node_data["node"], "kernel_shape", (kernel_shape + 1, kernel_shape + 1))

    # Update pads to keep same padding with the updated kernel shape
    updated_pads = compute_conv_same_pads(node_data["input_shape"][2:],
                                          (kernel_shape + 1, kernel_shape + 1),
                                          node_data["strides"])
    if has_field(node_data["node"], "pads"):
        replace_field(node_data["node"], "pads", updated_pads)
    else:
        node_data["node"].attribute.append(
            onnx.helper.make_attribute(key="pads", value=updated_pads))
