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
CenterNet model definition for detection
"""

__all__ = ["centernet_base", "centernet_voc_pretrained"]

import numpy as np

from keras import Model, initializers
from keras.layers import Conv2D, Add

from cnn2snn import set_akida_version, AkidaVersion

from .. import akidanet18_imagenet
from ..layer_blocks import (separable_conv_block, conv_block, conv_transpose_block,
                            sepconv_transpose_block)
from ..utils import fetch_file
from ..model_io import load_model, get_model_path
from ..imagenet.imagenet_train import rescale


def centernet_base(input_shape=(384, 384, 3),
                   classes=20,
                   input_scaling=(127, -1),
                   separable_cutoff=64):
    """ A Keras Model implementing the CenterNet architecture, on top of an AkidaNet backbone

    Args:
        input_shape (tuple, optional): input shape. Defaults to (384, 384, 3).
        classes (int, optional): number of output classes. Defaults to 20.
        input_scaling (tuple, optional): input scaling. Defaults to (127, -1).
        separable_cutoff (int, optional): maximum number of filters for standard Conv layers.
            Layers with more filters than this will be defined as separable Convs. Defaults to 64.

    Returns:
        keras.Model: a Keras Model instance.
    """
    def _build_backbone():
        base_model = akidanet18_imagenet(input_shape=input_shape,
                                         include_top=False,
                                         pooling="avg",
                                         input_scaling=input_scaling)
        # Last three layers immediately prior to stride-2 layers.
        # And a final layer, immediately prior to the GAP pooling op
        outputs_layer_names = ['stage_0/conv_3/relu', 'stage_1/conv_3/relu',
                               'pw_stage_2/conv_3/relu', 'pw_stage_3/conv_3/relu']

        outputs = [base_model.get_layer(name=name).output for name in outputs_layer_names]
        backbone = Model(inputs=base_model.inputs, outputs=outputs)
        return backbone

    def _get_block_params(n_filt, separable_cutoff):
        if n_filt <= separable_cutoff:
            neck_convs_ks = (3, 3)
            curr_block = conv_block
            block_type = "conv"
            transpose_block = conv_transpose_block
            kwargs = {}
        else:
            neck_convs_ks = (5, 5)
            curr_block = separable_conv_block
            block_type = "sepconv"
            transpose_block = sepconv_transpose_block
            kwargs = {"fused": False}
        return neck_convs_ks, curr_block, block_type, transpose_block, kwargs

    # This model is only available for Akida 2.0
    with set_akida_version(AkidaVersion.v2):
        # Create an AkidaNet network without top layers
        backbone = _build_backbone()

        # Rescale the backbone input shape
        if backbone.input.shape[1] != input_shape[0] or backbone.input.shape[2] != input_shape[1]:
            backbone = rescale(backbone, [input_shape[0], input_shape[1]])

        # Extract skip connections
        skips = backbone.output[::-1][1:]
        num_deconv_filters = [skip.shape[-1] for skip in skips]
        x = backbone.output[-1]

        for i, (n_filt) in enumerate(num_deconv_filters):
            neck_convs_ks, curr_block, block_type, transpose_block, kwargs = \
                _get_block_params(n_filt, separable_cutoff)

            x = curr_block(x,
                           filters=n_filt,
                           name=f'neck_{block_type}_{i}',
                           kernel_size=neck_convs_ks,
                           padding='same',
                           use_bias=False,
                           relu_activation='ReLU7.5',
                           add_batchnorm=True,
                           **kwargs)

            x = transpose_block(x,
                                filters=n_filt,
                                name=f"neck_transpose_{block_type}_{i}",
                                kernel_size=(4, 4),
                                padding="same",
                                strides=(2, 2),
                                use_bias=False,
                                relu_activation='ReLU7.5',
                                add_batchnorm=True)
            x = Add(name=f"neck_add_{i}")([x, skips[i]])

        # Build the head which is composed of 2 consecutive convs
        bias_initializer = initializers.Constant(float(-np.log((1 - 0.1) / 0.1)))
        init_kernel = initializers.RandomNormal(stddev=0.001, seed=6)
        # In the legacy model there is 3 branches of 64 filters each one.
        # This could be merged in one branch
        x = conv_block(x, 3 * 64, (3, 3),
                       add_batchnorm=True,
                       use_bias=False,
                       relu_activation='ReLU7.5',
                       padding="same",
                       name="head_conv_1",
                       kernel_initializer=init_kernel)
        # The output is built by #classes and box coordinates in xywh
        x = Conv2D(classes + 4,
                   (1, 1),
                   padding="same",
                   use_bias=True,
                   name="head_conv_2",
                   bias_initializer=bias_initializer,
                   kernel_initializer=init_kernel)(x)

    # Build the model
    return Model(inputs=backbone.input, outputs=x, name='centernet_base')


def centernet_voc_pretrained(quantized=True):
    """
    Helper method to retrieve an `centernet_base` model that was trained on VOC detection dataset.

    Args:
        quantized (bool, optional): a boolean indicating whether the model should be loaded
            quantized or not. Defaults to True.

    Returns:
        keras.Model: a Keras Model instance.

    """
    if quantized:
        model_name_v2 = 'centernet_akidanet18_voc_384_i8_w8_a8.h5'
        file_hash_v2 = 'cae0f8f36b2d8d01d6049f03185c05d5a9eb3deed47516f7968dc91bb051d81e'
    else:
        model_name_v2 = 'centernet_akidanet18_voc_384.h5'
        file_hash_v2 = '64f220a63aacf653bd672804a5500f98a8dda06029cbe58d327413c9edd4a12f'

    model_path, model_name, file_hash = get_model_path("centernet", model_name_v2=model_name_v2,
                                                       file_hash_v2=file_hash_v2)
    model_path = fetch_file(model_path, fname=model_name, file_hash=file_hash,
                            cache_subdir='models')
    return load_model(model_path)
