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

__all__ = ["OutputQuantizer"]

import tensorflow as tf
import keras

from ...tensors import QTensor, FixedPoint, QFloat
from ..recorders import TensorRecorder, FixedPointRecorder
from .quantizers import Quantizer


@keras.saving.register_keras_serializable()
class OutputQuantizer(Quantizer):
    """A uniform FixedPoint quantizer that selects the optimal number of fractional bits for the
    range of its inputs and updates them accordingly.

    The typical use case is to decrease the bitwidth of the result of a quantized layer operation to
    avoid a saturation in downstream operations.

    If the input is a QFloat, it is converted to a FixedPoint before updating its bitwidth.

    Args:
        bitwidth (int, optional): the quantization bitwidth. Defaults to 8.
        signed (bool, optional): whether the quantizer expects signed values or unsigned.
            Defaults to True.
        axis (str, optional): the quantization range is a scalar ('per-tensor') or a vector
            corresponding to the last axis ('per-axis'). Defaults to 'per-tensor'.
        scale_bits: (int, optional): the bitwidth to use when quantizing output scales.
            Defaults to 8.
        buffer_bitwidth: (int, optional): buffer bitwidth value. Defaults to 32.
    """

    def __init__(self,
                 bitwidth=8,
                 signed=True,
                 axis="per-tensor",
                 scale_bits=8,
                 buffer_bitwidth=32,
                 **kwargs):
        super().__init__(bitwidth, signed, **kwargs)
        if not (isinstance(axis, str) and axis in ["per-tensor", "per-axis"]):
            raise ValueError(f"Only support reduction 'per-tensor' or 'per-axis'. Given {axis}.")
        self.axis = axis
        self.scale_bits = scale_bits
        self.buffer_bitwidth = buffer_bitwidth
        # Add object that will store the shift values.
        self.shift = TensorRecorder(self.name + "/shift")

    def build(self, input_shape):
        """Build the layer.

        Args:
            input_shape (list): the shape of input tensor.
        """
        super().build(input_shape)
        # Convert axis to a list of int
        if self.axis == "per-axis":
            ndims = len(input_shape)
            if ndims < 3:
                raise ValueError("OutputQuantizer cannot quantize per-axis tensors "
                                 " with 2 dimensions or less.")
            self._axis = list(range(len(input_shape) - 1))
        else:
            self._axis = None

        # Declares the constant/vector that will store the maximum values of the input.
        self.range_max = self.add_weight(
            name="range_max",
            shape=input_shape[-1] if self._axis is not None else (),
            dtype=tf.float32,
            initializer="ones",
            synchronization=tf.VariableSynchronization.ON_READ,
            trainable=False,
            aggregation=tf.VariableAggregation.MEAN,
            experimental_autocast=False,
        )

        # Declare a rescaling_rate variable that will be set at calibration and that will hold
        # cross-layer equalization ideal range_max / calibrated range_max ratio.
        self.rescaling_rate = self.add_weight(
            name="rescaling_rate",
            shape=input_shape[-1] if self._axis is not None else (),
            dtype=tf.float32,
            initializer="ones",
            synchronization=tf.VariableSynchronization.ON_READ,
            trainable=False,
            aggregation=tf.VariableAggregation.MEAN
        )

    @property
    def frac_bits(self):
        """ Compute and return the number of fractional bits for this OutputQuantizer.

        Returns:
           tf.Tensor: an integer tensor of fractional bits
        """
        return tf.stop_gradient(FixedPoint.max_frac_bits(self.value_bits, self.range_max))

    def call(self, inputs):
        """Quantize the QTensor inputs to a lower bitwidth.

        The quantization happens with the following steps:

            1. Evaluate the nearest power(s) of two containing the quantization range(s)
            2. Quantize the inputs.

        Args:
            inputs (:obj:`QTensor`): the inputs tensor.

        Returns:
            :obj:`FixedPoint`: the quantized tensor.
        """
        if not isinstance(inputs, QTensor):
            raise TypeError("The OutputQuantizer accepts only QTensor inputs."
                            f"Received {type(inputs)} inputs.")

        if isinstance(inputs, QFloat):
            if self.scale_bits is None:
                raise ValueError(f"{self.name} receives QFloat inputs: the scale_bits parameter"
                                 " needs to be specified.")
            inputs_value_bits = inputs.fp.value_bits
            # Apply cross layer equalization rescaling
            rescaled_inputs = QFloat(inputs.fp, inputs.scales * self.rescaling_rate)
            rescaled_inputs = rescaled_inputs.promote(self.buffer_bitwidth)
            inputs, qscales = rescaled_inputs.to_fixed_point(self.scale_bits)
            if getattr(self, 'qscales', None) is None:
                # From Keras documentation, any variable creation taking place in call
                # should be wrapped with tf.init_scope
                with tf.init_scope():
                    self.qscales = FixedPointRecorder(self.name + "/qscales")
            self.qscales(qscales)
        else:
            inputs_value_bits = inputs.value_bits

        if inputs_value_bits <= self.value_bits:
            msg = f"Quantizing a {inputs_value_bits}-bit QTensor to "\
                f"{self.value_bits}-bit is pointless."
            if inputs_value_bits < self.value_bits:
                msg += " Use a promotion instead."
            raise ValueError(msg)

        # Rescale to center around range_max and compress to a lower bitwidth
        inputs, shift_value = inputs.rescale(self.frac_bits, self.value_bits)
        # update shift values
        self.shift(shift_value)
        return inputs

    def get_config(self):
        """Get the config of the layer.

        Returns:
            dict: the config of the layer.
        """
        config = super().get_config()
        config.update({"scale_bits": self.scale_bits})
        config.update({"axis": self.axis})
        config.update({"buffer_bitwidth": self.buffer_bitwidth})
        return config
