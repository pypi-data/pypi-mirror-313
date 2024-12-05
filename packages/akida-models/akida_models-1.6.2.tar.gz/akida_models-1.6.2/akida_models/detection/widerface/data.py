#!/usr/bin/env python
# ******************************************************************************
# Copyright 2024 Brainchip Holdings Ltd.
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
Load Widerface dataset
"""

__all__ = ["get_widerface_dataset"]

import os

import tensorflow as tf

try:
    import tensorflow_datasets as tfds
except ImportError:
    tfds = None

from ..data_utils import Coord, get_dataset_length, remove_empty_objects


def get_widerface_dataset(data_path, training=False):
    """ Loads wider_face dataset and builds a tf.dataset out of it.

    Args:
        data_path (str): path to the folder containing widerface tfrecords.
        training (bool, optional): True to retrieve training data,
            False for validation. Defaults to False.

    Returns:
        tf.dataset, int: the requested dataset (train or validation) and the dataset size.
    """

    assert tfds is not None, "To load wider_face dataset, tensorflow-datasets module must\
        be installed."

    write_dir = os.path.join(data_path, 'tfds')
    download_and_prepare_kwargs = {
        'download_config': tfds.download.DownloadConfig(manual_dir=data_path)
    }

    tfrecords_path = os.path.join(write_dir, 'wider_face')
    if not os.path.exists(tfrecords_path):
        _check_zip_files(data_path)

    split = 'train' if training else 'validation'

    dataset = tfds.load(
        'wider_face',
        data_dir=write_dir,
        split=split,
        shuffle_files=training,
        download_and_prepare_kwargs=download_and_prepare_kwargs
    )

    dataset = dataset.map(_is_valid_box).filter(remove_empty_objects)
    len_dataset = get_dataset_length(dataset)

    return dataset, len_dataset


def _is_valid_box(sample):
    image = sample['image']
    h_img = tf.cast(tf.shape(image)[0], tf.float32)
    w_img = tf.cast(tf.shape(image)[1], tf.float32)

    objects = sample['faces']
    bbox = objects['bbox']
    objects['label'] = tf.fill([tf.shape(objects['bbox'])[0]], 0)

    w_box = ((bbox[:, Coord.x2] - bbox[:, Coord.x1])) * w_img
    h_box = ((bbox[:, Coord.y2] - bbox[:, Coord.y1])) * h_img

    box_area = w_box * h_box
    img_area = w_img * h_img
    mask = box_area >= img_area / 60.0

    new_sample = {
        'image': image,
        'objects': {
            'bbox': objects['bbox'][mask],
            'label': objects['label'][mask],
        }
    }

    return new_sample


def _check_zip_files(data_path):
    zip_files = [
        "wider_face_split.zip",
        "WIDER_train.zip",
        "WIDER_val.zip",
        "WIDER_test.zip",
    ]
    for zip_file in zip_files:
        zip_path = os.path.join(data_path, zip_file)
        if not os.path.exists(zip_path):
            raise FileNotFoundError(
                f"Zip file {zip_file} not found in the specified data_path. "
                "Data can be downloaded at http://shuoyang1213.me/WIDERFACE/"
            )
