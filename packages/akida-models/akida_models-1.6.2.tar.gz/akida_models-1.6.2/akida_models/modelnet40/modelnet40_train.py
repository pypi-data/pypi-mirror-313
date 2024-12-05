#!/usr/bin/env python
# ******************************************************************************
# Copyright 2021 Brainchip Holdings Ltd.
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
ModelNet40 model training script.
"""

import os
import argparse
import numpy as np

from keras.callbacks import LearningRateScheduler

from cnn2snn import convert

from .preprocessing import get_modelnet, get_modelnet_from_file

from ..training import (get_training_parser, compile_model, print_history_stats, evaluate_model,
                        evaluate_akida_model, save_model)
from ..extract import extract_samples
from ..model_io import load_model


def get_data(batch_size, selected_points, knn_points):
    """ Loads data.

    Args:
        batch_size (int): the batch size
        selected_points (int): num points to process per sample.
        knn_points (int): number of points to include in each localised group.
            Must be a power of 2, and ideally an integer square (so 64, or 16
            for a deliberately small network, or 256 for large).

    Returns:
        tf.Dataset, tf.Dataset: train and test point with data augmentation
    """
    # This is the number of points sampled from each input file,
    # when parsing the data, and done only once (and saved as a .npz file)
    # for efficiency.
    train_points, train_labels, test_points, test_labels, _ = \
        get_modelnet_from_file(num_points=1024)

    train_dataset, test_dataset = get_modelnet(train_points,
                                               train_labels,
                                               test_points,
                                               test_labels,
                                               batch_size=batch_size,
                                               selected_points=selected_points,
                                               knn_points=knn_points)

    return train_dataset, test_dataset


def train_model(model, train_dataset, test_dataset, epochs):
    """ Trains the model.

    Args:
        model (keras.Model): the model to train.
        train_dataset (tf.dataset): train data.
        test_dataset (tf.dataset): test data.
        epochs (int): the number of epochs.
    """
    # Learning rate scheduler
    callbacks = []
    max_lr = 0.001
    min_lr = max_lr * 0.01
    lr_decay = (min_lr / max_lr)**(1. / epochs)
    lr_scheduler = LearningRateScheduler(lambda e: max_lr * lr_decay**e)
    callbacks.append(lr_scheduler)

    history = model.fit(train_dataset,
                        validation_data=test_dataset,
                        epochs=epochs,
                        callbacks=callbacks)
    print_history_stats(history)


def main():
    """ Entry point for script and CLI usage.
    """
    global_parser = argparse.ArgumentParser(add_help=False)
    global_parser.add_argument(
        "-p",
        "--selected_points",
        type=int,
        default=64,
        help="The number of points to process per sample. \
                        (defaults to %(default)s)")
    global_parser.add_argument("-n",
                               "--knn_points",
                               type=int,
                               default=32,
                               help="The number of points to include in each \
                        localised group. (defaults to %(default)s)")

    parser = get_training_parser(batch_size=16, global_parser=global_parser, extract=True)[0]
    args = parser.parse_args()

    # Load the source model
    model = load_model(args.model)

    # Compile model
    compile_model(model, loss="sparse_categorical_crossentropy")

    # Load data
    train_dataset, test_dataset = get_data(args.batch_size,
                                           args.selected_points,
                                           args.knn_points)

    # Disable QuantizeML assertions
    os.environ["ASSERT_ENABLED"] = "0"

    # Train model
    if args.action == "train":
        train_model(model, train_dataset, test_dataset, args.epochs)
        save_model(model, args.model, args.savemodel, args.action)
    elif args.action == "eval":
        # Evaluate model accuracy
        if args.akida:
            model = convert(model)
            preds, labels = evaluate_akida_model(model, test_dataset, 'softmax')
            accuracy = (np.argmax(preds, 1) == labels).mean()
            print(f"Akida accuracy: {accuracy}")
        else:
            evaluate_model(model, test_dataset)
    elif args.action == 'extract':
        # Extract samples from dataset
        extract_samples(args.savefile, train_dataset, args.batch_size)


if __name__ == "__main__":
    main()
