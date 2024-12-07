# Copyright (C) 2023 ETH Zurich
# Institute for Particle Physics and Astrophysics
# Author: Silvan Fischbacher

import itertools
import os

import numpy as np
import pytest
from cosmic_toolbox import arraytools as at
from cosmic_toolbox import file_utils
from sklearn.datasets import load_breast_cancer

from edelweiss.classifier import (
    Classifier,
    MultiClassClassifier,
    MultiClassifier,
    load_classifier,
    load_multiclassifier,
)


@pytest.fixture
def data_clf():
    data = load_breast_cancer()
    X, y = data.data, data.target
    X = at.arr2rec(X, data.feature_names)
    return X, y


@pytest.fixture
def data_clf_arr():
    data = load_breast_cancer()
    X, y = data.data, data.target
    return X, y


def test_classifier(data_clf, data_clf_arr):
    clfs = ["XGB", "RandomForest"]
    scalers = ["standard", "robust"]
    calibrate_options = [True, False]
    cv_options = [0, 2]

    for (i_clf, calibrate), (i_sc, cv) in itertools.product(
        enumerate(calibrate_options), enumerate(cv_options)
    ):
        args = {
            "clf": clfs[i_clf],
            "scaler": scalers[i_sc],
            "calibrate": calibrate,
            "cv": cv,
        }
        clf = Classifier(**args)
        X, y = data_clf
        clf.train(X, y)
        clf.predict(X)
        clf.predict_proba(X)
        clf.test(X, y)
        filename = os.path.join(os.path.dirname(__file__), "test_clf")
        clf.save(filename, "")
        clf = load_classifier(filename, "")
        clf.predict(X)
        clf.predict_proba(X)
        clf.predict_non_proba(X)
        file_utils.robust_remove(filename)

        clf = Classifier(**args)
        X, y = data_clf_arr
        clf.train(X, y)
        clf.predict(X)
        clf.predict_proba(X)
        clf.predict_non_proba(X)
        clf.test(X, y, non_proba=True)
        filename = os.path.join(os.path.dirname(__file__), "test_clf")
        clf.save(filename)
        clf = load_classifier(filename)
        clf.predict(X)
        clf.predict_proba(X)
        file_utils.robust_remove(filename)


def test_multiclassifier(data_clf):
    clf = MultiClassifier(split_label="split_label")
    X, y = data_clf
    X = at.add_cols(X, ["split_label"])
    X["split_label"] = np.random.randint(-1, 2, len(X))
    clf.train(X, y)
    clf.predict(X)
    clf.predict_proba(X)
    clf.predict_non_proba(X)
    clf.test(X, y)
    clf.test(X, y, non_proba=True)
    filename = os.path.join(os.path.dirname(__file__), "test_clf")
    clf.save(filename, "")
    clf = load_multiclassifier(filename, "")
    clf.predict(X)
    clf.predict_proba(X)
    clf.predict_non_proba(X)
    clf.save(filename)
    clf = load_multiclassifier(filename)
    clf.predict(X[X["split_label"] == 0])
    clf.predict_proba(X[X["split_label"] == 0])
    clf.predict_non_proba(X[X["split_label"] == 0])
    file_utils.robust_remove(filename)


def test_multiclass_classifier():
    X = np.random.rand(100, 10)
    y = np.random.randint(0, 2, 100)

    clf = MultiClassClassifier()
    clf.train(X, y)
    clf.predict(X)
    clf.predict_proba(X)
    clf.predict_non_proba(X)
    clf.test(X, y)
    clf.test(X, y, non_proba=True)
    clf.save("test_clf")
    clf = load_classifier("test_clf")
    clf.predict(X)
    clf.predict_proba(X)
    file_utils.robust_remove("test_clf")
