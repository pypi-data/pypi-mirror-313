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
ReLU > MaxPool inversion helper.
"""

__all__ = ["invert_relu_maxpool"]

from keras.layers import MaxPool2D, ReLU

from .transforms_utils import find_layers_pairs, invert_layer_pairs


def invert_relu_maxpool(model):
    """ Inverts ReLU and MaxPool2D layers in a model to have MaxPool2D before ReLU.

    This transformation produces a strictly equivalent model.

    Args:
        model (keras.Model): a model

    Returns:
        keras.Model: keras.Model: the original model or the updated model
    """
    # Find ReLU followed by MaxPool2D layer pairs that are candidates for inversion
    map_relu_mp = find_layers_pairs(model, ReLU, MaxPool2D)

    # When there are no valid candidates, return the original model
    if not map_relu_mp:
        return model

    # Rebuild a model with MP and ReLU inverted by editing the configuration
    return invert_layer_pairs(model, map_relu_mp)
