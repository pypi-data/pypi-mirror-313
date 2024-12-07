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

__all__ = ["StatefulRecurrent", "QuantizedStatefulRecurrent", "reset_states",
           "StatefulProjection", "QuantizedStatefulProjection", "update_batch_size"]

import keras
import tensorflow as tf

from .recorders import (NonTrackVariable, TensorRecorder, NonTrackFixedPointVariable,
                        FixedPointRecorder)
from .layers_base import (register_quantize_target, tensor_inputs, apply_buffer_bitwidth,
                          register_aligned_inputs, QuantizedLayer, neural_layer_init,
                          rescale_outputs, get_quantization_params)
from .quantizers import WeightQuantizer, OutputQuantizer
from ..tensors import FixedPoint, QTensor, QFloat


@keras.saving.register_keras_serializable()
class StatefulRecurrent(keras.layers.Layer):
    """ A recurrent layer with an internal state.  """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._internal_state_real = NonTrackVariable("internal_state_real")
        self._internal_state_imag = NonTrackVariable("internal_state_imag")

    def build(self, input_shape):
        assert input_shape[0] is not None, f"{self.name} must be built with a known batch size."

        with tf.name_scope(self.name + '/'):
            super().build(input_shape)

            # 'A' weight is a complex64 tensor stored as two float32 tensor to ease quantization
            self.A_real = self.add_weight(name='A_real', shape=(input_shape[-1],))
            self.A_imag = self.add_weight(name='A_imag', shape=(input_shape[-1],))

            # Initialize the internal state variables, drop the timesteps dimension
            self._internal_state_real.init_var(tf.zeros((input_shape[0], input_shape[-1])))
            self._internal_state_imag.init_var(tf.zeros((input_shape[0], input_shape[-1])))

    def call(self, inputs):
        """ For every input step, the internal state is updated using the inputs which should be the
        updated state from the previous layer.
        """
        # Build output tensors that will contain all updates, initialize them with internal state
        multiples = [1, inputs.shape[1], 1]
        state_real = tf.tile(tf.expand_dims(self._internal_state_real.var, axis=1), multiples)
        state_imag = tf.tile(tf.expand_dims(self._internal_state_imag.var, axis=1), multiples)

        # Loop over timesteps
        for i in range(tf.shape(inputs)[1]):
            # Compute real and imaginary part separately
            updated_real = state_real[:, i - 1] * self.A_real - \
                state_imag[:, i - 1] * self.A_imag + inputs[:, i]
            updated_imag = self.A_imag * state_real[:, i - 1] + \
                self.A_real * state_imag[:, i - 1]
            indices = tf.stack([tf.range(state_real.shape[0]), tf.repeat(i, state_real.shape[0])],
                               axis=1)
            state_real = tf.tensor_scatter_nd_update(state_real, indices, updated_real)
            state_imag = tf.tensor_scatter_nd_update(state_imag, indices, updated_imag)

        # Update internal state for next call
        self._internal_state_real.set_var(state_real[:, -1])
        self._internal_state_imag.set_var(state_imag[:, -1])
        return tf.stack([state_real, state_imag], -1)

    def reset_layer_states(self):
        self._internal_state_real.reset_var()
        self._internal_state_imag.reset_var()


