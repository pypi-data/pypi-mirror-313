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
__all__ = ["QuantizedAdd", "get_qadd", "QuantizedConcat", "get_qconcat"]

import numpy as np

from onnx import TensorProto as TP
from onnx.helper import make_node

from .base_layer import OnnxLayer, register_node_format
from .subgraph_ops import cast_tensors_to, get_scale_out_ops, get_input_shift_ops
from .subgraph_ops.activation import get_activation_ops
from ..graph_tools import TENSOR_SHAPE, get_tensor_shape, get_node
from ..quantization.weights import align_to
from ..quantization.outputs import downscale_fp
from ..graph_tools import get_field


def get_qadd(nodes, graph):
    # Both inputs should not be constants
    weight_names = [x.name for x in graph.initializer]
    if nodes[0].input[0] in weight_names or nodes[0].input[1] in weight_names:
        raise ValueError("Unsupported Add: inputs should be tensors.")

    add_node = nodes[0]
    add_name = add_node.name

    act_node = get_node(nodes, 'Relu')
    qadd = QuantizedAdd(name=add_name, activation=bool(act_node))

    return qadd


def get_qconcat(nodes, graph):
    concat_node = nodes[0]
    concat_name = concat_node.name
    concat_axis = get_field(concat_node, "axis")
    return QuantizedConcat(name=concat_name, axis=concat_axis)


@register_node_format(requires_fp_inputs=True)
class QuantizedAdd(OnnxLayer):
    """Intermediate representation of Add() as an exportable node.

    Args:
        activation (bool, optional): whether to apply relu operation. Defaults to False.
        name (str, optional): the node name. Defaults to ''.
    """

    def __init__(self, activation=False, name=''):
        super().__init__("QuantizedAdd", name=name)

        # Save properties need to serialize operation name
        self.serialize_attr["activation"] = activation

    @property
    def op_type(self):
        # Overriding op_type as ReLU comes after Scaling
        op_name = self.base_name
        if self.serialize_attr["scale"]:
            op_name += "Scaled"
        if self.serialize_attr["activation"]:
            op_name += "ReLU"
        return op_name

    def __build__(self, a_input_ts, b_input_ts, downscale=True):
        assert a_input_ts.dtype == b_input_ts.dtype == np.int8
        assert a_input_ts.shape == b_input_ts.shape

        # The chain of operations is modified if downscale is needed
        self.serialize_attr["scale"] = downscale

        # Compute output shape
        output_type = "int8" if downscale else "int32"
        output_ts = TENSOR_SHAPE(a_input_ts.shape, np.dtype(output_type))
        return output_ts

    def __quantize__(self, a_qinput, b_qinput, out_tensor_range, force_fp=False):
        def _round_pot(x):
            return 2.0**np.round(np.log2(x))

        x1_scale = a_qinput.weights["scale"]
        x2_scale = b_qinput.weights["scale"]
        # This quantization is feasible if and only if input scales are power-of-two
        np.testing.assert_array_equal(x1_scale, _round_pot(x1_scale), "Required a power-of-two")
        np.testing.assert_array_equal(x2_scale, _round_pot(x2_scale), "Required a power-of-two")

        # Prepare tensors list with unique names
        prefix = self.name + "_"

        # Transpose scales to align with channels
        output_shape = get_tensor_shape(self.output)
        x1_scale = align_to(x1_scale, len(output_shape))
        x2_scale = align_to(x2_scale, len(output_shape))

        # We expected input scales are a power-of-two. Take i_scale as a max of both scales
        i_scale = np.maximum(x1_scale, x2_scale)

        # Shift to apply for each input will be
        weights_dict = {prefix + "x1_shift": (i_scale / x1_scale).astype("int32"),
                        prefix + "x2_shift": (i_scale / x2_scale).astype("int32")}

        if "Scaled" not in self.op_type:
            out_scale = i_scale.squeeze()
        else:
            # Now consider calibrated output range
            scale, s_out, out_scale = downscale_fp(out_tensor_range, i_scale, bitwidth=8)
            # Add does not have output scale. We fold scale into shift as a power-of-two.
            # This will force an 'output scale' = 1
            s_out = 2.0**(np.log2(s_out) - np.ceil(np.log2(scale)))
            weights_dict.update({prefix + "S_out": s_out.astype(np.float32)})

        # Return quantized weights and output scale
        return weights_dict, out_scale

    @staticmethod
    def build_subgraph(op_type):
        # Cast inputs and shift to float.
        nodes, t_names = cast_tensors_to(["X", "Y", "Xs", "Ys"])

        # Align inputs with input shift
        nodes += get_input_shift_ops(t_names[0], t_names[2], "Xshifted")
        nodes += get_input_shift_ops(t_names[1], t_names[3], "Yshifted")

        # Perform addition
        nodes.append(make_node("Add", inputs=["Xshifted", "Yshifted"], outputs=["Zi"]))

        # Apply final output shift (optional)
        if "Scaled" in op_type:
            shift_nodes, shift_t_names = cast_tensors_to(["", "Shift"])
            nodes += shift_nodes
            nodes += get_scale_out_ops("Zi", "Zscaled", *shift_t_names)
            nodes.append(make_node("Cast", ["Zscaled"], ["Z"], to=TP.INT8))
        else:
            nodes.append(make_node("Cast", ["Zi"], ["Z"], to=TP.INT32))

        # Activation (optional)
        if "ReLU" in op_type:
            # rename previous output
            nodes[-1].output[0] = "Z_no_act"
            nodes += get_activation_ops(nodes[-1].output[0], "Z")

        return nodes


class QuantizedConcat(OnnxLayer):
    """Intermediate representation of Concatenate() as an exportable node.

    Args:
        name (str, optional): the node name. Defaults to ''.
    """

    def __init__(self, axis,  name=''):
        if axis != 1:
            raise NotImplementedError("Axis != 1 in Concat is not supported yet.")
        super().__init__("QuantizedConcat", axis=axis, name=name)

    def __build__(self, a_input_ts, b_input_ts, downscale=False):
        # return the concatenated shape
        b, c, w, h = a_input_ts.shape
        concat_output_shape = (b, a_input_ts.shape[1] + b_input_ts.shape[1], w, h)
        output_ts = TENSOR_SHAPE(concat_output_shape, a_input_ts.dtype)
        return output_ts

    def __quantize__(self, a_qinput, b_qinput, out_tensor_range, force_fp=False):
        # get scale and broadcast to input shape in case of per tensor
        x1_scale = a_qinput.weights["scale"]
        x1_shape = get_tensor_shape(a_qinput.output)
        x1_scale = x1_scale * np.ones(x1_shape[1])
        x2_scale = b_qinput.weights["scale"]
        x2_shape = get_tensor_shape(b_qinput.output)
        x2_scale = x2_scale * np.ones(x2_shape[1])
        # concatenate scales
        out_scale = np.concatenate((x1_scale, x2_scale))
        return {}, out_scale

    @staticmethod
    def build_subgraph(op_type):
        # Perform concatenation
        return [make_node("Concat", inputs=["X", "Y"], outputs=["Zi"], axis=1)]
