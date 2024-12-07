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

__all__ = ["AlignedWeightQuantizer"]

import tensorflow as tf
import keras

from ...tensors import QFloat
from ..recorders import TensorRecorder, QFloatRecorder
from .quantizers import Quantizer


@keras.saving.register_keras_serializable()
class AlignedWeightQuantizer(Quantizer):
    """A uniform quantizer that converts a float Tensor to a QFloat representation.

    Unlike its sibling the WeightQuantizer, it does not evaluate the fractional bits and scales of
    the resulting QFloat, but instead aligns them on those of another QFloat input.

    Args:
        bitwidth (int, optional): the quantization bitwidth. Defaults to 8.
        signed (bool, optional): whether the quantizer expects signed values or unsigned.
            Defaults to True.
    """

    def __init__(self, bitwidth=8, signed=True, **kwargs):
        super().__init__(bitwidth, signed, **kwargs)
        # Add the object that will store the shift values.
        self.shift = TensorRecorder(self.name + "/shift")
        self.qweights = QFloatRecorder(self.name + "/qweights")

    def call(self, inputs, other):
        """Quantize the float inputs, aligned on another QFloat

        The quantization is done in several steps:

            1. Compute the quantization ranges,
            2. Evaluate the maximum fractional bits,
            3. Quantize the inputs as a QFloat,
            4. Align the QFloat fractional bits on the other.

        Args:
            inputs (tf.Tensor): the inputs tensor.
            other (:obj:`QFloat`): a tensor to align on.

        Returns:
            :obj:`QFloat`: a quantized tensor with the same scales and frac_bits as other.
        """
        if not isinstance(inputs, (tf.Tensor, tf.Variable)):
            raise ValueError(
                f"{type(inputs)} as first param is not supported."
                "AlignedWeightQuantizer only accepts tf.Tensor.")
        if not isinstance(other, QFloat):
            raise ValueError(
                f"{type(other)} as second param is not supported."
                "AlignedWeightQuantizer only accepts QFloat.")

        other_value_bits = other.fp.value_bits
        other_frac_bits = other.fp.frac_bits

        # Compute the symmetric quantization ranges from the inputs. When the bitwidth
        # is greater than 4 (e.g. 8 bits), experimentations have shown that models quantized
        # per axis (especially for the bias) have a better performance.
        # However for the 4bits, the performance was lower if we quantize per axis that's why
        # we keep it per tensor.
        if self.bitwidth > 4:
            # if the inputs are 0D or 1D vector, the ranges will have the same shape as the inputs.
            # In the other case for 2D or 3D (e.g. PositionEmbs), we reduce all axis
            # except the last.
            ndims = len(tf.shape(inputs))
            axis = list(range(ndims - 1))
        else:
            axis = None

        ranges = tf.math.reduce_max(tf.math.abs(inputs), axis=axis)
        # Evaluate the maximum fractional bits we can use for the specified ranges
        frac_bits = QFloat.max_frac_bits(self.value_bits, ranges, other.scales)
        # Remove the input-dependent fractional bits from the gradient tape to avoid a loopback
        frac_bits = tf.stop_gradient(frac_bits)
        # Clamp the ideal frac_bits to the other fractional bits, to avoid downscaling afterwards
        frac_bits = tf.minimum(frac_bits, other_frac_bits)
        # Quantize the inputs with the resulting fractional bits and other scales
        outputs = QFloat.quantize(inputs, self.value_bits, other.scales, frac_bits)
        # Now, upscale to the other fractional bits
        outputs, shift = outputs.upscale(other_frac_bits, other_value_bits)
        # record quantized weights (including shift and promote)
        self.qweights(outputs)
        # record shift values to be able to recreate and store unshifted weights
        self.shift(shift)
        return outputs
