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

__all__ = ["QuantizedPermute"]

import tensorflow as tf
import keras

from ..layers_base import (register_quantize_target, tensor_inputs, register_no_output_quantizer,
                           register_aligned_inputs)
from ...tensors import FixedPoint
from ...debugging import assert_equal


@register_quantize_target(keras.layers.Permute)
@register_no_output_quantizer
@register_aligned_inputs
@keras.saving.register_keras_serializable()
class QuantizedPermute(keras.layers.Permute):
    """A Permute layer that operates on quantized inputs

    Note: Keras Permute layer simply wraps the Tensorflow transpose op.

    Args:
        dims (tuple of ints): Permutation pattern does not include the
            samples dimension. Indexing starts at 1.
            For instance, `(2, 1)` permutes the first and second dimensions
            of the input.
    """

    @tensor_inputs([FixedPoint])
    def call(self, inputs):
        if not inputs.per_tensor:
            # Different fractional-bits are defined for the last axis, so
            # it must be preserved during the transposition
            last_axis = tf.rank(inputs.values) - 1
            assert_equal(self.dims[-1], last_axis)
        # Transpose only the values
        transposed_values = super().call(inputs.values)
        # Return a FixedPoint with the modified values
        return FixedPoint(transposed_values, inputs.value_bits, inputs.frac_bits)
