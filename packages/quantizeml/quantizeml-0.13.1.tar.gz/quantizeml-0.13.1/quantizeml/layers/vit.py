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

__all__ = ["ClassToken", "QuantizedClassToken",
           "AddPositionEmbs", "QuantizedAddPositionEmbs",
           "ExtractToken", "QuantizedExtractToken"]

import keras
import tensorflow as tf

from .layers_base import (register_quantize_target, register_no_output_quantizer, rescale_outputs,
                          tensor_inputs, register_aligned_inputs, apply_buffer_bitwidth,
                          QuantizedLayer)
from .quantizers import AlignedWeightQuantizer, OutputQuantizer
from ..tensors import QFloat, FixedPoint


@keras.saving.register_keras_serializable()
class ClassToken(keras.layers.Layer):
    """Append a class token to an input layer.

    Args:
        initializer (keras.initializers.Initializer): Initializer for the class
            variable. Defaults to None.
    """

    def __init__(self, *args, initializer=None, **kwargs):
        super().__init__(*args, **kwargs)
        if initializer is None:
            initializer = keras.initializers.TruncatedNormal(stddev=0.02)
        self.initializer = initializer

    def build(self, input_shape):
        # Ensure variables are build with the appropriate name
        with tf.name_scope(self.name + '/'):
            super().build(input_shape)
            self.hidden_size = input_shape[-1]
            self.cls = tf.Variable(
                name="cls",
                initial_value=self.initializer(
                    shape=(1, 1, self.hidden_size), dtype="float32"),
                trainable=True,
            )

    def call(self, inputs):
        batch_size = tf.shape(inputs)[0]
        cls_broadcasted = tf.cast(
            tf.broadcast_to(self.cls, [batch_size, 1, self.hidden_size]),
            dtype=inputs.dtype,
        )
        return tf.concat([cls_broadcasted, inputs], 1)


@keras.saving.register_keras_serializable()
class AddPositionEmbs(keras.layers.Layer):
    """Adds (optionally learned) positional embeddings to the inputs.

    Args:
        initializer (keras.initializers.Initializer): Initializer for the class
            variable. Defaults to None.
    """

    def __init__(self, *args, initializer=None, **kwargs):
        super().__init__(*args, **kwargs)
        if initializer is None:
            initializer = keras.initializers.TruncatedNormal(stddev=0.02)
        self.initializer = initializer

    def build(self, input_shape):
        assert len(
            input_shape) == 3, f"Number of dimensions should be 3, got {len(input_shape)}"
        # Ensure variables are build with the appropriate name
        with tf.name_scope(self.name + '/'):
            super().build(input_shape)
            self.pe = tf.Variable(
                name="pos_embedding",
                initial_value=self.initializer(
                    shape=(1, input_shape[1], input_shape[2])),
                dtype="float32",
                trainable=True,
            )

    def call(self, inputs):
        return inputs + tf.cast(self.pe, dtype=inputs.dtype)


@register_quantize_target(ClassToken)
@register_no_output_quantizer
@keras.saving.register_keras_serializable()
class QuantizedClassToken(QuantizedLayer, ClassToken):
    """Quantize the :class:`ClassToken` layer, allowing quantization of the output.

    Args:
        quant_config (dict, optional): the serialized quantization configuration. Defaults to None.
    """

    def __init__(self, *args, quant_config=None, **kwargs):
        super().__init__(*args, quant_config=quant_config, **kwargs)
        cls_quantizer_cfg = self.quant_config.get("cls_quantizer", {})
        self.cls_quantizer = AlignedWeightQuantizer(name="cls_quantizer", **cls_quantizer_cfg)
        self.buffer_bitwidth = apply_buffer_bitwidth(self.quant_config, signed=True)

    @tensor_inputs([QFloat])
    def call(self, inputs):
        batch_size = tf.shape(inputs.values)[0]

        # Quantize the token and align it with the inputs
        cls = self.cls_quantizer(self.cls, inputs)

        # We need to broadcast the token along the batch size and set its token dimension to 1
        cls_broadcasted = tf.broadcast_to(cls, [batch_size, 1, self.hidden_size])

        return tf.concat([cls_broadcasted, inputs], 1)


@register_quantize_target(AddPositionEmbs)
@keras.saving.register_keras_serializable()
class QuantizedAddPositionEmbs(QuantizedLayer, AddPositionEmbs):
    """Quantize the :class:`AddPositionEmbs` layer, allowing operations in FixedPoint domain.

    Args:
        quant_config (dict, optional): the serialized quantization configuration. Defaults to None.
    """

    def __init__(self, *args, quant_config=None, **kwargs):
        super().__init__(*args, quant_config=quant_config, **kwargs)
        out_quant_cfg = self.quant_config.get("output_quantizer", False)
        if out_quant_cfg:
            self.out_quantizer = OutputQuantizer(
                name="output_quantizer", **out_quant_cfg)
        else:
            self.out_quantizer = None
        pe_quantizer_cfg = self.quant_config.get("pe_quantizer", {})
        self.pe_quantizer = AlignedWeightQuantizer(name="pe_quantizer", **pe_quantizer_cfg)
        self.buffer_bitwidth = apply_buffer_bitwidth(self.quant_config, signed=True)

    @tensor_inputs([QFloat])
    @rescale_outputs
    def call(self, inputs):
        # Quantize position embeddings and align them on the inputs
        pe = self.pe_quantizer(self.pe, inputs)

        # Add position embeddings
        return inputs + pe


@keras.saving.register_keras_serializable()
class ExtractToken(keras.layers.Layer):
    """ Wrapper class of `tf.gather` operation that allows to extract a Token.

    Args:
        token (int): the indice of the token to extract.
        axis (int, optional): axis over which the user gather the token. Defaults to 1.

    """

    def __init__(self, *args, token, axis=1, **kwargs):
        super().__init__(*args, **kwargs)
        self.token = token
        self.axis = axis

    def call(self, inputs):
        return tf.gather(inputs, self.token, axis=self.axis)

    def get_config(self):
        config = super().get_config()
        config.update({"token": self.token})
        config.update({"axis": self.axis})
        return config


@register_quantize_target(ExtractToken)
@register_no_output_quantizer
@register_aligned_inputs
@keras.saving.register_keras_serializable()
class QuantizedExtractToken(QuantizedLayer, ExtractToken):
    """ Quantized version of the ExtractToken layer. Accepts only FixedPoint inputs.
    """

    @tensor_inputs([FixedPoint])
    def call(self, inputs):
        return tf.gather(inputs, self.token, axis=self.axis)

    def get_config(self):
        return ExtractToken.get_config(self)
