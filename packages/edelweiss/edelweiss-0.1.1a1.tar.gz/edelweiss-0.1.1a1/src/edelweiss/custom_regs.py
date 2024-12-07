# Copyright (C) 2024 ETH Zurich
# Institute for Particle Physics and Astrophysics
# Author: Silvan Fischbacher
# created: Sat Jan 27 2024

import tensorflow as tf
from sklearn.base import BaseEstimator
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import Dropout

from edelweiss.tf_utils import EpochProgressCallback


class NeuralNetworkRegressor(BaseEstimator):
    """
    Neural network regressor based on Keras Sequential model

    :param hidden_units: tuple/list, optional (default=(64, 64))
        The number of units per hidden layer
    :param learning_rate: float, optional (default=0.001)
        The learning rate for the Adam optimizer
    :param epochs: int, optional (default=10)
        The number of epochs to train the model
    :param batch_size: int, optional (default=32)
        The batch size for training the model
    :param loss: str, optional (default="mse")
        The loss function to use
    :param activation: str, optional (default="relu")
        The activation function to use for the hidden layers
    :param activation_output: str, optional (default="linear")
        The activation function to use for the output layer
    """

    def __init__(
        self,
        hidden_units=(64, 64),
        learning_rate=0.001,
        epochs=10,
        batch_size=32,
        loss="mse",
        activation="relu",
        activation_output="linear",
        dropout_prob=0.0,
    ):
        self.hidden_units = hidden_units
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.batch_size = batch_size
        self.loss = loss
        self.activation = activation
        self.activation_output = activation_output
        self.dropout_prob = dropout_prob

    def fit(self, X, y, sample_weight=None, early_stopping_patience=10):
        """
        Fit the neural network model

        :param X: array-like, shape (n_samples, n_features)
            The training input samples
        :param y: array-like, shape (n_samples, n_outputs)
            The target values
        :param sample_weight: array-like, shape (n_samples,), optional (default=None)
        :param early_stopping_patience: int, optional (default=10)
            The number of epochs with no improvement after which training will be
            stopped
        """

        # create model
        model = tf.keras.Sequential()
        model.add(
            tf.keras.layers.Dense(
                self.hidden_units[0],
                input_dim=X.shape[1],
                activation=self.activation,
            )
        )
        for units in self.hidden_units[1:]:
            model.add(tf.keras.layers.Dense(units, activation=self.activation))
            model.add(Dropout(self.dropout_prob))
        model.add(tf.keras.layers.Dense(y.shape[1], activation=self.activation_output))
        model.summary()

        # compile model
        model.compile(
            loss=self.loss,
            optimizer=tf.keras.optimizers.Adam(learning_rate=self.learning_rate),
            metrics=["mse"],
            weighted_metrics=["mse"],
        )

        # fit model
        early_stopping = EarlyStopping(
            monitor="val_loss",
            patience=early_stopping_patience,
            restore_best_weights=True,
        )
        model.fit(
            X,
            y,
            sample_weight=sample_weight,
            epochs=self.epochs,
            batch_size=self.batch_size,
            validation_split=0.2,
            callbacks=[early_stopping, EpochProgressCallback(total_epochs=self.epochs)],
            verbose=0,
        )

        self.model = model

    def predict(self, X):
        """
        Predict the output from the input.

        :param X: the input data
        :return: the predicted output
        """
        return self.model.predict(X, verbose=0)
