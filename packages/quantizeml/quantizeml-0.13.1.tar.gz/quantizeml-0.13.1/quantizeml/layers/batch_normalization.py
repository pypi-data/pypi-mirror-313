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

__all__ = ["QuantizedBatchNormalization"]

import tensorflow as tf
import keras

from .layers_base import (register_quantize_target, rescale_outputs, register_aligned_inputs,
                          tensor_inputs, apply_buffer_bitwidth, QuantizedLayer)
from .quantizers import WeightQuantizer, AlignedWeightQuantizer, OutputQuantizer
from ..tensors import QTensor


def _validate_axis(axis, input_shape):
    """Validate an axis value and returns its standardized form.

    Args:
        axis (int, list, tuple): Value to validate. Can be an integer or a list/tuple of integers.
            Integers may be negative.
        input_shape (tuple): Reference input shape that the axis/axes refer to.

    Returns:
       list: normalized form of `axis`, i.e. a list with all-positive values.
    """
    input_shape = tf.TensorShape(input_shape)
    rank = input_shape.rank
    if not rank:
        raise ValueError(f"Input has undefined rank. Received: input_shape={input_shape}")

    # Convert axis to list and resolve negatives
    if isinstance(axis, int):
        axis = [axis]
    else:
        axis = list(axis)
    for idx, x in enumerate(axis):
        if x < 0:
            axis[idx] = rank + x

    # Validate axes
    for x in axis:
        if x < 0 or x >= rank:
            raise ValueError("Invalid value for `axis` argument. Expected 0 <= axis < inputs.rank "
                             f"(with inputs.rank={rank}). Received: axis={tuple(axis)}")
    if len(axis) != len(set(axis)):
        raise ValueError(f"Duplicate axis: {tuple(axis)}")
    return axis


