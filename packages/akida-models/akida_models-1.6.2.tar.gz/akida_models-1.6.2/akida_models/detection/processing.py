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
Processing tools for YOLO data handling.
"""

__all__ = ["BoundingBox", "load_image", "preprocess_image", "get_affine_transform",
           "apply_affine_transform_to_bboxes", "desize_bboxes", "decode_output",
           "create_yolo_targets"]


import cv2
import numpy as np
import tensorflow as tf
from .data_utils import Coord
from .box_utils import compute_center_wh, compute_center_xy


class BoundingBox:
    """ Utility class to represent a bounding box.

    The box is defined by its top left corner (x1, y1), bottom right corner
    (x2, y2), label, score and classes.
    """

    def __init__(self, x1, y1, x2, y2, score=-1, classes=None):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.label = -1
        self.score = score
        self.classes = classes

    def __repr__(self):
        return "<BoundingBox({}, {}, {}, {}, {}, {}, {})>\n".format(
            self.x1, self.x2, self.y1, self.y2, self.get_label(),
            self.get_score(), self.classes)

    def get_label(self):
        """ Returns the label for this bounding box.

        Returns:
            Index of the label as an integer.
        """
        if self.label == -1:
            self.label = tf.argmax(self.classes)
        return self.label

    def get_score(self):
        """ Returns the score for this bounding box.

        Returns:
            Confidence as a float.
        """
        if self.score == -1:
            self.score = self.classes[self.get_label()]
        return self.score

    def iou(self, other):
        """ Computes intersection over union ratio between this bounding box and
        another one.

        Args:
            other (BoundingBox): the other bounding box for IOU computation

        Returns:
            IOU value as a float
        """

        def _interval_overlap(interval_1, interval_2):
            x1, x2 = interval_1
            x3, x4 = interval_2
            x1, x2, x3, x4 = (tf.cast(x1, dtype=tf.float32),
                              tf.cast(x2, dtype=tf.float32),
                              tf.cast(x3, dtype=tf.float32),
                              tf.cast(x4, dtype=tf.float32))

            if x3 < x1:
                if x4 < x1:
                    return tf.constant(0, dtype=tf.float32)
                return tf.minimum(x2, x4) - x1
            if x2 < x3:
                return tf.constant(0, dtype=tf.float32)
            return tf.minimum(x2, x4) - x3

        intersect_w = _interval_overlap([self.x1, self.x2],
                                        [other.x1, other.x2])
        intersect_h = _interval_overlap([self.y1, self.y2],
                                        [other.y1, other.y2])

        intersect = intersect_w * intersect_h

        w1, h1 = self.x2 - self.x1, self.y2 - self.y1
        w2, h2 = other.x2 - other.x1, other.y2 - other.y1

        union = w1 * h1 + w2 * h2 - intersect

        return tf.cast(intersect, dtype=tf.float32) / tf.cast(union, dtype=tf.float32)


def load_image(image_path):
    """ Loads an image from a path.

    Args:
        image_path (string): full path of the image to load

    Returns:
        a Tensorflow image Tensor
    """
    raw_image = tf.io.read_file(image_path)
    return tf.image.decode_jpeg(raw_image, channels=3)


def get_affine_transform(source_point, source_size, dest_size, inverse=False):
    """
    Construct an affine transformation matrix to map between source and destination sizes.
    Note that to construct an affine transformation we need three points.

    Args:
        source_point (np.ndarray): A point in the source image to be mapped, usually the center.
        source_size (tuple): The size of the source image in the form (width, height).
        dest_size (tuple): The desired image size in the form (width, height).
        inverse (bool, optional): If True, compute the inverse affine transformation.
            Defaults to False.

    Returns:
        np.ndarray: A 2x3 affine transformation matrix.
    """
    def _get_3rd_point(point1, point2):
        # The third point, which is obtained by rotating the vector
        # from the first to the second point by 90 degrees and adding
        # it to the second point. This ensures that the
        # resizing is aspect-ratio maintaining.
        vector = point1 - point2
        orthogonal_to_vector = np.array([-vector[1], vector[0]], dtype=np.float32)

        return point2 + orthogonal_to_vector

    # Calculate the scale ratio to preserve the aspect ratio
    scale_ratio = np.minimum(dest_size[0] / source_size[0], dest_size[1] / source_size[1])

    # Destination image center point
    dest_center_x = dest_size[0] * 0.5
    dest_center_y = dest_size[1] * 0.5
    dest_point = np.array([dest_center_x, dest_center_y], dtype=np.float32)

    # Initialize source and destination points arrays
    source_points = np.zeros((3, 2), dtype=np.float32)
    dest_points = np.zeros((3, 2), dtype=np.float32)

    # Set the first points to be the source center point and destination center point
    source_points[0, :] = source_point
    dest_points[0, :] = dest_point

    # Set the second points based on the magnitude (in this case 100 pixels up from the center)
    magnitude = 100.0
    source_points[1, :] = source_point + np.array([0, magnitude], dtype=np.float32)
    dst_dir = np.array([0, magnitude * scale_ratio], dtype=np.float32)
    dest_points[1, :] = dest_point + dst_dir

    # Third point
    source_points[2:, :] = _get_3rd_point(source_points[0, :], source_points[1, :])
    dest_points[2:, :] = _get_3rd_point(dest_points[0, :], dest_points[1, :])

    # Compute the affine transformation matrix
    if inverse:
        transform = cv2.getAffineTransform(np.float32(dest_points), np.float32(source_points))
    else:
        transform = cv2.getAffineTransform(np.float32(source_points), np.float32(dest_points))

    return transform


def preprocess_image(image, input_shape, affine_transform=None):
    """
    Resize an image to the specified dimensions using either a normal resize or
    an affine transformation in order to preserve aspect ratio.

    Args:
        image (np.ndarray): input image with size represented as (h, w, c).
        input_shape (tuple): tuple containing desired image
            dimension in form of (h, w, c).
        affine_transform (np.ndarray, optional): A 2x3 affine transformation matrix.
            Defaults to None.

    Returns:
        np.ndarray: the resized image.
    """
    if affine_transform is not None:
        image = cv2.warpAffine(image, affine_transform, (input_shape[1], input_shape[0]),
                               flags=cv2.INTER_LINEAR)
    else:
        image = tf.compat.v1.image.resize(image, [input_shape[0], input_shape[1]],
                                          method=tf.image.ResizeMethod.BILINEAR,
                                          align_corners=False)
        image = image.numpy()

    return image


def apply_affine_transform_to_bboxes(bboxes, affine_transform):
    """
    Apply an affine transformation to multiple bounding boxes.

    Args:
        bboxes (np.ndarray): A numpy array of shape (N, 4) representing N bounding boxes,
            each defined by the coordinates [y1, x1, y2, x2].
        affine_transform (np.ndarray): A 2x3 affine transformation matrix.

    Returns:
        np.ndarray: A numpy array of shape (N, 4) with the transformed bounding boxes,
        in the format of [y1, x1, y2, x2].
    """
    # Reshape bounding boxes to have shape (num_boxes, 2, 2)
    # to treat them as point [(y1, x1), (y2, x2)]
    bboxes = bboxes.reshape(-1, 2, 2)
    # ((y1, x1), (y2, x2)) -> ((x1, y1), (x2, y2))
    bboxes = bboxes[:, :, ::-1]
    # Stack bounding box coordinates with ones to apply affine transform as it is
    # a 2x3 matrix
    bboxes = np.concatenate([bboxes, np.ones((bboxes.shape[0], 2, 1), dtype=np.float32)], axis=2)
    # Apply the transformation matrix
    bboxes = np.dot(bboxes, affine_transform.T)
    # ((x1, y1), (x2, y2)) - > ((y1, x1), (y2, x2))
    bboxes = bboxes[:, :, ::-1]
    # Reshape to to [y1, x1, y2, x2] format
    return bboxes.reshape(-1, 4)


def desize_bboxes(bboxes, scores, raw_height, raw_width,
                  input_height, input_width, preserve_aspect_ratio):
    """
    Reverse the resizing of bounding boxes to match the original image dimensions.

    This operation must be the inverse of the resizing applied during preprocessing
    in the validation or testing pipelines. The version defined here is for an aspect-ratio
    conserving resize, scaled by the longest side.

    Args:
        bboxes (np.ndarray): A numpy array of shape (N, 4) representing N bounding boxes,
            each defined by the coordinates [y1, x1, y2, x2].
        raw_height (int): The original height of the image.
        raw_width (int): The original width of the image.
        input_height (int): The height of the resized image used during processing.
        input_width (int): The width of the resized image used during processing.
        preserve_aspect_ratio (bool): Whether aspect ratio is preserved during resizing or not.

    Returns:
        np.ndarray: A numpy array of shape (N, 4) with the bounding boxes resized to match the
        original image dimensions, each defined by the coordinates [y1, x1, y2, x2].
    """
    if preserve_aspect_ratio:
        # To absolute coordinates with respect to the resized image
        bboxes = np.array([[box.y1 * input_height,
                            box.x1 * input_width,
                            box.y2 * input_height,
                            box.x2 * input_width] for box in bboxes])
        center = np.array([raw_width / 2., raw_height / 2.], dtype=np.float32)
        inverse_affine_transform = get_affine_transform(center, [raw_width, raw_height],
                                                        [input_width, input_height], inverse=True)
        bboxes = apply_affine_transform_to_bboxes(bboxes, inverse_affine_transform)
        bboxes = np.clip(bboxes, 0, [raw_height-1, raw_width-1, raw_height-1, raw_width-1])
        bboxes = np.column_stack([bboxes, scores])
        bboxes = np.array([[box[Coord.x1], box[Coord.y1], box[Coord.x2], box[Coord.y2], box[4]]
                           for box in bboxes])
    else:
        # To absolute coordinates with respect to the original image
        bboxes = np.array([[box.x1 * raw_width,
                            box.y1 * raw_height,
                            box.x2 * raw_width,
                            box.y2 * raw_height] for box in bboxes])
        bboxes = np.column_stack([bboxes, scores])

    return bboxes


def create_yolo_targets(objects,
                        grid_size,
                        num_classes,
                        anchors):
    """
    Creates YOLO-style targets tensor for the given objects.

    Args:
        objects (dict): Dictionary containing information about objects in the image,
            including labels and bounding boxes.
        grid_size (tuple): The grid size used for YOLO target generation.
        num_classes (int): The number of classes.
        anchors (list): List of anchor boxes.

    Returns:
        targets (tf.Tensor): The targets output tensor.
    """
    def _update_bbox_target(bbox, grid_y, grid_x, best_anchor, targets):
        for i in range(4):
            indices_bbox = [[grid_y, grid_x, best_anchor, i]]
            targets = tf.tensor_scatter_nd_update(targets, indices_bbox, updates=[bbox[i]])
        return targets

    def _update_confidence_target(grid_y, grid_x, best_anchor, targets):
        indices_confidence = [[grid_y, grid_x, best_anchor, 4]]
        return tf.tensor_scatter_nd_update(targets, indices_confidence, updates=[1.])

    def _update_class_target(grid_y, grid_x, best_anchor, obj_indx, targets):
        indices_class = [[grid_y, grid_x, best_anchor, tf.cast(5 + obj_indx, tf.int32)]]
        return tf.tensor_scatter_nd_update(targets, indices_class, updates=[1.])

    n_anchors = len(anchors)
    anchors = [BoundingBox(0, 0, anchors[i][0], anchors[i][1]) for i in range(len(anchors))]
    targets = tf.zeros((grid_size[0], grid_size[1], n_anchors, 5 + num_classes),
                       dtype=tf.float32)
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

                box = [center_x, center_y, center_w, center_h]
                # find the anchor that best predicts this box
                best_anchor = -1
                max_iou = tf.constant(-1, dtype=tf.float32)

                shifted_box = BoundingBox(0, 0, center_w, center_h)

                for anchor_id, anchor in enumerate(anchors):
                    iou = shifted_box.iou(anchor)

                    if max_iou < iou:
                        best_anchor = anchor_id
                        max_iou = iou

                targets = _update_bbox_target(box, grid_y, grid_x, best_anchor, targets)
                targets = _update_confidence_target(grid_y, grid_x, best_anchor, targets)
                targets = _update_class_target(grid_y, grid_x, best_anchor, obj_indx, targets)

    return targets


def decode_output(output, anchors, nb_classes, obj_threshold=0.5, nms_threshold=0.5):
    """ Decodes a YOLO model output.

    Args:
        output (tf.Tensor): model output to decode
        anchors (list): list of anchors boxes
        nb_classes (int): number of classes
        obj_threshold (float, optional): confidence threshold for a box. Defaults to 0.5.
        nms_threshold (float, optional): non-maximal supression threshold. Defaults to 0.5.

    Returns:
        List of `BoundingBox` objects
    """

    def _sigmoid(x):
        return 1. / (1. + np.exp(-x))

    def _softmax(x, axis=-1, t=-100.):
        x = x - np.max(x)

        if np.min(x) < t:
            x = x / np.min(x) * t

        e_x = np.exp(x)

        return e_x / e_x.sum(axis, keepdims=True)

    grid_h, grid_w, nb_box = output.shape[:3]

    boxes = []

    # decode the output by the network
    output[..., 4] = _sigmoid(output[..., 4])
    output[..., 5:] = output[..., 4][..., np.newaxis] * _softmax(output[..., 5:])
    output[..., 5:] *= output[..., 5:] > obj_threshold

    col, row, _ = np.meshgrid(np.arange(grid_w), np.arange(grid_h), np.arange(nb_box))

    x = (col + _sigmoid(output[..., 0])) / grid_w
    y = (row + _sigmoid(output[..., 1])) / grid_h
    w = np.array(anchors)[:, 0] * np.exp(output[..., 2]) / grid_w
    h = np.array(anchors)[:, 1] * np.exp(output[..., 3]) / grid_h

    x1 = np.maximum(x - w / 2, 0)
    y1 = np.maximum(y - h / 2, 0)
    x2 = np.minimum(x + w / 2, grid_w)
    y2 = np.minimum(y + h / 2, grid_h)

    confidence = output[..., 4]
    classes = output[..., 5:]
    mask = np.sum(classes, axis=-1) > 0
    indices = np.where(mask)

    for i in range(len(indices[0])):
        row_idx, col_idx, box_idx = indices[0][i], indices[1][i], indices[2][i]

        box = BoundingBox(x1[row_idx, col_idx, box_idx],
                          y1[row_idx, col_idx, box_idx],
                          x2[row_idx, col_idx, box_idx],
                          y2[row_idx, col_idx, box_idx],
                          confidence[row_idx, col_idx, box_idx],
                          classes[row_idx, col_idx, box_idx])

        boxes.append(box)

    # suppress non-maximal boxes
    for c in range(nb_classes):
        sorted_indices = np.argsort([box.classes[c] for box in boxes])[::-1]
        for ind, index_i in enumerate(sorted_indices):
            if boxes[index_i].score == 0 or boxes[index_i].classes[c] == 0:
                continue

            for j in range(ind + 1, len(sorted_indices)):
                index_j = sorted_indices[j]
                if boxes[index_j].score == 0:
                    continue

                # filter out redundant boxes (same class and overlapping too
                # much)
                if (boxes[index_i].iou(boxes[index_j]) >= nms_threshold) and (
                        c == boxes[index_i].get_label()) and (
                            c == boxes[index_j].get_label()):
                    boxes[index_j].score = 0

    # remove the boxes which are less likely than a obj_threshold
    boxes = [box for box in boxes if box.get_score() > obj_threshold]

    return boxes
