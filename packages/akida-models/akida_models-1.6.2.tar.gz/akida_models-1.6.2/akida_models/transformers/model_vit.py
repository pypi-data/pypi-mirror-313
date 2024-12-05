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

__all__ = ["vit_imagenet", "vit_ti16", "bc_vit_ti16", "bc_vit_ti16_imagenet_pretrained", "vit_s16",
           "vit_s32", "vit_b16", "vit_b32", "vit_l16", "vit_l32", "CONFIG_TI", "CONFIG_S",
           "CONFIG_B", "CONFIG_L", "apply_embedding_weights"]

import keras
import warnings
import numpy as np
import scipy as sp
import typing_extensions as tx

from quantizeml.layers import AddPositionEmbs, ClassToken, ExtractToken
from quantizeml import load_model

from ..layer_blocks import transformer_block, norm_to_layer
from ..utils import fetch_file
from ..model_io import get_model_path


ConfigDict = tx.TypedDict(
    "ConfigDict",
    {
        "dropout": float,
        "mlp_dim": int,
        "num_heads": int,
        "num_blocks": int,
        "hidden_size": int,
    },
)

CONFIG_TI: ConfigDict = {
    "dropout": 0.0,
    "mlp_dim": 768,
    "num_heads": 3,
    "num_blocks": 12,
    "hidden_size": 192,
}

CONFIG_S: ConfigDict = {
    "dropout": 0.1,
    "mlp_dim": 1536,
    "num_heads": 6,
    "num_blocks": 12,
    "hidden_size": 384,
}

CONFIG_B: ConfigDict = {
    "dropout": 0.1,
    "mlp_dim": 3072,
    "num_heads": 12,
    "num_blocks": 12,
    "hidden_size": 768,
}

CONFIG_L: ConfigDict = {
    "dropout": 0.1,
    "mlp_dim": 4096,
    "num_heads": 16,
    "num_blocks": 24,
    "hidden_size": 1024,
}


def apply_embedding_weights(target_layer, source_weights, num_patches, num_tokens=1):
    """Apply embedding weights to a target layer.

    Args:
        target_layer (:obj:`keras.Layer`): The target layer to which weights will be applied.
        source_weights (list of :obj:`np.array`): The source weights.
        num_patches (int or tuple): Number of patches in xy spatial dimension, extracted from
            embedding layer.
        num_tokens (int, optional): Number of tokens. Defaults to 1.
    """
    assert isinstance(source_weights, list), "source_weights must be a list of numpy arrays"
    expected_shape = target_layer.weights[0].shape

    # number of patches constrains
    if isinstance(num_patches, int):
        num_patches = (num_patches, num_patches)
    assert len(num_patches) == 2, "num_patches must contain at most two values"
    assert all(x > 0 for x in num_patches), "every patch must be greater than 0"

    if expected_shape != source_weights[0].shape:
        token, grid = source_weights[0][0, :num_tokens], source_weights[0][0, num_tokens:]
        sin = int(np.sqrt(grid.shape[0]))
        sout_x = num_patches[0]
        sout_y = num_patches[1]
        warnings.warn(
            "Resizing position embeddings from " f"{sin}, {sin} to {sout_x}, {sout_y}",
            UserWarning,
        )
        zoom = (sout_y / sin, sout_x / sin, 1)
        grid = sp.ndimage.zoom(grid.reshape(sin, sin, -1), zoom, order=1).reshape(
            sout_x * sout_y, -1
        )
        new_weights = np.concatenate([token, grid], axis=0)[np.newaxis]
        source_weights = [new_weights] + source_weights[1:]
    target_layer.set_weights(source_weights)


