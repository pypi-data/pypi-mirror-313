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
import tensorflow as tf
import keras

from ...debugging import assert_rank_at_least
from ..fixed_point import FixedPoint
from ..qfloat import QFloat


@tf.experimental.dispatch_for_api(tf.linalg.matmul)
def fp_fp_matmul(a: FixedPoint,
                 b: FixedPoint,
                 transpose_a=False,
                 transpose_b=False,
                 adjoint_a=False,
                 adjoint_b=False,
                 a_is_sparse=False,
                 b_is_sparse=False,
                 output_type=None,
                 name=None):
    """Multiplies matrix `a` by matrix `b`, producing `a` * `b`.

    Args:
        a (:obj:`FixedPoint`): a FixedPoint of rank > 1.
        b (:obj:`FixedPoint`): a FixedPoint with same rank as `a`.
        transpose_a (bool, optional): if `True`, `a` is transposed before multiplication.
            Defaults to False.
        transpose_b (bool, optional): if `True`, `b` is transposed before multiplication.
            Defaults to False.
        adjoint_a (bool, optional): if `True`, `a` is conjugated and transposed before
            multiplication. Defaults to False.
        adjoint_b (bool, optional): if `True`, `b` is conjugated and transposed before
            multiplication. Defaults to False.
        a_is_sparse (bool, optional): must be False, argument kept for compatibility with
            original tf.matmul. Defaults to False.
        b_is_sparse (bool, optional): must be False, argument kept for compatibility with
            original tf.matmul. Defaults to False.
        output_type (NoneType, optional): must be None, argument kept for compatibility
            with original tf.matmul. Defaults to None.
        name (str, optional): the name for the operation. Defaults to None.

    Returns:
        :obj:`FixedPoint`: the multiplied FixedPoint.
    """
    if a_is_sparse:
        raise ValueError(
            f"Unsupported argument: a_is_sparse, provided {a_is_sparse}")
    if b_is_sparse:
        raise ValueError(
            f"Unsupported argument: b_is_sparse, provided {b_is_sparse}")
    if output_type is not None:
        raise ValueError(
            f"Unsupported argument: output_type, provided {output_type}")

    # We don't support matmul between vectors
    assert_rank_at_least(a.values, 2)
    assert_rank_at_least(b.values, 2)

    # Since the last dimension is collapsed by the matmul, (a,b) must be quantized per-tensor
    if not transpose_a:
        a.assert_per_tensor()
    if transpose_b:
        b.assert_per_tensor()

    # Do matmul on values
    m_values = tf.matmul(a.values, b.values, transpose_a, transpose_b, adjoint_a, adjoint_b, name)

    # Return a new FixedPoint
    return FixedPoint(m_values, a.value_bits, a.frac_bits + b.frac_bits)


@tf.experimental.dispatch_for_api(tf.linalg.matmul)
def fp_qf_matmul(a: FixedPoint,
                 b: QFloat,
                 transpose_a=False,
                 transpose_b=False,
                 adjoint_a=False,
                 adjoint_b=False,
                 a_is_sparse=False,
                 b_is_sparse=False,
                 output_type=None,
                 name=None):
    """Multiplies matrix `a` by matrix `b`, producing `a` * `b`.

    Args:
        a (:obj:`FixedPoint`): a FixedPoint of rank > 1.
        b (:obj:`QFloat`): a QFloat with same rank as `a`.
        transpose_a (bool, optional): if `True`, `a` is transposed before multiplication.
            Defaults to False.
        transpose_b (bool, optional): if `True`, `b` is transposed before multiplication.
            Defaults to False.
        adjoint_a (bool, optional): if `True`, `a` is conjugated and transposed before
            multiplication. Defaults to False.
        adjoint_b (bool, optional): if `True`, `b` is conjugated and transposed before
            multiplication. Defaults to False.
        a_is_sparse (bool, optional): must be False, argument kept for compatibility with
            original tf.matmul. Defaults to False.
        b_is_sparse (bool, optional): must be False, argument kept for compatibility with
            original tf.matmul. Defaults to False.
        output_type (NoneType, optional): must be None, argument kept for compatibility
            with original tf.matmul. Defaults to None.
        name (str, optional): the name for the operation. Defaults to None.

    Returns:
        :obj:`QFloat`: the multiplied QFloat.
    """
    # If b is transposed, its last dimension will collapse, so it must be per-tensor
    if transpose_b:
        b.assert_per_tensor()

    # Do matmul on a and b inner FixedPoint
    fp_prod = tf.matmul(a, b.fp, transpose_a, transpose_b, adjoint_a, adjoint_b, name)

    # Return a new QFloat with the same scales
    return QFloat(fp_prod, b.scales)


