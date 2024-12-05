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
"""
Tools to unfuse SeparableConv2D layers from a model.
"""

__all__ = ["unfuse_sepconv2d"]

from copy import deepcopy

from keras.models import Sequential
from keras.layers import SeparableConv2D
from quantizeml.models.utils import apply_weights_to_model
from quantizeml.models.transforms.transforms_utils import (
    get_layer_index, get_layers_by_type, update_inbound)


def _find_sepconv_layers(model):
    """ Retrieves SeparableConv2D layers.

    Args:
        model (keras.Model): a model

    Returns:
        dict: map between a SeparableConv2D and the layer that follows
    """
    map_sepconv_next = {}

    # Get all SeparableConv2D layers present in the model
    sep_conv_layers = get_layers_by_type(model, SeparableConv2D)

    for sep_conv in sep_conv_layers:
        # Limit support to single inbound/outbound
        outbounds = sep_conv.outbound_nodes
        if len(sep_conv.inbound_nodes) != 1 or len(outbounds) != 1:
            continue

        following_layer = outbounds[0].layer
        # At this point the SeparableConv2D is a valid candidate
        map_sepconv_next[sep_conv] = following_layer

    # Check if the last model layer is a SeparableConv2D if it's the case add it
    # to dict but with None as a special value (to indicate that it has no outbound layer)
    last_layer = model.layers[-1]
    if isinstance(last_layer, SeparableConv2D):
        map_sepconv_next[last_layer] = None
    return map_sepconv_next


def _get_depthwise_conf(sep_layer):
    """ Helper function to unfuse a SeparableConv2D layer. This function returns the
        corresponding DepthwiseConv2D layer configuration and its generated name.

    Args:
        sep_layer (keras.Layer): a keras SeparableConv2D layer

    Returns:
        dict: the DepthwiseConv2D layer configuration
    """
    assert isinstance(sep_layer, SeparableConv2D), ("_get_depthwise_conf accepts only "
                                                    "SeparableConv2D layers. "
                                                    f"Got {type(sep_layer)}")
    dw_name = "dw_" + sep_layer.name
    sep_layer_config = sep_layer.get_config()
    depthwise_initializer = sep_layer_config.get("depthwise_initializer",
                                                 {'class_name': 'GlorotUniform',
                                                  'config': {'seed': None}})
    depthwise_regularizer = sep_layer_config.get("depthwise_regularizer", None)
    depthwise_constraint = sep_layer_config.get("depthwise_constraint", None)

    dw_layer_conf = {'class_name': 'DepthwiseConv2D',
                     'config': {'name': dw_name, 'trainable': sep_layer.trainable,
                                'dtype': sep_layer.dtype,
                                'kernel_size': sep_layer.kernel_size,
                                'strides': sep_layer.strides,
                                'padding': sep_layer.padding, 'data_format': sep_layer.data_format,
                                'dilation_rate': sep_layer.dilation_rate,
                                'groups': sep_layer.groups, 'activation': 'linear',
                                'use_bias': False,
                                'bias_initializer': {'class_name': 'Zeros', 'config': {}},
                                'bias_regularizer': None,
                                'bias_constraint': None,
                                'activity_regularizer': None,
                                'depth_multiplier': sep_layer.depth_multiplier,
                                'depthwise_initializer': depthwise_initializer,
                                'depthwise_regularizer': depthwise_regularizer,
                                'depthwise_constraint': depthwise_constraint}}

    return dw_layer_conf


def _get_pointwise_conf(sep_layer):
    """ Helper function to unfuse a SeparableConv2D layer. This function returns the
        corresponding (pointwise)Conv2D layer configuration and its generated name.

    Args:
        sep_layer (keras.Layer): a keras SeparableConv2D layer

    Returns:
        dict: the (pointwise)Conv2D layer configuration
    """
    assert isinstance(sep_layer, SeparableConv2D), ("_get_pointwise_conf accepts only "
                                                    "SeparableConv2D layers. "
                                                    f"Got {type(sep_layer)}")
    pw_name = "pw_" + sep_layer.name
    sep_layer_config = sep_layer.get_config()
    pointwise_initializer = sep_layer_config.get("pointwise_initializer",
                                                 {'class_name': 'GlorotUniform',
                                                  'config': {'seed': None}})
    pointwise_regularizer = sep_layer_config.get("pointwise_regularizer", None)
    pointwise_constraint = sep_layer_config.get("pointwise_constraint", None)
    bias_initializer = sep_layer_config.get("bias_initializer",
                                            {'class_name': 'Zeros', 'config': {}})
    bias_regularizer = sep_layer_config.get("bias_regularizer", None)
    bias_constraint = sep_layer_config.get("bias_constraint", None)
    activation = sep_layer_config.get("activation", "linear")
    activity_regularizer = sep_layer_config.get("activity_regularizer", None)

    pw_layer_conf = {'class_name': 'Conv2D',
                     'config': {'name': pw_name, 'trainable': sep_layer.trainable,
                                'dtype': sep_layer.dtype, 'filters': sep_layer.filters,
                                'kernel_size': (1, 1), 'strides': (1, 1),
                                'padding': 'same', 'data_format': sep_layer.data_format,
                                'dilation_rate': (1, 1), 'groups': sep_layer.groups,
                                'activation': activation, 'use_bias': sep_layer.use_bias,
                                'kernel_initializer': pointwise_initializer,
                                'bias_initializer': bias_initializer,
                                'kernel_regularizer': pointwise_regularizer,
                                'bias_regularizer': bias_regularizer,
                                'activity_regularizer': activity_regularizer,
                                'kernel_constraint': pointwise_constraint,
                                'bias_constraint': bias_constraint}}

    return pw_layer_conf


