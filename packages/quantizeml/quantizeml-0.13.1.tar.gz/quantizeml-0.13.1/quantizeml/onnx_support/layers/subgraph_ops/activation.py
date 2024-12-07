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
__all__ = ["get_activation_ops"]

from onnx import TensorProto
from onnx.helper import make_node


def get_activation_ops(in_name, out_name, clip=False):
    """Return the activation operation chain.

    Args:
        in_name (str): the input tensor name.
        out_name (str): the required output tensor name.
        clip (bool, optional): whether to include max_value. Defaults to False.

    Returns:
        list of NodeProto: the operation chain.
    """
    nodes = [make_node("Relu", [in_name], [out_name])]
    if clip:
        nodes[0].output[0] = f"{in_name}/relu"
        # Compute bounded activation as Min(input, max_value)
        nodes += [make_node("Cast", ["max_value"], ["max_value/cast"], to=TensorProto.FLOAT),
                  make_node("Min", [nodes[0].output[0], "max_value/cast"], [out_name])]
    return nodes
