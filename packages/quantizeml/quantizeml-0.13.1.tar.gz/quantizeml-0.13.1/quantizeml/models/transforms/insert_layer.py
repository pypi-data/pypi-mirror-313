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
Utility methods to insert layers in a model.
"""

__all__ = ['insert_layer', 'insert_rescaling', 'insert_in_config']

from copy import deepcopy

from keras.layers import serialize, InputLayer, Rescaling
from keras.models import Model, Sequential

from .transforms_utils import (get_layer_index, inbound_node_generator,
                               replace_layer_name_for_connection_info, get_layers_by_type)
from ..utils import apply_weights_to_model
from ...layers.quantizers import OutputQuantizer, Dequantizer


def insert_in_config(model, target_layer_name, new_layer, config, outbound_names=None):
    """ Inserts the given layer in the model after the layer with the name target_layer_name by
    editing the given configuration.

    Args:
        model (keras.Model): the model to update
        target_layer_name (str): name of the layer after which to insert a layer
        new_layer (keras.layers.Layer): layer to insert
        config (dict): model dict config being updated
        outbound_names (list, optional): list of outbounds layers names for the inserted
            layer. When not specified, the outbound_names outbounds are retrieved from the given
            model. Providing incoherent names will result in an invalid model graph. Defaults to
            None.
    """
    layers_config = config['layers']

    # Prepare the layer configuration to be inserted
    new_layer_config = serialize(new_layer)

    # Handling sequential and functional models differently:
    #   - sequential models 'layers' configuration is a sorted list of the layers, so we just need
    #     to insert the new layer within that list,
    #   - for functional models, the layers inbound and outbounds are updated first
    if not isinstance(model, Sequential):
        # The layer name is added to the configuration
        new_layer_config['name'] = new_layer.name

        # Retrieve target_layer outbounds if None specified.
        if outbound_names is None:
            target_outbounds = model.get_layer(target_layer_name).outbound_nodes
            outbound_names = [outbound.layer.name for outbound in target_outbounds]

        # OutputQuantizer does not support multiple inputs so target layers with multiple outputs
        # are rejected
        if len(outbound_names) > 1 and isinstance(new_layer, OutputQuantizer):
            raise RuntimeError("Inserting an OutputQuantizer after a layer with multiple outputs "
                               "is not supported.")

        if len(outbound_names):
            # Initialize the new layer inbounds
            new_layer_inbounds = []

            # Replace inbounds from the layers after the target layer with the inserted layer
            outbound_ids = [get_layer_index(layers_config, outbound) for outbound in outbound_names]
            for id in outbound_ids:
                for inbound_node in inbound_node_generator(layers_config[id]):
                    if isinstance(inbound_node, dict):
                        inbound_node = inbound_node.values()
                    for connection_info in inbound_node:
                        matched = replace_layer_name_for_connection_info(connection_info,
                                                                         target_layer_name,
                                                                         new_layer.name)
                        # Store the replaced inbound as it will later be used by the inserted layer
                        if matched and matched not in new_layer_inbounds:
                            new_layer_inbounds.append(matched)

            # Set the inserted layer inbounds
            new_layer_config['inbound_nodes'] = [new_layer_inbounds]

        else:
            # If target layer has no outbounds (ie. it's a model output), update the model
            # output layers list
            for index, out_layer in enumerate(config['output_layers']):
                if out_layer[0] == target_layer_name:
                    config['output_layers'][index][0] = new_layer.name

            # The inserted layer takes the target layer as its inbound
            new_layer_config['inbound_nodes'] = [[[target_layer_name, 0, 0, {}]]]

    # The new layer configuration can now be inserted into the layers config
    layers_config.insert(get_layer_index(layers_config, target_layer_name) + 1, new_layer_config)


def _insert_layer(model, target_layer_name, new_layer):
    """ Inserts the given layer in the model after the layer with the name target_layer_name.

    Args:
        model (keras.Model): the model to update
        target_layer_name (str): name of the layer after which to insert a layer
        new_layer (keras.layers.Layer): layer to insert

    Returns:
        keras.Model: the new model
    """
    # Check that the model has a layer with then given target_layer_name
    if not any(ly.name == target_layer_name for ly in model.layers):
        raise ValueError(f'{target_layer_name} not found in model.')

    # get_config documentation mentions that a copy should be made when planning to modify the
    # config
    config = deepcopy(model.get_config())

    # Insert layer in config graph
    insert_in_config(model, target_layer_name, new_layer, config)

    # Reconstruct model from the config
    if isinstance(model, Sequential):
        new_model = Sequential.from_config(config)
    else:
        new_model = Model.from_config(config)

    # Load original weights
    variables_dict = {var.name: var for var in model.variables}
    apply_weights_to_model(new_model, variables_dict, False)
    return new_model


def insert_layer(model, target_layer_name, new_layer):
    """ Inserts the given layer in the model after the layer with the name target_layer_name.

    Note that new_layer type is restricted to (OutputQuantizer, Dequantizer).

    Args:
        model (keras.Model): the model to update
        target_layer_name (str): name of the layer after which to insert a layer
        new_layer (keras.layers.Layer): layer to insert

    Raises:
        ValueError: when target_layer_name is not found in model or new_layer is not in
            (OutputQuantizer, Dequantizer)

    Returns:
        keras.Model: the new model
    """
    # Check added layer type
    if not isinstance(new_layer, (OutputQuantizer, Dequantizer)):
        raise ValueError(f'Inserted layer must be of type OutputQuantizer or Dequantizer, \
                        `received {type(new_layer)}.')

    return _insert_layer(model, target_layer_name, new_layer)


def insert_rescaling(model, scale, offset):
    """ Inserts a Rescaling as first layer of the Model (after the Input)

    Args:
        model (keras.Model): the model to update
        scale (float): the Rescaling scale
        offset (float): the Rescaling offset

    Raises:
        ValueError: when the Model does not have an Input layer.

    Returns:
        keras.Model: the new model
    """
    first_layers = get_layers_by_type(model, InputLayer)
    if len(first_layers) == 0:
        raise ValueError("Inserting a Rescaling layer in a Model without an Input layer is not"
                         " supported.")
    for target_layer in first_layers:
        model = _insert_layer(model, target_layer.name, Rescaling(scale, offset))
    return model
