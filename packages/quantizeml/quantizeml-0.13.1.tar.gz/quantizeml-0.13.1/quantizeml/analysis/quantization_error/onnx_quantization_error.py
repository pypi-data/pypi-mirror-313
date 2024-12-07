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
import numpy as np
import onnxruntime

from ...onnx_support.quantization.quantize import ONNXModel
from ...onnx_support.graph_tools import get_field
from ...onnx_support.quantization.weights import align_to
from ...onnx_support.random import generate_onnx_random_samples
from ..tools import extract_submodel_from_qnode
from .common import compare, remove_outliers, eval_metrics, compute_saturation

skippable_qnodes = ("InputQuantizer", "Dequantizer")


def _is_measurable(qnode):
    return qnode.op_type not in skippable_qnodes and qnode.domain == "com.brainchip"


def _get_scale_zp(node, qmodel):
    scale, zp = get_field(node, "scale"), 0
    # Zero point could be different to zero if node is an InputQuantizer
    if node.op_type == "InputQuantizer":
        zp = qmodel.get_variable(node.input[2])
    return scale, zp


def _dequantize(x, scales, zp=0, otype="float32"):
    return ((x.astype("int32") - align_to(zp, x.ndim)) / align_to(scales, x.ndim)).astype(otype)


def _get_node(node_name, model):
    node = model.find_node_by_name(node_name)
    if node is None:
        raise RuntimeError(f"{model.name} must have node '{node_name}'")
    return node


def _compute_mask(x):
    min_value = np.iinfo(x.dtype).min
    max_value = np.iinfo(x.dtype).max
    mask = (x > min_value) & (x < max_value)
    return mask


def _search_quantized_target_nodes(model, target_node_name=None):
    if target_node_name is not None:
        target_nodes = [_get_node(target_node_name, model)]
    else:
        target_nodes = model.nodes()
    # Filter target nodes
    target_nodes = [node for node in target_nodes if _is_measurable(node)]
    if len(target_nodes) == 0:
        raise ValueError(f"{model.name} does not contain nodes that generate quantization error!")
    return target_nodes


def compare_outputs(foutputs, qoutputs, qscales, per_channel=False):
    """Measures the error in a set of arrays

    Args:
        foutputs (np.ndarray): the output of a float layer.
        qoutputs (np.ndarray): the quantized output to be compare with ``foutputs``.
        qscales (np.ndarray): scales to dequantize ``qoutputs``.
        per_channel (bool, optional): comparison is done for each channel. Defaults to False.

    Returns:
        dict or list: the quantization error.
    """
    assert np.issubdtype(qoutputs.dtype, np.integer), f"{qoutputs} must be integer"

    axis = (1 if foutputs.ndim > 1 else 0) if per_channel else None
    # Saturation is reduced through axis = 1 (format BCHW)
    saturation = compute_saturation(qoutputs, axis=axis)

    # Creates a mask where is indicated if a value saturate or not
    mask = _compute_mask(qoutputs)

    # Compare float/quantized outputs.
    # Note we need to dequantize qoutputs to be compared with foutputs
    # as well as excluding saturated values, since the error is ambiguous out of range.
    qoutputs = _dequantize(qoutputs, qscales)
    foutputs = remove_outliers(foutputs, mask, axis=axis)
    qoutputs = remove_outliers(qoutputs, mask, axis=axis)
    return compare(foutputs, qoutputs, saturation)


