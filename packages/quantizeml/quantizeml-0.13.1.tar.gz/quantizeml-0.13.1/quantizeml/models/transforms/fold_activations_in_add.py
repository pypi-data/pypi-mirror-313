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
"""
Transformation to fold unbounded ReLU layers that come after an Add layer.
"""

__all__ = ['fold_activations_in_add']

import keras.layers

from copy import deepcopy
from keras.saving import serialize_keras_object

from ... import layers as quantizeml_layers
from ..utils import apply_weights_to_model
from .transforms_utils import get_layer_index, get_layers, find_layers_pairs, update_inbound


def fold_activations_in_add(model):
    """Returns a new model where Activation layers (Unbounded ReLU) are folded
    into previous Add layers.

    Args:
        model (keras.Model): a model

    Returns:
        keras.Model: the original model or a model with Unbounded ReLU
        layers folded in their preceding Add Layer
    """
    map_add_layer_to_relu = _find_add_relu_to_fold(model)

    # When there are no valid candidates, return the original model
    if len(map_add_layer_to_relu) == 0:
        return model

    model_folded = _fold_activations_in_add(model, map_add_layer_to_relu)

    return model_folded


def _find_add_relu_to_fold(model):
    """Retrieves ReLU layers that can be folded.

    Only ReLUs without a specified maximum value (i.e., unbounded ReLUs)
    that comes after an Add layer are expected to be folded.

    Args:
        model (keras.Model): a model

    Returns:
        dict: map between an Add layer and its ReLU layer to be folded
    """
    supported_layers = (keras.layers.Add, quantizeml_layers.Add)
    add_layer_to_relu_candidates = find_layers_pairs(model, supported_layers, keras.layers.ReLU)

    # Remove pairs that do not meet the condition
    map_add_layer_to_relu = {}
    for inbound, relu in add_layer_to_relu_candidates.items():
        # if the ReLU after the Add has a max_value, we don't fold it
        if relu.max_value is not None:
            continue
        map_add_layer_to_relu[inbound] = relu
    return map_add_layer_to_relu


def _fold_activations_in_add(model, map_add_layer_to_relu):
    """Edits the model configuration to remove ReLU layer and rebuilds a model.

    Args:
        model (keras.Model): a model
        map_add_layer_to_relu (dict): map between an Add layer and its ReLU layer to be folded

    Returns:
        keras.Model: an updated model with Unbounded ReLU layers folded in their preceding Add Layer
    """
    config = deepcopy(model.get_config())
    layers = config['layers']
    new_output_name = None

    for add_layer, relu_layer in map_add_layer_to_relu.items():
        # get index of add layer
        add_index = get_layer_index(layers, add_layer.name)
        name_add = add_layer.name

        # Update Add layer config
        new_config = quantizeml_layers.Add.from_config(layers[add_index]['config'])
        layers[add_index].update(serialize_keras_object(new_config))
        layers[add_index]['config']['activation'] = True

        # Get the layers after relu, ie. outbounds layers
        relu_outbound_names = [outbound.layer.name for outbound in relu_layer.outbound_nodes]
        outbound_ids = [get_layer_index(layers, relu_outbound)
                        for relu_outbound in relu_outbound_names]

        # If ReLU is the last layer (no outbound), store its name and inbound name so that the model
        # output can be updated later
        if len(outbound_ids) == 0:
            new_output_name = name_add
            last_relu = relu_layer.name

        for id in outbound_ids:
            update_inbound(layers[id], relu_layer.name, name_add)

    # Remove ReLU layer
    layers_to_remove = get_layers(config, [relu.name for relu in map_add_layer_to_relu.values()])
    for layer_to_remove in layers_to_remove:
        layers.remove(layer_to_remove)

    # Update the model outputs if needed
    if new_output_name:
        for index, out_layer in enumerate(config['output_layers']):
            if out_layer[0] == last_relu:
                config['output_layers'][index][0] = new_output_name

    updated_model = model.from_config(config)
    variables_dict = {var.name: var for var in model.variables}
    apply_weights_to_model(updated_model, variables_dict)

    return updated_model
