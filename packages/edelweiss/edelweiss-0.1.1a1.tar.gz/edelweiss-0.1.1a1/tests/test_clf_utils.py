# Copyright (C) 2024 ETH Zurich
# Institute for Particle Physics and Astrophysics
# Author: Silvan Fischbacher
# created: Wed Jul 24 2024

import numpy as np
import pytest
from catboost import CatBoostClassifier
from lightgbm import LGBMClassifier
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier,
)
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import (
    MaxAbsScaler,
    MinMaxScaler,
    QuantileTransformer,
    RobustScaler,
    StandardScaler,
)
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier

from edelweiss.clf_utils import (
    custom_roc_auc_score,
    get_classifier,
    get_classifier_args,
    get_clf_name,
    get_detection_label,
    get_scaler,
    get_scorer,
    load_hyperparams,
    ngal_hist_scorer,
    ngal_scorer,
)
from edelweiss.custom_clfs import NeuralNetworkClassifier


def test_get_clf_name():
    assert get_clf_name() is None
    assert get_clf_name(1) == "clf_cv/clf_1"


def test_get_classifier():
    classifiers = {
        "RandomForest": RandomForestClassifier,
        "XGB": XGBClassifier,
        "MLP": MLPClassifier,
        "LogisticRegression": LogisticRegression,
        "LinearSVC": LinearSVC,
        "DecisionTree": DecisionTreeClassifier,
        "AdaBoost": AdaBoostClassifier,
        "KNN": KNeighborsClassifier,
        "QDA": QuadraticDiscriminantAnalysis,
        "GaussianNB": GaussianNB,
        "GradientBoosting": GradientBoostingClassifier,
        "CatBoost": CatBoostClassifier,
        "LightGBM": LGBMClassifier,
        "NeuralNetwork": NeuralNetworkClassifier,
    }

    for name, clf_class in classifiers.items():
        clf = get_classifier(name)
        assert isinstance(clf, Pipeline)
        assert isinstance(clf.steps[1][1], clf_class)

    with pytest.raises(ValueError, match="unknown_classifier not known"):
        get_classifier("unknown_classifier")


def test_get_scaler():
    scalers = {
        "standard": StandardScaler,
        "minmax": MinMaxScaler,
        "maxabs": MaxAbsScaler,
        "robust": RobustScaler,
        "quantile": QuantileTransformer,
    }

    for name, scaler_class in scalers.items():
        scaler = get_scaler(name)
        assert isinstance(scaler, scaler_class)

    with pytest.raises(ValueError, match="unknown_scaler not known"):
        get_scaler("unknown_scaler")


def test_get_detection_label():
    clf_data = np.zeros(
        10,
        dtype=[
            ("detected", "bool"),
            ("detected_band1", "bool"),
            ("detected_band2", "bool"),
        ],
    )
    clf_data["detected"] = [
        True,
        False,
        True,
        False,
        True,
        False,
        True,
        False,
        True,
        False,
    ]
    clf_data["detected_band1"] = [
        True,
        False,
        True,
        False,
        True,
        False,
        True,
        False,
        True,
        False,
    ]
    clf_data["detected_band2"] = [
        False,
        True,
        False,
        True,
        False,
        True,
        False,
        True,
        False,
        True,
    ]

    y, det_labels = get_detection_label(clf_data, bands=["band1", "band2"])
    assert np.array_equal(y, clf_data["detected"])
    assert det_labels == ["detected"]

    y, det_labels = get_detection_label(
        clf_data, bands=["band1", "band2"], n_detected_bands=1
    )
    assert np.array_equal(y, np.ones(10, dtype=bool))
    assert det_labels == ["detected_band1", "detected_band2"]


def test_get_scorer():
    scorer = get_scorer("ngal")
    assert scorer._score_func == ngal_scorer

    scorer = get_scorer("roc_auc")
    assert scorer._score_func == custom_roc_auc_score

    assert get_scorer("accuracy") == "accuracy"


def test_load_hyperparams():
    class UnknownClassifier:
        pass

    classifiers = [
        LogisticRegression(),
        LinearSVC(),
        KNeighborsClassifier(),
        DecisionTreeClassifier(),
        RandomForestClassifier(),
        XGBClassifier(),
        MLPClassifier(),
        AdaBoostClassifier(),
        QuadraticDiscriminantAnalysis(),
        GaussianNB(),
        GradientBoostingClassifier(),
        CatBoostClassifier(),
        LGBMClassifier(),
        NeuralNetworkClassifier(),
        UnknownClassifier(),
    ]

    for clf in classifiers:
        params = load_hyperparams(clf)
        assert isinstance(params, dict)


def test_ngal_scorer():
    y_true = np.array([0, 1, 0, 1, 0, 1])
    y_pred = np.array([0, 1, 1, 0, 1, 0])
    score = ngal_scorer(y_true, y_pred)
    assert score == 0


def test_custom_roc_auc_score():
    y_true = np.array([0, 1, 0, 1, 0, 1])
    y_prob = np.array(
        [[0.9, 0.1], [0.2, 0.8], [0.6, 0.4], [0.4, 0.6], [0.1, 0.9], [0.8, 0.2]]
    )
    score = custom_roc_auc_score(y_true, y_prob)
    assert 0 <= score <= 1


def test_ngal_hist_scorer():
    y_true = np.array([0, 1, 0, 1, 0, 1], dtype=bool)
    y_pred = np.array([0, 1, 1, 0, 1, 0], dtype=bool)
    mag = np.array([20, 21, 22, 23, 24, 25])
    score = ngal_hist_scorer(y_true, y_pred, mag)
    assert isinstance(score, np.ndarray)


def test_get_classifier_args():
    conf = {"classifier_args": {"RandomForest": {"n_estimators": 100}, "SVC": {"C": 1}}}
    args = get_classifier_args("RandomForest", conf)
    assert args == {"n_estimators": 100}

    args = get_classifier_args("unknown_classifier", conf)
    assert args == {}
