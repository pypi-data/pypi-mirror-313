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

__all__ = ["OutputObserver"]

import tensorflow as tf
import keras

from keras.layers import Layer

from .layers_base import check_arg_constraints


@keras.saving.register_keras_serializable()
class OutputObserver(Layer):
    """ Calibration layer.

    This layer is used to compute the future `range_max` of the equivalent OutputQuantizer in the
    quantized model. It is placed where the OutputQuantizer will be inserted (end of blocks) and
    accumulates the observed maximum values (with momentum) for input in the float model.

    Args:
        axis (str): the quantization range is a scalar ('per-tensor') or a vector
            corresponding to the last axis ('per-axis'). Defaults to 'per-tensor'.
        momentum (float): the momentum for the moving average. Defaults to 0.9.
    """
    arg_constraints = {'axis': lambda: ["per-tensor", "per-axis"]}

    def __init__(self, axis="per-tensor", momentum=0.9, **kwargs):
        super().__init__(**kwargs)
        self.axis = axis
        self.momentum = momentum
        self._decay = tf.convert_to_tensor(1.0 - momentum, name="decay")
        check_arg_constraints(self, self.get_config())

    def build(self, input_shape):
        """Build the layer.

        Args:
            input_shape (list): the shape of input tensor.
        """
        super().build(input_shape)
        # Convert axis to a list of int
        if self.axis == "per-axis":
            ndims = len(input_shape)
            if ndims < 3:
                raise ValueError("OutputObserver cannot quantize per-axis tensors "
                                 " with 2 dimensions or less.")
            self._axis = list(range(len(input_shape) - 1))
        else:
            self._axis = None

        # Declares the constant/vector that will store the maximum values of the input.
        self.range_max = self.add_weight(
            name="range_max",
            shape=input_shape[-1] if self._axis is not None else (),
            dtype=tf.float32,
            initializer="ones",
            synchronization=tf.VariableSynchronization.ON_READ,
            trainable=False,
            aggregation=tf.VariableAggregation.MEAN,
            experimental_autocast=False,
        )

    def call(self, inputs):
        """ Observe inputs and update the maximum value with momentum.

        Args:
            inputs (tf.Tensor): the inputs tensor.

        Returns:
            tf.Tensor: unchanged inputs
        """
        # Compute the new range_max from inputs
        range_max = tf.math.reduce_max(tf.math.abs(inputs), self._axis)

        # If range_max was never updated set their newly computed values otherwise update with
        # moving average algorithm
        if tf.reduce_all(tf.math.equal(self.range_max, tf.constant(1.))):
            new_range_max = range_max
        else:
            # The new value is just the multiplication by decay
            old_value = self.range_max
            update_delta = (old_value - tf.cast(range_max, old_value.dtype)) * self._decay
            new_range_max = old_value - update_delta
        self.range_max.assign(new_range_max)
        return inputs

    def get_config(self):
        """Get the config of the layer.

        Returns:
            dict: the config of the layer.
        """
        config = super().get_config()
        config.update({"axis": self.axis, "momentum": self.momentum})
        return config
