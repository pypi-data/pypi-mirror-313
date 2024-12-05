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
PointNet++ model definition for ModelNet40 classification.
"""

__all__ = ["pointnet_plus_modelnet40", "pointnet_plus_modelnet40_pretrained"]

from keras import layers, Model, regularizers

from .pointnet_utils import get_reshape_factor
from ..layer_blocks import conv_block, dense_block, act_to_layer
from ..utils import fetch_file, get_params_by_version
from ..model_io import load_model, get_model_path


def pointnet_plus_modelnet40(selected_points=64, features=3, knn_points=32, classes=40, alpha=1.0):
    """ Instantiates a PointNet++ model for the ModelNet40 classification.

    This example implements the point cloud deep learning paper
    `PointNet (Qi et al., 2017) <https://arxiv.org/abs/1612.00593>`_. For a
    detailed introduction on PointNet see `this blog post
    <https://medium.com/@luis_gonzales/an-in-depth-look-at-pointnet-111d7efdaa1a>`_.

    PointNet++ is conceived as a repeated series of operations: sampling and
    grouping of points, followed by the trainable convnet itself. Those
    operations are then repeated at increased scale.
    Each of the selected points is taken as the centroid of the K-nearest
    neighbours. This defines a localized group.

    Note: input preprocessing is included as part of the model (as a Rescaling layer). This model
    expects inputs to be float tensors of pixels with values in the [0, 255] range.

    Args:
        selected_points (int, optional): the number of points to process per
            sample. Defaults to 64.
        features (int, optional): the number of features. Expected values are
            1 or 3. Default is 3.
        knn_points (int, optional): the number of points to include in each
            localised group. Must be a power of 2, and ideally an integer square
            (so 64, or 16 for a deliberately small network, or 256 for large).
            Defaults to 32.
        classes (int, optional): the number of classes for the classifier.
            Default is 40.
        alpha (float, optional): network filters multiplier. Default is 1.0.

    Returns:
        keras.Model: a quantized Keras model for PointNet++/ModelNet40.
    """
    # Model version management
    _, post_relu_gap, relu_activation = get_params_by_version()

    # Adapt input shape with preprocessing
    reshape_factor = get_reshape_factor(knn_points)
    input_shape = (knn_points // reshape_factor,
                   selected_points * reshape_factor, features)

    inputs = layers.Input(shape=input_shape, name="input")
    base_filter_num = round(32 * alpha)
    reg = regularizers.l1_l2(1e-7, 1e-7)

    # Rescale [0, 255] inputs to [-1, 1]
    x = layers.Rescaling(1./127, -1, name="rescaling")(inputs)

    # Block 1
    x = conv_block(x,
                   filters=base_filter_num,
                   name='block_1/conv_1',
                   kernel_size=(3, 3),
                   padding='same',
                   add_batchnorm=True,
                   relu_activation=False)
    x = act_to_layer(relu_activation, activity_regularizer=reg, name='block_1/conv_1/relu_1')(x)

    x = conv_block(x,
                   filters=base_filter_num,
                   name='block_1/conv_2',
                   kernel_size=(1, 1),
                   padding='same',
                   add_batchnorm=True,
                   relu_activation=False)
    x = act_to_layer(relu_activation, activity_regularizer=reg, name='block_1/conv_2/relu_1')(x)
    x = layers.MaxPool2D(padding='same', name='max_pooling2d')(x)

    # Block 2
    x = conv_block(x,
                   filters=base_filter_num * 2,
                   name='block_2/conv_1',
                   kernel_size=(1, 1),
                   padding='same',
                   add_batchnorm=True,
                   relu_activation=False)
    x = act_to_layer(relu_activation, activity_regularizer=reg, name='block_2/conv_1/relu_1')(x)
    x = conv_block(x,
                   filters=base_filter_num * 2,
                   name='block_2/conv_2',
                   kernel_size=(1, 1),
                   padding='same',
                   add_batchnorm=True,
                   relu_activation=False)
    x = act_to_layer(relu_activation, activity_regularizer=reg, name='block_2/conv_2/relu_1')(x)
    if knn_points >= 8:
        x = layers.MaxPool2D(padding='same', name='max_pooling2d_1')(x)

    # Block 3
    x = conv_block(x,
                   filters=base_filter_num * 4,
                   name='block_3/conv_1',
                   kernel_size=(1, 1),
                   padding='same',
                   add_batchnorm=True,
                   relu_activation=False)
    x = act_to_layer(relu_activation, activity_regularizer=reg, name='block_3/conv_1/relu_1')(x)
    x = conv_block(x,
                   filters=base_filter_num * 4,
                   name='block_3/conv_2',
                   kernel_size=(1, 1),
                   padding='same',
                   add_batchnorm=True,
                   relu_activation=False)
    x = act_to_layer(relu_activation, activity_regularizer=reg, name='block_3/conv_2/relu_1')(x)
    if knn_points >= 32:
        x = layers.MaxPool2D(padding='same', name='max_pooling2d_2')(x)

    # Block 4
    x = conv_block(x,
                   filters=base_filter_num * 8,
                   name='block_4/conv_1',
                   kernel_size=(1, 1),
                   padding='same',
                   add_batchnorm=True,
                   relu_activation=False)
    x = act_to_layer(relu_activation, activity_regularizer=reg, name='block_4/conv_1/relu_1')(x)
    if knn_points >= 128:
        x = layers.MaxPool2D(padding='same', name='max_pooling2d_3')(x)

    # Block 5
    x = conv_block(x,
                   filters=base_filter_num * 16,
                   name='block_5/conv_1',
                   kernel_size=(1, 1),
                   pooling='global_avg',
                   post_relu_gap=post_relu_gap,
                   padding='same',
                   add_batchnorm=True)

    # Block 6
    x = layers.Reshape((1, 1, x.shape[-1]))(x)
    x = dense_block(x,
                    units=base_filter_num * 16,
                    name='fc_1',
                    relu_activation=relu_activation,
                    add_batchnorm=True)
    x = dense_block(x,
                    units=base_filter_num * 8,
                    name='fc_2',
                    relu_activation=relu_activation,
                    add_batchnorm=True)
    x = layers.Dense(classes, activation=None, name="dense")(x)
    act_function = 'softmax' if classes > 1 else 'sigmoid'
    x = layers.Activation(act_function, name=f'act_{act_function}')(x)
    outputs = layers.Reshape((classes,))(x)

    return Model(inputs=inputs, outputs=outputs, name="pointnet_plus")


def pointnet_plus_modelnet40_pretrained(quantized=True):
    """
    Helper method to retrieve a `pointnet_plus` model that was trained on
    ModelNet40 dataset.

    Args:
        quantized (bool, optional): a boolean indicating whether the model should be loaded
            quantized or not. Defaults to True.

    Returns:
        keras.Model: a Keras Model instance.
    """
    if quantized:
        model_name_v1 = 'pointnet_plus_modelnet40_iq8_wq4_aq4.h5'
        file_hash_v1 = '8c6cb08a72909a50e2792f9b0b52c17e9972a9a42e8ace11443e811c18b6573c'
        model_name_v2 = 'pointnet_plus_modelnet40_i8_w8_a8.h5'
        file_hash_v2 = 'e97664416fb2e8b66573e0718d4107d813ba87472abb24ab0bf6aeb511e3042e'
    else:
        model_name_v1 = 'pointnet_plus_modelnet40.h5'
        file_hash_v1 = '1499e8d629642c0f67436bdc8ba7d883c2f1cc1f5993a758588fa177a3fc585c'
        model_name_v2 = 'pointnet_plus_modelnet40.h5'
        file_hash_v2 = '4c9ce75c9acc9a98070ba3a385f388e3672a534972f6e921e2746b1b8e451e92'

    model_path, model_name, file_hash = get_model_path("pointnet_plus", model_name_v1, file_hash_v1,
                                                       model_name_v2, file_hash_v2)
    model_path = fetch_file(model_path,
                            fname=model_name,
                            file_hash=file_hash,
                            cache_subdir='models')

    return load_model(model_path)
