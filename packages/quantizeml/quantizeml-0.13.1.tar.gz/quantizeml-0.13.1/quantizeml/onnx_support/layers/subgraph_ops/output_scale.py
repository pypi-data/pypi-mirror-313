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
__all__ = ["get_scale_out_ops"]

from onnx.helper import make_node


def get_scale_out_ops(in_name, out_name, scale_name="Scale", shift_name="Shift", saturate=True):
    """Return the scale out operation chain, following the steps:

    1. Apply shift and scale to inputs,
    2. Perform Round(x) as Floor(x + 0.5) (to workaround banker's rounding),
    3. (Optional) Clip in output range [-128, 127].

    Args:
        in_name (str): the input tensor name.
        out_name (str): the required output tensor name.
        scale_name (str, optional): the scale tensor name. Defaults to Scale.
        shift_name (str, optional): the shift tensor name. Defaults to Shift.
        saturate (bool, optional): whether to saturate the output. Defaults to True.

    Returns:
        list of NodeProto: the operation chain.
    """
    nodes = []
    # Apply shift + scale
    # Note: We apply first shift to avoid (on float) the saturation due to the mantissa.
    nodes.append(make_node("Div", [in_name, shift_name], [f"{in_name}/scaled"]))
    if scale_name:
        nodes[-1].output[0] = f"{in_name}/div"
        nodes.append(make_node("Mul", [f"{in_name}/div", scale_name], [f"{in_name}/scaled"]))
    # Round as Floor(x + 0.5)
    # Note: for positive shift, the results being integer, the rounding has no effect.
    # We therefore apply the same operations for both shifts.
    y_out_name = out_name if not saturate else f"{in_name}/q"
    nodes += [make_node("Constant", [], ["OneHalf"], value_float=0.5),
              make_node("Add", [f"{in_name}/scaled", "OneHalf"], [f"{in_name}/half"]),
              make_node("Floor", [f"{in_name}/half"], [y_out_name])]
    # 3. Clip in output range (optional)
    if saturate:
        nodes += [make_node("Constant", [], ["min_range"], value_float=-128.0),
                  make_node("Constant", [], ["max_range"], value_float=127.0),
                  make_node("Clip", [f"{in_name}/q", "min_range", "max_range"], [out_name])]
    return nodes
