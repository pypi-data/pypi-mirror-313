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
Transformation to split Concatenate layers with more than two
inputs into multiple Concatenate layers with exactly two inputs.
"""

__all__ = ['split_concat_layers']

import keras
from keras.saving import serialize_keras_object

from ..utils import apply_weights_to_model
from .transforms_utils import get_layer_index


def split_concat_layers(model):
    """Returns a new model where Concatenate layers with more than two
    inputs are split into multiple Concatenate layers with exactly
    two inputs.

    Args:
        model (keras.Model): a model

    Returns:
        keras.Model: the original model or a model with Concatenate layers
        that have exactly two inputs.
    """
    concat_layers = _find_concat_with_more_than_two_inputs(model)

    # When there are no valid candidates, return the original model
    if len(concat_layers) == 0:
        return model

    updated_model = _split_concat(model, concat_layers)
    return updated_model


def _find_concat_with_more_than_two_inputs(model):
    concat_layers = []

    for layer in model.layers:
        if isinstance(layer, keras.layers.Concatenate) and len(layer.input) > 2:
            concat_layers.append(layer)

    return concat_layers


def _split_concat(model, concat_layers):
    config = model.get_config()
    layers = config["layers"]

    for concat_layer in concat_layers:
        concat_index = get_layer_index(layers, concat_layer.name)
        inbounds = layers[concat_index]['inbound_nodes'][0]

        new_layers = []
        num_inputs = len(inbounds)
        base_name = concat_layer.name
        current_input = inbounds[0][0]

        for i in range(1, num_inputs):
            # Name will be base_name for the last created Concat, for the others
            # it will be base_name_{second_inbound}
            new_name = base_name if i == num_inputs - 1 else f"{base_name}_{inbounds[i][0]}"
            # Create new Concatenate layer where the two inbound layers
            # are the current layer and the next inbound layer
            new_layer = serialize_keras_object(
                keras.layers.Concatenate.from_config(layers[concat_index]['config']))
            new_layer["inbound_nodes"] = [[[current_input, 0, 0, {}],
                                           [inbounds[i][0], 0, 0, {}]]]
            new_layer["name"] = new_name
            new_layer['config']['name'] = new_layer["name"]
            new_layers.append(new_layer)

            # Update current input
            current_input = new_layer["name"]

        layers.pop(concat_index)
        layers.extend(new_layers)

    updated_model = model.from_config(config)
    variables_dict = {var.name: var for var in model.variables}
    apply_weights_to_model(updated_model, variables_dict)

    return updated_model