@register_quantize_target(keras.layers.BatchNormalization)
@register_aligned_inputs
@keras.saving.register_keras_serializable()
class QuantizedBatchNormalization(QuantizedLayer):
    r"""Layer that normalizes its inputs, on the last axis.

    The normalization is applied like this:

    .. math::

        y = \\frac{(x - \\mu) \\cdot \\gamma}{\\sigma} + \\beta \\
            = \\frac{x \\cdot \\gamma}{\\sigma} - \\
              \\frac{\\mu\\cdot \\gamma}{\\gamma} + \\beta

    if we consider:

    .. math:: a = \\frac{\\gamma}{\\sigma}

    and

    .. math:: b = -\\frac{\\mu\\cdot \\gamma}{\\sigma} + \\beta


    The normalization can be re-written as:

    .. math:: y = a \\cdot x + b

    Note that this layer will hold variables with names gamma, beta, moving_mean (:math:`\\mu`),
    and moving_variance (:math:`\\sigma = \\sqrt{moving\_variance + \\epsilon}`), so they can be
    converted from a BatchNormalization layer. However, it's a and b that are going to be quantized.

    Args:
        quant_config (dict, optional): the serialized quantization configuration. Defaults to None.
        axis (int, optional): The axis that was normalized on the
            BatchNormalization layer. The only supported value is the
            last dimension.
        epsilon (float, optional): Small value to avoid dividing by zero.
            Defaults to 1e-3.
    """

    ignored_args = ["momentum",
                    "center",
                    "scale",
                    "beta_initializer",
                    "gamma_initializer",
                    "moving_mean_initializer",
                    "moving_variance_initializer",
                    "beta_regularizer",
                    "gamma_regularizer",
                    "beta_constraint",
                    "gamma_constraint",
                    "renorm",
                    "renorm_clipping",
                    "renorm_momentum",
                    "fused",
                    "trainable",
                    "virtual_batch_size",
                    "adjustment"
                    ]

    def __init__(self,
                 *args,
                 quant_config=None,
                 axis=-1,
                 epsilon=1e-3,
                 **kwargs):
        super().__init__(*args, quant_config=quant_config, **kwargs)
        out_quant_cfg = self.quant_config.get("output_quantizer", False)
        if out_quant_cfg:
            self.out_quantizer = OutputQuantizer(
                name="output_quantizer", **out_quant_cfg)
        else:
            self.out_quantizer = None
        if "a_quantizer" not in self.quant_config:
            self.quant_config["a_quantizer"] = {"bitwidth": 8}
        a_quantizer_cfg = self.quant_config["a_quantizer"]
        self.a_quantizer = WeightQuantizer(name="a_quantizer", **a_quantizer_cfg)
        b_quantizer_cfg = self.quant_config.get("b_quantizer", {})
        self.b_quantizer = AlignedWeightQuantizer(name="b_quantizer", **b_quantizer_cfg)
        self.buffer_bitwidth = apply_buffer_bitwidth(self.quant_config, signed=True)

        # Define a small float number to avoid dividing by zero.
        self.epsilon = epsilon
        # Axis on which operation is applied
        self.axis = axis

    def build(self, input_shape):
        input_shape = tf.TensorShape(input_shape)
        rank = input_shape.rank

        if rank not in (3, 4):
            raise ValueError(
                "QuantizedBatchNormalization only supports 3D or 4D tensors. "
                f"Received tensor with shape: {tuple(input_shape)}.")

        # Normalize axis
        self.axis = _validate_axis(self.axis, input_shape)

        # Check selected axis is valid
        if len(self.axis) != 1 and (self.axis[0] != rank - 1):
            raise ValueError("QuantizedBatchNormalization only supports axis "
                             "argument set to the last dimension.")

        # Shape for variables is always as if it was applied on the
        # last dimension.
        param_shape = input_shape[-1]

        # Add BN compatible weights
        # Gamma
        self.gamma = self.add_weight(
            name="gamma",
            shape=param_shape,
            dtype=tf.float32,
            initializer="ones",
            regularizer=None,
            constraint=None,
            trainable=True,
            experimental_autocast=False,
        )
        # Beta
        self.beta = self.add_weight(
            name="beta",
            shape=param_shape,
            dtype=tf.float32,
            initializer="zeros",
            regularizer=None,
            constraint=None,
            trainable=True,
            experimental_autocast=False,
        )
        # Mu = moving mean
        self.moving_mean = self.add_weight(
            name="moving_mean",
            shape=param_shape,
            dtype=tf.float32,
            initializer="zeros",
            regularizer=None,
            constraint=None,
            trainable=False,
            experimental_autocast=False,
        )
        # Sigma² = moving variance
        self.moving_variance = self.add_weight(
            name="moving_variance",
            shape=param_shape,
            dtype=tf.float32,
            initializer="ones",
            regularizer=None,
            constraint=None,
            trainable=False,
            experimental_autocast=False,
        )

    @property
    def sigma_rec(self):
        # Sigma reciprocal = 1 / sigma = 1 / sqrt(moving_variance + epsilon)
        sigma_rec = tf.math.rsqrt(self.moving_variance + self.epsilon)
        return sigma_rec

    @property
    def a(self):
        a_var = self.gamma * self.sigma_rec
        q_a = self.a_quantizer(a_var)
        return q_a

    def b(self, inputs):
        sigma_rec = self.sigma_rec
        b_var = -self.moving_mean * self.gamma * sigma_rec + self.beta
        q_b = self.b_quantizer(b_var, inputs)
        return q_b

    @tensor_inputs([QTensor])
    @rescale_outputs
    def call(self, inputs):
        # Calculation is equivalent to
        # y = (x - mu) * gamma / sigma + beta
        #   = x * gamma / sigma - mu * gamma / sigma + beta
        #
        # So if we consider
        # a = gamma / sigma
        # b = -mu * gamma / sigma + beta
        # Then the evaluation is just y = a * x + b.

        # outputs = a * x
        outputs = tf.multiply(inputs, self.a)

        # quantize and retrieve b, aligned on the outputs to allow sum
        b = self.b(outputs)
        # y = outputs + b
        return tf.add(outputs, b)

    def get_config(self):
        config = super().get_config()
        config.update({"epsilon": self.epsilon, "axis": self.axis})
        return config
