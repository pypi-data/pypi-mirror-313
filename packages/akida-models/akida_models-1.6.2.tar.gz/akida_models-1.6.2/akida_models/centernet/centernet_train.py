#!/usr/bin/env python
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
Training script for CenterNet models
"""
import os
import numpy as np
import argparse

from keras import Model
from cnn2snn import convert

from ..training import (get_training_parser, freeze_model_before,
                        compile_model, save_model, RestoreBest)
from ..detection.map_evaluation import MapEvaluation
from ..param_scheduler import get_cosine_lr_scheduler
from ..utils import get_tensorboard_callback
from ..model_io import load_model
from ..extract import extract_samples

from .centernet_loss import CenternetLoss
from .centernet_processing import decode_output
from ..detection.preprocess_data import preprocess_dataset
from .centernet_utils import build_centernet_aug_pipeline, create_centernet_targets
from ..detection.data import get_detection_datasets


def _decode_centernet_output_fn(output, anchors, nb_classes, obj_threshold=0.5, nms_threshold=0.5):
    # Ignore attributes from original MAPEvaluator
    return decode_output(output, nb_classes, obj_threshold=obj_threshold)


def train(model, train_data, valid_data, num_train, num_valid, labels, lr_max, obj_threshold,
          epochs, batch_size, grid_size, train_times, period, tune=False, out_dir=None):
    """ Trains the model.

    Args:
        model (keras.Model): the model to train.
        train_data (tf.dataset): training data.
        valid_data (tf.dataset): validation data.
        num_train (int): size of training data.
        num_valid (int): size of validation data.
        labels (list): classes name.
        lr_max (float): max learning rate to take in learning rate scheduler.
        obj_threshold (float): confidence threshold for inference procedure.
        epochs (int): the number of epochs.
        batch_size (int): the batch size.
        grid_size (tuple): the spatial hw output size.
        train_times (int): factor to increase the steps per epoch.
        period (int): periodicity the mAP is computed and printed.
        tune (bool, optional): wheter the model will be tuned or not, modifying ``lr_max``.
            Defaults to False.
        out_dir (str, optional): folder name to save logs. Defaults to None
    """
    # Build batch generators
    input_shape = model.input.shape[1:]

    # data augmentation pipeline
    aug_pipe = build_centernet_aug_pipeline()

    # create the data generators
    train_dataset = preprocess_dataset(dataset=train_data,
                                       input_shape=input_shape,
                                       grid_size=grid_size,
                                       labels=labels,
                                       batch_size=batch_size,
                                       aug_pipe=aug_pipe,
                                       preserve_aspect_ratio=True,
                                       create_targets_fn=create_centernet_targets,
                                       training=True)

    valid_dataset = preprocess_dataset(dataset=valid_data,
                                       input_shape=input_shape,
                                       grid_size=grid_size,
                                       labels=labels,
                                       batch_size=batch_size,
                                       aug_pipe=aug_pipe,
                                       preserve_aspect_ratio=True,
                                       create_targets_fn=create_centernet_targets,
                                       training=False)

    # Create callbacks
    steps_per_epoch = int(np.ceil(num_train / batch_size)) * train_times
    map_evaluator_cb = MapEvaluation(model,
                                     valid_data,
                                     num_valid,
                                     labels,
                                     anchors=None,
                                     period=period,
                                     obj_threshold=obj_threshold,
                                     max_box_per_image=50,
                                     preserve_aspect_ratio=True,
                                     decode_output_fn=_decode_centernet_output_fn)
    lrs_callback = get_cosine_lr_scheduler(lr_max,
                                           steps_per_epoch * epochs,
                                           pct_start=0.001 if tune else 0.3)
    tensorboard = get_tensorboard_callback(out_dir, prefix="centernet")

    callbacks = [map_evaluator_cb, lrs_callback, tensorboard]

    if period == 1:
        restore_model = RestoreBest(model, monitor="map")
        callbacks.append(restore_model)

    # Start the training process
    model.fit(x=train_dataset,
              steps_per_epoch=steps_per_epoch,
              epochs=epochs,
              validation_data=valid_dataset,
              callbacks=callbacks,
              workers=12,
              max_queue_size=40)


def evaluate(model, valid_data, num_valid, labels, obj_threshold):
    """ Evaluates model performances.

    Args:
        model (keras.Model or akida.Model): the model to evaluate.
        valid_data (tf.dataset): validation data.
        num_valid (int): size of validation data.
        labels (list): classes name.
        obj_threshold (float): confidence threshold for inference procedure.
    """
    # Create the mAP evaluator
    map_evaluator = MapEvaluation(model,
                                  valid_data,
                                  num_valid,
                                  labels,
                                  anchors=None,
                                  obj_threshold=obj_threshold,
                                  max_box_per_image=50,
                                  preserve_aspect_ratio=True,
                                  is_keras_model=isinstance(model, Model),
                                  decode_output_fn=_decode_centernet_output_fn)

    # Compute mAP scores and display them
    map_dict, average_precisions = map_evaluator.evaluate_map()
    mAP = sum(map_dict.values()) / len(map_dict)

    print('mAP 50: {:.4f}'.format(map_dict[0.5]))
    print('mAP 75: {:.4f}'.format(map_dict[0.75]))
    for label, average_precision in average_precisions.items():
        print(labels[label], '{:.4f}'.format(average_precision))
    print('mAP: {:.4f}'.format(mAP))


def extract_centernet_samples(im_size, data, grid_size, labels, num_samples, out_file):
    """ Extract samples from data and save them to a npz file.

    Args:
        im_size (int): image size
        data (tf.dataset): TF dataset
        grid_size (tuple): the grid size
        labels (list): list of labels
        num_samples (int): number of samples to extract
        out_file (str): name of output file
    """
    aug_pipe = build_centernet_aug_pipeline()
    dataset = preprocess_dataset(dataset=data,
                                 input_shape=im_size,
                                 grid_size=grid_size,
                                 labels=labels,
                                 aug_pipe=aug_pipe,
                                 create_targets_fn=create_centernet_targets,
                                 batch_size=num_samples,
                                 training=True)
    extract_samples(out_file, dataset, num_samples)


def main():
    """ Entry point for script and CLI usage. """
    global_parser = argparse.ArgumentParser(add_help=False)
    global_parser.add_argument("-d", "--data", default=None,
                               help="The directory containing VOC data.")
    global_parser.add_argument(
        "dataset_name", help="Name of the dataset.",
        choices=['voc', 'coco']
    )
    global_parser.add_argument("-lr", "--learning_rate", type=float,
                               default=1e-2, help="Learning rate value.")
    global_parser.add_argument("-tt", "--train_times", type=int,
                               default=10, help="Train times.")
    global_parser.add_argument("-p", "--period", type=int,
                               default=4, help="periodicity the model is evaluated")
    global_parser.add_argument("-obj", "--obj_thresh", type=float, default=0.1,
                               help="Confidence threshold for a box. Defaults to %(default)s")
    global_parser.add_argument("-o", "--out_dir", type=str, default='./logs',
                               help="The output directory (logs). Defaults to %(default)s")
    parsers = get_training_parser(batch_size=128, freeze_before=True, tune=True, extract=True,
                                  global_parser=global_parser)
    args = parsers[0].parse_args()

    # Load data
    train_data, valid_data, labels, num_train, num_valid = get_detection_datasets(
        args.data, args.dataset_name)

    # Load the source model
    model = load_model(args.model)

    grid_size = model.output.shape[1:3]

    nlabels, nmodel = len(labels), model.output.shape[-1]
    if nlabels + 4 != nmodel:
        raise ValueError(f"Model's output ({nmodel}) does not match with "
                         f"number of labels ({nlabels}) + 4. "
                         f"Check the data file {args.data} or input model {args.model}.")
    # Freeze the model
    if "freeze_before" in args:
        freeze_model_before(model, args.freeze_before)

    # Compile model
    learning_rate = args.learning_rate
    compile_model(model, learning_rate=learning_rate, loss=CenternetLoss(), metrics=None)

    # Disable QuantizeML assertions
    os.environ["ASSERT_ENABLED"] = "0"

    if args.action in ["train", "tune"]:
        train(model, train_data, valid_data, num_train, num_valid, labels, learning_rate,
              args.obj_thresh, args.epochs, args.batch_size, grid_size,
              train_times=args.train_times, period=args.period,
              out_dir=args.out_dir, tune=args.action == "tune")
        save_model(model, args.model, args.savemodel, args.action)
    elif args.action == "eval":
        # Evaluate model accuracy
        if args.akida:
            model = convert(model)
        evaluate(model, valid_data, num_valid, labels, args.obj_thresh)

    elif args.action == 'extract':
        input_shape = model.input.shape[1:]
        extract_centernet_samples(input_shape, train_data, grid_size,
                                  labels, args.batch_size, args.savefile)


if __name__ == "__main__":
    main()
