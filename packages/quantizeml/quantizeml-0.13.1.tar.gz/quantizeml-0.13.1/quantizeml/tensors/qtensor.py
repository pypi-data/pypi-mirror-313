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
from copy import copy
import tensorflow as tf


from ..debugging import assert_equal


@tf.custom_gradient
def round_through(x):
    rounded = tf.math.round(x)

    def grad(upstream):
        return upstream
    return rounded, grad


@tf.custom_gradient
def floor_through(x):
    floored = tf.math.floor(x)

    def grad(upstream):
        return upstream
    return floored, grad


@tf.custom_gradient
def ceil_through(x):
    ceiled = tf.math.ceil(x)

    def grad(upstream):
        return upstream
    return ceiled, grad


@tf.custom_gradient
def saturate(x, n):
    """Saturate x values on [-2^n, 2^n - 1]

    This function is a wrapper around tf.clip_by_values that exhibits a
    simplified gradient for a better efficiency.
    Unlike tf.clip_by_value, the gradient outside the clipping range is not zero.

    Args:
        x (tf.Tensor): a tensor of float values representing integer.
        n (tf.Tensor): the target bitwidth.

    Returns:
        the resulting clipped tensor and its gradient function.

    """
    # Clamp values to [-2^n, 2^n - 1]
    int_max = tf.math.pow(2.0, n)
    saturated = tf.clip_by_value(x, -int_max, int_max - 1, name="saturate")

    def grad(upstream):
        # The gradient of x is 1 everywhere
        dx = upstream
        # The gradient of n is zero (constant)
        dn = tf.zeros_like(n)
        return dx, dn

    return saturated, grad


class QTensor(tf.experimental.ExtensionType):
    """Abstract class to exchange quantized tensors between layers
    """
    shape: tf.TensorShape  # Required to convert to a KerasTensor

    @property
    def name(self):
        """Returns the QTensor name

        Returns:
            str: the QTensor name
        """
        raise NotImplementedError

    @property
    def per_tensor(self):
        """Returns if QTensor is quantized per-tensor

        Returns:
            bool: True if QTensor is quantized per-tensor or False on per-axis case.
        """
        raise NotImplementedError

    def to_float(self):
        """Returns a float representation of the QTensor

        Returns:
            tf.Tensor: the float representation.
        """
        raise NotImplementedError

    def __getitem__(self):
        """Retrieve a slice or element from the QTensor

        Returns:
            :obj:`QTensor`: the sliced QTensor
        """
        raise NotImplementedError

    def clone(self):
        """Returns a copy of the QTensor

        Returns:
            :obj:`QTensor`: the copy.
        """
        return copy(self)

    def __str__(self):
        class_name = self.__class__.__name__
        x_float = self.to_float()
        return f"{class_name}: {x_float}"

    @staticmethod
    def int_max(value_bits):
        return 2 ** value_bits - 1

    def assert_per_tensor(self):
        """Asserts that a QTensor is quantized per-tensor"""
        assert_equal(self.per_tensor, True, message=f"{self.name} is not per-tensor.")


def pow2(n):
    """Return the power of two of an integer

    Args:
        n (`tf.tensor`, int): the positive or negative exponent

    Returns:
        tf.Tensor: a float tensor containing the PoT of the input.
    """
    return tf.pow(2.0, tf.cast(n, tf.float32))


def ceil_log2(x):
    """Return the closest power of two exponent of a float tensor.

    This evaluates for each element of the input tensor the integer exponent leading
    to the closest power-of-two higher than the input.

    In hardware, if the inputs are represented as integer, this operation can
    be implemented by identifying the leading bit index and increment the result
    by 1.

    Example: ceil_log2(7) = ceil_log2(0b00000111) = 2 + 1 = 3

    Args:
        x (tf.Tensor): the source tensor

    Returns:
        tf.Tensor: a float tensor containing integer values
            representing the closest PoT exponents.
    """
    return ceil_through(tf.experimental.numpy.log2(tf.cast(x, tf.float32)))


def floor_log2(x):
    """Return the closest power of two exponent of a float tensor.

    This evaluates for each element of the input tensor the integer exponent leading
    to the closest power-of-two lower than the input (except if x < 1).

    In hardware, if the inputs are represented as integer, this operation can
    be implemented by identifying the leading bit index.

    Example: floor_log2(7) = floor_pow2(0b00000111) = 2

    Args:
        x (tf.Tensor): the source tensor

    Returns:
        tf.Tensor: a float tensor containing integer values
            representing the closest PoT exponents.
    """
    return floor_through(tf.experimental.numpy.log2(tf.cast(x, tf.float32)))


def round_log2(x):
    """Return the closest power of two exponent of a float tensor.

    This evaluates for each element of the input tensor the integer exponent leading
    to the closest power-of-two.

    In hardware, if the inputs are represented as integer, this operation can
    be implemented by:
    - identifying the leading bit index,
    - increment by 1 if the previous bit is 1 also.

    Example: round_log2(7) = round_log2(0b00000111) = 2 + 1 = 3
             round_log2(5) = round_log2(0b00000101) = 2

    Args:
        x (tf.Tensor): the source tensor

    Returns:
        tf.Tensor: a float tensor containing integer values
            representing the closest PoT exponents.
    """
    return round_through(tf.experimental.numpy.log2(tf.cast(x, tf.float32)))


def convert_ellipsis_into_slices(values_rank, idx):
    """
    Converts an Ellipsis (`...`) if found in the indexing tuple into a series of slice objects
    that cover the remaining dimensions of the tensor.

    Args:
        values_rank (int): The rank (number of dimensions) of the tensor being indexed.
        idx (tuple): The indexing tuple that may contain an Ellipsis.

    Returns:
        tuple: A new indexing tuple with the Ellipsis replaced by appropriate slices.
    """
    new_idx = ()
    for element in idx:
        if element == ...:
            for _ in range(values_rank - len(idx) + 1):
                new_idx += (slice(None, None, None),)
        else:
            new_idx += (element,)
    return new_idx


def slice_tensor_by_index(idx, values_rank, tensor):
    """
    Slices the frac_bits or scales tensor when slicing a QTensor.

    Args:
        idx (tuple/slice/int/Ellipsis): The indexing tuple.
        values_rank (int): The rank (number of dimensions) of the values tensor.
        tensor (tf.Tensor): The frac_bits/scale tensor to slice.

    Returns:
        tf.Tensor: the sliced frac_bits/scale tensor tensor.
    """
    assert_equal(tf.rank(tensor), 1)
    if isinstance(idx, tuple):
        # Convert Ellipsis into actual slices
        if any(x is Ellipsis for x in idx):
            idx = convert_ellipsis_into_slices(values_rank, idx)

        # Case where the number of indices matches the rank of the values tensor
        if values_rank == len(idx):
            # frac_bits/scale have maximum 1 dimension so the slicing is done on the last dimension.
            return tensor[idx[-1]]

        # Case where the frac_bits/scales tensor has fewer dimensions than the remaining positions
        elif values_rank - len(idx) - 1 >= 0:
            return tensor

        # Case where the frac_bits/scales tensor needs more dimensions
        else:
            m = 1 - (values_rank - len(idx))
            fb_ind = idx[-m:]
            fb_ind += (Ellipsis,)
            return tensor[fb_ind]

    # Case where the index is not a tuple (int, ellipsis, scalar)
    # and values values has more dimensions than the frac_bits/scales tensor
    elif values_rank > 1:
        return tensor

    # Case where the values and tensor have the same dimensions
    else:
        return tensor[idx]
