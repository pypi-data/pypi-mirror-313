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
__all__ = ["InputQuantizer", "Dequantizer", "get_input_quantizer"]

import numpy as np
import uuid

from onnx.helper import make_node, make_tensor_value_info, np_dtype_to_tensor_dtype
from onnx import AttributeProto as AP
from onnx import ValueInfoProto
from onnxruntime.quantization.calibrate import TensorData

from .base_layer import OnnxLayer
from .layer_compatibility import check_node_link_to_input, check_node_has_one_initializer
from ..graph_tools import (TENSOR_SHAPE, value_info_to_tensor_shape, array_to_tp, get_field,
                           get_variable, get_node, has_field, to_field)

from ..quantization.input_scale import input_zp_scale
from ...models import get_quantization_params


def get_input_quantizer(nodes, graph):
    check_node_link_to_input(nodes[0], graph)

    perm = None
    transpose_node = get_node(nodes, "Transpose")
    if (transpose_node := get_node(nodes, "Transpose")) is not None:
        perm = get_field(transpose_node, "perm")

    input_ts = graph.input[0]
    input_signed = get_quantization_params().input_dtype.kind == "i"
    input_quantizer = InputQuantizer(name="quantize",
                                     input_tp=input_ts,
                                     input_signed=input_signed,
                                     perm=perm)

    # Sets rescaling weights
    if (mul_node := get_node(nodes, "Mul")) is not None:
        check_node_has_one_initializer(mul_node, graph)
        input_quantizer.set_weight("input_scale", get_variable(mul_node.input[1], graph))
    if (add_node := get_node(nodes, "Add")) is not None:
        check_node_has_one_initializer(add_node, graph)
        input_quantizer.set_weight("offset", get_variable(add_node.input[1], graph))
    return input_quantizer


def _compute_quantization_parameters(r_scale, r_offset, out_tensor_range, signed):
    assert isinstance(out_tensor_range, TensorData)
    # Computing the ranges before the Rescale node (e.g. the model inputs)

    in_tensor_range = [(x - r_offset) / r_scale for x in out_tensor_range.range_value]
    in_tensor_range = TensorData(lowest=np.minimum(*in_tensor_range),
                                 highest=np.maximum(*in_tensor_range))

    # Compute scale and zero point to quantize the inputs
    input_scale, input_zp = input_zp_scale(in_tensor_range, allow_zp=not signed)

    # Compute scale and output to dequantize the outputs
    output_scale, output_zp = input_zp_scale(out_tensor_range, allow_zp=not signed)

    # Check constraints
    err_msg = "Impossible to quantize inputs when folding rescale: "
    if not signed:
        # Compare if rescale is valid
        np.testing.assert_allclose(input_scale / output_scale,
                                   r_scale,
                                   atol=1e-3,
                                   err_msg=err_msg + "input/output scales ratio is not valid.")
    else:
        np.testing.assert_equal(r_offset, 0, err_msg + "offset must be zero when input is signed.")
    return (input_scale, input_zp), (output_scale, output_zp)


class InputQuantizer(OnnxLayer):
    """Intermediate representation of QuantizeLinear(), use to quantize the input.

    Args:
        input_tp (TensorProto): the input of the ONNX model.
        perm (list, optional): list representing the permutations of the rescale node.
            Defaults to None.
        input_signed (bool, optional): whether the input is signed. Defaults to False.
        name (str, optional): the node name. Defaults to ''.
    """

    def __init__(self, input_tp, perm=None, input_signed=False, name=''):
        super().__init__("InputQuantizer", name=name, perm=perm)
        self.input_signed = input_signed
        self._input = [input_tp]

        # Declare weights
        self._add_weight("input_scale")
        self._add_weight("offset")

    def __build__(self, downscale=True):
        assert downscale, f"{self.name} ({self.base_name}) does not support 32bit output"
        input_ts = value_info_to_tensor_shape(self.input)
        assert input_ts.dtype == np.float32

        # Add/initialize weights
        zp_dtype = "int8" if self.input_signed else "uint8"
        self._add_weight("zero_point", value=np.zeros(input_ts.shape[1]), dtype=zp_dtype)
        if self.weights["input_scale"].size == 0:
            self.set_weight("input_scale", np.ones((), dtype="float32"))
        if self.weights["offset"].size == 0:
            self.set_weight("offset", np.zeros((), dtype="float32"))

        # Update perm attribute
        input_ndim = len(input_ts.shape)
        if has_field(self, "perm"):
            perm = get_field(self, "perm")
        else:
            perm = list(range(input_ndim))
            self.attribute.append(to_field("perm", perm))

        # Compute output shape
        output_shape = tuple(input_ts.shape[i] for i in perm)
        output_ts = TENSOR_SHAPE(output_shape, np.dtype(zp_dtype))

        # Assert wrong weights format
        first_channel_expected_shape = (1,) + output_shape[1:2] + (1,) * (input_ndim - 2)
        if (self.weights["input_scale"].size != 1 and
                self.weights["input_scale"].shape != first_channel_expected_shape):
            raise ValueError(f"Unsupported 'input_scale' in {self.name} ({self.base_name}): "
                             "it must be brodcastable in the channels dimension.")
        if (self.weights["offset"].size != 1 and
                self.weights["offset"].shape != first_channel_expected_shape):
            raise ValueError(f"Unsupported 'offset' in {self.name} ({self.base_name}): "
                             "it must be brodcastable in the channels dimension.")
        return output_ts

    def __quantize__(self, out_tensor_range, force_fp=False):
        if force_fp:
            raise NotImplementedError("Force input scale to be a FP is not implemented yet.")

        # Calibration was done by axis=1. Therefore we can squeeze dimension in mean/offset
        rescale_scale = np.squeeze(self.weights["input_scale"])
        rescale_offset = np.squeeze(self.weights["offset"])

        # Computing quantization parameters
        input_scale_zp, output_scale_zp = _compute_quantization_parameters(rescale_scale,
                                                                           rescale_offset,
                                                                           out_tensor_range,
                                                                           self.input_signed)

        # Scale to set in weights is the reciprocal of ONNX calibrated one.
        input_scale = np.array(1 / input_scale_zp[0], dtype=np.float32)

        # Compute weights to serialize
        weights = {f"{self.name}_scale": input_scale, f"{self.name}_zp": input_scale_zp[1]}

        # Save zero point (used by next layer)
        self.set_weight("zero_point", output_scale_zp[1])
        return weights, output_scale_zp[0]

    @staticmethod
    def build_subgraph(op_type):
        nodes = [make_node('Transpose', inputs=["X"], outputs=["Yi"])]
        nodes[-1].attribute.append(AP(name="perm", ref_attr_name="perm", type=AP.INTS))
        nodes.append(make_node('QuantizeLinear', inputs=["Yi", "scale", "zp"], outputs=["Y"]))
        return nodes


