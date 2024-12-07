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

__all__ = ["fuse_relu_clip_nodes"]

import numpy as np
import onnx.helper
import onnx.numpy_helper

from ..model import ONNXModel


def _find_clip_relu_sequence(model):
    for node in model.nodes():
        node_outbounds = model.get_children(node)

        # Find candidate node and get the type of the next node if there is one
        if node.op_type in ("Clip", "Relu") and len(node_outbounds) == 1:
            outbound = node_outbounds[0]
            if outbound.op_type in ("Clip", "Relu"):
                return [node, outbound]
    return None


def _get_min_max_values(model, node):
    if node.op_type == "Relu":
        node_min = np.array(0.0, dtype=np.float32)
        node_max = np.array(np.inf, dtype=np.float32)
    else:
        # We add empty min/max if they are not present
        if len(node.input) == 1:
            node.input.extend(["", ""])
        elif len(node.input) == 2:
            node.input.append("")

        node_min = np.array(-np.inf, dtype=np.float32) if node.input[1] == "" \
            else model.get_variable(node.input[1])

        node_max = np.array(np.inf, dtype=np.float32) if node.input[2] == "" \
            else model.get_variable(node.input[2])

    return node_min, node_max


def _set_tensor_proto_value(model, node, value, suffix):
    tp_name = f"{node.input[0]}/{suffix}"
    new_node_tp = onnx.numpy_helper.from_array(value, tp_name)
    node_input_index = 1 if suffix == "min" else 2

    if (node_tp := model.get_initializer(tp_name)) is not None:
        # update tensor proto
        node_tp.CopyFrom(new_node_tp)
    else:
        # Create new tensor proto
        model.initializer().append(new_node_tp)

    node.input[node_input_index] = tp_name


def fuse_relu_clip_nodes(model):
    """Fuses successives Clip/ReLU nodes

    Args:
        model (ONNXModel): The ONNX model to be processed.
    """
    assert isinstance(model, ONNXModel)

    # We consider successively the following sequences of nodes:
    # Clip > Clip or Clip > ReLU or ReLU > Clip or ReLU > ReLU
    while True:
        # Find Clip/ReLU sequences
        sequence = _find_clip_relu_sequence(model)

        if sequence is None:
            break  # No more sequence

        # find min max of each node of the sequence
        min1, max1 = _get_min_max_values(model, sequence[0])
        min2, max2 = _get_min_max_values(model, sequence[1])

        # compute new min max values
        new_min = np.maximum(min1, min2)
        new_max = np.minimum(max1, max2)

        # create new node
        # In case both nodes are ReLUs, we create a ReLU node
        if sequence[0].op_type == "Relu" and sequence[1].op_type == "Relu":
            new_node = onnx.helper.make_node("Relu", inputs=sequence[0].input,
                                             outputs=sequence[1].output)
        else:
            new_node = onnx.helper.make_node("Clip", inputs=[sequence[0].input[0], "", ""],
                                             outputs=sequence[1].output)

            if not np.isinf(new_min):
                _set_tensor_proto_value(model, new_node, new_min, "min")

            if not np.isinf(new_max):
                _set_tensor_proto_value(model, new_node, new_max, "max")

        # Remove Unused value_info which is the output of the first node of the sequence
        value_info_to_remove = model.find_value_info_by_name(sequence[0].output[0])
        model.graph().value_info.remove(value_info_to_remove)

        # Remove the sequence and add the new node
        model.remove_nodes(sequence)
        model.add_node(new_node)

    # As we add new nodes, we need to topologically sort the model graph
    model.topological_sort()
    model.clean_initializers()
    model.check_model()