@register_quantize_target([StatefulRecurrent], has_weights=True)
@keras.saving.register_keras_serializable()
class QuantizedStatefulRecurrent(QuantizedLayer, StatefulRecurrent):
    """ A quantized version of the StatefulRecurrent layer that operates on quantized inputs,
    weights and internal state.

    Note that internal state is quantized to 16-bits for accuracy reasons, inputs and outputs of
    this layer are then also 16-bits.

    Args:
        quant_config (dict, optional): the serialized quantization configuration. Defaults to None.
    """

    def __init__(self, *args, quant_config=None, **kwargs):
        super().__init__(*args, quant_config=quant_config, **kwargs)

        self._internal_state_real = NonTrackFixedPointVariable("internal_state_real")
        self._internal_state_imag = NonTrackFixedPointVariable("internal_state_imag")

        # Build weight quantizer for A_real and A_imag (sharing the same quantizer)
        default_weight_bits = get_quantization_params().weight_bits
        if "a_quantizer" not in self.quant_config:
            self.quant_config["a_quantizer"] = {"bitwidth": default_weight_bits}
        # Forcing to:
        #   - per-tensor to ensure alignement in the call operations
        #   - FixedPoint quantization to prevent scale_out operations on internal_state
        self.quant_config["a_quantizer"].update({"axis": None, "fp_quantizer": True})
        a_quantizer_cfg = self.quant_config["a_quantizer"]
        self.a_quantizer = WeightQuantizer(name="a_quantizer", **a_quantizer_cfg)

        # Finalize output quantizer, add one with default configuration if there is None in the
        # config as state must be quantized
        default_output_bits = get_quantization_params().output_bits
        if "output_quantizer" not in self.quant_config:
            self.quant_config["output_quantizer"] = {"bitwidth": default_output_bits}
        # Forcing to:
        #   - per-tensor to ensure alignement in real and imag are always aligned
        self.quant_config["output_quantizer"].update({"axis": "per-tensor"})
        out_quant_cfg = self.quant_config["output_quantizer"]
        self.out_quantizer = OutputQuantizer(name="output_quantizer", **out_quant_cfg)
        self.buffer_bitwidth = apply_buffer_bitwidth(self.quant_config, signed=True)

        # Prepare the variable that should be recorded
        self.new_state_shift = TensorRecorder(name=self.name + "/new_state_shift")

    def build(self, input_shape):
        assert input_shape[0] is not None, f"{self.name} must be built with a known batch size."

        with tf.name_scope(self.name + '/'):
            # Explicitly build the Keras.layer and not StatefulRecurrent because state is not of
            # the same type
            keras.layers.Layer.build(self, input_shape)

            # 'A' weight is a complex64 tensor stored as two float32 tensor to ease quantization
            self.A_real = self.add_weight(name='A_real', shape=(input_shape[-1],))
            self.A_imag = self.add_weight(name='A_imag', shape=(input_shape[-1],))

            # Explicitly build the OutputQuantizer so that output frac_bits can be computed
            self.out_quantizer.build((input_shape[0], input_shape[-1]))

            # Initialize the internal state variables
            zeros = FixedPoint(tf.zeros((input_shape[0], input_shape[-1])),
                               self.out_quantizer.value_bits, self.out_quantizer.frac_bits)
            self._internal_state_real.init_var(zeros)
            self._internal_state_imag.init_var(zeros)

    @tensor_inputs([QTensor])
    def call(self, inputs):
        if isinstance(inputs, QFloat):
            # Handle QFloat inputs by quantizing the scale: reuse output quantizer to get scale_bits
            # because the Stateful layer should be homogeneous
            inputs, qscales = inputs.to_fixed_point(self.out_quantizer.bitwidth)
            if getattr(self, 'new_state_scale', None) is None:
                # From Keras documentation, any variable creation taking place in call
                # should be wrapped with tf.init_scope
                with tf.init_scope():
                    self.new_state_scale = FixedPointRecorder(self.name + "/new_state_scale")
            self.new_state_scale(qscales)

        # Quantize A matrices
        A_real = self.a_quantizer(self.A_real)
        A_imag = self.a_quantizer(self.A_imag)

        # Align inputs with {A * state}, which is out_quantizer.frac_bits + A.frac_bits
        inputs, shift = inputs.rescale(self.out_quantizer.frac_bits + A_real.frac_bits,
                                       inputs.value_bits)
        self.new_state_shift(shift)

        # Set the appropriate frac_bit in state variable
        self._internal_state_real._frac_bits.assign(self.out_quantizer.frac_bits)
        self._internal_state_imag._frac_bits.assign(self.out_quantizer.frac_bits)

        # Define state update step
        internal_state_real_step = self._internal_state_real.var
        internal_state_imag_step = self._internal_state_imag.var

        # Build output tensors that will contain all updates, initialize them with internal state
        zero_fp = FixedPoint(tf.zeros(inputs.shape),
                             self._internal_state_real.var.value_bits,
                             self._internal_state_real.var.frac_bits)
        next_internal_state_real, next_internal_state_imag = zero_fp, zero_fp

        # Define a zero padding value
        padding_value = FixedPoint(0, self.out_quantizer.value_bits,
                                   self._internal_state_real._frac_bits)

        # Loop over timesteps
        timesteps = tf.shape(inputs)[1]
        for i in range(timesteps):
            # Promote internal_state_step
            internal_state_real_step = internal_state_real_step.promote(self.buffer_bitwidth)
            internal_state_imag_step = internal_state_imag_step.promote(self.buffer_bitwidth)

            # Update internal state: compute real and imaginary part separately using current step
            updated_real = tf.multiply(internal_state_real_step, A_real) - \
                tf.multiply(internal_state_imag_step, A_imag)

            # Get the inputs for this step
            input_step = inputs[:, i]

            # At this point addition is possible
            updated_real = updated_real + input_step

            # Same for imaginary part
            updated_imag = tf.multiply(internal_state_real_step, A_imag) + \
                tf.multiply(internal_state_imag_step, A_real)

            # Quantize down the update for next step using the layer output quantizer
            internal_state_real_step = self.out_quantizer(updated_real)
            internal_state_imag_step = self.out_quantizer(updated_imag)

            # Store the updates in next_internal_state. To do so, pad the updated state with zeroes
            # to left and right in order to rebuild a 'full' state where i-th timestep is equal to
            # computed update. Then add it to next_internal_state that was initialized to zeroes:
            # this effectively mimics an inplace update (working around Tensorflow logic).
            paddings = [[0, 0], [i, timesteps - 1 - i], [0, 0]]
            padded_real = tf.pad(tf.expand_dims(internal_state_real_step, axis=1),
                                 paddings=paddings, constant_values=padding_value)
            padded_imag = tf.pad(tf.expand_dims(internal_state_imag_step, axis=1),
                                 paddings=paddings, constant_values=padding_value)
            # Ensure the shape is as expected because TensorFlow will not tolerate shape changes
            # within the loop
            padded_real.values.set_shape(next_internal_state_real.shape)
            padded_imag.values.set_shape(next_internal_state_imag.shape)
            next_internal_state_real += padded_real
            next_internal_state_imag += padded_imag

        # Update internal state members
        self._internal_state_real.set_var(internal_state_real_step)
        self._internal_state_imag.set_var(internal_state_imag_step)

        # Return the concatenated states
        return tf.stack([next_internal_state_real, next_internal_state_imag], -1)