@tf.experimental.dispatch_for_api(tf.linalg.matmul)
def qf_qf_matmul(a: QFloat,
                 b: QFloat,
                 transpose_a=False,
                 transpose_b=False,
                 adjoint_a=False,
                 adjoint_b=False,
                 a_is_sparse=False,
                 b_is_sparse=False,
                 output_type=None,
                 name=None):
    """Multiplies matrix `a` by matrix `b`, producing `a` * `b`.

    Args:
        a (:obj:`QFloat`): a QFloat of rank > 1.
        b (:obj:`QFloat`): a QFloat with same rank as `a`.
        transpose_a (bool, optional): if `True`, `a` is transposed before multiplication.
            Defaults to False.
        transpose_b (bool, optional): if `True`, `b` is transposed before multiplication.
            Defaults to False.
        adjoint_a (bool, optional): if `True`, `a` is conjugated and transposed before
            multiplication. Defaults to False.
        adjoint_b (bool, optional): if `True`, `b` is conjugated and transposed before
            multiplication. Defaults to False.
        a_is_sparse (bool, optional): must be False, argument kept for compatibility with
            original tf.matmul. Defaults to False.
        b_is_sparse (bool, optional): must be False, argument kept for compatibility with
            original tf.matmul. Defaults to False.
        output_type (NoneType, optional): must be None, argument kept for compatibility
            with original tf.matmul. Defaults to None.
        name (str, optional): the name for the operation. Defaults to None.

    Returns:
        :obj:`QFloat`: the multiplied QFloat.
    """
    # the first input must be per-tensor to be able to multiply the scales
    a.assert_per_tensor()
    # The second input must also be per-tensor if it is transposed
    if transpose_b:
        b.assert_per_tensor()

    # Do matmul on a and b inner FixedPoint
    fp_prod = tf.matmul(a.fp, b.fp, transpose_a, transpose_b, adjoint_a, adjoint_b, name)

    # Return a new QFloat with multiplied scales
    return QFloat(fp_prod, a.scales * b.scales)


@tf.experimental.dispatch_for_api(keras.backend.depthwise_conv2d)
def fp_fp_depthwise_conv2d(x: FixedPoint,
                           depthwise_kernel: FixedPoint,
                           strides=(1, 1),
                           padding='valid',
                           data_format=None,
                           dilation_rate=(1, 1)):
    """ 2D convolution with separable filters.

    Args:
        x (obj:`FixedPoint`): input tensor.
        depthwise_kernel (:obj:`FixedPoint`): convolution kernel for the depthwise convolution.
        strides (tuple, optional): strides tuple (length 2). Defaults to (1, 1).
        padding (str, optional): `"same"` or `"valid"`. Defaults to 'valid'.
        data_format (str, optional): `"channels_last"` or `"channels_first"`. Defaults to None.
        dilation_rate (tuple, optional): tuple of integers, dilation rates for the separable
            convolution. Defaults to (1, 1).

    Returns:
        :obj:`FixedPoint`: output tensor.

    """
    # Unlike other convolutions, the depthwise does not require its inputs to
    # be quantized per-tensor as the input channels are processed independently

    # Do convolution on values
    conv_values = keras.backend.depthwise_conv2d(x.values, depthwise_kernel.values, strides,
                                                 padding, data_format, dilation_rate)

    # Evaluate the outputs fractional bits
    kernel_frac_bits = depthwise_kernel.frac_bits
    if not depthwise_kernel.per_tensor:
        # Remove the last dimension of the broadcastable depthwise filters frac bits
        kernel_frac_bits = tf.squeeze(kernel_frac_bits)
    # The output fractional bits are the sum of inputs and filters frac bits
    frac_bits = x.frac_bits + kernel_frac_bits

    # Return a new FixedPoint
    return FixedPoint(conv_values, x.value_bits, frac_bits)


