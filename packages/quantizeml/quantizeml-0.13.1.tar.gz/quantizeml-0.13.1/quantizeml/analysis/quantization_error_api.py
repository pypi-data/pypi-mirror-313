#!/usr/bin/env python
# ******************************************************************************
# Copyright 2024 Brainchip Holdings Ltd.
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
__all__ = ["measure_layer_quantization_error", "measure_cumulative_quantization_error"]

import keras
import onnx

from .quantization_error import (keras_layer_quantization_error, onnx_node_quantization_error,
                                 keras_cumulative_quantization_error,
                                 onnx_cumulative_quantization_error)


def measure_layer_quantization_error(fmodel, qmodel, target_layer=None, batch_size=16, seed=None):
    """Measures the layer quantization error

    Returns a dictionary where the keys are the name of each layer and the values are a dictionary
    composed of the set of the following metrics:

        * Symmetrical Mean Absolute Percentage Error (SMAPE): :func:`tools.metrics.SMAPE`
        * Saturation: Percentage of how many values in the quantized layer saturate

    Example:
        >>> summary = measure_layer_quantization_error(fmodel, qmodel)
        >>> assert isinstance(summary[a_layer_name], dict)
        >>> assert "SMAPE" in summary[a_layer_name]

    Args:
        fmodel (onnx.ModelProto or tf.keras.Model): the float model.
        qmodel (onnx.ModelProto or tf.keras.Model): the quantized version of `fmodel`.
        target_layer (str, optional): computation error is performed only in the target layer/node,
            expanding the analysis to each output channel. Defaults to None.
        batch_size (int, optional): the batch size of the samples to be generated.
            It allows a better metrics generalization, but consumes more resources. Defaults to 16.
        seed (int, optional): a random seed. Defaults to None.

    Returns:
        dict: the quantization error for each layer

    Notes:
        * Layers/Nodes that do not produce quantization errors will not be taken into account
          (e.g. QuantizedReshape).
    """
    keras_model_types = (keras.Sequential, keras.Model)
    # Check both models have the same type
    if isinstance(fmodel, onnx.ModelProto) and isinstance(qmodel, onnx.ModelProto):
        summary = onnx_node_quantization_error(fmodel,
                                               qmodel,
                                               target_node=target_layer,
                                               batch_size=batch_size,
                                               seed=seed)
    elif isinstance(fmodel, keras_model_types) and isinstance(qmodel, keras_model_types):
        summary = keras_layer_quantization_error(fmodel,
                                                 qmodel,
                                                 target_layer=target_layer,
                                                 batch_size=batch_size,
                                                 seed=seed)
    else:
        model_types = (onnx.ModelProto, *keras_model_types)
        raise TypeError(f"Both models should be the same type, one of {model_types}. "
                        f"Received: {type(fmodel)} and {type(fmodel)}.")
    return summary


def measure_cumulative_quantization_error(fmodel,
                                          qmodel,
                                          target_layer=None,
                                          batch_size=16,
                                          seed=None):
    """Measures the cumulative quantization error

    Returns a dictionary where the keys are the name of each layer and the values are a dictionary
    composed of the set of the following metrics:

        * Symmetrical Mean Absolute Percentage Error (SMAPE): :func:`tools.metrics.SMAPE`
        * Saturation: Percentage of how many values in the quantized layer saturate

    Each metric measures the quantization error from the input to the layer.

    Example:
        >>> summary = measure_cumulative_quantization_error(fmodel, qmodel)
        >>> assert isinstance(summary[a_layer_name], dict)
        >>> assert "SMAPE" in summary[a_layer_name]

    Args:
        fmodel (onnx.ModelProto or tf.keras.Model): the float model.
        qmodel (onnx.ModelProto or tf.keras.Model): the quantized version of `fmodel`.
        target_layer (str, optional): error computation is performed only in the target layer/node,
            expanding the analysis to each output channel. Defaults to None.
        batch_size (int, optional): the batch size of the samples to be generated.
            It allows a better metrics generalization, but consumes more resources. Defaults to 16.
        seed (int, optional): a random seed. Defaults to None.

    Returns:
        dict: the quantization error for each layer

    Notes:
        * Layers/Nodes that do not produce quantization errors will not be taken into account
          (e.g. QuantizedReshape).
    """
    keras_model_types = (keras.Sequential, keras.Model)
    # Check both models have the same type
    if isinstance(fmodel, onnx.ModelProto) and isinstance(qmodel, onnx.ModelProto):
        summary = onnx_cumulative_quantization_error(fmodel,
                                                     qmodel,
                                                     target_node=target_layer,
                                                     batch_size=batch_size,
                                                     seed=seed)
    elif isinstance(fmodel, keras_model_types) and isinstance(qmodel, keras_model_types):
        summary = keras_cumulative_quantization_error(fmodel,
                                                      qmodel,
                                                      target_layer=target_layer,
                                                      batch_size=batch_size,
                                                      seed=seed)
    else:
        model_types = (onnx.ModelProto, *keras_model_types)
        raise TypeError(f"Both models should be the same type, one of {model_types}. "
                        f"Received: {type(fmodel)} and {type(fmodel)}.")
    return summary
