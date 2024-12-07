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

__all__ = ["WeightQuantizer"]

import tensorflow as tf
import keras

from ...tensors import QTensor, QFloat, FixedPoint
from ..recorders import QFloatRecorder, FixedPointRecorder
from .quantizers import Quantizer


@keras.saving.register_keras_serializable()
class WeightQuantizer(Quantizer):
    """A uniform quantizer that converts a float Tensor to a QFloat representation.

    In order, the WeightQuantizer:

        - evaluates the scales required to align the values on optimal ranges for FixedPoint
          quantization,
        - quantizes the rescaled Tensor as a FixedPoint and returns a QFloat.

    Args:
        bitwidth (int, optional): the quantization bitwidth, defaults to 4.
        signed (bool, optional): whether the quantizer expects signed values or unsigned.
            Defaults to True.
        axis (int, optional): the quantization range is a scalar (None) or a vector corresponding to
            the given axis. Defaults to -1.
        fp_quantizer (bool, optional): True to enable FixedPoint quantization, QFloat otherwise.
            Defaults to False.
    """

    def __init__(self, bitwidth=4, signed=True, axis=-1, fp_quantizer=False, **kwargs):
        super().__init__(bitwidth, signed, **kwargs)
        self.axis = axis
        self.fp_quantizer = fp_quantizer
        qw_name = self.name + "/qweights"
        if self.fp_quantizer:
            self.qweights = FixedPointRecorder(qw_name)
        else:
            self.qweights = QFloatRecorder(qw_name)

    def build(self, input_shape):
        """Build the layer.

        Args:
            input_shape (list): the shape of input tensor.
        """
        super().build(input_shape)
        # Convert axis to a list of int
        if self.axis is not None and len(input_shape) > 1:
            axis_list = list(range(len(input_shape)))
            positive_axis = self.axis if self.axis >= 0 else len(axis_list) + self.axis
            if positive_axis < 0 or positive_axis > len(axis_list) - 1:
                raise ValueError(f"Axis {self.axis} is not valid in {self.name}.")
            axis_list.pop(positive_axis)
            self._axis = axis_list
        else:
            self._axis = None

    def call(self, inputs):
        """Quantize the float inputs

        The quantization is done in two steps:

            1. Compute the quantization ranges,
            2. Quantize the inputs.

        Args:
            inputs (tf.Tensor): the inputs tensor.

        Returns:
            :obj:`QFloat`: the quantized tensor.
        """
        if isinstance(inputs, QTensor):
            raise ValueError(
                f"{type(inputs)} input is not supported. WeightQuantizer only accepts float"
                " inputs.")

        # Compute the quantization ranges from the inputs
        ranges = tf.math.reduce_max(tf.math.abs(inputs), self._axis)
        if self.axis in [-2, 2] and inputs.shape[-1] == 1 and len(inputs.shape) > 2:
            # Expand the shape of the ranges so that it is broacastable on the inputs
            ranges = tf.expand_dims(ranges, -1)

        if self.fp_quantizer:
            # Build a FixedPoint when scale is disabled
            frac_bits = tf.stop_gradient(FixedPoint.max_frac_bits(self.value_bits, ranges))
            qweights = FixedPoint.quantize(inputs, self.value_bits, frac_bits)
        else:
            # Evaluate the scales to align on the optimal quantization ranges
            scales = QFloat.optimal_scales(ranges, self.value_bits)
            # Clip scales lower bound to avoid quantizing very tiny values. Minimum is defined
            # as 1e-6, value low enough to be considered as zero.
            scales = tf.maximum(scales, 1e-6)
            # Since we use the optimal quantization ranges [-int_max -1, int_max], the inner
            # FixedPoint can be quantized with exactly zero fractional bits
            qweights = QFloat.quantize(inputs, self.value_bits, scales, 0.)
        # Record the quantized weights (it does nothing if recording is disabled)
        self.qweights(qweights)
        return qweights

    def get_config(self):
        """Get the config of the layer.

        Returns:
            dict: the config of the layer.
        """
        config = super().get_config()
        config.update({"axis": self.axis, "fp_quantizer": self.fp_quantizer})
        return config
