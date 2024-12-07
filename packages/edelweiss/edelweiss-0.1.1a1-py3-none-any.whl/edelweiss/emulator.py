# Copyright (C) 2023 ETH Zurich
# Institute for Particle Physics and Astrophysics
# Author: Silvan Fischbacher

from cosmic_toolbox import logger

from edelweiss.classifier import load_classifier, load_multiclassifier
from edelweiss.nflow import load_nflow

LOGGER = logger.get_logger(__file__)


def load_emulator(
    path,
    bands=("g", "r", "i", "z", "y"),
    multiclassifier=False,
    subfolder_clf=None,
    subfolder_nflow=None,
):
    """
    Load an emulator from a given path. If bands is None, returns the classifier and
    normalizing flow. If bands is not None, returns the classifier and a dictionary of
    normalizing flows for each band.

    :param path: path to the folder containing the emulator
    :param bands: the bands to load (if None, assumes that there is only one nflow)
    :param multiclassifier: whether to load a multiclassifier or not
    :param subfolder_clf: subfolder of the emulator folder where the classifier is
                          stored
    :param subfolder_nflow: subfolder of the emulator folder where the normalizing flow
    is stored
    :return: the loaded classifier and normalizing flow
    """
    if multiclassifier:
        clf = load_multiclassifier(path, subfolder=subfolder_clf)
    else:
        clf = load_classifier(path, subfolder=subfolder_clf)
    if bands is not None:
        nflow = {}
        for band in bands:
            nflow[band] = load_nflow(path, band=band, subfolder=subfolder_nflow)
    else:
        nflow = load_nflow(path, subfolder=subfolder_nflow)
    return clf, nflow
