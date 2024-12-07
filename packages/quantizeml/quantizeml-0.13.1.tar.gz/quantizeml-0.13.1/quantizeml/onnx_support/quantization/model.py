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
__all__ = ['ONNXModel']

import warnings

import onnx
import onnx.numpy_helper
import onnx.version_converter
from onnxruntime.quantization.onnx_model import ONNXModel as Model

from ..graph_tools import get_tensor_shape, get_tensor_dtype, find_value_info_by_name


class ONNXModel(Model):
    """Interface with some tools to handle ``onnx.ModelProto`` objects

    Args:
        Model (``onnx.ModelProto`): the base model
    """

    def __init__(self, model):
        super().__init__(model)
        self.check_model()

    @property
    def name(self):
        return self.model.graph.name

    @property
    def input(self):
        return self.model.graph.input

    @property
    def output(self):
        return self.model.graph.output

    @property
    def op_type_nodes(self):
        return tuple(x.op_type for x in self.nodes())

    @property
    def serialized(self):
        return self.model.SerializeToString()

    def check_model(self):
        """Check the consistency of a model.

        An exception is raised if the test fails.
        """
        onnx.checker.check_model(self.model, full_check=True)

    def clean_graph_io(self):
        # Remove the 'inputs' and 'outputs' that are contained in initializer graph field:
        # these are constants and may not be considered as inputs/outputs of the graph
        for value_info in self.input[:]:
            initializer = self.get_initializer(value_info.name)
            if initializer is not None:
                self.input.remove(value_info)

        for value_info in self.output[:]:
            initializer = self.get_initializer(value_info.name)
            if initializer is not None:
                self.output.remove(value_info)

    def update_model_version(self):
        # Try to replace the ONNX version in the graph with the current one
        version = onnx.defs.onnx_opset_version()
        try:
            self.model = onnx.version_converter.convert_version(self.model, target_version=version)
        except Exception as e:
            warnings.warn(f"Impossible to convert model in version {version}. The model may not be "
                          f"compatible with the quantization pipeline. Reason: \n{str(e)}")

        # Once the opset has been updated, IR_VERSION should be compatible with the latest version.
        self.model.ir_version = onnx.IR_VERSION

    def clone(self):
        model = onnx.ModelProto()
        model.CopyFrom(self.model)
        return ONNXModel(model)

    def get_variable(self, name):
        """Helper to get the value of an initializar as np.array.

        Args:
            name (str): the name of the variable.

        Returns:
            np.array: the value of the variable.
        """
        initializer = self.get_initializer(name)
        assert initializer, f"'{name}' was not found in initializer field."
        return onnx.numpy_helper.to_array(initializer)

    def get_input_shape(self, input_name=None):
        """Read the input shape(s) in the graph.

        Args:
            tensor_name (str, optional): return the shape only for this tensor. Defaults to None.

        Returns:
            dict or tuple: the shape of each input in the graph
        """
        if input_name is not None:
            input_value_info = self.find_value_info_by_name(input_name)
            assert input_value_info, f"{input_name} does not exist in the graph inputs."
            return get_tensor_shape(input_value_info)
        return {x.name: get_tensor_shape(x) for x in self.input}

    def get_input_dtype(self, input_name=None):
        """Read the input type(s) in the graph.

        Args:
            tensor_name (str, optional): return the type only for this tensor. Defaults to None.

        Returns:
            dict or np.ndarray: the type of each input in the graph
        """
        if input_name is not None:
            input_value_info = self.find_value_info_by_name(input_name)
            assert input_value_info, f"{input_name} does not exist in the graph inputs."
            return get_tensor_dtype(input_value_info)
        return {x.name: get_tensor_dtype(x) for x in self.input}

    def find_node_by_name(self, node_name):
        """Find a node by its name in the graph

        Args:
            node_name (str): the node name

        Returns:
            NodeProto: the node found
        """
        return super().find_node_by_name(node_name, [], self.graph())

    def find_value_info_by_name(self, tensor_name):
        """Return a value info by its name

        Args:
            tensor_name (str): the tensor name

        Returns:
            NodeProto: the node found
        """
        return find_value_info_by_name(self.graph(), tensor_name)

    def get_node_inputs(self, node):
        """Return the set of non initializer inputs in a node

        Args:
            node (NodeProto): the node to extract the inputs

        Returns:
            list: the non initializer inputs
        """
        initializer_names = self.get_initializer_name_set()
        non_initializer_inputs = []
        for input in node.input:
            # check input is not an initializer and it's not empty (e.g. '')
            if input not in initializer_names and len(input) > 0:
                non_initializer_inputs.append(input)
        return non_initializer_inputs

    def _clear_node_initializers(self, node):
        initializers_to_remove = []

        for input_name in node.input:
            initializer = self.get_initializer(input_name)
            if initializer and len(self.find_nodes_by_initializer(self.graph(), initializer)) == 1:
                initializers_to_remove.append(initializer)

        self.remove_initializers(initializers_to_remove)

    def _remove_node_metadata(self, node_to_remove):
        # Case for skip connections
        non_initializer_inputs = self.get_node_inputs(node_to_remove)

        if len(non_initializer_inputs) > 1:
            raise ValueError(
                f"Cannot remove node {node_to_remove.name} ({node_to_remove.op_type}) as it has "
                f"more than one non-initializer input."
            )

        target_value_info = self.find_value_info_by_name(node_to_remove.output[0])

        # Case where node_to_remove is the last node
        if target_value_info in self.output:
            # Rename graph output name. In this case, the value info is the graph output
            target_value_info.name = node_to_remove.input[0]

        else:
            # Update the input connections of subsequent nodes to bypass node_to_remove
            self.replace_input_of_all_nodes(node_to_remove.output[0], node_to_remove.input[0])
            self._clear_node_initializers(node_to_remove)

            # Remove node_to_remove output value info
            if target_value_info is not None:
                self.graph().value_info.remove(target_value_info)

    def remove_node(self, node_to_remove, update_graph=False):
        """
        Removes a specified node from the ONNX model's graph and optionally updates the graph.

        Args:
            node_to_remove (NodeProto): The node object to be removed from the graph.
            update_graph (bool, optional): If True, the graph's structure will be updated to handle
                the removal by adjusting the outbound inputs. Defaults to False.
        """
        if update_graph:
            self._remove_node_metadata(node_to_remove)
        super().remove_node(node_to_remove)

    def remove_nodes(self, nodes_to_remove, update_graph=False):
        """
        Removes a list of specified nodes from the ONNX model's graph
        and optionally updates the graph.

        Args:
            nodes_to_remove (list): A list of node objects to be removed from the graph.
            update_graph (bool, optional): If True, the graph's structure will be updated to handle
                the removal by adjusting the outbound inputs. Defaults to False.
        """
        for node in nodes_to_remove:
            self.remove_node(node, update_graph)
