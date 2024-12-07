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
Helper that prepares a model for quantization.
"""

__all__ = ['sanitize']

from . import (align_rescaling, invert_batchnorm_pooling, fold_batchnorms, remove_zeropadding2d,
               invert_relu_maxpool, replace_lambda, convert_conv_to_dw_conv, remove_reshape,
               fold_activations_in_add, split_layers_with_relu, split_concat_layers,
               convert_even_to_odd_kernel)


def sanitize(model):
    """ Sanitize a model preparing it for quantization.

    This is a wrapping successive calls to several model transformations which aims at making the
    model quantization ready.

    Args:
        model (keras.Model): the input model

    Returns:
        keras.Model: the sanitized model
    """

    # Replace lambda layers
    model = replace_lambda(model)

    # Splits layers with 'relu' activation into two separate layers
    # one without activation and one with a separate 'relu' activation layer.
    model = split_layers_with_relu(model)

    # Replace Conv2D layers that behave as DepthwiseConv2D to the latest.
    model = convert_conv_to_dw_conv(model)

    # Multiple Reshape/Flatten removal transformation
    model = remove_reshape(model)

    # Align Rescaling (if needed)
    model = align_rescaling(model)

    # Invert ReLU <-> MaxPool layers so that MaxPool comes first
    model = invert_relu_maxpool(model)

    # Invert BN <-> Pooling layers and fold BN into their preceding layers
    model = invert_batchnorm_pooling(model)
    model = fold_batchnorms(model)

    # Fold ReLUs with no max_value that comes after an Add layer
    model = fold_activations_in_add(model)

    # Remove unsupported ZeroPadding2D layers and replace them with 'same' padding convolution when
    # possible
    model = remove_zeropadding2d(model)

    # Split Concatenate layers with more than two inputs into multiple Concatenate layers
    # with exactly two inputs when possible
    model = split_concat_layers(model)

    # Convert even kernels to odd for Conv2D et DepthwiseConv2D when possible
    model = convert_even_to_odd_kernel(model)
    return model
