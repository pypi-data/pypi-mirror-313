# Copyright (C) 2023 ETH Zurich
# Institute for Particle Physics and Astrophysics
# Author: Silvan Fischbacher

import os
import pickle

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from cosmic_toolbox import arraytools as at
from cosmic_toolbox import colors, file_utils
from cosmic_toolbox.logger import get_logger
from sklearn.calibration import CalibratedClassifierCV, calibration_curve
from sklearn.metrics import (accuracy_score, average_precision_score,
                             brier_score_loss, f1_score, log_loss,
                             precision_recall_curve, precision_score,
                             recall_score, roc_auc_score, roc_curve)
from sklearn.model_selection import GridSearchCV

from edelweiss import clf_utils as utils

LOGGER = get_logger(__file__)
COL = colors.get_colors()
colors.set_cycle()


def get_confusion_matrix(y_true, y_pred):
    """
    Get the confusion matrix for the classifier.

    :param y_true: true labels
    :param y_pred: predicted labels
    :return: True Positives, True Negatives, False Positives, False Negatives
    """

    tp = y_pred & y_true
    tn = ~y_pred & ~y_true
    fp = y_pred & ~y_true
    fn = ~y_pred & y_true
    return tp, tn, fp, fn


def plot_hist_fp_fn_tp_tn(
    param,
    y_true,
    y_pred,
    output_directory=".",
    clf="classifier",
    final=False,
    save_plot=False,
):
    """
    Plot the stacked histogram of one parameter (e.g. i-band magnitude) for the
    different confusion matrix elements.

    :param param: parameter to plot
    :param y_true: true labels
    :param y_pred: predicted labels
    :param output_directory: directory to save the plot
    :param clf: classifier object or name of the classifier
    :param final: if True, the plot is for the final classifier
    :param save_plot: if True, save the plot
    """
    # TODO: something strange happens in the plotting.
    tp, tn, fp, fn = get_confusion_matrix(y_true, y_pred)
    fig = plt.figure()
    plt.hist(
        [param[fp], param[fn], param[tp], param[tn]],
        bins=100,
        stacked=True,
        label=["FP", "FN", "TP", "TN"],
        color=[COL["r"], COL["orange"], COL["g"], COL["b"]],
        density=True,
    )
    plt.ylim(0, 0.2)
    plt.legend()
    plt.xlabel("i-band magnitude")
    plt.ylabel("Normalized counts (stacked)")
    name = get_name(clf, final=final)
    path = os.path.join(output_directory, "clf/figures/")
    file_utils.robust_makedirs(path)
    path += f"stacked_hist_{name}"
    if save_plot:
        plt.savefig(path + ".pdf", bbox_inches="tight")
        with open(path + ".pkl", "wb") as fh:
            pickle.dump(fig, fh)


def plot_hist_n_gal(
    param,
    y_true,
    y_pred,
    output_directory=".",
    clf="classifier",
    final=False,
    save_plot=False,
    fig=None,
):
    """
    Plot the histogram of detected galaxies for the classifer and the true detected
    galaxies for one parameter (e.g. i-band magnitude).

    :param param: parameter to plot
    :param y_true: true labels
    :param y_pred: predicted labels
    :param output_directory: directory to save the plot
    :param clf: classifier object or name of the classifier
    :param final: if True, the plot is for the final classifier
    :param save_plot: if True, save the plot
    :param fig: figure object, if None, create a new figure
    """
    # TODO: something strange happens in the plotting.
    _, bins = np.histogram(param[y_true], bins=100)

    if fig is None:
        fig, ax = plt.subplots()
        ax.set_xlabel("i-band magnitude")
        ax.set_ylabel("galaxy counts")
        ax.set_title("Number of detected galaxies")
        ax.hist(param[y_true], bins=bins, label="true detected galaxies", color="grey")
    else:
        ax = fig.get_axes()[0]
    name = get_name(clf, final=False)
    ax.hist(param[y_pred], bins=bins, histtype="step", label=name)
    ax.legend()
    name = get_name(clf, final=final)
    path = os.path.join(output_directory, "clf/figures/")
    file_utils.robust_makedirs(path)
    path += f"stacked_hist_{name}"
    if save_plot:
        plt.savefig(path + ".pdf", bbox_inches="tight")
        with open(path + ".pkl", "wb") as fh:
            pickle.dump(fig, fh)
    return fig


