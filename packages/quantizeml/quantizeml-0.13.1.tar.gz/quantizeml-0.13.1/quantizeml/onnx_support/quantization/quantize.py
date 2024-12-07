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
from collections import namedtuple
import warnings
import onnx
import numpy as np
from .calibration import calibrate
from .register_patterns import PATTERNS_MAP, CUSTOM_PATTERNS_MAP
from .model import ONNXModel
from ..graph_tools import infer_partial_io, generate_node_names
from .. import layers as onnx_qlayers
from .transforms import sanitize
from ...layers.quantization_params import QuantizationParams, quantization, get_quantization_params
from ..layers.base_layer import _GLOBAL_REQUIRES_FP_INPUTS, _GLOBAL_REQUIRES_DOWNSCALE

# Define named tuples for QuantizerPattern and Quantizer
Quantizer = namedtuple('Quantizer', ['qlayer', 'qinputs', 'out_name'])


def search_block_from_node(node, model, quantize_until=None):
    """Try to search a quantizable node sequence from a target node.

    Args:
        node (NodeProto): the search start node.
        model (ONNXModel): the model containing the node.
        quantize_until (str, optional): if provided, limit the search until a node
            whose output matches to it. Defaults to None.

    Returns:
        list: a quantizable sequence of nodes. ``None`` if none found.
    """
    for qpattern in CUSTOM_PATTERNS_MAP + PATTERNS_MAP:
        pattern = qpattern.pattern
        # Try to recognize a sequence of nodes equal to the pattern size
        block_nodes = [node]
        for _ in range(len(pattern) - 1):
            # End search if quantize_until is provided
            if block_nodes[-1].output[0] == quantize_until:
                break
            outbound_nodes = model.get_children(block_nodes[-1])
            # A valid sequence cannot contain multiple outbounds.
            if len(outbound_nodes) != 1:
                break
            # Add outbound in the list of nodes
            block_nodes.extend(outbound_nodes)
        block_id = tuple(node.op_type for node in block_nodes)
        if block_id == pattern:
            # The node search ends because a pattern matchs with block_id.
            # Return all quantized functions that match with the same id.
            target_fn_list = []
            for qpattern in CUSTOM_PATTERNS_MAP + PATTERNS_MAP:
                if qpattern.pattern == block_id:
                    target_fn_list.extend(qpattern.f)
            return block_nodes, target_fn_list


