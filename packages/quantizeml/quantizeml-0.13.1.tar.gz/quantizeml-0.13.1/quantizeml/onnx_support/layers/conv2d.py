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
__all__ = ["QuantizedConv2D", "get_qconv"]

import numpy as np

from onnx import AttributeProto as AP, TensorProto as TP
from onnx.helper import make_node

from .base_layer import OnnxLayer, register_node_format
from .subgraph_ops import cast_tensors_to, get_pool_ops, get_scale_out_ops
from .subgraph_ops.activation import get_activation_ops
from .subgraph_ops.padding import get_padding_ops, transform_pads_into_array
from .compute_shapes import compute_onnx_conv_output
from .layer_compatibility import check_clip_relu_compatibility
from ..graph_tools import (TENSOR_SHAPE, get_field, get_node, get_variable, get_tensor_shape,
                           check_node_attributes)
from ..quantization.weights import quantize_weights, quantize_vector, fold_zero_point, align_to
from ..quantization.outputs import downscale


def get_qconv(nodes, graph):
    conv_node = nodes[0]
    assert conv_node.op_type == 'Conv'

    # Check supported attributes
    weights = get_variable(conv_node.input[1], graph)
    valid_attr = {'auto_pad': ['NOTSET'], 'dilations': [[1] * (weights.ndim - 2)], 'group': [1]}
    check_node_attributes(conv_node, valid_attr)

    # Retrieve attributes
    strides = get_field(conv_node, 'strides', (1, 1))
    pool_type = "none"
    pool_size = (2, 2)
    pool_strides = (1, 1)
    pool_node = get_node(nodes, 'MaxPool')
    pool_pads = [0, 0, 0, 0]
    if pool_node:
        pool_type = "max"
        # kernel_shape attribute is mandatory for MaxPool
        pool_size = get_field(pool_node, 'kernel_shape')
        pool_strides = get_field(pool_node, 'strides', pool_strides)
        pool_pads = get_field(pool_node, "pads", pool_pads)
    pool_node = get_node(nodes, 'GlobalAveragePool')
    if pool_node:
        pool_type = "gap"

    act_node = get_node(nodes, 'Relu')
    clip_node = get_node(nodes, 'Clip')

    qconv = QuantizedConv2D(strides=strides,
                            pool_type=pool_type,
                            pool_size=pool_size,
                            pool_strides=pool_strides,
                            pool_pads=pool_pads,
                            activation=bool(act_node) or bool(clip_node),
                            name=conv_node.name)

    # Sets the weights to configure the operation chain
    qconv.set_weight("kernel", weights)
    # If third attribute is there and it is not empty, then there is a bias
    if len(conv_node.input) == 3 and conv_node.input[2]:
        qconv.set_weight("bias", get_variable(conv_node.input[2], graph))
    pads = get_field(conv_node, 'pads', False)
    if pads:
        qconv.set_weight("pads", transform_pads_into_array(pads))

    if clip_node:
        check_clip_relu_compatibility(clip_node, graph)
        qconv.set_weight("max_value", get_variable(clip_node.input[2], graph))

    return qconv


