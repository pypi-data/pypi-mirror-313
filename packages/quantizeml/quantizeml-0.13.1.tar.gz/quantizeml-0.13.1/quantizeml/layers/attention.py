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

__all__ = ["Attention", "string_to_softmax", "QuantizedAttention"]

import keras
import tensorflow as tf

from .layers_base import (register_quantize_target, register_aligned_inputs, apply_buffer_bitwidth,
                          QuantizedLayer)
from .reshaping import QuantizedReshape, QuantizedPermute
from .shiftmax import shiftmax, QuantizedShiftmax
from .recorders import TensorRecorder
from .quantizers import OutputQuantizer
from ..tensors import FixedPoint, round_log2, pow2


def string_to_softmax(s):
    """
    Convert a string to a softmax function.
    Available options are 'softmax' for standard softmax, 'shiftmax' for
    shiftmax.

    Args:
        s (str): string to convert.

    Returns:
        A softmax function.
    """
    if s == "softmax":
        return tf.nn.softmax
    if s in ("softmax2", "shiftmax"):
        return shiftmax

    raise NotImplementedError("softmax should be in ['softmax', 'shiftmax']"
                              f" but received {s}.")


@keras.saving.register_keras_serializable()
class Attention(keras.layers.Layer):
    """Dot-product attention layer with configurable softmax.

    Inputs are a tuple of tensors:

    - a query tensor of shape [batch, tokens, hidden],
    - a key tensor of shape [batch, tokens, hidden],
    - a value tensor of shape [batch, tokens, hidden].

    The calculation follows the steps:

    1. Split query, key, value per attention heads

        q, k, v : [batch, tokens, hidden] -> [batch, token, num_heads, dim]

    2. Calculate cross-token scores as a query-key dot product:

        scores = tf.matmul(query, key, transpose_b=True)

        scores : [batch, num_heads, token, token]

    3. Rescale score by dividing by the squared-root of dim.

    4. Use scores to calculate a mask

        mask = softmax(scores)

    5. Combine mask with value

        output = tf.matmul(mask, value)

        output: [batch, num_heads, token, dim]

    6. Merge heads to get back to 2D

        output: [batch, num_heads, token, dim] -> [batch, token, hidden]

    Args:
        num_heads (int): the number of attention heads
        softmax (str, optional): 'softmax' or 'shiftmax'. Defaults to 'softmax'

    """

    def __init__(self, num_heads, softmax="softmax", **kwargs):
        super().__init__(**kwargs)
        self.num_heads = num_heads
        self.softmax = softmax
        self.softmax_op = string_to_softmax(self.softmax)

    def build(self, input_shape):
        super().build(input_shape)
        assert len(input_shape) == 3
        self.hidden_size = input_shape[0][-1]
        if self.hidden_size % self.num_heads != 0:
            raise ValueError(
                f"Embedding dimension = {self.hidden_size} should be divisible"
                f" by number of heads = {self.num_heads}"
            )
        self.dim = self.hidden_size // self.num_heads

        # Attention replace score / scale by a shift.
        # For that, we need to calculate the shift_scale
        scale = tf.math.sqrt(tf.cast(self.dim, dtype=tf.float32))
        self.scale_shift = round_log2(scale)

    def separate_heads(self, x):
        x = keras.layers.Reshape((-1, self.num_heads, self.dim))(x)
        return keras.layers.Permute((2, 1, 3))(x)

    def call(self, inputs):
        # Separate 2D embeddings per head to obtain 3D inputs
        query = self.separate_heads(inputs[0])
        key = self.separate_heads(inputs[1])
        value = self.separate_heads(inputs[2])
        # Dot product query and key for each head and pairs of tokens
        score = tf.matmul(query, key, transpose_b=True)
        # Rescale the corresponding score, dividing it by 2**scale_shift
        scaled_score = score * pow2(-self.scale_shift)
        # Apply the configurable softmax operation
        mask = self.softmax_op(scaled_score, axis=-1)
        # Combine each score with value to obtain new embeddings per tokens
        output = tf.matmul(mask, value)
        # Join heads to get back to 2D embeddings per token
        output = keras.layers.Permute((2, 1, 3))(output)
        output = keras.layers.Reshape((-1, self.hidden_size))(output)
        return output, mask

    def get_config(self):
        config = super().get_config()
        softmax = self.softmax
        if self.softmax == 'softmax2':
            # softmax2 is the legacy name, use shiftmax now
            softmax = 'shiftmax'
        config.update(
            {
                "num_heads": self.num_heads,
                "softmax": softmax
            }
        )
        return config


@register_quantize_target(Attention)
@register_aligned_inputs
@keras.saving.register_keras_serializable()
class QuantizedAttention(QuantizedLayer, Attention):
    """An Attention layer that operates on quantized inputs

    Args:
        num_heads (int): the number of attention heads
        quant_config (dict, optional): the serialized quantization configuration. Defaults to None.
        softmax (str, optional): 'softmax' or 'shiftmax'. Defaults to 'shiftmax'
    """
    arg_constraints = {'softmax': 'shiftmax'}

    def __init__(self, num_heads, quant_config=None, softmax='shiftmax', **kwargs):
        super().__init__(num_heads=num_heads, softmax=softmax, quant_config=quant_config, **kwargs)

        out_quant_cfg = self.quant_config.get("output_quantizer", False)
        if out_quant_cfg:
            self.out_quantizer = OutputQuantizer(
                name="output_quantizer", **out_quant_cfg)
        else:
            self.out_quantizer = None

        # Override softmax operation
        softmax_quant_conf = self.quant_config.get("softmax", None)
        self.softmax_op = QuantizedShiftmax(
            quant_config=softmax_quant_conf, name="quantized_softmax")
        self.buffer_bitwidth = apply_buffer_bitwidth(self.quant_config, signed=True)
        # Add objects that will store the shift values.
        self.values_shift = TensorRecorder(self.name + "/value_shift")

    def separate_heads(self, x):
        x = QuantizedReshape((-1, self.num_heads, self.dim))(x)
        return QuantizedPermute((2, 1, 3))(x)

    def call(self, inputs):
        if any(not isinstance(x, FixedPoint) for x in inputs):
            # If any of the inputs is not a FixedPoint, raise an error
            raise ValueError("QuantizedAttention only accepts FixedPoint inputs")
        # Separate 2D embeddings per head to obtain 3D inputs
        query = self.separate_heads(inputs[0])
        key = self.separate_heads(inputs[1])
        # Expand the values to a higher bitwidth to avoid saturation and align them
        value, vshift = inputs[2].expand(self.buffer_bitwidth)
        self.values_shift(vshift)
        value = self.separate_heads(value)
        # Promote query to avoid saturation
        query = query.promote(self.buffer_bitwidth)
        # Dot product query and key for each head and pairs of tokens
        score = tf.matmul(query, key, transpose_b=True)
        # Rescale the corresponding score, dividing it by 2**scale_shift
        scaled_score = score >> self.scale_shift
        # Apply the configurable softmax operation
        mask = self.softmax_op(scaled_score)
        # Promote mask to make sure we don't overflow
        mask = mask.promote(self.buffer_bitwidth)
        # Combine each score with value to obtain new embeddings per tokens
        output = tf.matmul(mask, value)
        # Join heads to get back to 2D embeddings per token
        output = QuantizedPermute((2, 1, 3))(output)
        output = QuantizedReshape((-1, self.hidden_size))(output)
        # Refine output bitwidth precision if needed
        if self.out_quantizer is not None:
            output = self.out_quantizer(output)
        return output, mask
