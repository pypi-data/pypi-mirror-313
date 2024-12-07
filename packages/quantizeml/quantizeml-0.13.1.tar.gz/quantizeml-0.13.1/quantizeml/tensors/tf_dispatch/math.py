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

from ...debugging import assert_equal
from ..fixed_point import FixedPoint
from ..qfloat import QFloat


@tf.experimental.dispatch_for_api(tf.add)
def fp_add(x: FixedPoint, y: FixedPoint):
    return x + y


@tf.experimental.dispatch_for_api(tf.add)
def qf_add(x: QFloat, y: QFloat):
    return x + y


@tf.experimental.dispatch_for_api(tf.clip_by_value)
def fp_clip_by_value(t: FixedPoint,
                     clip_value_min: FixedPoint,
                     clip_value_max: FixedPoint,
                     name=None):
    """Clips tensor values to a specified min and max.

    Args:
        t (:obj:`FixedPoint`): the FixedPoint to be clipped.
        clip_value_min (:obj:`FixedPoint`): the minimum value.
        clip_value_max (:obj:`FixedPoint`): the maximum value.
        name (str, optional): the name for the Tensorflow ops. Defaults to None.

    Returns:
        :obj:`FixedPoint`: the clipped FixedPoint.
    """
    # The fractional bits of all inputs must be equal
    assert_equal(t.frac_bits, clip_value_min.frac_bits)
    assert_equal(t.frac_bits, clip_value_max.frac_bits)
    clip_values = tf.clip_by_value(t.values, clip_value_min.values, clip_value_max.values, name)
    return FixedPoint(clip_values, t.value_bits, t.frac_bits)


@tf.experimental.dispatch_for_api(tf.clip_by_value)
def qf_clip_by_value(t: QFloat,
                     clip_value_min: QFloat,
                     clip_value_max: QFloat,
                     name=None):
    """Clips tensor values to a specified min and max.

    Args:
        t (:obj:`QFloat`): the QFloat to be clipped.
        clip_value_min (:obj:`QFloat`): the minimum value.
        clip_value_max (:obj:`QFloat`): the maximum value.
        name (str, optional): the name for the Tensorflow ops. Defaults to None.

    Returns:
        :obj:`QFloat`: the clipped QFloat.
    """
    # The scales of all inputs must be equal
    assert_equal(t.scales, clip_value_min.scales)
    assert_equal(t.scales, clip_value_max.scales)
    clip_fp = tf.clip_by_value(t.fp, clip_value_min.fp, clip_value_max.fp, name)
    return QFloat(clip_fp, t.scales)


@tf.experimental.dispatch_for_api(tf.math.maximum)
def fp_maximum(x: FixedPoint, y: FixedPoint, name=None):
    """Returns the max of x and y element-wise.

    Args:
        x (:obj:`FixedPoint`): the first FixedPoint.
        y (:obj:`FixedPoint`): the second FixedPoint.
        name (str, optional): the name for the Tensorflow ops. Defaults to None.

    Returns:
        :obj:`FixedPoint`: the resulting FixedPoint.
    """
    # The inputs frac_bits must be equal
    assert_equal(x.frac_bits, y.frac_bits)
    # Choose the highest of both value bits
    value_bits = max(x.value_bits, y.value_bits)
    return FixedPoint(tf.math.maximum(x.values, y.values, name), value_bits, x.frac_bits)


@tf.experimental.dispatch_for_api(tf.math.maximum)
def qf_maximum(x: QFloat, y: QFloat, name=None):
    """Returns the max of x and y element-wise.

    Args:
        x (:obj:`QFloat`): the first QFloat.
        y (:obj:`QFloat`): the second QFloat.
        name (str, optional): the name for the Tensorflow ops. Defaults to None.

    Returns:
        :obj:`QFloat`: the resulting QFloat.
    """
    # The inputs scales must be equal
    assert_equal(x.scales, y.scales)
    max_fp = tf.math.maximum(x.fp, y.fp, name)
    return QFloat(max_fp, x.scales)


def _check_last_dim_reduced(input_tensor, axis):
    last_dim = input_tensor.shape.ndims - 1
    last_dim_reduced = axis is None or axis == -1 or axis == last_dim
    if isinstance(axis, (list, tuple)):
        last_dim_reduced = last_dim_reduced or last_dim in axis
    if last_dim_reduced:
        # The last dimension will be collapsed: inputs must be quantized per-tensor
        input_tensor.assert_per_tensor()


@tf.experimental.dispatch_for_api(tf.math.reduce_sum)
def fp_reduce_sum(input_tensor: FixedPoint, axis=None, keepdims=False, name=None):
    """Computes the sum of elements across dimensions of a FixedPoint.

    Args:
        input_tensor (:obj:`FixedPoint`): the FixedPoint to be summed.
        axis (list, optional): the dimensions to reduce. If None, reduces all
            dimensions. Defaults to None.
        keepdims (bool, optional): if true, retains reduced dimensions with length 1.
            Defaults to False.
        name (str, optional): the name for the Tensorflow ops. Defaults to None.

    Returns:
        :obj:`FixedPoint`: the summed FixedPoint.
    """
    _check_last_dim_reduced(input_tensor, axis)

    # Reduce sum
    s_values = tf.math.reduce_sum(
        input_tensor.values, axis, keepdims=keepdims, name=name)

    # Return a new FixedPoint
    return FixedPoint(s_values, input_tensor.value_bits, input_tensor.frac_bits)


