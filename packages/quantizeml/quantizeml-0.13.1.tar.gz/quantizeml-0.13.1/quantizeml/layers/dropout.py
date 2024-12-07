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

__all__ = ["QuantizedDropout"]

import keras

from .layers_base import (register_quantize_target, tensor_inputs, register_no_output_quantizer,
                          QuantizedLayer)
from ..tensors import QTensor


@register_quantize_target(keras.layers.Dropout)
@register_no_output_quantizer
@keras.saving.register_keras_serializable()
class QuantizedDropout(QuantizedLayer, keras.layers.Dropout):
    """ A dropout layer that operates on quantized inputs and weights.

    It is only implemented as a passthrough.
    """

    @tensor_inputs([QTensor])
    def call(self, inputs):
        # QuantizedDropout act as a pass through.
        return inputs

    def get_config(self):
        return keras.layers.Dropout.get_config(self)
