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

__all__ = ["recording", "TensorRecorder", "FixedPointRecorder", "QFloatRecorder", "Recorder",
           "NonTrackVariable", "NonTrackFixedPointVariable"]

import os
import tensorflow as tf
from contextlib import contextmanager

from ..tensors import FixedPoint, QFloat

RECORDING_ENV = "RECORDING_ENABLED"


@contextmanager
def recording(enable):
    """Enable or disable recording.

    Args:
        enable (bool): True to enable recording, False to disable it
    """
    value = "1" if enable else "0"
    _prev_state = os.environ.get(RECORDING_ENV, None)
    try:
        os.environ[RECORDING_ENV] = value
        yield
    finally:
        # Recover default value
        if _prev_state is not None:
            os.environ[RECORDING_ENV] = _prev_state
        else:
            os.environ.pop(RECORDING_ENV)


class BaseNonTrackVariable():
    """Base interface class for temporary variables that should be tracked only during the call and
        which does not require to be serialized within the layer.
    """

    def __init__(self, name=""):
        self._name = name
        self._var = None

    @property
    def var(self):
        raise NotImplementedError

    @tf.function
    def set_var(self, new_value):
        raise NotImplementedError

    @tf.function
    def init_var(self):
        raise NotImplementedError

    def reset_var(self):
        raise NotImplementedError


class NonTrackVariable(BaseNonTrackVariable):
    """A wrapper class for the temporary Tensor variables that should be tracked only during the
        call and which does not require to be serialized within the layer.
    """

    @property
    def var(self):
        return self._var

    @tf.function
    def set_var(self, new_value):
        self._var.assign(new_value)

    @tf.function
    def init_var(self, init_value, validate_shape=False):
        """Function that creates and initializes a variable, if it doesn't exist. This variable will
            be integrated in the layer graph and tracked (but not within the main layer variables).
            See pattern defined here: https://www.tensorflow.org/guide/function#creating_tfvariables

        Args:
            init_value (tf.Tensor): Tensor, or Python object convertible to a Tensor which is the
                initial value for the Variable. The initial value must have a shape specified
                unless validate_shape is set to False.
            validate_shape (bool, optional): If False, allows the variable to be initialized with a
                value of unknown shape. If True the shape of initial_value must be known.
                Defaults to False.
        """

        if self._var is None:
            self._var = tf.Variable(init_value, trainable=False,
                                    validate_shape=validate_shape,
                                    name=self._name,
                                    synchronization=tf.VariableSynchronization.ON_READ)

    def reset_var(self):
        """ Reset internal var."""
        if self._var is not None:
            self._var.assign_add(-self._var)


class NonTrackFixedPointVariable(BaseNonTrackVariable):
    """A wrapper class for the temporary FixedPoint variables that should be tracked only during
        the call and which does not require to be serialized within the layer.
    """

    def __init__(self, name=""):
        super().__init__(name)
        self._frac_bits = None
        self._value_bits = None

    @property
    def var(self):
        return None if self._var is None else FixedPoint(self._var, self._value_bits,
                                                         self._frac_bits)

    def promote(self, target_value_bits):
        return self.var.promote(target_value_bits)

    def expand(self, target_value_bits):
        return self.var.expand(target_value_bits)

    @tf.function
    def set_var(self, new_value):
        assert (isinstance(new_value, FixedPoint))
        self._var.assign(new_value.values)
        self._frac_bits.assign(new_value.frac_bits)
        self._value_bits = new_value.value_bits

    @tf.function
    def init_var(self, init_value, validate_shape=False):
        """Function that creates and initializes a variable, if it doesn't exist. This variable will
            be integrated in the layer graph and tracked (but not within the main layer variables).
            See pattern defined here: https://www.tensorflow.org/guide/function#creating_tfvariables

        Args:
            init_value (FixedPoint): initial FixedPoint variable.
            validate_shape (bool, optional): If False, allows the variable to be initialized with a
                value of unknown shape. If True the shape of initial_value must be known.
                Defaults to False.
        """
        assert (isinstance(init_value, FixedPoint))
        if self._var is None:
            self._var = tf.Variable(init_value.values, trainable=False,
                                    validate_shape=validate_shape,
                                    name=self._name,
                                    synchronization=tf.VariableSynchronization.ON_READ)

            self._frac_bits = tf.Variable(init_value.frac_bits, trainable=False,
                                          validate_shape=validate_shape,
                                          name=self._name + "/frac_bits",
                                          synchronization=tf.VariableSynchronization.ON_READ)

            self._value_bits = init_value.value_bits

    def reset_var(self):
        """ Reset internal var."""
        if self._var is not None:
            self._var.assign_add(-self._var)


