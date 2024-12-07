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
__all__ = ["get_node", "check_node_attributes", "generate_node_names"]


from .field import get_field


def get_node(nodes, op_type):
    """Helper to get a node of a specific type.

    Args:
        nodes (list of NodeProto): list of nodes.
        op_type (str): the type of the node to get.

    Returns:
        NodeProto: the node if found, None otherwise.
    """
    filtered_ops = [node for node in nodes if node.op_type == op_type]
    if len(filtered_ops) != 1:
        # Return None if not found or too many
        return None
    return filtered_ops[0]


def check_node_attributes(node, field_constraints):
    """Helper to check node attribute constraints

    Args:
        node (NodeProto): an onnx node.
        field_constraints (dict): a dictionary with the name of the field
            and the list of allowed values.
    """
    for name, values in field_constraints.items():
        try:
            current_value = get_field(node, name)
        except AssertionError:
            # When attribute is not found we continue
            continue

        if current_value not in values:
            raise ValueError(
                f"{node.name} ({node.op_type}) is supported with {name} in {values}, "
                f"not {current_value}.")


def generate_node_names(model):
    """Assigns a name to every node that does not have one.

    Args:
        model (onnx.ModelProto): the model to assign node names
    """
    for node in model.graph.node:
        if node.name == "":
            # Output tensor name is an unique name. We can use it as node name
            node.name = node.output[0]
