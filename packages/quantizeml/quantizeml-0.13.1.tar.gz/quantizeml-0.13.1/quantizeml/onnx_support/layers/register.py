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
__all__ = ["AKIDA_ONNX_LAYERS"]

from ..graph_tools import infer_partial_io

AKIDA_ONNX_LAYERS = []


def infer_function_parameters(nodes):
    """Provides the expected input, output and attribute names for
    the node sequence to define a function based on them.

    Args:
        nodes (list of NodeProto): the node sequence.

    Returns:
        list: the expected input, output and attribute names
    """
    # Infer ordered, not null and unique input/output names
    inputs, outputs = infer_partial_io(nodes)

    # Handle attribute list.
    attributes = set()
    for node in nodes:
        # We consider as attributes those with ref_attr_name != "":
        # it is the real link between node attribute names and attribute in function.
        node_attrs = [attr for attr in node.attribute if attr.ref_attr_name]
        new_attributes = set(attr.ref_attr_name for attr in node_attrs)
        attributes.update(new_attributes)
    return inputs, outputs, list(attributes)


def register_new_subgraph(func):
    """Try to register a new subgraph (view as a function in ONNX) under brainchip domain.

    Args:
        func (FunctionProto): the function to register.
    """
    global AKIDA_ONNX_LAYERS

    # Only register new functions (avoid duplicates)
    if all(f.name != func.name for f in AKIDA_ONNX_LAYERS):
        AKIDA_ONNX_LAYERS.append(func)
    return func
