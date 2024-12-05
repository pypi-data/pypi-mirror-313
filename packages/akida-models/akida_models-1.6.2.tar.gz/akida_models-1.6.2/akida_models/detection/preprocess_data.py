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
Apply transformations on images and labels
"""

__all__ = ["preprocess_dataset"]


import numpy as np
import tensorflow as tf

from .data_augmentation import (augment_sample,
                                init_random_vars,
                                fix_obj_position_and_size)
from .processing import get_affine_transform, preprocess_image


def _to_tensor(image, objects):
    image = tf.convert_to_tensor(image, dtype=tf.float32)
    objects['bbox'] = tf.convert_to_tensor(objects['bbox'], dtype=tf.float32)
    objects['label'] = tf.convert_to_tensor(objects['label'], dtype=tf.int32)

    return image, objects


def _to_numpy(image, objects):
    image = image.numpy()
    objects['bbox'] = objects['bbox'].numpy()
    objects['label'] = objects['label'].numpy()

    return image, objects


def _to_absolute_coord(boxes, h, w):
    return boxes * np.array([h, w, h, w])


def _to_relative_coord(boxes, h, w):
    return boxes / np.array([h, w, h, w])


def preprocess(image, objects, aug_pipe, labels, input_shape, training, preserve_aspect_ratio):
    """
    Preprocesses an image and its associated objects.

    Args:
        image (np.ndarray): the input image as a NumPy array.
        objects (dict): dictionary containing information about objects in the image,
            including labels and bounding boxes.
        aug_pipe (iaa.Augmenter): the augmentation pipeline.
        labels (list): list of labels of interest.
        input_shape (tuple): the desired input shape for the image.
        training (bool): enable training in the augmentation pipeline.
        preserve_aspect_ratio (bool): Whether aspect ratio is preserved during resizing or not.

    Returns:
        np.ndarray, dict: processed image and objects.
    """
    image, objects = _to_numpy(image, objects)

    h, w, _ = image.shape
    # Transform bbox coordinates to absolute so they are compatible with imgaug
    objects['bbox'] = _to_absolute_coord(objects['bbox'], h, w)
    flip, scale, offx, offy = init_random_vars(h, w)

    if training:
        augmented_image, augmented_objects = augment_sample(image, objects, aug_pipe, labels,
                                                            flip, scale, offx, offy)
        # Due to some transformation, some bboxes get deleted which throws an error in the next
        # steps. A quick fix is to not augment these images.
        if len(augmented_objects['bbox']) != 0:
            image = augmented_image
            objects = augmented_objects

    affine_transform = None
    if preserve_aspect_ratio:
        # We compute the affine transformation from the center point
        center = np.array([w / 2., h / 2.], dtype=np.float32)
        affine_transform = get_affine_transform(center, [w, h],
                                                [input_shape[1], input_shape[0]])

    image = preprocess_image(image, input_shape, affine_transform)
    objects = fix_obj_position_and_size(
        objects, h, w, input_shape, scale, offx, offy, training, flip, affine_transform)

    # Transform bbox coordinates back to relative
    objects['bbox'] = _to_relative_coord(objects['bbox'], input_shape[0], input_shape[1])
    image, objects = _to_tensor(image, objects)

    return image, objects


def preprocess_dataset(dataset,
                       input_shape,
                       grid_size,
                       labels,
                       batch_size,
                       aug_pipe,
                       create_targets_fn,
                       training=True,
                       preserve_aspect_ratio=False,
                       *args,
                       **kwargs):
    """
    Preprocesses the input dataset by applying the necessary image and label transformations.

    Args:
        dataset (tf.data.Dataset): The input dataset.
        input_shape (tuple): The desired input shape for the image.
        grid_size (tuple): The grid size used for YOLO target generation.
        labels (list[str]): List of class labels.
        batch_size (int): Batch size for the preprocessed dataset.
        aug_pipe (iaa.Augmenter): The augmentation pipeline.
        create_targets_fn (callable): Function for creating target labels.
            It should accept the following parameters: objects, grid_size, num_classes
            and others arguments such as anchors.
        training (bool, optional): Flag indicating whether the dataset is
            for training or not. Defaults to True.
        preserve_aspect_ratio (bool, optional): Whether aspect ratio is preserved
            during resizing. Defaults to False.

    Returns:
        dataset (tf.data.Dataset): The preprocessed dataset.
    """
    def preprocess_sample(sample):
        def _apply_transformation(image, bbox, label):
            objects = {'bbox': bbox, 'label': label}
            image, objects = preprocess(image, objects, aug_pipe, labels,
                                        input_shape, training, preserve_aspect_ratio)
            return image, objects['bbox'], objects['label']

        image, bbox, label = tf.py_function(_apply_transformation,
                                            inp=[sample['image'],
                                                 sample['objects']['bbox'],
                                                 sample['objects']['label']],
                                            Tout=[tf.float32, tf.float32, tf.int32])

        # Set the shape of the image to avoid unknown shape errors
        image.set_shape(input_shape)
        objects = {'bbox': bbox, 'label': label}
        targets = create_targets_fn(objects, grid_size, len(labels), *args, **kwargs)

        return image, targets

    if training:
        dataset = (dataset.shuffle(8 * batch_size)
                          .map(preprocess_sample, num_parallel_calls=tf.data.experimental.AUTOTUNE)
                          .batch(batch_size=batch_size, drop_remainder=True)
                          .repeat()
                          .prefetch(buffer_size=tf.data.experimental.AUTOTUNE))
    else:
        dataset = (dataset.map(preprocess_sample, num_parallel_calls=tf.data.experimental.AUTOTUNE)
                          .batch(batch_size=batch_size, drop_remainder=True))

    return dataset
