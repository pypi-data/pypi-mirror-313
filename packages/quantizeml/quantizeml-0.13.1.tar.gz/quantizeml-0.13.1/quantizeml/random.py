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
__all__ = ["generate_np_random_samples"]


import numpy as np


def generate_np_random_samples(size, dtype, min_value=None, max_value=None, seed=None):
    """Generate random numpy array samples.

    Args:
        size (tuple): Size of the samples.
        dtype (str or np.dtype): The desired data type of the output array
        min_value (int or float, optional): The minimum value of the generated samples.
            If set to None (default), it is interpreted as:
                - The smallest representable value for integer types.
                - 0.0 for floating-point types.
        max_value (int or float, optional): The maximum value of the generated samples.
            If set to None (default), it is interpreted as:
                - Maximum representable value for integer types.
                - 1.0 for floating-point types.
        seed (int, optional): a random seed (reproducibility purpose). Defaults to None.

    Returns:
        np.ndarray: random samples
    """
    rng = np.random.default_rng(seed=seed)
    dtype = np.dtype(dtype)

    if None in size:
        raise ValueError(f"Each dimension in size must be defined "
                         f"(None value found in dimension {size.index(None)}).")

    if np.issubdtype(dtype, np.integer):
        iinfo = np.iinfo(dtype)
        min_value = iinfo.min if min_value is None else min_value
        max_value = iinfo.max if max_value is None else max_value
        x = rng.integers(min_value, max_value, size, endpoint=True)
    else:
        min_value = 0.0 if min_value is None else min_value
        max_value = 1.0 if max_value is None else max_value
        x = rng.uniform(min_value, max_value, size)
    return x.astype(dtype)
