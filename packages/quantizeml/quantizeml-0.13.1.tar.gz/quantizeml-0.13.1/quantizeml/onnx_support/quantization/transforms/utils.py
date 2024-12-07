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
__all__ = ["compute_conv_same_pads"]


def compute_conv_same_pads(input_shape, kernel_shape, strides):
    """Compute pads values for convolutional nodes.

    Args:
        input_shape (tuple of ints): the input shape (Height, Width).
        kernel_shape (tuple of ints): the convolutional kernel shape.
        strides (tuple of ints): the convolutional strides.

    Returns:
        list of ints: the pads to apply.
    """
    x, y = input_shape
    filter_x, filter_y = kernel_shape
    stride_x, stride_y = strides

    if x % stride_x == 0:
        pad_along_x = max(filter_x - stride_x, 0)
    else:
        pad_along_x = max(filter_x - (x % stride_x), 0)
    if y % stride_y == 0:
        pad_along_y = max(filter_y - stride_y, 0)
    else:
        pad_along_y = max(filter_y - (y % stride_y), 0)
    pad_y1 = pad_along_y // 2
    pad_y2 = pad_along_y - pad_y1
    pad_x1 = pad_along_x // 2
    pad_x2 = pad_along_x - pad_x1
    return [pad_x1, pad_y1, pad_x2, pad_y2]
