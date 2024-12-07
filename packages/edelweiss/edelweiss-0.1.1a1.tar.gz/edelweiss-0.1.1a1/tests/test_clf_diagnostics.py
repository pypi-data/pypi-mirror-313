# Copyright (C) 2024 ETH Zurich
# Institute for Particle Physics and Astrophysics
# Author: Silvan Fischbacher
# created: Tue Jul 23 2024


import numpy as np
import pytest
from cosmic_toolbox import arraytools as at
from cosmic_toolbox import file_utils
from sklearn.datasets import load_breast_cancer

from edelweiss import clf_diagnostics, clf_utils
from edelweiss.classifier import Classifier


@pytest.fixture
def data_clf():
    data = load_breast_cancer()
    X, y = data.data, data.target
    X = at.arr2rec(X, data.feature_names)
    return X, y


def test_diagnostics(data_clf):
    X, y = data_clf
    clf = Classifier()
    clf.fit(X, y)
    clf_diagnostics.plot_diagnostics(clf, X, y, special_param=clf.params[0])
    path = "test/"
    clf_diagnostics.plot_diagnostics(
        clf, X, y, output_directory=path, special_param=clf.params[0], save_plot=True
    )
    file_utils.robust_remove(path)


def test_feature_importances(data_clf):
    X, y = data_clf
    clf = Classifier()
    clf.fit(X, y)
    clf_diagnostics.plot_feature_importances(clf)
    clf_diagnostics.plot_feature_importances(clf, summed=True)

    X, y = data_clf
    clf = Classifier(clf="MLP")
    clf.fit(X, y)
    clf_diagnostics.plot_feature_importances(clf)
    clf_diagnostics.plot_feature_importances(clf, summed=True)


def test_scores(data_clf):
    X, y = data_clf
    clf = Classifier()
    clf.fit(X, y)
    clf.test(X, y)
    clf_diagnostics.plot_all_scores(clf.test_scores)

    clf.save("test")
    np.save("test/clf/test_scores.npy", clf.test_scores)
    clf_diagnostics.plot_all_scores("test")

    clf_diagnostics.plot_all_scores(["test"], path_labels=["test"])
    file_utils.robust_remove("test/")


def test_spider_scores(data_clf):
    X, y = data_clf
    clf = Classifier()
    clf.fit(X, y)
    clf.test(X, y)
    y_pred = clf.predict(X)
    y_prob = clf.predict_proba(X)
    output_directory = "test/"
    clf.save(output_directory)
    fig = clf_diagnostics.plot_spider_scores(
        y, y_pred, y_prob, output_directory=output_directory, save_plot=True
    )
    clf_diagnostics.plot_spider_scores(
        y, y_pred, y_prob, output_directory=output_directory, fig=fig, print_scores=True
    )
    file_utils.robust_remove(output_directory)


def test_classifier_comparison(data_clf):
    conf = dict(classifier=["XGB", "MLP"], scaler=["standard", "minmax"])
    clfs = ["XGB_standard", "XGB_minmax", "MLP_standard", "MLP_minmax"]
    special_param = data_clf[0].dtype.names[0]
    n_clfs = len(conf["classifier"])
    n_scalers = len(conf["scaler"])
    for index in range(n_clfs * n_scalers):
        i_clf, i_scaler = np.unravel_index(index, (n_clfs, n_scalers))
        clf = Classifier(clf=conf["classifier"][i_clf], scaler=conf["scaler"][i_scaler])
        clf.fit(*data_clf)
        clf.save("test/", subfolder=clf_utils.get_clf_name(index))
        np.save(f"test/clf_cv/clf_test_data{index}.npy", data_clf[0])
        np.save(f"test/clf_cv/clf_test_labels{index}.npy", data_clf[1])
    clf_diagnostics.plot_classifier_comparison(
        clfs, conf, "test/", special_param=special_param
    )
    clf_diagnostics.plot_classifier_comparison(
        clfs, conf, ["test"] * 4, special_param=special_param, labels=["test"] * 4
    )
    clf_diagnostics.plot_classifier_comparison(
        clfs, conf, ["test"] * 4, special_param=special_param
    )
    file_utils.robust_remove("test/")


def test_scale_empty_spider_data():
    data = dict(feature1=[0, 1, 2], feature2=[0, 1, 2])
    data = at.dict2rec(data)
    data = clf_diagnostics.scale_data_for_spider(data)
    data = at.rec2arr(data)
    assert np.all(data >= 0)
    assert np.all(data <= 1)


def test_get_name(data_clf):
    X, y = data_clf

    assert clf_diagnostics.get_name("XGB") == "XGB"

    clf = Classifier(clf="XGB", calibrate=False)
    clf.fit(X, y)
    assert clf_diagnostics.get_name(clf) == "Standar_XGBClas_"
    assert clf_diagnostics.get_name(clf, final=True) == "final"

    clf = Classifier(clf="XGB", calibrate=True)
    clf.fit(X, y)
    assert clf_diagnostics.get_name(clf) == "Calibra_Standar_XGBClas_"

    clf = Classifier(clf="XGB", cv=2, calibrate=True, grid_search=True)
    clf.fit(X, y)
    assert clf_diagnostics.get_name(clf) == "Calibra_Standar_XGBClas_"

    clf = Classifier(clf="XGB", cv=2, calibrate=False, grid_search=True)
    clf.fit(X, y)
    assert clf_diagnostics.get_name(clf) == "Standar_XGBClas_"