def reset_states(model):
    """ Resets all StatefulRecurrent layers internal states in the model.

    Args:
        model (keras.Model): the model to reset
    """
    for layer in model.layers:
        if isinstance(layer, StatefulRecurrent):
            layer.reset_layer_states()


def update_batch_size(model, batch_size):
    """ Updates the batch size in a model.

    Similar to keras RNN/Cell behavior where batch size must be known, the StatefulRecurrent layer
    state is built with a (None, ...) shape that must be defined runtime. This helper allow to set
    or update a model batch size.

    Args:
        model (keras.Model): the model to update
        batch_size (int): batch size to set

    Returns:
        keras.Model: an updated model (the original model when batch size is unchanged)
    """
    # Update batch size in config
    config = model.get_config()
    input_shape = config['layers'][0]['config']['batch_input_shape']
    if input_shape[0] == batch_size:
        return model

    config['layers'][0]['config']['batch_input_shape'] = (batch_size, *input_shape[1:])

    # Force layers shapes to be recomputed
    for layer_config in config["layers"]:
        layer_config.pop('build_config', None)

    # Rebuild model and transfer weights
    updated_model = model.from_config(config)
    updated_model.set_weights(model.get_weights())
    return updated_model


@keras.saving.register_keras_serializable()
class StatefulProjection(keras.layers.Dense):
    """ Same as a Dense layer but with optional reshaping operation.

    Reshaping can happen both on the inputs and the outputs.

    Args:
        downshape (tuple, optional): target shape for downshape operation that happens before the
            dense. Defaults to None.
        upshape (tuple, optional): target shape for upshape operation that happens after the dense.
            Defaults to None.
    """

    def __init__(self, *args, downshape=None, upshape=None, subsample=1, **kwargs):
        super().__init__(*args, **kwargs)
        self.downshape = tuple(downshape) if downshape else None
        self.upshape = tuple(upshape) if upshape else None
        self.subsample = subsample

    def build(self, input_shape):
        with tf.name_scope(self.name + '/'):
            if self.downshape is None:
                super().build(input_shape)
            else:
                # When downshape is enabled, build the layer with the target shape so that variables
                # are build properly
                super().build(self.downshape)
                # Edit the input_spec so that from a graph point of view, this layer sees the
                # original input shape
                last_dim = tf.TensorShape(input_shape)[-1]
                self.input_spec = tf.keras.layers.InputSpec(min_ndim=2, axes={-1: last_dim})

    def call(self, inputs):
        # Apply the optional input downshape
        if self.downshape is not None:
            inputs = tf.reshape(inputs, (tf.shape(inputs)[0],) + self.downshape)

        # Apply the optional subsampling
        if self.subsample > 1:
            assert inputs.shape[1] % self.subsample == 0, \
                f"Number of timesteps: {inputs.shape[1]} must be a multiple of subsample " \
                f"ratio: {self.subsample}."
            inputs = inputs[:, (self.subsample - 1)::self.subsample, :]

        # Standard Dense operation
        outputs = super().call(inputs)

        # Apply the optional output upshape
        if self.upshape is not None:
            outputs = tf.reshape(outputs, (tf.shape(outputs)[0],) + self.upshape)
        return outputs

    def get_config(self):
        config = super().get_config()
        config["downshape"] = self.downshape
        config["upshape"] = self.upshape
        config["subsample"] = self.subsample
        return config


