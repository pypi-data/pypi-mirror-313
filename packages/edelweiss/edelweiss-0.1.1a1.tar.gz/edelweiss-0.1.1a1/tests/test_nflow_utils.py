# Copyright (C) 2024 ETH Zurich
# Institute for Particle Physics and Astrophysics
# Author: Silvan Fischbacher
# created: Wed Jul 24 2024

import argparse

import numpy as np
import pytest
import yaml
from cosmic_toolbox import arraytools as at
from cosmic_toolbox import file_utils
from sklearn.preprocessing import (MaxAbsScaler, MinMaxScaler,
                                   PowerTransformer, QuantileTransformer,
                                   RobustScaler, StandardScaler)

from edelweiss.nflow_utils import (ModelNotConvergedError, check_convergence,
                                   get_scalers, prepare_columns, prepare_data)


def test_check_convergence():
    check_convergence([1, 2, 3, 4, 5], min_loss=5)

    with pytest.raises(ModelNotConvergedError, match="loss too high: 10"):
        check_convergence([10, 12, 15], min_loss=5)

    with pytest.raises(ModelNotConvergedError, match="loss is NaN"):
        check_convergence([1, 2, 3, np.nan])

    with pytest.raises(ModelNotConvergedError, match="loss is inf"):
        check_convergence([1, 2, 3, np.inf])

    with pytest.raises(ModelNotConvergedError, match="loss is -inf"):
        check_convergence([1, 2, 3, -np.inf])


def test_prepare_columns():
    args = argparse.Namespace()
    config = {
        "input_band_dep": ["feature1", "feature2"],
        "input_band_indep": ["feature3", "feature4"],
        "output": ["output1", "output2"],
    }
    with open("config.yaml", "w") as f:
        yaml.dump(config, f)
    args.config_path = "config.yaml"
    args.bands = ["band1", "band2"]

    input_cols, output_cols = prepare_columns(args, bands=["band1", "band2"])
    assert input_cols == [
        "feature1_band1",
        "feature1_band2",
        "feature2_band1",
        "feature2_band2",
        "feature3",
        "feature4",
    ]
    assert output_cols == [
        "output1_band1",
        "output1_band2",
        "output2_band1",
        "output2_band2",
    ]

    input_cols, output_cols = prepare_columns(args)
    assert input_cols == ["feature1", "feature2", "feature3", "feature4"]
    assert output_cols == ["output1", "output2"]
    file_utils.robust_remove("config.yaml")


def test_prepare_data():
    args = argparse.Namespace()
    config = {
        "input_band_dep": ["feature1", "feature2"],
        "input_band_indep": ["feature3", "feature4"],
        "output": ["output1", "flux_frac"],
    }
    with open("config.yaml", "w") as f:
        yaml.dump(config, f)
    args.config_path = "config.yaml"
    args.bands = ["band1", "band2"]

    X = {
        "band1": {
            "feature1": np.array([1, 2]),
            "feature2": np.array([3, 4]),
            "feature3": np.array([5, 6]),
            "feature4": np.array([7, 8]),
            "output1": np.array([9, 10]),
            "FLUX_APER": np.array([11, 12]),
        },
        "band2": {
            "feature1": np.array([13, 14]),
            "feature2": np.array([15, 16]),
            "feature3": np.array([17, 18]),
            "feature4": np.array([19, 20]),
            "output1": np.array([21, 22]),
            "FLUX_APER": np.array([23, 24]),
        },
    }
    X = {k: at.dict2rec(v) for (k, v) in X.items()}

    result = prepare_data(args, X)
    assert result.dtype.names == (
        "feature3",
        "feature4",
        "feature1_band1",
        "feature1_band2",
        "feature2_band1",
        "feature2_band2",
        "output1_band1",
        "output1_band2",
        "flux_frac_band1",
        "flux_frac_band2",
    )
    file_utils.robust_remove("config.yaml")


def test_get_scalers():
    scalers = {
        "robust": RobustScaler,
        "power": PowerTransformer,
        "standard": StandardScaler,
        "minmax": MinMaxScaler,
        "maxabs": MaxAbsScaler,
        "quantile": QuantileTransformer,
    }

    for scaler_name, scaler_class in scalers.items():
        scaler_input, scaler_output = get_scalers(scaler_name)
        assert isinstance(scaler_input, scaler_class)
        assert isinstance(scaler_output, scaler_class)

    with pytest.raises(ValueError, match="Scaler not_implemented not implemented yet."):
        get_scalers("not_implemented")
