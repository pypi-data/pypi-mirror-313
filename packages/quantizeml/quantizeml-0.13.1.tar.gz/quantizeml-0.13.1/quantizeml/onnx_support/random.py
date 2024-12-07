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

__all__ = ["generate_onnx_random_samples"]

from ..random import generate_np_random_samples
from .graph_tools import value_info_to_tensor_shape


def generate_onnx_random_samples(graph, batch_size=1, min_value=None, max_value=None, seed=None):
    """Generate a random set of inputs for an ONNX graph.

    Args:
        graph (onnx.GraphProto): the target graph to generate inputs.
        batch_size (int, optional): a batch size. Defaults to 1.
        min_value (int or float, optional): The minimum value of the generated samples.
            Defaults to None.
        max_value (int or float, optional): The maximum value of the generated samples.
            Defaults to None.
        seed (int, optional): a random seed (reproducibility purpose). Defaults to None.

    Returns:
        dict: A dictionary where the keys represent the graph inputs, and the values
        are the corresponding random samples.
    """
    gen_inputs = {}
    for idx, input_vi in enumerate(graph.input):
        if seed is not None:
            seed = seed + idx

        # Retrieve shape from value info
        shape, dtype = value_info_to_tensor_shape(input_vi)

        gen_inputs[input_vi.name] = generate_np_random_samples(
            (batch_size, *shape[1:]), dtype, min_value, max_value,
            seed=seed)
    return gen_inputs
