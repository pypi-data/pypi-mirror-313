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
__all__ = ["get_op_version"]


import onnx


def get_op_version(op_type, model):
    """Helper to get the opset version of an operation type in the model.

    Args:
        op_type (str): the operation type
        model (ModelProto): the model containing the operation.

    Returns:
        int: the opset version
    """
    for opset_import in model.opset_import:
        if onnx.defs.has(op_type, opset_import.domain):
            return opset_import.version
    raise RuntimeError(f"Model does not contain a version for '{op_type}'.")
