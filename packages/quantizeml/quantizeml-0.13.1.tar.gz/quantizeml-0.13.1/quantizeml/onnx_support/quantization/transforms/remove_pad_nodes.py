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
__all__ = ['fold_pad_into_conv']

from ...graph_tools import get_field, replace_field, has_field, to_field
from ..model import ONNXModel


def fold_pad_into_conv(model):
    assert isinstance(model, ONNXModel)
    pre_msg_erro = "Impossible to fold {} into {}: "

    for tnode in model.nodes()[1:]:
        if tnode.op_type != 'Conv':
            continue
        pnode = model.get_parent(tnode, idx=0)
        if pnode is not None and pnode.op_type == 'Pad':
            # Pad node should have only one non initializer
            if len(model.get_node_inputs(pnode)) > 1:
                continue

            # Raise exception if pad has multiple outbounds
            node_outbounds = model.get_children(pnode)
            if len(node_outbounds) != 1:
                raise RuntimeError(pre_msg_erro.format(pnode.name, tnode.name) +
                                   f"Single outbound is required for {pnode.name} " +
                                   f"(found {[x.name for x in node_outbounds]}.")

            # Check valid model
            mode = get_field(pnode, "mode", "constant")
            if mode != "constant":
                raise RuntimeError(pre_msg_erro.format(pnode.name, tnode.name) +
                                   f"Unsupported '{mode}' mode.")

            # Check valid constant value
            if len(pnode.input) > 2 and pnode.input[2]:
                constant_value = model.get_variable(pnode.input[2])
                if constant_value != 0:
                    raise RuntimeError(pre_msg_erro.format(pnode.name, tnode.name) +
                                       "Constant value is not zero.")

            # Input rank in a 'Conv' is the same as kernel one
            input_ndim = model.get_variable(tnode.input[1]).ndim

            # Retrieve pad_pads and axes (if any)
            pad_pads = model.get_variable(pnode.input[1]).tolist()
            if len(pnode.input) > 3 and pnode.input[3]:
                axes = model.get_variable(pnode.input[3])
                axes = [x if x >= 0 else input_ndim + x for x in axes]
            else:
                axes = list(range(input_ndim))

            # Fulfill pad_pads in every dimension (filling with zero the other ones)
            for axis in range(input_ndim):
                if axis not in axes:
                    pad_len = len(pad_pads) // 2
                    pad_pads.insert(pad_len + axis, 0)
                    pad_pads.insert(axis, 0)

            # Check pad only in spatial dimensions
            if any(pad_pads[:2] + pad_pads[input_ndim:input_ndim + 2]):
                raise RuntimeError(pre_msg_erro.format(pnode.name, tnode.name) +
                                   "Pad has non-zero values on batch or channel dimension.")
            # Get only spatial pads
            new_pads = pad_pads[2:input_ndim] + pad_pads[input_ndim + 2:]

            # Replace conv pads = new + old
            if has_field(tnode, "pads"):
                target_pads = get_field(tnode, "pads", [0] * 2 * (input_ndim - 2))
                replace_field(tnode, "pads", [x + y for x, y in zip(target_pads, new_pads)])
            else:
                new_pads_attr = to_field("pads", new_pads)
                tnode.attribute.append(new_pads_attr)

            # Prune node
            model.remove_node(pnode, update_graph=True)

    # Clean graph, removing pointless initializers
    model.clean_initializers()
    model.check_model()