def plot_calibration_curve(
    y_true,
    y_prob,
    output_directory=".",
    clf="classifier",
    final=False,
    save_plot=False,
    fig=None,
):
    """
    Plot the calibration curve for the classifier.

    :param y_true: true labels
    :param y_prob: predicted probabilities
    :param output_directory: directory to save the plot
    :param clf: classifier object or name of the classifier
    :param final: if True, the plot is for the final classifier
    :param save_plot: if True, save the plot
    :param fig: figure object, if None, create a new figure
    """
    if fig is None:
        fig, ax = plt.subplots()
        ax.plot([0, 1], [0, 1], ls="--", color="k", label="perfect calibration")
        ax.set_xlabel("predicted probability")
        ax.set_ylabel("fraction of positives")
        ax.set_title("Calibration curve")
    else:
        ax = fig.get_axes()[0]

    prob_true, prob_pred = calibration_curve(y_true, y_prob, n_bins=20)
    name = get_name(clf, final=False)
    ax.plot(prob_pred, prob_true, label=name)
    ax.legend()
    name = get_name(clf, final=final)
    path = os.path.join(output_directory, "clf/figures/")
    file_utils.robust_makedirs(path)
    path += f"stacked_hist_{name}"
    if save_plot:
        plt.savefig(path + ".pdf", bbox_inches="tight")
        with open(path + ".pkl", "wb") as fh:
            pickle.dump(fig, fh)
    return fig


def plot_roc_curve(
    y_true,
    y_prob,
    output_directory=".",
    clf="classifier",
    final=False,
    save_plot=False,
    fig=None,
):
    """
    Plot the ROC curve for the classifier.

    :param y_true: true labels
    :param y_prob: predicted probabilities
    :param output_directory: directory to save the plot
    :param clf: classifier object or name of the classifier
    :param final: if True, the plot is for the final classifier
    :param save_plot: if True, save the plot
    :param fig: figure object, if None, create a new figure
    """
    fpr, tpr, _ = roc_curve(y_true, y_prob)

    if fig is None:
        fig, ax = plt.subplots()
        ax.set_xlabel("false positive rate")
        ax.set_ylabel("true positive rate")
        ax.set_title("ROC curve")
        ax.plot([0, 1], [0, 1], ls="--", color="k", label="random classifier")
        ax.plot([0, 0, 1], [0, 1, 1], ls=":", color="k", label="perfect classifier")
    else:
        ax = fig.get_axes()[0]
    ax.plot(fpr, tpr, label=get_name(clf, final=False))
    ax.legend()
    name = get_name(clf, final=final)
    path = os.path.join(output_directory, "clf/figures/")
    file_utils.robust_makedirs(path)
    path += f"stacked_hist_{name}"
    if save_plot:
        plt.savefig(path + ".pdf", bbox_inches="tight")
        with open(path + ".pkl", "wb") as fh:
            pickle.dump(fig, fh)
    return fig


def plot_pr_curve(
    y_true,
    y_prob,
    output_directory=".",
    clf="classifier",
    final=False,
    save_plot=False,
    fig=None,
):
    """
    Plot the precision-recall curve for the classifier.

    :param y_true: true labels
    :param y_prob: predicted probabilities
    :param output_directory: directory to save the plot
    :param clf: classifier object or name of the classifier
    :param final: if True, the plot is for the final classifier
    :param save_plot: if True, save the plot
    :param fig: figure object, if None, create a new figure
    :return: figure object
    """

    precision, recall, _ = precision_recall_curve(y_true, y_prob)

    if fig is None:
        fig, ax = plt.subplots()
        ax.plot([0, 1, 1], [1, 1, 0], ls=":", color="k", label="perfect classifier")
        ax.set_xlabel("recall")
        ax.set_ylabel("precision")
        ax.set_title("Precision-Recall curve")
    else:
        ax = fig.get_axes()[0]
    ax.plot(recall, precision, label=get_name(clf, final=False))
    ax.legend()
    name = get_name(clf, final=final)
    path = os.path.join(output_directory, "clf/figures/")
    file_utils.robust_makedirs(path)
    path += f"stacked_hist_{name}"
    if save_plot:
        fig.savefig(path + ".pdf", bbox_inches="tight")
        with open(path + ".pkl", "wb") as fh:
            pickle.dump(fig, fh)
    return fig


