# Copyright (C) 2024 ETH Zurich
# Institute for Particle Physics and Astrophysics
# Author: Silvan Fischbacher
# created: Wed Jul 24 2024


import numpy as np
import pytest
from cosmic_toolbox import arraytools as at
from cosmic_toolbox import file_utils

from edelweiss.classifier import Classifier, MultiClassifier
from edelweiss.emulator import load_emulator
from edelweiss.nflow import Nflow


@pytest.fixture
def data_clf():
    X = np.random.rand(100, 10)
    y = np.random.randint(0, 2, 100)

    yy = np.random.rand(100, 10)[y == 1]

    XX = np.hstack((X[y == 1], yy))
    X = at.arr2rec(X, ["f" + str(i) for i in range(10)])
    XX = at.arr2rec(XX, ["f" + str(i) for i in range(20)])
    return X, y, XX


@pytest.fixture
def data_clf_multi():
    X = np.random.rand(100, 10)
    y = np.random.randint(0, 2, 100)
    multiclass = np.random.randint(0, 3, 100)

    yy = np.random.rand(100, 10)[y == 1]
    X = np.hstack((X, multiclass[:, None]))
    XX = np.hstack((X[y == 1], yy))
    X = at.arr2rec(X, ["f" + str(i) for i in range(11)])
    XX = at.arr2rec(XX, ["f" + str(i) for i in range(21)])
    return X, y, XX


def test_emulator(data_clf):
    X, y, data = data_clf
    clf = Classifier()
    clf.fit(X, y)
    clf.save("test")

    nflow = Nflow(
        output=["f" + str(i) for i in range(10, 20)],
        input=["f" + str(i) for i in range(10)],
    )
    nflow.fit(data)
    nflow.save("test")

    clf, nflow = load_emulator("test", bands=None)
    clf.predict(X)
    clf.predict_proba(X)
    clf.predict_non_proba(X)
    clf.test(X, y)

    nflow.sample(data[["f" + str(i) for i in range(10)]])
    file_utils.robust_remove("test")


def test_emulator_multi(data_clf_multi):
    X, y, data = data_clf_multi
    clf = MultiClassifier(split_label="f10", labels=[0, 1, 2])
    clf.fit(X, y)
    clf.save("test")

    nflow = Nflow(
        output=["f" + str(i) for i in range(11, 21)],
        input=["f" + str(i) for i in range(11)],
    )
    nflow.fit(data)
    nflow.save("test")

    clf, nflow = load_emulator("test", bands=None, multiclassifier=True)
    clf.predict(X)
    clf.predict_proba(X)
    clf.predict_non_proba(X)
    clf.test(X, y)

    nflow.sample(data[["f" + str(i) for i in range(11)]])
    file_utils.robust_remove("test")


def test_emulator_multiband(data_clf):
    X, y, data = data_clf
    clf = Classifier()
    clf.fit(X, y)
    clf.save("test")

    bands = ["g", "r"]
    for b in bands:
        nflow = Nflow(
            output=["f" + str(i) for i in range(10, 20)],
            input=["f" + str(i) for i in range(10)],
        )
        nflow.fit(data)
        nflow.save("test", band=b)

    clf, nflow = load_emulator("test", bands=bands)
    clf.predict(X)
    clf.predict_proba(X)
    clf.predict_non_proba(X)
    clf.test(X, y)

    for b in bands:
        nflow[b].sample(data[["f" + str(i) for i in range(10)]])
    file_utils.robust_remove("test")
