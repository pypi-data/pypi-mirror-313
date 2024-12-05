#!/usr/bin/env python
# ******************************************************************************
# Copyright 2022 Brainchip Holdings Ltd.
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
ViT model definition.
Inspired from https://github.com/faustomorales/vit-keras/blob/master/vit_keras/vit.py.
"""

__all__ = ["deit_imagenet", "deit_ti16", "bc_deit_ti16", "bc_deit_dist_ti16_imagenet_pretrained",
           "deit_s16", "deit_b16"]

import keras

from quantizeml.layers import AddPositionEmbs, ClassToken, Add, ExtractToken
from quantizeml import load_model

from .model_vit import CONFIG_TI, CONFIG_S, CONFIG_B
from ..imagenet.imagenet_utils import IMAGENET_MEAN, IMAGENET_STD
from ..layer_blocks import norm_to_layer, transformer_block
from ..utils import fetch_file
from ..model_io import get_model_path


def deit_imagenet(input_shape,
                  num_blocks,
                  hidden_size,
                  num_heads,
                  name,
                  mlp_dim,
                  patch_size=16,
                  classes=1000,
                  dropout=0.1,
                  include_top=True,
                  distilled=False,
                  norm='LN',
                  last_norm='LN',
                  softmax='softmax',
                  act="GeLU"):
    """Instantiates the DeiT architecture.

    The Data-efficient image Transformers (DeiT) is a model for image classification,
    requiring far less data and far less computing resources compared to the original
    ViT model. It relies on a teacher-student strategy specific to transformers
    (distillation token).

    Please refer to https://arxiv.org/abs/2012.12877 for further details.

    Note: input preprocessing is included as part of the model (as a Rescaling layer). This model
    expects inputs to be float tensors of pixels with values in the [0, 255] range.

    Args:
        input_shape (tuple): image shape tuple
        num_blocks (int): the number of transformer blocks to use.
        hidden_size (int): the number of filters to use
        num_heads (int): the number of transformer heads
        name (str): the model name
        mlp_dim (int): the number of dimensions for the MLP output in the transformers.
        patch_size (int, optional): the size of each patch (must fit evenly in image size). Defaults
            to 16.
        classes (int, optional): number of classes to classify images into, only to be specified if
            `include_top` is True. Defaults to 1000.
        dropout (float, optional): fraction of the units to drop for dense layers. Defaults to 0.1.
        include_top (bool, optional): whether to include the final classifier head. If False,
            the output will correspond to that of the transformer. Defaults to True.
        distilled (bool, optional): Build model append a distilled token. Defaults to False.
        norm (str, optional): string that values in ['LN', 'GN1', 'BN', 'LMN'] and that allows to
            choose from LayerNormalization, GroupNormalization(groups=1, ...), BatchNormalization
            or LayerMadNormalization layers respectively in the model. Defaults to 'LN'.
        last_norm (str, optional): string that values in ['LN', 'BN']
            and that allows to choose from LayerNormalization or
            BatchNormalization in the classifier network. Defaults to 'LN'.
        softmax (str, optional): string with values in ['softmax', 'softmax2']
            that allows to choose between softmax and softmax2 in MHA. Defaults
            to 'softmax'.
        act (str, optional): string that values in ['GeLU', 'ReLUx', 'swish'] and that allows to
            choose from GeLU, ReLUx or swish activation in MLP block. Defaults to 'GeLU'.
    """
    assert ((input_shape[0] % patch_size == 0) and
            (input_shape[1] % patch_size == 0)), "image size must be a multiple of patch_size"

    if last_norm not in ('LN', 'BN'):
        raise NotImplementedError("last_norm should be in ['LN', 'BN']"
                                  f"but received {norm}.")

    # Normalize image adding rescaling layer
    x = keras.layers.Input(shape=input_shape, name="input")
    scale = list(1.0 / 255 / std for std in IMAGENET_STD)
    offset = list(-mean / std for mean, std in zip(IMAGENET_MEAN, IMAGENET_STD))
    y = keras.layers.Rescaling(scale=scale, offset=offset, name="Rescale")(x)

    # Build model
    y = keras.layers.Conv2D(
        filters=hidden_size,
        kernel_size=patch_size,
        strides=patch_size,
        padding="valid",
        name="Embedding",
        kernel_initializer=keras.initializers.TruncatedNormal(stddev=0.02),
        bias_initializer="zeros",
    )(y)
    y = keras.layers.Reshape((y.shape[1] * y.shape[2], hidden_size))(y)
    if distilled:
        y = ClassToken(name="DistToken")(y)
    y = ClassToken(name="ClassToken")(y)
    y = AddPositionEmbs(name="Transformer/PosEmbed")(y)
    for n in range(num_blocks):
        y, _ = transformer_block(
            y,
            num_heads=num_heads,
            hidden_size=hidden_size,
            mlp_dim=mlp_dim,
            dropout=dropout,
            name=f"Transformer/EncoderBlock_{n}",
            norm=norm,
            softmax=softmax,
            mlp_act=act,
        )

    # Include classification head
    if include_top:
        yt = norm_to_layer(last_norm)(
            epsilon=1e-6, name="Transformer/EncoderNorm")(y)
        y = ExtractToken(token=0, name="ExtractToken")(yt)
        y = keras.layers.Dense(classes, name="Head")(y)
        if distilled:
            yd = ExtractToken(token=1, name="ExtractToken_Dist")(yt)
            yd = keras.layers.Dense(classes, name="DistHead")(yd)
            y = Add(name="Add", average=True)([y, yd])

    # Add distilled flag
    model = keras.models.Model(inputs=x, outputs=y, name=name)
    model.isdistilled = distilled
    return model


def deit_ti16(input_shape=(224, 224, 3),
              classes=1000,
              distilled=False,
              norm='LN',
              last_norm='LN',
              softmax='softmax',
              act='GeLU',
              include_top=True):
    """Instantiates the DeiT-Tiny 16 architecture; that is a DeiT architecture with 3 attention heads,
    12 blocks and a patch size of 16.

    Args:
        input_shape (tuple, optional): input shape. Defaults to (224, 224, 3).
        classes (int, optional): number of classes. Defaults to 1000.
        distilled (bool, optional): build model appending a distilled token. Defaults to False.
        norm (str, optional): string that values in ['LN', 'GN1', 'BN', 'LMN'] and that allows to
            choose from LayerNormalization, GroupNormalization(groups=1, ...), BatchNormalization
            or LayerMadNormalization layers respectively in the model. Defaults to 'LN'.
        last_norm (str, optional): string that values in ['LN', 'BN']
            and that allows to choose from LayerNormalization or
            BatchNormalization in the classifier network. Defaults to 'LN'.
        softmax (str, optional): string with values in ['softmax', 'softmax2'] that allows to choose
            between softmax and softmax2 in attention block. Defaults to 'softmax'.
        act (str, optional): string that values in ['GeLU', 'ReLUx', 'swish'] and that allows to
            choose from GeLU, ReLUx or swish activation inside MLP. Defaults to 'GeLU'.
        include_top (bool, optional): whether to include the final classifier network.
            Defaults to True.

    Returns:
        keras.Model: the requested model
    """
    return deit_imagenet(
        name="deit-tiny",
        input_shape=input_shape,
        classes=classes,
        distilled=distilled,
        norm=norm,
        last_norm=last_norm,
        act=act,
        softmax=softmax,
        include_top=include_top,
        **CONFIG_TI,
    )


def bc_deit_ti16(input_shape=(224, 224, 3), classes=1000, distilled=False, include_top=True,
                 num_blocks=12):
    """Instantiates the DeiT-Tiny 16 architecture adapted for implementation on hardware,
    that is:

        - LayerNormalization replaced by LayerMadNormalization,
        - GeLU replaced by ReLU8 activations,
        - Softmax replaced by shiftmax.

    Args:
        input_shape (tuple, optional): input shape. Defaults to (224, 224, 3).
        classes (int, optional): number of classes. Defaults to 1000.
        distilled (bool, optional): build model appending a distilled token. Defaults to False.
        include_top (bool, optional): whether to include the final classifier network.
            Defaults to True.
        num_blocks (int, optional): the number of transformer blocks to use. Defaults to 12.

    Returns:
        keras.Model: the requested model
    """
    config_ti = CONFIG_TI.copy()
    config_ti["num_blocks"] = num_blocks

    return deit_imagenet(
        name="deit-tiny",
        input_shape=input_shape,
        classes=classes,
        distilled=distilled,
        norm="LMN",
        last_norm="BN",
        softmax="softmax2",
        act="ReLU8",
        include_top=include_top,
        **config_ti,
    )


def bc_deit_dist_ti16_imagenet_pretrained(quantized=True):
    """ Helper method to retrieve a DeiT-Tiny 16 model adapted for implementation on hardware,
    that is:

        - LayerNormalization replaced by LayerMadNormalization,
        - GeLU replaced by ReLU8 activations,
        - Softmax replaced by shiftmax,

    and that was trained on ImageNet dataset.

    Args:
        quantized (bool, optional): a boolean indicating whether the model should be loaded
            quantized or not. Defaults to True.

    Returns:
        keras.Model: a Keras Model instance
    """
    if quantized:
        model_name_v2 = 'bc_deit_dist_ti16_224_i8_w8_a8.h5'
        file_hash_v2 = '911cd14d3223831789c11234a9c99a6dd007ce9baec8a8d5b5f208644befaf54'
    else:
        model_name_v2 = 'bc_deit_dist_ti16_224.h5'
        file_hash_v2 = '40618ba14d894fc308ef149c1eb17ff601ad54a8bc0ad329dc6f7dba5ff86260'

    model_path, model_name, file_hash = get_model_path("deit", model_name_v2=model_name_v2,
                                                       file_hash_v2=file_hash_v2)
    model_path = fetch_file(model_path,
                            fname=model_name,
                            file_hash=file_hash,
                            cache_subdir='models')
    return load_model(model_path)


def deit_s16(input_shape=(224, 224, 3), classes=1000, distilled=False, include_top=True):
    """Instantiates the DeiT-Small 16 architecture; that is a ViT architecture with 6 attention heads,
    12 blocks and a patch size of 16.

    Args:
        input_shape (tuple, optional): input shape. Defaults to (224, 224, 3).
        classes (int, optional): number of classes. Defaults to 1000.
        distilled (bool, optional): build model appending a distilled token. Defaults to False.
        include_top (bool, optional): whether to include the final classifier network.
            Defaults to True.

    Returns:
        keras.Model: the requested model
    """
    return deit_imagenet(
        name="deit-small",
        input_shape=input_shape,
        classes=classes,
        distilled=distilled,
        include_top=include_top,
        **CONFIG_S,
    )


def deit_b16(input_shape=(224, 224, 3), classes=1000, distilled=False, include_top=True):
    """Instantiates the DeiT-B16 architecture; that is a ViT architecture with 12 attention heads,
    12 blocks and a patch size of 16.

    Args:
        input_shape (tuple, optional): input shape. Defaults to (224, 224, 3).
        classes (int, optional): number of classes. Defaults to 1000.
        distilled (bool, optional): build model appending a distilled token. Defaults to False.
        include_top (bool, optional): whether to include the final classifier network.
            Defaults to True.

    Returns:
        keras.Model: the requested model
    """
    return deit_imagenet(
        name="deit-base",
        input_shape=input_shape,
        classes=classes,
        distilled=distilled,
        include_top=include_top,
        **CONFIG_B,
    )
