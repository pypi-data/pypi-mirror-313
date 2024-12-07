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
__all__ = ["compute_conv_output", "compute_onnx_conv_output"]

from .base_layer import OnnxLayer
from ..graph_tools import get_field


def compute_conv_output(in_shape, kernel_shape, strides, pads=None):
    """Compute the output shape after applying a convolution for each spatial dimension

    Args:
        in_shape (tuple of ints): the input shape.
        kernel_shape (tuple of ints): the convolutional kernel shape.
        strides (tuple of ints): the convolutional strides.
        pads (tuple of ints): the pads to apply. Defaults to None.

    Returns:
        tuple of ints: the output shape after applying the convolution.
    """
    N = len(in_shape)
    assert N == len(strides) == len(kernel_shape)
    if pads is None:
        pads = [0] * N * 2
    assert len(in_shape) == len(pads) / 2

    out_shape = []
    for x, kx, sx, pl, pr in zip(in_shape, kernel_shape, strides, pads[:N], pads[N:]):
        y = (x + pl + pr - kx) // sx + 1
        out_shape.append(y)
    return tuple(out_shape)


def compute_onnx_conv_output(qlayer, input_shape, apply_pool=True, transpose=False):
    """Compute the output shape produced by qlayer for a given input shape.

    Args:
        qlayer (OnnxLayer): the layer with the parameters.
        input_shape (tuple of ints): the input shape.
        apply_pool (bool, optional): whether output shape has to include pool operation.
            Defaults to True.
        transpose (bool, optional): whether the input performs the transpose of the
            convolution. Defaults to False.

    Returns:
        tuple of ints: the output shape after applying the convolution.
    """
    isinstance(qlayer, OnnxLayer)
    kernel = qlayer.weights["kernel"]

    # Compute conv output shape
    spatial_dims = kernel.ndim - 2
    conv_strides = get_field(qlayer, "strides", (1,) * spatial_dims)

    if transpose:
        # Extract padding values
        conv_transpose_pads = get_field(qlayer, "pads")
        # Because of weight ordering (CFHW), the operation is different for transpose convolutions.
        output_shape = compute_transpose_conv_output(
            input_shape[2:], kernel.shape[2:], conv_strides, conv_transpose_pads)
        groups = get_field(qlayer, "groups", 1)
        n_filters = (kernel.shape[1] * groups,)
        return input_shape[:1] + n_filters + output_shape
    else:
        conv_pads = qlayer.weights["pads"].tolist()
        if any(conv_pads[:2]) or any(conv_pads[kernel.ndim:kernel.ndim + 2]):
            raise ValueError(f"Unsupported pads format in {qlayer.name}: no pad can be applied "
                             f"in batch or spatial dimension. Receives: {conv_pads}")
        conv_pads = conv_pads[2:kernel.ndim] + conv_pads[kernel.ndim + 2:]
        output_shape = compute_conv_output(
            input_shape[2:], kernel.shape[2:], conv_strides, conv_pads)

    # Compute max pool output shape
    if apply_pool:
        if "MaxPool" in qlayer.op_type:
            pool_size = get_field(qlayer, "pool_size", (2,) * spatial_dims)
            pool_strides = get_field(qlayer, "pool_strides", (1,) * spatial_dims)
            pool_pads = get_field(qlayer, "pool_pads", (0, 0) * spatial_dims)
            output_shape = compute_conv_output(output_shape, pool_size, pool_strides, pool_pads)
        elif "GlobalAvgPool" in qlayer.op_type:
            output_shape = (1,) * spatial_dims
    return input_shape[:1] + kernel.shape[:1] + output_shape


def compute_transpose_conv_output(in_shape, kernel_shape, strides, pads=None):
    """Compute the output shape after applying a transpose convolution
    on each spatial dimension

    Args:
        in_shape (tuple of ints): the input shape.
        kernel_shape (tuple of ints): the convolutional kernel shape.
        strides (tuple of ints): the convolutional strides.
        pads (tuple of ints, optional): the pads to apply. Defaults to None.

    Returns:
        tuple of ints: the output shape after applying the transpose convolution.
    """
    N = len(in_shape)
    assert N == len(strides) == len(kernel_shape)
    if pads is None:
        pads = [0] * N * 2

    assert N == len(pads) / 2

    out_shape = []
    for x, kx, sx, p_begin, p_end in zip(in_shape, kernel_shape, strides, pads[:N], pads[N:]):
        # From ONNX documentation https://onnx.ai/onnx/operators/onnx__ConvTranspose.html#summary
        # (ignoring dilation and output padding)
        # dim_out = stride[i] * (dim_in - 1) + kernel_shape[i] - pads[start_i] - pads[end_i]
        y = sx * (x - 1) + kx - p_begin - p_end
        out_shape.append(y)
    return tuple(out_shape)
