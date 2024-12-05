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
Utils for VOC and Widerface datasets.
"""

__all__ = ["Coord", "remove_empty_objects", "get_dataset_length"]

import tensorflow as tf


class Coord:
    """
    Static class representing bounding box coordinates.

    These values align with the TensorFlow Datasets (tfds) bounding box format.
    In tfds, the "bbox" feature is formatted as :
    tfds.features.BBox(ymin / height, xmin / width, ymax / height, xmax / width).
    """
    x1 = 1
    x2 = 3
    y1 = 0
    y2 = 2


def remove_empty_objects(sample):
    """
    Remove samples with empty objects.

    Args:
        sample (dict): A dictionary representing a sample with object information.
            {'image', 'objects': {'bbox', 'label'}}.

    Returns:
        tf.Tensor: A boolean tensor indicating whether the sample has non-empty objects.
    """
    is_empty = tf.reduce_all(tf.equal(tf.shape(sample['objects']['bbox'])[0], 0))
    return tf.math.logical_not(is_empty)


def get_dataset_length(dataset):
    """
    Get the length of a TF dataset.

    Args:
        dataset (tf.data.Dataset): A TF dataset containing elements.

    Returns:
        int: The number of elements in the dataset.
    """
    count = 0
    for _ in dataset:
        count += 1
    return count
