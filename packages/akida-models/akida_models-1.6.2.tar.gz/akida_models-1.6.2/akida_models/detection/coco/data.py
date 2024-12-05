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
Load COCO dataset
"""

__all__ = ["get_coco_dataset"]

import os

try:
    import tensorflow_datasets as tfds
except ImportError:
    tfds = None

from ..data_utils import remove_empty_objects, get_dataset_length


def get_coco_dataset(data_path, training=False):
    """ Loads coco dataset and builds a tf.dataset out of it.

    Args:
        data_path (str): path to the folder containing coco tfrecords.
        training (bool, optional): True to retrieve training data,
            False for validation. Defaults to False.

    Returns:
        tf.dataset, list, int: the requested dataset (train or validation), labels and the dataset
        size.
    """

    assert tfds is not None, "To load coco dataset, tensorflow-datasets module must\
        be installed."

    write_dir = os.path.join(data_path, 'tfds', 'data')

    download_and_prepare_kwargs = {
        'download_dir': os.path.join(write_dir, 'downloaded'),
        'download_config': tfds.download.DownloadConfig(manual_dir=data_path)
    }

    split = 'train' if training else 'validation'

    dataset, infos = tfds.load(
        'coco/2017',
        data_dir=write_dir,
        split=split,
        shuffle_files=training,
        download=True,
        download_and_prepare_kwargs=download_and_prepare_kwargs,
        with_info=True
    )
    dataset = dataset.filter(remove_empty_objects)
    labels = infos.features['objects']['label'].names
    dataset_length = get_dataset_length(dataset)

    return dataset, labels, dataset_length
