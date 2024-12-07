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

__all__ = ["Add", "QuantizedAdd", "QuantizedConcatenate"]

import keras
import tensorflow as tf

from .layers_base import (register_quantize_target, register_no_output_quantizer,
                          register_aligned_inputs, apply_buffer_bitwidth, QuantizedLayer)
from .quantizers import OutputQuantizer
from .recorders import TensorRecorder
from ..tensors import FixedPoint


@keras.saving.register_keras_serializable()
class Add(keras.layers.Layer):
    """Wrapper class of `keras.layers.Add` that allows to average inputs.

    We only support a tuple of two inputs with the same shape.

    Args:
        average (bool, optional): if `True`, compute the average across all inputs.
            Defaults to `False`.
        activation (bool, optional): If `True`, apply an activation function after
            the addition. Defaults to `False`.
    """

    def __init__(self, *args, average=False, activation=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.average = average
        self.activation = activation

    def build(self, input_shape):
        if not isinstance(input_shape, (list, tuple)) or len(input_shape) != 2:
            raise ValueError(f"{self.__class__.__name__} expects two input tensors")
        super().build(input_shape)

    def call(self, inputs):
        a, b = inputs
        output = tf.add(a, b)
        if self.average:
            output /= 2
        if self.activation:
            output = tf.nn.relu(output)
        return output

    def get_config(self):
        config = super().get_config()
        config["average"] = self.average
        config["activation"] = self.activation
        return config


# Note that keras.layers.Add is not registered as a quantized target because the class name 'Add' is
# enough and shared between Keras and QuantizeML
@register_quantize_target(Add)
@register_aligned_inputs
@keras.saving.register_keras_serializable()
class QuantizedAdd(QuantizedLayer, Add):
    """Sums two inputs and quantize the output.

    The two inputs must be provided as a list or tuple of FixedPoint or Tensors.

    The outputs are quantized according to the specified quantization configuration.

    Args:
        quant_config (dict, optional): the serialized quantization configuration. Defaults to None.
    """

    def __init__(self, *args, quant_config=None, **kwargs):
        super().__init__(*args, quant_config=quant_config, **kwargs)
        self.buffer_bitwidth = apply_buffer_bitwidth(self.quant_config, signed=True)
        out_quant_cfg = self.quant_config.get("output_quantizer", False)
        if out_quant_cfg:
            self.out_quantizer = OutputQuantizer(
                name="output_quantizer", **out_quant_cfg)
        else:
            self.out_quantizer = None
        # Add objects that will store the shift values.
        self.a_shift = TensorRecorder(self.name + "/a_shift")
        self.b_shift = TensorRecorder(self.name + "/b_shift")

    def _quantized_relu(self, inputs):
        # Inputs are always fixed points (as they come after an Add or after an output quantizer)
        # we can then represent the zero as a fixed point
        zero = FixedPoint(tf.constant(0.), inputs.value_bits, inputs.frac_bits)
        # ReLU inside the Add is always unbounded so we just remove negative values
        return tf.math.maximum(inputs, zero)

    def call(self, inputs):
        a, b = inputs
        if not (isinstance(a, FixedPoint) and isinstance(b, FixedPoint)):
            # If any of the inputs is not a FixedPoint, raise an error
            raise TypeError(f"QuantizedAdd only accepts FixedPoint\
                              inputs. Receives {(type(a), type(b))} inputs.")

        # Align intermediate inputs before adding them
        a, shift_ab = a.align(b, self.buffer_bitwidth)
        b, shift_ba = b.align(a, self.buffer_bitwidth)

        outputs = tf.add(a, b)
        if self.average:
            outputs = outputs >> 1

        # Compute shifts
        self.a_shift(shift_ab)
        self.b_shift(shift_ba)

        # Rescale outputs
        if self.out_quantizer is not None:
            outputs = self.out_quantizer(outputs)

        # Apply activation
        if self.activation:
            outputs = self._quantized_relu(outputs)

        return outputs


@register_quantize_target(keras.layers.Concatenate)
@register_no_output_quantizer
@register_aligned_inputs
@keras.saving.register_keras_serializable()
class QuantizedConcatenate(QuantizedLayer, keras.layers.Concatenate):
    """ A Concatenate layer that operates on quantized inputs
    """

    def call(self, inputs):
        a, b = inputs
        if not (isinstance(a, FixedPoint) and isinstance(b, FixedPoint)):
            # If any of the inputs is not a FixedPoint, raise an error
            raise TypeError(f"QuantizedConcatenate only accepts FixedPoint\
                              inputs. Receives {(type(a), type(b))} inputs.")

        return tf.concat([a, b], axis=self.axis)
