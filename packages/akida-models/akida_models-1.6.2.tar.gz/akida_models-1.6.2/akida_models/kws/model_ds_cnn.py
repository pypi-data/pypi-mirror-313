#!/usr/bin/env python
# ******************************************************************************
# Copyright 2020 Brainchip Holdings Ltd.
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
DS-CNN model definition for KWS classification.
"""

__all__ = ["ds_cnn_kws", "ds_cnn_kws_pretrained"]

from keras import Model
from keras.layers import Input, Reshape, Activation, Rescaling

from ..layer_blocks import conv_block, separable_conv_block, dense_block
from ..utils import fetch_file, get_params_by_version
from ..model_io import load_model, get_model_path


def ds_cnn_kws(input_shape=(49, 10, 1), classes=33, include_top=True, input_scaling=(255, 0)):
    """Instantiates a MobileNet-like model for the "Keyword Spotting" example.

    This model is based on the MobileNet architecture, mainly with fewer layers.
    The weights and activations are quantized such that it can be converted into
    an Akida model.

    This architecture is originated from https://arxiv.org/pdf/1711.07128.pdf
    and was created for the "Keyword Spotting" (KWS) or "Speech Commands"
    dataset.

    Note: input preprocessing is included as part of the model (as a Rescaling layer). This model
    expects inputs to be float tensors of pixels with values in the [0, 255] range.

    Args:
        input_shape (tuple, optional): input shape tuple of the model. Defaults to (49, 10, 1).
        classes (int, optional): optional number of classes to classify words into, only
            be specified if `include_top` is True. Defaults to 33.
        include_top (bool, optional): whether to include the classification layer at the top of the
            model. Defaults to True.
        input_scaling (tuple, optional): scale factor and offset to apply to
            inputs. Defaults to (255, 0). Note that following Akida convention,
            the scale factor is an integer used as a divisor.

    Returns:
        keras.Model: a Keras model for MobileNet/KWS
    """
    if include_top and not classes:
        raise ValueError("If 'include_top' is True, 'classes' must be set.")

    # Model version management
    fused, post_relu_gap, relu_activation = get_params_by_version()

    img_input = Input(shape=input_shape, name="input")

    if input_scaling is None:
        x = img_input
    else:
        scale, offset = input_scaling
        x = Rescaling(1. / scale, offset, name="rescaling")(img_input)

    x = conv_block(x,
                   filters=64,
                   kernel_size=(5, 5),
                   padding='same',
                   strides=(2, 2),
                   use_bias=False,
                   name='conv_0',
                   add_batchnorm=True,
                   relu_activation=relu_activation)

    x = separable_conv_block(x,
                             filters=64,
                             kernel_size=(3, 3),
                             padding='same',
                             use_bias=False,
                             name='separable_1',
                             add_batchnorm=True,
                             fused=fused,
                             relu_activation=relu_activation)

    x = separable_conv_block(x,
                             filters=64,
                             kernel_size=(3, 3),
                             padding='same',
                             use_bias=False,
                             name='separable_2',
                             add_batchnorm=True,
                             fused=fused,
                             relu_activation=relu_activation)

    x = separable_conv_block(x,
                             filters=64,
                             kernel_size=(3, 3),
                             padding='same',
                             use_bias=False,
                             name='separable_3',
                             add_batchnorm=True,
                             fused=fused,
                             relu_activation=relu_activation)

    x = separable_conv_block(x,
                             filters=64,
                             kernel_size=(3, 3),
                             padding='same',
                             use_bias=False,
                             name='separable_4',
                             pooling='global_avg',
                             add_batchnorm=True,
                             fused=fused,
                             post_relu_gap=post_relu_gap,
                             relu_activation=relu_activation)

    if include_top:
        x = dense_block(x,
                        units=classes,
                        name='dense_5',
                        use_bias=True,
                        relu_activation=False)
        act_function = 'softmax' if classes > 1 else 'sigmoid'
        x = Activation(act_function, name=f'act_{act_function}')(x)
    else:
        shape = (1, 1, int(64))
        x = Reshape(shape, name='reshape_1')(x)

    return Model(img_input, x, name='ds_cnn_kws')


def ds_cnn_kws_pretrained(quantized=True):
    """
    Helper method to retrieve a `ds_cnn_kws` model that was trained on
    KWS dataset.

    Args:
        quantized (bool, optional): a boolean indicating whether the model should be loaded
            quantized or not. Defaults to True.

    Returns:
        keras.Model: a Keras Model instance.

    """
    if quantized:
        model_name_v1 = 'ds_cnn_kws_iq8_wq4_aq4_laq1.h5'
        file_hash_v1 = '2ba6220bb9545857c99a327ec14d2d777420c7848cb6a9b17d87e5a01951fe6f'
        model_name_v2 = 'ds_cnn_kws_i8_w8_a8.h5'
        file_hash_v2 = '5b7c9e7b6016cef67a0c048bbbfbfc0590f0ec7af17879956234fb97cc774435'
    else:
        model_name_v1 = 'ds_cnn_kws.h5'
        file_hash_v1 = '95a51677b340ee2420015a8576a8aaf41e84138ac0334cd42080b60499b4f146'
        model_name_v2 = 'ds_cnn_kws.h5'
        file_hash_v2 = 'e897da2760206aad1328179c2b6861bae4f0e56a9380c78cf1287d18929a2143'

    model_path, model_name, file_hash = get_model_path("ds_cnn", model_name_v1, file_hash_v1,
                                                       model_name_v2, file_hash_v2)
    model_path = fetch_file(model_path,
                            fname=model_name,
                            file_hash=file_hash,
                            cache_subdir='models')
    return load_model(model_path)
