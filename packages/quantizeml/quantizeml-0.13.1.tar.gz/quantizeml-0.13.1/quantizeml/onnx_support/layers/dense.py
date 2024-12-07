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
__all__ = ["QuantizedDense1D", "get_qgemm"]

import numpy as np
from onnx import TensorProto as TP
from onnx.helper import make_node

from .base_layer import OnnxLayer
from .subgraph_ops import cast_tensors_to, get_scale_out_ops
from .subgraph_ops.activation import get_activation_ops
from .layer_compatibility import check_clip_relu_compatibility

from ..graph_tools import (TENSOR_SHAPE, get_node, get_variable, get_tensor_shape,
                           check_node_attributes)
from ..quantization.weights import quantize_weights, quantize_vector, align_to
from ..quantization.outputs import downscale


def get_qgemm(nodes, graph):
    gemm_node = get_node(nodes, 'Gemm')
    assert gemm_node is not None

    # Check supported attributes
    check_node_attributes(gemm_node, {'alpha': [1.0], 'beta': [1.0], 'transA': [0], 'transB': [1]})

    # Retrieve attributes
    flatten = bool(get_node(nodes, 'Flatten'))
    act_node = get_node(nodes, 'Relu')
    clip_node = get_node(nodes, 'Clip')
    qgemm = QuantizedDense1D(flatten=flatten,
                             activation=bool(act_node) or bool(clip_node),
                             name=gemm_node.name)

    # Sets the weights to configure the operation chain
    qgemm.set_weight("kernel", get_variable(gemm_node.input[1], graph))
    # If third attribute is there and it is not empty, then there is a bias
    if len(gemm_node.input) == 3 and gemm_node.input[2]:
        qgemm.set_weight("bias", get_variable(gemm_node.input[2], graph))
    if clip_node:
        check_clip_relu_compatibility(clip_node, graph)
        qgemm.set_weight("max_value", get_variable(clip_node.input[2], graph))

    return qgemm


class QuantizedDense1D(OnnxLayer):
    """Intermediate representation of Flatten() + QGemm() + ReLU() as an exportable node.

    Args:
        flatten (bool, optional): whether to flatten the inputs. Defaults to False.
        activation (bool, optional): whether to apply relu operation. Defaults to False.
        name (str, optional): the node name. Defaults to ''.
    """

    def __init__(self, flatten=False, activation=False, name=''):
        super().__init__("QuantizedDense1D", name=name)

        # Save properties need to serialize operation name
        self.serialize_attr["flatten"] = flatten
        self.serialize_attr["activation"] = activation

        # Declare weights
        self._add_weight("kernel")
        self._add_weight("bias")
        self._add_weight("max_value")

    def __build__(self, input_ts, downscale=True):
        assert input_ts.dtype == np.int8
        assert self.weights["kernel"].ndim == 2
        filters = self.weights["kernel"].shape[0]

        # The chain of operations is modified if downscale is needed
        self.serialize_attr["scale"] = downscale

        # Compute output shape
        output_type = "int8" if downscale else "int32"
        output_ts = TENSOR_SHAPE((input_ts.shape[0], filters), np.dtype(output_type))
        return output_ts

    def __quantize__(self, qinput, out_tensor_range, force_fp=False):
        i_scale = qinput.weights["scale"]
        kernel = self.weights["kernel"]
        filters, channels = kernel.shape

        # Rescale kernel according to input scale. This operation is different if
        # pattern contain a Flatten.
        assert i_scale.ndim <= 1
        if 'Flatten' in self.op_type:
            # If flatten is there, we need to reshape weights to apply input scale
            _, c, x, y = get_tensor_shape(self.input)
            # Unroll first flattened inputs
            kernel = np.reshape(kernel, (filters, c, x, y))
            # Divide kernel by input shape (that has shape of c)
            kernel = kernel / align_to(i_scale, kernel.ndim)
            # Reshape back to original shape
            kernel = np.reshape(kernel, (filters, channels))
        else:
            kernel = kernel / align_to(i_scale, kernel.ndim)
        # Quantize and set weights
        qweights, i_scale = quantize_weights(kernel)

        # Prepare tensors list with unique names
        gemm_name = self.name
        prefix = gemm_name + "_"
        weights_dict = {prefix + "Wi": qweights}
        if "Biased" in self.op_type:
            qbias = quantize_vector(self.weights["bias"], i_scale)
            weights_dict[prefix + "B"] = qbias

        # Reshape i_scale to match with channel axis
        i_scale = align_to(i_scale, qweights.ndim)

        # Quantize max value when there is an activation
        if "Clipped" in self.op_type:
            qmax_value = quantize_vector(self.weights["max_value"], i_scale, signed=False)
            weights_dict[prefix + "max_value"] = qmax_value

        if "Scaled" not in self.op_type:
            output_scale = i_scale.squeeze()
        else:
            # Now consider calibrated output range
            scale, s_out, output_scale = downscale(out_tensor_range, i_scale, force_fp=force_fp)
            # Add scale out inputs and weights
            weights_dict[prefix + "M"] = scale.astype("uint8")
            weights_dict[prefix + "S_out"] = s_out

        # Return quantized weights and ouput scale
        return weights_dict, output_scale

    @staticmethod
    def build_subgraph(op_type):
        # Cast input, weights (and bias) into float.
        t_names = ["X", "W", ""]
        if "Biased" in op_type:
            t_names[-1] = "bias"
        nodes, t_names = cast_tensors_to(t_names)

        # Flatten (optional)
        if "Flatten" in op_type:
            nodes.append(make_node("Flatten", inputs=t_names[:1], outputs=["Xflat"]))
            t_names[0] = "Xflat"

        # Gemm
        nodes.append(make_node("Gemm", inputs=t_names, outputs=["Yi"], transB=1))

        # Activation (optional)
        if "ReLU" in op_type:
            # Replace previous output as relu input
            nodes[-1].output.__setitem__(0, nodes[-1].op_type)
            nodes += get_activation_ops(nodes[-1].output[0], "Yi", "ReLUClipped" in op_type)

        # Apply final scale (with saturation) (optional)
        if "Scaled" in op_type:
            shift_nodes, shift_t_names = cast_tensors_to(["Scale", "Shift"])
            nodes += shift_nodes
            nodes += get_scale_out_ops("Yi", "Yscaled", *shift_t_names, saturate=True)
            nodes.append(make_node("Cast", ["Yscaled"], ["Y"], to=TP.INT8))
        else:
            nodes.append(make_node("Cast", ["Yi"], ["Y"], to=TP.INT32))
        return nodes
