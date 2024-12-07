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
__all__ = ["CalibrationDataReader"]

import numpy as np
import warnings

import onnx
from onnxruntime.quantization import CalibrationDataReader as _CalibrationDataReader

from .model import ONNXModel
from ...random import generate_np_random_samples


class CalibrationDataReader(_CalibrationDataReader):
    """Object to read or generate a set of samples to calibrate an ONNX model to be quantized.

    If samples are not specified, generate random samples in the range of [-1, 1]
    when input model type is float, otherwise infer ranges.

    Common use mode:
    >>> dr = CalibrationDataReader(onnx_path, num_samples=10, batch_size=1)
    >>> sample = dr.get_next()
    >>> assert sample[dr.inputs_name].shape[0] == 1
    >>> assert sample[dr.inputs_name].min() >= -1
    >>> assert sample[dr.inputs_name].max() <= 1

    Args:
        model (str or ModelProto or ONNXModel): the ONNX model (or its path) to be calibrated.
        samples (str or np.ndarray, optional): the samples (or its path) to process.
            If not provided, generate random samples following the model input shape
            and the batch_size attribute. Defaults to None.
        num_samples (int, optional): the number of samples to generate.
            Ignore it if samples are provided. Defaults to None.
        batch_size (int, optional): split samples in batches.
            Overwrite it when the model has static inputs. Defaults to 1.
    """

    def __init__(self,
                 model,
                 samples=None,
                 num_samples=None,
                 batch_size=1):

        # Read model
        model = _read_model(model)
        self.input_name = model.input[0].name
        input_shape = model.get_input_shape(input_name=self.input_name)
        input_type = model.get_input_dtype(input_name=self.input_name)

        # Read/Generate dataset
        self.batch_size = input_shape[0] if isinstance(input_shape[0], int) else batch_size or 1
        self.samples = _load_samples(samples, input_shape, input_type, num_samples=num_samples)

        # Truncate samples to fit model batch size (when is static)
        if isinstance(input_shape[0], int):
            N, res = divmod(self.samples.shape[0], self.batch_size)
            N *= self.batch_size
            if res != 0:
                warnings.warn("Truncating samples to fit model batch size "
                              f"({N} instead of {self.samples.shape[0]}).")
                self.samples = self.samples[:N]

        # Process samples
        self.index = 0
        self.num_samples = self.samples.shape[0] / self.batch_size

    def get_next(self):
        if self.index >= self.num_samples:
            print(f"\rCalibrating with {self.index}/{self.num_samples} samples", end="")
            return print()

        sample = self.samples[self.index * self.batch_size:(self.index + 1) * self.batch_size]
        self.index += 1
        return {self.input_name: sample}

    def rewind(self):
        self.index = 0


def _load_samples(samples, input_shape, input_type, num_samples=None):
    # Parse sample
    if isinstance(samples, str):
        data = np.load(samples)
        samples = np.concatenate([data[item] for item in data.files])
    elif samples is None:
        if num_samples is None:
            raise ValueError("Either samples or num_samples must be specified")
        samples = generate_np_random_samples((num_samples, *input_shape[1:]), input_type)
    if not isinstance(samples, np.ndarray):
        raise ValueError(f"Unrecognized '{type(samples)}' samples.")

    return samples


def _read_model(model):
    if isinstance(model, str):
        model = onnx.load_model(model)
    if isinstance(model, onnx.ModelProto):
        model = ONNXModel(model)
    if not isinstance(model, ONNXModel):
        raise ValueError(f"Unrecognized '{type(model)}' model.")

    assert len(model.input) == 1, "multi-input are not supported models yet"
    return model
