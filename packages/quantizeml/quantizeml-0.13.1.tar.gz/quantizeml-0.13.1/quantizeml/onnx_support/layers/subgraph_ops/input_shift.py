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
__all__ = ["get_input_shift_ops"]

from onnx.helper import make_node


def get_input_shift_ops(in_name, s_name, out_name):
    """Return the input shift operation chain

    Args:
        in_name (str): the input tensor name.
        s_name (str): the shift tensor name.
        out_name (str): the required output tensor name.

    Returns:
        list of NodeProto: the operation chain.
    """
    return [make_node("Mul", inputs=[in_name, s_name], outputs=[out_name])]