@tf.experimental.dispatch_for_api(keras.backend.depthwise_conv2d)
def fp_qf_depthwise_conv2d(x: FixedPoint,
                           depthwise_kernel: QFloat,
                           strides=(1, 1),
                           padding='valid',
                           data_format=None,
                           dilation_rate=(1, 1)):
    """ 2D convolution with separable filters.

    Args:
        x (obj:`FixedPoint`): input tensor.
        depthwise_kernel (:obj:`QFloat`): convolution kernel for the depthwise convolution.
        strides (tuple, optional): strides tuple (length 2). Defaults to (1, 1).
        padding (str, optional): `"same"` or `"valid"`. Defaults to 'valid'.
        data_format (str, optional): `"channels_last"` or `"channels_first"`. Defaults to None.
        dilation_rate (tuple, optional): tuple of integers, dilation rates for the separable
            convolution. Defaults to (1, 1).

    Returns:
        :obj:`QFloat`: output tensor.

    """
    # Do convolution on x and depthwise_kernel inner FixedPoint
    fp_conv = keras.backend.depthwise_conv2d(x, depthwise_kernel.fp, strides,
                                             padding, data_format, dilation_rate)

    # Evaluate the output scales
    scales = depthwise_kernel.scales
    if not depthwise_kernel.per_tensor:
        # Remove the last dimension of the broadcastable depthwise filters scales
        scales = tf.squeeze(scales)
    # Return a new QFloat with the same scales
    return QFloat(fp_conv, scales)


@tf.experimental.dispatch_for_api(tf.nn.convolution)
def fp_fp_convolution(
        input: FixedPoint,
        filters: FixedPoint,
        strides=None, padding="VALID", data_format=None, dilations=None, name=None):
    """Perform the convolution operation between input and filter tensors.

    Args:
        input (:obj:`FixedPoint`): The input FixedPoint.
        filters (:obj:`QFloat`): The filters FixedPoint.
        strides (list, optional): Sequence of N ints >= 1. Specifies the output stride.
            Defaults to None.
        padding (str, optional): A string, either `"VALID"` or `"SAME"`. The padding algorithm.
            Defaults to "VALID"
        data_format (str, optional): Specifies whether the channel dimension of
            the `input` and output is the last dimension (default, or if `data_format`
            does not start with "NC"), or the second dimension (if `data_format`
            starts with "NC").  For N=1, the valid values are "NWC" (default) and
            "NCW".  For N=2, the valid values are "NHWC" (default) and "NCHW".
            For N=3, the valid values are "NDHWC" (default) and "NCDHW".
        dilations (list, optional): Alias for dilation_rate. Sequence of N ints >= 1.
            Specifies the filter upsampling/input downsampling rate. Defaults to None.
        name (str, optional): the name for the Tensorflow ops. Defaults to None.

    Returns:
        :obj:`FixedPoint`: a FixedPoint containing the output values.
    """
    # Input must be quantized per-tensor because the products are eventually summed
    input.assert_per_tensor()

    # Do convolution on values
    conv_values = tf.nn.convolution(input.values, filters.values, strides, padding, data_format,
                                    dilations, name)

    # Return a new FixedPoint
    return FixedPoint(conv_values, input.value_bits, input.frac_bits + filters.frac_bits)


@tf.experimental.dispatch_for_api(tf.nn.convolution)
def fp_qf_convolution(
        input: FixedPoint,
        filters: QFloat,
        strides=None, padding="VALID", data_format=None, dilations=None, name=None):
    """Perform the convolution operation between input and filter tensors.

    Args:
        input (:obj:`FixedPoint`): The input FixedPoint.
        filters (:obj:`QFloat`): The filters QFloat.
        strides (list, optional): Sequence of N ints >= 1. Specifies the output stride.
            Defaults to None.
        padding (str, optional): A string, either `"VALID"` or `"SAME"`. The padding algorithm.
            Defaults to "VALID"
        data_format (str, optional): Specifies whether the channel dimension of
            the `input` and output is the last dimension (default, or if `data_format`
            does not start with "NC"), or the second dimension (if `data_format`
            starts with "NC"). For N=1, the valid values are "NWC" (default) and
            "NCW".  For N=2, the valid values are "NHWC" (default) and "NCHW".
            For N=3, the valid values are "NDHWC" (default) and "NCDHW".
        dilations (list, optional): Alias for dilation_rate. Sequence of N ints >= 1.
            Specifies the filter upsampling/input downsampling rate. Defaults to None.
        name (str, optional): the name for the Tensorflow ops. Defaults to None.

    Returns:
        :obj:`QFloat`: a QFloat containing the output values.
    """
    # Do convolution on input and filters inner FixedPoint
    fp_conv = tf.nn.convolution(input, filters.fp, strides, padding, data_format,
                                dilations, name)

    # Return a new QFloat with the same scales
    return QFloat(fp_conv, filters.scales)


