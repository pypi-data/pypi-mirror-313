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
"""
Transformation to fold BatchNormalization layers in a model.
"""

__all__ = ['fold_batchnorms']

import keras
import numpy as np
import tensorflow as tf

from copy import deepcopy
from keras.layers import (BatchNormalization, Conv2D, SeparableConv2D, Dense, DepthwiseConv2D,
                          Conv2DTranspose)

from .transforms_utils import get_layers, get_layer_index, update_inbound, find_layers_pairs
from ..utils import apply_weights_to_model
from ...layers import (PaddedConv2D, QuantizedConv2D, QuantizedSeparableConv2D, QuantizedDense,
                       QuantizedDepthwiseConv2D, QuantizedConv2DTranspose, DepthwiseConv2DTranspose,
                       QuantizedDepthwiseConv2DTranspose, BufferTempConv, DepthwiseBufferTempConv)


def fold_batchnorms(model):
    """Returns a new model where BatchNormalization layers are folded into previous layers.

    From a Keras model where BN layers follow processing layers, this function removes the BN layers
    and updates the preceding layers weights and bias accordingly. The new model is strictly
    equivalent to the previous one.

    Args:
        model (keras.Model): a model

    Returns:
        keras.Model: the original model or a model with BN folded
    """
    # Find foldable BN and their inbound
    map_prev_layer_to_bn = _find_batchnorms_to_fold(model)

    # When there are no valid candidates, return the original model
    if len(map_prev_layer_to_bn) == 0:
        return model

    # Rebuild a model without BN by editing the configuration
    model_folded = _get_BN_less_model(model, map_prev_layer_to_bn)

    # Set folded weights in the new model
    for layer, bn in map_prev_layer_to_bn.items():
        new_weights = _compute_BN_folded_weights(layer, bn)
        model_folded.get_layer(layer.name).set_weights(new_weights)

    return model_folded


def _find_batchnorms_to_fold(model):
    """ Retrieves BatchNormalization layers that can be folded.

    This is limited to BN layers that follow supported layer types.

    Args:
        model (keras.Model): a model

    Returns:
        dict: map between a layer and its BN layer to be folded

    Raises:
        RuntimeError: if the candidate BN has null gammas or BN is not applied on the last axis.
    """

    supported_layers = (Conv2D, PaddedConv2D, Conv2DTranspose, SeparableConv2D, DepthwiseConv2D,
                        Dense, QuantizedConv2D, QuantizedConv2DTranspose, QuantizedSeparableConv2D,
                        QuantizedDepthwiseConv2D, QuantizedDense, DepthwiseConv2DTranspose,
                        QuantizedDepthwiseConv2DTranspose, BufferTempConv, DepthwiseBufferTempConv)

    # Map between a layer and its following BN layer
    map_prev_layer_to_bn = find_layers_pairs(model, supported_layers, BatchNormalization)

    # Check valid "layer -> BN" candidates
    for bn in map_prev_layer_to_bn.values():
        # Null gammas are not supported: once folded, new kernel would be zero
        gamma = bn.get_weights()[0]
        if np.any(gamma == 0):
            raise RuntimeError(f"There are {np.sum(gamma == 0)} null gammas in the "
                               f"BatchNormalization layer '{bn.name}'. Null gammas are "
                               "not supported.")

        # Check BN axis parameter
        if (len(bn.axis) != 1 or bn.axis[0] != len(bn.input_shape) - 1):
            raise RuntimeError(f"The BatchNormalization must be applied on the last "
                               f"axis. '{bn.name}' layer has axis={bn.axis}.")
    return map_prev_layer_to_bn


