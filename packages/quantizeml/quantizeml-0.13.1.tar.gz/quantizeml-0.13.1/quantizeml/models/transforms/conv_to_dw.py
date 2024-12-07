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
"""
Helper that replaces Conv2D layers to DepthwiseConv2D when they behave as the latest.
"""

__all__ = ["convert_conv_to_dw_conv"]

import numpy as np
from copy import deepcopy
from keras.layers import Conv2D

from .transforms_utils import get_layers_by_type, get_layer_index


def convert_conv_to_dw_conv(model):
    """ Replaces Conv2D layers from a model to DepthwiseConv2D layers
    if groups==filters==input_channels, since they will have the same behavior.

    Args:
        model (keras.Model): the model of interest

    Returns:
        keras.Model: the original model or the modified one.
    """

    # Get all Conv2D layers present in the model
    conv2ds = get_layers_by_type(model, Conv2D)

    # When there are no valid candidates, return the original model
    if not conv2ds:
        return model

    # Copy configuration before applying modifications
    config = deepcopy(model.get_config())

    convertible_conv2d_names = list()
    for conv2d in conv2ds:
        layer_index = get_layer_index(config['layers'], conv2d.name)
        conv_config = config['layers'][layer_index]
        # Set useful param alias
        conv_input_channel = conv2d.input_shape[-1]
        conv_groups = conv_config['config']['groups']
        conv_filters = conv_config['config']['filters']
        # If in_channel==groups==filters the layer behaves as a DepthwiseConv2D
        if conv_input_channel == conv_groups == conv_filters:
            # keep track of convertible Conv2D layers
            convertible_conv2d_names.append(conv2d.name)
            conv_config['class_name'] = 'DepthwiseConv2D'
            for param in ['kernel_regularizer', 'kernel_initializer', 'kernel_constraint']:
                conv_config['config'][param.replace(
                    'kernel', 'depthwise')] = conv_config['config'].pop(param)
            for param in ['filters', 'groups']:
                conv_config['config'].pop(param)
    # Reconstruct model from the config
    updated_model = model.from_config(config)

    # Restore model weights
    for layer in updated_model.layers:
        weights = model.get_layer(layer.name).get_weights()
        # In order to set Conv2D (depthwise like) kernel into the newly created equivalent
        # DepthwiseConv2D, the last two dims of the kernel should be transposed.
        if layer.name in convertible_conv2d_names:
            assert weights[0].ndim == 4, "the layer kernel must have 4 dims"
            assert weights[0].shape[2] == 1, "The kernel 3rd dim must be 1"
            # Depthwise spatial kernels: ((H, W, C=1, F)) -> (H, W, F, 1)
            weights[0] = np.transpose(weights[0], axes=[0, 1, 3, 2])
        layer.set_weights(weights)

    return updated_model
