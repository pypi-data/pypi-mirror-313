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
"""
quantizeml main command-line interface.
"""

import argparse
import json
import os
import re
import numpy as np
import os.path

from importlib import metadata

from keras.models import Model, Sequential

from . import load_model, save_model
from .layers import QuantizationParams
from .models import quantize, dump_config
from .models.transforms import insert_rescaling
from .analysis.cli import main as analysis_cli, add_analysis_arguments


def quantize_model(model_path, quant_config, qparams, samples, num_samples, batch_size, epochs,
                   output_name=None, quantize_until=None):
    """ CLI entry point to quantize a model using the provided configuration.

    Args:
        model_path (str): Path to the model to quantize.
            Only supported for Keras and ONNX models.
        quant_config (str): Path to the quantization configuration file.
        qparams (QuantizationParams): global quantization parameters.
        samples (str): calibration samples file path.
        num_samples (int): number of samples to use in the provided samples.
        batch_size (int): batch size for calibration.
        epochs (int): number of epochs for calibration.
        output_name (str, optional): name of the output quantized model. If none provided
            set a default name as <model>_<config>.h5. Defaults to None.
        quantize_until (str, optional): Layer/node name up to which to quantize. Defaults to None.
    """
    # Build name for the output model
    model_name = os.path.splitext(model_path)[0]
    _, ext = os.path.splitext(model_path)
    model_ext = ext.lower()

    # Set default output_name using the config when there is one and the qparams otherwise
    if output_name is None:
        if quant_config:
            output_name = f"{model_name}_{os.path.splitext(os.path.basename(quant_config))[0]}.h5"
        else:
            # Quantization suffix has a well-identified structure, only keep the actual base name
            # without it
            model_name = re.split(r'(_i\d_w\d_a\d)', model_name)[0]
            output_name = f"{model_name}_i{qparams.input_weight_bits}_w{qparams.weight_bits}"\
                          f"_a{qparams.activation_bits}{model_ext}"

    # Load the configuration file
    if quant_config:
        with open(quant_config) as f:
            config = json.load(f)
    else:
        config = None

    # Load the model
    model = load_model(model_path)

    # Load calibration samples
    if samples:
        data = np.load(samples)
        samples_arr = np.concatenate([data[item] for item in data.files])
        num_samples = len(samples_arr)
    else:
        samples_arr = None

    # Quantize the model and save it
    print(f"Quantizing model {model_path} with configuration file {quant_config}.")
    model_q = quantize(model, q_config=config, qparams=qparams, samples=samples_arr,
                       num_samples=num_samples, batch_size=batch_size, epochs=epochs,
                       quantize_until=quantize_until)
    output_name = save_model(model_q, output_name)
    print(f"Saved quantized model to {output_name}.")


def dump_model_config(model_path, output_name=None):
    """ CLI entry point to dump the quantization configuration from a model.

    Args:
        model_path (str): Path to the model to extract the configuration from.
            Only supported for Keras models.
        output_name (str): Path to save the configuration.
            Defaults to <model_path>_quant_config.json.
    """
    # Build name for the output model
    if output_name is None:
        model_name = os.path.splitext(model_path)[0]
        output_name = f"{model_name}_quant_config.json"

    # Load the model and get its quantization configuration
    model = load_model(model_path)
    # Raise an error if the model isn't a Keras
    if not isinstance(model, (Model, Sequential)):
        raise TypeError("Expecting a Keras model.")
    config = dump_config(model)
    with open(output_name, "w") as f:
        json.dump(config, f, indent=4)
    print(f"Saved quantization configuration to {output_name}.")


def insert_rescaling_and_save(model_path, dest_path, scale, offset):
    """ CLI entry point to insert a Rescaling layer in a model.

    Args:
        model_path (str): Path to the source model.
            Only supported for Keras models.
        dest_path (str): Path to the destination model.
        scale (float): the Rescaling scale
        offset (float): the Rescaling offset
    """
    model = load_model(model_path)
    # Raise an error if the model isn't a Keras
    if not isinstance(model, (Model, Sequential)):
        raise TypeError("Expecting a Keras model.")
    updated = insert_rescaling(model, scale, offset)
    updated.save(dest_path)


