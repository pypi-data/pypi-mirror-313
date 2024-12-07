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
__all__ = ["plot_kernel_distribution"]

import os
import matplotlib.pyplot as plt

import onnx
from tensorboardX import SummaryWriter
from keras.layers import DepthwiseConv2D

from ..models import record_quantization_variables
from ..layers.layers_base import QuantizedLayer, WeightQuantizer
from ..models.transforms import sanitize as keras_sanitize
from ..onnx_support.quantization import ONNXModel
from ..onnx_support.quantization.transforms import sanitize as onnx_sanitize


def _plot_kernel_distribution_on_writer(writer, layer_name, kernel):
    kernel = kernel.reshape((kernel.shape[0], -1) if kernel.ndim > 1 else (1, -1))
    for idx, k in enumerate(kernel):
        writer.add_histogram(f"histograms/{layer_name}", k, idx)

    # Boxplot
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(16, 9))
    ax.boxplot(kernel.transpose(),
               patch_artist=True,
               vert=True,
               notch=True,
               boxprops={"facecolor": "orange"},
               medianprops={"color": "gray", "linewidth": 1.5},
               labels=[f"k{x}" for x in range(kernel.shape[0])])

    # Increase figure dpi and reduce pad layout
    fig.set_dpi(300)
    fig.tight_layout()
    writer.add_figure(f"boxplots/{layer_name}", figure=fig)


def _plot_onnx_kernel_distribution(model, logdir):
    def _get_kernel_name(node):
        skip_qnodes = ("QuantizedAdd", "InputQuantizer", "Dequantizer")
        if node.domain == "com.brainchip" and not any(sn in node.op_type for sn in skip_qnodes):
            # kernel in InputQuantizedConv is moved to position 2
            return node.input[1] if "InputConv" not in node.op_type else node.input[2]
        elif node.op_type in ("Conv", "Gemm"):
            return node.input[1]
        return None

    model = onnx_sanitize(model)
    logdir = os.path.join(logdir, model.name or "model")
    with SummaryWriter(log_dir=logdir) as writer:
        for idx, node in enumerate(model.nodes()):
            if (kernel_name := _get_kernel_name(node)):
                kernel = model.get_variable(kernel_name)
                # Unlike Keras, ONNX does not require nodes to be named.
                # In that case, we group the graphs by their id
                _plot_kernel_distribution_on_writer(writer, node.name or f"node_{idx}", kernel)


def _plot_keras_kernel_distribution(model, logdir):
    model = keras_sanitize(model)
    record_quantization_variables(model)
    logdir = os.path.join(logdir, model.name or "model")
    with SummaryWriter(log_dir=logdir) as writer:
        for layer in model.layers:
            weights = layer.get_weights()
            if len(weights) > 0:
                if isinstance(layer, QuantizedLayer):
                    # Search WeightQuantizer in layer
                    weights = None
                    for attr in layer.__dict__.values():
                        if isinstance(attr, WeightQuantizer):
                            # Replace weights by its quantized version
                            weights = [attr.qweights.value.values.numpy()]
                            break
                    # Skip quantized layer if it does not have a WeightQuantizer
                    if weights is None:
                        continue
                weights = weights[0]
                if weights.ndim >= 2:
                    # Weights are formartted as ONNX
                    list_axis = list(range(weights.ndim - 2))
                    if not isinstance(layer, DepthwiseConv2D):
                        weights = weights.transpose((-1, -2, *list_axis))
                    else:
                        # Axis (0,1) should be exchanged if layer is a DepthwiseConv2D
                        weights = weights.transpose((-2, -1, *list_axis))
                _plot_kernel_distribution_on_writer(writer, layer.name, weights)


def plot_kernel_distribution(model, logdir):
    """Plot the kernel distribution of each layer/node in the model.

    Distributions are plotted in two ways: histogram and boxplot

    After exporting them, the plots can be plotted through the command-line:

    >>> tensorboard --logdir=`logdir`

    Args:
        model (onnx.ModelProto or tf.keras.Model): the model to plot the kernel distribution
        logdir (str): the directory to save the plots
    """
    if isinstance(model, onnx.ModelProto):
        _plot_onnx_kernel_distribution(ONNXModel(model), logdir)
    else:
        _plot_keras_kernel_distribution(model, logdir)
    print(f"[INFO] Plots were saved on '{logdir}' successfully. They are available through "
          f"the command-line:\n>>> tensorboard --logdir={logdir}")
