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
Data augmentation for object detection
"""
__all__ = ['augment_sample', 'build_yolo_aug_pipeline', 'init_random_vars']

import cv2
import numpy as np
from imgaug import augmenters as iaa
from imgaug.augmentables.bbs import BoundingBoxesOnImage, BoundingBox as BoundingBoxAug

from .data_utils import Coord
from .processing import apply_affine_transform_to_bboxes


def augment_sample(image, objects, aug_pipe, labels, flip, scale, offx, offy):
    """
    Applies data augmentation to an image and its associated objects.

    Args:
        image (np.ndarray): the input image as a NumPy array.
        objects (dict): dictionary containing information about objects in the image,
            including labels and bounding boxes.
        aug_pipe (iaa.Augmenter): the augmentation pipeline.
        labels (list): list of labels of interest.
        flip (bool): binary value indicating whether to flip the image or not.
        scale (float): scaling factor for the image.
        offx (int): horizontal translation offset for the image.
        offy (int): vertical translation offset for the image.

    Returns:
        np.ndarray, dict: augmented image and objects.
    """
    h, w, _ = image.shape

    # Scale the image
    image = cv2.resize(image, (0, 0), fx=scale, fy=scale)

    # Translate the image
    image = image[offy:(offy + h), offx:(offx + w)]

    if flip:
        image = cv2.flip(image, 1)

    bbs = _objects_to_bbox(objects, labels, image.shape)
    image, bbs = aug_pipe(image=image, bounding_boxes=bbs)
    bbs.remove_out_of_image().clip_out_of_image()
    objects = _bbox_to_objects(bbs, labels)

    return image, objects


def _objects_to_bbox(objects, labels, image_shape):
    """
    Transforms objects bounding boxes from numpy array to BoundingBox format from imgaug library.

    Args:
        objects (dict): dictionary containing information about objects in the image,
            including labels and bounding boxes.
        labels (list): list of labels of interest.
        image_shape (tuple): the shape of the image on which the objects are placed.

    Returns:
        BoundingBoxesOnImage: BoundingBoxesOnImage object from imgaug library containing
            bounding boxes coordinates with their label.
    """
    boxes = objects['bbox']
    formattedbox = [BoundingBoxAug(x1=box[Coord.x1],
                                   y1=box[Coord.y1],
                                   x2=box[Coord.x2],
                                   y2=box[Coord.y2],
                                   label=labels[objects['label'][idx]])
                    for idx, box in enumerate(boxes)]

    return BoundingBoxesOnImage(formattedbox, shape=image_shape)


def _bbox_to_objects(boxes, labels):
    """
    Extracts bounding boxes from imgaug objects to a dictionary containing
        bounding box coordinates and corresponding labels.

    Args:
        boxes (list): list of imgaug bounding boxes.
        labels (list): list of labels of interest.

    Returns:
        dict: dictionary containing information about objects in the image,
            including labels and bounding boxes.
    """
    return {
        'bbox': [[bbox.y1, bbox.x1, bbox.y2, bbox.x2] for bbox in boxes],
        'label': [labels.index(box.label) for box in boxes]
    }


def init_random_vars(h, w):
    """
    Initialize random variables for data augmentation.

    Args:
        h (int): height of the input image.
        w (int): width of the input image.

    Returns:
        (bool, float, int, int): flip, scale, offx, offy.
    """
    rng = np.random.default_rng()

    flip = rng.choice(a=[False, True])
    scale = rng.uniform() / 10. + 1.

    max_offx = (scale - 1.) * w
    max_offy = (scale - 1.) * h
    offx = int(rng.uniform() * max_offx)
    offy = int(rng.uniform() * max_offy)

    return flip, scale, offx, offy


def fix_obj_position_and_size(objects, h, w, input_shape,
                              scale, offx, offy, training, flip, affine_transform=None):
    """
    Adjust object positions and sizes based on augmentation parameters.

    Args:
        objects (dict): dictionary containing information about objects in the image,
            including labels and bounding boxes.
        h (int): height of the input image.
        w (int): width of the input image.
        input_shape (tuple): the desired input shape for the image.
        scale (float): scaling factor for the image.
        offx (int): horizontal offset for translation.
        offy (int): vertical offset for translation.
        training (bool, optional): True to augment training data,
            False for validation.
        flip (bool): binary value indicating whether to flip the image or not.
        affine_transform (np.ndarray, optional): A 2x3 affine transformation matrix.
            Defaults to None.

    Returns:
        dict: updated objects information.
    """
    def _resize_bboxes(bboxes, input_h, input_w, affine_transform=None):
        if affine_transform is not None:
            bboxes = apply_affine_transform_to_bboxes(bboxes, affine_transform)
        else:
            raw_target_size_aspect_ratios = np.array([float(input_shape[0]) / h,
                                                      float(input_shape[1]) / w,
                                                      float(input_shape[0]) / h,
                                                      float(input_shape[1]) / w])
            bboxes = (bboxes * raw_target_size_aspect_ratios).astype(int)

        bboxes = np.clip(bboxes, 0, [input_h-1, input_w-1, input_h-1, input_w-1])

        return bboxes

    boxes = np.array(objects['bbox'])
    offset = np.array([offy, offx, offy, offx])

    if training:
        boxes = (boxes * scale - offset).astype(int)

    boxes = _resize_bboxes(boxes, input_shape[0], input_shape[1], affine_transform)

    if training and flip:
        xmin = boxes[:, Coord.x1].copy()
        boxes[:, Coord.x1] = input_shape[1] - boxes[:, Coord.x2]
        boxes[:, Coord.x2] = input_shape[1] - xmin

    objects['bbox'] = boxes

    return objects


def build_yolo_aug_pipeline():
    """ Defines a sequence of augmentation steps for Yolo training
    that will be applied to every image.

    Returns:
        iaa.Sequential: sequence of augmentation.
    """
    # augmentors by https://github.com/aleju/imgaug
    def sometimes(aug): return iaa.Sometimes(0.5, aug)

    # All augmenters with per_channel=0.5 will sample one value per
    # image in 50% of all cases. In all other cases they will sample new
    # values per channel.
    return iaa.Sequential(
        [
            # apply the following augmenters to most images
            sometimes(iaa.Affine()),
            # execute 0 to 5 of the following (less important) augmenters
            # per image. Don't execute all of them, as that would often be
            # way too strong
            iaa.SomeOf(
                (0, 5),
                [
                    iaa.OneOf([
                        # blur images with a sigma between 0 and 3.0
                        iaa.GaussianBlur((0, 3.0)),
                        # blur image using local means (kernel sizes between
                        # 2 and 7)
                        iaa.AverageBlur(k=(2, 7)),
                        # blur image using local medians (kernel sizes
                        # between 3 and 11)
                        iaa.MedianBlur(k=(3, 11)),
                    ]),
                    # sharpen images
                    iaa.Sharpen(alpha=(0, 1.0), lightness=(0.75, 1.5)),
                    # add gaussian noise
                    iaa.AdditiveGaussianNoise(
                        loc=0, scale=(0.0, 0.05 * 255), per_channel=0.5),
                    # randomly remove up to 10% of the pixels
                    iaa.OneOf([
                        iaa.Dropout((0.01, 0.1), per_channel=0.5),
                    ]),
                    # change brightness of images
                    iaa.Add((-10, 10), per_channel=0.5),
                    # change brightness of images
                    iaa.Multiply((0.5, 1.5), per_channel=0.5),
                    # improve or worsen the contrast
                    iaa.LinearContrast((0.5, 2.0), per_channel=0.5),
                ],
                random_order=True)
        ],
        random_order=True)