def _get_BN_less_model(model, map_prev_layer_to_bn):
    """ Edits the model configuration to remove BN layer and rebuilds a model.

    Args:
        model (keras.Model): a model
        map_prev_layer_to_bn (dict): map between a layer and its BN layer to be folded

    Returns:
        keras.Model: an updated model without BN layers
    """
    # get_config documentation mentions that a copy should be made when planning to modify the
    # config
    config = deepcopy(model.get_config())
    layers = config['layers']
    new_output_name = None

    for prev_layer, layer_bn in map_prev_layer_to_bn.items():
        # Set use_bias=True in layers where BN are folded to accept new computed weights
        prev_index = get_layer_index(layers, prev_layer.name)
        layers[prev_index]['config']['use_bias'] = True

        # For sequential model, the changes stop here: the BN layers will simply be removed in the
        # following step. For other models, the layers inbounds/outbounds must be rebuilt.
        if isinstance(model, keras.Sequential):
            continue

        # Retrieve the BN input layer. Assumes that BN has only 1 inbound.
        bn_index = get_layer_index(layers, layer_bn.name)
        # tfmot code: 'inbound_nodes' is a nested list where first element is the inbound layername,
        # e.g: [[['conv1', 0, 0, {} ]]]
        updated_inbound = layers[bn_index]['inbound_nodes'][0][0][0]

        # Get the layers after BN, ie. outbounds layers
        bn_outbound_names = [outbound.layer.name for outbound in layer_bn.outbound_nodes]
        outbound_ids = [get_layer_index(layers, bn_outbound) for bn_outbound in bn_outbound_names]

        # If BN is the last layer (no outbound), store its name and inbound name so that the model
        # output can be updated later
        if len(outbound_ids) == 0:
            new_output_name = updated_inbound
            last_bn = layer_bn.name

        # Update BN outbounds layers: their current inbound is the BN layer that will be folded so
        # it must be replaced with the BN previous layer (folding target or the BN inbound). This
        # results in by-passing the BN layer: inbound > BN > outbounds becomes inbound > outbounds.
        for id in outbound_ids:
            update_inbound(layers[id], layer_bn.name, updated_inbound)

    # Remove BN layers
    layers_to_remove = get_layers(config, [bn.name for bn in map_prev_layer_to_bn.values()])
    for layer_to_remove in layers_to_remove:
        layers.remove(layer_to_remove)

    # Update the model outputs if needed
    if new_output_name:
        for index, out_layer in enumerate(config['output_layers']):
            if out_layer[0] == last_bn:
                config['output_layers'][index][0] = new_output_name

    # Reconstruct model from the config, using the cloned layers.
    updated_model = model.from_config(config)

    # Restore model weights
    variables_dict = {var.name: var for var in model.variables}
    apply_weights_to_model(updated_model, variables_dict, False)
    return updated_model


def _compute_BN_folded_weights(target_layer, bn_layer):
    """ Computes the new weights of a layer after folding BatchNormalization into it.

    Args:
        target_layer (keras.layers.Layer): the layer where BN will be folded
        bn_layer (keras.layers.Layer): the BatchNormalization layer to fold into the preceding layer

    Returns:
        list: the new weights to set in the folded destination layer.
    """
    # Get kernel and bias weights of the target layer
    kernel_position = 0
    bias_position = 1
    if isinstance(target_layer, SeparableConv2D):
        kernel_position = 1
        bias_position = 2

    weights = target_layer.get_weights()
    kernel = weights[kernel_position]
    bias = weights[bias_position] if target_layer.use_bias else 0

    # Get BN weights
    gamma, beta, mean, var = bn_layer.get_weights()
    scale_BN = gamma / np.sqrt(var + bn_layer.epsilon)

    # Compute new folded kernel and bias
    if isinstance(target_layer, DepthwiseConv2D):
        # Last dimension of DepthwiseConv2D kernel is 1 so scale_BN should be reshaped to (shape, 1)
        # (first two dimensions will be broadcasted)
        new_kernel = kernel * scale_BN.reshape(*scale_BN.shape, 1)
    elif isinstance(target_layer, Conv2DTranspose):
        # Handle Conv2DTranspose kernels that are (h, w, filters, channels) instead of (h, w,
        # channels, filters)
        new_kernel = tf.transpose(kernel, (0, 1, 3, 2)) * scale_BN
        new_kernel = tf.transpose(new_kernel, (0, 1, 3, 2))
    else:
        new_kernel = kernel * scale_BN
    new_bias = beta + (bias - mean) * scale_BN

    # Return all weights with modified ones
    new_weights = weights
    new_weights[kernel_position] = new_kernel
    if target_layer.use_bias:
        new_weights[bias_position] = new_bias
    else:
        new_weights.append(new_bias)

    return new_weights