def quantize_calibrated(model, tensors_range, quantize_until=None):
    """
    Given a calibrated onnx model and associated tensor ranges, create a quantized onnx
    model compatible with Brainchip's Akida IP and returns it as a new onnx model.

    Args:
        model: model to quantize
        tensors_range: dictionary of tensor name and its range.
            Range is a tuple of min and max values.
            Example: {"input_0": (-1.23, +4.56)}
        quantize_until (str, optional): quantization is performed until this node.
            Defaults to None.

    Returns:
        quantized onnx model.
    """
    assert isinstance(model, ONNXModel)

    # Reject multi-input models (yet)
    if len(model.input) != 1:
        raise RuntimeError("Only single input models are supported.")
    if quantize_until and not any(node.name == quantize_until for node in model.nodes()):
        raise ValueError(f"'{quantize_until}' is not a recognized node in "
                         f"{model.graph().name}")

    # Rename operations to match with patterns
    graph = model.graph()

    # Copy target model to build a submodel with the remaining nodes (no quantizable)
    # and create an empty ONNXModel to build the new quantized model
    model_name = model.name or "quantized_model"
    qmodel = ONNXModel(onnx.helper.make_model(graph=onnx.GraphProto(name=model_name)))
    qmodel.input.extend(model.input)
    qmodel.set_opset_import(onnx_qlayers.DOMAIN, onnx_qlayers.VERSION)

    # Split nodes in blocks.
    # Note: list(nodes) clone each NodeProto in graph.node field
    remaining_nodes = list(model.nodes())

    # Start with all nodes linked to the input
    node_queue = []
    output_names = []
    qmodel.quantizers = []

    for node in model.nodes():
        if model.get_node_inputs(node) == [graph.input[0].name]:
            node_queue.append(node)
    while len(node_queue) > 0:
        # Process the first node in the queue
        target_node = node_queue.pop(0)
        # Creates a Quantizer if a sequence of nodes is found
        if block_qpattern := search_block_from_node(target_node, model, quantize_until):
            block_nodes, qpattern_func = block_qpattern
            # Each pattern is associated with a list of functions, prioritized by order.
            # The process tries the first function, and if it raises an exception,
            # it moves to the next one.
            error_trace = []
            for qlayer_func in qpattern_func:
                # Reset qlayer to avoid taking values from past iterations
                qlayer = None
                try:
                    # Initialize quantized layer
                    qlayer = qlayer_func(block_nodes, graph)
                    break
                except Exception as e:
                    # Try to quantize block nodes with next func
                    error_trace.append(f"{e.__class__.__name__}: {str(e)}")
                    continue

            if not isinstance(qlayer, onnx_qlayers.OnnxLayer):
                raise RuntimeError(f"Impossible to quantize {block_nodes}: it produces {qlayer} "
                                   f"which is not a valid {onnx_qlayers.OnnxLayer} object. \n"
                                   f"Error trace: \n\t* " + '\n\t* '.join(error_trace))

            # Find out if the inputs were quantized. If not, ignore the sequence
            try:
                qinputs = []
                for x in model.get_node_inputs(target_node):
                    if x == model.input[0].name:
                        # Skip nodes that are linked to inputs (e.g. InputQuantizer)
                        continue
                    quantizer_id = output_names.index(x)
                    qinputs.append(qmodel.quantizers[quantizer_id].qlayer)

            except ValueError:
                continue

            # Create intermediate Quantizer representation
            new_quantizer = Quantizer(qlayer, qinputs, block_nodes[-1].output[0])
            qmodel.quantizers.append(new_quantizer)
            # When quantize_until is provided, exclude output to stop quantization
            # for next nodes
            if new_quantizer.out_name != quantize_until:
                output_names.append(new_quantizer.out_name)
            else:
                output_names.append(None)
            # Remove nodes to be quantized from target model
            for node in block_nodes:
                remaining_nodes.remove(node)
            # Include in the queue the block children
            # Note get_children returns nodes in topological order, therefore a node
            # with multiple inputs will be processed once they have been quantized
            for child_node in model.get_children(block_nodes[-1]):
                if child_node not in node_queue:
                    node_queue.append(child_node)

    # No pattern was found if there is only InputQuantizer in quantizers list
    if len(qmodel.quantizers) <= 1:
        raise RuntimeError("No quantizable pattern found")

    # Compute each remaining input (those whose nodes are disconnected remaining model)
    partial_float_in, _ = infer_partial_io(remaining_nodes,
                                           exclude=list(model.get_initializer_name_set()))

    is_fully_quantized = len(remaining_nodes) == 0
    # Output needs to be dequantized when there are no remaining_nodes
    if is_fully_quantized:
        for node in graph.output:
            partial_float_in.append(node.name)

    apply_last_output_bits = is_fully_quantized and get_quantization_params().last_output_bits

    # Main loop: quantize qlayers and concatenate them in qnodes
    value_info = qmodel.graph().value_info
    for qidx, quantizer in enumerate(qmodel.quantizers):
        last_quantizer = quantizer.out_name in partial_float_in
        # Note downscale is just implemented for QuantizedAdd and QuantizedDense1D
        downscale = not last_quantizer or apply_last_output_bits or \
            isinstance(quantizer.qlayer, tuple(_GLOBAL_REQUIRES_DOWNSCALE))
        # QuantizedAdd constraint: power-of-two input scales are mandatory.
        # In other words, we force output scale to be a power-of-two if target node
        # has at least one QuantizedAdd outbound.
        force_fp = False
        for q in qmodel.quantizers[qidx + 1:]:
            if quantizer.qlayer in q.qinputs:
                force_fp = isinstance(q.qlayer, tuple(_GLOBAL_REQUIRES_FP_INPUTS))
        # Build node previous to quantization in order to assing a custom output name
        # Note that this is not the case for InputQuantizer, since it is a new node in the graph,
        # it must have a new name.
        if not isinstance(quantizer.qlayer, onnx_qlayers.InputQuantizer):
            input_vi = [qi.output for qi in quantizer.qinputs]
            quantizer.qlayer.build(*input_vi, out_name=quantizer.out_name, downscale=downscale)
        # Quantize node to retrieve NodeProto and list of TensorProto (weights)
        out_tensor_ranges = tensors_range[quantizer.out_name]
        qnode, onnx_weights = quantizer.qlayer.quantize(*quantizer.qinputs,
                                                        out_tensor_range=out_tensor_ranges,
                                                        force_fp=force_fp)
        # Include new quantized node into qmodel
        qmodel.add_node(qnode)
        value_info.append(quantizer.qlayer.output)
        if len(onnx_weights) > 0:
            qmodel.initializer_extend(onnx_weights)
        # Update output name list
        output_names[qidx] = qnode.output[0]

    # Add a Dequantizer
    io_deq_map = []
    qlayers = [qmodel.quantizers[output_names.index(iname)].qlayer for iname in partial_float_in]
    dequantizer = onnx_qlayers.Dequantizer(name="dequantizer")
    qnode, onnx_weights = dequantizer.quantize(*qlayers)
    qmodel.add_node(qnode)
    qmodel.initializer_extend(onnx_weights)
    # Make Dequantizer an output of the quantized model and an input of the remaining model
    qmodel.output.extend(dequantizer.output)
    # Save input output map (to merge submodels)
    io_deq_map = [(dequantizer.output[i].name, iname) for i, iname in enumerate(partial_float_in)]
    # Register functions in the quantized graph
    qmodel.model.functions.extend(onnx_qlayers.AKIDA_ONNX_LAYERS)

    # Finally build the quantized model
    if len(remaining_nodes) > 0:
        if quantize_until is None:
            warnings.warn("The following nodes were not quantized because their pattern "
                          "was not found in the scope: "
                          f"{[f'{x.name} ({x.op_type})' for x in remaining_nodes]}.")
        # Extract remaining submodel
        extractor = onnx.utils.Extractor(model.model)
        remaining_model = extractor.extract_model(partial_float_in, [model.output[0].name])
        # merge_models throws an error if it finds value_info name overlap in both models.
        # To avoid it, we give priority to those present in the quantized model.
        for value_info in list(remaining_model.graph.value_info):
            if qmodel.find_value_info_by_name(value_info.name):
                remaining_model.graph.value_info.remove(value_info)
        # Use onnx.compose helper tool to merge the models manually,
        # avoiding some issues (e.g. topological ordering).
        qmodel = onnx.compose.merge_models(qmodel.model, remaining_model, io_map=io_deq_map)
        qmodel = ONNXModel(qmodel)
    return qmodel


