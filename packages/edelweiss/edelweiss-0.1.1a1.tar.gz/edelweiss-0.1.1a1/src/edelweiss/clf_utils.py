# Copyright (C) 2022 ETH Zurich
# Institute for Particle Physics and Astrophysics
# Author: Silvan Fischbacher

import numpy as np
from catboost import CatBoostClassifier
from cosmic_toolbox.logger import get_logger
from lightgbm import LGBMClassifier
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.ensemble import (AdaBoostClassifier, GradientBoostingClassifier,
                              RandomForestClassifier)
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import make_scorer, roc_auc_score
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import (MaxAbsScaler, MinMaxScaler,
                                   QuantileTransformer, RobustScaler,
                                   StandardScaler)
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier

LOGGER = get_logger(__file__)


def get_clf_name(index=None):
    """
    Returns the name of the classifier file.

    :param index: index of the classifier
    :return: name of the classifier file
    """
    if index is None:
        return None
    return f"clf_cv/clf_{index}"


def get_classifier(classifier, scaler=None, **kwargs):
    """
    Returns the classifier object

    :param classifier: name of the classifier
    :param scaler: scaler object
    :param kwargs: additional arguments for the classifier
    :return: classifier object (sklearn pipeline)
    :raises: ValueError if classifier is not known
    """
    if scaler is None:
        scaler = RobustScaler()
    if classifier == "RandomForest":
        clf = RandomForestClassifier(**kwargs)
    elif classifier == "XGB":
        clf = XGBClassifier(**kwargs)
    elif classifier == "MLP":
        clf = MLPClassifier(**kwargs)
    elif classifier == "LogisticRegression":
        clf = LogisticRegression(**kwargs)
    elif classifier == "LinearSVC":
        clf = LinearSVC(**kwargs)
    elif classifier == "DecisionTree":
        clf = DecisionTreeClassifier(**kwargs)
    elif classifier == "AdaBoost":
        clf = AdaBoostClassifier(**kwargs)
    elif classifier == "KNN":
        clf = KNeighborsClassifier(**kwargs)
    elif classifier == "QDA":
        clf = QuadraticDiscriminantAnalysis(**kwargs)
    elif classifier == "GaussianNB":
        clf = GaussianNB(**kwargs)
    elif classifier == "NeuralNetwork":
        # Import here to avoid tensorflow warnings when not using the classifier
        from .custom_clfs import NeuralNetworkClassifier

        clf = NeuralNetworkClassifier(**kwargs)
    elif classifier == "GradientBoosting":
        clf = GradientBoostingClassifier(**kwargs)
    elif classifier == "CatBoost":
        clf = CatBoostClassifier(**kwargs)
    elif classifier == "LightGBM":
        clf = LGBMClassifier(**kwargs)
    else:
        raise ValueError(f"{classifier} not known")
    return Pipeline([("scaler", scaler), ("clf", clf)])


def get_scaler(scaler):
    """
    Returns the scaler object

    :param scaler: name of the scaler
    :return: scaler object
    :raises: ValueError if scaler is not known
    """

    if scaler == "standard":
        return StandardScaler()
    elif scaler == "minmax":
        return MinMaxScaler()
    elif scaler == "maxabs":
        return MaxAbsScaler()
    elif scaler == "robust":
        return RobustScaler()
    elif scaler == "quantile":
        return QuantileTransformer()
    else:
        raise ValueError(f"{scaler} not known")


def get_detection_label(clf, bands, n_detected_bands=None):
    """
    Get the detection label for the classifier.

    :param clf: classification data (rec array)
    :param bands: which bands the data has
    :param n_detected_bands: how many bands have to be detected such that the event is
    classified as detected, if None, the detection label is already given in clf
    :return: detection label (bool array) and the names of the detection labels
    """
    det_labels = []

    if n_detected_bands is None:
        y = clf["detected"]
        det_labels.append("detected")
        return y, det_labels

    y = np.zeros(len(clf))
    for band in bands:
        y += clf[f"detected_{band}"]
        det_labels.append(f"detected_{band}")
    return y >= n_detected_bands, det_labels


def get_scorer(score, **kwargs):
    """
    Returns the scorer object given input string.
    If not one of the known self defined scorers, returns the input string assuming
    it is a sklearn scorer.

    :param score: name of the scorer
    :kwargs: additional arguments for the scorer
    :return: scorer object
    """
    if score == "ngal":
        return make_scorer(ngal_scorer, greater_is_better=False)
    elif score == "roc_auc":
        return make_scorer(custom_roc_auc_score, needs_proba=True)
    else:
        return score


