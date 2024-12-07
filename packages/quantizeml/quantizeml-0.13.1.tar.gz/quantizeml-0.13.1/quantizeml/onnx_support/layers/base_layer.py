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
__all__ = ["OnnxLayer", "DOMAIN", "VERSION"]

import numpy as np
import uuid
from collections import defaultdict
import inspect

from onnx import ValueInfoProto
from onnx.helper import (make_function, make_node, make_opsetid, make_tensor_value_info,
                         np_dtype_to_tensor_dtype)
from onnx.defs import onnx_opset_version

from .register import register_new_subgraph, infer_function_parameters
from ..graph_tools import to_field, value_info_to_tensor_shape, array_to_tp

DOMAIN = "com.brainchip"
VERSION = 1

# List of quantized layers that requires a power of two scale
_GLOBAL_REQUIRES_FP_INPUTS = []

# List of quantized layers that should always output in 8bit
_GLOBAL_REQUIRES_DOWNSCALE = []


def register_node_format(requires_downscale=False, requires_fp_inputs=False):
    """Decorator to register the node format requirements such as whether it requires
    downscaling or fixed-point inputs.

    _GLOBAL_REQUIRES_FP_INPUTS and _GLOBAL_REQUIRES_DOWNSCALE are populated
    with the quantized node type.

    Args:
        requires_downscale (bool, optional): determines if the node class requires downscaling.
            Defaults to False.
        requires_fp_inputs (bool, optional): determines if the node class requires fixed-point
            inputs. Defaults to False.

    Returns:
        Callable: a decorator that registers the decorated class
    """
    def decorator(cls):
        if not inspect.isclass(cls):
            raise ValueError("Can only register class objects with 'register_node_format'.")
        if requires_downscale:
            _GLOBAL_REQUIRES_DOWNSCALE.append(cls)
        if requires_fp_inputs:
            _GLOBAL_REQUIRES_FP_INPUTS.append(cls)
        return cls
    return decorator


