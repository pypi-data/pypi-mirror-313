#!/usr/bin/env python
# ******************************************************************************
# Copyright 2022 Brainchip Holdings Ltd.
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

__all__ = ["hard_silu", "QuantizedReLU", "QuantizedActivation"]

import os
import numpy as np
import tensorflow as tf
import keras

from .layers_base import (register_quantize_target, rescale_outputs, register_aligned_inputs,
                          tensor_inputs, apply_buffer_bitwidth, QuantizedLayer)
from .quantizers import AlignedWeightQuantizer, OutputQuantizer
from .recorders import NonTrackVariable
from ..tensors import FixedPoint, QFloat, QTensor

LUT_ENV = "LUT_ENABLED"


@keras.saving.register_keras_serializable()
def hard_silu(x):
    """Hard SiLU activation function, also known as Hard Swish.

    It is defined as:

    - `0` if `if x < -3`
    - `x` if `x > 3`
    - `x * (x + 3) / 6` if `-3 <= x <= 3`

    It's a faster, piecewise linear approximation of the silu activation.

    Args:
        x(tf.Tensor): Input tensor.

    Returns:
        tf.Tensor: Output tensor.

    Reference:
        [A Howard, 2019](https://arxiv.org/abs/1905.02244)
    """
    return x * tf.nn.relu6(x + 3) / 6


@register_quantize_target(keras.layers.ReLU)
@keras.saving.register_keras_serializable()
class QuantizedReLU(QuantizedLayer):
    """Quantized version of the ReLU activation layer applicable on FixedPoint tensor.

    Args:
        max_value (float, optional): ReLU maximum value. Defaults to 6.
        quant_config (dict, optional): the serialized quantization configuration. Defaults to None.
    """
    arg_constraints = {
        'negative_slope': 0,
        'threshold': 0}
    ignored_args = ['negative_slope', 'threshold']

    def __init__(self, *args, max_value=6, quant_config=None, **kwargs):
        super().__init__(*args, quant_config=quant_config, **kwargs)

        # Use quant_config to build quantizers
        out_quant_cfg = self.quant_config.get("output_quantizer", False)
        if out_quant_cfg:
            self.out_quantizer = OutputQuantizer(name="output_quantizer", **out_quant_cfg)
        else:
            self.out_quantizer = None
        self.buffer_bitwidth = apply_buffer_bitwidth(self.quant_config, signed=False)
        if max_value is not None:
            # Store max_value
            if isinstance(max_value, np.ndarray):
                max_value = max_value.item()
            max_value_quantizer_cfg = self.quant_config.get("max_value_quantizer", {})
            self.max_value_quantizer = AlignedWeightQuantizer(name="max_value_quantizer",
                                                              signed=False,
                                                              **max_value_quantizer_cfg)
        self.max_value = max_value

    @tensor_inputs([QTensor])
    @rescale_outputs
    def call(self, inputs):
        """ReLU activation function.

        In other terms:

            1. clip the value between 0 and :attr:`max_value`.
            2. quantize the output if an output_quantizer is set.

        Args:
            inputs (:obj:`QFloat`): the inputs tensor.

        Returns:
            :obj:`FixedPoint`: QuantizedReLU outputs.
        """
        if isinstance(inputs, FixedPoint):
            # if inputs is FixedPoint, create an equivalent QFloat with scale
            # set to 1
            inputs = QFloat(inputs, tf.constant(1.))
        # Express zero as a QFloat aligned with the inputs because this is what the
        # dispatched operations expect.
        # The actual hardware implementation will simply use a zero integer.
        zero = QFloat(FixedPoint(tf.constant(0.), inputs.fp.value_bits, inputs.fp.frac_bits),
                      inputs.scales)

        if self.max_value is None:
            # Just remove negative values
            return tf.math.maximum(inputs, zero)
        # Quantize and align max_value with the inputs
        max_value = self.max_value_quantizer(tf.cast(self.max_value, tf.float32), inputs)
        # Clip the inputs
        return tf.clip_by_value(inputs, zero, max_value)

    def get_config(self):
        config = super().get_config()
        config.update({"max_value": self.max_value})
        return config


