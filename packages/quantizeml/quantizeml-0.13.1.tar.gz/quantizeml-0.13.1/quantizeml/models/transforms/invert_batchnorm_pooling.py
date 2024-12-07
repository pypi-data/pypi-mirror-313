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
""" Transformation to invert BatchNormalization and Pooling layers in a model."""

__all__ = ['invert_batchnorm_pooling']

import numpy as np

from keras.layers import BatchNormalization, MaxPool2D, GlobalAvgPool2D

from .transforms_utils import find_layers_pairs, invert_layer_pairs


def invert_batchnorm_pooling(model):
    """ Inverts pooling and BatchNormalization layers in a model to have BN layer before pooling.

    Returns a new model where pooling and batch normalization layers are inverted. From a Keras
    model where pooling layers precede batch normalization layers, this function places the BN
    layers before pooling layers. This is the first step before folding BN layers into processing
    layers.

    Note:
        Inversion of layers is equivalent only if the gammas of BN layers are positive. The
        function raises an error if not.

    Args:
        model (keras.Model): a model

    Returns:
        keras.Model: the updated model

    Raises:
        RuntimeError: if a candidate BatchNormalization layer has gamma values that are not strictly
            positive.
    """
    # Find pooling followed by BN layer pairs that are candidates for inversion
    map_pool_bn = find_layers_pairs(model, (MaxPool2D, GlobalAvgPool2D), BatchNormalization)

    # When there are no valid candidates, return the original model
    if not map_pool_bn:
        return model

    # Before inverting, check gamma values and update BN axis with GAP
    for pool, bn in map_pool_bn.items():
        gammas = bn.get_weights()[0]
        if isinstance(pool, MaxPool2D) and np.any(gammas <= 0):
            # It is impossible to invert MaxPool->BN with gammas <= 0
            raise RuntimeError(f"There are {np.sum(gammas <= 0)} negative gammas in the "
                               f"BatchNormalization layer {bn.name}. Negative gammas are "
                               "not supported.")
        if isinstance(pool, GlobalAvgPool2D):
            # Update BN axis when preceeded by GAP
            bn.axis = [-1]

    # Rebuild a model with pooling and BN inverted by editing the configuration
    return invert_layer_pairs(model, map_pool_bn)