def plot_spider_scores(
    y_true,
    y_pred,
    y_prob,
    output_directory=".",
    clf="classifier",
    final=False,
    save_plot=False,
    fig=None,
    ranges=None,
    print_scores=False,
):
    """
    Plot the spider scores for the classifier.

    :param y_true: true labels
    :param y_pred: predicted labels
    :param y_prob: predicted probabilities
    :param output_directory: directory to save the plot
    :param clf: classifier object or name of the classifier
    :param final: if True, the plot is for the final classifier
    :param save_plot: if True, save the plot
    :param fig: figure object, if None, create a new figure
    :param ranges: dictionary of ranges for each score
    :param print_scores: if True, print the scores
    :return: figure object
    """
    ranges = {} if ranges is None else ranges
    test_scores = setup_test()
    get_all_scores(test_scores, y_true, y_pred, y_prob)
    for p in test_scores:
        # remove the list structure
        test_scores[p] = test_scores[p][0]
    test_scores = at.dict2rec(test_scores)
    test_scores = at.add_cols(test_scores, ["n_gal_deviation"])
    test_scores["n_gal_deviation"] = (
        test_scores["n_galaxies_true"] - test_scores["n_galaxies_pred"]
    ) / test_scores["n_galaxies_true"]
    test_scores = at.delete_columns(test_scores, ["n_galaxies_true", "n_galaxies_pred"])
    if print_scores:
        print(clf)
        for score in test_scores.dtype.names:
            print(f"{score}: {test_scores[score]}")
        print("--------------------")
    if fig is None:
        fig, _ = plt.subplots(figsize=(10, 6), subplot_kw={"polar": True})
    fig, ax = _plot_spider(fig, test_scores, clf, ranges=ranges)
    ax.legend()
    name = get_name(clf, final=final)
    path = os.path.join(output_directory, "clf/figures/")
    file_utils.robust_makedirs(path)
    path += f"stacked_hist_{name}"
    if save_plot:
        fig.savefig(path + ".pdf", bbox_inches="tight")
        with open(path + ".pkl", "wb") as fh:
            pickle.dump(fig, fh)
    return fig


def _plot_spider(fig, data, label, ranges=None):
    """
    Plot the data in a spider plot.

    :param fig: figure object
    :param data: data to plot
    :param label: label for the data
    :param ranges: ranges for the different features
    :return: figure object
    """

    ranges = {} if ranges is None else ranges

    # Get the default ranges and update them with the given ranges
    r = ranges.copy()
    ranges = get_default_ranges_for_spider()
    ranges.update(r)

    # Prepare the data for the spider plot
    data = scale_data_for_spider(data, ranges)
    values, field_names = at.rec2arr(data, return_names=True)
    values = values.flatten()
    field_names = list(field_names)
    add_range_to_name(field_names, ranges)
    angles = np.linspace(0, 2 * np.pi, len(field_names), endpoint=False)
    values = np.concatenate((values, [values[0]]))  # Close the plot
    angles = np.concatenate((angles, [angles[0]]))  # Close the plot

    # Plot the data
    ax = fig.get_axes()[0]
    ax.plot(angles, values, label=label)

    # Add labels for each variable
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(field_names)
    ax.set_rticks(np.linspace(0, 1, 5))
    ax.set_rlim(0, 1)
    ax.set_yticklabels([])
    return fig, ax


