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
Tools to remove ZeroPadding2D layers from a model.
"""

__all__ = ["remove_zeropadding2d"]

from copy import deepcopy

from keras.models import Sequential
from keras.layers import ZeroPadding2D, Conv2D, SeparableConv2D, DepthwiseConv2D

from .transforms_utils import get_layers, get_layer_index, get_layers_by_type, update_inbound


def _find_removable_zeropadding(model):
    """ Retrieves ZeroPadding2D layers that can be removed.

    This is limited to ZeroPadding2D layers that come before supported layer types and that perform
    a 'same' padding.

    Args:
        model (keras.Model): a model

    Returns:
        dict: map between a ZeroPadding2D and the layer that follows
    """
    map_zeropadding_next = {}

    # Define layers that will support ZeroPadding removal
    supported_layers = (Conv2D, SeparableConv2D, DepthwiseConv2D)

    # Get all ZeroPadding2D layers present in the model
    zeropaddings = get_layers_by_type(model, ZeroPadding2D)

    # Sequential models must be built because a check must be done on shapes
    if zeropaddings and isinstance(model, Sequential) and not model.built:
        raise ValueError("This model has not yet been built.")

    # Find the ones that can be removed
    for zeropadding in zeropaddings:
        # Limit support to single inbound/outbound
        outbounds = zeropadding.outbound_nodes
        if len(zeropadding.inbound_nodes) != 1 or len(outbounds) != 1:
            continue

        # Check that the layer that follows is supported and has a 'valid' padding
        following_layer = outbounds[0].layer
        if not isinstance(following_layer, supported_layers) or following_layer.padding != 'valid':
            continue

        # Check that the combination of ZeroPadding2D + following layer performs a 'same' padding:
        # this is done by checking that next_layer.output_shape * strides = zeropadding.input_shape
        out_spatial_dims = following_layer.output_shape[1:3]
        stride = following_layer.strides
        rectified_out_spatial_dims = tuple(dim * s for dim, s in zip(out_spatial_dims, stride))
        if rectified_out_spatial_dims != zeropadding.input_shape[1:3]:
            continue

        # At this point the ZeroPadding2D is a valid candidate
        map_zeropadding_next[zeropadding] = following_layer
    return map_zeropadding_next


def _get_zeropadding_less_model(model, map_zeropadding_next):
    """ Edits the model configuration to remove ZeroPadding2D layers and rebuilds a model.

    Args:
        model (keras.Model): a model
        map_zeropadding_next (dict): map between a ZeroPadding2D and the layer that follows

    Returns:
        keras.Model: an updated model without ZeroPadding2D layers
    """
    # get_config documentation mentions that a copy should be made when planning to modify the
    # config
    config = deepcopy(model.get_config())
    layers = config['layers']

    for zeropadding, next_layer in map_zeropadding_next.items():
        # Set padding='same' in the layer that follows a ZeroPadding that will be removed
        next_index = get_layer_index(layers, next_layer.name)
        layers[next_index]['config']['padding'] = 'same'

        # For sequential model, the changes stop here: the ZeroPadding2D layers will simply be
        # removed in the following step. For other models, the layers inbounds/outbounds must be
        # rebuilt.
        if isinstance(model, Sequential):
            continue

        # Retrieve the ZeroPadding2D input layer, assuming it has only 1 inbound
        zeropadding_index = get_layer_index(layers, zeropadding.name)
        # tfmot code: 'inbound_nodes' is a nested list where first element is the inbound layername,
        # e.g: [[['conv1', 0, 0, {} ]]]
        updated_inbound = layers[zeropadding_index]['inbound_nodes'][0][0][0]

        # Update ZeroPadding2D outbounds layers: their current inbound is the ZeroPadding2D layer
        # that will be removed so it must be replaced with the ZeroPadding2D previous layer. This
        # results in by-passing the ZeroPadding2D layer: inbound > ZeroPadding2D > outbounds becomes
        # inbound > outbounds.
        update_inbound(layers[next_index], zeropadding.name, updated_inbound)

    # Remove ZeroPadding2D layers
    layers_to_remove = get_layers(config, [zp.name for zp in map_zeropadding_next.keys()])
    for layer_to_remove in layers_to_remove:
        layers.remove(layer_to_remove)

    # Reconstruct model from the config, using the cloned layers
    return model.from_config(config)


def remove_zeropadding2d(model):
    """ Removes ZeroPadding2D layers from a model.

    ZeroPadding2D layers will not be supported by quantization so this transform adds support so
    that when the ZeroPadding2D layers are immediately followed by a convolution layer with 'valid'
    padding, they are removed and the following convolution is updated with a 'same' padding
    instead. This can however only happen when the padding specified in ZeroPadding2D actually
    corresponds to a 'same' padding.

    Args:
        model (keras.Model): the model to update

    Returns:
        keras.Model: the original model or a new model with ZeroPadding2D removed
    """
    # Find ZeroPadding2D and following layer pairs that are candidates for removal
    map_zeropadding_next = _find_removable_zeropadding(model)

    # When there are no valid candidates, return the original model
    if not map_zeropadding_next:
        return model

    # Rebuild a model without ZeroPadding2D by editing the configuration
    updated_model = _get_zeropadding_less_model(model, map_zeropadding_next)

    # Restore model weights
    updated_model.set_weights(model.get_weights())
    return updated_model
