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

__all__ = ["convert_squeeze_reshape_to_flatten"]

import numpy as np

from ...graph_tools import get_tensor_shape, check_node_attributes
from ..model import ONNXModel


def convert_squeeze_reshape_to_flatten(model):
    """Converts Reshape or Squeeze nodes into a Flatten node when possible.

    Args:
        model (ONNXModel): The ONNX model to be processed.
    """
    assert isinstance(model, ONNXModel)

    expected_op_type = ("Reshape", "Squeeze")
    supported_attributes = {'allowzero': [0]}

    for node in model.nodes():
        if node.op_type in expected_op_type:
            # Reshape and Squeeze should have only one non initializer
            if len(model.get_node_inputs(node)) > 1:
                continue

            input_value_info = model.find_value_info_by_name(node.input[0])
            output_value_info = model.find_value_info_by_name(node.output[0])

            input_shape = get_tensor_shape(input_value_info)
            output_shape = get_tensor_shape(output_value_info)
            input_prod = np.prod(input_shape[1:])

            # Test if input shape flattened is equal to 2D output shape
            if (input_shape[0], input_prod) == output_shape:
                # Squeeze is not equivalent to Flatten if no axes are
                # specified, because in that case, if the batch size is 1,
                # Squeeze will remove it, unlike Flatten.
                if node.op_type == "Squeeze":
                    try:
                        axes = model.get_variable(node.input[1])
                        if 0 in axes:
                            # In case batch size is in the axis to be squeezed,
                            # we continue
                            continue
                    except IndexError:
                        # If no axes are provided, we continue
                        continue

                # Check node attributes
                try:
                    check_node_attributes(node, supported_attributes)
                except ValueError:
                    # We don't change the model when the node attributes
                    # do not match the required constraints
                    continue

                # Clean all attributes
                node.ClearField("attribute")

                # Change op to Flatten
                node.op_type = "Flatten"

                # Remove if there is a second input (e.g. shape/axes)
                if len(node.input) == 2:
                    node.input.pop(1)

    # Clean shape/axes from initializers
    model.clean_initializers()
    model.check_model()
