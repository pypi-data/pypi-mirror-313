# Copyright (C) 2023 ETH Zurich
# Institute for Particle Physics and Astrophysics
# Author: Silvan Fischbacher
# created: Mon Nov 06 2023

import numpy as np
import tensorflow as tf
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import Dropout

from edelweiss.tf_utils import EpochProgressCallback


class NeuralNetworkClassifier(BaseEstimator, ClassifierMixin):
    """
    Neural network classifier based on Keras Sequential model

    :param hidden_units: tuple/list, optional (default=(64, 32))
        The number of units per hidden layer
    :param learning_rate: float, optional (default=0.001)
        The learning rate for the Adam optimizer
    :param epochs: int, optional (default=10)
        The number of epochs to train the model
    :param batch_size: int, optional (default=32)
        The batch size for training the model
    :param loss: str, optional (default="auto")
        The loss function to use, defaults to binary_crossentropy if binary and
        sparse_categorical_crossentropy if multiclass
    :param activation: str, optional (default="relu")
        The activation function to use for the hidden layers
    :param activation_output: str, optional (default="auto")
        The activation function to use for the output layer, defaults to sigmoid for
        single class and softmax for multiclass
    :param sample_weight_col: int, optional (default=None)
    """

    def __init__(
        self,
        hidden_units=(64, 32),
        learning_rate=0.001,
        epochs=10,
        batch_size=32,
        loss="auto",
        activation="relu",
        activation_output="auto",
    ):
        self.hidden_units = hidden_units
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.batch_size = batch_size
        self.loss = loss
        self.activation = activation
        self.activation_output = activation_output
        self.model = None

    def fit(self, X, y, sample_weight=None, early_stopping_patience=10):
        """
        Fit the neural network model

        :param X: array-like, shape (n_samples, n_features)
            The training input samples
        :param y: array-like, shape (n_samples,)
            The target values
        :param sample_weight: array-like, shape (n_samples,), optional (default=None)
            Sample weights
        :param early_stopping_patience: int, optional (default=10)
            The number of epochs with no improvement after which training will be
            stopped
        """

        # Encode labels
        self.label_encoder = LabelEncoder()
        y_encoded = self.label_encoder.fit_transform(y)
        self.classes_ = self.label_encoder.classes_

        # Determine if it's binary or multiclass
        self.n_classes_ = len(self.classes_)
        self.is_binary_ = self.n_classes_ == 2

        # Adjust loss and activation_output based on problem type
        if self.loss == "auto":
            self.loss_ = (
                "binary_crossentropy"
                if self.is_binary_
                else "sparse_categorical_crossentropy"
            )
        else:
            self.loss_ = self.loss
        if self.activation_output == "auto":
            self.activation_output_ = "sigmoid" if self.is_binary_ else "softmax"
        else:
            self.activation_output_ = self.activation_output

        # Build the neural network model
        self._build_model(X.shape[1])

        # Compile the model
        self.model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=self.learning_rate),
            loss=self.loss_,
            metrics=["accuracy"],
        )

        # Add early stopping
        early_stopping = EarlyStopping(
            monitor="val_loss",
            patience=early_stopping_patience,
            restore_best_weights=True,
        )

        # Fit the model
        self.model.fit(
            X,
            y_encoded,
            sample_weight=sample_weight,
            epochs=self.epochs,
            batch_size=self.batch_size,
            validation_split=0.2,  # use 20% of the training data as validation data
            callbacks=[early_stopping, EpochProgressCallback(total_epochs=self.epochs)],
            verbose=0,
        )

    def _build_model(self, input_dim):
        """
        Build the neural network model

        :param input_dim: int
            The number of input features
        """
        self.model = tf.keras.Sequential()
        try:
            self.model.add(tf.keras.layers.InputLayer(shape=(input_dim,)))
        except Exception:  # pragma: no cover
            # backwards compatibility for tf<2.16
            self.model.add(tf.keras.layers.InputLayer(input_shape=(input_dim,)))
        for units in self.hidden_units:
            self.model.add(tf.keras.layers.Dense(units, activation=self.activation))
            self.model.add(Dropout(0.2))
        self.model.add(
            tf.keras.layers.Dense(
                1 if self.is_binary_ else self.n_classes_,
                activation=self.activation_output_,
            )
        )
        self.model.summary()

    def predict(self, X):
        """
        Predict the class labels for the provided data

        :param X: array-like, shape (n_samples, n_features)
            The input samples
        :return: array-like, shape (n_samples,)
            The predicted class labels
        """
        y_pred = self.model.predict(X, verbose=0)
        return self.label_encoder.inverse_transform(np.argmax(y_pred, axis=1))

    def predict_proba(self, X):
        """
        Predict the class probabilities for the provided data

        :param X: array-like, shape (n_samples, n_features)
            The input samples
        :return: array-like, shape (n_samples, n_classes)
            The predicted class probabilities
        """
        y_prob = self.model.predict(X, verbose=0)

        # for backwards compatibility
        if not hasattr(self, "is_binary_"):  # pragma: no cover
            self.is_binary_ = True

        if self.is_binary_:
            y_prob = y_prob.flatten()
            return np.column_stack((1 - y_prob, y_prob))
        else:
            return y_prob
