#!/usr/bin/env python
# ******************************************************************************
# Copyright 2024 Brainchip Holdings Ltd.
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
__all__ = ["extract_submodel_from_qnode"]

import onnx

from ...onnx_support.quantization import ONNXModel


def extract_submodel_from_qnode(qnode, qmodel, model_to_extract):
    """Extract a submodel of 'model_to_extract' that represents the 'qnode' chain of operations

    Args:
        qnode (onnx.NodeProto): the reference quantized node
        qmodel (ONNXModel): the model containing qnode
        model_to_extract (ONNXModel): Model to extract the chain of operations

    Returns:
        ONNXModel: a submodel of 'model_to_extract'
    """
    def _get_input_tensor_name(node, idx, model, skip_ops=[]):
        parent = model.get_parent(node, idx)
        if parent is not None and parent.op_type in skip_ops:
            return _get_input_tensor_name(parent, 0, model, skip_ops=skip_ops)
        return node.input[idx]

    if qnode.domain != "com.brainchip":
        raise ValueError(f"Unrecognized '{qnode.op_type}' quantized node.")
    elif qnode.op_type in ["InputQuantizer", "Dequantizer"]:
        raise ValueError(f"It is not possible to extract a submodel from {qnode.op_type}, "
                         f"since it does not represent any node in {model_to_extract.name}.")

    # Search node inputs
    input_names = []
    initializer_names = qmodel.get_initializer_name_set()
    for idx, iname in enumerate(qnode.input):
        if iname in initializer_names:
            # This input is an initializer (weight). Skip it
            continue

        if qnode not in model_to_extract.nodes():
            # iname will be replaced by input graph name if node is linked to an InputQuantizer,
            # since first float node is quantized as InputQuantizer + its quantized node
            # (e.g. Conv -> [InputQuantizer, QuantizedConv])
            iname = _get_input_tensor_name(qnode, idx, qmodel, skip_ops=["InputQuantizer"])
            # Nothing to do if node exist in 'model_to_extract'
        input_names.append(iname)

    # Extract submodel from 'model_to_extract_nodes' with nodes between the tensor names:
    # input_names -> node_1 -> node_2 -> ... -> node_n -> qnode.output[0]
    output_names = qnode.output[:1]
    try:
        extractor = onnx.utils.Extractor(model_to_extract.model)
        submodel = extractor.extract_model(input_names, output_names)
    except Exception as e:
        raise RuntimeError(f"{model_to_extract.name} does not contain tensor with names "
                           f"{input_names + output_names}. More detail in:\n{str(e)}")
    return ONNXModel(submodel)
