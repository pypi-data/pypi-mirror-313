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
__all__ = ["has_field", "get_field", "to_field", "replace_field"]

import numpy as np

import onnx
import onnx.numpy_helper
from onnx.helper import make_attribute
from onnxruntime.quantization.quant_utils import find_by_name


def has_field(node, name):
    """Helper to check if a node has a field given its name.

    Args:
        node (NodeProto): the node to read the field.
        name (str): the name of the field.

    Returns:
        bool: if the node contains the attribute.
    """
    attr = find_by_name(name, node.attribute)
    return attr is not None


def get_field(node, name: str, default=None):
    """Helper to get the value of a field of a node.

    Args:
        node (NodeProto): the node to read the field.
        name (str): the name of the field.
        default (Any, optional): if the field is not found, return this value.
            If not provided, raise an exception if not field. Defaults to None.

    Returns:
        the value of the field as np.array.
    """
    attr = find_by_name(name, node.attribute)
    if attr is None:
        assert default is not None, f"Node {node.name} does not have attribute {name}."
        # onnx.helper.get_attribute_value converts any tuple/list into a list
        if isinstance(default, (tuple, list)):
            default = list(default)
        return default
    value = onnx.helper.get_attribute_value(attr)
    if isinstance(value, onnx.TensorProto):
        # Convert value into an array when is a TensorProto
        value = onnx.numpy_helper.to_array(value)
    elif isinstance(value, bytes):
        value = value.decode()
    return value


def to_field(name, value):
    """Helper to convert a value into an AttributeProto.

    Args:
        name (str): the attribute name.
        value (Any): the attribute value.

    Returns:
        AttributeProto: the attribute
    """
    if not isinstance(value, onnx.AttributeProto):
        # Convert any numpy array into a ProtoTensor
        if isinstance(value, np.ndarray):
            value = onnx.numpy_helper.from_array(value)
        value = make_attribute(name, value)
    else:
        # Try to read the value to know if it is a valid attribute
        onnx.helper.get_attribute_value(value)
        # And verify name is correct
        assert value.name == name
    return value


def replace_field(node, attr_name, new_value):
    """Helper to replace the value of one attribute in a node by another.

    Args:
        node (NodeProto): the node.
        attr_name (str): the attribute name of the value to be replaced.
        new_value (Any): the new value.
    """
    # Convert new value into an attribute
    new_value_attr = to_field(attr_name, new_value)

    # We replace field only if types are the same
    old_attribute = find_by_name(attr_name, node.attribute)
    assert old_attribute is not None, f"Node {node.name} does not have attribute {attr_name}."
    if old_attribute.type != new_value_attr.type:
        raise ValueError(f"Wrong attribute type. Expected {old_attribute.type}")

    # Replace information
    old_attribute.CopyFrom(new_value_attr)
