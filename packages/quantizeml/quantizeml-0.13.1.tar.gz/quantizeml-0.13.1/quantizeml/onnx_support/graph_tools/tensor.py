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
__all__ = ["array_to_tp", "infer_partial_io", "get_tensor_shape", "get_tensor_dtype",
           "value_info_to_tensor_shape", "TENSOR_SHAPE", "find_value_info_by_name"]

import numpy as np
from collections import namedtuple

import onnx
import onnx.numpy_helper

TENSOR_SHAPE = namedtuple('TensorShape', ['shape', 'dtype'])


def get_tensor_shape(tensor_value_info):
    """Helper to extract the shape in a ValueInfoProto.

    Args:
        tensor_value_info (ValueInfoProto): the value info to read the shape.

    Returns:
        tuple: the tensor shape
    """
    assert isinstance(tensor_value_info, onnx.ValueInfoProto)
    tshape = tensor_value_info.type.tensor_type.shape.dim
    tshape = tuple(el.dim_param or None if el.dim_value == 0 else el.dim_value for el in tshape)
    if len(tshape) == 0 or not all(isinstance(dim, int) and dim != 0 for dim in tshape[1:]):
        raise RuntimeError(f"{tensor_value_info.name} shape ({tshape}) must be static "
                           "and it should has at least one known-dimension.")
    return tshape


def get_tensor_dtype(tensor_value_info):
    """Helper to extract the np.dtype in a ValueInfoProto.

    Args:
        tensor_value_info (ValueInfoProto): the value info to read the dtype.

    Returns:
        np.dtype: the tensor dtype
    """
    assert isinstance(tensor_value_info, onnx.ValueInfoProto)
    tensor_type = tensor_value_info.type.tensor_type.elem_type
    return onnx.helper.tensor_dtype_to_np_dtype(tensor_type)


def value_info_to_tensor_shape(x):
    """Helper to extract the shape and dtype contains in the input.

    Args:
        x (ValueInfoProto): the value info to read the shape.

    Returns:
        tuple: the tensor shape and dtype
    """
    return TENSOR_SHAPE(get_tensor_shape(x), get_tensor_dtype(x))


def array_to_tp(**kwargs):
    """Transform a numpy array list to TensorProto list

    Args:
        kwargs (dict, optional): a list of numpy arrays. Defaults to {}.

    Returns:
        list of TensorProto: the list of tensor proto.
    """
    # Transform each input in a TensorProto
    tensors = []
    for name, x in kwargs.items():
        if not isinstance(x, np.ndarray):
            x = np.array(x)
        tensors.append(onnx.numpy_helper.from_array(x, name))
    return tensors


def infer_partial_io(nodes, exclude=[]):
    """Infer the partial inputs/outputs for a list of 'connected' nodes.

    Args:
        nodes (list of NodeProto): the nodes list.
        exclude (list of str): exclude tensors with these names. Defaults to [].

    Returns:
        list, list: the inputs outputs infered.
    """
    # Search partial outputs
    def _extract_unique_not_null_elems(elems, exclude=[]):
        return sorted(set(el for el in elems if el not in exclude and el), key=elems.index)

    # Infer ordered, not null and unique input/output names
    all_inputs = sum([list(node.input) for node in nodes], [])
    all_outputs = sum([list(node.output) for node in nodes], [])
    inputs = _extract_unique_not_null_elems(all_inputs, exclude=all_outputs + exclude)
    outputs = _extract_unique_not_null_elems(all_outputs, exclude=all_inputs + exclude)
    return inputs, outputs


def find_value_info_by_name(graph, tensor_name):
    """Return a value info by its name

    Args:
        graph (GraphProto): the onnx graph
        tensor_name (str): the tensor name

    Returns:
        ValueInfoProto: the value info
    """
    for value_info in [*graph.input, *graph.output, *graph.value_info]:
        if value_info.name == tensor_name:
            return value_info
