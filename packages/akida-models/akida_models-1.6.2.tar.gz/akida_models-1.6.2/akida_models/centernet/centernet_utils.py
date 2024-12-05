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
Utils for Centernet.
"""

__all__ = ['build_centernet_aug_pipeline', 'create_centernet_targets']


import tensorflow as tf
from imgaug import augmenters as iaa

from ..detection.data_utils import Coord
from ..detection.box_utils import compute_center_wh, compute_center_xy


def _gaussian2D(radius, sigma=1, eps=tf.keras.backend.epsilon()):
    """Generate 2D gaussian kernel.

    Args:
        radius (int): Radius of gaussian kernel.
        sigma (int, optional): Sigma of gaussian function. Defaults to 1.
        eps (float, optional): Epsilon value. Defaults to 1e-7.

    Returns:
        tf.Tensor: Gaussian kernel with a `(2 * radius + 1) x (2 * radius + 1)` shape.
    """
    x = tf.reshape(tf.range(-radius, radius + 1, dtype=tf.float32), [1, -1])
    y = tf.reshape(tf.range(-radius, radius + 1, dtype=tf.float32), [-1, 1])
    h = tf.exp(-(x * x + y * y) / tf.cast((2 * sigma * sigma), dtype=tf.float32))

    # Clamp smaller values to zero
    h = tf.where(h < (eps * tf.reduce_max(h)), 0.0, h)

    return h


def _gen_gaussian_target(heatmap, center, obj_idx, radius):
    """Generate 2D gaussian heatmap.

    Args:
        heatmap (tf.Tensor): Input heatmap, the gaussian kernel will cover on it and maintain
            the max value.
        center (list[int]): Coordinates of gaussian kernel's center.
        obj_idx (int): The class index for the center point.
        radius (int): Radius of gaussian kernel.

    Returns:
        out_heatmap (tf.Tensor): Updated heatmap covered by gaussian kernel.

    Note:
        Taken from pytorch
    """
    diameter = 2 * radius + 1
    gaussian_kernel = _gaussian2D(radius, sigma=diameter / 6)
    x, y = center
    height = tf.shape(heatmap)[0]
    width = tf.shape(heatmap)[1]

    # Find the smallest value so that if the point is near the edge we don't end outside
    # (e.g. x = 3 and radius is 10, then we go from the x-3 to x+10)
    left = tf.minimum(x, radius)
    right = tf.minimum(width - x, radius + 1)
    top = tf.minimum(y, radius)
    bottom = tf.minimum(height - y, radius + 1)

    # Compare the gaussian kernel to the heatmap (in case there's already a point of
    # interest there) and keep the max value
    flattened_kernel = tf.reshape(gaussian_kernel, [-1])

    # Range the dimensions
    # Generate the grid of indices
    d0_range = tf.range(y - top, y + bottom)
    d1_range = tf.range(x - left, x + right)
    d1_grid, d0_grid = tf.meshgrid(d1_range, d0_range)

    # Flatten the grid of indices
    indices = tf.reshape(
        tf.stack([d1_grid, d0_grid, tf.fill(tf.shape(d0_grid), obj_idx)], axis=-1), (-1, 3))

    # Update heatmap
    heatmap = tf.tensor_scatter_nd_update(heatmap, indices, flattened_kernel)
    return heatmap


def _gaussian_radius(det_size, min_overlap):
    r"""Generate 2D gaussian radius.

    This function is modified from the `official github repo
    <https://github.com/princeton-vl/CornerNet-Lite/blob/master/core/sample/
    utils.py#L65>`_.

    Given ``min_overlap``, radius could computed by a quadratic equation
    according to Vieta's formulas.

    There are 3 cases for computing gaussian radius, details are following:

    - Case 1: one corner is inside the gt box and the other is outside.

    .. code:: text

        |<   width   >|

        lt-+----------+         -
        |  |          |         ^
        +--x----------+--+
        |  |          |  |
        |  |          |  |    height
        |  | overlap  |  |
        |  |          |  |
        |  |          |  |      v
        +--+---------br--+      -
        |          |  |
        +----------+--x

    To ensure IoU of generated box and gt box is larger than ``min_overlap``:

    .. math::
        \cfrac{(w-r)*(h-r)}{w*h+(w+h)r-r^2} \ge {iou} \quad\Rightarrow\quad
        {r^2-(w+h)r+\cfrac{1-iou}{1+iou}*w*h} \ge 0 \\
        {a} = 1,\quad{b} = {-(w+h)},\quad{c} = {\cfrac{1-iou}{1+iou}*w*h}
        {r} \le \cfrac{-b-\sqrt{b^2-4*a*c}}{2*a}

    - Case 2: both two corners are inside the gt box.

    .. code:: text

        |<   width   >|

        lt-+----------+         -
        |  |          |         ^
        +--x-------+  |
        |  |       |  |
        |  |overlap|  |       height
        |  |       |  |
        |  +-------x--+
        |          |  |         v
        +----------+-br         -

    To ensure IoU of generated box and gt box is larger than ``min_overlap``:

    .. math::
        \cfrac{(w-2*r)*(h-2*r)}{w*h} \ge {iou} \quad\Rightarrow\quad
        {4r^2-2(w+h)r+(1-iou)*w*h} \ge 0 \\
        {a} = 4,\quad {b} = {-2(w+h)},\quad {c} = {(1-iou)*w*h}
        {r} \le \cfrac{-b-\sqrt{b^2-4*a*c}}{2*a}

    - Case 3: both two corners are outside the gt box.

    .. code:: text

        |<   width   >|

        x--+----------------+
        |  |                |
        +-lt-------------+  |   -
        |  |             |  |   ^
        |  |             |  |
        |  |   overlap   |  | height
        |  |             |  |
        |  |             |  |   v
        |  +------------br--+   -
        |                |  |
        +----------------+--x

    To ensure IoU of generated box and gt box is larger than ``min_overlap``:

    .. math::
        \cfrac{w*h}{(w+2*r)*(h+2*r)} \ge {iou} \quad\Rightarrow\quad
        {4*iou*r^2+2*iou*(w+h)r+(iou-1)*w*h} \le 0 \\
        {a} = {4*iou},\quad {b} = {2*iou*(w+h)},\quad {c} = {(iou-1)*w*h} \\
        {r} \le \cfrac{-b+\sqrt{b^2-4*a*c}}{2*a}

    Args:
        det_size (list[int]): Shape of object.
        min_overlap (float): Min IoU with ground truth for boxes generated by
            keypoints inside the gaussian kernel.

    Returns:
        radius (tf.Tensor): Radius of gaussian kernel.

    Notes:
        Explanation of figure: ``lt`` and ``br`` indicates the left-top and bottom-right
        corner of ground truth box. ``x`` indicates the generated corner at the limited
        position when ``radius=r``.
    """
    height, width = det_size

    a1 = 1
    b1 = (height + width)
    c1 = width * height * (1 - min_overlap) / (1 + min_overlap)
    sq1 = tf.sqrt(b1**2 - 4 * a1 * c1)
    r1 = (b1 - sq1) / (2 * a1)

    a2 = 4
    b2 = 2 * (height + width)
    c2 = (1 - min_overlap) * width * height
    sq2 = tf.sqrt(b2**2 - 4 * a2 * c2)
    r2 = (b2 - sq2) / (2 * a2)

    a3 = 4 * min_overlap
    b3 = -2 * min_overlap * (height + width)
    c3 = (min_overlap - 1) * width * height
    sq3 = tf.sqrt(b3**2 - 4 * a3 * c3)
    r3 = (b3 + sq3) / (2 * a3)

    return tf.reduce_min([r1, r2, r3])


def build_centernet_aug_pipeline():
    """ Defines a sequence of augmentation steps for Centernet training
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
            sometimes(iaa.Affine(rotate=0)),
            # execute 0 to 5 of the following (less important) augmenters
            # per image. Don't execute all of them, as that would often be
            # way too strong
            iaa.SomeOf(
                (0, 5),
                [
                    iaa.OneOf([
                        # blur images with a sigma between 0 and 3.0
                        iaa.GaussianBlur((0, 3.0)),
                        # blur image using local means (kernel sizes between 2 and 7)
                        iaa.AverageBlur(k=(2, 7)),
                        # blur image using local medians (kernel sizes between 3 and 11)
                        iaa.MedianBlur(k=(3, 11)),
                    ]),
                    # sharpen images
                    iaa.Sharpen(alpha=(0, 1.0), lightness=(0.75, 1.5)),
                    iaa.LinearContrast((0.5, 2.0), per_channel=0.5),
                    iaa.AdditiveGaussianNoise(loc=0, scale=(0.0, 0.05 * 255), per_channel=0.5),
                    # randomly remove up to 10% of the pixels
                    iaa.OneOf([iaa.Dropout((0.01, 0.1), per_channel=0.5),
                               iaa.CoarseDropout((0.01, 0.05), size_percent=0.5)]),
                    # change brightness of images
                    iaa.Add((-10, 10), per_channel=0.5),
                    iaa.Multiply((0.5, 1.5), per_channel=0.5),
                    iaa.OneOf([
                        iaa.pillike.Equalize(),
                        iaa.pillike.Autocontrast()
                    ])
                ], random_order=True)
        ],
        random_order=True)


