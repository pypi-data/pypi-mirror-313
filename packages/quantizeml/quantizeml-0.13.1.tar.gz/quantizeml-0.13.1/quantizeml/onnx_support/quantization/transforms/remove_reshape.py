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

__all__ = ["remove_reshape"]

from ...graph_tools import get_tensor_shape
from ..model import ONNXModel


def _remove_redudant_flatten_reshape(model):
    def _find_reshape_flatten_sequence(model):
        expected_op_type = ("Reshape", "Flatten")
        for node in model.nodes():
            # Reshape should have only one non initializer, Flatten has by default one
            if len(model.get_node_inputs(node)) > 1:
                continue

            node_outbounds = model.get_children(node)

            # Find candidate node and get the type of the next node if there is one
            if (node.op_type in expected_op_type) and len(node_outbounds) == 1:
                outbound = node_outbounds[0]
                if outbound.op_type in expected_op_type:
                    return node
        return None

    # We consider successively the following sequences of nodes:
    # Reshape > Reshape or Reshape > Flatten or Flatten > Reshape or Flatten > Flatten
    while True:
        # Find a node that matches with the nodes pattern
        node_to_remove = _find_reshape_flatten_sequence(model)
        if node_to_remove is None:
            break  # No more node to delete

        # We remove the selected node
        model.remove_node(node_to_remove, update_graph=True)


def _remove_pointeless_reshape_flatten(model):
    nodes_to_remove = []

    for node in model.nodes():
        if node.op_type in ('Reshape', 'Flatten'):
            if len(model.get_node_inputs(node)) > 1:
                continue

            input_value_info = model.find_value_info_by_name(node.input[0])
            output_value_info = model.find_value_info_by_name(node.output[0])

            input_shape = get_tensor_shape(input_value_info)
            output_shape = get_tensor_shape(output_value_info)
            if input_shape == output_shape:
                nodes_to_remove.append(node)

    # Remove Reshape/Flatten nodes
    model.remove_nodes(nodes_to_remove, update_graph=True)


def remove_reshape(model):
    """Removes pointless Reshape/Flatten nodes (which input shape is the same as output shape)
    from the ONNX model. It also applies Multiple Reshape/Flatten transformations for
    the following patterns:
        - Reshape + Reshape → Reshape
        - Flatten + Flatten → Flatten
        - Reshape + Flatten → Flatten
        - Flatten + Reshape → Reshape

    Args:
        model (ONNXModel): The ONNX model to be processed.
    """
    assert isinstance(model, ONNXModel)

    _remove_redudant_flatten_reshape(model)
    _remove_pointeless_reshape_flatten(model)

    # Clean shape from initializers
    model.clean_initializers()
    model.check_model()
