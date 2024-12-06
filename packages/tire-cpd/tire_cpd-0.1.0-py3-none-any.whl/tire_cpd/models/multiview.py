import os
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
import tensorflow as tf
if os.environ["CUDA_VISIBLE_DEVICES"] == "0":
    physical_devices = tf.config.list_physical_devices('GPU')
    tf.config.experimental.set_memory_growth(physical_devices[0], True)
from tensorflow import keras
from tensorflow.keras.layers import Input, Dense, Layer, Conv1D, Conv1DTranspose, Flatten, Reshape, ELU, BatchNormalization, ReLU, LeakyReLU
from tensorflow.keras.models import Model
import numpy as np

def create_parallel_AEs(X, enable_summary, ws):
    initializer_glorot = tf.keras.initializers.GlorotUniform()
    initializer_he = tf.keras.initializers.HeUniform()

    # encoder
    input = Input(shape=(X.shape[1], X.shape[2], X.shape[3]), name="data")

    input_TD = input[:, :, :ws, :]
    ws_TD = input_TD.shape[2]
    input_FD = input[:, :, ws:, :]
    ws_FD = input_FD.shape[2]

    conv_S_L1_TD = Conv1D(filters=12, kernel_size=9, padding="same", kernel_initializer=initializer_he, strides=2,
                          activation=None, name="conv_S_L1_TD")
    conv_S_L1_FD = Conv1D(filters=12, kernel_size=9, padding="same", kernel_initializer=initializer_he, strides=2,
                          activation=None, name="conv_S_L1_FD")
    conv_S_L2_TD = Conv1D(filters=4, kernel_size=9, padding="same", kernel_initializer=initializer_he, strides=2,
                          activation=None, name="conv_S_L2_TD")
    conv_S_L2_FD = Conv1D(filters=4, kernel_size=9, padding="same", kernel_initializer=initializer_he, strides=2,
                          activation=None, name="conv_S_L2_FD")
    # conv_S_L3_TD = Conv1D(filters=1, kernel_size=9, padding="same", kernel_initializer=initializer_glorot, strides=1,
    #                       activation="tanh", name="conv_S_L3_TD")
    # conv_S_L3_FD = Conv1D(filters=1, kernel_size=9, padding="same", kernel_initializer=initializer_glorot, strides=1,
    #                       activation="tanh", name="conv_S_L3_FD")

    flatten_TD = Flatten(name="flatten_TD")
    flatten_FD = Flatten(name="flatten_FD")
    dense_TI = Dense(5, activation="tanh", name="dense_TI")
    dense_TV = Dense(5, activation="tanh", name="dense_TV")

    dense_TD = Dense(ws_TD // 4, name="dense_TD")
    dense_FD = Dense(ws_FD // 4, name="dense_FD")
    reshape_TD = Reshape((ws_TD // 4, -1), name="reshape_TD")
    reshape_FD = Reshape((ws_FD // 4, -1), name="reshape_FD")
    deconv_S_L1_TD = Conv1DTranspose(filters=4, kernel_size=9, padding="same", kernel_initializer=initializer_he,
                                     strides=2, activation=None, name="deconv_S_L1_TD")
    deconv_S_L1_FD = Conv1DTranspose(filters=4, kernel_size=9, padding="same", kernel_initializer=initializer_he,
                                     strides=2, activation=None, name="deconv_S_L1_FD")
    deconv_S_L2_TD = Conv1DTranspose(filters=12, kernel_size=9, padding="same", kernel_initializer=initializer_he,
                                     strides=2, activation=None, name="deconv_S_L2_TD")
    deconv_S_L2_FD = Conv1DTranspose(filters=12, kernel_size=9, padding="same", kernel_initializer=initializer_he,
                                     strides=2, activation=None, name="deconv_S_L2_FD")
    deconv_S_L3_TD = Conv1DTranspose(filters=X.shape[3], kernel_size=9, padding="same",
                                     kernel_initializer=initializer_glorot,
                                     strides=1, activation="tanh", name="deconv_S_L3_TD")
    deconv_S_L3_FD = Conv1DTranspose(filters=X.shape[3], kernel_size=9, padding="same",
                                     kernel_initializer=initializer_glorot,
                                     strides=1, activation="tanh", name="deconv_S_L3_FD")
    prelu_activ = ELU(name="elu_activation")

    bn1 = BatchNormalization()

    # extract TI and TV features for windows[0]
    conv_S1_TD = input_TD[:, 0, :, :]
    conv_S2_TD = input_TD[:, 1, :, :]
    conv_S1_FD = input_FD[:, 0, :, :]
    conv_S2_FD = input_FD[:, 1, :, :]

    conv_S1_TD = prelu_activ(conv_S_L1_TD(conv_S1_TD))
    conv_S1_TD = prelu_activ(conv_S_L2_TD(conv_S1_TD))
    # conv_S1_TD = conv_S_L3_TD(conv_S1_TD)
    flatten_S1_TD = flatten_TD(conv_S1_TD)

    conv_S1_FD = prelu_activ(conv_S_L1_FD(conv_S1_FD))
    conv_S1_FD = prelu_activ(conv_S_L2_FD(conv_S1_FD))
    # conv_S1_FD = conv_S_L3_FD(conv_S1_FD)
    flatten_S1_FD = flatten_FD(conv_S1_FD)

    flatten_S1 = tf.concat([flatten_S1_TD, flatten_S1_FD], axis=1)
    flatten_S1 = bn1(flatten_S1)

    TI_S1 = dense_TI(flatten_S1)
    TV_S1 = dense_TV(flatten_S1)

    # extract TI and TV features for windows[1]
    conv_S2_TD = prelu_activ(conv_S_L1_TD(conv_S2_TD))
    conv_S2_TD = prelu_activ(conv_S_L2_TD(conv_S2_TD))
    # conv_S2_TD = conv_S_L3_TD(conv_S2_TD)
    flatten_S2_TD = flatten_TD(conv_S2_TD)

    conv_S2_FD = prelu_activ(conv_S_L1_FD(conv_S2_FD))
    conv_S2_FD = prelu_activ(conv_S_L2_FD(conv_S2_FD))
    # conv_S2_FD = conv_S_L3_FD(conv_S2_FD)
    flatten_S2_FD = flatten_FD(conv_S2_FD)

    flatten_S2 = tf.concat([flatten_S2_TD, flatten_S2_FD], axis=1)
    flatten_S2 = bn1(flatten_S2)

    TI_S2 = dense_TI(flatten_S2)
    TV_S2 = dense_TV(flatten_S2)

    # define the TI features
    TI_features = tf.concat((tf.expand_dims(TI_S1, axis=1), tf.expand_dims(TI_S2, axis=1)), axis=1)

    # get the recoupled combinations to compute the diamond loss
    recoupled_S1 = tf.concat([TI_S2, TV_S1], axis=1)
    recoupled_S2 = tf.concat([TI_S1, TV_S2], axis=1)
    # recoupled_S1 = BatchNormalization()(recoupled_S1)
    # recoupled_S2 = BatchNormalization()(recoupled_S2)

    # reconstruct window[0]
    dense_S1_TD = reshape_TD(prelu_activ(dense_TD(recoupled_S1)))
    deconv_S1_TD = prelu_activ(deconv_S_L1_TD(dense_S1_TD))
    deconv_S1_TD = prelu_activ(deconv_S_L2_TD(deconv_S1_TD))
    deconv_S1_TD = deconv_S_L3_TD(deconv_S1_TD)

    dense_S1_FD = reshape_FD(prelu_activ(dense_FD(recoupled_S1)))
    deconv_S1_FD = prelu_activ(deconv_S_L1_FD(dense_S1_FD))
    deconv_S1_FD = prelu_activ(deconv_S_L2_FD(deconv_S1_FD))
    deconv_S1_FD = deconv_S_L3_FD(deconv_S1_FD)

    deconv_S1 = tf.concat([deconv_S1_TD, deconv_S1_FD], axis=1)

    # reconstruct window[1]
    dense_S2_TD = reshape_TD(prelu_activ(dense_TD(recoupled_S2)))
    deconv_S2_TD = prelu_activ(deconv_S_L1_TD(dense_S2_TD))
    deconv_S2_TD = prelu_activ(deconv_S_L2_TD(deconv_S2_TD))
    deconv_S2_TD = deconv_S_L3_TD(deconv_S2_TD)

    dense_S2_FD = reshape_FD(prelu_activ(dense_FD(recoupled_S2)))
    deconv_S2_FD = prelu_activ(deconv_S_L1_FD(dense_S2_FD))
    deconv_S2_FD = prelu_activ(deconv_S_L2_FD(deconv_S2_FD))
    deconv_S2_FD = deconv_S_L3_FD(deconv_S2_FD)

    deconv_S2 = tf.concat([deconv_S2_TD, deconv_S2_FD], axis=1)

    deconv_S = tf.concat([tf.expand_dims(deconv_S1, axis=1), tf.expand_dims(deconv_S2, axis=1)], axis=1)

    pae = Model(inputs=input, outputs=deconv_S)
    encoder = Model(input, TI_features)
    if enable_summary:
        pae.summary()

    square_diff1 = tf.square(input[:, :, :ws, :] - deconv_S[:, :, :ws, :])
    cp_loss_TD = tf.reduce_mean(square_diff1) / ws_TD

    square_diff2 = tf.square(input[:, :, ws:, :] - deconv_S[:, :, ws:, :])
    cp_loss_FD = tf.reduce_mean(square_diff2) / ws_FD

    pae.add_loss(cp_loss_TD)
    pae.add_metric(cp_loss_TD, name='cp_loss_TD', aggregation='mean')
    pae.add_loss(cp_loss_FD)
    pae.add_metric(cp_loss_FD, name='cp_loss_FD', aggregation='mean')

    # square_diff = tf.square(flatten_S1 - flatten_S2)
    # tfc_loss = tf.reduce_mean(square_diff)
    # pae.add_loss(tfc_loss)
    # pae.add_metric(tfc_loss, name='tfc_loss', aggregation='mean')

    optimizer = keras.optimizers.Adam(learning_rate=1e-3)
    pae.compile(optimizer=optimizer)
    return pae, encoder


def prepare_inputs(windows, nr_ae=2):
    new_windows = []
    nr_windows = windows.shape[0]
    for i in range(nr_ae):
        new_windows.append(windows[i: nr_windows - nr_ae + 1 + i])
    return np.transpose(new_windows, (1, 0, 2, 3))


def concat_windows_bot_domain(windows_TD, windows_FD):
    windows_both = np.concatenate((windows_TD, windows_FD), axis=1)
    return windows_both


def train_model(windows, window_size=40, enable_summary=False, verbose=1, nr_epochs=200, nr_patience=20):
    new_windows = prepare_inputs(windows, nr_ae=2)
    pae, encoder = create_parallel_AEs(new_windows, enable_summary, window_size)
    callback = tf.keras.callbacks.EarlyStopping(monitor='loss', patience=nr_patience)

    pae.fit({'data': new_windows},
            epochs=nr_epochs,
            verbose=verbose,
            batch_size=256,
            shuffle=True,
            validation_split=0.0,
            initial_epoch=0,
            callbacks=[callback]
            )

    encoded_windows = encoder.predict(new_windows)
    encoded_windows = np.concatenate((encoded_windows[:, 0, :], encoded_windows[-1:, 1, :]), axis=0)
    return encoded_windows