@register_node_format(requires_downscale=True)
class QuantizedConv2D(OnnxLayer):
    """Intermediate representation of QLinearConv() + MaxPool() + ReLU() as an exportable node.

    Args:
        strides (list of int, optional): the convolutional strides. Defaults to [1, 1].
        pool_type (str, optional): the pool type, one of {"none", "max", "gap"}. Defaults to "none".
        pool_size (list of int, optional): the kernel pool shape.
            Ignore it when pool_type != "max". Defaults to (2, 2).
        pool_stride (list of int, optional): the kernel strides.
            Ignore it when pool_type != "max". Defaults to (2, 2).
        pool_pads (list of int, optional): the size of each padding dimension.
            Ignore it when pool_type != "max". Defaults to [0, 0, 0, 0].
        input_conv (bool, optional): whether it is extended the set of operations of
            the basic QuantizedConv2D, allowing to modify the padding value per input channel.
            Defaults to False.
        activation (bool, optional): whether to apply relu operation. Defaults to False.
        name (str, optional): the node name. Defaults to ''.
    """

    def __init__(self,
                 strides=[1, 1],
                 pool_type="none",
                 pool_size=(2, 2),
                 pool_strides=(2, 2),
                 pool_pads=[0, 0, 0, 0],
                 activation=False,
                 name=''):
        assert pool_type in ["none", "max", "gap"]
        super().__init__("QuantizedConv2D",
                         strides=strides,
                         pool_size=pool_size,
                         pool_strides=pool_strides,
                         pool_pads=pool_pads,
                         name=name)

        # Save properties need to serialize operation name
        self.serialize_attr["pool_type"] = pool_type
        self.serialize_attr["activation"] = activation
        self.serialize_attr["scale"] = True

        # Declare weights
        self._add_weight("kernel")
        self._add_weight("bias")
        self._add_weight("max_value")
        self._add_weight("pads", dtype="int64")

    def __build__(self, input_ts, downscale=True):
        assert input_ts.dtype in (np.uint8, np.int8)
        assert downscale, f"{self.name} ({self.base_name}) does not support 32bit output"
        assert self.weights["kernel"].ndim == 4

        # The chain of operations is modified by the type of input:
        kernel_shape = self.weights["kernel"].shape
        if input_ts.dtype == np.uint8:
            self.base_name = "QuantizedInputConv2D"
            if self.weights["bias"].size == 0:
                # Bias is mandatory on this configuration
                filters = kernel_shape[0]
                self.set_weight("bias", np.zeros(filters, dtype="float32"))

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
        # To do that first reshape i_scale to put it into axis = 1 and be capable of broadcasting.
        assert i_scale.ndim <= 1
        kernel = self.weights["kernel"]
        kernel = kernel / align_to(i_scale, kernel.ndim, axis=1)
        # Quantize and set weights
        qweights, i_scale = quantize_weights(kernel)

        # Prepare tensors list with unique names
        conv_name = self.name
        prefix = conv_name + "_"
        weights_dict = {}
        bias = self.weights["bias"]
        if "InputConv" in self.op_type:
            # If calibration was done per tensor, repeat zero point over each channel
            zero_point = qinput.weights["zero_point"]
            if zero_point.size == 1:
                zero_point = np.repeat(zero_point, kernel.shape[1])
            weights_dict[prefix + "Xpad"] = zero_point
            # Fold zero point in bias
            # Note: Dequantize kernel instead to use the float to reduce quantization error
            kernel = qweights / align_to(i_scale, qweights.ndim, axis=0)
            bias = fold_zero_point(bias, kernel, zero_point)
        weights_dict[prefix + "Wi"] = qweights
        if "Biased" in self.op_type:
            qbias = quantize_vector(bias, i_scale)
            weights_dict[prefix + "B"] = qbias
        weights_dict[prefix + "pads"] = self.weights["pads"]

        # Reshape i_scale to match with channel axis
        i_scale = align_to(i_scale, qweights.ndim)

        # Quantize max value when there is an activation
        if "Clipped" in self.op_type:
            qmax_value = quantize_vector(self.weights["max_value"], i_scale, signed=False)
            weights_dict[prefix + "max_value"] = qmax_value

        # Fold spatial dimension when GAP
        if "GlobalAvgPool" in self.op_type:
            input_shape = get_tensor_shape(self.input)
            input_shape = compute_onnx_conv_output(self, input_shape, apply_pool=False)
            i_scale *= input_shape[-2] * input_shape[-1]

        # Now consider calibrated output range
        scale, s_out, ocalib_scale = downscale(out_tensor_range, i_scale, force_fp=force_fp)
        weights_dict.update({prefix + "M": scale.astype("uint8"), prefix + "S_out": s_out})

        # Return quantized weights and ouput scale
        return weights_dict, ocalib_scale

    @staticmethod
    def build_subgraph(op_type):
        # Cast input, weights (and bias) into float.
        t_names = ["X", "", "W", ""]
        if "InputConv" in op_type:
            t_names[1] = "x_pad_value"
        if "Biased" in op_type:
            t_names[-1] = "bias"
        nodes, t_names = cast_tensors_to(t_names)

        # Pad + convolution
        nodes += get_padding_ops(t_names[0], "Xi", t_names[1])
        conv_tensor_names = nodes[-1].output[:1] + t_names[2:]
        nodes.append(make_node("Conv", inputs=conv_tensor_names, outputs=["Yi"]))
        nodes[-1].attribute.append(AP(name="strides", ref_attr_name="strides", type=AP.INTS))

        # Maxpool (optional)
        if "MaxPool" in op_type:
            # Replace previous output as maxpool input
            nodes[-1].output.__setitem__(0, nodes[-1].op_type)
            nodes += get_pool_ops(nodes[-1].output[0], "Yi", pool_op_type="MaxPool")

        # Activation (optional)
        if "ReLU" in op_type:
            # Replace previous output as relu input
            nodes[-1].output.__setitem__(0, nodes[-1].op_type)
            nodes += get_activation_ops(nodes[-1].output[0], "Yi", "ReLUClipped" in op_type)

        # AvgPool (optional)
        if "GlobalAvgPool" in op_type:
            # Replace previous output as maxpool input
            nodes[-1].output.__setitem__(0, nodes[-1].op_type)
            nodes += get_pool_ops(nodes[-1].output[0], "Yi", pool_op_type="GlobalAvgPool")

        # Scale out (with saturation) in float domain
        shift_nodes, shift_t_names = cast_tensors_to(["Scale", "Shift"])
        nodes += shift_nodes
        nodes += get_scale_out_ops("Yi", "Yscaled", *shift_t_names)
        # Cast output to expect type
        nodes.append(make_node("Cast", ["Yscaled"], ["Y"], to=TP.INT8))
        return nodes
