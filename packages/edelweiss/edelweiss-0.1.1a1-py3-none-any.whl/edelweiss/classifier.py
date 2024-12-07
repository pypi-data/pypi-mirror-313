# Copyright (C) 2023 ETH Zurich
# Institute for Particle Physics and Astrophysics
# Author: Silvan Fischbacher

import contextlib
import os
import pickle

import joblib
import numpy as np
from cosmic_toolbox import arraytools as at
from cosmic_toolbox import file_utils, logger
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import GridSearchCV

from edelweiss import clf_diagnostics, clf_utils

LOGGER = logger.get_logger(__file__)


def load_classifier(path, subfolder=None):
    """
    Load a classifier from a given path.

    :param path: path to the folder containing the emulator
    :param subfolder: subfolder of the emulator folder where the classifier is stored
    :return: the loaded classifier
    """
    if subfolder is None:
        subfolder = "clf"
    output_directory = os.path.join(path, subfolder)

    # Load classifier state

    # Load classifier state
    with open(os.path.join(output_directory, "clf.pkl"), "rb") as f:
        clf = pickle.load(f)

    # Load pipeline

    # Load pipeline
    clf.pipe = joblib.load(os.path.join(output_directory, "model.pkl"))

    # Load TF models if needed
    if clf.clf == "NeuralNetwork":
        import tensorflow as tf

        if clf.calibrate:
            # Load calibrated models
            for i, calibrated_clf in enumerate(clf.pipe.calibrated_classifiers_):
                try:
                    # First try loading as h5 (Keras 2 format)
                    model_path = os.path.join(
                        output_directory, f"tf_calibrated_model_{i}.h5"
                    )
                    if os.path.exists(model_path):
                        model = tf.keras.models.load_model(model_path)
                    else:  # pragma: no cover
                        # Try Keras 3 format
                        model = tf.keras.models.load_model(
                            os.path.join(
                                output_directory, f"tf_calibrated_model_{i}.keras"
                            )
                        )
                except Exception as e:  # pragma: no cover
                    LOGGER.error(f"Failed to load model: {e}")
                    raise

                if clf.cv > 1:
                    calibrated_clf.estimator.best_estimator_.named_steps[
                        "clf"
                    ].model = model
                else:
                    calibrated_clf.estimator.named_steps["clf"].model = model
        else:
            try:
                # First try loading as h5 (Keras 2 format)
                model_path = os.path.join(output_directory, "tf_model.h5")
                if os.path.exists(model_path):
                    model = tf.keras.models.load_model(model_path)
                else:  # pragma: no cover
                    # Try Keras 3 format
                    model = tf.keras.models.load_model(
                        os.path.join(output_directory, "tf_model.keras")
                    )
            except Exception as e:  # pragma: no cover
                LOGGER.error(f"Failed to load model: {e}")
                raise

            if clf.cv > 1:
                clf.pipe.best_estimator_.named_steps["clf"].model = model
            else:
                clf.pipe.named_steps["clf"].model = model

    return clf


