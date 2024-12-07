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

__all__ = ["convert_avg_to_gap"]

from ...graph_tools import get_tensor_shape, check_node_attributes
from ..model import ONNXModel


def convert_avg_to_gap(model):
    """
    Converts AveragePool node to GlobalAveragePool if the kernel shape is equal to
    spatial dimensions.

    Args:
        model (ONNXModel): The ONNX model to be processed.
    """
    assert isinstance(model, ONNXModel)

    supported_attributes = {'auto_pad': ['NOTSET']}

    for node in model.nodes():
        if node.op_type == 'AveragePool':
            value_info = model.find_value_info_by_name(node.input[0])

            # shape format : (B, C, H, W)
            input_shape = get_tensor_shape(value_info)

            try:
                supported_attributes.update({'kernel_shape': [list(input_shape[2:])],
                                             'pads': [[0] * len(input_shape)]})
                check_node_attributes(node, supported_attributes)
                node.op_type = "GlobalAveragePool"
                node.ClearField('attribute')

            except ValueError:
                # We continue when the node attributes
                # do not match the required constraints
                continue
    model.check_model()
