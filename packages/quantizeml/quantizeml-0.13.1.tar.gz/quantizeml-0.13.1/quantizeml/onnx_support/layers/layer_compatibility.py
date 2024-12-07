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
__all__ = ["check_clip_relu_compatibility", "check_conv_depthwise_compatibility",
           "check_node_link_to_input", "check_node_has_one_initializer"]


from ..graph_tools import get_variable, get_field


def check_clip_relu_compatibility(clip_node, graph):
    """Checks the compatibility of a Clip node with ReLU activation in an ONNX graph.

    This function ensures that the Clip node has a minimum value input and that
    the min_value is set to zero, which is required for compatibility with ReLU.

    Args:
        clip_node (onnx.NodeProto): The Clip node to be checked.
        graph (onnx.GraphProto): The ONNX graph containing the Clip node.

    Raises:
        ValueError: If the Clip node does not have a min_value input.
        ValueError: If the min_value is not set to zero.
    """
    pre_msg_erro = "Impossible to handle Clip {} node: "

    if len(clip_node.input) == 1 or not clip_node.input[1]:
        raise ValueError(pre_msg_erro.format(clip_node.name) + "Expected a min_value input.")

    min_value = get_variable(clip_node.input[1], graph)
    if min_value != 0:
        raise ValueError(pre_msg_erro.format(clip_node.name) + "min_value must be zero.")


def check_conv_depthwise_compatibility(conv_node, graph):
    """Checks the compatibility of a convolutional node with depthwise convolution in an ONNX graph.

    This function ensures that the convolutional node can be transformed into a
    depthwise convolution. A convolution can be considered depthwise if the
    number of groups is equal to the number of filters and the kernel shape.
    Then, the resulting kernel shape will be (groups, 1, Kx, Ky).

    Args:
        conv_node (onnx.NodeProto): The convolutional node to be checked.
        graph (onnx.GraphProto): The ONNX graph containing the convolutional node.

    Raises:
        RuntimeError: If the groups attribute is equal to 1, indicating standard convolution.
        ValueError: If the number of groups does not equal the number of filters.
        ValueError: If the kernel shape in the input channel axis is not equal to 1.
    """
    groups = get_field(conv_node, "group", 1)

    # Retrieve kernel shape
    kernel_shape = get_variable(conv_node.input[1], graph).shape

    if groups == 1:
        raise RuntimeError("For groups = 1, it is handled by the Conv layer.")

    expect_kernel_shape = (groups, 1, *kernel_shape[2:])
    if kernel_shape[:2] != expect_kernel_shape[:2]:
        raise ValueError(f"Impossible to handle groups={groups} on {conv_node.name} node. "
                         f"A kernel format equal to {expect_kernel_shape} was expected "
                         f"(found {kernel_shape}).")


def check_node_link_to_input(node, graph):
    """Check the compatibility of a node to be converted into InputQuantizer:

    It must be connected to the input.

    Args:
        node (onnx.NodeProto): the node to be checked.
        graph (onnx.GraphProto): the ONNX graph containing the node.
    """
    ginputs = [x.name for x in graph.input]
    if node.input[0] not in ginputs:
        raise ValueError(f"Impossible to handle {node.name} ({node.op_type}): "
                         "it must be linked to one input.")


def check_node_has_one_initializer(node, graph):
    """Check the compatibility of a Mul/Add nodes to be converted into InputQuantizer:

    They must multiply/add a vector by a constant.

    Args:
        node (onnx.NodeProto): the node to be checked.
        graph (onnx.GraphProto): the ONNX graph containing the node.
    """
    initializers = [x.name for x in graph.initializer]
    if len(node.input) != 2 or node.input[1] not in initializers:
        raise ValueError(f"Impossible to handle {node.name} ({node.op_type}): "
                         "an initializer is expected in the second position.")