class OnnxLayer:
    """Abstract class that represents an onnx subgraph in brainchip domain.

    Child must define the attributes on __init__ and return the node list (subgraph) on
    build_subgraph(). If these requirements are met, make_node() could be used to
    define/register the custom node.

    Args:
        base_name (str): the operation type base name.
        name (str, optional): the node name. Defaults to ''.
        kwargs (dict, optional): the custom attributes. Each attribute type will be
            infered by ``onnx.helper.make_attribute()``. Defaults to {}.
    """

    def __init__(self, base_name, name='', **kwargs):
        self.base_name = base_name
        self.name = name
        self._input = None
        self._output = None
        self.serialize_attr = defaultdict(bool)

        # Load attributes
        # Note: this field is called 'attribute' to align it to the same ONNX standard
        self.attribute = self._load_attributes(**kwargs)

        # Create empty variable to save the weights
        self._weights = {}

    @property
    def op_type(self):
        op_name = self.base_name
        if self.serialize_attr["flatten"]:
            op_name += "Flatten"
        bias = self.weights.get("bias", np.array([]))
        if bias.size > 0:
            op_name += "Biased"
        pool_type = self.serialize_attr["pool_type"]
        if pool_type == "max":
            op_name += "MaxPool"
        elif pool_type == "gap":
            op_name += "GlobalAvgPool"
        if self.serialize_attr["activation"]:
            op_name += "ReLU"
            # We assume unbounded activation when max_value = 0
            max_value = self.weights.get("max_value", np.array([]))
            if np.any(max_value != 0):
                op_name += "Clipped"
        if self.serialize_attr["scale"]:
            op_name += "Scaled"
        return op_name

    @property
    def input(self):
        assert self._input is not None, f"{self.name} has not being built yet."
        return self._input[0] if len(self._input) == 1 else self._input

    @property
    def output(self):
        assert self._output is not None, f"{self.name} has not being built yet."
        return self._output

    @property
    def weights(self):
        return self._weights

    def _load_attributes(self, **kwargs):
        attrs = []
        for key, value in kwargs.items():
            # Convert each non None value in an AttributeProto
            if value is not None:
                value = to_field(key, value)
                attrs.append(value)
        return attrs

    @staticmethod
    def build_subgraph(op_type):
        """Define the subgraph

        Args:
            op_type (str): operation type to build

        Returns:
            list of NodeProto: the operation sequence.
        """
        raise NotImplementedError("Child must implement this function")

    def _add_weight(self, name, value=[], dtype="float32"):
        """Add a new weight into the object.

        Note:
            Weights have to be created on child in __init__.
        """
        self._weights[name] = np.array(value, dtype)

    def set_weight(self, name, value):
        """Set a weights that can be extracted from the float model

        Args:
            name (str): the weight to modify
            value (np.ndarray): the new value
        """
        assert isinstance(value, np.ndarray), f"Expected {value} is a numpy array."
        if name not in self.weights:
            raise ValueError(f"{self.name} ({self.base_name}) does not recognize '{name}'. "
                             f"Availables: {list(self.weights)}")
        if value.dtype != self.weights[name].dtype:
            raise ValueError(f"{self.base_name}/{name} does not match with expected type "
                             f"({self._weights[name].dtype}). Receives {value.dtype}")
        self._weights[name] = value

    def __build__(self, *input_tensor_shapes, downscale=True):
        """Build weights and compute the output shape

        Args:
            *input_tensor_shapes (tuple): the input shapes and types
            downscale (bool, optional): whether to apply downscale operation. Defaults to True.

        Returns:
            tuple: the output shape and type
        """
        raise NotImplementedError("Child must implement this function")

    def build(self, *inputs_vi, out_name=None, downscale=True):
        """Build the layer in several steps:

        1. Build extra weights, needed at quantization time.
        2. Check weights integrity given the input shape.
        3. Compute output shape.

        Args:
            inputs_vi (list of ValueInfoProto): list of inputs value info.
            out_name (str, optional): the output tensor name. Defaults to None.
            downscale (bool, optional): whether to apply downscale operation,
                which will change the output type. Defaults to True.
        """
        assert all(isinstance(x, ValueInfoProto) for x in inputs_vi)
        # Replace empty name
        if not self.name:
            self.name = str(uuid.uuid4())
        # Convert ValueInfoProto into TensorShape
        input_ts = [value_info_to_tensor_shape(x) for x in inputs_vi]
        if len(inputs_vi) > 0:
            self._input = inputs_vi
        output_ts = self.__build__(*input_ts, downscale=downscale)
        self._output = make_tensor_value_info(out_name or self.name,
                                              elem_type=np_dtype_to_tensor_dtype(output_ts.dtype),
                                              shape=output_ts.shape)
        # Special weights: each qlayer must have an output scale and (potentially) a zero point.
        # But the zero point type may change depending on the layer type.
        # That is why we add it only if child did not do it
        scale_zp_shape = output_ts.shape[1]
        self._add_weight("scale", value=np.ones(scale_zp_shape), dtype="float64")
        if "zero_point" not in self.weights:
            self._add_weight("zero_point", value=np.zeros(scale_zp_shape), dtype="int8")

    def __quantize__(self, *qlayers, out_tensor_range, force_fp=False):
        """Build weights and compute the output scale

        Args:
            qlayers (list of OnnxLayer): the input layers. Input scales and zero points
                will be deduced from these.
            out_tensor_range (TensorData): the ranges computed by calibration.
            force_fp (bool, optional): whether to force output scale as a power-of-two.
                Defaults to False.

        Returns:
            tuple: quantized weights and output scale
        """
        raise NotImplementedError("Child must implement this function")

    def quantize(self, *qlayers, out_tensor_range, force_fp=False, downscale=True):
        """Quantize the float weights given a set of input scales and zero points.

        Args:
            qlayers (list of OnnxLayer): the input layers. Input scales and zero points
                will be deduced from these.
            out_tensor_range (TensorData): the ranges computed by calibration.
            force_fp (bool, optional): whether to force output scale as a power-of-two.
                Defaults to False.
            downscale (bool, optional): whether to apply downscale operation,
                which will change the output type. Defaults to True.

        Returns:
            NodeProto, list of TensorProto: serialized objects to build the ONNX graph.
        """
        if self._output is None or self._input is None:
            # Build the layer if required
            input_ts = [qly.output for qly in qlayers]
            self.build(*input_ts, downscale=downscale)
        # Quantize weights
        qweights, output_scale = self.__quantize__(*qlayers,
                                                   out_tensor_range=out_tensor_range,
                                                   force_fp=force_fp)
        # Save output scale to be recovered for next qlayer
        self.set_weight("scale", output_scale)
        # Return ONNX node and weights
        inputs = [ts.name for ts in self._input] + list(qweights)
        onnx_node = self.make_node(inputs, [self.output.name])
        onnx_weights = array_to_tp(**qweights)
        # Although output scale is not used in the operation chain, we store it as
        # an attribute to allow us to dequantize the output at any time.
        onnx_node.attribute.append(to_field("scale", self.weights["scale"]))
        return onnx_node, onnx_weights

    def make_node(self, inputs, outputs):
        """Return the NodeProto, setting the attributes.

        Args:
            inputs (list of str): list of input names.
            outputs (list of str): list of output names.

        Returns:
            NodeProto: the corresponding node.
        """
        # Build the subgraph (implemented in derived classes) and register subgraph
        # to make it available, unless previously registered already
        nodes = self.build_subgraph(self.op_type)
        inputs_fn, outputs_fn, attributes_fn = infer_function_parameters(nodes)
        func = make_function(domain=DOMAIN,
                             fname=self.op_type,
                             inputs=inputs_fn,
                             outputs=outputs_fn,
                             nodes=nodes,
                             opset_imports=[make_opsetid("", onnx_opset_version())],
                             attributes=attributes_fn)
        register_new_subgraph(func)

        # Return the node with corresponding attributes
        node = make_node(self.op_type, inputs, outputs, self.name, domain=DOMAIN)
        consume_attrs = [attr for attr in self.attribute if attr.name in func.attribute]
        node.attribute.extend(consume_attrs)
        return node