def quantization_error(fmodel, qmodel, target_node=None, batch_size=16, seed=None):
    """Measures the node quantization error in a set of ONNX models

    Args:
        fmodel (onnx.ModelProto): the float model.
        qmodel (onnx.ModelProto): the quantized version of `fmodel`.
        target_node (str, optional): computation error is performed only in the target node,
            expanding the analysis to each output channel. Defaults to None.
        batch_size (int, optional): the batch size. Defaults to 16.
        seed (int, optional): a random seed. Defaults to None.

    Returns:
        dict: the quantization error of the target nodes
    """
    fmodel = ONNXModel(fmodel)
    qmodel = ONNXModel(qmodel).clone()

    # Search target nodes and update graph outputs
    qtarget_nodes = _search_quantized_target_nodes(qmodel, target_node_name=target_node)

    # Create a quantized intermediate model with the inputs of qtarget_nodes
    qmodel.graph().ClearField("output")
    for qnode in qtarget_nodes:
        for iname in qnode.input:
            qvi = qmodel.find_value_info_by_name(iname)
            if qvi is not None and qvi not in qmodel.output:
                qmodel.output.append(qvi)

    # Retrieve all scales and zero points. Need to compute float inputs
    in_scales, in_zps, out_names = {}, {}, []
    outputs_to_node = qmodel.output_name_to_node()
    for qvi in qmodel.output:
        in_scales[qvi.name], in_zps[qvi.name] = _get_scale_zp(outputs_to_node[qvi.name], qmodel)
        out_names.append(qvi.name)

    # Generate a random set of samples
    samples = generate_onnx_random_samples(qmodel, batch_size=batch_size, seed=seed)

    # Compute quantization error per layer:
    # Generate the set of input quantized samples
    qinputs = onnxruntime.InferenceSession(qmodel.serialized).run(None, samples)
    qinputs = dict(zip(out_names, qinputs))

    # Compute quantization error per quantized node
    summary = {}
    per_channel = target_node is not None
    for qnode in qtarget_nodes:
        # Extract submodel from fmodel that represent the qnode operations in float-domain
        subfmodel = extract_submodel_from_qnode(qnode, qmodel, fmodel)

        # Extract a submodel from qmodel which contains just qnode
        subqmodel = extract_submodel_from_qnode(qnode, qmodel, qmodel)

        # Build feeds
        # Note: input names may change given qmodel has new nodes (e.g. InputQuantizer)
        qfeed = {k: qinputs[k] for k in [vi.name for vi in subqmodel.input]}
        ffeed = {k: _dequantize(qinputs[qk], in_scales[qk], zp=in_zps[qk])
                 for qk, k in zip(qfeed.keys(), [x.name for x in subfmodel.input])}

        # Forward inputs in submodels
        foutputs = onnxruntime.InferenceSession(subfmodel.serialized).run(None, ffeed)[0]
        qoutputs = onnxruntime.InferenceSession(subqmodel.serialized).run(None, qfeed)[0]
        scale, _ = _get_scale_zp(qnode, qmodel)

        # Compare results
        qerror = eval_metrics(compare_outputs(foutputs, qoutputs, scale, per_channel=per_channel))
        summary[f"{qnode.name} ({qnode.op_type})"] = qerror
    return summary


def cumulative_quantization_error(fmodel, qmodel, target_node=None, batch_size=16, seed=None):
    """Measures the cumulative quantization error in a set of ONNX models

    Args:
        fmodel (onnx.ModelProto): the float model.
        qmodel (onnx.ModelProto): the quantized version of `fmodel`.
        target_node (str, optional): error computation is performed only in the target node,
            expanding the analysis to each output channel. Defaults to None.
        batch_size (int, optional): the batch size. Defaults to 16.
        seed (int, optional): a random seed. Defaults to None.

    Returns:
        dict: the quantization error by each layer
    """
    def _copy_vi_and_replace_type(x, new_type):
        new_vi = x.__deepcopy__()
        new_vi.type.tensor_type.elem_type = new_type
        return new_vi

    # We clone the models to avoid modifying the original ones
    qmodel = ONNXModel(qmodel).clone()
    fmodel = ONNXModel(fmodel).clone()

    # Input name between both models should be the same
    in_qnames = [vi.name for vi in qmodel.input]
    if [vi.name for vi in fmodel.input] != in_qnames:
        raise RuntimeError(f"{fmodel.name} does not contain tensor with names {in_qnames}")

    # Search target nodes and update graph outputs
    per_channel = target_node is not None
    qtarget_nodes = _search_quantized_target_nodes(qmodel, target_node_name=target_node)

    # Create the intermediate models with multiple outputs
    fout_type = fmodel.output[0].type.tensor_type.elem_type
    fmodel.graph().ClearField("output")
    qmodel.graph().ClearField("output")
    foutput_names = [node.output[0] for node in fmodel.nodes()]
    for qnode in qtarget_nodes:
        # Search qnode.output in ValueInfoProto.
        # It will be a new output of the quantized model.
        qvi = qmodel.find_value_info_by_name(qnode.output[0])
        qmodel.output.append(qvi)

        # Intermediate quantized outputs must be contained in fmodel
        if qvi.name not in foutput_names:
            raise RuntimeError(f"{fmodel.name} does not contain '{qvi.name}'")

        # Since the name of the intermediate outputs between fmodel and qmodel must be the same,
        # we can include qvi as an output of fmodel. Note that the type must be updated
        vi = _copy_vi_and_replace_type(qvi, new_type=fout_type)
        fmodel.output.append(vi)

    # Generate a random set of samples and split them in batches of 1
    samples = generate_onnx_random_samples(fmodel, batch_size=batch_size, seed=seed)

    # Create sessions
    fsess = onnxruntime.InferenceSession(fmodel.serialized)
    qsess = onnxruntime.InferenceSession(qmodel.serialized)

    # Compute cumulative quantization error
    summary = {}
    outputs = fsess.run(None, samples), qsess.run(None, samples)
    for qnode, foutputs, qoutputs in zip(qtarget_nodes, *outputs):
        key = f"{qnode.name} ({qnode.op_type})"
        # Retrieve scale to dequantize qoutputs
        qscales, _ = _get_scale_zp(qnode, qmodel)

        # Compute cumulative quantization error
        qerror = eval_metrics(compare_outputs(foutputs, qoutputs, qscales, per_channel=per_channel))
        summary[key] = qerror
    return summary