@tf.experimental.dispatch_for_api(tf.math.reduce_sum)
def qf_reduce_sum(input_tensor: QFloat, axis=None, keepdims=False, name=None):
    """Computes the sum of elements across dimensions of a QFloat.

    Args:
        input_tensor (:obj:`QFloat`): the QFloat to be summed.
        axis (list, optional): the dimensions to reduce. If None, reduces all
            dimensions. Defaults to None.
        keepdims (bool, optional): if true, retains reduced dimensions with length 1.
            Defaults to False.
        name (str, optional): the name for the Tensorflow ops. Defaults to None.

    Returns:
        :obj:`QFloat`: the summed QFloat.
    """
    _check_last_dim_reduced(input_tensor, axis)

    # Reduce sum
    s_fp = tf.math.reduce_sum(input_tensor.fp, axis, keepdims=keepdims, name=name)

    # Return a new QFloat with the same scales
    return QFloat(s_fp, input_tensor.scales)


@tf.experimental.dispatch_for_api(tf.math.reduce_max)
def fp_reduce_max(input_tensor: FixedPoint,
                  axis=None,
                  keepdims=False,
                  name=None):
    """Computes the maximum of elements across dimensions of a FixedPoint.

    Args:
        input_tensor (:obj:`FixedPoint`): the FixedPoint to be estimated.
        axis (list, optional): the dimensions to reduce. If None, reduces all
            dimensions. Defaults to None.
        keepdims (bool, optional): if true, retains reduced dimensions with length 1.
            Defaults to False.
        name (str, optional): the name for the Tensorflow ops. Defaults to None.

    Returns:
        :obj:`FixedPoint`: the maximum FixedPoint.
    """
    # We only support reduce_max if the input is per-tensor
    input_tensor.assert_per_tensor()

    # Reduce max
    s_values = tf.math.reduce_max(input_tensor.values,
                                  axis,
                                  keepdims=keepdims,
                                  name=name)
    # Return a new FixedPoint
    return FixedPoint(s_values, input_tensor.value_bits, input_tensor.frac_bits)


@tf.experimental.dispatch_for_api(tf.math.multiply)
def fp_fp_multiply(x: FixedPoint, y: FixedPoint, name=None):
    """Returns an element-wise x * y.

    Args:
        x (:obj:`FixedPoint`): a FixedPoint
        y (:obj:`FixedPoint`): a FixedPoint
        name (str, optional): A name for the operation

    Returns:
        :obj:`FixedPoint`: an object with the same shape as x
    """
    values = tf.math.multiply(x.values, y.values, name)
    return FixedPoint(values, x.value_bits, x.frac_bits + y.frac_bits)


@tf.experimental.dispatch_for_api(tf.math.multiply)
def fp_qf_multiply(x: FixedPoint, y: QFloat, name=None):
    """Returns an element-wise x * y.

    Args:
        x (:obj:`FixedPoint`): a FixedPoint
        y (:obj:`QFloat`): a QFloat
        name (str, optional): A name for the operation

    Returns:
        :obj:`QFloat`: an object with the same shape as x
    """
    # Multiply x by y inner FixedPoint
    # To produce a per-tensor FixedPoint, x must be per-tensor
    x.assert_per_tensor()
    mul = tf.math.multiply(x, y.fp, name)
    # Return a new QFloat with y scales
    return QFloat(mul, y.scales)


@tf.experimental.dispatch_for_api(tf.math.multiply)
def qf_qf_multiply(x: QFloat, y: QFloat, name=None):
    """Returns an element-wise x * y.

    Args:
        x (:obj:`QFloat`): a QFloat
        y (:obj:`QFloat`): a QFloat
        name (str, optional): A name for the operation

    Returns:
        :obj:`QFloat`: an object with the same shape as x
    """
    # To produce a per-tensor FixedPoint, x must be per-tensor
    x.assert_per_tensor()
    # Multiply x and y inner FixedPoints
    mul = tf.math.multiply(x.fp, y.fp, name)
    # Evaluate the resulting scales as the product of both scales
    scales = x.scales * y.scales
    # Return a new QFloat
    return QFloat(mul, scales)


@tf.experimental.dispatch_for_api(tf.math.divide)
def fp_fp_divide(x: FixedPoint, y: FixedPoint, name=None):
    """Computes Python style division of `x` by `y`.

    Args:
        x (:obj:`FixedPoint`): the FixedPoint to divide
        y (:obj:`FixedPoint`): the FixedPoint divisor
        name (str, optional): A name for the operation

    Returns:
        :obj:`FixedPoint`: an object with the same shape as x
    """
    return x / y


@tf.experimental.dispatch_for_api(tf.math.divide)
def qf_fp_divide(x: QFloat, y: FixedPoint, name=None):
    """Computes Python style division of `x` by `y`.

    Args:
        x (:obj:`QFloat`): the QFloat to divide
        y (:obj:`FixedPoint`): the FixedPoint divisor
        name (str, optional): A name for the operation

    Returns:
        :obj:`QFloat`: an object with the same shape as x
    """
    # Divide x inner FixedPoint by y
    # To produce a per-tensor FixedPoint, y must be per-tensor
    y.assert_per_tensor()
    div = tf.math.divide(x.fp, y, name)
    # Return a new QFloat with x scales
    return QFloat(div, x.scales)