@tf.experimental.dispatch_for_api(tf.nn.convolution)
def qf_qf_convolution(
        input: QFloat,
        filters: QFloat,
        strides=None, padding="VALID", data_format=None, dilations=None, name=None):
    """Perform the convolution operation between input and filter tensors.

    Args:
        input (:obj:`QFloat`): The input QFloat.
        filters (:obj:`QFloat`): The filters QFloat.
        strides (list, optional): Sequence of N ints >= 1. Specifies the output stride.
            Defaults to None.
        padding (str, optional): A string, either `"VALID"` or `"SAME"`. The padding algorithm.
            Defaults to "VALID"
        data_format (str, optional): Specifies whether the channel dimension of
            the `input` and output is the last dimension (default, or if `data_format`
            does not start with "NC"), or the second dimension (if `data_format`
            starts with "NC"). For N=1, the valid values are "NWC" (default) and
            "NCW". For N=2, the valid values are "NHWC" (default) and "NCHW".
            For N=3, the valid values are "NDHWC" (default) and "NCDHW".
        dilations (list, optional): Alias for dilation_rate. Sequence of N ints >= 1.
            Specifies the filter upsampling/input downsampling rate. Defaults to None.
        name (str, optional): the name for the Tensorflow ops. Defaults to None.

    Returns:
        :obj:`QFloat`: a QFloat containing the output values.
    """
    # Input must be quantized per-tensor because the scales need to be multiplied
    input.assert_per_tensor()

    # Do convolution on input and filters inner FixedPoint(s)
    conv_fp = tf.nn.convolution(input.fp, filters.fp, strides, padding, data_format,
                                dilations, name)

    # Evaluate the resulting scales as the product of both scales
    conv_scales = input.scales * filters.scales
    return QFloat(conv_fp, conv_scales)


@tf.experimental.dispatch_for_api(keras.backend.conv2d_transpose)
def fp_fp_conv2d_transpose(
        x: FixedPoint,
        kernel: FixedPoint,
        output_shape, strides=(1, 1), padding='valid', data_format=None, dilation_rate=(1, 1)):
    """The transpose of conv2d.

    This operation is sometimes called "deconvolution" after (Zeiler et al., 2010), but is
    really the transpose (gradient) of atrous_conv2d rather than an actual deconvolution.

    Args:
        x (:obj:`FixedPoint`): A 4-D FixedPoint of shape [batch, height, width, in_channels] for
            NHWC data format or [batch, in_channels, height, width] for NCHW data format.
        kernel (:obj:`FixedPoint`): A FixedPoint with a [height, width, out_channels, in_channels]
            shape. Kernel's in_channels dimension must match that of input.
        output_shape (tf.Tensor): A 1-D Tensor representing the output shape of the
            deconvolution op.
        strides (list, optional): Sequence of 2 ints >= 1. Specifies the output stride.
            Defaults to (1, 1).
        padding (str, optional): A string, either `'valid'` or `'same'`. The padding algorithm.
            Defaults to 'valid'
        data_format (str, optional): Specifies whether the channel dimension of
            the `input` and output is the last dimension (default, or if `data_format`
            does not start with "NC"), or the second dimension (if `data_format`
            starts with "NC"). For N=1, the valid values are "NWC" (default) and
            "NCW". For N=2, the valid values are "NHWC" (default) and "NCHW".
            For N=3, the valid values are "NDHWC" (default) and "NCDHW".
        dilation_rate (list, optional): Sequence of 2 ints >= 1.
            Specifies the filter upsampling/input downsampling rate. Defaults to (1, 1).

    Returns:
        :obj:`FixedPoint`: a FixedPoint containing the output values.
    """
    # Input must be quantized per-tensor because the products are eventually summed
    x.assert_per_tensor()

    # Transpose filter values so that they have the shape expected by the tensorflow op:
    #  (h, w, filters, channels)
    filter_values = tf.transpose(kernel.values, (0, 1, 3, 2))

    # Do conv2d_transpose on values
    conv_values = keras.backend.conv2d_transpose(x.values, filter_values, output_shape, strides,
                                                 padding, data_format, dilation_rate)

    # Return a new FixedPoint
    return FixedPoint(conv_values, x.value_bits, x.frac_bits + kernel.frac_bits)


