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
Input/output on models.
"""

import warnings
import os
import numpy as np
from pathlib import Path
from posixpath import join as urljoin

from onnx import load_model as load_onnx_model

from cnn2snn import load_quantized_model, get_akida_version, AkidaVersion

from quantizeml.models.utils import apply_weights_to_model
import akida


def load_model(model_path, custom_layers=None, compile_model=True):
    """
    Loads an Onnx or Keras or quantized model.
    An error is raised if the provided model extension is not
    supported.

    Args:
        model_path (str): path of the model to load.
        custom_layers (dict, optional): custom layers to add to the Keras model. Defaults to None.
        compile_model (bool, optional): whether to compile the Keras model. Defaults to True.

    Returns:
        keras.models.Model or onnx.ModelProto or Akida.Model : Loaded model.

    Raises:
        ValueError: if the model could not be loaded using Keras and ONNX loaders.
    """
    _, model_extension = os.path.splitext(model_path.lower())

    if model_extension == '.h5':
        model = load_quantized_model(model_path,
                                     custom_objects=custom_layers,
                                     compile_model=compile_model)
    elif model_extension == '.onnx':
        model = load_onnx_model(model_path)
    elif model_extension == '.fbz':
        model = akida.Model(model_path)
    else:
        raise ValueError(
            f"Unsupported model extension: '{model_extension}'. "
            f"Expected model with extension(s): {['h5', 'onnx', 'fbz']}"
        )
    return model


def load_weights(model, weights_path):
    """Loads weights from a npz file and apply it to a model.

    Go through the dictionary of weights of the npz file, find the
    corresponding variable in the model and partially load its weights.

    Args:
        model (keras.Model): the model to update
        weights_path (str): the path of the npz file to load
    """
    # Check the npz file validity
    path = Path(weights_path)
    if not path.is_file():
        raise ValueError(f"File `{weights_path}` not found.")

    # Open the npz file
    weights_dict = np.load(weights_path)

    # Apply the weights to the model
    apply_weights_to_model(model, weights_dict)


def save_weights(model, weights_path):
    """Save model weights on an npz file.

    Takes a model and save the weights of all its layers into an npz file.

    Args:
        model (keras.Model): the model to save its weights
        weights_path (str): the path of the npz file to save
    """
    weights_dict = {}
    for var in model.variables:
        weights_dict[var.name] = var

    np.savez(weights_path, **weights_dict)


def get_model_path(subdir="", model_name_v1=None, file_hash_v1=None, model_name_v2=None,
                   file_hash_v2=None):
    """Selects the model file on the server depending on the AkidaVersion.

    The model path, model name and its hash depends on the Akida version context.

    Args:
        subdir (str, optional): the subdirectory where the model is on the data server.
            Defaults to "".
        model_name_v1 (str, optional): the model v1 name. Defaults to None.
        file_hash_v1 (str, optional): the model file v1 hash. Defaults to None.
        model_name_v2 (str, optional): the model v2 name. Defaults to None.
        file_hash_v2 (str, optional): the model file v2 hash. Defaults to None.

    Returns:
        str, str, str: the model path, model name and file hash.
    """
    assert get_akida_version() in [AkidaVersion.v1, AkidaVersion.v2]
    # To guard against parameter usage errors. For a same version, both parameters should be used
    # or stayed to None.
    assert type(model_name_v1) == type(file_hash_v1), "All v1 parameters should be used"
    assert type(model_name_v2) == type(file_hash_v2), "All v2 parameters should be used"

    if get_akida_version() == AkidaVersion.v1:
        if not model_name_v1:
            raise ValueError('Requested model is not available for Akida v1.')
        warnings.warn(f'Model {model_name_v1} has been trained with akida_models 1.1.10 which is '
                      'the last version supporting 1.0 models training')
        model_base_folder = 'https://data.brainchip.com/models/AkidaV1/'
        model_name = model_name_v1
        file_hash = file_hash_v1
    else:
        if not model_name_v2:
            raise ValueError('Requested model is not available for Akida v2.')
        model_base_folder = 'https://data.brainchip.com/models/AkidaV2/'
        model_name = model_name_v2
        file_hash = file_hash_v2

    # build the full path
    model_path = urljoin(model_base_folder, subdir, model_name)
    return model_path, model_name, file_hash
