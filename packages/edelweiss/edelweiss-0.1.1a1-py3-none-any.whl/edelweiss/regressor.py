# Copyright (C) 2024 ETH Zurich
# Institute for Particle Physics and Astrophysics
# Author: Silvan Fischbacher
# created: Sat Jan 27 2024


import os
import pickle

import joblib
import numpy as np
from cosmic_toolbox import arraytools as at
from cosmic_toolbox import file_utils, logger
from sklearn.utils.class_weight import compute_sample_weight

from edelweiss import clf_utils, reg_utils

LOGGER = logger.get_logger(__file__)


def load_regressor(path, name="regressor"):
    """
    Load a regressor from a given path.

    :param path: path to the folder containing the regressor
    :param name: the name of the regressor
    :return: the loaded regressor
    """
    with open(os.path.join(path, name + ".pkl"), "rb") as f:
        reg = pickle.load(f)
    reg.pipe = joblib.load(os.path.join(path, "model.pkl"))
    LOGGER.info(f"Regressor loaded from {path}")
    return reg


class Regressor:
    """
    Wrapper class for a several regression models.

    :param scaler: the scaler to use for the regressor
    :param reg: the regressor to use
    :param cv: number of cross validation folds, if 0 no cross validation is performed
    :param cv_scoring: the scoring method to use for cross validation
    :param input_params: the names of the input parameters
    :param output_params: the names of the output parameters
    :param reg_kwargs: additional keyword arguments for the regressor

    """

    def __init__(
        self,
        scaler="standard",
        reg="linear",
        cv=0,
        cv_scoring="neg_mean_squared_error",
        input_params=None,
        output_params=None,
        **reg_kwargs,
    ):
        """
        Initialize the regressor.
        """
        self.scaler = scaler
        sc = clf_utils.get_scaler(scaler)
        self.y_scaler = clf_utils.get_scaler(scaler)
        self.reg = reg
        self.pipe = reg_utils.get_regressor(reg, sc, **reg_kwargs)
        self.cv = cv
        self.cv_scoring = cv_scoring
        self.reg_kwargs = reg_kwargs
        self.input_params = input_params
        self.output_params = output_params
        self._regressor = None
        self._scaler = None
        self.mad = None
        self.mse = None
        self.max_error = None

    def train(self, X, y, flat_param=None, **args):
        """
        Train the regressor.

        :param X: the training data
        :param y: the training labels
        """
        X, y = self._check_if_recarray(X, y)

        if self.input_params is None:
            self.input_params = []
            for i in range(X.shape[1]):
                self.input_params.append(f"param_{i}")
        if self.output_params is None:
            self.output_params = []
            for i in range(y.shape[1]):
                self.output_params.append(f"param_{i}")

        LOGGER.info("Training regressor")
        LOGGER.info(f"Input parameters: {self.input_params}")
        LOGGER.info(f"Output parameters: {self.output_params}")
        LOGGER.info(f"Number of training samples: {X.shape[0]}")

        if self.cv > 1:
            LOGGER.error("Cross validation not implemented yet")

        y = self.y_scaler.fit_transform(y)

        sample_weight = None
        if flat_param is not None:
            flat_param_index = np.where(np.array(self.input_params) == flat_param)[0]
            if len(flat_param_index) == 0:
                # flat param is an output param
                flat_param_index = np.where(np.array(self.output_params) == flat_param)[
                    0
                ]
                sample_weight = compute_sample_weight(
                    "balanced", y[:, flat_param_index]
                )
            else:
                # flat param is an input param
                flat_param_index = flat_param_index[0]
                sample_weight = compute_sample_weight(
                    "balanced", X[:, flat_param_index]
                )
            self.pipe.fit(X, y, reg__sample_weight=sample_weight, **args)
        else:
            self.pipe.fit(X, y, **args)

    fit = train

    def _predict(self, X):
        """
        Predict the output from the input.

        :param X: the input data
        :return: the predicted output as an array
        """
        X, _ = self._check_if_recarray(X, None)
        y = np.atleast_2d(self.pipe.predict(X))
        return self.y_scaler.inverse_transform(y)

    def predict(self, X):
        """
        Predict the output from the input.

        :param X: the input data
        :return: the predicted output as a recarray
        """
        y = self._predict(X)
        return at.arr2rec(y, names=self.output_params)

    __call__ = predict

    def test(self, X, y):
        """
        Test the regressor.

        :param X: the test data
        :param y: the test labels
        """
        X, y = self._check_if_recarray(X, y)
        LOGGER.info("Testing regressor")
        LOGGER.info(f"Number of test samples: {X.shape[0]}")
        y_pred = self._predict(X)
        mad = np.mean(np.abs(y - y_pred), axis=0)
        mse = np.mean((y - y_pred) ** 2, axis=0)
        max_error = np.max(np.abs(y - y_pred), axis=0)
        self.mad = at.arr2rec(mad, names=self.output_params)
        self.mse = at.arr2rec(mse, names=self.output_params)
        self.max_error = at.arr2rec(max_error, names=self.output_params)
        LOGGER.info(f"max MAD: {max(mad)}")
        LOGGER.info(f"max MSE: {max(mse)}")
        LOGGER.info(f"max Max error: {max(max_error)}")

        relative_mad = mad / np.mean(np.abs(y), axis=0)
        relative_mse = mse / np.mean(y**2, axis=0)
        relative_max_error = max_error / np.max(np.abs(y), axis=0)
        self.relative_mad = at.arr2rec(relative_mad, names=self.output_params)
        self.relative_mse = at.arr2rec(relative_mse, names=self.output_params)
        self.relative_max_error = at.arr2rec(
            relative_max_error, names=self.output_params
        )
        LOGGER.info(f"max relative MAD: {max(relative_mad)}")
        LOGGER.info(f"max relative MSE: {max(relative_mse)}")
        LOGGER.info(f"max relative Max error: {max(relative_max_error)}")

    def save(self, path, name="regressor"):
        """
        Save the regressor to a given path.

        :param path: the path where to save the regressor
        :param name: the name of the regressor
        """
        file_utils.robust_makedirs(path)
        joblib.dump(self.pipe, os.path.join(path, "model.pkl"))
        with open(os.path.join(path, name + ".pkl"), "wb") as f:
            pickle.dump(self, f)
        LOGGER.info(f"Regressor saved to {path}")

    def _check_if_recarray(self, X, y=None):
        try:
            X, x_names = at.rec2arr(X, return_names=True)
            if self.input_params is None:
                self.input_params = x_names
            if y is not None:
                y, y_names = at.rec2arr(y, return_names=True)
                if self.output_params is None:
                    self.output_params = y_names
        except Exception:
            # is already a normal array
            return X, y
        assert self.input_params == x_names, "Input parameters do not match"
        if y is not None:
            assert self.output_params == y_names, "Output parameters do not match"
        return X, y
