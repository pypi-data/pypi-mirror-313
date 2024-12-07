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
__all__ = ["get_variable"]

import onnx
import onnx.numpy_helper

from onnxruntime.quantization.quant_utils import find_by_name


def get_variable(name, graph):
    """Helper to get the value of an initializar as np.array.

    Args:
        name (str): the name of the variable.
        graph (GraphProto): the graph containing the variable.

    Returns:
        np.array: the value of the variable.
    """
    initializer = find_by_name(name, graph.initializer)
    return onnx.numpy_helper.to_array(initializer)
