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

__all__ = ["Quantizer", "Dequantizer"]

import tensorflow as tf
import keras

from keras.layers import Layer

from ...tensors import QTensor, QFloat
from ..recorders import TensorRecorder


class Quantizer(Layer):
    """The base class for all quantizers.

    The bitwidth defines the number of quantization levels on which the
    values will be quantized.
    For a quantizer that accepts unsigned values, the maximum quantization
    level is :math:`2 ^ {bitwidth} - 1`.
    For a quantizer that accepts signed values, we lose one bit of precision to
    store the sign.
    When the quantizer is signed, the quantization interval is asymmetric around
    zero (i.e range: :math:`[- 2 ^ {bitwidth - 1}, 2 ^ {bitwidth - 1} - 1]`).

    Args:
        bitwidth (int): the quantization bitwidth.
        signed (bool, optional): whether the quantizer expects signed values or unsigned.
            Defaults to True.
    """

    def __init__(self, bitwidth, signed=True, **kwargs):
        min_bitwidth = 2 if signed else 1
        if not isinstance(bitwidth, int) or bitwidth < min_bitwidth:
            raise ValueError(
                f"Bitwidth should be an int >= {min_bitwidth}, currently {bitwidth}")
        self.bitwidth = bitwidth
        self.signed = signed
        self.value_bits = bitwidth - 1 if signed else bitwidth
        super().__init__(**kwargs)

    def get_config(self):
        """Get the config of the layer.

        Returns:
            dict: the config of the layer.
        """
        config = super().get_config()
        config.update({"bitwidth": self.bitwidth})
        config.update({"signed": self.signed})
        return config


@keras.saving.register_keras_serializable()
class Dequantizer(Layer):
    """ Layer that allows to dequantize its inputs.
    """
    scales: list = None
    frac_bits: list = None

    def _build_records(self, inputs):
        def _build(x):
            record_fb = record_scale = None
            # From Keras documentation, any variable creation taking place
            # in call should be wrapped with tf.init_scope
            with tf.init_scope():
                if isinstance(x, QTensor):
                    record_fb = TensorRecorder(self.name + "/record_fb")
                if isinstance(x, QFloat):
                    record_scale = TensorRecorder(self.name + "/record_scale")
            return record_fb, record_scale

        if self.frac_bits is not None:
            # Nothing to do
            return
        if not isinstance(inputs, (tuple, list)):
            # Manage single inputs
            self.frac_bits, self.scales = _build(inputs)
            return

        self.frac_bits = []
        self.scales = []
        with tf.init_scope():
            for x in inputs:
                frac_bits, scales = _build(x)
                self.frac_bits.append(frac_bits)
                self.scales.append(scales)

    def call(self, inputs):
        """Convert QTensor inputs to float.

        Args:
            inputs (tf.Tensor or :obj:`QTensor`): the inputs tensor(s).

        Returns:
            tf.Tensor: the dequantized tensor(s).
        """

        def dequantize(x, frac_bits_recorder=None, scales_recorder=None):
            if isinstance(x, QTensor):
                if frac_bits_recorder is not None:
                    frac_bits_recorder(x.fp.frac_bits if isinstance(x, QFloat) else x.frac_bits)
                if scales_recorder is not None:
                    scales_recorder(x.scales)
                return x.to_float()
            return x

        # Build records
        self._build_records(inputs)

        # Apply dequantizer
        if isinstance(inputs, (list, tuple)):
            return [dequantize(x, fb, scales) for x, fb, scales in
                    zip(inputs, self.frac_bits, self.scales)]

        return dequantize(inputs, self.frac_bits, self.scales)
