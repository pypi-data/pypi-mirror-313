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
Layers blocks definitions.
"""
from functools import partial

from keras.layers import (BatchNormalization, ReLU, Conv2D, DepthwiseConv2D, SeparableConv2D, Dense,
                          MaxPool2D, GlobalAvgPool2D, LayerNormalization, Dropout, Add,
                          Conv2DTranspose, Reshape, Conv3D)
from keras.activations import swish, gelu
from keras.initializers import TruncatedNormal
import tensorflow as tf

from quantizeml.layers import (Attention, LayerMadNormalization, DepthwiseConv2DTranspose,
                               ExtractToken)
from .utils import get_params_by_version


def _add_pooling_layer(x, pooling_type, pool_size, padding, layer_base_name):
    """Add a pooling layer in the graph.

    From an input tensor 'x', the function returns the output tensor after
    a pooling layer defined by 'pooling_type'.

    Args:
        x (tf.Tensor): the input tensor
        pooling_type (str): type of pooling among the following: 'max' or 'global_avg'.
        pool_size (int or tuple of 2 integers): factors by which to
            downscale (vertical, horizontal). (2, 2) will halve the input in
            both spatial dimension. If only one integer is specified, the same
            window length will be used for both dimensions.
        padding (str): one of "valid" or "same" (case-insensitive).
        layer_base_name (str): base name for the pooling layer.

    Returns:
        tf.Tensor: an output tensor after pooling
    """
    if pooling_type == 'max':
        return MaxPool2D(pool_size=pool_size,
                         padding=padding,
                         name=layer_base_name + '/maxpool')(x)
    if pooling_type == 'global_avg':
        return GlobalAvgPool2D(name=layer_base_name + '/global_avg')(x)
    raise ValueError("'pooling_type' argument must be 'max' or 'global_avg'.")


def conv_block(inputs,
               filters,
               kernel_size,
               pooling=None,
               post_relu_gap=False,
               pool_size=(2, 2),
               add_batchnorm=False,
               relu_activation='ReLU3.75',
               **kwargs):
    """Adds a convolutional layer with optional layers in the following order:
    max pooling, batch normalization, activation.

    Args:
        inputs (tf.Tensor): input tensor of shape `(rows, cols, channels)`
        filters (int): the dimensionality of the output space
            (i.e. the number of output filters in the convolution).
        kernel_size (int or tuple of 2 integers): specifying the
            height and width of the 2D convolution kernel.
            Can be a single integer to specify the same value for
            all spatial dimensions.
        pooling (str, optional): add a pooling layer of type 'pooling' among the values 'max' or
            'global_avg', with pooling size set to pool_size. If 'None', no pooling will be added.
        post_relu_gap (bool, optional): when pooling is 'global_avg', indicates if the pooling comes
            before or after ReLU activation. Defaults to False.
        pool_size (int or tuple of 2 integers, optional): factors by which to downscale (vertical,
            horizontal). (2, 2) will halve the input in both spatial dimension. If only one integer
            is specified, the same window length will be used for both dimensions.
        add_batchnorm (bool, optional): add a BatchNormalization layer
        relu_activation (str, optional): the ReLU activation to add to the layer in the form 'ReLUx'
            where 'x' is the max_value to use. Set to False to disable activation. Defaults to
            'ReLU3.75'.
        **kwargs: arguments passed to the keras.Conv2D layer, such as
            strides, padding, use_bias, weight_regularizer, etc.

    Returns:
        tf.Tensor: output tensor of conv2D block.
    """
    if 'activation' in kwargs and kwargs['activation']:
        raise ValueError("Keyword argument 'activation' in conv_block must be None.")
    if 'dilation_rate' in kwargs and kwargs['dilation_rate'] not in [1, [1, 1], (1, 1)]:
        raise ValueError("Keyword argument 'dilation_rate' is not supported in conv_block.")

    conv_layer = Conv2D(filters, kernel_size, **kwargs)
    x = conv_layer(inputs)

    if pooling == 'max' or (pooling == 'global_avg' and not post_relu_gap):
        x = _add_pooling_layer(x, pooling, pool_size, conv_layer.padding, conv_layer.name)

    if add_batchnorm:
        x = BatchNormalization(name=conv_layer.name + '/BN')(x)

    if relu_activation:
        x = act_to_layer(relu_activation, name=conv_layer.name + '/relu')(x)

    if post_relu_gap and pooling == 'global_avg':
        x = _add_pooling_layer(x, pooling, pool_size, conv_layer.padding, conv_layer.name)
    return x


def separable_conv_block(inputs,
                         filters,
                         kernel_size,
                         strides=1,
                         padding="same",
                         use_bias=True,
                         pooling=None,
                         post_relu_gap=False,
                         pool_size=(2, 2),
                         add_batchnorm=False,
                         relu_activation='ReLU3.75',
                         fused=True,
                         name=None,
                         kernel_initializer='glorot_uniform',
                         pointwise_regularizer=None):
    """Adds a separable convolutional layer with optional layers in the
    following order: global average pooling, max pooling, batch normalization,
    activation.

    Args:
        inputs (tf.Tensor): input tensor of shape `(height, width, channels)`
        filters (int): the dimensionality of the output space
            (i.e. the number of output filters in the pointwise convolution).
        kernel_size (int or tuple of 2 integers): specifying the
            height and width of the 2D convolution window. Can be a single
            integer to specify the same value for all spatial dimensions.
        strides (int or tuple of 2 integers, optional): strides of the depthwise convolution.
            Defaults to 1.
        padding (str, optional): padding mode for the depthwise convolution. Defaults to 'same'.
        use_bias (bool, optional): whether the layer uses a bias vector. Defaults to True.
        pooling (str, optional): add a pooling layer of type 'pooling' among the values 'max', or
            'global_avg', with pooling size set to pool_size. If 'None', no pooling will be added.
        post_relu_gap (bool, optional): when pooling is 'global_avg', indicates if the pooling comes
            before or after ReLU activation. Defaults to False.
        pool_size (int or tuple of 2 integers, optional): factors by which to downscale (vertical,
            horizontal). (2, 2) will halve the input in both spatial dimension. If only one integer
            is specified, the same window length will be used for both dimensions.
        add_batchnorm (bool, optional): add a BatchNormalization layer
        relu_activation (str, optional): the ReLU activation to add to the layer in the form 'ReLUx'
            where 'x' is the max_value to use. Set to False to disable activation. Defaults to
            'ReLU3.75'.
        fused (bool, optional): If True use a SeparableConv2D layer otherwise use a
            DepthwiseConv2D + Conv2D layers. Defaults to True.
        name (str, optional): name of the layer. Defaults to None.
        kernel_initializer (keras.initializer, optional): initializer for both kernels. Defaults to
            'glorot_uniform'.
        pointwise_regularizer (keras.regularizers, optional): regularizer function applied to the
            pointwise kernel matrix. Defaults to None.

    Returns:
        tf.Tensor: output tensor of separable conv block.
    """
    if name:
        dw_name = "dw_" + name
        pw_name = "pw_" + name

    else:
        dw_name = pw_name = None
    # if fused set a SeparableConv2D layer
    if fused:
        sep_conv_layer = SeparableConv2D(filters, kernel_size, strides=strides, padding=padding,
                                         use_bias=use_bias,
                                         depthwise_initializer=kernel_initializer,
                                         pointwise_initializer=kernel_initializer,
                                         pointwise_regularizer=pointwise_regularizer,
                                         name=name)
        x = sep_conv_layer(inputs)
        main_layer_name = sep_conv_layer.name
    # if not fused set a DepthwiseConv2D + Conv2D layer (the Conv2D applies a Pointwise convolution)
    else:
        depth_conv_layer = DepthwiseConv2D(kernel_size, strides=strides, padding=padding,
                                           use_bias=False,
                                           depthwise_initializer=kernel_initializer,
                                           name=dw_name)
        point_conv_layer = Conv2D(filters, (1, 1), use_bias=use_bias, padding='same',
                                  kernel_initializer=kernel_initializer,
                                  kernel_regularizer=pointwise_regularizer,
                                  name=pw_name)

        x = depth_conv_layer(inputs)
        x = point_conv_layer(x)

        main_layer_name = point_conv_layer.name

    if pooling == 'max' or (pooling == 'global_avg' and not post_relu_gap):
        x = _add_pooling_layer(x, pooling, pool_size, padding, main_layer_name)

    if add_batchnorm:
        x = BatchNormalization(name=main_layer_name + '/BN')(x)

    if relu_activation:
        x = act_to_layer(relu_activation, name=main_layer_name + '/relu')(x)

    if post_relu_gap and pooling == 'global_avg':
        x = _add_pooling_layer(x, pooling, pool_size, padding, main_layer_name)
    return x


def dense_block(inputs,
                units,
                add_batchnorm=False,
                relu_activation='ReLU3.75',
                **kwargs):
    """Adds a dense layer with optional layers in the following order:
    batch normalization, activation.

    Args:
        inputs (tf.Tensor): Input tensor of shape `(rows, cols, channels)`
        units (int): dimensionality of the output space
        add_batchnorm (bool, optional): add a BatchNormalization layer
        relu_activation (str, optional): the ReLU activation to add to the layer in the form 'ReLUx'
            where 'x' is the max_value to use. Set to False to disable activation. Defaults to
            'ReLU3.75'.
        **kwargs: arguments passed to the Dense layer, such as
            use_bias, kernel_initializer, weight_regularizer, etc.

    Returns:
        tf.Tensor: output tensor of the dense block.
    """
    if 'activation' in kwargs and kwargs['activation']:
        raise ValueError("Keyword argument 'activation' in dense_block must be None.")

    dense_layer = Dense(units, **kwargs)
    x = dense_layer(inputs)

    if add_batchnorm:
        x = BatchNormalization(name=dense_layer.name + '/BN')(x)

    if relu_activation:
        x = act_to_layer(relu_activation, name=dense_layer.name + '/relu')(x)

    return x


def act_to_layer(act, **kwargs):
    """ Get activation layer from string.

    This is needed because one cannot serialize a class in layer.get_config, the string is thus
    serialized instead.

    Args:
        act (str): string that values in ['GeLU', 'ReLUx', 'swish'] and that allows to choose from
            GeLU, ReLUx or swish activation inside MLP.

    Returns:
        keras.layers: the activation layer class
    """
    if act == 'GeLU':
        act_funct = gelu
    elif 'ReLU' in act:
        if act == 'ReLU':
            max_value = None
        else:
            try:
                max_value = float(act[4:])
            except ValueError:
                raise ValueError("ReLU must be in the form 'ReLUx', where x is the max-value")
        act_funct = ReLU(max_value=max_value, **kwargs)
    elif act == 'swish':
        act_funct = swish
    else:
        raise NotImplementedError(
            f"act should be in ['GeLU', 'ReLUx', 'swish'] but received {act}.")

    return act_funct


def norm_to_layer(norm):
    """ Get normalization layer from string.

    This is needed because one cannot serialize a class in layer.get_config, the string is thus
    serialized instead.

    Args:
        norm (str): string that values in ['LN', 'GN1', 'BN', 'LMN'] and that allows to choose from
            LayerNormalization, GroupNormalization(groups=1, ...), BatchNormalization or
            LayerMadNormalization layers respectively in the model.

    Returns:
        keras.layers: the normalization layer class
    """
    if norm == 'LN':
        norm_funct = LayerNormalization
    elif norm == 'GN1':
        norm_funct = partial(tf.keras.layers.GroupNormalization, groups=1)
    elif norm == 'BN':
        norm_funct = BatchNormalization
    elif norm == 'LMN':
        norm_funct = LayerMadNormalization
    else:
        raise NotImplementedError("norm should be in ['LN', 'GN1', 'BN', 'LMN']"
                                  f" but received {norm}.")

    return norm_funct


def mlp_block(inputs, mlp_dim, dropout, name, mlp_act="GeLU"):
    """ MLP block definition.

    Args:
        inputs (tf.Tensor): inputs
        mlp_dim (int): number of units in the first dense layer
        dropout (float): dropout rate
        name (str): used as a base name for the layers in the block
        mlp_act (str, optional): string that values in ['GeLU', 'ReLUx', 'swish'] and that allows to
            choose from GeLU, ReLUx or swish activation. Defaults to "GeLU".

    Returns:
        tf.Tensor: MLP block outputs
    """
    initializer = {
        "kernel_initializer": TruncatedNormal(stddev=0.02),
        "bias_initializer": "zeros",
    }
    x = Dense(
        mlp_dim,
        name=f"{name}/Dense_0",
        **initializer,
    )(inputs)
    x = act_to_layer(mlp_act, name=f"{name}/activation")(x)
    x = Dropout(dropout)(x)
    x = Dense(
        inputs.shape[-1],
        name=f"{name}/Dense_1",
        **initializer,
    )(x)
    outputs = Dropout(dropout)(x)
    return outputs


def multi_head_attention(x, num_heads, hidden_size, name, softmax="softmax"):
    """Multi-head attention block definition.

    Args:
        x (tf.Tensor): inputs
        num_heads (int): the number of attention heads
        hidden_size (int): query, key and value dense layers representation size (units)
        name (str): used as a base name for the layers in the block
        softmax (str, optional): string with values in ['softmax', 'softmax2'] that allows to choose
            between softmax and softmax2 activation. Defaults to 'softmax'.

    Raises:
        ValueError: if hidden_size is not a multiple of num_heads

    Returns:
        (tf.Tensor, tf.Tensor): block outputs and attention softmaxed scores
    """
    if hidden_size % num_heads != 0:
        raise ValueError(
            f"Embedding dimension = {hidden_size} should be divisible "
            f"by number of heads = {num_heads}"
        )
    initializer = {
        "kernel_initializer": TruncatedNormal(stddev=0.02),
        "bias_initializer": "zeros",
    }
    query = Dense(hidden_size, name=f"{name}/query", **initializer)(x)
    key = Dense(hidden_size, name=f"{name}/key", **initializer)(x)
    value = Dense(hidden_size, name=f"{name}/value", **initializer)(x)
    attention, weights = Attention(num_heads=num_heads, softmax=softmax,
                                   name=f"{name}/attention")([query, key, value])
    output = Dense(hidden_size, name=f"{name}/out", **initializer)(attention)
    return output, weights


def transformer_block(inputs, num_heads, hidden_size, mlp_dim, dropout, name,
                      norm='LN', softmax='softmax', mlp_act="GeLU"):
    """Transformer block definition.

    Args:
        inputs (tf.Tensor): inputs
        num_heads (int): the number of attention heads
        hidden_size (int): multi-head attention block internal size
        mlp_dim (int): MLP block internal size
        dropout (float): dropout rate
        name (str): used as a base name for the layers in the block
        norm (str, optional): string that values in ['LN', 'GN1', 'BN', 'LMN'] and that allows to
            choose from LayerNormalization, GroupNormalization(groups=1, ...), BatchNormalization
            or LayerMadNormalization layers respectively in the block. Defaults to 'LN'.
        softmax (str, optional): string with values in ['softmax', 'softmax2'] that allows to choose
            between softmax and softmax2 activation in attention. Defaults to 'softmax'.
        mlp_act (str, optional): string that values in ['GeLU', 'ReLUx', 'swish'] and that allows to
            choose from GeLU, ReLUx or swish activation in the MLP block. Defaults to "GeLU".

    Returns:
        (tf.Tensor, (tf.Tensor, tf.Tensor)): block outputs and (attention softmaxed scores, the
        normalized sum of inputs and attention outputs)
    """
    x = norm_to_layer(norm)(epsilon=1e-6, name=f"{name}/LayerNorm_0")(inputs)
    x, weights = multi_head_attention(x,
                                      num_heads=num_heads,
                                      hidden_size=hidden_size,
                                      name=f"{name}/MultiHeadDotProductAttention_1",
                                      softmax=softmax
                                      )
    x = Dropout(dropout)(x)
    x_norm2 = Add(name=f"{name}/add_1")([x, inputs])
    y = norm_to_layer(norm)(epsilon=1e-6, name=f"{name}/LayerNorm_2")(x_norm2)
    y = mlp_block(y, mlp_dim, dropout, f"{name}/MlpBlock", mlp_act)
    outputs = Add(name=f"{name}/add_2")([x_norm2, y])
    return outputs, (weights, x_norm2)


def conv_transpose_block(inputs,
                         filters,
                         kernel_size,
                         add_batchnorm=False,
                         relu_activation='ReLU8',
                         **kwargs):
    """Adds a transposed convolutional layer with optional layers in the following order:
    batch normalization, activation.

    Args:
        inputs (tf.Tensor): input tensor of shape `(rows, cols, channels)`
        filters (int): the dimensionality of the output space (i.e. the number of output filters in
            the convolution).
        kernel_size (int or tuple of 2 integers): specifying the height and width of the 2D
            convolution kernel. Can be a single integer to specify the same value for all spatial
            dimensions.
        add_batchnorm (bool, optional): add a BatchNormalization layer. Defaults to False.
        relu_activation (str, optional): the ReLU activation to add to the layer in the form 'ReLUx'
            where 'x' is the max_value to use. Set to False to disable activation. Defaults to
            'ReLU3.75'.
        **kwargs: arguments passed to the keras.Conv2DTranspose layer, such as strides, padding,
            use_bias, weight_regularizer, etc.

    Returns:
        tf.Tensor: output tensor of transposed convolution block.
    """
    if 'activation' in kwargs and kwargs['activation']:
        raise ValueError("Keyword argument 'activation' in conv_transpose_block must be None.")
    if 'dilation_rate' in kwargs and kwargs['dilation_rate'] not in [1, [1, 1], (1, 1)]:
        raise ValueError("Keyword argument 'dilation_rate' is not supported in "
                         "conv_transpose_block.")

    conv_trans_layer = Conv2DTranspose(filters, kernel_size, **kwargs)
    x = conv_trans_layer(inputs)

    if add_batchnorm:
        x = BatchNormalization(name=conv_trans_layer.name + '/BN')(x)

    if relu_activation:
        x = act_to_layer(relu_activation, name=conv_trans_layer.name + '/relu')(x)

    return x


def sepconv_transpose_block(inputs,
                            filters,
                            kernel_size,
                            strides=2,
                            padding='same',
                            use_bias=True,
                            add_batchnorm=False,
                            relu_activation='ReLU3.75',
                            name=None,
                            kernel_initializer='glorot_uniform',
                            pointwise_regularizer=None):
    """Adds a transposed separable convolutional layer with optional layers in the following order:
    batch normalization, activation.

    The separable operation is made of a DepthwiseConv2DTranspose followed by a pointwise Conv2D.

    Args:
        inputs (tf.Tensor): input tensor of shape `(rows, cols, channels)`
        filters (int): the dimensionality of the output space (i.e. the number of output filters in
            the pointwise convolution).
        kernel_size (int or tuple of 2 integers): specifying the height and width of the depthwise
            transpose kernel. Can be a single integer to specify the same value for all spatial
            dimensions.
        strides (int or tuple of 2 integers, optional): strides of the transposed depthwise.
            Defaults to 2.
        padding (str, optional): padding mode for the transposed depthwise. Defaults to 'same'.
        use_bias (bool, optional): whether the layer uses a bias vectors. Defaults to True.
        add_batchnorm (bool, optional): add a BatchNormalization layer. Defaults to False.
        relu_activation (str, optional): the ReLU activation to add to the layer in the form 'ReLUx'
            where 'x' is the max_value to use. Set to False to disable activation. Defaults to
            'ReLU3.75'.
        name (str, optional): name of the layer. Defaults to None.
        kernel_initializer (keras.initializer, optional): initializer for both kernels. Defaults to
            'glorot_uniform'.
        pointwise_regularizer (keras.regularizers, optional): regularizer function applied to the
            pointwise kernel matrix. Defaults to None.

    Returns:
        tf.Tensor: output tensor of transposed separable convolution block.
    """
    if name:
        dw_name = "dw_" + name
        pw_name = "pw_" + name
    else:
        dw_name, pw_name = None, None

    dw_trans_layer = DepthwiseConv2DTranspose(kernel_size,
                                              strides=strides,
                                              padding=padding,
                                              use_bias=use_bias,
                                              depthwise_initializer=kernel_initializer,
                                              name=dw_name)
    pw_layer = Conv2D(filters,
                      kernel_size=1,
                      padding='valid',
                      use_bias=use_bias,
                      kernel_regularizer=pointwise_regularizer,
                      kernel_initializer=kernel_initializer,
                      name=pw_name)

    x = dw_trans_layer(inputs)
    x = pw_layer(x)

    if add_batchnorm:
        x = BatchNormalization(name=pw_layer.name + '/BN')(x)

    if relu_activation:
        x = act_to_layer(relu_activation, name=pw_layer.name + '/relu')(x)

    return x


def yolo_head_block(x, num_boxes, classes, filters=1024):
    """Adds the `YOLOv2 detection head <https://arxiv.org/pdf/1612.08242.pdf>`_, at the output
    of a model.

    Args:
        x (:obj:`tf.Tensor`): input tensor of shape `(rows, cols, channels)`.
        num_boxes (int): number of boxes.
        classes (int): number of classes.
        filters (int, optional): number of filters in hidden layers. Defaults to 1024.

    Returns:
        :obj:`tf.Tensor`: output tensor of yolo detection head block.

    Notes:
        This block replaces conv layers by separable_conv, to decrease the amount of parameters.
    """
    # Model version management
    fused, _, relu_activation = get_params_by_version(relu_v2='ReLU7.5')

    x = separable_conv_block(x, filters=filters, name='1conv',
                             kernel_size=(3, 3), padding='same', use_bias=False,
                             relu_activation=relu_activation, add_batchnorm=True, fused=fused)
    x = separable_conv_block(x, filters=filters, name='2conv',
                             kernel_size=(3, 3), padding='same', use_bias=False,
                             relu_activation=relu_activation, add_batchnorm=True, fused=fused)
    x = separable_conv_block(x, filters=filters, name='3conv',
                             kernel_size=(3, 3), padding='same', use_bias=False,
                             relu_activation=relu_activation, add_batchnorm=True, fused=fused)
    x = separable_conv_block(x, filters=(num_boxes * (4 + 1 + classes)), name='detection_layer',
                             kernel_size=(3, 3), padding='same', use_bias=True,
                             relu_activation=False, add_batchnorm=False, fused=fused)
    return x


def vit_extract_feature_map(y, feat_shape, num_non_patch=1):
    """Add a ExtractToken + Reshape layers to convert the plain ViT output into a feature map.

    All tokens will be extracted except those considered as class tokens (``num_non_patch``)

    Args:
        y (:obj:`tf.Tensor`): output of ViT classifier model.
        feat_shape (tuple of int): height/width desired output size
        num_non_patch (int, optional): number of non-patch tokens to exclude on the final output.
            Defaults to 1.

    Returns:
        :obj:`keras.Model`: ViT with new layers
    """
    y = ExtractToken(name="extract_features", token=list(range(num_non_patch, y.shape[1])))(y)
    y = Reshape(target_shape=(*feat_shape, y.shape[-1]), name="features")(y)
    return y


def conv3d_block(inputs,
                 filters,
                 kernel_size,
                 add_batchnorm=False,
                 relu_activation='ReLU3.75',
                 reg_factor=None,
                 **kwargs):
    """Adds a Conv3D layer with optional layers: batch normalization and activation.

    Args:
        inputs (tf.Tensor): input tensor
        filters (int): the dimensionality of the output space
        kernel_size (int or tuple): dimensions of the convolution kernel.
        add_batchnorm (bool, optional): add a BatchNormalization layer. Defaults to False.
        relu_activation (str, optional): the ReLU activation to add to the layer in the form 'ReLUx'
            where 'x' is the max_value to use. Set to False to disable activation. Defaults to
            'ReLU3.75'.
        reg_factor (float, optional): the L1-regularization factor of the ActivityRegularization
            layers that are added after the ReLU layers if reg_factor is not None.
            Defaults to None.
        **kwargs: arguments passed to the keras.Conv3D layer, such as strides, use_bias, etc.

    Returns:
        tf.Tensor: output tensor of conv2D block.
    """
    if 'activation' in kwargs and kwargs['activation']:
        raise ValueError("Keyword argument 'activation' in conv3d_block must be None.")
    # If it's a temporal Conv3d with a same padding, convert it to a one sided-left padding,
    # by adding a ZeroPadding3D layer and setting the Conv3D padding to "valid"
    if kernel_size[0] != 1 and kwargs.get('padding', 'valid') == 'same':
        padding_layer = tf.keras.layers.ZeroPadding3D(
            padding=((kernel_size[0] - 1, 0), (0, 0), (0, 0)))
        inputs = padding_layer(inputs)
        kwargs['padding'] = 'valid'
    conv_layer = Conv3D(filters, kernel_size, **kwargs)
    x = conv_layer(inputs)

    if add_batchnorm:
        x = BatchNormalization(name=conv_layer.name + '/BN')(x)

    if relu_activation:
        x = act_to_layer(relu_activation, name=conv_layer.name + '/relu')(x)
        if reg_factor:
            x = tf.keras.layers.ActivityRegularization(l1=reg_factor)(x)
    return x


def spatiotemporal_block(inputs, in_channels, med_channels, out_channels, t_kernel_size, t_stride,
                         t_depthwise, s_depthwise, index, reg_factor=None):
    """ Add a spatiotemporal block to the inputs.

    The spatio-temporal block consists of a temporal convolution (potentially separable) followed by
    a spatial convolution (potentially separable).

    Note that the depthwise layers are implemented as Conv3D with groups=filters because TensorFlow
    does not have a DepthwiseConv3D layer.

    Args:
        inputs (tf.Tensor): input tensor
        in_channels (int): input channels
        med_channels (int): middle channels (channels after the temporal conv layer)
        out_channels (int): output channels (channels after the spatial conv layer)
        t_kernel_size (int): the temporal kernel size
        t_stride (int): the temporal kernel stride
        t_depthwise (bool): whether the temporal layer is dw_separable
        s_depthwise (bool): whether the spatial layer is dw_separable
        index (int): index of the block
        reg_factor (float, optional): the L1-regularization factor of the ActivityRegularization
            layers that are added after the ReLU layers if reg_factor is not None.
            Defaults to None.

    Returns:
        tf.Tensor: output tensor of the spatiotemporal block.
    """
    if not t_depthwise:
        x = conv3d_block(inputs,
                         med_channels,
                         (t_kernel_size, 1, 1),
                         add_batchnorm=True,
                         relu_activation='ReLU',
                         strides=(t_stride, 1, 1),
                         padding='same',
                         use_bias=True,
                         name=f'convt_full_{index}',
                         reg_factor=reg_factor)
    else:
        # This is a DepthwiseConv3D (groups=filters)
        x = conv3d_block(inputs,
                         in_channels,
                         (t_kernel_size, 1, 1),
                         add_batchnorm=True,
                         relu_activation='ReLU',
                         strides=(t_stride, 1, 1),
                         padding='same',
                         groups=in_channels,
                         use_bias=False,
                         name=f'convt_dw_{index}',
                         reg_factor=reg_factor)
        x = conv3d_block(x,
                         med_channels,
                         (1, 1, 1),
                         add_batchnorm=True,
                         relu_activation='ReLU',
                         name=f'convt_pw_{index}',
                         reg_factor=reg_factor)

    if not s_depthwise:
        x = conv3d_block(x,
                         out_channels,
                         (1, 3, 3),
                         add_batchnorm=True,
                         relu_activation='ReLU',
                         strides=(1, 2, 2),
                         padding='same',
                         use_bias=True,
                         name=f'convs_full_{index}',
                         reg_factor=reg_factor)
    else:
        # This is a DepthwiseConv3D (groups=filters)
        x = conv3d_block(x,
                         med_channels,
                         (1, 3, 3),
                         add_batchnorm=True,
                         relu_activation='ReLU',
                         strides=(1, 2, 2),
                         padding='same',
                         groups=med_channels,
                         use_bias=False,
                         name=f'convs_dw_{index}',
                         reg_factor=reg_factor)
        x = conv3d_block(x,
                         out_channels,
                         (1, 1, 1),
                         add_batchnorm=True,
                         relu_activation='ReLU',
                         name=f'convs_pw_{index}',
                         reg_factor=reg_factor)
    return x