def load_hyperparams(clf):
    """
    Loads the hyperparameters for the classifier for the CV search.

    :param clf: classifier object
    :return: hyperparameter grid
    """

    if isinstance(clf, (LogisticRegression, LinearSVC)):
        param_grid = {"clf__C": [0.1, 1, 10, 100]}

    elif isinstance(clf, KNeighborsClassifier):
        param_grid = {
            "clf__n_neighbors": [5, 10, 100, 250, 500, 750],
            "clf__weights": ["uniform", "distance"],
        }
    elif isinstance(clf, DecisionTreeClassifier):
        param_grid = {
            "clf__max_depth": [3, 5, 7, 9, 11],
            "clf__min_samples_split": [2, 4, 6, 8, 10],
        }
    elif isinstance(clf, RandomForestClassifier):
        param_grid = {
            "clf__n_estimators": [20, 50, 100],
            "clf__max_depth": [None, 10, 20, 30],
            "clf__min_samples_split": [4, 6, 8, 10, 12],
        }
    elif isinstance(clf, XGBClassifier):
        param_grid = {
            "clf__learning_rate": [0.01, 0.1, 0.5, 1],
            "clf__max_depth": [3, 5, 7, 9],
            "clf__n_estimators": [5, 10, 50, 100],
        }
    elif isinstance(clf, MLPClassifier):
        param_grid = {
            "clf__hidden_layer_sizes": [
                (10,),
                (100,),
                (250,),
                (500,),
                (750,),
            ],
            "clf__alpha": [0.001, 0.01, 0.1],
        }
    elif isinstance(clf, AdaBoostClassifier):
        param_grid = {
            "clf__n_estimators": [1000, 5000],
            "clf__learning_rate": [0.01, 0.1],
        }
    elif isinstance(clf, QuadraticDiscriminantAnalysis):
        param_grid = {"clf__reg_param": [0.0, 0.01, 0.1, 1, 10]}
    elif isinstance(clf, GaussianNB):
        param_grid = {}
    elif isinstance(clf, GradientBoostingClassifier):
        param_grid = {
            "clf__n_estimators": [100, 500],
            "clf__learning_rate": [0.01, 0.1],
            "clf__max_depth": [3, 5, 7],
        }
    elif isinstance(clf, CatBoostClassifier):
        param_grid = {
            "clf__learning_rate": [0.03, 0.06],
            "clf__depth": [3, 6, 9],
            "clf__l2_leaf_reg": [2, 3, 4],
            "clf__boosting_type": ["Ordered", "Plain"],
        }
    elif isinstance(clf, LGBMClassifier):
        param_grid = {
            "clf__num_leaves": [5, 20, 31],
            "clf__learning_rate": [0.05, 0.1, 0.2],
            "clf__n_estimators": [50, 100, 150],
        }
    else:
        from .custom_clfs import NeuralNetworkClassifier

        if isinstance(clf, NeuralNetworkClassifier):
            param_grid = {
                "clf__hidden_units": [(32, 64, 32), (512, 512, 512), (10, 10)],
                "clf__learning_rate": [0.0001, 0.001],
                "clf__epochs": [1000],
                "clf__batch_size": [10000],
            }
        else:
            LOGGER.warning(f"Classifier {clf} not known.")
            param_grid = {}

    return param_grid


def ngal_scorer(y_true, y_pred):
    """
    Scorer accounting for the number of galaxies in the sample.
    score = (N_pred - N_true)**2

    :param y_true: true labels (detected or not)
    :param y_pred: predicted labels (detected or not)
    :return: score
    """
    return (sum(y_pred) - sum(y_true)) ** 2


def custom_roc_auc_score(y_true, y_prob):
    """
    Scorer for the ROC AUC score using y_prob

    :param y_true: true labels (detected or not)
    :param y_prob: predicted probabilities (2D array)
    :return: score
    """
    return roc_auc_score(y_true, y_prob[:, 1])


def ngal_hist_scorer(y_true, y_pred, mag, bins=100, range=(15, 30)):
    """
    Scorer accounting for the number of galaxies in the sample on a histogram level.
    score = (N_pred - N_true)**2

    :param y_true: true labels (detected or not)
    :param y_pred: predicted labels (detected or not)
    :param mag: magnitude of the galaxies
    :return: score
    """
    hist_true = np.histogram(mag[y_true], bins=bins, range=range)[0]
    hist_pred = np.histogram(mag[y_pred], bins=bins, range=range)[0]
    return (hist_pred - hist_true) ** 2


def get_classifier_args(clf, conf):
    """
    Returns the arguments for the classifier defined in the config file

    :param clf: classifier name
    :param conf: config file
    :return: arguments for the classifier
    """
    try:
        return conf["classifier_args"][clf]
    except KeyError:
        LOGGER.warning(f"Classifier {clf} not found in config file.")
        return {}
