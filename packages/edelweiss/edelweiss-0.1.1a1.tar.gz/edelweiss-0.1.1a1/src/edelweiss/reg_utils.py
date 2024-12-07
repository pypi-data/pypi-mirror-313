# Copyright (C) 2024 ETH Zurich
# Institute for Particle Physics and Astrophysics
# Author: Silvan Fischbacher
# created: Sat Jan 27 2024


from catboost import CatBoostRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF
from sklearn.linear_model import ElasticNet, Lasso, LinearRegression, Ridge
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import Pipeline
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor


def get_regressor(regressor, scaler, **kwargs):
    """
    Returns the regressor object

    :param regressor: name of the regressor
    :param scaler: scaler object
    :param kwargs: additional arguments for the regressor
    :return: regressor object (sklearn pipeline)
    :raises: ValueError if regressor is not known
    """
    if regressor == "linear":
        reg = LinearRegression(**kwargs)
    elif regressor == "ridge":
        reg = Ridge(**kwargs)
    elif regressor == "lasso":
        reg = Lasso(**kwargs)
    elif regressor == "elasticnet":
        reg = ElasticNet(**kwargs)
    elif regressor == "knn":
        reg = KNeighborsRegressor(**kwargs)
    elif regressor == "svr":
        reg = SVR(**kwargs)
    elif regressor == "RandomForest":
        reg = RandomForestRegressor(**kwargs)
    elif regressor == "XGB":
        reg = XGBRegressor(**kwargs)
    elif regressor == "CatBoost":
        reg = CatBoostRegressor(**kwargs)
    elif regressor == "MLP":
        reg = MLPRegressor(**kwargs)
    elif regressor == "DecisionTree":
        reg = DecisionTreeRegressor(**kwargs)
    elif regressor == "NeuralNetwork":
        from .custom_regs import NeuralNetworkRegressor

        reg = NeuralNetworkRegressor(**kwargs)
    elif regressor == "GaussianProcess":
        if "kernel" not in kwargs:
            kernel = RBF()
            reg = GaussianProcessRegressor(kernel=kernel, **kwargs)
        else:
            reg = GaussianProcessRegressor(**kwargs)
    else:
        raise ValueError(f"{regressor} not known")
    return Pipeline([("scaler", scaler), ("reg", reg)])
