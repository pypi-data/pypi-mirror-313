#!/usr/bin/env python
# ******************************************************************************
# Copyright 2022 Brainchip Holdings Ltd.
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
Portrait128 training script.
"""

import os
import argparse

import tensorflow as tf
import numpy as np
from keras.metrics import BinaryIoU

from cnn2snn import convert

from ..param_scheduler import get_cosine_lr_scheduler
from ..training import (get_training_parser, compile_model, evaluate_model, print_history_stats,
                        RestoreBest, save_model)
from ..extract import extract_samples
from ..model_io import load_model


def _train_eval_split(x, y, validation_split=0.2, random_state=None):
    """
    Splits the input data into training and validation sets.

    Args:
        x (numpy.ndarray): The input features.
        y (numpy.ndarray): The corresponding labels.
        validation_split (float, optional): Fraction of the original dataset
            used as the validation set. Should be in the range [0, 1]. Defaults to 0.2
        random_state (int, optional): Seed for reproducibility. Default to None.

    Returns:
        (numpy.ndarray, numpy.ndarray, numpy.ndarray, numpy.ndarray): Train and eval sets.
    """
    rng = np.random.default_rng(random_state)

    num_samples = len(x)
    indices = np.arange(num_samples)
    rng.shuffle(indices)

    validation_size = int(validation_split * num_samples)
    validation_indices = indices[:validation_size]
    train_indices = indices[validation_size:]

    x_train, x_val = x[train_indices], x[validation_indices]
    y_train, y_val = y[train_indices], y[validation_indices]

    return x_train, x_val, y_train, y_val


def get_data(path, batch_size):
    """ Loads Portrait128 data.

    Args:
        path (str): path to npy data
        batch_size (int): the batch size

    Returns:
        tuple: train dataset, validation dataset, steps per epoch and validation step
    """
    x = np.load(os.path.join(path, "img_uint8.npy"))
    y = np.load(os.path.join(path, "msk_uint8.npy")) / 255

    seed = 1
    x_train, x_val, y_train, y_val = _train_eval_split(x,
                                                       y,
                                                       validation_split=0.2,
                                                       random_state=seed)
    data_augmentation = tf.keras.Sequential([
        tf.keras.layers.RandomFlip("horizontal", seed=seed),
        tf.keras.layers.RandomTranslation(height_factor=0.1, width_factor=0.1, seed=seed),
        tf.keras.layers.RandomZoom(0.2, seed=seed),
    ])

    def data_generator(images, masks):
        for image, mask in zip(images, masks):
            yield image, mask

    def apply_data_augmentation(image, mask):
        # Concatenate image and mask along the last axis
        combined = tf.concat([image, mask], axis=-1)
        # Apply the same augmentation to both image and mask
        augmented_combined = data_augmentation(combined)
        # Split the augmented combined tensor back into image and mask
        augmented_image, augmented_mask = tf.split(augmented_combined, [3, 1], axis=-1)

        return augmented_image, augmented_mask

    train_dataset = tf.data.Dataset.from_generator(
        generator=lambda: data_generator(x_train, y_train),
        output_signature=(
            tf.TensorSpec(shape=x_train.shape[1:], dtype=tf.float32),
            tf.TensorSpec(shape=y_train.shape[1:], dtype=tf.float32)
        )
    )

    validation_dataset = tf.data.Dataset.from_generator(
        generator=lambda: data_generator(x_val, y_val),
        output_signature=(
            tf.TensorSpec(shape=x_val.shape[1:], dtype=tf.float32),
            tf.TensorSpec(shape=y_val.shape[1:], dtype=tf.float32)
        )
    )

    SHUFFLE_BUFFER_SIZE = 1000
    train_batches = (train_dataset
                     .shuffle(SHUFFLE_BUFFER_SIZE)
                     .map(apply_data_augmentation)
                     .batch(batch_size)
                     .repeat()
                     .prefetch(buffer_size=tf.data.experimental.AUTOTUNE))

    validation_batches = validation_dataset.batch(batch_size)

    steps_per_epoch = len(x_train) // batch_size
    val_steps = len(x_val) // batch_size

    return train_batches, validation_batches, steps_per_epoch, val_steps


def train_model(model, train_ds, steps_per_epoch, val_ds, val_steps, epochs, learning_rate):
    """ Trains the model.

    Args:
        model (keras.Model): the model to train
        train_ds (tensorflow.dataset): train data
        steps_per_epoch (int): training steps
        val_ds (tensorflow.dataset): validation data
        val_steps (int): validation steps
        epochs (int): the number of epochs
        learning_rate (float): the learning rate
    """
    # Define learning rate scheduler
    callbacks = [get_cosine_lr_scheduler(learning_rate, epochs * steps_per_epoch, True)]

    # Model checkpoints (save best model and retrieve it when training is complete)
    restore_model = RestoreBest(model, monitor="val_binary_io_u")
    callbacks.append(restore_model)

    history = model.fit(train_ds,
                        epochs=epochs,
                        steps_per_epoch=steps_per_epoch,
                        validation_steps=val_steps,
                        validation_data=val_ds,
                        callbacks=callbacks)
    print_history_stats(history)


def evaluate_akida_model(model, val_ds, val_steps):
    """ Evaluates Akida model.

    Args:
        model (akida.Model): model to evaluate
        val_ds (tensorflow.dataset): validation data
        val_steps (int): validation steps
    """
    # Initialize to None to allow different shapes depending on the caller
    labels = None
    pots = None

    for _ in range(val_steps):
        batch, label_batch = next(iter(val_ds))
        pots_batch = model.predict(batch.numpy().astype('uint8'))

        if labels is None:
            labels = label_batch
            pots = pots_batch
        else:
            labels = np.concatenate((labels, label_batch))
            pots = np.concatenate((pots, pots_batch))
    preds = tf.keras.activations.sigmoid(pots)

    m_binary_iou = tf.keras.metrics.BinaryIoU(target_class_ids=[0, 1], threshold=0.5)
    m_binary_iou.update_state(labels, preds)
    binary_iou = m_binary_iou.result().numpy()

    m_accuracy = tf.keras.metrics.Accuracy()
    m_accuracy.update_state(labels, preds > 0.5)
    accuracy = m_accuracy.result().numpy()
    print(f"Akida BinaryIoU/pixel accuracy: {binary_iou:.4f}/{100*accuracy:.2f}%")


def main():
    """ Entry point for script and CLI usage.

    Note: Download the Portrait-Segmentation dataset from
    [Portrait128website](https://github.com/anilsathyan7/Portrait-Segmentation)
    """
    global_parser = argparse.ArgumentParser(add_help=False)
    global_parser.add_argument("-d", "--data", type=str,
                               required=True,
                               help="Path to the Portrait128 data.")

    parsers = get_training_parser(batch_size=32, tune=True, extract=True,
                                  global_parser=global_parser)
    args = parsers[0].parse_args()

    # Load the source model
    model = load_model(args.model)

    # Compile model
    learning_rate = 3e-5
    if args.action == "tune":
        learning_rate /= 10

    compile_model(model, learning_rate=learning_rate, loss='binary_crossentropy',
                  metrics=[BinaryIoU(), 'accuracy'])

    # Load data
    train_ds, val_ds, steps_per_epoch, val_steps = get_data(args.data, args.batch_size)

    # Disable QuantizeML assertions
    os.environ["ASSERT_ENABLED"] = "0"

    # Train model
    if args.action in ["train", "tune"]:
        train_model(model, train_ds, steps_per_epoch, val_ds,
                    val_steps, args.epochs, learning_rate)
        save_model(model, args.model, args.savemodel, args.action)
    elif args.action == "eval":
        # Evaluate model accuracy
        if args.akida:
            model = convert(model)
            evaluate_akida_model(model, val_ds, val_steps)
        else:
            evaluate_model(model, val_ds, steps=val_steps, print_history=True)
    elif args.action == 'extract':
        # Extract samples from dataset
        extract_samples(args.savefile, train_ds, args.batch_size)


if __name__ == "__main__":
    main()
