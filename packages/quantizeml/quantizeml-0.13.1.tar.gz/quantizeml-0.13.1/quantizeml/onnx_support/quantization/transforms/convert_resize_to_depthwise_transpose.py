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

__all__ = ["convert_resize_to_depthwise_transpose"]

import numpy as np
import onnx.numpy_helper
from onnx.helper import make_attribute

from ...graph_tools import check_node_attributes, get_tensor_shape
from ..model import ONNXModel


def _check_node_inputs(model, resize_node):
    if resize_node.input[1] != '' or len(resize_node.input) != 3:
        raise ValueError("Expected a Resize node with 3 inputs, with the second "
                         "input expected to be empty")

    # Since only a scale factor of 2 is supported along spatial dimensions,
    # the scales array must be exactly [1, 1, 2, 2]
    scales = model.get_variable(resize_node.input[2]).astype("int")
    np.testing.assert_equal(scales, [1, 1, 2, 2], "Expected scales to be [1, 1, 2, 2]")


def convert_resize_to_depthwise_transpose(model):
    """Converts Resize nodes (which represent The Upsample<mode=nearest, scale_factor=2>)
    to DepthwiseConv2DTranspose.

    Args:
        model (ONNXModel): The ONNX model to be processed.
    """
    def _set_node_weights(resize_node, group):
        # Get scales tensor proto from the resize node
        scales_tp = model.get_initializer(resize_node.input[2])

        # To replicate the behavior of Resize, we use a kernel of shape (3x3)
        # with the following weights accross each channel:
        # [1, 1, 0]
        # [1, 1, 0]
        # [0, 0, 0]
        weights = np.ones([group, 1, 3, 3], dtype=np.float32)
        weights[:, 0, :2, 2] = 0
        weights[:, 0, 2] = 0

        # Change scales initializer by the depthwiseConvTranspose weights.
        scales_tp.CopyFrom(onnx.numpy_helper.from_array(weights, resize_node.input[2]))

    def _set_node_attributes(resize_node, group, strides, pads):
        group_attr = make_attribute(key="group", value=group)
        strides_attr = make_attribute(key="strides", value=strides)
        pads_attr = make_attribute(key="pads", value=pads)

        resize_node.attribute.extend([pads_attr, strides_attr, group_attr])

    assert isinstance(model, ONNXModel)

    resize_nodes = [node for node in model.nodes() if node.op_type == "Resize"]
    # Return if no resize nodes are found
    if len(resize_nodes) == 0:
        return

    supported_attributes = {'coordinate_transformation_mode': ['asymmetric'],
                            'cubic_coeff_a': [-0.75],
                            'mode': ['nearest'],
                            'nearest_mode': ['floor']}

    for resize_node in resize_nodes:
        # Check node attributes
        try:
            _check_node_inputs(model, resize_node)
            check_node_attributes(resize_node, supported_attributes)
        except (ValueError, AssertionError):
            # We don't change the model when the node attributes and inputs
            # do not match the required constraints
            continue

        resize_node.op_type = 'ConvTranspose'
        resize_node.ClearField('attribute')

        # group = input_channels
        group = get_tensor_shape(model.find_value_info_by_name(resize_node.input[0]))[1]

        # Since only a scale factor of 2 is supported strides are always [2, 2]
        strides = [2, 2]

        # As kernel shape of 3x3 is used, same padding needs to be used.
        # To replicate the behavior of same padding, in this case, it's
        # SAME_UPPER, see https://onnx.ai/onnx/operators/onnx__ConvTranspose.html#summary
        # on how to compute the padding values
        pads = [0, 0, 1, 1]

        _set_node_weights(resize_node, group)
        _set_node_attributes(resize_node, group, strides, pads)

        # Scales initializers are at the third position, that's why we need to swap inputs
        # so that the weights of the ConvTranspose are in the correct position
        resize_node.input[1], resize_node.input[2] = resize_node.input[2], resize_node.input[1]
        # Pop empty input (which represents roi for the Resize node)
        resize_node.input.pop(2)

    model.check_model()