@tf.experimental.dispatch_for_api(keras.backend.conv2d_transpose)
def fp_qf_conv2d_transpose(
        x: FixedPoint,
        kernel: QFloat,
        output_shape, strides=(1, 1), padding='valid', data_format=None, dilation_rate=(1, 1)):
    """The transpose of conv2d.

    This operation is sometimes called "deconvolution" after (Zeiler et al., 2010), but is
    really the transpose (gradient) of atrous_conv2d rather than an actual deconvolution.

    Args:
        x (:obj:`FixedPoint`): A 4-D FixedPoint of shape [batch, height, width, in_channels] for
            NHWC data format or [batch, in_channels, height, width] for NCHW data format.
        kernel (:obj:`QFloat`): A QFloat of shape [height, width, out_channels, in_channels]
            shape. Kernel's in_channels dimension must match that of input.
        output_shape (tf.Tensor): A 1-D Tensor representing the output shape of the
            deconvolution op.
        strides (list, optional): Sequence of 2 ints >= 1. Specifies the output stride.
            Defaults to (1, 1).
        padding (str, optional): A string, either `'valid'` or `'same'`. The padding algorithm.
            Defaults to 'valid'
        data_format (str, optional): Specifies whether the channel dimension of
            the `input` and output is the last dimension (default, or if `data_format`
            does not start with "NC"), or the second dimension (if `data_format`
            starts with "NC"). For N=1, the valid values are "NWC" (default) and
            "NCW". For N=2, the valid values are "NHWC" (default) and "NCHW".
            For N=3, the valid values are "NDHWC" (default) and "NCDHW".
        dilation_rate (list, optional): Sequence of 2 ints >= 1.
            Specifies the filter upsampling/input downsampling rate. Defaults to (1, 1).

    Returns:
        :obj:`QFloat`: a QFloat containing the output values.
    """
    # Input must be quantized per-tensor because the products are eventually summed
    x.assert_per_tensor()

    # Do conv2d_transpose on inputs and filter inner FixedPoint
    conv_values = keras.backend.conv2d_transpose(x, kernel.fp, output_shape, strides,
                                                 padding, data_format, dilation_rate)

    # Return a new QFloat
    return QFloat(conv_values, kernel.scales)


@tf.experimental.dispatch_for_api(tf.nn.max_pool)
def fp_max_pool2d(
        input: FixedPoint,
        ksize, strides, padding, data_format=None, name=None):
    """Perform the max pooling operation

    Downsamples the input along its spatial dimensions by taking the maximum value over an input
    window for each channel of the input. The window is shifted by strides along each dimension.

    Args:
        input (:obj:`FixedPoint`): A 4-D FixedPoint of shape [batch, height, width, in_channels] for
            NHWC data format or [batch, in_channels, height, width] for NCHW data format.
        ksize (list): An int or list of ints that has length 1, N or N+2. The size of the window
            for each dimension of the input tensor.
        strides (list): Sequence of N ints >= 1. Specifies the output stride.
        padding (str, optional): A string, either `"VALID"` or `"SAME"`. The padding algorithm.
            Defaults to "VALID"
        data_format (str, optional): Specifies the channel dimension. For N=1 it can be
            either "NWC" (default) or "NCW", for N=2 it can be either "NHWC" (default) or "NCHW" and
            for N=3 either "NDHWC" (default) or "NCDHW".
        name (str, optional): the name for the Tensorflow ops. Defaults to None.

    Returns:
        :obj:`FixedPoint`: a FixedPoint containing the output values.
    """
    # Do max_pool on values
    max_pool_values = tf.nn.max_pool(input.values, ksize, strides, padding, data_format, name)

    # Return a new FixedPoint
    return FixedPoint(max_pool_values, input.value_bits, input.frac_bits)


@tf.experimental.dispatch_for_api(tf.nn.max_pool)
def qf_max_pool2d(
        input: QFloat,
        ksize, strides, padding, data_format=None, name=None):
    """Perform the max pooling operation

    Downsamples the input along its spatial dimensions by taking the maximum value over an input
    window for each channel of the input. The window is shifted by strides along each dimension.

    Args:
        input (:obj:`QFloat`): A 4-D QFloat of shape [batch, height, width, in_channels] for
            NHWC data format or [batch, in_channels, height, width] for NCHW data format.
        ksize (int, list): An int or list of ints that has length 1, N or N+2. The size of the
            window for each dimension of the input tensor.
        strides (list): Sequence of N ints >= 1. Specifies the output stride.
        padding (str, optional): A string, either `"VALID"` or `"SAME"`. The padding algorithm.
            Defaults to "VALID"
        data_format (str, optional): Specifies the channel dimension. For N=1 it can be
            either "NWC" (default) or "NCW", for N=2 it can be either "NHWC" (default) or "NCHW" and
            for N=3 either "NDHWC" (default) or "NCDHW".
        name (str, optional): the name for the Tensorflow ops. Defaults to None.

    Returns:
        :obj:`QFloat`: a QFloat containing the output values.
    """
    # Do max_pool on inputs inner FixedPoint
    max_pool_fp = tf.nn.max_pool(input.fp, ksize, strides, padding, data_format, name)

    # Return a new QFloat
    return QFloat(max_pool_fp, input.scales)
