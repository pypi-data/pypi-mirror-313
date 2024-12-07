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
"""
Layer decorators.
"""

import inspect
import tensorflow as tf
from copy import deepcopy

from .quantization_params import get_quantization_params
from .quantizers import WeightQuantizer, AlignedWeightQuantizer, OutputQuantizer
from .recorders import TensorRecorder
from ..tensors import FixedPoint


class QuantizedLayer(tf.keras.layers.Layer):
    """Interface to define a quantized layer

    It allows to verify if the arguments match with those expected by ``arg_constraints``
    and remove those in ``ignored_args``.

    Both should be defined as class variables.

    Notes:
        * ``ignored_args`` is a list with the argument names to be skipped
        * ``arg_constraints`` is a dictionnary where each set of (key, value) corresponds
          to the argument name and the allowed value. For multiple ones, it may be a callable
          that returns the list of values (e.g. lambda: [value1, value2, ...])
    """

    def __init__(self, *args, quant_config=None, **kwargs):
        check_arg_constraints(self, kwargs)
        self._pop_ignored_args(kwargs)
        self.quant_config = init_quant_config(quant_config)
        super().__init__(*args, **kwargs)

    def _pop_ignored_args(self, config):
        """Function to handle arguments that should be ignored, i.e. dropped from config

        Args:
            config (dict): the argument list
        """
        if not isinstance(ignored_args := getattr(self, 'ignored_args', []), list):
            raise RuntimeError(f"'ignored_args' in {self.name} must be a list.")
        for arg in ignored_args:
            config.pop(arg, None)

    def build(self, input_shape):
        # Ensure variables are build with the appropriate name
        with tf.name_scope(self.name + '/'):
            super().build(input_shape)

    def get_config(self):
        config = super().get_config()
        self._pop_ignored_args(config)
        config.update({"quant_config": deepcopy(self.quant_config)})
        return config


# Mapper to match float layer with its quantized version, populated thanks to
# `register_quantize_target` decorator on quantized layers.
_GLOBAL_LAYER_TO_QLAYER = {}

# List of quantized layers that cannot rescale their outputs (no output quantizer)
_GLOBAL_NO_OUTPUT_QUANTIZER = []

# List of quantized layers that require aligned inputs
_GLOBAL_ALIGNED_INPUTS = []

# List of quantized layers that has quantizable weights
_GLOBAL_QUANTIZABLE_WEIGHTS = []


def register_quantize_target(base_layer, has_weights=False):
    """Register the current class as a target for the quantization of a keras layer.

    This decorator injects the decorated class into the _GLOBAL_LAYER_TO_QLAYER dictionary, so that
    it registered as the quantization target for the provided `base_layer`.

    Also, base_layer is injected on _GLOBAL_QUANTIZABLE_WEIGHTS list if has_weights=True.

    Args:
        base_layer (keras.Layer, list): the origin layer (or list of) that should be quantized as
            the current class
        has_weights (bool, optional): whether the layer has weights to be quantized.
            Defaults to False.

    Returns:
        Callable: a decorator that registers the decorated class
    """
    def _register_target(target, arg):
        """Register the current class as a target for the quantization of a keras layer.

        Args:
            target (keras.Layer): the target to register
            arg (Cls): the current class to register
        """
        base_class_name = target.__name__

        if not inspect.isclass(arg):
            raise ValueError("Can only register class objects with 'register_quantize_target'.")

        if base_class_name in _GLOBAL_LAYER_TO_QLAYER:
            raise ValueError(f"{base_class_name} has already been registered to "
                             f"{_GLOBAL_LAYER_TO_QLAYER[base_class_name]}.")

        _GLOBAL_LAYER_TO_QLAYER.update({base_class_name: arg})

    def decorator(arg):
        targets = base_layer if isinstance(base_layer, list) else [base_layer]
        for target in targets:
            _register_target(target, arg)
        if has_weights:
            _GLOBAL_QUANTIZABLE_WEIGHTS.append(arg)
        return arg

    return decorator


def register_no_output_quantizer(arg):
    """Register the decorated class as not able to rescale its outputs.

    _GLOBAL_NO_OUTPUT_QUANTIZER is populated with the quantized layer type.

    Args:
        arg (Cls): the class to register

    Returns:
        Callable: a decorator that registers the decorated class
    """
    if not inspect.isclass(arg):
        raise ValueError("Can only register class objects with 'register_no_output_quantizer'.")
    _GLOBAL_NO_OUTPUT_QUANTIZER.append(arg)
    return arg


