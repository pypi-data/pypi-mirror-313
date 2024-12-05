#!/usr/bin/env python
# coding: utf-8
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
Helper to load 10 samples of ImageNet-like data.
"""
__all__ = ["get_preprocessed_samples"]

import csv
import os

import numpy as np
from tensorflow.image import decode_jpeg
from tensorflow.io import read_file

from akida_models.imagenet import preprocessing
from akida_models.utils import fetch_file


def get_preprocessed_samples(image_size=224, num_channels=3):
    """
    Load and preprocess a 10 ImageNet-like images for testing.

    Args:
        image_size (int, optional): The target size for the images. Defaults to 224.
        num_channels (int, optional): The number of channels in the images. Defaults to 3.

    Returns:
        x_test, labels_test (tuple): 4D and 1D numpy array of the preprocessed images and their
                        corresponding labels
    """
    num_images = 10

    file_path = fetch_file(
        fname="imagenet_like.zip",
        origin="https://data.brainchip.com/dataset-mirror/imagenet_like/imagenet_like.zip",
        cache_subdir='datasets/imagenet_like',
        extract=True)

    data_folder = os.path.dirname(file_path)
    x_test, x_test_files = _get_images(data_folder, num_images, image_size, num_channels)
    labels_test = _get_labels(data_folder, num_images, x_test_files)

    return x_test, labels_test


def _get_images(data_folder, num_images, image_size, num_channels):
    """
    Load and preprocess ImageNet-like test images.

    Args:
        data_folder (str): Folder where images are located.
        num_images (int): Number of images to load.
        image_size (int): Target size for the images.
        num_channels (int): Number of channels in the images.

    Returns:
        Tuple (`np.ndarray`, List[str]): Preprocessed images and corresponding file names.
    """
    # Load images for test set
    x_test_files = []
    x_test = np.zeros((num_images, image_size, image_size, num_channels)).astype('uint8')

    for idx in range(num_images):
        test_file = 'image_' + str(idx + 1).zfill(2) + '.jpg'
        x_test_files.append(test_file)
        img_path = os.path.join(data_folder, test_file)
        base_image = read_file(img_path)
        image = decode_jpeg(base_image, channels=num_channels)
        image = preprocessing.preprocess_image(image, (image_size, image_size))
        x_test[idx, :, :, :] = np.expand_dims(image, axis=0)

    return x_test, x_test_files


def _get_labels(data_folder, num_images, x_test_files):
    """
    Parse labels file for ImageNet-like test samples.

    Args:
        data_folder (str): Folder where labels file is located.
        num_images (int): Number of images.
        x_test_files (List[str]): List of file names for test samples.

    Returns:
        labels_test (np.ndarray): NumPy array of labels for the test samples.
    """
    # Parse labels file
    fname = os.path.join(data_folder, 'labels_validation.txt')
    validation_labels = dict()

    with open(fname, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ')
        for row in reader:
            validation_labels[row[0]] = row[1]

    # Get labels for the test set by index
    labels_test = np.zeros(num_images)
    for i in range(num_images):
        labels_test[i] = int(validation_labels[x_test_files[i]])

    return labels_test
