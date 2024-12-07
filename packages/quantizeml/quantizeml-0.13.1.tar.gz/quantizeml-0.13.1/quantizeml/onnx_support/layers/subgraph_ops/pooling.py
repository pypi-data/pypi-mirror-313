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
__all__ = ["get_pool_ops"]

from onnx import AttributeProto as AP
from onnx.helper import make_node


def get_pool_ops(in_name, out_name, pool_op_type="MaxPool"):
    """Return the pool operation chain.

    Args:
        in_name (str): the input tensor name.
        out_name (str): the required output tensor name.
        pool_op_type (str): the pool type (one of {"MaxPool"}).

    Returns:
        list of NodeProto: the operation chain.
    """
    # Create the node
    if pool_op_type == "MaxPool":
        pool_node = make_node("MaxPool", [in_name], [out_name])
        # Conv have similar attributes than MaxPool. To avoid share them,
        # we define new reference values.
        pool_node.attribute.extend([
            AP(name="kernel_shape", ref_attr_name="pool_size", type=AP.INTS),
            AP(name="strides", ref_attr_name="pool_strides", type=AP.INTS),
            AP(name="pads", ref_attr_name="pool_pads", type=AP.INTS)])
        # Append Maxpool to the operation chain
        nodes = [pool_node]
    elif pool_op_type == "GlobalAvgPool":
        # Append GAP to the operation chain, as ReduceSum
        # Note: spatial dimensions have to fold in output scale
        nodes = [make_node("Constant", [], ["GAP/axes"], value_ints=[-2, -1]),
                 make_node("ReduceSum", [in_name, "GAP/axes"], [out_name])]
    else:
        raise ValueError(f"Unrecognized {pool_op_type} pool operation type.")
    return nodes