def register_aligned_inputs(arg):
    """Register the decorated class as requiring aligned inputs.

    _GLOBAL_ALIGNED_INPUTS is populated with the quantized layer type.

    Args:
        arg (Cls): the class to register

    Returns:
        Callable: a decorator that registers the decorated class
    """
    if not inspect.isclass(arg):
        raise ValueError("Can only register class objects with 'register_aligned_inputs'.")
    _GLOBAL_ALIGNED_INPUTS.append(arg)
    return arg


def rescale_outputs(call):
    """ Decorator to rescale the outputs produced by a layer 'call' function.

    Args:
        call (Callable): the decorated call function

    Returns:
        Callable: the decorated function
    """

    def decorator(self, inputs):
        outputs = call(self, inputs)
        if self.out_quantizer is not None:
            outputs = self.out_quantizer(outputs)
        return outputs
    return decorator


def tensor_inputs(supported):
    """ Decorator to check the input tensors passed to a layer `call`.

    Args:
        supported (list): list of supported input types

    Returns:
        Callable: the decorated function
    """

    def decorator(call):
        if not isinstance(supported, (list, tuple)):
            raise TypeError(f"'supported' must be a list or a tuple, received {type(supported)}.")

        def check_inputs(self, inputs):
            # Raise an error if the inputs are not in the 'supported' types
            if not isinstance(inputs, tuple(supported)):
                raise TypeError(f"{self.__class__.__name__} only accepts {supported} inputs. "
                                f"Receives {type(inputs)} inputs.")

            if isinstance(inputs, tf.Tensor):
                if not inputs.dtype.is_integer:
                    # Cast float inputs following the quantization context
                    default_input_dtype = get_quantization_params().input_dtype
                    inputs = tf.cast(inputs, default_input_dtype)
                # Deduce in_bits from inputs type
                in_bits = inputs.dtype.size * 8
                if not inputs.dtype.is_unsigned:
                    in_bits -= 1
                inputs = FixedPoint(inputs, in_bits, 0)
            # If the layer is a (Depthwise)BTC the input alignement is handled directly in the
            # layer call method, after the input is added to the fifo.
            if self.__class__.__name__ in ['QuantizedBufferTempConv',
                                           'QuantizedDepthwiseBufferTempConv']:
                return call(self, inputs)
            if getattr(self, 'buffer_bitwidth', None) is not None:
                if (isinstance(inputs, FixedPoint) and not inputs.per_tensor
                        and self.__class__.__name__ not in
                        ['QuantizedDepthwiseConv2D', 'QuantizedExtractToken', 'QuantizedReLU']):
                    # Expand the inputs to a higher bitwidth to avoid saturation and align them.
                    # Depthwise layers do not require input_shift because each channel is
                    # handled by a single filter.
                    inputs, shift = inputs.expand(self.buffer_bitwidth)
                    if getattr(self, 'input_shift', None) is None:
                        # Add object that will store the shift values.
                        # From Keras documentation, any variable creation taking place in call
                        # should be wrapped with tf.init_scope
                        with tf.init_scope():
                            self.input_shift = TensorRecorder(name=self.name + "/input_shift")
                    self.input_shift(shift)
                else:
                    # Promote inputs to avoid a saturation
                    inputs = inputs.promote(self.buffer_bitwidth)
            return call(self, inputs)
        return check_inputs
    return decorator


