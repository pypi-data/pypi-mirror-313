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
__all__ = ["QuantizedDepthwise2D", "get_qdepthwise"]

import numpy as np

from onnx import AttributeProto as AP, TensorProto as TP
from onnx.helper import make_node

from .base_layer import OnnxLayer, register_node_format
from .subgraph_ops import cast_tensors_to, get_scale_out_ops
from .subgraph_ops.activation import get_activation_ops
from .subgraph_ops.padding import get_padding_ops, transform_pads_into_array
from .compute_shapes import compute_onnx_conv_output
from .layer_compatibility import check_conv_depthwise_compatibility, check_clip_relu_compatibility
from ..graph_tools import (TENSOR_SHAPE, get_field, get_node, get_variable, to_field,
                           check_node_attributes)
from ..quantization.weights import quantize_weights, quantize_vector, align_to
from ..quantization.outputs import downscale


def get_qdepthwise(nodes, graph):
    conv_node = nodes[0]

    # Check supported attributes
    weights = get_variable(conv_node.input[1], graph)
    check_conv_depthwise_compatibility(conv_node, graph)

    valid_attr = {'auto_pad': ['NOTSET'], 'dilations': [[1] * (weights.ndim - 2)]}
    check_node_attributes(conv_node, valid_attr)

    # Retrieve attributes
    strides = get_field(conv_node, 'strides', (1, 1))
    act_node = get_node(nodes, 'Relu')
    clip_node = get_node(nodes, 'Clip')

    qdepthwise = QuantizedDepthwise2D(strides=strides,
                                      activation=bool(act_node) or bool(clip_node),
                                      name=conv_node.name)

    # Sets the weights to configure the operation chain
    qdepthwise.set_weight("kernel", weights)
    # If third attribute is there and it is not empty, then there is a bias
    if len(conv_node.input) == 3 and conv_node.input[2]:
        qdepthwise.set_weight("bias", get_variable(conv_node.input[2], graph))
    pads = get_field(conv_node, 'pads', False)
    if pads:
        qdepthwise.set_weight("pads", transform_pads_into_array(pads))

    if clip_node:
        check_clip_relu_compatibility(clip_node, graph)
        qdepthwise.set_weight("max_value", get_variable(clip_node.input[2], graph))

    return qdepthwise


@register_node_format(requires_downscale=True)
class QuantizedDepthwise2D(OnnxLayer):
    """Intermediate representation of Conv() + MaxPool() + ReLU() as an exportable node.

    Args:
        strides (list of int, optional): the convolutional strides. Defaults to [1, 1].
        activation (bool, optional): whether to apply relu operation. Defaults to False.
        name (str, optional): the node name. Defaults to ''.
    """

    def __init__(self, strides=[1, 1], activation=False, name=''):
        # Serialize attributes in operation name
        super().__init__("QuantizedDepthwise2D", strides=strides, name=name)

        # Save properties need to serialize operation name
        self.serialize_attr["activation"] = activation
        self.serialize_attr["scale"] = True

        # Declare weights
        self._add_weight("kernel")
        self._add_weight("bias")
        self._add_weight("max_value")
        self._add_weight("pads", dtype="int64")

    def __build__(self, input_ts, downscale=True):
        assert input_ts.dtype == np.int8
        assert downscale, f"{self.name} ({self.base_name}) does not support 32bit output"
        assert self.weights["kernel"].ndim == 4
        kernel_shape = self.weights["kernel"].shape
        expect_shape = (input_ts.shape[1], 1, *kernel_shape[-2:])
        if expect_shape != kernel_shape:
            raise ValueError("Kernel shape does not match with the following format: "
                             f"(input channels, 1, Kx, Ky). Receives: {kernel_shape} and "
                             f"expected: {expect_shape}")
        # Include groups in node as attribute
        self.attribute.append(to_field("groups", expect_shape[0]))

        # Initialize weights
        if self.weights["pads"].size == 0:
            self.set_weight("pads", np.zeros(len(kernel_shape) * 2, dtype="int64"))

        # Compute output shape
        conv_output_shape = compute_onnx_conv_output(self, input_ts.shape)
        output_ts = TENSOR_SHAPE(conv_output_shape, np.dtype("int8"))
        return output_ts

    def __quantize__(self, qinput, out_tensor_range, force_fp=False):
        i_scale = qinput.weights["scale"]
        # Perform cross-layer equalization, i.e.: rescale weights with input scale.
        # To do that first reshape i_scale to put it into axis = 0 (depthwise format) and be
        # capable of broadcasting.
        assert i_scale.ndim <= 1
        kernel = self.weights["kernel"]
        kernel = kernel / align_to(i_scale, kernel.ndim, axis=0)
        # Quantize and set weights
        qweights, i_scale = quantize_weights(kernel)

        # Prepare tensors list with unique names
        dw_name = self.name
        prefix = dw_name + "_"
        weights_dict = {prefix + "Wi": qweights}
        if "Biased" in self.op_type:
            qbias = quantize_vector(self.weights["bias"], i_scale)
            weights_dict[prefix + "B"] = qbias
        weights_dict[prefix + "pads"] = self.weights["pads"]

        # Reshape i_scale to match with channel axis
        i_scale = align_to(i_scale, qweights.ndim)

        # Quantize max value when there is an activation
        if "Clipped" in self.op_type:
            qmax_value = quantize_vector(
                self.weights["max_value"], i_scale, signed=False)
            weights_dict[prefix + "max_value"] = qmax_value

        # Now consider calibrated output range
        scale, s_out, o_scale = downscale(out_tensor_range, i_scale, force_fp=force_fp)
        weights_dict.update({prefix + "M": scale.astype("uint8"), prefix + "S_out": s_out})

        # Return quantized weights and ouput scale
        return weights_dict, o_scale

    @staticmethod
    def build_subgraph(op_type):
        # Cast input, weights (and bias) into float.
        t_names = ["X", "W", ""]
        if "Biased" in op_type:
            t_names[-1] = "bias"
        nodes, t_names = cast_tensors_to(t_names)

        # Pad + convolution
        nodes += get_padding_ops(t_names[0], "Xi")
        t_names[0] = "Xi"
        nodes.append(make_node("Conv", inputs=t_names, outputs=["Yi"]))
        # Constrain attribute that we allow
        nodes[-1].attribute.extend([AP(name="strides", ref_attr_name="strides", type=AP.INTS),
                                   AP(name="group", ref_attr_name="groups", type=AP.INT)])

        # Activation (optional)
        if "ReLU" in op_type:
            # Replace previous output as relu input
            nodes[-1].output.__setitem__(0, nodes[-1].op_type)
            nodes += get_activation_ops(nodes[-1].output[0], "Yi", "ReLUClipped" in op_type)

        # Scale out (with saturation) in float domain
        shift_nodes, shift_t_names = cast_tensors_to(["Scale", "Shift"])
        nodes += shift_nodes
        nodes += get_scale_out_ops("Yi", "Yscaled", *shift_t_names)
        # Cast output to expect type
        nodes.append(make_node("Cast", ["Yscaled"], ["Y"], to=TP.INT8))
        return nodes
