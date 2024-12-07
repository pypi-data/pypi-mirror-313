#!/usr/bin/env python
# ******************************************************************************
# Copyright 2022 Brainchip Holdings Ltd.
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
Common utility methods used in quantization models.
"""

__all__ = ['apply_weights_to_model']

import warnings


def apply_weights_to_model(model, weights, verbose=True):
    """Loads weights from a dictionary and apply it to a model.

    Go through the dictionary of weights, find the corresponding variable in the
    model and partially load its weights.

    Args:
        model (keras.Model): the model to update
        weights (dict): the dictionary of weights
        verbose (bool, optional): if True, throw warning messages if a dict item is not found in the
            model. Defaults to True.
    """
    if len(weights) == 0:
        warnings.warn("There is no weight to apply to the model.")
        return

    # Go through the dictionary of weights with each item
    for key, value in weights.items():
        value_applied = False
        for dest_var in model.variables:
            if key == dest_var.name:
                # Apply the current item value
                dest_var.assign(value)
                value_applied = True
                break
        if not value_applied and verbose:
            warnings.warn(f"Variable '{key}' not found in the model.")
