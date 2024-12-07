# Copyright (C) 2023 ETH Zurich
# Institute for Particle Physics and Astrophysics
# Author: Silvan Fischbacher

import numpy as np
from cosmic_toolbox import arraytools as at
from cosmic_toolbox import file_utils
from cosmic_toolbox.logger import get_logger
from sklearn.preprocessing import (MaxAbsScaler, MinMaxScaler,
                                   PowerTransformer, QuantileTransformer,
                                   RobustScaler, StandardScaler)

LOGGER = get_logger(__file__)


class ModelNotConvergedError(Exception):
    """
    Custom error class for when a has not converged.
    """

    def __init__(self, model_name, reason=None):
        """
        Initialize the custom error.

        :param model_name: name of the model that did not converge
        :param reason: reason why the model did not converge
        """
        message = f"The {model_name} model did not converge."
        if reason is not None:
            message += f" Reason: {reason}"
        super().__init__(message)


def check_convergence(losses, min_loss=5):
    """
    Check if the model has converged.

    :param losses: list of losses
    :param min_loss: minimum loss, if the loss is higher than this,
    the model has not converged
    :raises ModelNotConvergedError: if the model has not converged
    """

    if np.nanmin(losses) > min_loss:
        raise ModelNotConvergedError(
            "normalizing flow", reason=f"loss too high: {np.nanmin(losses)}"
        )
    if np.isnan(losses[-1]):
        raise ModelNotConvergedError("normalizing flow", reason="loss is NaN")
    if losses[-1] == np.inf:
        raise ModelNotConvergedError("normalizing flow", reason="loss is inf")
    if losses[-1] == -np.inf:
        raise ModelNotConvergedError("normalizing flow", reason="loss is -inf")


def prepare_columns(args, bands=None):
    """
    Prepare the columns for the training of the normalizing flow.

    :param args: arparse arguments
    :param bands: list of bands to use, if None, no bands are used
    :return: input and output columns
    """

    conf = file_utils.read_yaml(args.config_path)
    input = []
    output = []
    for par in conf["input_band_dep"]:
        if bands is not None:
            for band in bands:
                input.append(f"{par}_{band}")
        else:
            input.append(par)

    for par in conf["input_band_indep"]:
        input.append(par)

    for par in conf["output"]:
        if bands is not None:
            for band in bands:
                output.append(f"{par}_{band}")
        else:
            output.append(par)
    return input, output


def prepare_data(args, X):
    """
    Prepare the data for the training of the normalizing flow by combining the different
    bands to one array.

    :param args: argparse arguments
    :param X: dictionary with the data (keys are the bands)
    :return: rec array with the data
    """
    try:
        from legacy_abc.analysis.mmd_scalings.mmd_scalings_utils import \
            add_fluxfrac_col
    except Exception:
        LOGGER.warning(
            "Could not import add_fluxfrac_col from legacy_abc."
            " Check if the function used here is correct."
        )

        def add_fluxfrac_col(catalogs, list_bands):
            list_flux = []
            for band in list_bands:
                list_flux.append(catalogs[band]["FLUX_APER"])
            flux_total = np.array(list_flux).sum(axis=0)

            for band in list_bands:
                if "flux_frac" not in catalogs[band].dtype.names:
                    catalogs[band] = at.add_cols(catalogs[band], names=["flux_frac"])
                catalogs[band]["flux_frac"] = catalogs[band]["FLUX_APER"] / flux_total

    conf = file_utils.read_yaml(args.config_path)

    if "flux_frac" in conf["output"]:
        add_fluxfrac_col(X, args.bands)
    data = {}
    for par in conf["input_band_indep"]:
        data[par] = X[list(X.keys())[0]][par]
    for par in conf["input_band_dep"]:
        for band in args.bands:
            data[f"{par}_{band}"] = X[band][par]
    for par in conf["output"]:
        for band in args.bands:
            data[f"{par}_{band}"] = X[band][par]
    return at.dict2rec(data)


def get_scalers(scaler):
    """
    Get the scalers from the name.

    :param scaler: name of the scaler (str)
    :return: scaler
    :raises ValueError: if the scaler is not implemented
    """

    if scaler == "robust":
        return RobustScaler(), RobustScaler()
    elif scaler == "power":
        return PowerTransformer(), PowerTransformer()
    elif scaler == "standard":
        return StandardScaler(), StandardScaler()
    elif scaler == "minmax":
        return MinMaxScaler(), MinMaxScaler()
    elif scaler == "maxabs":
        return MaxAbsScaler(), MaxAbsScaler()
    elif scaler == "quantile":
        return QuantileTransformer(), QuantileTransformer()
    else:
        raise ValueError(f"Scaler {scaler} not implemented yet.")
