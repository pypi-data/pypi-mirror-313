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

__all__ = ["shiftmax", "Shiftmax", "QuantizedShiftmax"]

import tensorflow as tf
import keras

from .layers_base import (register_quantize_target, register_no_output_quantizer,
                          register_aligned_inputs, apply_buffer_bitwidth, QuantizedLayer)
from .recorders import TensorRecorder
from ..tensors import FixedPoint, floor_through, round_log2, pow2


def shiftmax(logits, axis=-1):
    """Computes softmax-like activations, but using base 2 for the exponential.

    Used as approximation of the softmax activation.

    This function performs the equivalent of

        >>>  logits = tf.floor(logits)
        >>>  exp = 2 ** logits
        >>>  sum_exp_shift = tf.round(tf.log2(tf.reduce_sum(exp, axis, keepdims=True)))
        >>>  softmax = exp / 2 ** sum_exp_shift = 2 ** (logits -  sum_exp_shift)


    When 2 ** :attr:`sum_exp_shift` is an approximated of sum_exp as a Power-of-Two (PoT)

    To avoid a high exponential (and a tf.inf representation by tensorflow), we adopt the
    following equivalence:

    Making the variable change :math:`y=logits-x0`, we reach the same result as
    :math:`p=shiftmax(logits)`, because,

    .. math::
        p' = \\frac{2^y}{sum(2^y)}
           = \\frac{2^{logits-x0}}{sum(2^{logits-x0})}
           = \\frac{2^{logits} * 2^{-x0}}{2^{-x0} * sum(2^{logits})}
           = \\frac{2^{logits}}{sum(2^{logits})}
           = p

    We take :math:`x0 = max(logits)`.

    Args:
        logits (tf.Tensor): a non-empty `Tensor`.
        axis (int, list, optional): the dimension shiftmax would be performed
            on. The default is -1 which indicates the last dimension.

    Returns:
        tf.Tensor: value of shiftmax function with the same type and shape as `logits`.

    Raises:
        InvalidArgumentError: if `logits` is empty or `axis` is beyond the last
            dimension of `logits`.

    Note:
        We floor the :attr:`logits` to approximate the results to those expected
        when quantizing the operation.
    """
    logits = floor_through(logits)
    logits = logits - tf.reduce_max(logits, axis=axis, keepdims=True)
    exp = tf.cast(2**logits, dtype=logits.dtype)
    sum_exp = tf.reduce_sum(exp, axis=axis, keepdims=True)
    sum_exp_shift = round_log2(sum_exp)
    return 2 ** (logits - sum_exp_shift)


