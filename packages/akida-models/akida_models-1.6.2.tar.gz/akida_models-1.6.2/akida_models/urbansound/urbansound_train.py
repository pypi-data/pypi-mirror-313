#!/usr/bin/env python
# ==============================================================================
# Copyright 2024 Brainchip Holdings Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""
Training script for a vit based model on the urbansound8k dataset.

"""

import os
import argparse
import random
import soundata
import numpy as np
from keras.callbacks import ReduceLROnPlateau
from keras.losses import SparseCategoricalCrossentropy
from keras.metrics import SparseCategoricalAccuracy
from cnn2snn import convert
import akida
from akida_models.training import (save_model, get_training_parser,
                                   print_history_stats, RestoreBest, compile_model)
from akida_models.model_io import load_model
from akida_models.extract import extract_samples
from .preprocessing import process_dataset


def train_model(model, preprocessed_dataset, epochs_per_fold, batch_size, test_fold_id):
    """ Trains the model on the folds ids that are different from the test_fold_id.
    (e.g: if test_fold_id==10 uses the folds from 1 to 9 for the training)

    Args:
        model (keras.Model): the model to train
        preprocessed_dataset (dict): the preprocessed dataset.
        epochs_per_fold (int): the number of epochs per fold
        batch_size (int): training batch size.
        test_fold_id (int): the validation/testing fold id.
    """
    def _shuffle_training_data(samples, labels):
        combined_list = list(zip(samples, labels))
        random.shuffle(combined_list)
        shuffled_samples, shuffled_labels = zip(*combined_list)
        return shuffled_samples, shuffled_labels

    # ReduceLROnPlateau scheduler
    callbacks = []
    scheduler = ReduceLROnPlateau(monitor='val_loss',
                                  factor=0.3,
                                  patience=3,
                                  verbose=1,
                                  mode='min',
                                  min_lr=1e-6)
    callbacks.append(scheduler)

    # Model checkpoints (save best model and retrieve it when training is complete)
    restore_model = RestoreBest(model, monitor="val_sparse_categorical_accuracy")
    callbacks.append(restore_model)

    train_samples, train_labels = [], []
    # Separate the training samples from the testing ones
    for fold_id in preprocessed_dataset.keys():
        if fold_id != test_fold_id:
            train_samples.extend(preprocessed_dataset[str(fold_id)]['samples'])
            train_labels.extend(preprocessed_dataset[str(fold_id)]['labels'])
    # Shuffle the training samples
    train_samples, train_labels = _shuffle_training_data(train_samples, train_labels)
    # Testing samples are the one from the test_fold_id fold
    test_samples = preprocessed_dataset[str(test_fold_id)]['samples']
    test_labels = preprocessed_dataset[str(test_fold_id)]['labels']

    history = model.fit(np.asarray(train_samples),
                        np.asarray(train_labels),
                        validation_data=(np.asarray(test_samples), np.asarray(test_labels)),
                        batch_size=batch_size,
                        epochs=epochs_per_fold,
                        callbacks=callbacks,
                        verbose=1)
    print_history_stats(history)


def evaluate_model(model, preprocessed_dataset, test_fold_id, batch_size=32):
    """ Evaluates the trained model.

    Args:
        model (keras.Model or akida.Model): model to evaluate.
        preprocessed_dataset (dict): the preprocessed dataset.
        test_fold_id (int): the validation/testing fold id.
        batch_size (int, optional): The evaluation batch_size. Used only during the Akida
            evaluation to accelerate it. Defaults to 32.

    """

    test_samples = np.asarray(preprocessed_dataset[str(test_fold_id)]['samples'])
    test_labels = np.asarray(preprocessed_dataset[str(test_fold_id)]['labels'])
    if isinstance(model, akida.Model):
        accuracy = model.evaluate(test_samples, test_labels, batch_size=batch_size)
        print(f"Akida accuracy: {accuracy}")
    else:
        scores = model.evaluate(test_samples, test_labels, verbose=1)
        print(f"Validation accuracy: {scores[1]}")


def main():
    """ Entry point for script and CLI usage.

    Note: Download the UrbanSound8k dataset from
    [UrbanSoundwebsite](https://urbansounddataset.weebly.com/urbansound8k.html)
    using the [soundata](https://github.com/soundata/soundata) library.
    """
    global_parser = argparse.ArgumentParser(add_help=False)
    global_parser.add_argument("-d", "--data", type=str,
                               required=True,
                               help="Path to the UrbanSound8k data.")

    parsers = get_training_parser(batch_size=32, extract=True, tune=True,
                                  global_parser=global_parser)
    args = parsers[0].parse_args()

    # Load the source model
    model = load_model(args.model)

    # Compile model. Use a higher learning rate for the train and a lower one for the tuning/QAT
    learning_rate = 3e-4 if args.action == "train" else 3e-7
    loss = SparseCategoricalCrossentropy(from_logits=True)
    metric = SparseCategoricalAccuracy()
    compile_model(model, learning_rate, loss, [metric])

    # Disable QuantizeML assertions
    os.environ["ASSERT_ENABLED"] = "0"

    assert soundata is not None, "To load urbansound8k dataset, Soundata package must\
        be installed. Note: Its installation might requires to install the libasound2-dev package\
        (on Linux distribution : apt-get install libasound2-dev)"

    # Load dataset
    dataset = soundata.initialize('urbansound8k', data_home=args.data)
    # Download the dataset's index to be able to validate it
    dataset.download(["index"])
    valid_dataset = True
    # Validate that all the expected files are there and valid
    # dataset.validate() returns a tuple of two dict in the shape:
    # ({'metadata': {}, 'clips': {}}, {'metadata': {}, 'clips': {}}) where the first represents the
    # locally missing elements and the second the ones with invalid checksum. Here the check
    # asserts that all the elements are present and valid. If not download the dataset.
    for dict_clips in dataset.validate():
        for key in dict_clips.keys():
            if dict_clips[key]:
                valid_dataset = False
    if not valid_dataset:
        dataset.download(force_overwrite=True, cleanup=True)

    # Preprocess the dataset samples
    processed_dataset = process_dataset(dataset, model.input_shape[1:3])

    # Set the fold '10' as the default testing/validation dataset.
    test_fold_id = 10

    # Train model
    if args.action in ["train", "tune"]:
        train_model(model, processed_dataset, args.epochs, args.batch_size, test_fold_id)
        save_model(model, args.model, args.savemodel, args.action)
    # Evaluate model accuracy
    elif args.action == "eval":
        if args.akida:
            model = convert(model)
        evaluate_model(model, processed_dataset, test_fold_id, args.batch_size)
    elif args.action == 'extract':
        # Extract samples from training dataset here by default from the fold '1' (it can be any
        # fold different from the test_fold_id)
        extract_samples(args.savefile, np.asarray(processed_dataset['1']['samples']),
                        args.batch_size)


if __name__ == "__main__":
    main()