def scale_data_for_spider(data, ranges=None):
    """
    Scale the data for the spider plot such that the chosen range corresponds to the
    0-1 range of the spider plot.

    If the lower value of the range is higher than the upper value, the data is
    inverted.

    :param data: data to scale
    :ranges: dictionary with the ranges for each variable, if a parameter is not in the
    dictionary, the default range is (0, 1)
    :return: scaled data
    """
    ranges = {} if ranges is None else ranges
    for par in data.dtype.names:
        try:
            low, high = ranges[par]
        except Exception:
            low, high = 0, 1

        if low > high:
            data[par] = 1 - (data[par] - high) / (low - high)

        else:
            data[par] = (data[par] - low) / (high - low)
        data[par] = np.clip(data[par], 0, 1)
    return data


def get_default_ranges_for_spider():
    """
    Get the default ranges for the spider plot.

    :return: dictionary with the ranges for each variable
    """
    ranges = {
        "accuracy": (0.5, 1),
        "precision": (0.5, 1),
        "recall": (0.5, 1),
        "f1": (0.5, 1),
        "n_gal_deviation": (-0.1, 0.1),
        "auc_roc_score": (0.5, 1),
        "log_loss_score": (0.5, 0),
        "brier_score": (0.1, 0),
        "auc_pr_score": (0.5, 1),
    }
    return ranges


def add_range_to_name(field_names, ranges):
    """
    Add the range to the name of the variable such that the range is visible in the
    spider plot.

    :param field_names: list with the names of the variables
    :param ranges: dictionary with the ranges for each variable
    """
    for i, f in enumerate(field_names):
        field_names[i] = f + f": {ranges[f]}"


def get_name(clf, final=False):
    """
    Get the name to add to the classifier

    :param clf: classifier object (from sklearn) or name of the classifier
    :param final: if True, the classifier was tested on the test data.
    :return: name
    """
    from edelweiss.classifier import Classifier, MultiClassifier

    name = ""
    if isinstance(clf, str):
        return clf
    elif isinstance(clf, Classifier) | isinstance(clf, MultiClassifier):
        return get_name(clf.pipe, final=final)
    elif isinstance(clf, CalibratedClassifierCV):
        clf_names = ["CalibratedClassifier"]
        if isinstance(clf.estimator, GridSearchCV):
            clf_names.extend(list(clf.estimator.estimator.named_steps.values()))
        else:
            clf_names.extend(list(clf.estimator.named_steps.values()))
    else:
        if isinstance(clf, GridSearchCV):
            clf_names = list(clf.estimator.named_steps.values())
        else:
            try:
                clf_names = list(clf.named_steps.values())
            except Exception:  # pragma: no cover
                clf_names = ["clf"]

    for n in clf_names:
        name += str(n)[:7]
        name += "_"
    if final:
        name = "final"
    return name


def plot_diagnostics(
    clf,
    X_test,
    y_test,
    output_directory=".",
    final=False,
    save_plot=False,
    special_param="mag_i",
):
    """
    Plot the diagnostics for the classifier.

    :param clf: classifier object
    :param X_test: test data
    :param y_test: true labels
    :param output_directory: directory to save the plots
    :param final: if True, the classifier was tested on the test data.
    :param save_plot: if True, save the plots
    :param special_param: param to plot the histogram for
    """
    # Get the predictions
    y_prob = clf.predict_proba(X_test)
    y_pred = clf.predict(X_test)

    # Make sure the labels are boolean
    if not isinstance(y_pred[0], bool):
        y_pred = y_pred.astype(bool)
    if not isinstance(y_test[0], bool):
        y_test = y_test.astype(bool)

    # plot the diagnostics
    param = X_test[special_param]
    plot_hist_fp_fn_tp_tn(
        param, y_test, y_pred, output_directory, clf, final=final, save_plot=save_plot
    )
    plot_hist_n_gal(
        param, y_test, y_pred, output_directory, clf, final=final, save_plot=save_plot
    )
    plot_calibration_curve(
        y_test, y_prob, output_directory, clf, final=final, save_plot=save_plot
    )
    plot_roc_curve(
        y_test, y_prob, output_directory, clf, final=final, save_plot=save_plot
    )
    plot_pr_curve(
        y_test, y_prob, output_directory, clf, final=final, save_plot=save_plot
    )


