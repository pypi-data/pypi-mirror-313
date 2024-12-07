# Copyright (C) 2023 ETH Zurich
# Institute for Particle Physics and Astrophysics
# Author: Silvan Fischbacher

import os
import pickle

import joblib
import numpy as np
import pandas as pd
from cosmic_toolbox import file_utils, logger
from pzflow import Flow

from edelweiss import nflow_utils

LOGGER = logger.get_logger(__file__)


def load_nflow(path, band=None, subfolder=None):
    """
    Load a normalizing flow from a given path.

    :param path: path to the folder containing the emulator
    :param band: the band to load (if None, assumes that there is only one nflow)
    :param subfolder: subfolder of the emulator folder where the normalizing flow is
                      stored
    :return: the loaded normalizing flow
    """
    if subfolder is None:
        subfolder = "nflow"
    if band is not None:
        subfolder = subfolder + "_" + band
    output_directory = os.path.join(path, subfolder)
    with open(os.path.join(output_directory, "nflow.pkl"), "rb") as f:
        nflow = pickle.load(f)
    nflow.flow = Flow(file=os.path.join(output_directory, "model.pkl"))
    nflow.scaler_input = joblib.load(
        os.path.join(output_directory, "scalers/flow_scaler_input.pkl")
    )
    nflow.scaler_output = joblib.load(
        os.path.join(output_directory, "scalers/flow_scaler_output.pkl")
    )
    return nflow


class Nflow:
    """
    The normalizing flow class that wraps a pzflow normalizing flow.

    :param output: the names of the output parameters
    :param input: the names of the input parameters (=conditional parameters)
    :param scaler: the scaler to use for the normalizing flow
    """

    def __init__(self, output=None, input=None, scaler="standard"):
        """
        Initialize the normalizing flow.
        """
        if isinstance(input, tuple):
            input = np.array(input)
        if isinstance(output, tuple):
            output = np.array(output)
        self.input = input
        self.output = output
        if input is None:
            input = []
        if output is None:
            output = []
        self.all_params = np.concatenate([input, output])
        self.scaler = scaler
        self.scaler_input, self.scaler_output = nflow_utils.get_scalers(scaler)

    def train(
        self,
        X,
        epochs=100,
        batch_size=1024,
        progress_bar=True,
        verbose=True,
        min_loss=5,
    ):
        """
        Train the normalizing flow.

        :param X: the features to train on (recarray)
        :param epochs: number of epochs
        :param batch_size: batch size
        :param progress_bar: whether to show a progress bar
        :param verbose: whether to print the losses
        :param min_loss: minimum loss that is allowed for convergence
        """
        self.epochs = epochs
        self.batch_size = batch_size
        LOGGER.info("==============================")
        LOGGER.info("Training normalizing flow with")
        LOGGER.info(f"{len(X)} samples and")
        LOGGER.info(f"conditional parameters: {self.input}")
        LOGGER.info(f"other parameters: {self.output}")
        LOGGER.info("==============================")

        X = pd.DataFrame(X)
        if self.input is not None:
            X[self.input] = self.scaler_input.fit_transform(X[self.input])
        if self.output is None:
            self.output = X.columns
            self.all_params = self.output
        X[self.output] = self.scaler_output.fit_transform(X[self.output])

        self.flow = Flow(data_columns=self.output, conditional_columns=self.input)

        self.losses = self.flow.train(
            X,
            epochs=epochs,
            batch_size=batch_size,
            progress_bar=progress_bar,
            verbose=verbose,
        )
        nflow_utils.check_convergence(self.losses, min_loss=min_loss)
        LOGGER.info(
            "Training completed with best loss at"
            f" epoch {np.argmin(self.losses)}/{self.epochs}"
            f" with loss {np.min(self.losses):.2f}"
        )

    fit = train

    def sample(self, X=None, n_samples=1):
        """
        Sample from the normalizing flow.

        :param X: the features to sample from (recarray or None for non-conditional
                  sampling)
        :param n_samples: number of samples to draw, number of total samples is
                          n_samples * len(X)
        :return: the sampled features (including the conditional parameters)
        """

        if X is not None:
            params = X.dtype.names
            assert np.all(
                list(params) == self.input
            ), "Input parameters do not match the trained parameters"

            X = pd.DataFrame(X)
            X[self.input] = self.scaler_input.transform(X[self.input])

        f = self.flow.sample(n_samples, conditions=X)
        f = f.reindex(columns=self.all_params)

        # Find NaNs and replace with mean
        f.replace([np.inf, -np.inf], np.nan, inplace=True)
        nan_inf_mask = f.isna()
        n_nans = f.isna().sum().sum()
        if n_nans > 0:
            LOGGER.warning(f"Found {n_nans} NaNs or infs in the sampled data")
            column_means = f.mean()
            f.fillna(column_means, inplace=True)

        # Inverse transform
        if self.input is not None:
            f[self.input] = self.scaler_input.inverse_transform(f[self.input])
        f[self.output] = self.scaler_output.inverse_transform(f[self.output])

        # Reintroduce NaNs
        f[nan_inf_mask] = np.nan
        return f.to_records(index=False)

    __call__ = sample

    def save(self, path, band=None, subfolder=None):
        """
        Save the normalizing flow to a given path.

        :param path: path to the folder where the emulator is saved
        :param subfolder: subfolder of the emulator folder where the normalizing flow is
                          stored
        """
        if subfolder is None:
            subfolder = "nflow"
        if band is not None:
            subfolder = subfolder + "_" + band
        output_directory = os.path.join(path, subfolder)
        file_utils.robust_makedirs(output_directory)

        flow_path = os.path.join(output_directory, "model.pkl")
        self.flow.save(flow_path)
        self.flow = None
        LOGGER.debug(f"Flow saved to {flow_path}")

        scaler_path = os.path.join(output_directory, "scalers")
        file_utils.robust_makedirs(scaler_path)
        scaler_input_path = os.path.join(scaler_path, "flow_scaler_input.pkl")
        scaler_output_path = os.path.join(scaler_path, "flow_scaler_output.pkl")
        joblib.dump(self.scaler_input, scaler_input_path)
        joblib.dump(self.scaler_output, scaler_output_path)
        self.scaler_input = None
        self.scaler_output = None
        LOGGER.debug(f"Scalers saved to {scaler_path}")
        with open(os.path.join(output_directory, "nflow.pkl"), "wb") as f:
            pickle.dump(self, f)
        LOGGER.info(f"Normalizing flow saved to {output_directory}")
