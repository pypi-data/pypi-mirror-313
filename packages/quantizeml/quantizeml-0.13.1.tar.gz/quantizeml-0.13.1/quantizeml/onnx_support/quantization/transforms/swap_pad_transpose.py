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

__all__ = ["swap_pad_transpose"]


import numpy as np
import onnx

from ...graph_tools import get_field
from ..model import ONNXModel


def _find_pad_transpose_sequence(model):
    # Finds and returns sublists of nodes in the model that match
    # (Pad, Transpose) patterns.
    node_patterns = []

    for node in model.nodes():
        node_outbounds = model.get_children(node)

        if node.op_type == "Pad" and len(node_outbounds) == 1:
            outbound = node_outbounds[0]
            if outbound.op_type == "Transpose":
                node_patterns.append([node, outbound])

    return node_patterns


def swap_pad_transpose(model):
    """Swaps Pad and Transpose nodes.

    Args:
        model (ONNXModel): The ONNX model to be processed.
    """

    assert isinstance(model, ONNXModel)

    pad_transpose_sequences = _find_pad_transpose_sequence(model)

    if len(pad_transpose_sequences) == 0:
        return

    for pad_node, tranpose_node in pad_transpose_sequences:
        # Compute number of dimensions to set the default value for perm
        transpose_input_vi = model.find_value_info_by_name(tranpose_node.input[0])
        dims = list(range(len(transpose_input_vi.type.tensor_type.shape.dim)))

        # Default value is the number of dimensions reversed
        perm = get_field(tranpose_node, "perm", dims[::-1])
        try:
            # Pad axes is at the 4th position
            pad_axes = model.get_variable(pad_node.input[3])
            pad_axes_tp = model.get_initializer(pad_node.input[3])

            # Map pad axes to their respective indices in the perm list
            updated_pad_axes = [perm.index(x) for x in pad_axes]
            pad_axes_tp.CopyFrom(onnx.numpy_helper.from_array(
                np.array(updated_pad_axes, pad_axes.dtype), pad_node.input[3]))

        # Catch IndexError when there is no fourth input and an AssertionError when it is empty
        # This case represents Pad without pad axes
        except (IndexError, AssertionError):
            pads = model.get_variable(pad_node.input[1])
            pads_tp = model.get_initializer(pad_node.input[1])

            # As pads have len(perm) * 2 positions, we construct the same
            # perm for the remaining pads positions
            perm_to_apply = perm + [(i + len(perm)) for i in perm]

            # Update pads
            updated_pads = [pads[i] for i in perm_to_apply]
            pads_tp.CopyFrom(onnx.numpy_helper.from_array(
                np.array(updated_pads, pads.dtype), pad_node.input[1]))

        # Update intermediate value_info shape which is the output of the pad node.
        # After the swap, it will be the output of the transpose node, so perm is
        # applied to the pad input value info
        value_info_to_update = model.find_value_info_by_name(pad_node.output[0])
        pad_input_vi = model.find_value_info_by_name(pad_node.input[0])
        updated_dims = [pad_input_vi.type.tensor_type.shape.dim[i] for i in perm]
        value_info_to_update.type.tensor_type.shape.CopyFrom(
            onnx.TensorShapeProto(dim=updated_dims))

        # Switch nodes inputs/outputs
        tranpose_node.input[0], pad_node.input[0] = pad_node.input[0], tranpose_node.input[0]
        tranpose_node.output[0], pad_node.output[0] = pad_node.output[0], tranpose_node.output[0]

    # As we swap nodes, we need to topologically sort the model
    model.topological_sort()
    model.check_model()
