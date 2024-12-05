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
AkidaNet18 model definition for ImageNet classification.

AkidaNet18 architecture is inspired both from AkidaNet and ResNet18: same depth and dimensions than
ResNet18 but without skip connections and using SeparableConvolution layers.

"""

__all__ = ["akidanet18_imagenet", "akidanet18_imagenet_pretrained"]

from keras import Model, regularizers
from keras.layers import Input, Rescaling

from .imagenet_utils import obtain_input_shape
from ..layer_blocks import conv_block, separable_conv_block, dense_block
from ..utils import fetch_file
from ..model_io import load_model, get_model_path


def akidanet18_imagenet(input_shape=None,
                        include_top=True,
                        pooling=None,
                        classes=1000,
                        depths=(4, 4, 4, 4),
                        dimensions=(64, 128, 256, 512),
                        input_scaling=(128, -1)):
    """Instantiates the AkidaNet18 architecture.

    Note: input preprocessing is included as part of the model (as a Rescaling layer). This model
    expects inputs to be float tensors of pixels with values in the [0, 255] range.

    Args:
        input_shape (tuple, optional): shape tuple. Defaults to None.
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
        depth (tuple, optional): number of layers in each stages of the model. The length of the
            tuple defines the number of stages. Defaults to (4, 4, 4, 4).
        dimensions (tuple, optional): number of filters in each stage on the model. The length of
            the tuple must be equal to the length of the `depth` tuple. Defaults to
            (64, 128, 256, 512).
        input_scaling (tuple, optional): scale factor and offset to apply to
            inputs. Defaults to (128, -1). Note that following Akida convention,
            the scale factor is an integer used as a divisor.

    Returns:
        keras.Model: a Keras model for AkidaNet/ImageNet.

    Raises:
        ValueError: in case of invalid input shape or mismatching `depth` and `dimensions`.
    """
    # Sanity checks
    stages = len(depths)
    if len(dimensions) != stages:
        raise ValueError(f"'depth' and 'dimensions' must be of the same length, received: {depths} "
                         f"and {dimensions}.")

    # Define weight regularization, will apply to the convolutional layers and
    # to all pointwise weights of separable convolutional layers.
    weight_regularizer = regularizers.l2(4e-5)

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

    # ConvNext stem layer: 4x4 kernel with stride 4
    x = conv_block(x,
                   filters=int(dimensions[0]),
                   name='convnext_stem',
                   kernel_size=(4, 4),
                   padding='same',
                   use_bias=False,
                   strides=4,
                   add_batchnorm=True,
                   relu_activation='ReLU7.5',
                   kernel_regularizer=weight_regularizer)

    # Define the stages
    for stage in range(stages):
        # Like for AkidaNet, early layers (first 2 stages) are defined as standard Convolutional and
        # next layers are SeparableConvolutional layers
        if stage < 2:
            current_block = conv_block
            kwarg = {"kernel_regularizer": weight_regularizer}
        else:
            current_block = separable_conv_block
            kwarg = {"pointwise_regularizer": weight_regularizer, "fused": False}

        strides = 2 if stage > 0 else 1
        for i in range(depths[stage]):
            # First layer in stage comes with strides 2 except in first stage where strides is
            # handled by the previous stem
            strides = 2 if i == 0 and stage > 0 else 1

            # Handle final pooling in last layer of last stage
            if stage == stages - 1 and i == depths[stage] - 1:
                pool = 'global_avg' if include_top or pooling == 'avg' else None
            else:
                pool = None

            x = current_block(x,
                              filters=int(dimensions[stage]),
                              name=f'stage_{stage}/conv_{i}',
                              kernel_size=(3, 3),
                              strides=strides,
                              padding='same',
                              use_bias=False,
                              pooling=pool,
                              add_batchnorm=True,
                              relu_activation='ReLU7.5',
                              post_relu_gap=True,
                              **kwarg)

    # Classification layer
    if include_top:
        x = dense_block(x,
                        classes,
                        add_batchnorm=False,
                        relu_activation=False,
                        kernel_initializer="he_normal",
                        name='classifier',
                        kernel_regularizer=weight_regularizer)

    # Create model
    return Model(img_input, x, name='akidanet18_%s_%s' % (input_shape[0], classes))


def akidanet18_imagenet_pretrained(quantized=True):
    """
    Helper method to retrieve an `akidanet18_imagenet` model that was trained on ImageNet dataset.

    Args:
        quantized (bool, optional): a boolean indicating whether the model should be loaded
            quantized or not. Defaults to True.

    Returns:
        keras.Model: a Keras Model instance.

    """
    # Note: cannot be converted to v1 so we should ultimately removed v1 support and only keep v2
    if quantized:
        model_name_v2 = 'akidanet18_imagenet_224_i8_w8_a8.h5'
        file_hash_v2 = '3ee6309b6a8e5aad570fc22d750e9d1e8db82d9a250e9d8f09e009a815db7a3c'
    else:
        model_name_v2 = 'akidanet18_imagenet_224.h5'
        file_hash_v2 = 'e52cf2a20b786a488b75f371b8b89f0c95a383dafc1331eea51b2356552d9704'

    model_path, model_name, file_hash = get_model_path("akidanet18", model_name_v2=model_name_v2,
                                                       file_hash_v2=file_hash_v2)
    model_path = fetch_file(model_path,
                            fname=model_name,
                            file_hash=file_hash,
                            cache_subdir='models')
    return load_model(model_path)
