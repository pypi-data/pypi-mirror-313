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
KWS model training script.
"""

import os
import pickle

from keras.utils import to_categorical

from cnn2snn import quantize_layer, convert

from ..cyclic_lr import CyclicLR
from ..training import (get_training_parser, compile_model, evaluate_model, print_history_stats,
                        RestoreBest, save_model)
from ..extract import extract_samples
from ..utils import fetch_file
from ..model_io import load_model


def get_data():
    """ Loads KWS data.

    Returns:
        tuple: train data, train labels, validation data and validation labels
    """
    # Load pre-processed dataset
    fname = fetch_file(
        'https://data.brainchip.com/dataset-mirror/kws/kws_preprocessed_all_words_except_backward_follow_forward.pkl',
        fname='kws_preprocessed_all_words_except_backward_follow_forward.pkl',
        cache_subdir=os.path.join('datasets', 'kws'))

    print('Loading pre-processed dataset...')
    with open(fname, 'rb') as f:
        [x_train, y_train, x_val, y_val, _, _, _, _] = pickle.load(f)

    return x_train.astype('float32'), y_train, x_val.astype('float32'), y_val


def train_model(model, x_train, y_train, x_val, y_val, batch_size, epochs):
    """ Trains the model.

    Args:
        model (keras.Model): the model to train
        x_train (numpy.ndarray): train data
        y_train (numpy.ndarray): train labels
        x_val (numpy.ndarray): validation data
        y_val (numpy.ndarray): validation labels
        batch_size (int): the batch size
        epochs (int): the number of epochs
    """
    # Warn user if number of epochs is not a multiple of 8
    if epochs % 8:
        print("WARNING: for better performance, the number of epochs "
              f" must be a multiple of 8; got 'epochs' = {epochs}")

    # Training parameters (cyclical learning rate)
    scaler = 4
    base_lr = 5e-6
    max_lr = 2e-3

    # Cyclical learning rate
    callbacks = []
    clr = CyclicLR(base_lr=base_lr,
                   max_lr=max_lr,
                   step_size=scaler * x_train.shape[0] / batch_size,
                   mode='triangular')
    callbacks.append(clr)

    # Model checkpoints (save best model and retrieve it when training is complete)
    restore_model = RestoreBest(model)
    callbacks.append(restore_model)

    history = model.fit(x_train,
                        to_categorical(y_train),
                        batch_size=batch_size,
                        epochs=epochs,
                        verbose=1,
                        validation_data=(x_val, to_categorical(y_val)),
                        callbacks=callbacks)
    print_history_stats(history)


def main():
    """ Entry point for script and CLI usage.
    """
    parsers = get_training_parser(batch_size=100, global_batch_size=False, extract=True)

    train_parser = parsers[1]
    train_parser.add_argument("-laq",
                              "--last_activ_quantization",
                              type=int,
                              default=None,
                              help="The last layer activation quantization")

    args = parsers[0].parse_args()

    # Load the source model
    model = load_model(args.model)

    # If specified, change the last layer activation bitwidth
    if "last_activ_quantization" in args and args.last_activ_quantization:
        model = quantize_layer(model, 'separable_4/relu', args.last_activ_quantization)

    # Compile model
    compile_model(model, learning_rate=2e-3)

    # Load data
    x_train, y_train, x_val, y_val = get_data()

    # Disable QuantizeML assertions
    os.environ["ASSERT_ENABLED"] = "0"

    # Train model
    if args.action == "train":
        train_model(model, x_train, y_train, x_val, y_val, args.batch_size, args.epochs)
        save_model(model, args.model, args.savemodel, args.action)
    elif args.action == "eval":
        # Evaluate model accuracy
        if args.akida:
            model_ak = convert(model)
            accuracy = model_ak.evaluate(x_val.astype('uint8'), y_val)
            print(f"Accuracy: {accuracy}")
        else:
            evaluate_model(model, x_val, y=to_categorical(y_val))
    elif args.action == 'extract':
        # Extract samples from dataset
        extract_samples(args.savefile, x_train, args.batch_size)


if __name__ == "__main__":
    main()
