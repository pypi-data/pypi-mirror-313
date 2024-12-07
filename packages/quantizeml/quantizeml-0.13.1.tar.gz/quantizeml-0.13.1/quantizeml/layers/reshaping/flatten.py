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

__all__ = ["QuantizedFlatten"]

import tensorflow as tf
import keras
import functools
import operator

from ..layers_base import (register_quantize_target, tensor_inputs, register_no_output_quantizer,
                           register_aligned_inputs)
from ..recorders import TensorRecorder
from ...tensors import FixedPoint


@register_quantize_target(keras.layers.Flatten)
@register_no_output_quantizer
@register_aligned_inputs
@keras.saving.register_keras_serializable()
class QuantizedFlatten(keras.layers.Flatten):
    """A Flatten layer that operates on quantized inputs
    """

    @tensor_inputs([FixedPoint])
    def call(self, inputs):
        if not inputs.per_tensor:
            inputs, shift = inputs.expand(inputs.value_bits)
            if getattr(self, 'input_shift', None) is None:
                with tf.init_scope():
                    self.input_shift = TensorRecorder(name=self.name + "/input_shift")
            self.input_shift(shift)
        if tf.executing_eagerly():
            flattened_shape = tf.constant([inputs.shape[0], -1])
        else:
            non_batch_dims = inputs.shape[1:]
            last_dim = int(functools.reduce(operator.mul, non_batch_dims))
            flattened_shape = tf.constant([-1, last_dim])
        return tf.reshape(inputs, flattened_shape)
