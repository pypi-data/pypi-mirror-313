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
"""
QuantizedSeparableConv2D layer definition.
"""

__all__ = ["QuantizedSeparableConv2D"]

import tensorflow as tf
import keras

from keras.layers import SeparableConv2D
from keras import backend

from .layers_base import (register_quantize_target, rescale_outputs, tensor_inputs,
                          neural_layer_init, register_aligned_inputs, QuantizedLayer)
from ..tensors import FixedPoint


@register_quantize_target(SeparableConv2D, has_weights=True)
@register_aligned_inputs
@keras.saving.register_keras_serializable()
class QuantizedSeparableConv2D(QuantizedLayer, SeparableConv2D):
    """ A separable convolutional layer that operates on quantized inputs and weights.

    Args:
        quant_config (dict, optional): the serialized quantization configuration. Defaults to None.
    """
    arg_constraints = {'depth_multiplier': 1}

    @neural_layer_init(True)
    def __init__(self, *args, quant_config=None, **kwargs):
        pass

    @tensor_inputs([FixedPoint, tf.Tensor])
    @rescale_outputs
    def call(self, inputs):
        # Although the dephwise operation does not require it, we only accept inputs quantized
        # per-tensor to avoid increasing too much the fractional bits of the depthwise outputs.
        inputs.assert_per_tensor()

        # Quantize the weights
        depthwise_kernel = self.dw_weight_quantizer(self.depthwise_kernel)
        pointwise_kernel = self.pw_weight_quantizer(self.pointwise_kernel)

        dw_outputs_q = backend.depthwise_conv2d(
            inputs,
            depthwise_kernel,
            strides=self.strides,
            padding=self.padding,
            dilation_rate=self.dilation_rate,
            data_format=self.data_format)

        outputs = tf.nn.convolution(
            dw_outputs_q,
            pointwise_kernel,
            strides=[1, 1, 1, 1],
            padding='VALID',
            data_format="NHWC" if self.data_format == "channels_last" else "NCHW")

        if self.use_bias:
            # Quantize bias and align it on the outputs
            bias = self.bias_quantizer(self.bias, outputs)
            outputs = tf.add(outputs, bias)

        return outputs
