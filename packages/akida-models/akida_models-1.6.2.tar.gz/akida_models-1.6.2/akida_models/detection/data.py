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
Loads detection datasets (VOC, Widerface, COCO).
"""
__all__ = ["get_detection_datasets"]


from .voc.data import get_voc_dataset
from .widerface.data import get_widerface_dataset
from .coco.data import get_coco_dataset


def _get_voc_data(data_path, labels_of_interest):
    train_data, labels, num_train = get_voc_dataset(data_path,
                                                    labels=labels_of_interest,
                                                    training=True)
    valid_data, labels, num_valid = get_voc_dataset(data_path,
                                                    labels=labels_of_interest,
                                                    training=False)

    return train_data, valid_data, labels, num_train, num_valid


def _get_widerface_data(data_path):
    train_data, num_train = get_widerface_dataset(data_path,
                                                  training=True)
    valid_data, num_valid = get_widerface_dataset(data_path,
                                                  training=False)

    return train_data, valid_data, num_train, num_valid


def _get_coco_data(data_path):
    train_data, labels, num_train = get_coco_dataset(data_path,
                                                     training=True)
    valid_data, _, num_valid = get_coco_dataset(data_path,
                                                training=False)

    return train_data, valid_data, labels, num_train, num_valid


def get_detection_datasets(data_path, dataset_name, full_set=True):
    """ Loads VOC, Widerface or COCO data.

    Args:
        data_path (str): path to the folder containing tfrecords files
            for VOC, Widerface or COCO data.
        dataset_name (str): Name of the dataset. Choices in [coco, voc, widerface].
        full_set (bool, optional): When dataset is 'voc', set to False to limit to 'car' and
            'person' labels. Defaults to True.

    Returns:
        tf.dataset, tf.dataset, list, int, int: train and validation data, labels, sizes of train
        and validation data.
    """
    if dataset_name == "voc":
        if full_set:
            labels_of_interest = ['aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus',
                                  'car', 'cat', 'chair', 'cow', 'diningtable', 'dog', 'horse',
                                  'motorbike', 'person', 'pottedplant', 'sheep', 'sofa',
                                  'train', 'tvmonitor']
        else:
            labels_of_interest = ['car', 'person']
        train_data, valid_data, labels, num_train, num_valid = _get_voc_data(data_path,
                                                                             labels_of_interest)
    elif dataset_name == "coco":
        train_data, valid_data, labels, num_train, num_valid = _get_coco_data(data_path)

    elif dataset_name == "widerface":
        labels = ["face"]
        train_data, valid_data, num_train, num_valid = _get_widerface_data(data_path)

    else:
        raise ValueError(f"Invalid dataset name : {dataset_name}. It has to be from "
                         f"[voc, coco, widerface].")

    return train_data, valid_data, labels, num_train, num_valid