def main():
    """ CLI entry point.

    Contains an argument parser with specific arguments depending on the model to be created.
    Complete arguments lists available using the -h or --help argument.

    """
    # Define a strictly positive int type for parameters
    def positive_int(value):
        ivalue = int(value)
        if ivalue <= 0:
            raise argparse.ArgumentTypeError("%s is an invalid value, must be >0." % value)
        return ivalue

    parser = argparse.ArgumentParser()
    sp = parser.add_subparsers(dest="action")
    sp.add_parser("version", help="Display quantizeml version.")

    # Quantize arguments
    q_parser = sp.add_parser(
        "quantize", help="Quantize an input model, given a quantization configuration file.")
    q_parser.add_argument("-m", "--model", type=str, required=True, help="Model to quantize")
    q_parser.add_argument("-c", "--quantization_config", type=str, default=None,
                          help="Quantization configuration file")
    q_parser.add_argument("-a", "--activation_bits", type=positive_int, default=8,
                          help="Activation quantization bitwidth")
    q_parser.add_argument("-o", "--output_bits", type=positive_int, default=8,
                          help="Output quantization bitwidth")
    q_parser.add_argument("--per_tensor_activations", action='store_true',
                          help="Quantize activations per-tensor")
    q_parser.add_argument("-w", "--weight_bits", type=positive_int, default=8,
                          help="Weight quantization bitwidth")
    q_parser.add_argument("-i", "--input_weight_bits", type=positive_int, default=8,
                          help="Input layer weight quantization bitwidth")
    q_parser.add_argument("-id", "--input_dtype", type=str, default="uint8",
                          help="Numpy-like dtype format to quantize the inputs")
    q_parser.add_argument("-b", "--buffer_bits", type=positive_int, default=32,
                          help="Buffer quantization bitwidth")
    q_parser.add_argument("-lob", "--last_output_bits", type=int, default=None,
                          help="Bitwidth of the model output")
    q_parser.add_argument("-s", "--save_name", type=str,
                          help="Name for saving the quantized model.")
    q_parser.add_argument("-sa", "--samples", type=str, default=None,
                          help="Set of samples to calibrate the model (.npz file).")
    q_parser.add_argument("-ns", "--num_samples", type=positive_int, default=1024,
                          help="Number of samples to use for calibration, only used when 'samples'"
                               " is not provided.")
    q_parser.add_argument("-bs", "--batch_size", type=positive_int, default=32,
                          help="Batch size for calibration.")
    q_parser.add_argument("-e", "--epochs", type=positive_int, default=1,
                          help="Number of epochs for calibration.")
    q_parser.add_argument("-qu", "--quantize_until", type=str, default=None,
                          help="Layer/node name up to which to quantize. "
                          "By default the whole model is quantized.")

    # Dump config arguments
    c_parser = sp.add_parser(
        "config", help="Extract quantization configuration from a Keras model.")
    c_parser.add_argument("-m", "--model", type=str, required=True,
                          help="Model to extract config from.")
    c_parser.add_argument("-o", "--output_path", type=str, help="Store quantization configuration. "
                          "Defaults to <model>_quant_config.json")

    # insert_rescaling action and arguments
    ir_parser = sp.add_parser(
        "insert_rescaling", help="Insert a Rescaling layer at the beginning of the Keras model.")
    ir_parser.add_argument("-m", "--model", type=str, required=True,
                           help="Path to the source Model")
    ir_parser.add_argument("-d", "--dest_model", type=str, required=True,
                           help="Path to the destination Model")
    ir_parser.add_argument("-s", "--scale", type=float, required=True,
                           help="The Rescaling scale")
    ir_parser.add_argument("-o", "--offset", type=float, required=True,
                           help="The Rescaling offset")

    # Analysis actions
    a_parser = sp.add_parser("analysis",
                             help="Tool set to analyze potential models to be quantized")
    add_analysis_arguments(a_parser)

    args = parser.parse_args()

    if args.action == "version":
        print(metadata.version('quantizeml'))
    elif args.action == "quantize":
        qparams = QuantizationParams(activation_bits=args.activation_bits,
                                     output_bits=args.output_bits,
                                     per_tensor_activations=args.per_tensor_activations,
                                     weight_bits=args.weight_bits,
                                     input_weight_bits=args.input_weight_bits,
                                     buffer_bits=args.buffer_bits,
                                     input_dtype=args.input_dtype,
                                     last_output_bits=args.last_output_bits)
        quantize_model(
            model_path=args.model,
            quant_config=args.quantization_config,
            qparams=qparams,
            samples=args.samples,
            num_samples=args.num_samples,
            batch_size=args.batch_size,
            epochs=args.epochs,
            output_name=args.save_name,
            quantize_until=args.quantize_until,
        )
    elif args.action == "config":
        dump_model_config(
            model_path=args.model,
            output_name=args.output_path,
        )
    elif args.action == "insert_rescaling":
        insert_rescaling_and_save(args.model, args.dest_model, args.scale, args.offset)
    elif args.action == "analysis":
        analysis_cli(args)