class Classifier:
    """
    The detection classifer class that wraps a sklearn classifier.

    :param scaler: the scaler to use for the classifier, options: standard, minmax,
        maxabs, robust, quantile
    :param clf: the classifier to use, options are: XGB, MLP, RandomForest,
                NeuralNetwork, LogisticRegression, LinearSVC, DecisionTree, AdaBoost,
                GaussianNB, QDA, KNN,
    :param calibrate: whether to calibrate the probabilities
    :param cv: number of cross validation folds, if 0 no cross validation is performed
    :param cv_scoring: the scoring method to use for cross validation
    :param params: the names of the parameters
    :param clf_kwargs: additional keyword arguments for the classifier
    """

    def __init__(
        self,
        scaler="standard",
        clf="XGB",
        calibrate=True,
        cv=0,
        cv_scoring="f1",
        params=None,
        **clf_kwargs,
    ):
        """
        Initialize the classifier.
        """
        self.scaler = scaler
        self.clf = clf
        sc = clf_utils.get_scaler(scaler)
        self.pipe = clf_utils.get_classifier(clf, sc, **clf_kwargs)
        self.calibrate = calibrate
        self.cv = cv
        self.cv_scoring = cv_scoring
        self.params = params
        self.test_scores = None

    def train(self, X, y, param_grid=None, **args):
        """
        Train the classifier.

        :param X: the features to train on (array or recarray)
        :param y: the labels to train on
        :param param_grid: the hyperparameter grid to search over
        :param args: additional arguments for the classifier
        """
        X = self._check_if_recarray(X)

        if self.params is None:
            self.params = np.arange(X.shape[1])
            LOGGER.warning("No parameter names provided, numbers are used instead")
        else:
            assert len(self.params) == X.shape[1], (
                "Number of parameters in training data does not match number"
                " of parameters provided before"
            )

        LOGGER.info("Training this model:")
        if self.calibrate:
            LOGGER.info("CalibratedClassifierCV")
        clf_names = self.pipe.named_steps.items()
        for name, estimator in clf_names:
            LOGGER.info(f"{name}:")
            LOGGER.info(estimator)
        LOGGER.info(f"number of samples: {X.shape[0]}")
        LOGGER.info("-------------------")

        # tune hyperparameters with grid search
        if self.cv > 1:
            LOGGER.info("Start cross validation")
            if param_grid is None:
                param_grid = clf_utils.load_hyperparams(self.pipe["clf"])
            scorer = clf_utils.get_scorer(self.cv_scoring)

            # Set up the grid search
            if "SLURM_CPUS_PER_TASK" in os.environ:  # pragma: no cover
                n_jobs = max(int(os.environ["SLURM_CPUS_PER_TASK"]) // 4, 1)
            else:
                n_jobs = 1
            LOGGER.info(f"Running the Grid search on {n_jobs} jobs")
            self.pipe = GridSearchCV(
                estimator=self.pipe,
                param_grid=param_grid,
                scoring=scorer,
                cv=self.cv,
                n_jobs=n_jobs,
            )

            if self.calibrate:
                self.pipe = CalibratedClassifierCV(
                    self.pipe, cv=self.cv, method="isotonic"
                )

            # Run the grid search
            self.pipe.fit(X, y, **args)

            if self.calibrate:
                best_params = self.pipe.calibrated_classifiers_[
                    0
                ].estimator.best_params_
            else:
                best_params = self.pipe.best_params_
            LOGGER.info("Best parameters found by grid search: %s", best_params)
        else:
            if self.calibrate:
                self.pipe = CalibratedClassifierCV(self.pipe, cv=2, method="isotonic")
            self.pipe.fit(X, y, **args)
        self._get_feature_importance()
        self._get_summed_feature_importance()
        LOGGER.info("Training completed")

    fit = train

    def predict(self, X, prob_multiplier=1.0):
        """
        Predict the labels for a given set of features.

        :param X: the features to predict on (array or recarry)
        :return: the predicted labels
        """
        X = self._check_if_recarray(X)
        y_prob = self.pipe.predict_proba(X)[:, 1] * prob_multiplier
        y_prob = np.clip(y_prob, 0, 1)
        y_pred = y_prob > np.random.rand(len(y_prob))
        return y_pred

    def predict_proba(self, X):
        """
        Predict the probabilities for a given set of features.

        :param X: the features to predict on (array or recarry)
        :return: the predicted probabilities
        """
        X = self._check_if_recarray(X)
        y_prob = self.pipe.predict_proba(X)[:, 1]
        return y_prob

    def predict_non_proba(self, X):
        """
        Predict the probabilities for a given set of features.

        :param X: the features to predict on (array or recarry)
        :return: the predicted probabilities
        """
        X = self._check_if_recarray(X)
        y_pred = self.pipe.predict(X)
        return y_pred.astype(bool)

    __call__ = predict

    def save(self, path, subfolder=None):
        """Save the classifier to a given path."""
        if subfolder is None:
            subfolder = "clf"
        output_directory = os.path.join(path, subfolder)
        file_utils.robust_makedirs(output_directory)

        # Create clean pipeline copy without TF models
        clean_pipe = self._create_clean_pipeline()

        # Save pipeline
        joblib.dump(clean_pipe, os.path.join(output_directory, "model.pkl"))

        # Save TF models if needed
        if self.clf == "NeuralNetwork":
            if self.calibrate:
                self._save_calibrated_tf_models(output_directory)
            else:
                # For GridSearchCV, save the best model
                if self.cv > 1:
                    base_model = self.pipe.best_estimator_.named_steps["clf"].model
                else:
                    base_model = self.pipe.named_steps["clf"].model

                # Save in both formats for compatibility
                base_model.save(os.path.join(output_directory, "tf_model.h5"))
                with contextlib.suppress(Exception):
                    base_model.save(
                        os.path.join(output_directory, "tf_model.keras"),
                        save_format="keras_v3",
                    )

        # Save classifier state
        self.pipe = None
        with open(os.path.join(output_directory, "clf.pkl"), "wb") as f:
            pickle.dump(self, f)
        LOGGER.info(f"Classifier saved to {output_directory}")

    def _create_clean_pipeline(self):
        """Create copy of pipeline without TF models."""
        import copy

        # Store model references
        if self.clf == "NeuralNetwork":
            # Temporarily remove models
            if self.calibrate:
                models = []
                for clf in self.pipe.calibrated_classifiers_:
                    if self.cv > 1:
                        model = clf.estimator.best_estimator_.named_steps["clf"].model
                        clf.estimator.best_estimator_.named_steps["clf"].model = None
                    else:
                        model = clf.estimator.named_steps["clf"].model
                        clf.estimator.named_steps["clf"].model = None
                    models.append(model)
            else:
                if self.cv > 1:
                    model = self.pipe.best_estimator_.named_steps["clf"].model
                    self.pipe.best_estimator_.named_steps["clf"].model = None
                else:
                    model = self.pipe.named_steps["clf"].model
                    self.pipe.named_steps["clf"].model = None

        # deepcopy without tf models
        clean_pipe = copy.deepcopy(self.pipe)

        # Restore original models
        if self.clf == "NeuralNetwork":
            if self.calibrate:
                for i, clf in enumerate(self.pipe.calibrated_classifiers_):
                    if self.cv > 1:
                        clf.estimator.best_estimator_.named_steps["clf"].model = models[
                            i
                        ]
                    else:
                        clf.estimator.named_steps["clf"].model = models[i]
            else:
                if self.cv > 1:
                    self.pipe.best_estimator_.named_steps["clf"].model = model
                else:
                    self.pipe.named_steps["clf"].model = model

        return clean_pipe

    def _save_calibrated_tf_models(self, output_directory):
        """Save calibrated TF models separately."""
        for i, clf in enumerate(self.pipe.calibrated_classifiers_):
            if self.cv > 1:
                model = clf.estimator.best_estimator_.named_steps["clf"].model
            else:
                model = clf.estimator.named_steps["clf"].model

            # Save in both formats for compatibility
            model.save(os.path.join(output_directory, f"tf_calibrated_model_{i}.h5"))
            with contextlib.suppress(Exception):
                model.save(
                    os.path.join(output_directory, f"tf_calibrated_model_{i}.keras"),
                    save_format="keras_v3",
                )

    def test(self, X_test, y_test, non_proba=False):
        """
        Tests the classifier on the test data

        :param test_arr: dict where the test scores will be saved
        :param clf: classifier
        :param X_test: test data
        :param y_test: test labels
        :param non_proba: whether to use non-probabilistic predictions
        """

        # get probability of being detected
        y_prob = self.predict_proba(X_test)
        y_pred = self.predict_non_proba(X_test) if non_proba else self.predict(X_test)
        test_arr = clf_diagnostics.setup_test()
        clf_diagnostics.get_all_scores(test_arr, y_test, y_pred, y_prob)
        test_arr = at.dict2rec(test_arr)
        self.test_scores = test_arr

    def _check_if_recarray(self, X):
        try:
            X, names = at.rec2arr(X, return_names=True)
            if self.params is None:
                self.params = names
            else:
                assert np.all(
                    names == self.params
                ), "Input parameters do not match the trained parameters"
            return X
        except Exception:
            return X

    def _get_feature_importance(self):
        with contextlib.suppress(Exception):
            # Try to get the feature importances if clf is GridSearchCV
            importances = self.pipe.best_estimator_["clf"].feature_importances_
            self.feature_importances = at.arr2rec(importances, self.params)
            return
        try:
            # Try to get the feature importances if clf is CalibratedClassifierCV
            importances = self.pipe.calibrated_classifiers_[
                0
            ].estimator._final_estimator.feature_importances_
            self.feature_importances = at.arr2rec(importances, self.params)
            return
        except Exception:
            with contextlib.suppress(Exception):
                # Try to get the feature importances if clf is CalibratedClassifierCV
                # and GridSearchCV
                importances = (
                    self.pipe.calibrated_classifiers_[0]
                    .estimator.best_estimator_.named_steps["clf"]
                    .feature_importances_
                )
                self.feature_importances = at.arr2rec(importances, self.params)
                return
        try:
            # Try to get the feature importances if clf is not GridSearchCV
            importances = self.pipe["clf"].feature_importances_
            self.feature_importances = at.arr2rec(importances, self.params)
            return
        except Exception:
            self.feature_importances = None

    def _get_summed_feature_importance(self):
        """
        Sum the feature importances of the same parameter across different bands.
        Should be run after _get_feature_importance.
        """
        feature_importances = self.feature_importances
        if feature_importances is None:
            self.summed_feature_importances = None
            return

        # Create a dictionary to store the summed values based on modified prefixes
        summed_features = {}

        # Iterate through the feature importances, remove last character if suffix
        # length is 1
        for key in feature_importances.dtype.names:
            parts = key.split("_")
            prefix = (
                "_".join(parts[:-1]) if len(parts[-1]) == 1 and len(parts) > 1 else key
            )  # Remove the last character if suffix length is 1

            if prefix not in summed_features:
                summed_features[prefix] = 0.0

            summed_features[prefix] += feature_importances[key]

        self.summed_feature_importances = at.dict2rec(summed_features)


def load_multiclassifier(path, subfolder=None):
    """
    Load a multiclassifier from a given path.

    :param path: path to the folder containing the emulator
    :param subfolder: subfolder of the emulator folder where the classifier is stored
    :return: the loaded classifier
    """
    if subfolder is None:
        subfolder = "clf"
    output_directory = os.path.join(path, subfolder)
    with open(os.path.join(output_directory, "clf.pkl"), "rb") as f:
        clf = pickle.load(f)
    clf.pipe = []
    for label in clf.labels:
        clf.pipe.append(load_classifier(path, subfolder=f"{subfolder}_{label}"))
    LOGGER.debug(f"Classifier loaded from {output_directory}")
    return clf


class MultiClassifier:
    """
    A classifier class that trains multiple classifiers for a specific label. This label
    could e.g. be the galaxy type (star, red galaxy, blue galaxy).

    :param split_label: the label to split the data in different classifers
    :param labels: the different labels of the split label
    :param scaler: the scaler to use for the classifier
    :param clf: the classifier to use
    :param calibrate: whether to calibrate the probabilities
    :param cv: number of cross validation folds, if 0 no cross validation is performed
    :param cv_scoring: the scoring method to use for cross validation
    :param params: the names of the parameters
    :param clf_kwargs: additional keyword arguments for the classifier
    """

    def __init__(
        self,
        split_label="galaxy_type",
        labels=None,
        scaler="standard",
        clf="XGB",
        calibrate=True,
        cv=0,
        cv_scoring="f1",
        params=None,
        **clf_kwargs,
    ):
        """
        Initialize the classifier.
        """
        if labels is None:
            labels = [-1, 0, 1]
        self.split_label = split_label
        self.labels = labels
        self.scaler = scaler
        self.clf = clf
        self.pipe = [
            Classifier(
                scaler=scaler,
                clf=clf,
                calibrate=calibrate,
                cv=cv,
                cv_scoring=cv_scoring,
                params=params,
                **clf_kwargs,
            )
            for _ in self.labels
        ]

    def train(self, X, y):
        """
        Train the classifier.
        """
        # TODO: dirty hack, fix this
        self.params = X.dtype.names
        for i, label in enumerate(self.labels):
            idx = X[self.split_label] == label
            X_ = at.delete_cols(X[idx], self.split_label)
            self.pipe[i].train(X_, y[idx])

    fit = train

    def predict(self, X):
        """
        Predict the labels for a given set of features.
        """
        y_pred = np.zeros(len(X), dtype=bool)
        for i, label in enumerate(self.labels):
            idx = X[self.split_label] == label
            if np.sum(idx) == 0:
                continue
            X_ = at.delete_cols(X[idx], self.split_label)
            y_pred[idx] = self.pipe[i].predict(X_)
        return y_pred

    def predict_proba(self, X):
        """
        Predict the probabilities for a given set of features.
        """
        y_prob = np.zeros(len(X), dtype=float)
        for i, label in enumerate(self.labels):
            idx = X[self.split_label] == label
            if np.sum(idx) == 0:
                continue
            y_prob[idx] = self.pipe[i].predict_proba(X[idx])
        return y_prob

    def predict_non_proba(self, X):
        """
        Predict the probabilities for a given set of features.
        """
        y_pred = np.zeros(len(X), dtype=bool)
        for i, label in enumerate(self.labels):
            idx = X[self.split_label] == label
            if np.sum(idx) == 0:
                continue
            X_ = at.delete_cols(X[idx], self.split_label)
            y_pred[idx] = self.pipe[i].predict_non_proba(X_)
        return y_pred

    __call__ = predict

    def save(self, path, subfolder=None):
        """
        Save the classifier to a given path.

        :param path: path to the folder where the emulator is saved
        :param subfolder: subfolder of the emulator folder where the classifier is
                          stored
        """
        if subfolder is None:
            subfolder = "clf"
        output_directory = os.path.join(path, subfolder)
        file_utils.robust_makedirs(output_directory)
        for i, label in enumerate(self.labels):
            self.pipe[i].save(path, subfolder=f"{subfolder}_{label}")
        self.pipe = None
        with open(os.path.join(path, subfolder, "clf.pkl"), "wb") as f:
            pickle.dump(self, f)
        LOGGER.info(f"MultiClassifier saved to {os.path.join(path, subfolder)}")

    def test(self, X_test, y_test, non_proba=False):
        """
        Tests the classifier on the test data

        :param test_arr: dict where the test scores will be saved
        :param clf: classifier
        :param X_test: test data
        :param y_test: test labels
        :param non_proba: whether to use non-probabilistic predictions
        """
        # get probability of being detected
        y_prob = self.predict_proba(X_test)
        y_pred = self.predict_non_proba(X_test) if non_proba else self.predict(X_test)
        test_arr = clf_diagnostics.setup_test()
        clf_diagnostics.get_all_scores(test_arr, y_test, y_pred, y_prob)
        test_arr = at.dict2rec(test_arr)
        self.test_scores = test_arr


class MultiClassClassifier(Classifier):
    """
    The detection classifer class that wraps a sklearn classifier for multiple classes.

    :param scaler: the scaler to use for the classifier, options: standard, minmax,
        maxabs, robust, quantile
    :param clf: the classifier to use, options are: XGB, MLP, RandomForest,
                NeuralNetwork, LogisticRegression, LinearSVC, DecisionTree, AdaBoost,
                GaussianNB, QDA, KNN,
    :param calibrate: whether to calibrate the probabilities
    :param cv: number of cross validation folds, if 0 no cross validation is performed
    :param cv_scoring: the scoring method to use for cross validation
    :param params: the names of the parameters
    :param clf_kwargs: additional keyword arguments for the classifier
    """

    def predict(self, X):
        """
        Predict the labels for a given set of features.

        :param X: the features to predict on (array or recarry)
        :return: the predicted labels
        """
        X = self._check_if_recarray(X)
        y_prob = self.pipe.predict_proba(X)
        y_pred = np.array([np.random.choice(len(prob), p=prob) for prob in y_prob])

        return y_pred

    def predict_proba(self, X):
        """
        Predict the probabilities for a given set of features.

        :param X: the features to predict on (array or recarry)
        :return: the predicted probabilities
        """
        X = self._check_if_recarray(X)
        y_prob = self.pipe.predict_proba(X)
        return y_prob

    def predict_non_proba(self, X):
        """
        Predict the class non-probabilistically for a given set of features.

        :param X: the features to predict on (array or recarry)
        :return: the predicted probabilities
        """
        X = self._check_if_recarray(X)
        y_pred = self.pipe.predict(X)
        return y_pred

    def test(self, X_test, y_test, non_proba=False):
        y_pred = self.predict_non_proba(X_test) if non_proba else self.predict(X_test)
        y_prob = self.predict_proba(X_test)

        test_arr = clf_diagnostics.setup_test(multi_class=True)
        clf_diagnostics.get_all_scores_multiclass(test_arr, y_test, y_pred, y_prob)
        test_arr = at.dict2rec(test_arr)
        self.test_scores = test_arr
