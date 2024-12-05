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
Training script for MNIST models.
"""

import os
from keras.datasets import mnist
from keras.losses import SparseCategoricalCrossentropy

from cnn2snn import convert

import numpy as np

from ..training import (get_training_parser, compile_model, evaluate_model, print_history_stats,
                        save_model, RestoreBest)
from ..extract import extract_samples
from ..model_io import load_model


def get_data():
    """ Loads MNIST data.

    Returns:
        tuple: train data, train labels, test data and test labels
    """
    # The data, shuffled and split between train and test sets
    (x_train, y_train), (x_test, y_test) = mnist.load_data()

    # Normalize data
    x_train = x_train.astype("float32")
    x_train = np.reshape(x_train, (-1, 28, 28, 1))

    x_test = x_test.astype("float32")
    x_test = np.reshape(x_test, (-1, 28, 28, 1))

    return x_train, y_train, x_test, y_test


def train_model(model, x_train, y_train, x_test, y_test, batch_size, epochs):
    """ Trains the model without the distillation.

    Args:
        model (keras.Model): the model to train
        x_train (numpy.ndarray): train data
        y_train (numpy.ndarray): train labels
        x_test (numpy.ndarray): test data
        y_test (numpy.ndarray): test labels
        batch_size (int): the batch size
        epochs (int): the number of epochs
    """
    history = model.fit(x_train, y_train, batch_size, epochs, validation_data=(x_test, y_test),
                        callbacks=[RestoreBest(model)])
    print_history_stats(history)


def main():
    """ Entry point for script and CLI usage.
    """
    parsers = get_training_parser(batch_size=128, tune=True, global_batch_size=False, extract=True)
    args = parsers[0].parse_args()

    # Load the source model
    model = load_model(args.model)

    # Compile model
    lr = 1e-4
    if args.action == 'tune':
        lr = 3e-5
    compile_model(model, learning_rate=lr, loss=SparseCategoricalCrossentropy(from_logits=True))

    # Load data
    x_train, y_train, x_test, y_test = get_data()

    # Disable QuantizeML assertions
    os.environ["ASSERT_ENABLED"] = "0"

    # Train model
    if args.action in ["train", "tune"]:
        train_model(model, x_train, y_train, x_test, y_test, args.batch_size, args.epochs)
        save_model(model, args.model, args.savemodel, args.action)
    elif args.action == "eval":
        # Evaluate model accuracy
        if args.akida:
            model_ak = convert(model)
            accuracy = model_ak.evaluate(x_test.astype('uint8'), y_test)
            print(f"Accuracy: {accuracy}")
        else:
            evaluate_model(model, x_test, y=y_test)
    elif args.action == 'extract':
        # Extract samples from dataset
        extract_samples(args.savefile, x_train, args.batch_size)


if __name__ == "__main__":
    main()