class NonTrackQFloatVariable(BaseNonTrackVariable):
    """A wrapper class for the temporary QFloat variables that should be tracked only during
        the call and which does not require to be serialized within the layer.
    """

    def __init__(self, name=""):
        super().__init__(name)
        self._fp = NonTrackFixedPointVariable(name=name)
        self._scales = None

    @property
    def var(self):
        return None if self._scales is None else QFloat(self._fp.var, self._scales)

    def promote(self, target_value_bits):
        return self.var.promote(target_value_bits)

    def expand(self, target_value_bits):
        return self.var.expand(target_value_bits)

    @tf.function
    def set_var(self, new_value):
        assert (isinstance(new_value, QFloat))
        self._fp.set_var(new_value.fp)
        self._scales.assign(new_value.scales)

    @tf.function
    def init_var(self, init_value, validate_shape=False):
        """Function that creates and initializes a variable, if it doesn't exist. This variable will
            be integrated in the layer graph and tracked (but not within the main layer variables).
            See pattern defined here: https://www.tensorflow.org/guide/function#creating_tfvariables

        Args:
            init_value (QFloat): initial QFloat variable.
            validate_shape (bool, optional): If False, allows the variable to be initialized with a
                value of unknown shape. If True the shape of initial_value must be known.
                Defaults to False.
        """
        assert (isinstance(init_value, QFloat))
        if self._scales is None:
            self._fp.init_var(init_value.fp, validate_shape)

            self._scales = tf.Variable(init_value.scales, trainable=False,
                                       validate_shape=validate_shape,
                                       name=self._name + "/scales",
                                       synchronization=tf.VariableSynchronization.ON_READ)

    def reset_var(self):
        """ Reset internal var."""
        if self._scales is not None:
            self._fp.reset_var()


class Recorder():
    """A wrapper class with useful properties/methods for a recorder
    """

    def __init__(self, *args, name="", **kwargs):
        super().__init__(*args, **kwargs)
        self._name = name

    @property
    def value(self):
        """Get the recorded value.

        Returns:
            Any: value of the stored record or None.
        """
        raise NotImplementedError("Child must implement this property")

    @property
    def name(self):
        return self._name if self._name is not None else "record"

    @property
    def recording(self):
        """Flag to specify if the object is in recording mode or not.

        Returns:
            bool: True if recording mode is enabled, False otherwise.
        """
        value = os.environ.get(RECORDING_ENV, "0")
        return (value == "1")

    def __call__(self, inputs):
        raise NotImplementedError("Child must implement this function")


class TensorRecorder(Recorder, NonTrackVariable):
    """Wrapper class to store and retrieve a tf.Tensor extracted from a graph.

    This is mainly used to recover FixedPoint alignment shift information.
    """

    @property
    def value(self):
        """Get the recorded value.

        Returns:
            tf.Tensor: value of the stored record or None.
        """
        return None if self._var is None else self._var.value()

    def __call__(self, inputs):
        """Record the values of the inputs if recording is True.

        Args:
            inputs (tf.Tensor): new values.

        Returns:
            tf.Tensor: the inputs.
        """
        self.init_var(tf.zeros_like(inputs), True)
        if self.recording:
            # Store the new values
            self.set_var(inputs)
        return inputs


class FixedPointRecorder(Recorder):
    """Wrapper class to store and retrieve a FixedPoint extracted from a graph.

    This is mainly used to recover FixedPoint quantized weights.
    """

    def __init__(self, name=""):
        super().__init__(name=name)
        if name != "":
            name += "/"
        self._values = TensorRecorder(name + "values/record")
        self._frac_bits = TensorRecorder(name + "frac_bits/record")
        self._value_bits = None

    @property
    def value(self):
        """Get the recorded value.

        Returns:
            :obj:`FixedPoint`: value of the stored record or None.
        """
        return None if self._value_bits is None else FixedPoint(self._values.value,
                                                                self._value_bits,
                                                                self._frac_bits.value)

    def __call__(self, inputs):
        """Record the values of the inputs if recording is True.

        Args:
            inputs (:obj:`FixedPoint`): new values.

        Returns:
            :obj:`FixedPoint`: the inputs.
        """
        if self.recording:
            self._value_bits = inputs.value_bits
        self._values(inputs.values)
        self._frac_bits(inputs.frac_bits)
        return inputs


class QFloatRecorder(Recorder):
    """Wrapper class to store and retrieve a QFloat extracted from a graph.

    This is mainly used to recover QFloat quantized weights.
    """

    def __init__(self, name=""):
        super().__init__(name=name)
        self._fp = FixedPointRecorder(name)
        scales_name = "scales/record"
        if name != "":
            scales_name = name + "/" + scales_name
        self._scales = TensorRecorder(scales_name)

    @property
    def value(self):
        """Get the recorded value.

        Returns:
            :obj:`QFloat`: value of the stored record or None.
        """
        return None if self._fp.value is None else QFloat(self._fp.value, self._scales.value)

    def __call__(self, inputs):
        """Record the values of the inputs if recording is True.

        Args:
            inputs (:obj:`QFloat`): new values.

        Returns:
            :obj:`QFloat`: the inputs.
        """
        self._fp(inputs.fp)
        self._scales(inputs.scales)
        return inputs