def _get_unfused_sepconv_model(model, map_sepconv_layers):
    """Edits the model configuration to unfuse SeparableConv2D layers and rebuilds a model.
    Returns also a dict mapping the new unfused layers variable names with their
    corresponding values (i.e from the main SeparableConv2D layer).

    Args:
        model (keras.Model): a model
        map_sepconv_layers (dict): map between a SeparableConv2D and the layer that follows (None
            if the SeparableConv2D layer is the last model layer)

    Returns:
        tuple (keras.Model, dict): (an updated model with unfused SeparableConv2D layers,
        new layers variables)
    """
    # get_config documentation mentions that a copy should be made when planning to modify the
    # config
    config = deepcopy(model.get_config())
    layers = config['layers']

    # Create an empty dict that will be populated with the new layers variables names
    # and their corresponding values
    sep_layers_vars_dict = {}

    for sep_conv, next_layer in map_sepconv_layers.items():
        # Get the index of the SeparableConv2D layer
        sep_conv_index = get_layer_index(layers, sep_conv.name)

        # Get the original SeparableConv2D layer inbound informations if available
        sep_conv_inbounds_conf = layers[sep_conv_index].get('inbound_nodes', None)

        # Get DepthwiseConv2D conf from the main SeparableConv2D layer
        dw_conf = _get_depthwise_conf(sep_conv)
        # Replace the SeparableConv2D by a DepthwiseConv2D
        layers[sep_conv_index] = dw_conf

        # And insert after it a Conv2D layer (i.e pointwise conv2d)
        pw_conf = _get_pointwise_conf(sep_conv)
        layers.insert(sep_conv_index + 1, pw_conf)

        # Get new layers names
        dw_name = dw_conf['config']['name']
        pw_name = pw_conf['config']['name']
        # Get new layers var names
        dw_kernel_name = dw_name+"/depthwise_kernel:0"
        pw_kernel_name = pw_name+"/kernel:0"
        pw_bias_name = pw_name+"/bias:0"
        # Map new vars with the corresponding ones from the SeparableConv2D layer
        sep_layers_vars_dict[dw_kernel_name] = sep_conv.depthwise_kernel
        sep_layers_vars_dict[pw_kernel_name] = sep_conv.pointwise_kernel
        sep_layers_vars_dict[pw_bias_name] = sep_conv.bias

        # For sequential model, the changes stop here: the SeparableConv2D layers will simply be
        # replaced by an equivalent DepthwiseConv2D + (pointwise)Conv2D layers. For other models,
        # the layers inbounds/outbounds must be rebuilt.
        if isinstance(model, Sequential):
            continue

        # Retrieve the new DepthwiseConv2D index
        dw_layer_index = get_layer_index(layers, dw_name)
        layers[dw_layer_index]['name'] = dw_name
        # Set the new DepthwiseConv2D layer inbounds (those are the main SeparableConv2D inbounds)
        layers[dw_layer_index]['inbound_nodes'] = sep_conv_inbounds_conf

        # Retrieve the new (pointwise)Conv2D index (dw_layer_index + 1)
        pw_layer_index = dw_layer_index + 1
        layers[pw_layer_index]['name'] = pw_name
        # Set the new (pointwise)Conv2D layer inbounds (its the new DepthwiseConv2D layer)
        # tfmot code: 'inbound_nodes' is a nested list where first element is the inbound layername,
        # e.g: [[['conv1', 0, 0, {} ]]]
        layers[pw_layer_index]['inbound_nodes'] = [[[dw_name, 0, 0, {}]]]

        if next_layer:
            # Retrieve the next layer index
            next_layer_index = get_layer_index(layers, next_layer.name)
            # Update the next layer inbound layer (i.e the main SeparableConv2D layer) by the
            # new (pointwise)Conv2D
            update_inbound(layers[next_layer_index], sep_conv.name, pw_name)
        else:
            config['output_layers'] = [[pw_name, 0, 0]]

    # Reconstruct model from the config, using the cloned layers
    return model.from_config(config), sep_layers_vars_dict


def unfuse_sepconv2d(model):
    """ Unfuse the SeparableConv2D layers of a model by replacing them with an equivalent
    DepthwiseConv2D + (pointwise)Conv2D layers.

    Args:
        model (keras.Model): the model to update

    Returns:
        keras.Model: the original model or a new model with unfused SeparableConv2D layers
    """
    # Find SeparableConv2D
    map_sepconv_layers = _find_sepconv_layers(model)

    # When there are no valid candidates, return the original model
    if not map_sepconv_layers:
        return model

    # Rebuild a model with unfused SeparableConv2D by editing the configuration
    updated_model, sep_layers_vars_dict = _get_unfused_sepconv_model(model, map_sepconv_layers)

    # Load original weights
    variables_dict = {}

    for layer in model.layers:
        if not isinstance(layer, SeparableConv2D):
            for var in layer.variables:
                variables_dict[var.name] = var

    variables_dict.update(sep_layers_vars_dict)
    apply_weights_to_model(updated_model, variables_dict, False)

    return updated_model