class Dequantizer(OnnxLayer):
    """Intermediate representation of DequantizeLinear(), use to dequantize the inputs.

    Args:
        name (str, optional): the node name. Defaults to ''.
    """

    def __init__(self, name=''):
        super().__init__("Dequantizer", name=name)

    def __build__(self, *input_ts):
        assert len(input_ts) >= 1
        assert [ts.dtype in (np.int8, np.int32) for ts in input_ts]

        # Compute output shapes
        output_ts = [TENSOR_SHAPE(ts.shape, np.dtype("float32")) for ts in input_ts]
        return output_ts

    @property
    def op_type(self):
        op_name = self.base_name
        if self.serialize_attr["num_inputs"] > 1:
            op_name += str(self.serialize_attr["num_inputs"])

        return op_name

    def build(self, *inputs_vi):
        assert all(isinstance(x, ValueInfoProto) for x in inputs_vi)

        # Serialize the number of inputs
        self.serialize_attr["num_inputs"] = len(inputs_vi)

        # Replace empty name
        if not self.name:
            self.name = str(uuid.uuid4())

        # Convert ValueInfoProto into TensorShape for each input
        self._input = inputs_vi
        input_ts = [value_info_to_tensor_shape(x) for x in inputs_vi]

        output_ts = self.__build__(*input_ts)
        self._output = [make_tensor_value_info(f"{vi.name}/dequantize",
                                               elem_type=np_dtype_to_tensor_dtype(out_ts.dtype),
                                               shape=out_ts.shape)
                        for vi, out_ts in zip(inputs_vi, output_ts)]

    def quantize(self, *qlayers):
        # To keep homogenity with the other layers, this function is called 'quantize'
        # even though it does the opposite (dequantize): apply scale in the inputs integers.
        if self._output is None or self._input is None:
            # Build the layer if required
            input_ts = [qly.output for qly in qlayers]
            self.build(*input_ts)

        # Scale to set in weights is the reciprocal of ONNX calibrated one.
        i_scales = [qlayer.weights["scale"] for qlayer in qlayers]
        scales = [np.array(1 / i_scale, dtype=np.float32) for i_scale in i_scales]

        # Return ONNX node and weights
        output_names = [out.name for out in self.output]
        weights = {f"{self.name}_scale_{i+1}": scale for i, scale in enumerate(scales)}
        if len(self.output) == 1:
            # Remove suffix when number of inputs/outputs is one
            weights[f"{self.name}_scale"] = weights.pop(f"{self.name}_scale_1")

        # Inputs should be ordered as follows : X1, S1, X2, S2...
        input_names = [ts.name for ts in self._input]
        inputs = sum(list(zip(input_names, weights)), ())

        onnx_node = self.make_node(inputs, output_names)
        onnx_weights = array_to_tp(**weights)
        return onnx_node, onnx_weights

    @staticmethod
    def build_subgraph(op_type):
        # When there is only one output, the op_type is called Dequantizer
        node_params = []
        if op_type != 'Dequantizer':
            num_inputs = int(op_type.replace('Dequantizer', ''))
            for i in range(1, num_inputs + 1):
                node_params.append({"inputs": [f"X{i}", f"scale_{i}"], "outputs": [f"Y{i}"]})
        else:
            node_params.append({"inputs": ["X", "scale"], "outputs": ["Y"]})
        nodes = [make_node('DequantizeLinear', **nparams) for nparams in node_params]
        return nodes
