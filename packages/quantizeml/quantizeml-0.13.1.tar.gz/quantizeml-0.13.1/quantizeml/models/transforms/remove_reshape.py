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
Multiple Reshape/Flatten transformations
"""

__all__ = ["remove_reshape"]

from keras.layers import Reshape, Flatten
from keras.models import Sequential
from copy import deepcopy
from .transforms_utils import get_layers, get_layer_index, update_inbound


def _find_reshape_flatten_sequence(model):
    """ Retrieves a Reshape/Flatten layer that is followed by another

    Args:
        model (keras.Model): the model

    Returns:
        keras.layer: a Reshape or Flatten layer that is followed by another. Or None if not found.
    """
    expected_type = (Reshape, Flatten)
    for layer in model.layers:
        # Find candidate layer and get the type of the next layer if there is one
        if isinstance(layer, expected_type) and len(layer.outbound_nodes) == 1:
            outbound = layer.outbound_nodes[0].layer
            if isinstance(outbound, expected_type):
                return layer
    return None


def _get_layer_less_model(model, layer_del):
    """ Edits the model configuration to remove the layer_del and rebuilds a model.

    Args:
        model (keras.Model): the model
        layer_del (keras.layer): the layer to delete

    Returns:
        keras.Model: the updated model without the layer to delete
    """
    # get_config documentation mentions that a copy should be made when planning to modify the
    # config.
    config = deepcopy(model.get_config())
    layers = config['layers']

    # For sequential model, the changes stop here: the layer will simply be removed in the
    # following step. For other models, the layers inbounds/outbounds must be rebuilt.
    if not isinstance(model, Sequential):
        del_index = get_layer_index(layers, layer_del.name)
        # tfmot code: 'inbound_nodes' is a nested list where first element is the inbound layername,
        # e.g: [[['conv1', 0, 0, {} ]]]
        updated_inbound = layers[del_index]['inbound_nodes'][0][0][0]

        # Get the layers after del_index, ie. outbounds layers
        del_outbound_names = [outbound.layer.name for outbound in layer_del.outbound_nodes]
        outbound_ids = [
            get_layer_index(layers, del_outbound) for del_outbound in del_outbound_names]

        # "inbound > layer_del > outbounds" becomes "inbound > outbounds"
        for id in outbound_ids:
            update_inbound(layers[id], layer_del.name, updated_inbound)

    # Remove the layer
    layers_to_remove = get_layers(config, layer_del.name)
    assert len(layers_to_remove) == 1
    layers.remove(layers_to_remove[0])

    # Reconstruct model from the config, using the cloned layers
    updated_model = model.from_config(config)

    return updated_model


def remove_reshape(model):
    """ Multiple Reshape/Flatten transformations

    The patterns are:
    - Reshape + Reshape → Reshape
    - Flatten + Flatten → Flatten
    - Reshape + Flatten → Flatten
    - Flatten + Reshape → Reshape

    Args:
        model (keras.Model): a model

    Returns:
        keras.Model: the original model or the updated model if needed
    """
    # We consider successively the following sequences of layers:
    # Reshape > Reshape or Reshape > Flatten or Flatten > Reshape or Flatten > Flatten
    updated_model = model
    while True:
        # Find a layer that matches with the layers pattern
        layers_to_delete = _find_reshape_flatten_sequence(updated_model)
        if layers_to_delete is None:
            break  # No more layer to delete

        # We remove the selected layer
        updated_model = _get_layer_less_model(updated_model, layers_to_delete)

    # Restore model weights if there is a transformation
    if model != updated_model:
        updated_model.set_weights(model.get_weights())

    return updated_model