@keras.saving.register_keras_serializable()
@register_quantize_target(keras.layers.Activation)
@register_aligned_inputs
class QuantizedActivation(QuantizedLayer, keras.layers.Activation):
    """Quantized version of `keras.layers.Activation` layer applicable on ``FixedPoint`` tensor.

    The input values are mapped through a look-up-table that simulates the activation behavior.

    Example
        >>> # Represent 2.5 as a FixedPoint
        >>> input = FixedPoint(5, value_bits=3, frac_bits=1)
        >>> # QuantizedActivation.call() maps `input` through the table to obtain
        >>> # an integer that represent the float value of tf.nn.gelu(2.5)
        >>> output = QuantizedActivation(activation="gelu")(input)
        >>> assert output.values == 80
        >>> # Or which is equivalent in float domain
        >>> max_error = 2 ** -(output.frac_bits + 1)
        >>> assert tf.abs(output.to_float() - tf.nn.gelu(2.5)) < max_error

    Args:
        activation (callable or str): Activation function. It could be a callable,
            or the name of an activation from the keras.activations namespace.
        quant_config (dict, optional): the serialized quantization configuration. Defaults to None.
    """
    arg_constraints = {'activation': lambda: ["gelu", "swish", "Custom>hard_silu"]}
    DEFAULT_INPUT_BITWIDTH = 11
    DEFAULT_LUT_BITWIDTH = 14

    def __init__(self, activation, *args, quant_config=None, **kwargs):
        super().__init__(activation, *args, quant_config=quant_config, **kwargs)

        # Retrieve quantization parameters
        if "lut_bitwidth" not in self.quant_config:
            self.quant_config["lut_bitwidth"] = self.DEFAULT_LUT_BITWIDTH
        self.lut_bits = self.quant_config["lut_bitwidth"] - 1

        # Use quant_config to build quantizers
        out_quant_cfg = self.quant_config.get("output_quantizer", False)
        if out_quant_cfg:
            self.out_quantizer = OutputQuantizer(name="output_quantizer", **out_quant_cfg)
        else:
            self.out_quantizer = None

        # Create dynamic table and variable to save output frac_bits
        self.values = tf.lookup.experimental.MutableHashTable(key_dtype=tf.int32,
                                                              value_dtype=tf.float32,
                                                              default_value=2**self.lut_bits + 1,
                                                              name="values_table")
        self.frac_bits = NonTrackVariable("frac_bits")

    @property
    def using_lut(self):
        """Flag to specify if the inference should be given through look-up-table approach

        Returns:
            bool: True if lut is enabled, False otherwise.
        """
        value = os.environ.get(LUT_ENV, "0")
        return value == "1"

    @tf.function
    def record_values_in_table(self, value_bits, frac_bits):
        """Generate a set of inputs and outputs to record the look-up-table.

        Inputs are generated in the full range based on ``value_bits``.

        Args:
            value_bits (int): bits to define the range of values to be generated.
            frac_bits (tf.Tensor): frac_bits to convert the generated values in a FixedPoint.

        Returns:
            tf.Tensor: the expected frac_bits representing the values contained in the table.
        """
        # Generates the full range values between [-(2 ** value_bits), 2 ** value_bits - 1].
        int_max = 2 ** value_bits
        values = tf.range(-int_max, int_max, dtype=tf.int32)
        inputs = FixedPoint(values, value_bits=value_bits, frac_bits=frac_bits)

        # Forward float inputs through activation
        x = inputs.to_float()
        y = self.activation(x)

        # Apply dynamic quantization to compute output integer values.
        range_max = tf.reduce_max(tf.abs(y))
        out_frac_bits = tf.stop_gradient(FixedPoint.max_frac_bits(self.lut_bits, range_max))
        outputs = FixedPoint.quantize(y, self.lut_bits, frac_bits=out_frac_bits)

        # Insert values in table
        self.values.insert(values, outputs.values)

        # Return the static output frac_bits
        return out_frac_bits

    @tensor_inputs([FixedPoint])
    @rescale_outputs
    def call(self, inputs):
        # Values stored in the table can only be calculated if the input is per_tensor
        if not inputs.per_tensor:
            raise TypeError(f"{self.__class__.__name__} only supports per-tensor inputs.")

        self.frac_bits.init_var(inputs.frac_bits)

        # Set values in table if table is empty (low computational cost)
        if self.values.size() == 0:
            out_frac_bits = self.record_values_in_table(inputs.value_bits, inputs.frac_bits)
            out_frac_bits = tf.stop_gradient(out_frac_bits)
            self.frac_bits.set_var(out_frac_bits)

        # Look-up-table has a high cost in inference.
        # It is possible to increase the speed if we avoid it through a
        # DeQuantization-reQuantization (DQ-Q) approach:
        if not self.using_lut:
            # 1. Dequantize the inputs
            x = inputs.to_float()
            # 2. Apply activation in float domain
            x = self.activation(x)
            # 3. Requantize from static quantization approach
            outputs = FixedPoint.quantize(x, value_bits=self.lut_bits, frac_bits=self.frac_bits.var)
        else:
            # Forward inputs.values into values table
            inputs = tf.cast(inputs.values, tf.int32)
            values = self.values.lookup(inputs)

            # MutableHashTable forgets the output shape. That is why we set it explicitly.
            values.set_shape(inputs.shape)

            # Build the output FixedPoint
            outputs = FixedPoint(values, value_bits=self.lut_bits, frac_bits=self.frac_bits.var)
        return outputs
