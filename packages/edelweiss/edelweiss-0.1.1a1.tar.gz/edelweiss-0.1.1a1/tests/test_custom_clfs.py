# Copyright (C) 2024 ETH Zurich
# Institute for Particle Physics and Astrophysics
# Author: Silvan Fischbacher
# created: Wed Jul 24 2024


import numpy as np
import pytest
import tensorflow as tf
from cosmic_toolbox import arraytools as at
from cosmic_toolbox import file_utils
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split

from edelweiss.classifier import Classifier, load_classifier
from edelweiss.custom_clfs import NeuralNetworkClassifier


def test_constructor():
    clf = NeuralNetworkClassifier()
    clf.fit(np.random.rand(100, 10), np.random.randint(2, size=100))
    assert clf.hidden_units == (64, 32)
    assert clf.learning_rate == 0.001
    assert clf.epochs == 10
    assert clf.batch_size == 32
    assert clf.loss == "auto"
    assert clf.activation == "relu"
    assert clf.activation_output == "auto"

    clf = NeuralNetworkClassifier(
        hidden_units=(128, 64),
        learning_rate=0.01,
        epochs=20,
        batch_size=64,
        loss="categorical_crossentropy",
        activation="tanh",
        activation_output="softmax",
    )
    clf.fit(np.random.rand(100, 10), np.random.randint(2, size=100))
    assert clf.hidden_units == (128, 64)
    assert clf.learning_rate == 0.01
    assert clf.epochs == 20
    assert clf.batch_size == 64
    assert clf.loss == "categorical_crossentropy"
    assert clf.activation == "tanh"
    assert clf.activation_output == "softmax"


def test_build_model():
    clf = NeuralNetworkClassifier()
    clf.fit(np.random.rand(100, 10), np.random.randint(2, size=100))
    model = clf.model
    assert isinstance(model, tf.keras.Sequential)
    assert model.input_shape == (None, 10)
    assert model.output_shape == (None, 1)


def test_fit():
    clf = NeuralNetworkClassifier(epochs=5)
    X = np.random.rand(100, 10)
    y = np.random.randint(2, size=100)

    clf.fit(X, y)
    assert hasattr(clf, "model")
    assert isinstance(clf.model, tf.keras.Sequential)

    sample_weight = np.random.rand(100)
    clf.fit(X, y, sample_weight=sample_weight)
    assert hasattr(clf, "model")
    assert isinstance(clf.model, tf.keras.Sequential)


def test_early_stopping():
    clf = NeuralNetworkClassifier(epochs=50)
    X = np.random.rand(100, 10)
    y = np.random.randint(2, size=100)

    clf.fit(X, y, early_stopping_patience=1)
    assert hasattr(clf, "model")
    assert isinstance(clf.model, tf.keras.Sequential)


def test_predict():
    clf = NeuralNetworkClassifier(epochs=5)
    X = np.random.rand(100, 10)
    y = np.random.randint(2, size=100)

    clf.fit(X, y)
    predictions = clf.predict(X)
    assert len(predictions) == 100
    assert set(predictions).issubset(set(clf.classes_))


def test_predict_proba():
    clf = NeuralNetworkClassifier(epochs=5)
    X = np.random.rand(100, 10)
    y = np.random.randint(2, size=100)

    clf.fit(X, y)
    probabilities = clf.predict_proba(X)
    assert probabilities.shape == (100, 2)
    assert np.all(probabilities >= 0) and np.all(probabilities <= 1)


def test_non_binary():
    clf = NeuralNetworkClassifier(epochs=5)
    X = np.random.rand(100, 10)
    y = np.random.randint(3, size=100)

    clf.fit(X, y)
    predictions = clf.predict(X)
    assert len(predictions) == 100
    assert set(predictions).issubset(set(clf.classes_))

    probabilities = clf.predict_proba(X)
    assert probabilities.shape == (100, 3)
    assert np.all(probabilities >= 0) and np.all(probabilities <= 1)


@pytest.fixture
def get_data():
    np.random.seed(1996)
    data = load_breast_cancer()
    X = at.arr2rec(data.data, names=data["feature_names"])
    y = data.target
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )
    return X_train, X_test, y_train, y_test


def test_save_load_basic(get_data):
    X_train, X_test, y_train, y_test = get_data
    clf = Classifier(clf="NeuralNetwork", calibrate=False, cv=0, epochs=5)
    clf.fit(X_train, y_train)
    clf.test(X_test, y_test)
    clf.save("test_save_load_basic")

    clf_loaded = load_classifier("test_save_load_basic")
    clf_loaded.test_scores = None
    clf_loaded.test(X_test, y_test)

    assert np.isclose(
        clf_loaded.test_scores["auc_roc_score"],
        clf.test_scores["auc_roc_score"],
        atol=1e-4,
    )
    file_utils.robust_remove("test_save_load_basic")


def test_save_load_calibrate(get_data):
    X_train, X_test, y_train, y_test = get_data
    clf = Classifier(clf="NeuralNetwork", calibrate=True, cv=0, epochs=5)
    clf.fit(X_train, y_train)
    clf.test(X_test, y_test)
    clf.save("test_save_load_calibrate")

    clf_loaded = load_classifier("test_save_load_calibrate")
    clf_loaded.test_scores = None
    clf_loaded.test(X_test, y_test)

    assert np.isclose(
        clf_loaded.test_scores["auc_roc_score"],
        clf.test_scores["auc_roc_score"],
        atol=1e-4,
    )
    file_utils.robust_remove("test_save_load_calibrate")


def test_save_load_cv(get_data):
    X_train, X_test, y_train, y_test = get_data
    param_grid = {
        "clf__hidden_units": [(64, 32), (128, 64)],
    }
    clf = Classifier(clf="NeuralNetwork", calibrate=False, cv=2, epochs=5)
    clf.fit(X_train, y_train, param_grid)
    clf.test(X_test, y_test)
    clf.save("test_save_load_cv")

    clf_loaded = load_classifier("test_save_load_cv")
    clf_loaded.test_scores = None
    clf_loaded.test(X_test, y_test)

    assert np.isclose(
        clf_loaded.test_scores["auc_roc_score"],
        clf.test_scores["auc_roc_score"],
        atol=1e-4,
    )
    file_utils.robust_remove("test_save_load_cv")


def test_save_load_cv_calibrate(get_data):
    X_train, X_test, y_train, y_test = get_data
    param_grid = {
        "clf__hidden_units": [(64, 32), (128, 64)],
    }
    clf = Classifier(clf="NeuralNetwork", calibrate=True, cv=2, epochs=5)
    clf.fit(X_train, y_train, param_grid=param_grid)
    clf.test(X_test, y_test)
    clf.save("test_save_load_cv_calibrate")

    clf_loaded = load_classifier("test_save_load_cv_calibrate")
    clf_loaded.test_scores = None
    clf_loaded.test(X_test, y_test)

    assert np.isclose(
        clf_loaded.test_scores["auc_roc_score"],
        clf.test_scores["auc_roc_score"],
        atol=1e-4,
    )
    file_utils.robust_remove("test_save_load_cv_calibrate")
