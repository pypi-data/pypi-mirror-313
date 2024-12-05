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
Training script for YOLO models.
"""

import argparse
import os
import pickle

import numpy as np
from cnn2snn import convert
from keras import Model
from keras.callbacks import EarlyStopping
from keras.layers import Reshape

from ..extract import extract_samples
from ..model_io import load_model
from ..training import (compile_model, freeze_model_before,
                        get_training_parser, save_model)
from ..utils import get_tensorboard_callback
from .map_evaluation import MapEvaluation
from .preprocess_data import preprocess_dataset
from .yolo_loss import YoloLoss
from .data_augmentation import build_yolo_aug_pipeline
from .processing import create_yolo_targets
from .data import get_detection_datasets


def get_anchors(anchors_path):
    """Loads anchors

    Args:
        anchors_path (str): path to anchors pickle file.

    Returns:
        list: list of anchors.
    """
    with open(anchors_path, 'rb') as handle:
        anchors = pickle.load(handle)
    return anchors


def train(model, train_data, valid_data, num_train, num_valid, anchors, labels, obj_threshold,
          nms_threshold, epochs, batch_size, train_times, grid_size, out_dir):
    """ Trains the model.

    Args:
        model (keras.Model): the model to train
        train_data (tf.dataset): training data
        valid_data (tf.dataset): validation data
        num_train (int): size of training data
        num_valid (int): size of validation data
        anchors (list): list of anchors
        labels (list): list of labels
        obj_threshold (float): confidence threshold for a box
        nms_threshold (float): non-maximal supression threshold
        epochs (int): the number of epochs
        batch_size (int): the batch size
        train_times (int): factor to increase the steps per epoch
        grid_size (tuple): the grid size
        out_dir (str): parent directory for logs folder
    """
    # Build batch generators
    input_shape = model.input.shape[1:]
    aug_pipe = build_yolo_aug_pipeline()

    train_dataset = preprocess_dataset(dataset=train_data,
                                       input_shape=input_shape,
                                       grid_size=grid_size,
                                       labels=labels,
                                       batch_size=batch_size,
                                       aug_pipe=aug_pipe,
                                       create_targets_fn=create_yolo_targets,
                                       training=True,
                                       anchors=anchors)

    valid_dataset = preprocess_dataset(dataset=valid_data,
                                       input_shape=input_shape,
                                       grid_size=grid_size,
                                       labels=labels,
                                       batch_size=batch_size,
                                       aug_pipe=aug_pipe,
                                       create_targets_fn=create_yolo_targets,
                                       training=False,
                                       anchors=anchors)
    # Create callbacks
    early_stop_cb = EarlyStopping(monitor='val_loss',
                                  min_delta=0.001,
                                  patience=10,
                                  mode='min',
                                  verbose=1)

    map_evaluator_cb = MapEvaluation(model,
                                     valid_data,
                                     num_valid,
                                     labels,
                                     anchors,
                                     period=1,
                                     obj_threshold=obj_threshold,
                                     nms_threshold=nms_threshold)

    tensorboard_cb = get_tensorboard_callback(out_dir, prefix='yolo')
    train_steps = int(np.ceil(num_train / batch_size)) * train_times

    callbacks = [early_stop_cb, map_evaluator_cb, tensorboard_cb]

    # Start the training process
    model.fit(train_dataset,
              steps_per_epoch=train_steps,
              epochs=epochs,
              validation_data=valid_dataset,
              callbacks=callbacks,
              workers=12,
              max_queue_size=40)


def evaluate(model, valid_data, num_valid, anchors, labels, obj_threshold, nms_threshold):
    """ Evaluates model performances.

    Args:
        model (keras.Model or akida.Model): the model to evaluate
        valid_data (tf.dataset): validation data
        num_valid (int): size of validation data
        anchors (list): list of anchors
        labels (list): list of labels
        obj_threshold (float): confidence threshold for a box
        nms_threshold (float): non-maximal supression threshold
    """
    # Create the mAP evaluator
    map_evaluator = MapEvaluation(model,
                                  valid_data,
                                  num_valid,
                                  labels,
                                  anchors,
                                  obj_threshold=obj_threshold,
                                  nms_threshold=nms_threshold,
                                  is_keras_model=isinstance(model, Model))

    # Compute mAP scores and display them
    map_dict, average_precisions = map_evaluator.evaluate_map()
    mAP = sum(map_dict.values()) / len(map_dict)

    print('mAP 50: {:.4f}'.format(map_dict[0.5]))
    print('mAP 75: {:.4f}'.format(map_dict[0.75]))
    for label, average_precision in average_precisions.items():
        print(labels[label], '{:.4f}'.format(average_precision))
    print('mAP: {:.4f}'.format(mAP))


def extract_yolo_samples(im_size, data, grid_size, anchors, labels, num_samples, out_file):
    """ Extract samples from data and save them to a npz file.

    Args:
        im_size (int): image size
        data (tf.dataset): TF dataset
        grid_size (tuple): the grid size
        anchors (list): list of anchors
        labels (list): list of labels
        num_samples (int): number of samples to extract
        out_file (str): name of output file
    """
    aug_pipe = build_yolo_aug_pipeline()
    dataset = preprocess_dataset(dataset=data,
                                 input_shape=im_size,
                                 grid_size=grid_size,
                                 labels=labels,
                                 anchors=anchors,
                                 aug_pipe=aug_pipe,
                                 create_targets_fn=create_yolo_targets,
                                 batch_size=num_samples,
                                 training=True)
    extract_samples(out_file, dataset, num_samples)


def main():
    """ Entry point for script and CLI usage.

    Note: PASCAL VOC2007 and VOC2012 can be downloaded at
    http://host.robots.ox.ac.uk/pascal/VOC/voc2007/ and
    http://host.robots.ox.ac.uk/pascal/VOC/voc2012/. Because those source website are known to be
    unreachable, datasets are also available on Brainchip data server
    https://data.brainchip.com/dataset-mirror/voc/ and under /hdd/datasets/VOCdevkit.
    Also, Widerface dataset can be downloaded at http://shuoyang1213.me/WIDERFACE/.
    For convenience, the TF records files are available under /hdd/datasets/widerface/.
    """
    global_parser = argparse.ArgumentParser(add_help=False)
    global_parser.add_argument(
        "-d",
        "--data",
        required=True,
        help="The directory containing VOC, WiderFace or COCO data.")
    global_parser.add_argument(
        "dataset_name",
        help="Name of the dataset.",
        choices=['voc', 'coco', 'widerface']
    )
    global_parser.add_argument("-lr",
                               "--learning_rate",
                               type=float,
                               default=5e-4,
                               help="Learning rate value.")
    global_parser.add_argument("-tt",
                               "--train_times",
                               type=int,
                               default=10,
                               help="Train times.")
    global_parser.add_argument("-ap",
                               "--anchors_path",
                               required=True,
                               help="Path to anchors boxes file.")
    global_parser.add_argument("-obj",
                               "--obj_thresh",
                               type=float,
                               default=0.5,
                               help="Confidence threshold for a box")
    global_parser.add_argument("-nms",
                               "--nms_thresh",
                               type=float,
                               default=0.5,
                               help="Non-Maximal Suppression threshold.")
    global_parser.add_argument("-o",
                               "--out_dir",
                               type=str,
                               default="./logs",
                               help="The output directory (logs, checkpoints).")

    parsers = get_training_parser(batch_size=128,
                                  freeze_before=True,
                                  tune=True,
                                  extract=True,
                                  global_parser=global_parser)

    args = parsers[0].parse_args()

    # Load the source model
    base_model = load_model(args.model)

    # Load data. Only use full VOC when num_classes > 2, that is last dimension is > 4 + 1 + 2
    anchors = get_anchors(args.anchors_path)
    full_set = (args.dataset_name != 'voc'
                or base_model.output_shape[-1] // len(anchors) > 4 + 1 + 2)
    train_data, valid_data, labels, num_train, num_valid = \
        get_detection_datasets(args.data, args.dataset_name, full_set)

    # Create a final reshape layer for loss computation
    grid_size = base_model.output_shape[1:3]
    output = Reshape(
        (grid_size[1], grid_size[0], len(anchors), 4 + 1 + len(labels)),
        name="YOLO_output")(base_model.output)

    # Build the full model
    model = Model(base_model.input, output)

    # Freeze the model
    if "freeze_before" in args:
        freeze_model_before(model, args.freeze_before)

    # Compile model
    learning_rate = args.learning_rate

    compile_model(model,
                  learning_rate=learning_rate,
                  loss=YoloLoss(anchors, grid_size, args.batch_size),
                  metrics=None)

    # Disable QuantizeML assertions
    os.environ["ASSERT_ENABLED"] = "0"

    # Train model
    if args.action in ["train", "tune"]:
        train(model, train_data, valid_data, num_train, num_valid, anchors, labels, args.obj_thresh,
              args.nms_thresh, args.epochs, args.batch_size, args.train_times, grid_size,
              args.out_dir)
        # Remove the last reshape layer introduced for training
        model = Model(model.input, model.layers[-2].output)
        save_model(model, args.model, args.savemodel, args.action)

    elif args.action == 'eval':
        # Evaluate model accuracy
        if args.akida:
            # Drop the last reshape layer that is not Akida compatible
            if model.layers[-1].name == 'YOLO_output':
                model = Model(model.input, model.layers[-2].output)
            model = convert(model)
        evaluate(model, valid_data, num_valid, anchors, labels, args.obj_thresh,
                 args.nms_thresh)

    elif args.action == 'extract':
        input_shape = model.input.shape[1:]
        extract_yolo_samples(input_shape, train_data, grid_size, anchors,
                             labels, args.batch_size, args.savefile)


if __name__ == "__main__":
    main()
