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
import numpy as np

# Akida weights range is [-127, 127], int8
AKIDA_W_MAX = 127.0


def quantize_vector(x, scale, bitwidth=8, signed=True):
    # Decrease bitwidth when signed
    if signed:
        bitwidth -= 1
    # Project input
    proj_x = x * scale
    # Inputs needs to be quantized to bitwidth-bit
    epsilon = 2**-8
    x_int_bits = np.ceil(np.log2(np.abs(proj_x + epsilon)))
    qx_shift = np.maximum(0, x_int_bits - bitwidth).astype(np.int32)
    qx_8 = np.round(proj_x / (2 ** qx_shift)).astype(np.int32)
    # Rebuild quantized inputs
    return qx_8 << qx_shift


def quantize_weights(kernel):
    # Absolute max value calculated on first dim
    q_axis = tuple(range(1, kernel.ndim))
    abs_max = np.abs(kernel).max(q_axis)
    # Clip absolute max value
    abs_max = np.maximum(abs_max, 2.**-16)
    # Calculate float scale
    scale = AKIDA_W_MAX / abs_max
    # Project weights and bias to quantized int8 domain, but keeping them in float
    proj_kernel = kernel * align_to(scale, kernel.ndim, axis=0)
    # Now kernel can be finally be quantized to int8
    qkernel = np.round(proj_kernel)
    qkernel = np.clip(qkernel, -128, 127)
    qkernel = qkernel.astype(np.int8)
    return qkernel, scale


def fold_zero_point(bias, kernel, zero_point):
    # Fold zero point into bias.
    # To reduce quantization error, kernel should be quantized / dequantized previously.
    # Note this is possible if we project each zero point through
    # its respective axis in the weights (with FCXY format)
    zero_point = align_to(zero_point, kernel.ndim)
    q_axis = tuple(range(1, kernel.ndim))
    bias = bias - (zero_point.astype("float32") * kernel).sum(axis=q_axis)
    return bias


def align_to(x, ndims, axis=1):
    # Reshape x in order to have ndims, moving the information to a decided axis
    align_shape = [1 if axis != i else -1 for i in range(ndims)]
    return np.reshape(x, align_shape)
