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
Transforms utility methods.
"""

from copy import deepcopy

from keras.models import Sequential
from keras.layers import Layer


def get_layers(config, layer_names):
    """Extracts layers from a model configuration.

    Args:
        config (dict): JSON formatted model configuration
        layer_names (list): list of layer names to extract

    Returns:
        list: layers configurations
    """
    return [layer for layer in config['layers'] if layer['config']['name'] in layer_names]


def get_layer_index(layers, layer_name):
    """Retrieves the layer index within the layer list.

    Args:
        layers (list): list of JSON formatted layers configurations
        layer_name (str): layer name to retrieve

    Returns:
        int: the layer index
    """
    for index, ly in enumerate(layers):
        if ly['config']['name'] == layer_name:
            return index
    return -1


def inbound_node_generator(layer):
    """Layer configuration inbound node generator.

    Args:
        layer (dict): JSON formatted layer configuration

    Yields:
        list: inbound node
    """
    for inbound_node in layer['inbound_nodes']:
        if (isinstance(inbound_node, list) and len(inbound_node) > 0 and
                isinstance(inbound_node[0], str)):
            yield [inbound_node]
        else:
            yield inbound_node


def replace_layer_name_for_connection_info(connection_info, match_name, replacement_name):
    """Updates an inbound node name.

    Args:
        connection_info (list): inbound node information
        match_name (str): inbound node name to update
        replacement_name (str): inbound node name to set

    Returns:
        list: the original inbound node if an update happened, None otherwise
    """
    # Note that is from tfmot and the connection_info structure is not really documented:
    # it is a nested list where the first item is the inbound layer name.
    # For example: [[['conv1', 0, 0, {} ]]] or [[['batch_normalization', 0, 0, {}]]]
    original_info = connection_info.copy()
    match_found = False
    if connection_info[0] == match_name:
        match_found = True
        connection_info[0] = replacement_name
    for key in connection_info[3]:
        if isinstance(connection_info[3][key], list):
            if connection_info[3][key][0] == match_name:
                match_found = True
                connection_info[3][key][0] = replacement_name
    return original_info if match_found else None


def get_layers_by_type(model, layer_type):
    """Recursively find layers matching the specified type.

    Args:
        model (keras.Model): the source model.
        layer_type (class): the Layer class to look for.

    Returns:
        list(keras.layers.Layer): a list of layers
    """
    def _get_layers(layer, layers):
        if isinstance(layer, layer_type):
            layers.append(layer)
        for attr in layer.__dict__.values():
            if isinstance(attr, Layer):
                _get_layers(attr, layers)
    layers = []
    for layer in model.layers:
        _get_layers(layer, layers)
    return layers


def update_inbound(layer_config, name, updated_inbound):
    """ Update the layer 'name' inbound in config with the provided name.

    Args:
        layer_config (dict): layer config to udpate
        name (str): name of the inbound to replace
        updated_inbound (str): new inbound name
    """
    for inbound_node in inbound_node_generator(layer_config):
        if isinstance(inbound_node, dict):
            inbound_node = inbound_node.values()
        for connection_info in inbound_node:
            replace_layer_name_for_connection_info(connection_info, name, updated_inbound)


def find_layers_pairs(model, first_type, second_type):
    """ Retrieves first_type > second_type layer pairs in a model.

    Args:
        model (keras.Model): a model
        first_type (keras.Layer): a first layer
        second_type (keras.Layer): a second layer

    Returns:
        dict: layer pairs
    """
    pairs = {}

    # Get all 'second_type' layers present in the model
    dst_layers = get_layers_by_type(model, second_type)

    # Find 'second_type' layers that have only one inbound layer that is a 'first_type' layer
    # and  that at the same time it has a single outbound ('second_type').
    for ly in dst_layers:
        parent_layer = ly.inbound_nodes[0].inbound_layers
        if isinstance(parent_layer, first_type) and len(parent_layer.outbound_nodes) == 1:
            pairs[parent_layer] = ly
    return pairs


def invert_layer_pairs(model, pairs):
    """ Edits the model configuration to invert the layer pairs and rebuilds a model.

    Args:
        model (keras.Model): a model
        pairs (dict): map between a layer and its outbound

    Returns:
        keras.Model: an updated model
    """
    # get_config documentation mentions that a copy should be made when planning to modify the
    # config
    config = deepcopy(model.get_config())
    layers = config['layers']
    new_output_name = None

    for first, second in pairs.items():
        # Retrieve layer indexes
        first_index = get_layer_index(layers, first.name)
        second_index = get_layer_index(layers, second.name)

        if isinstance(model, Sequential):
            # For Sequential model, inverting the indexes is enough
            layers[second_index], layers[first_index] = layers[first_index], layers[second_index]
        else:
            # For functional models, inbounds must be updated
            original_first_inbound = layers[first_index]['inbound_nodes'][0][0][0]

            # Update 'second' by replacing the 'first' inbound with the 'first' previous layer
            update_inbound(layers[second_index], first.name, original_first_inbound)
            # Update 'first' by replacing the original inbound with 'second'
            update_inbound(layers[first_index], original_first_inbound, second.name)

            # Then get the layers after 'second', ie. outbounds layers
            second_outbound_names = [outbound.layer.name for outbound in second.outbound_nodes]
            outbound_ids = [
                get_layer_index(layers, bn_outbound)
                for bn_outbound in second_outbound_names
            ]

            # If 'second' is the last layer (no outbound), store its name and the associated 'first'
            # name so that the model output can be updated later
            if len(outbound_ids) == 0:
                new_output_name = first.name
                last_mp = second.name

            # Finally, update the outbounds by replacing their 'second' inbound with 'first'
            for id in outbound_ids:
                update_inbound(layers[id], second.name, first.name)

    # Update the model outputs if needed
    if new_output_name:
        for index, out_layer in enumerate(config['output_layers']):
            if out_layer[0] == last_mp:
                config['output_layers'][index][0] = new_output_name

    # Reconstruct model from the config, using the cloned layers
    updated_model = model.from_config(config)

    # Restore model weights
    updated_model.set_weights(model.get_weights())
    return updated_model


def get_inbound_layers_config(layer, model_config):
    """ Retrieve the inbound layers config of 'layer'

    Args:
        layer (dict): the target layer
        model_config (dict): the config where to search the inbounds

    Returns:
        list: the config of the inbound layers
    """
    if 'inbound_nodes' in layer:
        # The config comes from a keras.Model.
        # First, recover layer names
        inbound_layer_names = []
        for inbound_node in inbound_node_generator(layer):
            if isinstance(inbound_node, dict):
                inbound_node = inbound_node.values()
            for connection_info in inbound_node:
                inbound_layer_names.append(connection_info[0])
        # Next, match name with layer config
        inbound_layers = get_layers(model_config, inbound_layer_names)
    else:
        # The config comes from a keras.Sequential.
        # Inbound layer can be found from the index of the layer
        layer_id = model_config['layers'].index(layer)
        inbound_layers = [model_config['layers'][layer_id - 1]] if layer_id > 0 else []
    return inbound_layers