def plot_all_scores(scores, path_labels=None):
    """
    Plot all scores for the classifiers. Input can either be directly a recarray with
    the scores or the path to the scores or a list of paths to the scores. If a list
    is given, the scores of the different paths are combined and plotted with different
    colors.

    :param scores: recarray with the scores or path to the scores or list of paths
    :param path_labels: list of labels for the different paths
    """

    # Load scores if path is given
    if isinstance(scores, str):
        # assuming path to main folder
        scores = np.load(os.path.join(scores, "clf/test_scores.npy"))
        colors = None

    elif isinstance(scores, list):
        # assuming list of paths to scores
        scores = [np.load(os.path.join(path, "clf/test_scores.npy")) for path in scores]
        colors = []
        default_colors = list(COL.values())
        for i, s in enumerate(scores):
            # prepare colors for the different classifiers
            colors += len(s) * [default_colors[i]]
        scores = np.concatenate(scores)

    else:
        # assuming recarray
        colors = None

    # Setup the recarray
    try:
        names = scores["clf"]
    except Exception:
        names = len(scores) * ["classifier"]
        names = np.array(names)
    n_gal_true = scores["n_galaxies_true"][0]
    scores = at.delete_columns(scores, ["clf", "n_galaxies_true"])

    # Plot all scores
    for param in scores.dtype.names:
        data = scores[param]

        # Sort classifiers
        indices = np.argsort(data)
        data = data[indices]
        current_names = names[indices]
        x = np.arange(len(current_names))
        col = None if colors is None else np.array(colors)[indices]
        fig_width = int(len(current_names) / 3)
        plt.figure(figsize=(fig_width, 2))
        plt.title(param)

        if param == "n_galaxies_pred":
            # Plot the difference to the true number of galaxies
            y = data - n_gal_true
            sign_switch_index = next(
                (i for i, (y1, y2) in enumerate(zip(y, y[1:])) if y1 * y2 <= 0), None
            )
            if sign_switch_index is None:
                sign_switch_index = len(y) if y[0] < 0 else -1

            plt.bar(x, y, color=col)
            plt.xticks(x, current_names)
            plt.axvline(x=sign_switch_index + 0.5, color="k", ls="--")

            # Update the ticks to actual galaxies
            ticks, _ = plt.yticks()
            new_ticks = [int(tick + n_gal_true) for tick in ticks]
            plt.yticks(ticks, new_ticks)

        else:
            # Plot the scores
            plt.bar(x, data, color=col)
            plt.xticks(x, current_names)
            # Set ylim for the scores to relevant parts
            if (param != "log_loss_score") & (param != "brier_score"):
                plt.ylim(0.5, 1)

        plt.grid(axis="y")
        plt.xticks(rotation=90)

        if path_labels is not None:
            # create legend with colors of the different classifiers
            patches = []
            for i, label in enumerate(path_labels):
                patches.append(mpl.patches.Patch(color=default_colors[i], label=label))
            plt.legend(handles=patches, bbox_to_anchor=(1.05, 1), loc="upper left")
        plt.xlim(-0.5, len(current_names) - 0.5)


def plot_classifier_comparison(
    clfs,
    conf,
    path,
    spider_ranges=None,
    labels=None,
    print_scores=False,
    special_param="mag_i",
):
    """
    Plot the diagnostics for chosen classifiers. If the classifiers are not all from
    same path, the conf and path parameters should be lists of the same length as clfs.

    :param clfs: list of classifier names
    :param conf: configuration dictionary or list of dictionaries
    :param path: path to the data or list of paths
    :param spider_ranges: dictionary with the ranges for the spider plot
    :param labels: list of labels for the different paths
    :param print_scores: if True, print the scores for the different classifiers
    :param special_param: param to plot the histogram for
    """
    spider_ranges = {} if spider_ranges is None else spider_ranges
    figs = [None, None, None, None, None]
    if isinstance(path, list):
        if not isinstance(conf, list):
            conf = [conf] * len(path)
        for i, p in enumerate(path):
            label = labels[i] if labels is not None else None
            _plot_classifier_comparison(
                clfs[i],
                conf[i],
                p,
                figs,
                spider_ranges,
                label,
                print_scores,
                special_param,
            )
    else:
        _plot_classifier_comparison(
            clfs, conf, path, figs, spider_ranges, labels, print_scores, special_param
        )


