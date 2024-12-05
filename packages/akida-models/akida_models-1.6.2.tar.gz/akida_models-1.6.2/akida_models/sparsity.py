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
import tensorflow as tf

from .model_io import load_model
import akida
from tensorflow.keras import Model

from akida.core import LayerType, Model as ak_model

import onnxruntime
from onnx import ModelProto
from quantizeml.onnx_support.quantization.quantize import ONNXModel
from quantizeml.onnx_support.quantization.transforms import sanitize
from quantizeml.onnx_support.graph_tools import value_info_to_tensor_shape
from quantizeml.random import generate_np_random_samples


def display_sparsity(model_path, layer_names=None, layer_types=None,
                     samples_path=None, batch_size=100, verbose=True):
    """Compute the sparsity of a model across selected layers and samples.

    This function loads a model from the specified path and computes the sparsity for specified
    layers (if not specified, ReLU layers for float models, layers with OutputQuantizer for
    quantized models, all layers for akida models and Clip and ReLU nodes for ONNX models) using
    input samples.

    Args:
        model_path (str): Path to the model file.
        layer_names (list, optional): List of layer names to compute sparsity for. If None,
            sparsity is computed for relevant layers. Defaults to None.
        layer_types (tuple, optional): The types of layers for which sparsity will be computed.
            layer_types is a tuple of type when display_sparsity is applied on keras or akida
            models, and a tuple of str when applied on onnx models. Defaults to None.
        samples_path (str, optional): Path to the dataset (e.g., a .npz file containing data).
            If None, sparsity is computed with randomly generated samples. Defaults to None.
        batch_size (int, optional): The number of tensors to generate or extract. Defaults to 100.
        verbose (bool, optional): Whether to print detailed sparsity results for each layer.

    Raises:
        Exception: If the model cannot be loaded or an unsupported model format is provided.
    """
    if layer_names and layer_types:
        raise ValueError(
            "It is not possible to request both options, " +
            "either provide layer_names or layer_types parameter.")

    model = load_model(model_path, compile_model=False)

    if isinstance(model, Model):
        samples_shape = model.input_shape[1:]
        dtype = model.dtype

    elif isinstance(model, ak_model):
        samples_shape = tuple(model.input_shape)
        first_layer = model.layers[0]
        if first_layer.parameters.layer_type == akida.LayerType.InputData:
            dtype = "int" if first_layer.output_signed else "uint"
            dtype += f"{np.ceil(first_layer.input_bits/8)*8:.0f}"
            dtype = np.dtype(dtype)
        else:
            dtype = np.uint8

    elif isinstance(model, ModelProto):
        model = ONNXModel(model)
        samples_shape, dtype = value_info_to_tensor_shape(model.input[0])
        samples_shape = samples_shape[1:]

    else:
        raise NotImplementedError("Sparsity computation is only " +
                                  "supported for Keras and Akida and ONNX models.")

    if samples_path:
        array = np.load(samples_path)['data']
        if batch_size > len(array):
            raise ValueError("Batch size exceeds the available number " +
                             "of tensors in the dataset.")
        samples = array[:batch_size, ...].astype(dtype)
    else:
        samples = generate_np_random_samples(size=(batch_size,) + samples_shape, dtype=dtype)

    if isinstance(model, Model):
        results = _compute_sparsity_tf(model=model,
                                       layer_names=layer_names,
                                       layer_types=layer_types,
                                       samples=samples)
    elif isinstance(model, ak_model):
        results = _compute_sparsity_ak(model=model,
                                       layer_names=layer_names,
                                       layer_types=layer_types,
                                       samples=samples)
    elif isinstance(model, ONNXModel):
        results = _compute_sparsity_onnx(model=model,
                                         node_names=layer_names,
                                         node_types=layer_types,
                                         samples=samples)

    if verbose:
        for layer, sparsity in results.items():
            print(f"{layer} : {float(f'{sparsity:.3f}')}")
    print(f'Mean sparsity : {np.mean(list(results.values()))}')


