import tensorflow as tf
from tensorflow.keras import layers, initializers, Model, Input
from tensorflow.keras.layers import Activation

def swish(x):
    # swish activation function
    b = 1
    return x * tf.math.sigmoid(x)

def GetSafeDepth():
    return 3

activation = swish

# model hyper parameters
initializer = initializers.glorot_normal
normalize = layers.BatchNormalization

#
def GetModel(input_shape, classes, growth_rate,  n_layers_per_block):
    """
    Defines the complete graph model for the Tiramisu based on the provided
    parameters.
    Args:
        x: Tensor, input image to segment.
        training: Bool Tesnor, indicating whether training or not.

    Returns:
        x: Tensor, raw unscaled logits of predicted segmentation.
    """
    # n_layers_per_block #[3, 4, 5, 7, 10, 12]  # [2, 3, 4, 5]
    nb_blocks = len(n_layers_per_block)

    input = Input(input_shape)
    print(input_shape)
    # training = Input(shape=(None,), dtype=tf.bool)
    training = Input(shape=(None,), dtype=tf.bool)
    concats = []
    with tf.compat.v1.variable_scope('encoder'):
        x = layers.Conv2D(filters=48,
                          kernel_size=[3, 3],
                          strides=[1, 1],
                          padding='SAME',
                          dilation_rate=[1, 1],
                          activation=activation,
                          kernel_initializer=initializer(),
                          name='first_conv3x3')(input)
        for block_nb in range(0, nb_blocks):
            dense = dense_block(x, training, block_nb, n_layers_per_block, 'down_dense_block_' + str(block_nb), growth_rate)

            if block_nb != nb_blocks - 1:
                x = tf.concat([x, dense], axis=3, name='down_concat_' + str(block_nb))
                concats.append(x)
                x = transition_down(x, training, x.get_shape()[-1], 'trans_down_' + str(block_nb))

        x = dense

    with tf.compat.v1.variable_scope('decoder'):
        for i, block_nb in enumerate(range(nb_blocks - 1, 0, -1)):
            x = transition_up(x, x.get_shape()[-1], 'trans_up_' + str(block_nb))

            x = tf.concat([x, concats[len(concats) - i - 1]], axis=3, name='up_concat_' + str(block_nb))
            x = dense_block(x, training, block_nb, n_layers_per_block, 'up_dense_block_' + str(block_nb), growth_rate)

    with tf.compat.v1.variable_scope('prediction'):
        x = layers.Conv2D(filters=classes,
                          kernel_size=[1, 1],
                          strides=[1, 1],
                          padding='SAME',
                          dilation_rate=[1, 1],
                          kernel_initializer=initializer(),
                          name='last_conv1x1')(x)
        x = Activation('linear', dtype='float32')(x)
    # x = Activation('linear', dtype='float32')(x)
    model = Model(inputs=[input, training], outputs=x)
    return model


def batch_norm(x, training, name):
    """
    Wrapper for batch normalization in tensorflow, updates moving batch statistics
    if training, uses trained parameters if inferring.
    Args:
        x: Tensor, the input to normalize.
        training: Boolean tensor, indicates if training or not.
        name: String, name of the op in the graph.

    Returns:
        x: Batch normalized input.
    """
    with tf.compat.v1.variable_scope(name):
        x = tf.cond(training, lambda: layers.BatchNormalization(axis=3, trainable=True)(x),
                    lambda: layers.BatchNormalization(axis=3, trainable=False))(x)
    return x


def conv_layer(x, training, filters, name):
    """
    Forms the atomic layer of the tiramisu, does three operation in sequence:
    batch normalization -> Relu -> 2D Convolution.
    Args:
        x: Tensor, input feature map.
        training: Bool Tensor, indicating whether training or not.
        filters: Integer, indicating the number of filters in the output feat. map.
        name: String, naming the op in the graph.

    Returns:
        x: Tensor, Result of applying batch norm -> Relu -> Convolution.
    """
    with tf.name_scope(name):
        #x = batch_norm(x, training, name=name + '_bn')
        x = normalize()(x)
        x = tf.nn.relu(x, name=name + '_relu')
        x = layers.Conv2D(filters=filters,
                          kernel_size=[3, 3],
                          strides=[1, 1],
                          padding='SAME',
                          dilation_rate=[1, 1],
                          activation=activation,
                          kernel_initializer=initializer(),
                          name=name + '_conv3x3')(x)

    return x


def dense_block(x, training, block_nb, layers_per_block, name, growth_rate):
    """
    Forms the dense block of the Tiramisu to calculate features at a specified growth rate.
    Each conv layer in the dense block calculate growth_rate feature maps, which are sequentially
    concatenated to build a larger final output.
    Args:
        x: Tensor, input to the Dense Block.
        training: Bool Tensor, indicating whether training or testing.
        block_nb: Int, identifying the block in the graph.
        name: String, identifying the layers in the graph.

    Returns:
        x: Tesnor, the output of the dense block.
    """
    dense_out = []
    with tf.name_scope(name):
        for i in range(layers_per_block[block_nb]):
            conv = conv_layer(x, training, growth_rate, name=name + '_layer_' + str(i))
            x = tf.concat([conv, x], axis=3)
            dense_out.append(conv)

        x = tf.concat(dense_out, axis=3)

    return x


def transition_down(x, training, filters, name):
    """
    Down-samples the input feature map by half using maxpooling.
    Args:
        x: Tensor, input to downsample.
        training: Bool tensor, indicating whether training or inferring.
        filters: Integer, indicating the number of output filters.
        name: String, identifying the ops in the graph.

    Returns:
        x: Tensor, result of downsampling.
    """
    with tf.name_scope(name):
        #x = batch_norm(x, training, name=name + '_bn')
        x = normalize()(x)
        x = tf.nn.relu(x, name=name + 'relu')
        x = layers.Conv2D(filters=filters,
                          kernel_size=[1, 1],
                          strides=[1, 1],
                          padding='SAME',
                          dilation_rate=[1, 1],
                          activation=activation,
                          kernel_initializer=initializer(),
                          name=name + '_conv1x1')(x)
        x = tf.nn.max_pool(x, [1, 2, 2, 1], [1, 2, 2, 1], padding='SAME', name=name + '_maxpool2x2')

    return x


def transition_up(x, filters, name):
    """
    Up-samples the input feature maps using transpose convolutions.
    Args:
        x: Tensor, input feature map to upsample.
        filters: Integer, number of filters in the output.
        name: String, identifying the op in the graph.

    Returns:
        x: Tensor, result of up-sampling.
    """
    with tf.name_scope(name):
        x = layers.Conv2DTranspose(filters=filters,
                                   kernel_size=[3, 3],
                                   strides=[2, 2],
                                   padding='SAME',
                                   activation=activation,
                                   kernel_initializer=initializer(),
                                   name=name + '_trans_conv3x3')(x)

    return x

