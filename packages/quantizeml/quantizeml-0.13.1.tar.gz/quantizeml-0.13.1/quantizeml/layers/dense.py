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

__all__ = ["QuantizedDense"]

import tensorflow as tf
import keras

from .layers_base import (register_quantize_target, rescale_outputs, tensor_inputs,
                          neural_layer_init, register_aligned_inputs, QuantizedLayer)
from ..tensors import QTensor


@register_quantize_target(keras.layers.Dense, has_weights=True)
@register_aligned_inputs
@keras.saving.register_keras_serializable()
class QuantizedDense(QuantizedLayer, keras.layers.Dense):
    """A Dense layer that operates on quantized inputs and weights

    Args:
        quant_config (dict, optional): the serialized quantization configuration. Defaults to None.
    """
    @neural_layer_init(False)
    def __init__(self, *args, quant_config=None, **kwargs):
        # Limit buffer bitwidth to 27 for HW constraint
        self.quant_config['buffer_bitwidth'] = min(28, self.quant_config['buffer_bitwidth'])
        self.buffer_bitwidth = self.quant_config['buffer_bitwidth'] - 1

    @tensor_inputs([QTensor, tf.Tensor])
    @rescale_outputs
    def call(self, inputs):
        # Quantize the weights
        kernel = self.weight_quantizer(self.kernel)

        outputs = tf.matmul(inputs, kernel)

        if self.use_bias:
            # Quantize and align biases
            bias = self.bias_quantizer(self.bias, outputs)
            outputs = tf.add(outputs, bias)

        return outputs
