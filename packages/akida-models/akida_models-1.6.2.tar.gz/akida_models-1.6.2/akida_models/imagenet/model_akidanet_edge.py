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
This model is an adaptation of the `akidanet_imagenet` model for edge
applications. It is based on AkidaNet with top layers replaced by a quantized
spike extractor and a classification layer.
"""

__all__ = ["akidanet_edge_imagenet", "akidanet_edge_imagenet_pretrained",
           "akidanet_faceidentification_edge_pretrained"]

from keras import Model
from keras.layers import Reshape

from cnn2snn import quantize_layer

from ..layer_blocks import separable_conv_block, dense_block
from ..utils import fetch_file, get_params_by_version
from ..model_io import load_model, get_model_path


def akidanet_edge_imagenet(base_model, classes, base_layer="classifier"):
    """Instantiates an AkidaNet-edge architecture.

    Args:
        base_model (str/keras.Model): an akidanet_imagenet base model.
        classes (int): the number of classes for the edge classifier.
        base_layer (str, optional): the last base layer. Defaults to "classifier".

    Returns:
        keras.Model: a Keras Model instance.
    """
    if isinstance(base_model, str):
        base_model = load_model(base_model)

    try:
        # Identify the base model classifier
        base_classifier = base_model.get_layer(base_layer)
        # Determine if the base model is quantized with CNN2SNN
        is_base_quantized_cnn2snn = str(base_classifier.__module__).startswith("cnn2snn")
        if is_base_quantized_cnn2snn:
            # Remember the classifier weight bitwidth
            wq = base_classifier.quantizer.bitwidth
        # Check the base model is not quantized with QuantizeML
        is_base_quantized_quantizeml = str(base_classifier.__module__).startswith("quantizeml")
        if is_base_quantized_quantizeml:
            raise ValueError("A QuantizeML quantized backbone is not supported, "
                             "use a float model and quantize with QuantizeML.")
    except Exception as e:
        raise ValueError("The base model is not an expected AkidaNet/Imagenet model.") from e

    # Model version management
    fused, _, _ = get_params_by_version()

    # Recreate a model with all layers up to the classifier
    x = base_classifier.input
    x = Reshape((1, 1, x.shape[-1]))(x)
    # Add the new end layer with kernel_size (3, 3) instead of (1, 1) for
    # hardware compatibility reasons
    # Because it will be quantized to 1 bit, the ReLU max_value should be set to 1
    x = separable_conv_block(x,
                             filters=2048,
                             kernel_size=(3, 3),
                             padding='same',
                             use_bias=False,
                             add_batchnorm=True,
                             name='spike_generator',
                             fused=fused,
                             relu_activation='ReLU1')

    # Then add the Akida edge learning layer that will be dropped after
    x = dense_block(x,
                    classes,
                    name="classification_layer",
                    relu_activation=False,
                    add_batchnorm=False,
                    use_bias=False)
    x = Reshape((classes,))(x)

    # Create model
    model = Model(inputs=base_model.input,
                  outputs=x,
                  name=f"{base_model.name}_edge")

    # When targeting Akida V1 and with a quantized base model, edge layers can be quantized with
    # CNN2SNN and tuned which is not the case with a quantizeml quantization.
    # (float head training is required).
    if is_base_quantized_cnn2snn:
        # Quantize edge layers
        model = quantize_layer(model, 'spike_generator', wq)
        model = quantize_layer(model, 'spike_generator/relu', 1)
        # NOTE: quantization set to 2 here, to be as close as
        # possible to the Akida native layer that will replace this one,
        # with binary weights.
        model = quantize_layer(model, 'classification_layer', 2)

    return model


def akidanet_edge_imagenet_pretrained(quantized=True):
    """ Helper method to retrieve a `akidanet_edge_imagenet` model that was
    trained on ImageNet dataset.

    Args:
        quantized (bool): a boolean indicating whether the model should be loaded quantized or not

    Returns:
        keras.Model: a Keras Model instance.

    """
    if quantized:
        model_name_v1 = 'akidanet_imagenet_224_alpha_50_edge_iq8_wq4_aq4.h5'
        file_hash_v1 = '71ffc3acb09e5682e479505f6b288bd2736311ce46d3974bdf7b2c02916e52a8'
        model_name_v2 = 'akidanet_imagenet_224_alpha_0.5_edge_i8_w8_a8.h5'
        file_hash_v2 = '411ace11f534c51431458ed541c0f73b14e520f6787fb5a0b47f671510841aff'
    else:
        model_name_v1 = 'akidanet_imagenet_224_alpha_50_edge.h5'
        file_hash_v1 = '586ab1fb1baf9e171c54bbc6f4e7ef9fd6910bb5b169ef5b9dd5a29122683d31'
        model_name_v2 = 'akidanet_imagenet_224_alpha_0.5_edge.h5'
        file_hash_v2 = '9763ff8d95d2be88766339171c5ffb6f407f706802bb5939d39c87e5218521ed'

    model_path, model_name, file_hash = get_model_path("akidanet_edge", model_name_v1, file_hash_v1,
                                                       model_name_v2, file_hash_v2)
    model_path = fetch_file(model_path,
                            fname=model_name,
                            file_hash=file_hash,
                            cache_subdir='models')
    return load_model(model_path)


def akidanet_faceidentification_edge_pretrained(quantized=True):
    """
    Helper method to retrieve an `akidanet_edge_imagenet` model that was trained
    on CASIA Webface dataset and that performs face identification.

    Args:
        quantized (bool, optional): a boolean indicating whether the model should be loaded
            quantized or not. Defaults to True.

    Returns:
        keras.Model: a Keras Model instance.

    """
    if quantized:
        model_name_v1 = 'akidanet_faceidentification_edge_iq8_wq4_aq4.h5'
        file_hash_v1 = '61838682cc88cec6dc9a347f1a301bfa9e94fbcbc7a52a273789259de07d3104'
        model_name_v2 = 'akidanet_faceidentification_edge_i8_w4_a4.h5'
        file_hash_v2 = '72b90d6cd07a90d0f6bd6293407ca520a5ac74c7fc0b0a264259d54bd80862e8'
    else:
        model_name_v1 = 'akidanet_faceidentification_edge.h5'
        file_hash_v1 = 'fc0e6f06078dcafb503ec8944a871c781297bc120ef6335b17a17f6f8b316bbf'
        model_name_v2 = 'akidanet_faceidentification_edge.h5'
        file_hash_v2 = 'bc5054c3370c8194d27380df0f99c5ac285ce160d04c7776e665436668fe416f'

    model_path, model_name, file_hash = get_model_path("akidanet_edge", model_name_v1, file_hash_v1,
                                                       model_name_v2, file_hash_v2)
    model_path = fetch_file(model_path,
                            fname=model_name,
                            file_hash=file_hash,
                            cache_subdir='models')
    return load_model(model_path)
