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

__all__ = ["convert_min_max_to_clip"]

import numpy as np
import onnx
import onnx.numpy_helper

from ..model import ONNXModel


def convert_min_max_to_clip(model):
    """Transforms Min or Max nodes into a Clip node.

    Args:
        model (ONNXModel): The ONNX model to be processed.
    """
    assert isinstance(model, ONNXModel)

    def _swap_inputs(model, node):
        # for Min and Max node, we need to put the non initializer input on the first
        # position if it is not.
        initializer = model.get_initializer(node.input[0])
        if initializer is not None:
            node.input[0], node.input[1] = node.input[1], node.input[0]

    for node in model.nodes():
        # Min or Max nodes should have exactly two inputs
        if node.op_type in ("Max", "Min") and len(node.input) == 2:
            # if both inputs are non initializers, we do nothing
            if len(model.get_node_inputs(node)) == 2:
                return

            _swap_inputs(model, node)

            node_value = model.get_variable(node.input[1])
            # Conversion from Min/Max to Clip is not possible when the node's value
            # size is greater than 1, as Clip only supports a scalar value.
            if node_value.size != 1:
                continue

            node_value_tp = model.get_initializer(node.input[1])
            node_value_tp.CopyFrom(onnx.numpy_helper.from_array(
                np.array(node_value.item(), np.float32), node.input[1]))

            if node.op_type == "Min":
                # Add an empty min. Min should be before Max that's why we swap min and max
                node.input.append("")
                node.input[1], node.input[2] = node.input[2], node.input[1]
            # convert to Clip
            node.op_type = "Clip"
    model.check_model()