def quantize(model,
             qparams=QuantizationParams(),
             samples=None,
             num_samples=1024,
             batch_size=None,
             quantize_until=None):
    """
    Given an onnx model and calibration data reader, create a quantized onnx
    model compatible with Brainchip's Akida IP and returns it as a new onnx model.

    Args:

        model (ModelProto): the onnx model instance to quantize
        qparams (QuantizationParams, optional): Quantization parameters. It is used
            to determine if quantizing per-tensor or per-axis.
        samples (list of numpy arrays, optional): List of input samples to use for
            calibration. If not provided, random samples will be generated. Defaults
            to None.
        num_samples (int, optional): Number of samples to use for calibration.
            Defaults to 1024.
        batch_size (int, optional): Batch size to use for calibration. Defaults to
            None.
        quantize_until (str, optional): name of the node until which to quantize:
            other nodes after it will stay unchanged. Defaults to None.

    Returns:
        quantized onnx model.
    """
    # For now only a limited QuantizationParams configuration is supported: test that
    if (
            qparams.activation_bits != 8 or
            qparams.buffer_bits != 32 or
            qparams.input_weight_bits != 8 or
            qparams.output_bits != 8 or
            qparams.weight_bits != 8):
        raise ValueError("Only default bitwidth qparams is allowed.")
    if qparams.input_dtype not in (np.uint8, np.int8):
        raise ValueError("Only {'uint8', 'int8'} is allowed as input_dtype. Receives: " +
                         str(qparams.input_dtype))
    if qparams.last_output_bits not in (None, 8):
        raise ValueError("Only {None, 8} is allowed as last_output_bits. Receives: " +
                         str(qparams.last_output_bits))

    # Generate node names if needed
    generate_node_names(model)

    # Parse ModelProto into a ONNXModel
    onnx_model = ONNXModel(model)

    # Sanitize the input model
    onnx_model = sanitize(onnx_model)

    # Compute statistical ranges
    tensors_range = calibrate(onnx_model.model,
                              samples,
                              num_samples,
                              batch_size,
                              per_tensor_activations=qparams.per_tensor_activations)

    # Quantize model with tensors_range
    with quantization(qparams):
        qmodel = quantize_calibrated(onnx_model, tensors_range, quantize_until=quantize_until)
    return qmodel.model
