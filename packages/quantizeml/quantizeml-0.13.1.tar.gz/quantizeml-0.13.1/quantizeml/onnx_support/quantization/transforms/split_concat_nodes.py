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

__all__ = ["split_concat_nodes"]

import onnx.helper
import onnx.numpy_helper

from ..model import ONNXModel


def split_concat_nodes(model):
    """Splits Concat nodes with more than two inputs into multiple
    Concat nodes with exactly two inputs.

    Args:
        model (ONNXModel): The ONNX model to be processed.
    """

    assert isinstance(model, ONNXModel)

    concat_nodes = _find_concat_with_more_than_two_inputs(model)

    # Nothing to do when there are no valid candidates
    if len(concat_nodes) == 0:
        return

    _split_concat(model, concat_nodes)


def _find_concat_with_more_than_two_inputs(model):
    concat_nodes = []

    for node in model.nodes():
        if node.op_type == "Concat" and len(node.input) > 2:
            concat_nodes.append(node)

    return concat_nodes


def _split_concat(model, concat_nodes):
    nodes_to_remove = []
    nodes_to_add = []

    for concat_node in concat_nodes:
        num_inputs = len(concat_node.input)
        current_input = concat_node.input[0]
        base_name = concat_node.output[0]

        for i in range(1, num_inputs):
            # Name will be base_name for the last created Concat, for the others
            # it will be base_name_{second_inbound_node}
            new_name = base_name if i == num_inputs - 1 else f"{base_name}_{concat_node.input[i]}"
            # Create new Concat node where the two inbound nodes
            # are the current node and the next inbound node
            new_concat_node = onnx.helper.make_node("Concat",
                                                    inputs=[current_input, concat_node.input[i]],
                                                    outputs=[new_name],
                                                    axis=concat_node.attribute[0].i)

            # The current_input become the new_concat_node
            current_input = new_name
            nodes_to_add.append(new_concat_node)

        nodes_to_remove.append(concat_node)

    model.add_nodes(nodes_to_add)
    model.remove_nodes(nodes_to_remove)

    # As we add new nodes, we need to topologically sort the model graph
    model.topological_sort()
    model.check_model()
