# Copyright (C) 2024 ETH Zurich
# Institute for Particle Physics and Astrophysics
# Author: Silvan Fischbacher
# created: Sat Jan 27 2024


import numpy as np
import pytest
from catboost import CatBoostRegressor
from cosmic_toolbox import arraytools as at
from sklearn.ensemble import RandomForestRegressor
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF
from sklearn.linear_model import ElasticNet, Lasso, LinearRegression, Ridge
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from edelweiss.custom_regs import NeuralNetworkRegressor
from edelweiss.reg_utils import get_regressor
from edelweiss.regressor import Regressor, load_regressor


def test_regressor_initialization():
    reg = Regressor()
    assert reg.scaler == "standard"
    assert reg.reg == "linear"
    assert reg.cv == 0
    assert reg.cv_scoring == "neg_mean_squared_error"
    assert reg.input_params is None
    assert reg.output_params is None


def test_regressor_train_and_predict():
    reg = Regressor()
    X_train = np.random.rand(100, 5)
    y_train = np.random.rand(100, 1)
    reg.train(X_train, y_train)
    X_test = np.random.rand(10, 5)
    y_pred = reg.predict(X_test)
    assert y_pred.shape == (10,)
    reg.test(X_train, y_train)


def test_regressor_recarray():
    reg = Regressor()
    X_train = np.random.rand(100, 5)
    X_train = at.arr2rec(
        X_train, names=["param_1", "param_2", "param_3", "param_4", "param_5"]
    )
    y_train = np.random.rand(100, 1)
    y_train = at.arr2rec(y_train, names=["output_1"])
    reg.train(X_train, y_train)
    X_test = np.random.rand(10, 5)
    X_test = at.arr2rec(
        X_test, names=["param_1", "param_2", "param_3", "param_4", "param_5"]
    )
    y_pred = reg.predict(X_test)
    assert y_pred.shape == (10,)
    reg.test(X_train, y_train)

    reg = Regressor()
    X_train = np.random.rand(100, 5)
    X_train = at.arr2rec(
        X_train, names=["param_1", "param_2", "param_3", "param_4", "param_5"]
    )
    y_train = np.random.rand(100, 2)
    y_train = at.arr2rec(y_train, names=["output_1", "output_2"])
    reg.train(X_train, y_train)
    X_test = np.random.rand(10, 5)
    X_test = at.arr2rec(
        X_test, names=["param_1", "param_2", "param_3", "param_4", "param_5"]
    )
    y_pred = reg.predict(X_test)
    assert y_pred.shape == (10,)
    reg.test(X_train, y_train)


def test_regressor_save_and_load(tmpdir):
    reg = Regressor()
    X_train = np.random.rand(100, 5)
    y_train = np.random.rand(100, 1)
    reg.train(X_train, y_train)
    reg.save(str(tmpdir))
    loaded_reg = load_regressor(str(tmpdir))
    X_test = np.random.rand(10, 5)
    y_pred = at.rec2arr(reg.predict(X_test))
    y_pred_loaded = at.rec2arr(loaded_reg.predict(X_test))
    assert np.allclose(y_pred, y_pred_loaded)


def test_get_regressor():
    regs = {
        "linear": LinearRegression,
        "ridge": Ridge,
        "lasso": Lasso,
        "elasticnet": ElasticNet,
        "knn": KNeighborsRegressor,
        "svr": SVR,
        "DecisionTree": DecisionTreeRegressor,
        "RandomForest": RandomForestRegressor,
        "MLP": MLPRegressor,
        "XGB": XGBRegressor,
        "CatBoost": CatBoostRegressor,
        "GaussianProcess": GaussianProcessRegressor,
        "NeuralNetwork": NeuralNetworkRegressor,
    }
    for reg_name, reg in regs.items():
        r = get_regressor(reg_name, StandardScaler())
        assert isinstance(r, Pipeline)
        assert len(r.steps) == 2
        assert r.steps[0][0] == "scaler"
        assert r.steps[1][0] == "reg"
        assert isinstance(r.steps[0][1], StandardScaler)
        assert isinstance(r.steps[1][1], reg)
    r = get_regressor("GaussianProcess", StandardScaler(), kernel=RBF())
    assert isinstance(r, Pipeline)
    assert len(r.steps) == 2
    assert r.steps[0][0] == "scaler"
    assert r.steps[1][0] == "reg"
    assert isinstance(r.steps[0][1], StandardScaler)
    assert isinstance(r.steps[1][1], GaussianProcessRegressor)
    assert isinstance(r.steps[1][1].kernel, RBF)
    with pytest.raises(ValueError):
        reg = get_regressor("unknown", StandardScaler())


def test_regressor_train_and_predict_with_flat_param():
    reg = Regressor()
    X_train = np.random.rand(100, 5)
    X_train = at.arr2rec(
        X_train, names=["param_1", "param_2", "param_3", "param_4", "param_5"]
    )
    y_train = np.random.rand(100, 1)
    y_train = at.arr2rec(y_train, names=["output_1"])
    reg.train(X_train, y_train, flat_param="param_1")
    X_test = np.random.rand(10, 5)
    X_test = at.arr2rec(
        X_test, names=["param_1", "param_2", "param_3", "param_4", "param_5"]
    )
    y_pred = reg.predict(X_test)
    assert y_pred.shape == (10,)
    reg.test(X_train, y_train)

    reg = Regressor()
    reg.train(X_train, y_train, flat_param="output_1")
    y_pred = reg.predict(X_test)
    assert y_pred.shape == (10,)
    reg.test(X_train, y_train)


def test_regressor_train_and_predict_with_cv():
    reg = Regressor(cv=3)
    X_train = np.random.rand(100, 5)
    y_train = np.random.rand(100, 1)
    reg.train(X_train, y_train)
    X_test = np.random.rand(10, 5)
    y_pred = reg.predict(X_test)
    assert y_pred.shape == (10,)
    reg.test(X_train, y_train)


def test_regressor_with_multi_dimensional_output():
    reg = Regressor()
    X_train = np.random.rand(100, 5)
    y_train = np.random.rand(100, 2)
    reg.train(X_train, y_train)
    X_test = np.random.rand(10, 5)
    y_pred = reg.predict(X_test)
    assert y_pred.shape == (10,)
    assert len(y_pred.dtype.names) == 2
    reg.test(X_train, y_train)


def test_custom_reg():
    reg = Regressor(
        reg="NeuralNetwork",
        hidden_units=(128, 64),
        learning_rate=0.01,
        epochs=20,
        batch_size=64,
        loss="mean_squared_error",
        activation="tanh",
        activation_output="linear",
    )
    X = np.random.rand(100, 5)
    y = np.random.rand(100, 1)
    reg.train(X, y)
    y_pred = reg.predict(X)
    assert y_pred.shape == (100,)
