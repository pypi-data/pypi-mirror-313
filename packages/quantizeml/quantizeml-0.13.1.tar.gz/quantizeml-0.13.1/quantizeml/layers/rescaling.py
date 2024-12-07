#!/usr/bin/env python
# ******************************************************************************
# Copyright 2023 Brainchip Holdings Ltd.
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

__all__ = ["QuantizedRescaling"]

import keras.layers
import tensorflow as tf
import keras

from .layers_base import (register_quantize_target, register_no_output_quantizer, tensor_inputs,
                          QuantizedLayer)
from ..tensors import QFloat


@register_quantize_target(keras.layers.Rescaling)
@register_no_output_quantizer
@keras.saving.register_keras_serializable()
class QuantizedRescaling(QuantizedLayer, keras.layers.Rescaling):
    """A layer that multiplies integer inputs by a scale

    This is a simplified version of the keras Rescaling layer:

    - it only supports a scalar scale,
    - it only supports zero offsets.

    This layer assumes the inputs are 8-bit integer: it simply wraps them into
    an 8-bit per-tensor QFloat with the specified scale.

    Args:
        scale (float): a scalar scale.
    """

    def __init__(self, scale, **kwargs):
        super().__init__(scale, **kwargs)
        if tf.rank(self.scale) > 0:
            raise ValueError("QuantizedRescaling only accepts scalar scale.")
        if tf.reduce_any(self.offset != 0):
            raise ValueError("QuantizedRescaling only accepts zero offset.")

    @tensor_inputs([tf.Tensor])
    def call(self, inputs):
        # Wrap them into a QFloat with the specified scale
        return QFloat(inputs, self.scale)

    def get_config(self):
        return keras.layers.Rescaling.get_config(self)