def neural_layer_init(separable, bias_bits=8):
    """ Decorator to initialize a neural layer.

    Args:
        separable (bool): True if the layer has separable weights.
        bias_bits (int, optional): bitwidth to set in bias quantizer. Defaults to 8.

    Returns:
        Callable: the decorated function
    """
    def decorator(init):
        def wrapper(self, *args, **kwargs):
            # First call super().__init__
            super_init = getattr(super(type(self), self), "__init__")
            # Checks params
            activation = kwargs.get('activation')
            if activation and activation != 'linear':
                raise ValueError(f"{self.__class__.__name__} does not support activation. "
                                 f"Receives {activation} activation.")
            # Handle special parameter "padding_value" that must not be passed to super()
            updated_kwargs = kwargs.copy()
            updated_kwargs.pop('padding_value', None)
            super_init(*args, **updated_kwargs)

            # Check data format
            if hasattr(self, "data_format") and self.data_format != "channels_last":
                raise TypeError(f"{self.__class__.__name__} only accepts channels_last data_format."
                                f" Receives {self.data_format}.")
            # Then start neural layer init
            default_weight_bits = get_quantization_params().weight_bits

            # Use quant_config to build quantizers
            if separable:
                # Separable layer has two weights quantizers to handle different max values
                if "dw_weight_quantizer" not in self.quant_config:
                    self.quant_config["dw_weight_quantizer"] = {"bitwidth": default_weight_bits}
                dw_weight_quantizer_cfg = self.quant_config["dw_weight_quantizer"]
                # Separable depthwise weights are quantized per-tensor
                dw_weight_quantizer_cfg.update({'axis': None})
                self.dw_weight_quantizer = WeightQuantizer(name="dw_weight_quantizer",
                                                           **dw_weight_quantizer_cfg)
                if "pw_weight_quantizer" not in self.quant_config:
                    self.quant_config["pw_weight_quantizer"] = {"bitwidth": default_weight_bits}
                pw_weight_quantizer_cfg = self.quant_config["pw_weight_quantizer"]
                self.pw_weight_quantizer = WeightQuantizer(name="pw_weight_quantizer",
                                                           **pw_weight_quantizer_cfg)
            else:
                if "weight_quantizer" not in self.quant_config:
                    self.quant_config["weight_quantizer"] = {"bitwidth": default_weight_bits}
                weight_quantizer_cfg = self.quant_config["weight_quantizer"]
                self.weight_quantizer = WeightQuantizer(name="weight_quantizer",
                                                        **weight_quantizer_cfg)

            # Finalize output and bias quantizers
            out_quant_cfg = self.quant_config.get("output_quantizer", False)
            if out_quant_cfg:
                self.out_quantizer = OutputQuantizer(name="output_quantizer", **out_quant_cfg)
            else:
                self.out_quantizer = None
            if self.use_bias:
                bias_quantizer_cfg = self.quant_config.get("bias_quantizer",
                                                           {"bitwidth": bias_bits})
                self.bias_quantizer = AlignedWeightQuantizer(name="bias_quantizer",
                                                             **bias_quantizer_cfg)
            self.buffer_bitwidth = apply_buffer_bitwidth(self.quant_config, signed=True)

            # Baseline init
            init(self, *args, **kwargs)
        return wrapper
    return decorator


def init_quant_config(quant_config):
    """Ensures that modifications do not affect the original quantization configuration.

    Args:
        quant_config (dict): the serialized quantization configuration.

    Returns:
        dict: a serialized quantization configuration.
    """
    if isinstance(quant_config, dict):
        return deepcopy(quant_config)
    return dict()


def apply_buffer_bitwidth(quant_config, signed=True):
    """ Read buffer_bitwidth on quant_config. If it is missing,
    set 'buffer_bitwidth' parameter in ``quant_config`` with default value given by the context.

    Args:
        quant_config (dict): the serialized quantization configuration.
        signed (bool, optional): whether operations will be done with sign. Defaults to True.

    Returns:
        int: buffer bitwidth value
    """
    buffer_bits = quant_config.get("buffer_bitwidth", None)
    if buffer_bits is None:
        buffer_bits = get_quantization_params().buffer_bits
        quant_config["buffer_bitwidth"] = buffer_bits
    if signed:
        buffer_bits -= 1
    return buffer_bits


def check_arg_constraints(layer, config):
    """Function to check unsupported arguments in config

    Args:
        layer (keras.Layer): layer to extract unsupported arguments
        config (dict): the list of arguments to check

    Note: This function does not remove arg from config, given there are layers
        that still need these parameters (with their default value). Please use
        pop_ignored_args if they have to be removed.
    """
    if not isinstance(arg_constraints := getattr(layer, 'arg_constraints', {}), dict):
        raise RuntimeError(f"'arg_constraints' in {layer.name} must be a dict.")
    for arg, arg_value in arg_constraints.items():
        supported_values = arg_value() if callable(arg_value) else [arg_value]
        if arg in config and not any(config[arg] == x for x in supported_values):
            lname = getattr(layer, 'name', config.get('name', layer.__class__.__name__))
            raise RuntimeError(
                f"Argument '{arg}' in layer '{lname}' is only supported with "
                f"one of {supported_values}. Receives '{config[arg]}'.")