def _plot_classifier_comparison(
    clfs,
    conf,
    path,
    figs,
    spider_ranges=None,
    label=None,
    print_scores=False,
    special_param="mag_i",
):
    """
    Plot the diagnostics for chosen classifiers.

    :param clfs: list of classifier names
    :param conf: configuration dictionary
    :param path: path to the data
    :param figs: list of figures
    :param spider_ranges: dictionary with the ranges for the spider plot
    :param labels: list of labels for the different paths
    :param print_scores: if True, print the scores for the different classifiers
    :param special_param: param to plot the histogram for
    """
    spider_ranges = {} if spider_ranges is None else spider_ranges
    n_clfs = len(conf["classifier"])
    n_scalers = len(conf["scaler"])
    for index in range(n_clfs * n_scalers):
        i_clf, i_scaler = np.unravel_index(index, (n_clfs, n_scalers))
        clf_name = f"{conf['classifier'][i_clf]}_{conf['scaler'][i_scaler]}"
        if clf_name in clfs:
            name = label if label is not None else clf_name
            _add_plot(
                figs, index, name, path, spider_ranges, print_scores, special_param
            )


def plot_feature_importances(clf, clf_name="classifier", summed=False):
    """
    Plots the feature importances for the classifier.

    :param clf: classifier object
    :param names: names of the features
    :param clf_name: name of the classifier
    :param summed: if True, the summed feature importances are plotted
    """
    if clf.feature_importances is None:
        LOGGER.warning("No feature importances found")
        return
    if summed:
        feat_imp, par = at.rec2arr(clf.feature_importances, return_names=True)
    else:
        feat_imp, par = at.rec2arr(clf.summed_feature_importances, return_names=True)
    par = np.array(list(par))
    feat_imp = feat_imp.flatten()

    plt.figure(figsize=(10, 5))
    plt.title(f"Feature importance for {clf_name}")
    plt.bar(par, feat_imp)
    plt.xticks(rotation=90)


def _add_plot(
    figs,
    index,
    clf_name,
    path=".",
    spider_ranges=None,
    print_scores=False,
    special_param="mag_i",
):
    """
    Add the plots for the classifier to the figure objects.

    :param figs: list of figure objects
    :param index: index of the classifier
    :param clf_name: name of the classifier
    :param path: path to the data
    :param spider_ranges: dictionary with the ranges for the spider plot
    :param print_scores: if True, print the scores for the different classifiers
    :param special_param: param to plot the histogram for
    :return: list of updated figure objects
    """
    spider_ranges = {} if spider_ranges is None else spider_ranges
    # Load the data
    from edelweiss.emulator import load_classifier

    clf = load_classifier(path, utils.get_clf_name(index))
    X_test = np.load(os.path.join(path, f"clf_cv/clf_test_data{index}.npy"))
    y_true = np.load(os.path.join(path, f"clf_cv/clf_test_labels{index}.npy"))

    # Get the predictions
    y_prob = clf.predict_proba(X_test)
    y_pred = clf.predict(X_test)

    # Add the plots
    figs[0] = plot_pr_curve(y_true, y_prob, clf=clf_name, fig=figs[0])
    figs[1] = plot_roc_curve(y_true, y_prob, clf=clf_name, fig=figs[1])
    figs[2] = plot_calibration_curve(y_true, y_prob, clf=clf_name, fig=figs[2])
    figs[3] = plot_hist_n_gal(
        X_test[special_param], y_true, y_pred, clf=clf_name, fig=figs[3]
    )
    figs[4] = plot_spider_scores(
        y_true,
        y_pred,
        y_prob,
        clf=clf_name,
        fig=figs[4],
        ranges=spider_ranges,
        print_scores=print_scores,
    )
    plot_feature_importances(clf, clf.params, clf_name)

    return figs


