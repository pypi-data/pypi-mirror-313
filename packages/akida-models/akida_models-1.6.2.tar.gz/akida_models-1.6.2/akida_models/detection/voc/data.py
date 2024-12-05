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
Load VOC dataset
"""

__all__ = ["get_voc_dataset"]

import os

import tensorflow as tf

try:
    import tensorflow_datasets as tfds
except ImportError:
    tfds = None

from ..data_utils import get_dataset_length, remove_empty_objects


def get_voc_dataset(data_path, labels=["car", "person"], training=False):
    """ Loads voc dataset and builds a tf.dataset out of it.

    Args:
        data_path (str): path to the folder containing voc tar files
        labels (list[str], optional): list of labels of interest as strings.
             Defaults to ["car", "person"].
        training (bool, optional): True to retrieve training data,
            False for validation. Defaults to False.

    Returns:
        tf.dataset, labels (list[str]), int: the requested dataset (train or validation), the
        list of labels and the dataset size.
    """

    assert tfds is not None, "To load voc dataset, tensorflow-datasets module must\
        be installed."

    write_dir = os.path.join(data_path, 'tfds')

    download_and_prepare_kwargs = {
        'download_config': tfds.download.DownloadConfig(manual_dir=data_path)
    }

    tfrecords_path = os.path.join(write_dir, 'data', 'voc')
    if not os.path.exists(tfrecords_path):
        _check_zip_files(data_path)

    split = 'train+validation' if training else 'test'
    data_dir = os.path.join(write_dir, 'data')

    if training:
        (dataset12), infos = tfds.load("voc/2012",
                                       split=split,
                                       with_info=True,
                                       data_dir=data_dir,
                                       shuffle_files=training,
                                       download_and_prepare_kwargs=download_and_prepare_kwargs)
        (dataset07), _ = tfds.load("voc/2007",
                                   split=split,
                                   with_info=True,
                                   data_dir=data_dir,
                                   shuffle_files=training,
                                   download_and_prepare_kwargs=download_and_prepare_kwargs)
        dataset = dataset12.concatenate(dataset07)
    else:
        dataset, infos = tfds.load("voc/2007",
                                   split=split,
                                   with_info=True,
                                   data_dir=data_dir,
                                   shuffle_files=training,
                                   download_and_prepare_kwargs=download_and_prepare_kwargs)

    voc_labels = infos.features['labels'].names
    dataset = (dataset
               .map(lambda x: _filter_labels(x, labels, voc_labels))
               .map(_filter_difficult_labels)
               .filter(remove_empty_objects))

    num_samples = get_dataset_length(dataset)

    return dataset, labels, num_samples


def _filter_labels(sample, labels_of_interest, voc_labels):
    objects = sample['objects']
    labels_indices = [voc_labels.index(label) for label in labels_of_interest]
    labels_tensor = tf.constant(labels_indices, dtype=tf.int64)

    # Map label indices to indices in labels_of_interest
    def _map_labels(label):
        return tf.where(tf.equal(labels_tensor, label))[0][0]

    mask = tf.reduce_any(tf.equal(objects['label'][:, tf.newaxis], labels_indices), axis=1)
    mapped_labels = tf.map_fn(_map_labels, objects['label'][mask], fn_output_signature=tf.int64)

    # Filter the object to include only the objects of interest
    filtered_objects = {
        'bbox': objects['bbox'][mask],
        'is_difficult': objects['is_difficult'][mask],
        'is_truncated': objects['is_truncated'][mask],
        'label': mapped_labels,
        'pose': objects['pose'][mask]
    }
    sample['labels'] = filtered_objects['label']
    sample['labels_no_difficult'] = filtered_objects['is_difficult']
    sample['objects'] = filtered_objects

    return sample


def _filter_difficult_labels(sample):
    objects = sample['objects']
    mask = tf.math.logical_not(sample['labels_no_difficult'])

    # Filter the 'objects' with is_difficult is False
    filtered_objects = {
        'bbox': objects['bbox'][mask],
        'label': objects['label'][mask],
    }

    new_sample = {
        'image': sample['image'],
        'objects': filtered_objects
    }

    return new_sample


def _check_zip_files(data_path):
    zip_files = [
        "VOC2012test.tar",
        "VOCtest_06-Nov-2007.tar",
        "VOCtrainval_06-Nov-2007.tar",
        "VOCtrainval_11-May-2012.tar"
    ]
    for zip_file in zip_files:
        zip_path = os.path.join(data_path, zip_file)
        if not os.path.exists(zip_path):
            raise FileNotFoundError(
                f"Zip file {zip_file} not found in the specified data_path. "
                "Data can be downloaded at http://host.robots.ox.ac.uk/pascal/VOC/"
            )
