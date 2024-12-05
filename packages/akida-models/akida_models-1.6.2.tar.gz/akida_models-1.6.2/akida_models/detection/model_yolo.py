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
YOLO model definition for detection.
"""

__all__ = ["yolo_base", "yolo_widerface_pretrained", "yolo_voc_pretrained"]

import pickle

import numpy as np

from keras import Model
from cnn2snn import get_akida_version, AkidaVersion

from ..layer_blocks import yolo_head_block
from ..imagenet.model_akidanet import akidanet_imagenet
from ..utils import fetch_file
from ..model_io import load_model, get_model_path


def yolo_base(input_shape=(224, 224, 3), classes=1, nb_box=5, alpha=1.0, input_scaling=(127.5, -1)):
    """ Instantiates the YOLOv2 architecture.

    Args:
        input_shape (tuple, optional): input shape tuple. Defaults to (224, 224, 3).
        classes (int, optional): number of classes to classify images into. Defaults to 1.
        nb_box (int, optional): number of anchors boxes to use. Defaults to 5.
        alpha (float, optional): controls the width of the model. Defaults to 1.0.
        input_scaling (tuple, optional): scale factor and offset to apply to
            inputs. Defaults to (127.5, -1). Note that following Akida
            convention, the scale factor is a number used as a divisor.

    Returns:
        keras.Model: a Keras Model instance.

    """
    # Create an AkidaNet network without top layers
    base_model = akidanet_imagenet(input_shape=input_shape, alpha=alpha, include_top=False,
                                   input_scaling=input_scaling)

    # Add YOLO top layers to the base model
    input_shape = base_model.input_shape
    x = yolo_head_block(base_model.layers[-1].output, num_boxes=nb_box, classes=classes)
    model = Model(inputs=base_model.input, outputs=x, name='yolo_base')

    # Initialize detection layer weights
    layers = [layer for layer in model.layers if "detection_layer" in layer.name]
    assert len(layers) in (1, 2), "No detection layer found."

    if len(layers) == 1:
        # sepconv is fused on Akida v1
        layer = layers[0]
        detection_weights = layer.get_weights()
        dw_weights_shape = detection_weights[0].shape
        pw_weights_shape = detection_weights[1].shape
        bias_shape = detection_weights[2].shape
    else:
        # sepconv is unfused on Akida v2
        dw_layer = layers[0]
        pw_layer = layers[1]
        dw_weights = dw_layer.get_weights()
        assert len(dw_weights) == 1  # no bias
        pw_weights = pw_layer.get_weights()
        dw_weights_shape = dw_weights[0].shape
        pw_weights_shape = pw_weights[0].shape
        bias_shape = pw_weights[1].shape

    mu, sigma = 0, 0.1

    grid_size = model.output_shape[1:3]
    grid_area = grid_size[0] * grid_size[1]

    dw_kernel = np.random.normal(mu, sigma,
                                 size=dw_weights_shape) / grid_area
    pw_kernel = np.random.normal(mu, sigma,
                                 size=pw_weights_shape) / grid_area
    bias = np.random.normal(mu, sigma,
                            size=bias_shape) / grid_area

    if len(layers) == 1:
        layer.set_weights([dw_kernel, pw_kernel, bias])
    else:
        dw_layer.set_weights([dw_kernel])
        pw_layer.set_weights([pw_kernel, bias])

    return model


def yolo_widerface_pretrained(quantized=True):
    """
    Helper method to retrieve a `yolo_base` model that was trained on WiderFace
    dataset and the anchors that are needed to interpet the model output.

    Args:
        quantized (bool, optional): a boolean indicating whether the model should be loaded
            quantized or not. Defaults to True.

    Returns:
        keras.Model, list: a Keras Model instance and a list of anchors.

    """
    anchors_name = 'widerface_anchors.pkl'
    anchors_path = fetch_file(
        'https://data.brainchip.com/dataset-mirror/widerface/' + anchors_name,
        fname=anchors_name,
        file_hash='325f92336a310d83fed71765436ee343bf3e39cbc12fd099d30677761aee9376',
        cache_subdir='datasets/widerface')
    with open(anchors_path, 'rb') as handle:
        anchors = pickle.load(handle)

    if quantized:
        model_name_v1 = 'yolo_akidanet_widerface_iq8_wq4_aq4.h5'
        file_hash_v1 = 'd55744cbfbbe1131aa26015f38d99f1df7026347bae8f66683259e366e7b6e03'
        model_name_v2 = 'yolo_akidanet_widerface_i8_w8_a8.h5'
        file_hash_v2 = '30ad6408da8a0479b40be2d8b0b1b5caa595cd6d19a2b1c392ad10c315784468'
    else:
        model_name_v1 = 'yolo_akidanet_widerface.h5'
        file_hash_v1 = 'fc1eedb343a97b637f7877a9978d0230962360643578f5fe357034d653b37e44'
        model_name_v2 = 'yolo_akidanet_widerface.h5'
        file_hash_v2 = 'fdb28048d93548956616fe368b6b7f924650a558ea2ed9c3572e774948f6b6e1'

    model_path, model_name, file_hash = get_model_path("yolo", model_name_v1, file_hash_v1,
                                                       model_name_v2, file_hash_v2)
    model_path = fetch_file(model_path,
                            fname=model_name,
                            file_hash=file_hash,
                            cache_subdir='models')

    return load_model(model_path), anchors


def yolo_voc_pretrained(quantized=True):
    """
    Helper method to retrieve a `yolo_base` model that was trained on PASCAL
    VOC2012 dataset for 'person' and 'car' classes only, and the anchors that
    are needed to interpet the model output.

    Args:
        quantized (bool, optional): a boolean indicating whether the model should be loaded
            quantized or not. Defaults to True.

    Returns:
        keras.Model, list: a Keras Model instance and a list of anchors.

    """
    if get_akida_version() == AkidaVersion.v1:
        anchors_name = 'voc_anchors_v1.pkl'
        anchors_path = fetch_file(
            'https://data.brainchip.com/dataset-mirror/voc/' + anchors_name,
            fname=anchors_name,
            file_hash='b1fe1ed12691e100646cf52b1320f05abd17b2f546d3e12cdee87758cc9ed0ba',
            cache_subdir='datasets/voc')
    else:
        anchors_name = 'coco_anchors.pkl'
        anchors_path = fetch_file(
            'https://data.brainchip.com/dataset-mirror/coco/' + anchors_name,
            fname=anchors_name,
            file_hash='36993699182495dd843158583515bd8d1412da978c55286ba0fefa88f5a8cace',
            cache_subdir='datasets/coco')
    with open(anchors_path, 'rb') as handle:
        anchors = pickle.load(handle)

    if quantized:
        model_name_v1 = 'yolo_akidanet_voc_iq8_wq4_aq4.h5'
        file_hash_v1 = 'e65b0b6bd4b08c2796c3bbea89343748195e29e240ce28e70489c53d06ca69d9'
        model_name_v2 = 'yolo_akidanet_voc_i8_w8_a8.h5'
        file_hash_v2 = 'd12826f96d1f3a1b1ff5753b31a1a82afa834ed80fc1a96f5da37e084336a822'
    else:
        model_name_v1 = 'yolo_akidanet_voc.h5'
        file_hash_v1 = '5dff1dd3afafd512e105fa416b444431ca5f816ccc42d9efb49cfa34bd13e91d'
        model_name_v2 = 'yolo_akidanet_voc.h5'
        file_hash_v2 = 'e680e43a136ed3ba23580f4f4bf02be01fdf53d2675fec9c51116e9e79c083ae'

    model_path, model_name, file_hash = get_model_path("yolo", model_name_v1, file_hash_v1,
                                                       model_name_v2, file_hash_v2)
    model_path = fetch_file(model_path,
                            fname=model_name,
                            file_hash=file_hash,
                            cache_subdir='models')

    return load_model(model_path), anchors
