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
QuantizedDepthwiseConv2D layer definition.
"""

__all__ = ["QuantizedDepthwiseConv2D", "DepthwiseConv2DTranspose",
           "QuantizedDepthwiseConv2DTranspose"]


import tensorflow as tf
import keras

from keras import backend
from keras.layers import DepthwiseConv2D

from .layers_base import (register_quantize_target, rescale_outputs, tensor_inputs,
                          neural_layer_init, register_aligned_inputs, check_arg_constraints,
                          QuantizedLayer)
from .convolution import deconv_output_length
from ..tensors import FixedPoint, QFloat


@register_quantize_target(DepthwiseConv2D, has_weights=True)
@register_aligned_inputs
@keras.saving.register_keras_serializable()
class QuantizedDepthwiseConv2D(QuantizedLayer, DepthwiseConv2D):
    """ A depthwise convolutional layer that operates on quantized inputs and weights.

    Args:
        quant_config (dict, optional): the serialized quantization configuration. Defaults to None.
    """
    @neural_layer_init(False)
    def __init__(self, *args, quant_config=None, **kwargs):
        # Override WeightQuantizer axis to -2 which corresponds to the channel dimension of the
        # depthwise operation.
        self.weight_quantizer.axis = -2
        self.quant_config['weight_quantizer']['axis'] = -2

        # Limit buffer bitwidth to 27
        self.quant_config['buffer_bitwidth'] = min(28, self.quant_config['buffer_bitwidth'])
        self.buffer_bitwidth = self.quant_config['buffer_bitwidth'] - 1

    @tensor_inputs([FixedPoint, tf.Tensor])
    @rescale_outputs
    def call(self, inputs):
        # Quantize the weights
        depthwise_kernel = self.weight_quantizer(self.depthwise_kernel)

        outputs = backend.depthwise_conv2d(
            inputs,
            depthwise_kernel,
            strides=self.strides,
            padding=self.padding,
            dilation_rate=self.dilation_rate,
            data_format=self.data_format)

        if self.use_bias:
            # Quantize bias and align it on the outputs
            bias = self.bias_quantizer(self.bias, outputs)
            outputs = tf.add(outputs, bias)

        return outputs


@keras.saving.register_keras_serializable()
class DepthwiseConv2DTranspose(DepthwiseConv2D):
    """ A transposed depthwise convolutional layer.

    It performs a transposed depthwise convolution on inputs.
    """
    arg_constraints = {
        'dilation_rate': lambda: [1, [1, 1], (1, 1)],
        'depth_multiplier': 1,
        'strides': lambda: [2, [2, 2], (2, 2)],
        'padding': 'same'
    }

    def __init__(self, *args, **kwargs):
        check_arg_constraints(self, kwargs)
        super().__init__(*args, **kwargs)

    def build(self, input_shape):
        # Ensure variables are build with the appropriate name
        with tf.name_scope(self.name + '/'):
            super().build(input_shape)

    def call(self, inputs):
        # Infer the dynamic output shape
        inputs_shape = tf.shape(inputs)
        out_height = deconv_output_length(
            inputs_shape[1],
            self.kernel_size[0],
            padding=self.padding,
            stride=self.strides[0],
            dilation=self.dilation_rate[0])
        out_width = deconv_output_length(
            inputs_shape[2],
            self.kernel_size[1],
            padding=self.padding,
            stride=self.strides[1],
            dilation=self.dilation_rate[1])
        output_shape = tf.stack((inputs_shape[0], out_height, out_width, 1))
        # Duplicate output_shape to create a placeholder that could be iterated in
        # tf.vectorized_map, making keras happy.
        output_shape = tf.repeat([output_shape], repeats=inputs_shape[-1], axis=0)

        # Inputs and kernels must be transposed to have their channel
        # dimension first because the tf.vectorized_map call that follows will
        # unpack them on dimension 0. The channel dimension is virtually
        # restored using expand_dims so that elements have the appropriate
        # shape for the conv2d_transpose call (with a channel dimension of 1
        # which is expected in the depthwise process).
        inputs_channel_first = tf.transpose(inputs, (3, 0, 1, 2))
        inputs_channel_first = tf.expand_dims(inputs_channel_first, -1)
        kernel_channel_first = tf.transpose(
            self.depthwise_kernel, (2, 0, 1, 3))
        kernel_channel_first = tf.expand_dims(kernel_channel_first, -2)

        dw_outputs = tf.vectorized_map(
            lambda x: backend.conv2d_transpose(x[0],
                                               x[1],
                                               output_shape=x[2],
                                               strides=self.strides,
                                               padding=self.padding),
            (inputs_channel_first, kernel_channel_first, output_shape))
        outputs = tf.transpose(tf.squeeze(dw_outputs, axis=-1), (1, 2, 3, 0))

        # Last dimension is lost when building layer outputs in model.
        outputs = tf.reshape(outputs, (inputs_shape[0], out_height, out_width, inputs_shape[-1]))

        if self.use_bias:
            outputs = tf.add(outputs, self.bias)
        return outputs


@register_quantize_target(DepthwiseConv2DTranspose, has_weights=True)
@register_aligned_inputs
@keras.saving.register_keras_serializable()
class QuantizedDepthwiseConv2DTranspose(QuantizedLayer, DepthwiseConv2DTranspose):
    """ A transposed depthwise convolutional layer that operates on quantized
    inputs and weights.

    Args:
        quant_config (dict, optional): the serialized quantization
          configuration. Defaults to None.
    """

    @neural_layer_init(separable=False)
    def __init__(self, *args, quant_config=None, **kwargs):
        # By default neural_layer_init quantizer will be set to -1 (per-axis), but
        # in this very layer it will need to be set per-tensor to complete
        # the conv2d transpose operation. Weight quantizer axis is overridden,
        # and quant_config is updated accordingly.
        self.weight_quantizer.axis = None
        self.quant_config['weight_quantizer']['axis'] = None

        # Limit buffer bitwidth to 27
        self.quant_config['buffer_bitwidth'] = min(28, self.quant_config['buffer_bitwidth'])
        self.buffer_bitwidth = self.quant_config['buffer_bitwidth'] - 1

    @tensor_inputs([FixedPoint])
    @rescale_outputs
    def call(self, inputs):
        # Infer the dynamic output shape
        inputs_shape = tf.shape(inputs)
        out_height = deconv_output_length(
            inputs_shape[1],
            self.kernel_size[0],
            padding=self.padding,
            stride=self.strides[0],
            dilation=self.dilation_rate[0])
        out_width = deconv_output_length(
            inputs_shape[2],
            self.kernel_size[1],
            padding=self.padding,
            stride=self.strides[1],
            dilation=self.dilation_rate[1])
        output_shape = tf.stack((inputs_shape[0], out_height, out_width, 1))
        # Duplicate output_shape to create a placeholder that could be iterated in
        # tf.vectorized_map, making keras happy.
        output_shape = tf.repeat([output_shape], repeats=inputs_shape[-1], axis=0)

        # Quantize the depthwise kernels
        depthwise_kernel = self.weight_quantizer(self.depthwise_kernel)

        # Inputs and kernels must be transposed to have their channel
        # dimension first because the tf.vectorized_map call that follows will
        # unpack them on dimension 0. The channel dimension is virtually
        # restored using expand_dims so that elements have the appropriate
        # shape for the conv2d_transpose call (with a channel dimension of 1
        # which is expected in the depthwise process).
        inputs_channel_first = tf.transpose(inputs, (3, 0, 1, 2))
        inputs_channel_first = tf.expand_dims(inputs_channel_first, -1)
        kernel_channel_first = tf.transpose(depthwise_kernel,
                                            (2, 0, 1, 3))
        kernel_channel_first = tf.expand_dims(kernel_channel_first, -2)

        # Perform the depthwise operation on values using conv2d_transpose on
        # each channel
        dw_values = tf.vectorized_map(
            lambda x: backend.conv2d_transpose(x[0],
                                               x[1],
                                               output_shape=x[2],
                                               strides=self.strides,
                                               padding=self.padding),
            (inputs_channel_first.values, kernel_channel_first.values, output_shape))
        dw_values = tf.transpose(tf.squeeze(dw_values, axis=-1), (1, 2, 3, 0))

        # Last dimension is lost when building layer outputs in model.
        dw_values = tf.reshape(dw_values,
                               (inputs_shape[0], out_height, out_width, inputs_shape[-1]))

        # Build a new FixedPoint
        outputs = FixedPoint(dw_values, inputs.value_bits, inputs.frac_bits)
        # Build a new QFloat
        outputs = QFloat(outputs, kernel_channel_first.scales)

        if self.use_bias:
            # Quantize biases and align them on the outputs
            bias = self.bias_quantizer(self.bias, outputs)
            # Add biases
            outputs = tf.add(outputs, bias)

        return outputs
