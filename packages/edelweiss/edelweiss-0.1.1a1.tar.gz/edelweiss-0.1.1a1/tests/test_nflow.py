# Copyright (C) 2023 ETH Zurich
# Institute for Particle Physics and Astrophysics
# Author: Silvan Fischbacher

import os

import numpy as np
import pytest
from cosmic_toolbox import arraytools as at
from cosmic_toolbox import file_utils

from edelweiss.nflow import Nflow, load_nflow


@pytest.fixture
def data_nflow():
    np.random.seed(42)

    conditional_params = np.random.randn(10000, 5)

    output_params = np.zeros((10000, 5))

    output_params[:, 0] = 2 * conditional_params[:, 0] + np.random.randn(10000) * 0.5
    output_params[:, 1] = (
        np.exp(0.5 * conditional_params[:, 1]) + np.random.randn(10000) * 0.3
    )
    output_params[:, 2] = (
        np.sin(conditional_params[:, 2]) + np.random.randn(10000) * 0.2
    )
    output_params[:, 3] = (
        np.maximum(0, conditional_params[:, 3]) + np.random.randn(10000) * 0.4
    )
    output_params[:, 4] = conditional_params[:, 4] ** 2 + np.random.randn(10000) * 0.1

    dataset = np.hstack((conditional_params, output_params))
    names = [f"param_{i}" for i in range(10)]
    input = names[:5]
    output = names[5:]
    data = at.arr2rec(dataset, names)
    return data, input, output


def test_nflow(data_nflow):
    scalers = ["quantile", "robust"]
    epochs = [10, 20]
    batch_sizes = [100, 200]
    n_samples = [1, 10]
    for scaler, epoch, batch_size, n in zip(scalers, epochs, batch_sizes, n_samples):
        data, input, output = data_nflow
        nflow = Nflow(input=input, output=output, scaler=scaler)
        nflow.train(data, epochs=epoch, batch_size=batch_size)
        sampled_data = nflow.sample(data[input], n_samples=n)
        assert len(sampled_data) == n * len(data)
        filename = os.path.join(os.path.dirname(__file__), "test_nflow")
        nflow.save(filename, "")
        nflow = load_nflow(filename, "")
        sampled_data = nflow.sample(data[input], n_samples=n)
        assert len(sampled_data) == n * len(data)
        file_utils.robust_remove(filename)


def test_nflow_input_output(data_nflow):
    nflow = Nflow(input=("param_0", "param_1"), output=("param_5", "param_6"))
    nflow.train(data_nflow[0], epochs=10, batch_size=100)
    s = nflow.sample(data_nflow[0][["param_0", "param_1"]], n_samples=1)
    assert len(s.dtype.names) == 4

    nflow = Nflow(output=("param_5", "param_6"))
    nflow.train(data_nflow[0], epochs=10, batch_size=100)
    s = nflow.sample(n_samples=1)
    assert len(s.dtype.names) == 2

    nflow = Nflow()
    nflow.train(data_nflow[0], epochs=10, batch_size=100, min_loss=10)
    s = nflow.sample(n_samples=1)
    assert len(s.dtype.names) == 10


def test_nflow_with_nans(data_nflow):
    data, input, output = data_nflow
    nflow = Nflow(input=input, output=output)
    nflow.train(data, epochs=10, batch_size=100)
    data2 = data.copy()
    data2["param_0"][5] = np.nan
    sampled_data = nflow.sample(data2[input], n_samples=1)
    assert len(sampled_data) == len(data)