def create_centernet_targets(objects,
                             grid_size,
                             num_classes):
    """
    Creates Centernet-style targets tensor for the given objects.

    Args:
        objects (dict): Dictionary containing information about objects in the image,
            including labels and bounding boxes.
        grid_size (tuple): The grid size used for Centernet target generation.
        num_classes (int): The number of classes.

    Returns:
        targets (tf.Tensor): The targets output tensor.
    """
    targets = tf.zeros((grid_size[0], grid_size[1], 2 + 2 + num_classes), dtype=tf.float32)
    num_objects = tf.shape(objects['label'])[0]

    for idx in range(num_objects):
        bbox = objects['bbox'][idx]
        if bbox[Coord.x2] > bbox[Coord.x1] and bbox[Coord.y2] > bbox[Coord.y1]:
            center_x, center_y = compute_center_xy(bbox, grid_size)

            # find grid index where the center is located
            grid_x = tf.cast(center_x, tf.int32)
            grid_y = tf.cast(center_y, tf.int32)

            if grid_x < grid_size[1] and grid_y < grid_size[0]:
                obj_indx = objects['label'][idx]

                center_w, center_h = compute_center_wh(bbox, grid_size)
                # get the center point and use a gaussian kernel as the target
                radius = _gaussian_radius([center_h, center_w], min_overlap=0.3)
                # check that the radius is positive
                radius = tf.maximum(tf.cast(radius, dtype=tf.int32), 0)
                heatmap = tf.zeros(
                    (grid_size[0], grid_size[1], num_classes)
                )
                heatmap = _gen_gaussian_target(heatmap, [grid_y, grid_x], obj_indx, radius)

                # update targets heatmap
                indices = [[i, j, k] for i in range(grid_size[0]) for j in range(
                    grid_size[1]) for k in range(num_classes)]
                updates = tf.gather_nd(params=heatmap, indices=indices)
                targets = tf.tensor_scatter_nd_add(targets, indices, updates)

                # update targets width
                targets = tf.tensor_scatter_nd_update(
                    targets, [[grid_y, grid_x, num_classes]], [center_w])

                # update targets height
                targets = tf.tensor_scatter_nd_update(
                    targets, [[grid_y, grid_x, num_classes + 1]], [center_h])

                # update targets center x
                targets = tf.tensor_scatter_nd_update(
                    targets,
                    [[grid_y, grid_x, num_classes + 2]],
                    [center_x - tf.cast(grid_x, dtype=tf.float32)])

                # update targets center y
                targets = tf.tensor_scatter_nd_update(
                    targets,
                    [[grid_y, grid_x, num_classes + 3]],
                    [center_y - tf.cast(grid_y, dtype=tf.float32)])

    return targets
