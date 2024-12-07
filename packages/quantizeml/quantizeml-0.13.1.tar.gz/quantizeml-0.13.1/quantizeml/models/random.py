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

__all__ = ["generate_keras_random_samples"]


import tensorflow as tf

from ..random import generate_np_random_samples
from ..layers import get_quantization_params


def generate_keras_random_samples(model, batch_size=1, seed=None):
    """Generate a random set of inputs for a model.

    Args:
        model (tf.keras.Model): the target model to generate inputs.
        batch_size (int, optional): a batch size. Defaults to 1.
        seed (int, optional): a random seed (reproducibility purpose). Defaults to None.

    Returns:
        np.ndarray: a set of samples
    """
    input_specs_list = model.input if isinstance(model.input, (list, tuple)) else [model.input]
    gen_inputs = []
    for idx, keras_spec in enumerate(input_specs_list):
        if seed is not None:
            seed = seed + idx
        input_shape = (batch_size, *keras_spec.shape[1:])
        input_dtype = keras_spec.dtype
        if not input_dtype.is_integer:
            input_dtype = tf.as_dtype(get_quantization_params().input_dtype)

        xq = generate_np_random_samples(input_shape, input_dtype.as_numpy_dtype, seed=seed)
        gen_inputs.append(xq)

    if not isinstance(model.input, (list, tuple)):
        return gen_inputs[0]
    return gen_inputs
