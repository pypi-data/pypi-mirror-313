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
Helper that replaces lambdas with their equivalent Keras layer.
"""

__all__ = ["replace_lambda"]

from copy import deepcopy
from keras.layers import Activation
from keras.src.layers import TFOpLambda

from .transforms_utils import get_layers_by_type, get_layer_index, inbound_node_generator


def _update_inbound_nodes(layer_config, target):
    """ Update a Lambda layer inbound node towards their Layer equivalent.

    Args:
        layer_config (dict): config of the lambda layer
        target (str): class name of the target layer

    Returns:
        str: name of the lambda operation
    """
    name = None
    if 'inbound_nodes' not in layer_config:
        # A layer from a sequence model does not have 'inbound_nodes'.
        # So, nothing to do in this case
        return name
    for inbound_node in inbound_node_generator(layer_config):
        if isinstance(inbound_node, dict):
            inbound_node = inbound_node.values()
        connection_info = inbound_node[0]
        # "connection_info[-1]" holds the lambda config, that is the op name and other lambda
        # specific parameters. Code below will retrieve meaningful parameters that will be used to
        # define the config of the new layer and will then be dropped.
        if target == 'Reshape':
            # Set the 'target_shape' parameter from the 'shape' attribute
            layer_config['config']['target_shape'] = connection_info[-1].get('shape')
        elif target == 'Permute':
            # Set the 'dims' parameter from the 'perm' attribute
            perm = connection_info[-1].get('perm')
            # Permute 'dims' must start at 1 but transpose 'perm' starts at 0
            layer_config['config']['dims'] = [p + 1 for p in perm]
        elif target == "Add":
            # Get the second inbound currently defined as {'y': ['name', 0, 0]}
            other_inbound = connection_info[-1].get('y')
            # Modify it to fit the ['name', 0, 0, {}] convention
            other_inbound.append({})
            # Add the updated inbound into the inbound_node list and set it in layer_config
            inbound_node.append(other_inbound)
            layer_config['inbound_nodes'] = [inbound_node]
        # Retrieve the lambda name as it will be used to set the name for the layer
        name = connection_info[-1].get('name', None)
        # Drop the lambda config
        connection_info[-1] = {}
    return name


def replace_lambda(model):
    """ Replaces lambda layers from a model with their equivalent Keras layer.

    This transform handles the following replacements:

        - Lambda(relu) or Activation('relu') → ReLU,
        - Lambda(transpose) → Permute,
        - Lambda(reshape) → Reshape,
        - Lambda(add) → Add,
        - Lambda('gelu') → Activation('gelu'),
        - Lambda('silu') → Activation('silu').

    Args:
        model (keras.Model): the model of interest

    Returns:
        keras.Model: the original model or a new one with lambda replaced.
    """
    # Map function names to Keras layers
    lambda_to_layer = {
        'nn.relu': 'ReLU',
        'math.add': 'Add',
        '__operators__.add': 'Add',
        'reshape': 'Reshape',
        'transpose': 'Permute',
        'compat.v1.transpose': 'Permute',
        'nn.silu': 'Activation',
        'nn.gelu': 'Activation',
    }

    # Get all Activations and TFOpLambda layers present in the model
    lambdas = get_layers_by_type(model, (Activation, TFOpLambda))

    # When there are no valid candidates, return the original model
    if not lambdas:
        return model

    # Copy configuration before applying modifications
    config = deepcopy(model.get_config())

    for layer in lambdas:
        layer_index = get_layer_index(config['layers'], layer.name)
        layer_config = config['layers'][layer_index]
        # Replace 'relu' Activations layers with ReLU layers
        if (layer_config['class_name'] == 'Activation'
                and layer_config['config']['activation'] == 'relu'):
            # Drop the 'activation' parameter and update 'class_name'
            layer_config['config'].pop('activation')
            layer_config['class_name'] = 'ReLU'
        # Replace TFOpLambda layers
        elif layer_config['class_name'] == 'TFOpLambda':
            # Retrieve the function used in the config and get the equivalent Keras layer name
            target = lambda_to_layer.get(layer_config['config']['function'], None)
            if target:
                # Drop the 'function' parameter and update 'class_name'
                op_name = layer_config['config'].pop('function').replace('nn.', '')
                layer_config['class_name'] = target
                # If target is 'Activation', put op_name in 'activation' parameter
                if target == "Activation":
                    layer_config['config']['activation'] = op_name
                # Update the inbound part of the config: the last element of the inbound list of
                # lambda layers will contain the lambda op parameters that are used to set the
                # config for the new layer.
                new_name = _update_inbound_nodes(layer_config, target)
                # If layer name was updated, use the new name everywhere in the config
                if new_name:
                    # Serialize the dict into a string
                    str_config = str(config)
                    # Replace name using 'old_name' for an exact match
                    str_config = str_config.replace(f"'{layer_config['name']}'", f"'{new_name}'")
                    # Deserialize the updated string into a dict
                    config = eval(str_config)

    # Reconstruct model from the config
    updated_model = model.from_config(config)

    # Restore model weights
    updated_model.set_weights(model.get_weights())
    return updated_model