def vit_imagenet(input_shape,
                 patch_size,
                 num_blocks,
                 hidden_size,
                 num_heads,
                 name,
                 mlp_dim,
                 classes=1000,
                 dropout=0.1,
                 include_top=True,
                 norm='LN',
                 last_norm='LN',
                 softmax='softmax',
                 act="GeLU"):
    """Instantiates the ViT architecture.

    The Vision Transformer (ViT) is a model for image classification that employs a Transformer-like
    architecture over patches of the image. An image is split into fixed-size patches, each of them
    are then linearly embedded, position embeddings are added, and the resulting sequence of vectors
    are fed to a standard Transformer encoder.

    Please refer to https://arxiv.org/abs/2010.11929 for further details.

    Note: input preprocessing is included as part of the model (as a Rescaling layer). This model
    expects inputs to be float tensors of pixels with values in the [0, 255] range.

    Args:
        input_shape (tuple): image shape tuple
        patch_size (int): the size of each patch (must fit evenly in image size)
        num_blocks (int): the number of transformer blocks to use.
        hidden_size (int): the number of filters to use
        num_heads (int): the number of transformer heads
        name (str): the model name
        mlp_dim (int): the number of dimensions for the MLP output in the transformers.
        classes (int, optional): number of classes to classify images into, only to be specified if
            `include_top` is True. Defaults to 1000.
        dropout (float, optional): fraction of the units to drop for dense layers. Defaults to 0.1.
        include_top (bool, optional): whether to include the final classifier head. If False,
            the output will correspond to that of the transformer. Defaults to True.
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
    assert (input_shape[0] % patch_size == 0) and (
        input_shape[1] % patch_size == 0), "image size must be a multiple of patch_size"

    if last_norm not in ('LN', 'BN'):
        raise NotImplementedError("last_norm should be in ['LN', 'BN']"
                                  f"but received {norm}.")

    # Normalize image adding rescaling layer
    x = keras.layers.Input(shape=input_shape, name="input")
    y = keras.layers.Rescaling(1 / 127.5, -1, name="Rescale")(x)

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
        y = norm_to_layer(last_norm)(
            epsilon=1e-6, name="Transformer/EncoderNorm")(y)
        y = ExtractToken(token=0, name="ExtractToken")(y)
        y = keras.layers.Dense(classes, name="Head")(y)
    return keras.models.Model(inputs=x, outputs=y, name=name)


def vit_ti16(input_shape=(224, 224, 3),
             classes=1000,
             norm='LN',
             last_norm='LN',
             softmax='softmax',
             act='GeLU',
             include_top=True):
    """Instantiates the ViT-Tiny 16 architecture; that is a ViT architecture with 3 attention heads,
    12 blocks and a patch size of 16.

    Args:
        input_shape (tuple, optional): input shape. Defaults to (224, 224, 3).
        classes (int, optional): number of classes. Defaults to 1000.
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
    return vit_imagenet(
        name="vit-tiny",
        patch_size=16,
        input_shape=input_shape,
        classes=classes,
        norm=norm,
        last_norm=last_norm,
        act=act,
        softmax=softmax,
        include_top=include_top,
        **CONFIG_TI
    )


def bc_vit_ti16(input_shape=(224, 224, 3), classes=1000, include_top=True, num_blocks=12):
    """Instantiates the ViT-Tiny 16 architecture adapted for implementation on hardware,
    that is:

        - LayerNormalization replaced by LayerMadNormalization,
        - GeLU replaced by ReLU8 activations,
        - Softmax replaced by shiftmax.

    Args:
        input_shape (tuple, optional): input shape. Defaults to (224, 224, 3).
        classes (int, optional): number of classes. Defaults to 1000.
        include_top (bool, optional): whether to include the final classifier network.
            Defaults to True.
        num_blocks (int, optional): the number of transformer blocks to use. Defaults to 12.

    Returns:
        keras.Model: the requested model
    """
    config_ti = CONFIG_TI.copy()
    config_ti["num_blocks"] = num_blocks

    return vit_imagenet(
        name="vit-tiny",
        patch_size=16,
        input_shape=input_shape,
        classes=classes,
        norm="LMN",
        last_norm="BN",
        softmax="softmax2",
        act="ReLU8",
        include_top=include_top,
        **config_ti
    )


