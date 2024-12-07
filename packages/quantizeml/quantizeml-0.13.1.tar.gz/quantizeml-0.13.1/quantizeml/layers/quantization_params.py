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

__all__ = ["QuantizationParams", "get_quantization_params", "quantization"]

import numpy as np
from contextlib import contextmanager


class QuantizationParams:
    """ Class that holds quantization parameters.

    This is a read-only data class.

    Args:
        activation_bits (int, optional): activations quantization bitwidth. Defaults to 8.
        per_tensor_activations (bool, optional): whether to quantize activation per-tensor or
            per-axis. Defaults to False.
        weight_bits (int, optional): weights quantization bitwidth. Defaults to 8.
        output_bits (int, optional): outputs quantization bitwidth. Defaults to 8.
        input_weight_bits (int, optional): weights quantization bitwidth for the first layer.
            Defaults to 8.
        input_dtype (np.dtype or str, optional): expected model input format. If given as a string,
            should follow numpy string type requirements. Defaults to 'uint8'.
        buffer_bits (int, optional): maximal buffer bitwidth allowed in operations.
            Defaults to 32.
        last_output_bits (int, optional): when provided, sets the bitwidth of the model output. the
            Defaults to None.
    """

    def __init__(self, activation_bits=8, per_tensor_activations=False, weight_bits=8,
                 output_bits=8, input_weight_bits=8, input_dtype='uint8', buffer_bits=32,
                 last_output_bits=None):
        self._activation_bits = activation_bits
        self._per_tensor_activations = per_tensor_activations
        self._weight_bits = weight_bits
        self._output_bits = output_bits
        self._input_weight_bits = input_weight_bits
        self._buffer_bits = buffer_bits
        self._input_dtype = np.dtype(input_dtype)
        self._last_output_bits = last_output_bits
        if not np.issubdtype(self._input_dtype, np.integer):
            raise ValueError(f"Unsupported {self._input_dtype} input dtype: "
                             "it should be a integer subdtype.")

    @property
    def activation_bits(self):
        return self._activation_bits

    @property
    def per_tensor_activations(self):
        return self._per_tensor_activations

    @property
    def weight_bits(self):
        return self._weight_bits

    @property
    def output_bits(self):
        return self._output_bits

    @property
    def input_weight_bits(self):
        return self._input_weight_bits

    @property
    def input_dtype(self):
        return self._input_dtype

    @property
    def buffer_bits(self):
        return self._buffer_bits

    @property
    def last_output_bits(self):
        return self._last_output_bits

    def __repr__(self) -> str:
        return (
            f"QuantizationParams("
            f"activation_bits={self.activation_bits}, "
            f"per_tensor_activations={self.per_tensor_activations}, "
            f"weight_bits={self.weight_bits}, "
            f"output_bits={self.output_bits}, "
            f"input_weight_bits={self.input_weight_bits}, "
            f"input_dtype={str(self.input_dtype)}, "
            f"buffer_bits={self.buffer_bits}, "
            f"last_output_bits={self.last_output_bits})"
        )

    def __str__(self) -> str:
        return (
            f"Activation bits: {self.activation_bits}, "
            f"Per tensor activations: {self.per_tensor_activations}, "
            f"Weight bits: {self.weight_bits}, "
            f"Output bits: {self.output_bits}, "
            f"Input weight bits: {self.input_weight_bits}, "
            f"Input dtype: {str(self.input_dtype)}, "
            f"Buffer bits: {self.buffer_bits}, "
            f"last_output_bits: {self.last_output_bits})"
        )


_quantization = QuantizationParams()


def get_quantization_params():
    """ Returns global quantization parameters.

    Returns:
        QuantizationParams: the quantization parameters
    """
    return _quantization


@contextmanager
def quantization(qparams):
    """ Sets quantization parameters in a context.

    Args:
        qparams (QuantizationParams): quantization parameters
    """
    # Use of global parameters
    global _quantization
    previous_state = _quantization
    try:
        # Set provided values
        _quantization = qparams
        yield
    finally:
        # Restore previous state
        _quantization = previous_state