@register_quantize_target([StatefulProjection], has_weights=True)
@register_aligned_inputs
@keras.saving.register_keras_serializable()
class QuantizedStatefulProjection(QuantizedLayer, StatefulProjection):
    """ A quantized version of the StatefulProjection layer that operates on quantized inputs.
    """
    @neural_layer_init(False, bias_bits=16)
    def __init__(self, *args, **kwargs):
        # Weight quantizer must be per-tensor to allow upshaping, override it when necessary
        if self.upshape is not None:
            self.quant_config["weight_quantizer"]["axis"] = None
            weight_quantizer_cfg = self.quant_config["weight_quantizer"]
            self.weight_quantizer = WeightQuantizer(name="weight_quantizer",
                                                    **weight_quantizer_cfg)

    @tensor_inputs([QTensor, tf.Tensor])
    @rescale_outputs
    def call(self, inputs):
        if self.downshape is not None:
            inputs = tf.reshape(inputs, (tf.shape(inputs)[0],) + self.downshape)

        if self.subsample > 1:
            assert inputs.shape[1] % self.subsample == 0, \
                f"Number of timesteps: {inputs.shape[1]} must be a multiple of subsample " \
                f"ratio: {self.subsample}."
            inputs = inputs[:, (self.subsample - 1)::self.subsample, :]

        # Quantize the weights
        kernel = self.weight_quantizer(self.kernel)

        outputs = tf.matmul(inputs, kernel)

        if self.use_bias:
            # Quantize and align biases
            bias = self.bias_quantizer(self.bias, outputs)
            outputs = tf.add(outputs, bias)

        if self.upshape is not None:
            outputs = tf.reshape(outputs, (tf.shape(outputs)[0],) + self.upshape)
        return outputs
