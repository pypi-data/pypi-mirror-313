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
VGG model definition for UTKFace regression.
"""

__all__ = ["vgg_utk_face", "vgg_utk_face_pretrained"]

from keras import Model
from keras.layers import Dropout, Input, Rescaling

from ..layer_blocks import conv_block, dense_block
from ..utils import fetch_file, get_params_by_version
from ..model_io import load_model, get_model_path


def vgg_utk_face(input_shape=(32, 32, 3), input_scaling=(127, -1)):
    """Instantiates a VGG-like model for the regression example on age
    estimation using UTKFace dataset.

    Note: input preprocessing is included as part of the model (as a Rescaling layer). This model
    expects inputs to be float tensors of pixels with values in the [0, 255] range.

    Args:
        input_shape (tuple, optional): input shape tuple of the model. Defaults to (32, 32, 3).
        input_scaling (tuple, optional): scale factor and offset to apply to
            inputs. Defaults to (127, -1). Note that following Akida convention,
            the scale factor is an integer used as a divisor.

    Returns:
        keras.Model: a Keras model for VGG/UTKFace
    """
    img_input = Input(shape=input_shape, name="input")

    if input_scaling is None:
        x = img_input
    else:
        scale, offset = input_scaling
        x = Rescaling(1. / scale, offset, name="rescaling")(img_input)

    # Model version management
    _, post_relu_gap, relu_activation = get_params_by_version()

    x = conv_block(x,
                   filters=32,
                   kernel_size=(3, 3),
                   name='conv_0',
                   use_bias=False,
                   relu_activation=relu_activation,
                   add_batchnorm=True)

    x = conv_block(x,
                   filters=32,
                   kernel_size=(3, 3),
                   name='conv_1',
                   padding='same',
                   pooling='max',
                   pool_size=2,
                   use_bias=False,
                   relu_activation=relu_activation,
                   add_batchnorm=True)

    x = Dropout(0.3, name="dropout_3")(x)

    x = conv_block(x,
                   filters=64,
                   kernel_size=(3, 3),
                   padding='same',
                   name='conv_2',
                   use_bias=False,
                   relu_activation=relu_activation,
                   add_batchnorm=True)

    x = conv_block(x,
                   filters=64,
                   kernel_size=(3, 3),
                   padding='same',
                   name='conv_3',
                   pooling='max',
                   pool_size=2,
                   use_bias=False,
                   relu_activation=relu_activation,
                   add_batchnorm=True)

    x = Dropout(0.3, name="dropout_4")(x)

    x = conv_block(x,
                   filters=84,
                   kernel_size=(3, 3),
                   padding='same',
                   name='conv_4',
                   use_bias=False,
                   relu_activation=relu_activation,
                   pooling='global_avg',
                   post_relu_gap=post_relu_gap,
                   add_batchnorm=True)

    x = Dropout(0.3, name="dropout_5")(x)

    x = dense_block(x,
                    units=64,
                    name='dense_1',
                    use_bias=False,
                    relu_activation=relu_activation,
                    add_batchnorm=True)

    x = dense_block(x, units=1, name='dense_2', relu_activation=False)

    return Model(img_input, x, name='vgg_utk_face')


def vgg_utk_face_pretrained(quantized=True):
    """
    Helper method to retrieve a `vgg_utk_face` model that was trained on
    UTK Face dataset.

    Args:
        quantized (bool, optional): a boolean indicating whether the model should be loaded
            quantized or not. Defaults to True.

    Returns:
        keras.Model: a Keras Model instance.

    """
    if quantized:
        model_name_v1 = 'vgg_utk_face_iq8_wq2_aq2.h5'
        file_hash_v1 = 'e341d2d5e4655846ddc7aceff0d4e324cbfbcca16f3cfefc65e7b0863e4a23a3'
        model_name_v2 = 'vgg_utk_face_i8_w8_a8.h5'
        file_hash_v2 = 'c7a728368885cd743155cf3ba877abfd487e282adfaa2f1aa613750d3c858bd1'
    else:
        model_name_v1 = 'vgg_utk_face.h5'
        file_hash_v1 = '3f9084c452ef006a16f10f2d124804b6db267f7a5149b735a9c383a9b00a4922'
        model_name_v2 = 'vgg_utk_face.h5'
        file_hash_v2 = 'f1fc29e4ab0c1615902d0dd48afc6bad1f3bbf4b1a6a2e3642e5c2ee37208121'

    model_path, model_name, file_hash = get_model_path("vgg", model_name_v1, file_hash_v1,
                                                       model_name_v2, file_hash_v2)
    model_path = fetch_file(model_path,
                            fname=model_name,
                            file_hash=file_hash,
                            cache_subdir='models')
    return load_model(model_path)
