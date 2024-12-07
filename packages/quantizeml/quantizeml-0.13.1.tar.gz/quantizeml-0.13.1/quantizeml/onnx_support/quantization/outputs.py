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
from onnxruntime.quantization.calibrate import TensorData

from .fixed_point import to_fixed_point
from .input_scale import input_scale_no_zp
from .weights import align_to


def downscale(output_range, i_scale, force_fp=False, bitwidth=8):
    """Calculates the scale that should be applied to an integer tensor
    with i_scale to project it to a desired bitwidth.

    The following set of operations must be applied to the tensor to project it
    into the output scale:

    >>> out_tensor = tensor * scale
    >>> out_tensor = out_tensor >> log2(shift)

    Args:
        output_range (tuple): the calibrate tensor range
        i_scale (np.ndarray): the input scale
        force_fp (bool, optional): whether to force output scale as a power-of-two.
            Defaults to False.
        bitwidth (int, optional): the desired output bitwidth. Defaults to 8.

    Returns:
        np.ndarray, np.ndarray, np.ndarray: the integer scale/shift and the new float scale
    """
    if force_fp:
        # The multi-input layers supported in akida (such as Add) do not include a scale-in
        # operation but only a shift-in. In consequence output must be downscaled as a fixed-point.
        return downscale_fp(output_range, i_scale, bitwidth=bitwidth)
    return downscale_qf(output_range, i_scale, bitwidth)


def downscale_qf(output_range, i_scale, bitwidth=8):
    # Consider all outputs to be 8-bits, otherwise the scale would be different.
    ocalib_scale = input_scale_no_zp(output_range)
    # Divide o_calib_scale by i_scale in the same axis to obtain output scale:
    # this will consider the input scale into account.
    o_scale = align_to(ocalib_scale, i_scale.ndim) / i_scale
    # Quantize o_scale to fit in scale + shift at 8 bit
    scale, shift = to_fixed_point(o_scale, bitwidth=bitwidth, signed=False)
    # Return shift value as a power of two
    s_out = np.array(2. ** shift, dtype=np.float32)
    return scale, s_out, np.array(ocalib_scale, "float64")


def downscale_fp(output_range, i_scale, bitwidth=8):
    assert isinstance(output_range, TensorData)
    # Dequantize inputs in integer domain (apply scale out), multiplying by the inverse scale
    scale, in_shift = to_fixed_point(1.0 / i_scale, bitwidth=bitwidth, signed=False)
    # Compute the required output shift to come out in 8bits
    output_max = np.maximum(np.abs(output_range.lowest), np.abs(output_range.highest))
    _, out_shift = to_fixed_point(output_max, bitwidth=bitwidth, signed=True, clamp=True)
    # Compute shift to go from in_shift to out_shift in the same axis
    # The shift can be positive (left-shift) or negative (rounded right-shift)
    shift = align_to(out_shift, i_scale.ndim) - in_shift
    # A positive shift exceeding the target bitwidth always leads to a saturation
    np.testing.assert_array_less(shift, bitwidth,
                                 f"Cannot rescale inputs to {bitwidth} as it will saturate.")
    # In ONNX output shift is done as division (against to akida: a left shift)
    shift = np.array(2. ** -shift, dtype=np.float32)
    # Finally, outputs will have a fractional scale
    o_scale = np.array(2.0 ** out_shift, "float64")
    return scale, shift, o_scale