@keras.saving.register_keras_serializable()
class Shiftmax(keras.layers.Layer):
    """Wrapper class of `shiftmax` function, that calculates a softmax-like
    activation.

    Note that shiftmax operation is performed always along the last axis.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def call(self, inputs):
        output = shiftmax(inputs)
        return output


@register_quantize_target(Shiftmax)
@register_no_output_quantizer
@register_aligned_inputs
@keras.saving.register_keras_serializable()
class QuantizedShiftmax(QuantizedLayer):
    """A quantized layer to do a quantized function similar to the softmax, but
    using base 2 instead of e. So we replace

    .. math:: softmax(x_i) = \\frac{e^{x_i}}{sum(e^{x_k})}

    With this:

    .. math:: softmax2(x_i) = \\frac{2^{x_i}}{sum(2^{x_k})}

    This approximation is close enough to the original function. In order to
    make it more hardware friendly, we also approximated the :math:`sum(2^{x_k})`
    to the closest power of two:

    .. math:: shiftmax(x_i) = \\frac{2^{x_i}}{2^{round(log2(sum(2^{x_k})))}}

    So it can be implemented with a simple shift operation.

    Implementation is inspired from this paper:

    Cardarilli, G.C., Di Nunzio, L., Fazzolari, R. et al.
    A pseudo-softmax function for hardware-based high speed image classification.
    Sci Rep 11, 15307 (2021). https://doi.org/10.1038/s41598-021-94691-7

    Args:
        quant_config (dict, optional): the serialized quantization configuration. Defaults to None.
    """

    def __init__(self, *args, quant_config=None, **kwargs):
        super().__init__(*args, quant_config=quant_config, **kwargs)
        self.buffer_bitwidth = apply_buffer_bitwidth(self.quant_config, signed=True)
        self.exp_bitwidth = self.quant_config.get("exp_bitwidth", 10)
        if self.buffer_bitwidth <= 2 * self.exp_bitwidth:
            raise ValueError(f"exp_bitwidth={self.exp_bitwidth} must be less than "
                             f"half of buffer_size={self.buffer_bitwidth}.")
        # Add objects that will store the shift values.
        self.input_shift = TensorRecorder(self.name + "/input_shift")

    def call(self, x):
        # Raise an error if the inputs are not FixedPoint
        if not isinstance(x, FixedPoint):
            raise TypeError("QuantizedShiftmax only accepts FixedPoint inputs. Receives "
                            f"{type(x)} inputs.")

        # To avoid overflowing, some modifications are made to the input.
        # First remove the fractional part of the input (floor(x)). We can do
        # this because the exponential function will return very big numbers,
        # so fractional ones can be ignored in the ratio with the sum.
        x, shift = x.floor()
        # update shift values if recording is enabled
        self.input_shift(shift)

        # Since x has been floored, we can directly use its values
        x = x.values

        # The pseudo-softmax is defined as:
        #
        # p = 2^x/sum(2^x)
        #
        # but we do this instead:
        #
        # p' = p = 2^y/sum(2^y)
        #
        # where
        #
        # y = x - x0
        #
        # because,
        #
        # p' = 2^y/sum(2^y) = 2^(x - x0)/sum(2^(x - x0)) = (2^x * 2^-x0)/(2^-x0 * sum(2^x))
        #    = 2^x/sum(2^x) = p
        #
        # On the other hand, we choose x0 to be the maximum of x, minus a positive
        # integer constant "exp_bitwidth". So now
        #
        # y = x - (max(x) - exp_bitwidth)
        #
        # This makes sure that y is never higher than exp_bitwidth
        x_max = tf.reduce_max(x, axis=-1, keepdims=True)
        x0 = x_max - self.exp_bitwidth
        y = x - x0

        # To evaluate exp = 2^y, we target a maximum precision of exp_bitwidth.
        # As a consequence, we will neglect all values that are below -exp_bitwidth,
        # considering:
        # - that they don't contribute much to the exponential sum,
        # - that they would be quantized to zero after the division.
        exp_values = tf.where(y >= -self.exp_bitwidth, pow2(y + self.exp_bitwidth), 0)
        # Note that we could do the operation directly on the values, but we store
        # values in a FixedPoint to make sure we don't saturate the underlying buffer
        exp = FixedPoint(exp_values, self.buffer_bitwidth, self.exp_bitwidth)
        # To calculate 2^y, hardware can just:
        # - set exp to zero if y < -exp_bitwidth,
        # - do a left shift applying a fixed offset of self.exp_bitwidth.
        # Example:
        #   exp_bitwidth = 4
        #   y = [-5, 3, -4, -1, 1]
        #   exp = [0, 1 << (4 + 3), 1 << (4 - 4), 1 << (4 - 1), 1 << (4 + 1)]
        #   exp = [0, 128, 1, 8, 32]

        # Calculate the sum of the exponential (saturation may happen here).
        sum_exp = tf.reduce_sum(exp, axis=-1, keepdims=True)

        # Like the float version, instead of dividing by sum_exp, we simply approximate
        # it to the closest integer log2 to perform a shift instead of a division.
        # Please refer to the description of round_log2 for a description of the hardware operation.
        # Note here that we need to substract the frac_bits as the values are scaled up.
        sum_exp_shift = round_log2(sum_exp.values) - sum_exp.frac_bits
        outputs = exp.shift(-sum_exp_shift)

        # Since sum_exp > exp, the results are between [0,1].
        # We can therefore rewrite the output as:
        return FixedPoint(outputs.values, self.exp_bitwidth + 1, self.exp_bitwidth)
