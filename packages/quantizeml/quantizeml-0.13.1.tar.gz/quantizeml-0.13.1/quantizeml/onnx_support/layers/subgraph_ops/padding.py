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
__all__ = ["get_padding_ops"]

import numpy as np

from onnx.helper import make_node


def transform_pads_into_array(pads):
    """Return the expected pads to apply in the custom operation.

    Args:
        pads (list of int): the pads to transform.

    Returns:
        TensorProto: pads as tensor.
    """
    assert len(pads) == 4, "Expect 4 values for pads"
    # ONNX Pad expect a 1D tensor of shape [2 * num_axes]. Given we should apply pads
    # over XY dimensions, others will be set to 0.
    # See https://onnx.ai/onnx/operators/onnx__Pad.html for more information.
    pads = [0, 0] + pads[:2] + [0, 0] + pads[2:]
    return np.array(pads, "int64")


def get_padding_ops(in_name, out_name, pad_value_name=""):
    """Return the pad operation chain.

    Args:
        in_name (str): the input tensor name.
        out_name (str): the required output tensor name.
        pad_value_name (str, optional): name of padding value.
            Takes a zero value when not specified. Defaults to "".

    Returns:
        list of NodeProto: the operation chain.
    """
    if not pad_value_name:
        return [make_node("Pad", inputs=[in_name, "pads"], outputs=[out_name])]

    # Knowledge: padding_value is a tensor and it contains one value per input channel.
    # The following sequence of operations is carried out to apply padding_value for each channel
    # X -> Sub(X, padding_value) -> Pad(Xsub, pad) -> Add(Xpadded, padding_value) -> Y

    nodes = [make_node("Constant", [], ["pad_axes"], value_ints=[1, 2]),
             make_node("Unsqueeze", [pad_value_name, "pad_axes"], ["unqueezed_pad"]),
             make_node("Sub", [in_name, "unqueezed_pad"], ["Xsub"]),
             make_node("Pad", ["Xsub", "pads"], ["Xpadded"]),
             make_node("Add", ["Xpadded", "unqueezed_pad"], [out_name])]
    return nodes
