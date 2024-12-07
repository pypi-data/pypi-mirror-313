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

__all__ = ["QuantizedMaxPool2D", "QuantizedGlobalAveragePooling2D"]

import tensorflow as tf
import keras

from keras.layers import MaxPool2D, GlobalAveragePooling2D

from .layers_base import (register_quantize_target, register_no_output_quantizer, rescale_outputs,
                          tensor_inputs, apply_buffer_bitwidth, QuantizedLayer)
from .quantizers import OutputQuantizer
from ..tensors import FixedPoint, QTensor, QFloat


@register_quantize_target(MaxPool2D)
@register_no_output_quantizer
@keras.saving.register_keras_serializable()
class QuantizedMaxPool2D(QuantizedLayer, MaxPool2D):
    """A max pooling layer that operates on quantized inputs.

    """
    @tensor_inputs([QTensor])
    def call(self, inputs):
        if self.data_format == "channels_last":
            ksize = (1,) + self.pool_size + (1,)
            strides = (1,) + self.strides + (1,)
            data_format = "NHWC"
        else:
            ksize = (1, 1) + self.pool_size
            strides = (1, 1) + self.strides
            data_format = "NCHW"

        padding = self.padding.upper()
        outputs = tf.nn.max_pool(inputs, ksize=ksize, strides=strides, padding=padding,
                                 data_format=data_format)
        return outputs

    def get_config(self):
        return MaxPool2D.get_config(self)


@register_quantize_target(GlobalAveragePooling2D)
@keras.saving.register_keras_serializable()
class QuantizedGlobalAveragePooling2D(QuantizedLayer, GlobalAveragePooling2D):
    """A global average pooling layer that operates on quantized inputs.

     Args:
        quant_config (dict, optional): the serialized quantization configuration. Defaults to None.
    """

    def __init__(self, quant_config=None, **kwargs):
        super().__init__(quant_config=quant_config, **kwargs)
        out_quant_cfg = self.quant_config.get("output_quantizer", False)
        if out_quant_cfg:
            self.out_quantizer = OutputQuantizer(
                name="output_quantizer", **out_quant_cfg)
        else:
            self.out_quantizer = None
        self.buffer_bitwidth = apply_buffer_bitwidth(self.quant_config, signed=False)

    def build(self, input_shape):
        super().build(input_shape)
        # Build the spatial size and its reciprocal
        self.spatial_size = (input_shape[1] * input_shape[2])
        self.spatial_size_rec = 1. / self.spatial_size

    @tensor_inputs([QTensor])
    @rescale_outputs
    def call(self, inputs):
        # The only use case where GAP would receive a FixedPoint is when inputs are coming from an
        # add layer and in that case they would necessarily be per-tensor.
        if isinstance(inputs, FixedPoint):
            inputs.assert_per_tensor()
        inputs_sum = tf.reduce_sum(inputs, axis=[1, 2], keepdims=self.keepdims)
        if isinstance(inputs, FixedPoint):
            return QFloat(inputs_sum, self.spatial_size_rec)
        return inputs_sum / self.spatial_size