def _compute_sparsity_tf(model, samples, layer_names=None, layer_types=None):
    """Compute the sparsity of selected layers in a TensorFlow model.

    This function calculates the sparsity (proportion of zero-valued elements)
    in specific layers of a TensorFlow model across a set of input samples.
    If layer names are provided, it computes sparsity for those layers, otherwise,
    it computes sparsity for all ReLU layers or layers with an OutputQuantizer.

    Args:
        model (tf.keras.Model): The TensorFlow model to analyze.
        samples (list): List of input samples to evaluate sparsity on.
        layer_names (list, optional): List of layer names to compute sparsity for. Defaults to None.
        layer_types (tuple of type, optional): The types of layers for which sparsity will be
            computed. Defaults to None. If None, it will compute sparsity for all ReLU or
            QuantizedReLU layers.

    Returns:
        dict: A dictionary where keys are layer names
            and values are the computed sparsity values.
    """
    outputs = []
    results = {}

    if layer_names:
        target_layers = [layer for layer in model.layers if layer.name in layer_names]
    elif layer_types:
        target_layers = [layer for layer in model.layers if isinstance(layer, layer_types)]
    else:
        target_layers = [layer for layer in model.layers
                         if isinstance(layer, tf.keras.layers.ReLU) or
                         hasattr(layer, 'out_quantizer') and layer.out_quantizer]

    if target_layers == []:
        raise ValueError("No layers found to compute the sparsity")

    for layer in target_layers:
        outputs.append(layer.output)

    new_model = Model(inputs=model.inputs, outputs=outputs, name="sparsity")

    all_outputs = new_model(samples)

    # If there is only one tensor in `target_layers`, wrap `all_outputs` in a list
    # to ensure `all_outputs` is always a list
    if len(target_layers) == 1:
        all_outputs = [all_outputs]
    for layer, out in zip(target_layers, all_outputs):
        if isinstance(out, tf.Tensor):
            results[layer.name] = np.sum(out == 0) / np.prod(out.shape)
        else:  # out is a FixedPoint or QTensor
            results[layer.name] = np.sum(out.values == 0) / np.prod(out.shape)

    return results


def _compute_sparsity_ak(model, samples, layer_names=None, layer_types=None):
    """Compute the sparsity of selected layers in an Akida model.

    This function calculates the sparsity (proportion of zero-valued elements)
    for specific layers in an Akida model by running forward passes on input samples.
    If layer names are provided, it computes sparsity for those layers; otherwise,
    it computes sparsity for all layers that have activation functions, excluding
    input and dequantizer layers.

    Args:
        model (akida.Model): The Akida model to analyze.
        samples (numpy.ndarray): Input samples to evaluate sparsity on.
        layer_names (list, optional): List of layer names to compute sparsity for. Defaults to None.
        layer_types (tuple of type, optional): The types of layers for which sparsity will be
            computed. Defaults to None. If None, sparsity is computed for all applicable layers
            with activations.

    Returns:
        dict: A dictionary where keys are layer names and values
            are the computed sparsity values.
    """
    results = {}

    if layer_names:
        target_layers = [layer for layer in model.layers if layer.name in layer_names]
    elif layer_types:
        target_layers = [layer for layer in model.layers
                         if layer.parameters.layer_type in layer_types]
    else:
        target_layers = [layer for layer in model.layers
                         if layer.parameters.layer_type not in (LayerType.InputData,
                                                                LayerType.Dequantizer)]

    if target_layers == []:
        raise ValueError("No layers found to compute the sparsity")

    for layer in target_layers:
        ind = model.layers.index(layer)
        sub_model = akida.Model(layers=model.layers[:ind + 1])
        output = sub_model.forward(samples)
        results[layer.name] = np.count_nonzero(output == 0) / np.prod(output.shape)

    return results


def _compute_sparsity_onnx(model, samples, node_names=None, node_types=None):
    """Compute the sparsity of selected nodes in an ONNX model.

    This function calculates the sparsity (proportion of zero-valued elements)
    for specific nodes in an ONNX model by running forward passes on input samples.
    If node names are provided, it computes sparsity for those nodes; otherwise,
    it computes sparsity for Clip and ReLU nodes.

    Args:
        model (onnx.ModelProto): The ONNX model to analyze.
        samples (numpy.ndarray): Input samples to evaluate sparsity on.
        node_names (list, optional): List of node names to compute sparsity for. Defautls to None.
        node_types (tuple of str, optional): The types of nodes for which sparsity will be computed.
            Defaults to None. If None, sparsity is computed for Clip and ReLU nodes.

    Returns:
        dict: A dictionary where keys are node names and values
            are the computed sparsity values.
    """
    is_quantized = any(node.domain == "com.brainchip" for node in model.nodes())
    if not is_quantized:
        model = sanitize(model)
    if node_types:
        target_nodes = [node for node in model.nodes() if node.op_type in node_types]
    elif is_quantized:
        target_nodes = [node for node in model.nodes() if node.op_type not in ("InputQuantizer",
                                                                               "Dequantizer")]
    else:
        target_nodes = [node for node in model.nodes() if node.op_type in ["Relu", "Clip"]]
    if node_names:
        target_nodes = [node for node in target_nodes if node.name in node_names]

    if len(target_nodes) == 0:
        raise ValueError("No nodes found to compute the sparsity")

    # Create an intermediate model with the inputs of target_nodes
    model.graph().ClearField("output")
    out_names = []
    for node in target_nodes:
        for oname in node.output:
            vi = model.find_value_info_by_name(oname)
            if vi is not None:
                model.output.append(vi)
                out_names.append(vi.name)

    samples_dict = {}
    samples_dict[model.input[0].name] = samples
    outputs = onnxruntime.InferenceSession(model.serialized).run(out_names, samples_dict)
    # Compute sparsity per node
    results = {}
    for node, output in zip(target_nodes, outputs):
        results[node.name] = np.count_nonzero(output == 0) / np.prod(output.shape)

    return results