def bc_vit_ti16_imagenet_pretrained(quantized=True):
    """ Helper method to retrieve a ViT-Tiny 16 model adapted for implementation on hardware,
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
        model_name_v2 = 'bc_vit_ti16_224_i8_w8_a8.h5'
        file_hash_v2 = 'b147503b81991a5fbfabdd704fd17eb94fadb9faac1bb664bd195a16292d2e7f'
    else:
        model_name_v2 = 'bc_vit_ti16_224.h5'
        file_hash_v2 = '7ae299f698abc545e21338b129dfbc0ff97ee9b994319e53e8605d34e3ee1f82'

    model_path, model_name, file_hash = get_model_path("vit", model_name_v2=model_name_v2,
                                                       file_hash_v2=file_hash_v2)
    model_path = fetch_file(model_path,
                            fname=model_name,
                            file_hash=file_hash,
                            cache_subdir='models')
    return load_model(model_path)


def vit_s16(input_shape=(224, 224, 3), classes=1000, include_top=True):
    """Instantiates the ViT-Small 16 architecture; that is a ViT architecture with 6 attention heads,
    12 blocks and a patch size of 16.

    Args:
        input_shape (tuple, optional): input shape. Defaults to (224, 224, 3).
        classes (int, optional): number of classes. Defaults to 1000.
        include_top (bool, optional): whether to include the final classifier network.
            Defaults to True.

    Returns:
        keras.Model: the requested model
    """
    return vit_imagenet(
        name="vit-s16",
        patch_size=16,
        input_shape=input_shape,
        classes=classes,
        include_top=include_top,
        **CONFIG_S
    )


def vit_s32(input_shape=(224, 224, 3), classes=1000, include_top=True):
    """Instantiates the ViT-Small 32 architecture; that is a ViT architecture with 6 attention heads,
    12 blocks and a patch size of 32.

    Args:
        input_shape (tuple, optional): input shape. Defaults to (224, 224, 3).
        classes (int, optional): number of classes. Defaults to 1000.
        include_top (bool, optional): whether to include the final classifier network.
            Defaults to True.

    Returns:
        keras.Model: the requested model
    """
    return vit_imagenet(
        name="vit-s32",
        patch_size=32,
        input_shape=input_shape,
        classes=classes,
        include_top=include_top,
        **CONFIG_S
    )


def vit_b16(input_shape=(224, 224, 3), classes=1000, include_top=True):
    """Instantiates the ViT-B16 architecture; that is a ViT architecture with 12 attention heads,
    12 blocks and a patch size of 16.

    Args:
        input_shape (tuple, optional): input shape. Defaults to (224, 224, 3).
        classes (int, optional): number of classes. Defaults to 1000.
        include_top (bool, optional): whether to include the final classifier network.
            Defaults to True.

    Returns:
        keras.Model: the requested model
    """
    return vit_imagenet(
        name="vit-b16",
        patch_size=16,
        input_shape=input_shape,
        classes=classes,
        include_top=include_top,
        **CONFIG_B
    )


def vit_b32(input_shape=(224, 224, 3), classes=1000, include_top=True):
    """Instantiates the ViT-B32 architecture; that is a ViT architecture with 12 attention heads,
    12 blocks and a patch size of 32.

    Args:
        input_shape (tuple, optional): input shape. Defaults to (224, 224, 3).
        classes (int, optional): number of classes. Defaults to 1000.
        include_top (bool, optional): whether to include the final classifier network.
            Defaults to True.

    Returns:
        keras.Model: the requested model
    """
    return vit_imagenet(
        name="vit-b32",
        patch_size=32,
        input_shape=input_shape,
        classes=classes,
        include_top=include_top,
        **CONFIG_B
    )


def vit_l16(input_shape=(384, 384, 3), classes=1000, include_top=True):
    """Instantiates the ViT-L16 architecture; that is a ViT architecture with 16 attention heads,
    24 blocks and a patch size of 16.

    Args:
        input_shape (tuple, optional): input shape. Defaults to (384, 384, 3).
        classes (int, optional): number of classes. Defaults to 1000.
        include_top (bool, optional): whether to include the final classifier network.
            Defaults to True.

    Returns:
        keras.Model: the requested model
    """
    return vit_imagenet(
        name="vit-l16",
        patch_size=16,
        input_shape=input_shape,
        classes=classes,
        include_top=include_top,
        **CONFIG_L
    )


def vit_l32(input_shape=(384, 384, 3), classes=1000, include_top=True):
    """Instantiates the ViT-L32 architecture; that is a ViT architecture with 16 attention heads,
    24 blocks and a patch size of 32.

    Args:
        input_shape (tuple, optional): input shape. Defaults to (384, 384, 3).
        classes (int, optional): number of classes. Defaults to 1000.
        include_top (bool, optional): whether to include the final classifier network.
            Defaults to True.

    Returns:
        keras.Model: the requested model
    """
    return vit_imagenet(
        name="vit-l32",
        patch_size=32,
        input_shape=input_shape,
        classes=classes,
        include_top=include_top,
        **CONFIG_L
    )