def setup_test(multi_class=False):
    """
    Returns a dict where the test scores will be saved.
    """

    test = {}
    test["accuracy"] = []
    test["precision"] = []
    test["recall"] = []
    test["f1"] = []
    if multi_class:
        return test
    test["n_galaxies_true"] = []
    test["n_galaxies_pred"] = []
    test["auc_roc_score"] = []
    test["log_loss_score"] = []
    test["brier_score"] = []
    test["auc_pr_score"] = []

    return test


def get_all_scores(test_arr, y_test, y_pred, y_prob):
    """
    Calculates all the scores and append them to the test_arr dict

    :param test_arr: dict where the test scores will be saved
    :param y_test: test labels
    :param y_pred: predicted labels
    :param y_prob: probability of being detected
    """
    LOGGER.info("Test scores:")
    LOGGER.info("------------")
    # calculate accuracy score
    accuracy = accuracy_score(y_test, y_pred)
    test_arr["accuracy"].append(accuracy)
    LOGGER.info(f"Accuracy: {accuracy}")

    # calculate precision score
    precision = precision_score(y_test, y_pred)
    test_arr["precision"].append(precision)
    LOGGER.info(f"Precision: {precision}")

    # calculate recall score
    recall = recall_score(y_test, y_pred)
    test_arr["recall"].append(recall)
    LOGGER.info(f"Recall: {recall}")

    # calculate f1 score
    f1 = f1_score(y_test, y_pred)
    test_arr["f1"].append(f1)
    LOGGER.info(f"F1 score: {f1}")

    # calculate number of galaxies
    n_galaxies_true = np.sum(y_test)
    test_arr["n_galaxies_true"].append(n_galaxies_true)
    n_galaxies_pred = np.sum(y_pred)
    test_arr["n_galaxies_pred"].append(n_galaxies_pred)
    LOGGER.info(f"Number of positives: {n_galaxies_pred} / {n_galaxies_true}")

    # calculate roc auc score of probabilities
    auc_roc_score = roc_auc_score(y_test, y_prob)
    test_arr["auc_roc_score"].append(auc_roc_score)
    LOGGER.info(f"ROC AUC score: {auc_roc_score}")

    # calculate log loss
    log_loss_score = log_loss(y_test, y_prob)
    test_arr["log_loss_score"].append(log_loss_score)
    LOGGER.info(f"Log loss score: {log_loss_score}")

    # calculate brier score
    brier_score = brier_score_loss(y_test, y_prob)
    test_arr["brier_score"].append(brier_score)
    LOGGER.info(f"Brier score: {brier_score}")

    # calculate average precision score (AUC-PR)
    auc_pr_score = average_precision_score(y_test, y_prob)
    test_arr["auc_pr_score"].append(auc_pr_score)
    LOGGER.info(f"AUC-PR score: {auc_pr_score}")

    LOGGER.info("------------")


def get_all_scores_multiclass(test_arr, y_test, y_pred, y_prob):
    """
    Calculates all the scores and append them to the test_arr dict for a multiclass
    classifier.

    :param test_arr: dict where the test scores will be saved
    :param y_test: test labels
    :param y_pred: predicted labels
    :param y_prob: probability of being detected
    """
    LOGGER.info("Test scores:")
    LOGGER.info("------------")
    # calculate accuracy score
    accuracy = accuracy_score(y_test, y_pred)
    test_arr["accuracy"].append(accuracy)
    LOGGER.info(f"Accuracy: {accuracy}")

    # calculate precision score
    precision = precision_score(y_test, y_pred, average="weighted")
    test_arr["precision"].append(precision)
    LOGGER.info(f"Precision: {precision}")

    # calculate recall score
    recall = recall_score(y_test, y_pred, average="weighted")
    test_arr["recall"].append(recall)
    LOGGER.info(f"Recall: {recall}")

    # calculate f1 score
    f1 = f1_score(y_test, y_pred, average="weighted")
    test_arr["f1"].append(f1)
    LOGGER.info(f"F1 score: {f1}")

    LOGGER.info("------------")
