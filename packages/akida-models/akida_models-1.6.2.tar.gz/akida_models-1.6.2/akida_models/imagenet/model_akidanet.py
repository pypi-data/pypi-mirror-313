#!/usr/bin/env python
# ******************************************************************************
# Copyright 2021 Brainchip Holdings Ltd.
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
AkidaNet model definition for ImageNet classification.

AkidaNet is an NSoC optimized model inspired from VGG and MobileNet V1
architectures. It can be used for multiple use cases through transfer learning.

"""

__all__ = ["akidanet_imagenet", "akidanet_imagenet_pretrained",
           "akidanet_faceidentification_pretrained", "akidanet_plantvillage_pretrained",
           "akidanet_vww_pretrained"]

from keras import Model, regularizers
from keras.layers import Input, Dropout, Rescaling

from .imagenet_utils import obtain_input_shape
from ..layer_blocks import conv_block, separable_conv_block, dense_block
from ..utils import fetch_file, get_params_by_version
from ..model_io import load_model, get_model_path


def akidanet_imagenet(input_shape=None,
                      alpha=1.0,
                      include_top=True,
                      pooling=None,
                      classes=1000,
                      input_scaling=(128, -1)):
    """Instantiates the AkidaNet architecture.

    Note: input preprocessing is included as part of the model (as a Rescaling layer). This model
    expects inputs to be float tensors of pixels with values in the [0, 255] range.

    Args:
        input_shape (tuple, optional): shape tuple. Defaults to None.
        alpha (float, optional): controls the width of the model.
            Defaults to 1.0.

            * If `alpha` < 1.0, proportionally decreases the number of filters
              in each layer.
            * If `alpha` > 1.0, proportionally increases the number of filters
              in each layer.
            * If `alpha` = 1, default number of filters from the paper are used
              at each layer.
        include_top (bool, optional): whether to include the fully-connected
            layer at the top of the model. Defaults to True.
        pooling (str, optional): optional pooling mode for feature extraction
            when `include_top` is `False`.
            Defaults to None.

            * `None` means that the output of the model will be the 4D tensor
              output of the last convolutional block.
            * `avg` means that global average pooling will be applied to the
              output of the last convolutional block, and thus the output of the
              model will be a 2D tensor.
        classes (int, optional): optional number of classes to classify images
            into, only to be specified if `include_top` is `True`. Defaults to 1000.
        input_scaling (tuple, optional): scale factor and offset to apply to
            inputs. Defaults to (128, -1). Note that following Akida convention,
            the scale factor is an integer used as a divisor.

    Returns:
        keras.Model: a Keras model for AkidaNet/ImageNet.

    Raises:
        ValueError: in case of invalid input shape.
    """
    # Define weight regularization, will apply to the convolutional layers and
    # to all pointwise weights of separable convolutional layers.
    weight_regularizer = regularizers.l2(4e-5)

    # Model version management
    fused, post_relu_gap, relu_activation = get_params_by_version(relu_v2='ReLU7.5')

    # Determine proper input shape and default size.
    if input_shape is None:
        default_size = 224
    else:
        rows = input_shape[0]
        cols = input_shape[1]

        if rows == cols and rows in [128, 160, 192, 224]:
            default_size = rows
        else:
            default_size = 224

    input_shape = obtain_input_shape(input_shape,
                                     default_size=default_size,
                                     min_size=32,
                                     include_top=include_top)

    img_input = Input(shape=input_shape, name="input")

    if input_scaling is None:
        x = img_input
    else:
        scale, offset = input_scaling
        x = Rescaling(1. / scale, offset, name="rescaling")(img_input)

    x = conv_block(x,
                   filters=int(32 * alpha),
                   name='conv_0',
                   kernel_size=(3, 3),
                   padding='same',
                   use_bias=False,
                   strides=2,
                   add_batchnorm=True,
                   relu_activation=relu_activation,
                   kernel_regularizer=weight_regularizer)

    x = conv_block(x,
                   filters=int(64 * alpha),
                   name='conv_1',
                   kernel_size=(3, 3),
                   padding='same',
                   use_bias=False,
                   add_batchnorm=True,
                   relu_activation=relu_activation,
                   kernel_regularizer=weight_regularizer)

    x = conv_block(x,
                   filters=int(128 * alpha),
                   name='conv_2',
                   kernel_size=(3, 3),
                   padding='same',
                   strides=2,
                   use_bias=False,
                   add_batchnorm=True,
                   relu_activation=relu_activation,
                   kernel_regularizer=weight_regularizer)

    x = conv_block(x,
                   filters=int(128 * alpha),
                   name='conv_3',
                   kernel_size=(3, 3),
                   padding='same',
                   use_bias=False,
                   add_batchnorm=True,
                   relu_activation=relu_activation,
                   kernel_regularizer=weight_regularizer)

    x = separable_conv_block(x,
                             filters=int(256 * alpha),
                             name='separable_4',
                             kernel_size=(3, 3),
                             padding='same',
                             strides=2,
                             use_bias=False,
                             add_batchnorm=True,
                             relu_activation=relu_activation,
                             fused=fused,
                             pointwise_regularizer=weight_regularizer)

    x = separable_conv_block(x,
                             filters=int(256 * alpha),
                             name='separable_5',
                             kernel_size=(3, 3),
                             padding='same',
                             use_bias=False,
                             add_batchnorm=True,
                             relu_activation=relu_activation,
                             fused=fused,
                             pointwise_regularizer=weight_regularizer)

    x = separable_conv_block(x,
                             filters=int(512 * alpha),
                             name='separable_6',
                             kernel_size=(3, 3),
                             padding='same',
                             strides=2,
                             use_bias=False,
                             add_batchnorm=True,
                             relu_activation=relu_activation,
                             fused=fused,
                             pointwise_regularizer=weight_regularizer)

    x = separable_conv_block(x,
                             filters=int(512 * alpha),
                             name='separable_7',
                             kernel_size=(3, 3),
                             padding='same',
                             use_bias=False,
                             add_batchnorm=True,
                             relu_activation=relu_activation,
                             fused=fused,
                             pointwise_regularizer=weight_regularizer)

    x = separable_conv_block(x,
                             filters=int(512 * alpha),
                             name='separable_8',
                             kernel_size=(3, 3),
                             padding='same',
                             use_bias=False,
                             add_batchnorm=True,
                             relu_activation=relu_activation,
                             fused=fused,
                             pointwise_regularizer=weight_regularizer)

    x = separable_conv_block(x,
                             filters=int(512 * alpha),
                             name='separable_9',
                             kernel_size=(3, 3),
                             padding='same',
                             use_bias=False,
                             add_batchnorm=True,
                             relu_activation=relu_activation,
                             fused=fused,
                             pointwise_regularizer=weight_regularizer)

    x = separable_conv_block(x,
                             filters=int(512 * alpha),
                             name='separable_10',
                             kernel_size=(3, 3),
                             padding='same',
                             use_bias=False,
                             add_batchnorm=True,
                             relu_activation=relu_activation,
                             fused=fused,
                             pointwise_regularizer=weight_regularizer)

    x = separable_conv_block(x,
                             filters=int(512 * alpha),
                             name='separable_11',
                             kernel_size=(3, 3),
                             padding='same',
                             use_bias=False,
                             add_batchnorm=True,
                             relu_activation=relu_activation,
                             fused=fused,
                             pointwise_regularizer=weight_regularizer)

    x = separable_conv_block(x,
                             filters=int(1024 * alpha),
                             name='separable_12',
                             kernel_size=(3, 3),
                             padding='same',
                             strides=2,
                             use_bias=False,
                             add_batchnorm=True,
                             relu_activation=relu_activation,
                             fused=fused,
                             pointwise_regularizer=weight_regularizer)

    # Last separable layer with global pooling
    layer_pooling = 'global_avg' if include_top or pooling == 'avg' else None
    x = separable_conv_block(x,
                             filters=int(1024 * alpha),
                             name='separable_13',
                             kernel_size=(3, 3),
                             padding='same',
                             pooling=layer_pooling,
                             use_bias=False,
                             add_batchnorm=True,
                             relu_activation=relu_activation,
                             fused=fused,
                             post_relu_gap=post_relu_gap,
                             pointwise_regularizer=weight_regularizer)

    if include_top:
        x = Dropout(1e-3, name='dropout')(x)
        x = dense_block(x,
                        classes,
                        name='classifier',
                        add_batchnorm=False,
                        relu_activation=False,
                        kernel_regularizer=weight_regularizer)

    # Create model.
    return Model(img_input, x, name='akidanet_%0.2f_%s_%s' % (alpha, input_shape[0], classes))


def akidanet_imagenet_pretrained(alpha=1.0, quantized=True):
    """
    Helper method to retrieve an `akidanet_imagenet` model that was trained on
    ImageNet dataset.

    Args:
        alpha (float, optional): width of the model, allowed values in [0.25,
            0.5, 1]. Defaults to 1.0.
        quantized (bool, optional): a boolean indicating whether the model should be loaded
            quantized or not. Defaults to True.

    Returns:
        keras.Model: a Keras Model instance.

    """
    if alpha == 1.0:
        if quantized:
            model_name_v1 = 'akidanet_imagenet_224_iq8_wq4_aq4.h5'
            file_hash_v1 = '359e0ff05abbb26fe215830ca467ef40761767c0d77f8c743c6d6e4fffa7a925'
            model_name_v2 = 'akidanet_imagenet_224_alpha_1_i8_w8_a8.h5'
            file_hash_v2 = '08ba150a1a21a69dfe8743b688ef1b018b8474826e5a26792d160614b4769267'
        else:
            model_name_v1 = 'akidanet_imagenet_224.h5'
            file_hash_v1 = '9208233d21c3251777b1f700b7c2c51491590133f97f81f04348ab131679b00f'
            model_name_v2 = 'akidanet_imagenet_224_alpha_1.h5'
            file_hash_v2 = 'fc4aaf81a8aec8792709ae0fa10aac2dcb9517202a6f919e049c4db96f272339'
    elif alpha == 0.5:
        if quantized:
            model_name_v1 = 'akidanet_imagenet_224_alpha_50_iq8_wq4_aq4.h5'
            file_hash_v1 = '1d9493115d43625f2644f8265f71b8487c4019047fc331e892a233a3d6520371'
            model_name_v2 = 'akidanet_imagenet_224_alpha_0.5_i8_w8_a8.h5'
            file_hash_v2 = '801bd49da790625672896050648cc348da93bb99ec61bce4c4f7dbbd25b9c1d6'
        else:
            model_name_v1 = 'akidanet_imagenet_224_alpha_50.h5'
            file_hash_v1 = '61f2883a6b798f922a5c0411296219a85f25581d7571f65546557b46066f058f'
            model_name_v2 = 'akidanet_imagenet_224_alpha_0.5.h5'
            file_hash_v2 = '6d202e9477d89192abe069e3a87105e0db8fe4a6a1a152afc933b687dd5418b8'
    elif alpha == 0.25:
        if quantized:
            model_name_v1 = 'akidanet_imagenet_224_alpha_25_iq8_wq4_aq4.h5'
            file_hash_v1 = '9146d6228d859d8b8db1c1b7a795471096e5a49ee4ff5656eabc6be749d42f5e'
            model_name_v2 = 'akidanet_imagenet_224_alpha_0.25_i8_w8_a8.h5'
            file_hash_v2 = '3ca17743c0bc815b80912f2a316c41bf4ca633d5fe8a0d647584e4f4260be88b'
        else:
            model_name_v1 = 'akidanet_imagenet_224_alpha_25.h5'
            file_hash_v1 = '23d96a1c73397a5c2060808f3843d99fa3cd96b5b1af36e03b0d039be393c001'
            model_name_v2 = 'akidanet_imagenet_224_alpha_0.25.h5'
            file_hash_v2 = 'bb2b39fc2e41009547eb267fd8b6c66d7a5a16e72ffed4a641ec82f50fb4370f'
    else:
        raise ValueError(
            f"Requested model with alpha={alpha} is not available.")

    model_path, model_name, file_hash = get_model_path("akidanet", model_name_v1, file_hash_v1,
                                                       model_name_v2, file_hash_v2)
    model_path = fetch_file(model_path,
                            fname=model_name,
                            file_hash=file_hash,
                            cache_subdir='models')
    return load_model(model_path)


def akidanet_faceidentification_pretrained(quantized=True):
    """
    Helper method to retrieve an `akidanet_imagenet` model that was trained on
    CASIA Webface dataset and that performs face identification.

    Args:
        quantized (bool, optional): a boolean indicating whether the model should be loaded
            quantized or not. Defaults to True.

    Returns:
        keras.Model: a Keras Model instance.

    """
    if quantized:
        model_name_v1 = 'akidanet_faceidentification_iq8_wq4_aq4.h5'
        file_hash_v1 = 'b287f86155c51dc73053f7e5f3e58be1beb4a35d543dd817a63a782ffaf5bff1'
        model_name_v2 = 'akidanet_faceidentification_i8_w8_a8.h5'
        file_hash_v2 = '6818d82b8a94ebe369b8973721856b43369e8b0ff10c31b41f2610983b7a9531'
    else:
        model_name_v1 = 'akidanet_faceidentification.h5'
        file_hash_v1 = '998b6cdce5adbdb0b7c3e9f8eb1011c3582e05f0c159e473d226a9a94c4309a1'
        model_name_v2 = 'akidanet_faceidentification.h5'
        file_hash_v2 = 'f7b65fbf520f51b3c0c6d8cb7fcc78391536f200a45dbc8b9bd16262ebd82b18'

    model_path, model_name, file_hash = get_model_path("akidanet", model_name_v1, file_hash_v1,
                                                       model_name_v2, file_hash_v2)
    model_path = fetch_file(model_path,
                            fname=model_name,
                            file_hash=file_hash,
                            cache_subdir='models')
    return load_model(model_path)


def akidanet_plantvillage_pretrained(quantized=True):
    """
    Helper method to retrieve an `akidanet_imagenet` model that was trained on
    PlantVillage dataset.

    Args:
        quantized (bool, optional): a boolean indicating whether the model should be loaded
            quantized or not. Defaults to True.

    Returns:
        keras.Model: a Keras Model instance.

    """
    if quantized:
        model_name_v1 = 'akidanet_plantvillage_iq8_wq4_aq4.h5'
        file_hash_v1 = '1400910c774fd78a5e6ea227ff28cb28e79ecec0909a378068cd9f40ddaf4e0a'
        model_name_v2 = 'akidanet_plantvillage_i8_w8_a8.h5'
        file_hash_v2 = '5b8f7f6eb5ce5fa84c8b3cb28cd9816c124063c256934e8291d62d40a24ed9ea'
    else:
        model_name_v1 = None
        file_hash_v1 = None
        model_name_v2 = 'akidanet_plantvillage.h5'
        file_hash_v2 = '625145dec17e286beb61b9f683dc2f518752e5f9203d3b69b27c07d802528dbd'

    model_path, model_name, file_hash = get_model_path("akidanet", model_name_v1, file_hash_v1,
                                                       model_name_v2, file_hash_v2)
    model_path = fetch_file(model_path,
                            fname=model_name,
                            file_hash=file_hash,
                            cache_subdir='models')
    return load_model(model_path)


def akidanet_vww_pretrained(quantized=True):
    """
    Helper method to retrieve an `akidanet_imagenet` model that was trained on
    VWW dataset.

    Args:
        quantized (bool, optional): a boolean indicating whether the model should be loaded
            quantized or not. Defaults to True.

    Returns:
        keras.Model: a Keras Model instance.

    """
    if quantized:
        model_name_v1 = 'akidanet_vww_iq8_wq4_aq4.h5'
        file_hash_v1 = 'cd130d90ed736447b6244dc1228e708b9dab20af0d2bf57b9a49df4362467ea8'
        model_name_v2 = 'akidanet_vww_i8_w8_a8.h5'
        file_hash_v2 = '5802a9555741c1daa2517458cab3c9550515d4d389fcdbc378fe5e102df8287d'
    else:
        model_name_v1 = 'akidanet_vww.h5'
        file_hash_v1 = '00e03f13226cd622ad92bdb3402c4b4399a69875f2dde6ccadfb235ad6994d78'
        model_name_v2 = 'akidanet_vww.h5'
        file_hash_v2 = '635cbb3cfa486f44d0fca7ca66dbc794b87b67d7d77ab32e06780ecb278c2c58'

    model_path, model_name, file_hash = get_model_path("akidanet", model_name_v1, file_hash_v1,
                                                       model_name_v2, file_hash_v2)
    model_path = fetch_file(model_path,
                            fname=model_name,
                            file_hash=file_hash,
                            cache_subdir='models')
    return load_model(model_path)
