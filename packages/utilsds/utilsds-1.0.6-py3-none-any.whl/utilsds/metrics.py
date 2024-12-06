"""
Metrics
"""

import numpy as np
import pandas as pd
from sklearn.metrics import (
    precision_score,
    recall_score,
    fbeta_score,
    accuracy_score,
    confusion_matrix,
)
from sklearn.model_selection import StratifiedKFold

# pylint: disable=dangerous-default-value, too-many-instance-attributes, too-many-arguments, bare-except, line-too-long, inconsistent-return-statements, consider-using-enumerate, no-else-return


class Metrics:
    """Calculates metrics for model and allows own metrics to be calculated.
    Parameters
    ----------
    classifier : object
        Classifier object with fit_predict methods.
    main_metric : str
        Name of the main metric used for optimization (e.g., 'accuracy_score', 'fbeta_score')
    metrics_average : str, optional (default='binary')
        Averaging method for metrics in multiclass classification.
    beta : float, optional (default=2)
        Beta parameter for fbeta_score metric.
    fbeta_average : str, optional (default='binary')
        Averaging method for fbeta_score in multiclass classification.
    fbeta_weights : list, optional (default=[0.5, 0.5])
        Weights for individual classes when calculating fbeta_score.
    own_metrics : dict, optional (default=None)
        Dictionary of custom metrics in format {'name': function(y_test, y_pred)}.
    """

    def __init__(
        self,
        classifier,
        main_metric: str,
        metrics_average: str = "binary",
        beta: float = 2,
        fbeta_average="binary",
        fbeta_weights=[0.5, 0.5],
        own_metrics: dict = None,
    ):
        self.classifier = classifier
        self.metrics_average = metrics_average
        self.beta: float = beta
        self.fbeta_average: str = fbeta_average
        self.fbeta_weights: list = fbeta_weights
        self.metrics = {}
        self.own_metrics = own_metrics
        self.main_metric = main_metric
        self.main_metric_score = None

        if self.own_metrics:
            self.add_own_metrics(self.own_metrics)
        self.set_main_metric(self.main_metric)

        assert sum(fbeta_weights) == 1, "Sum of fbeta_weights must be equal to 1."

    def custom_fbeta_score(self, y_test, y_pred):
        """
        Calculate fbeta score

        Parameters
        ----------
        y_test : pd.Series
            Target variable of test data
        y_pred : pd.Series
            Target variable of prediction model

        Returns
        -------
        float
            fbeta_score
        """
        if self.classifier.is_binary_class:
            score = fbeta_score(y_test, y_pred, beta=self.beta)
            return round(score, 4)
        else:
            scores = fbeta_score(
                y_true=y_test,
                y_pred=y_pred,
                beta=self.beta,
                average=self.fbeta_average,
            )
            calculated_fbeta_score = 0
            try:
                for i in range(len(scores)):
                    calculated_fbeta_score = (
                        calculated_fbeta_score + scores[i] * self.fbeta_weights[i]
                    )
                return calculated_fbeta_score
            except IndexError:
                print("length of scores and fbeta_werights are not equal")

    def specifity_score(self, y_test, y_pred):
        """Calculates specifity_score for binary_classification.

        Parameters
        ----------
        y_test : pd.Series
            Target variable of test data
        y_pred : pd.Series
            Target variable of prediction model

        Returns
        -------
        float
            Specifity score.
        """
        tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
        specificity = tn / (tn + fp)
        return specificity

    def calculate_metrics(self):
        """Calculate all metrics.

        Returns
        -------
        dict
            Dictionary containing {'key- name': value_of_given_metric}
        """
        metrics = {}
        if self.classifier.is_binary_class:
            metrics["specificity"] = self.specifity_score(
                self.classifier.y_test, self.classifier.y_pred
            )
        metrics["accuracy_score"] = accuracy_score(self.classifier.y_test, self.classifier.y_pred)
        metrics["precision_score"] = precision_score(
            self.classifier.y_test, self.classifier.y_pred, average=self.metrics_average
        )
        metrics["recall_score"] = recall_score(
            y_true=self.classifier.y_test,
            y_pred=self.classifier.y_pred,
            average=self.metrics_average,
        )
        if self.beta is not None:
            try:
                metrics["fbeta_score"] = self.custom_fbeta_score(
                    self.classifier.y_test, self.classifier.y_pred
                )
            except:
                print("Check params for fbeta_score calculations.")
        self.metrics = metrics
        if self.own_metrics:
            self.__calculate_own_metrics()
        self.metrics = {
            key: round(float(value), 4) for key, value in metrics.items()
        }  # convert all metrics to float
        return metrics

    def add_own_metrics(self, own_metrics: dict):
        """Add own metrics and calculate all metrics.

        Parameters
        ----------
            own_metrics (dict): Dictionary containing{'name_of_metric': function_to_calculate_metric},
                where function_to_calculate_metric must have parameters(y_test, y_pred).

        Returns
        -------
            None
        """
        self.own_metrics = own_metrics
        self.calculate_metrics()

    def __calculate_own_metrics(self):
        """Calculate all own metrics, by passing them two arguments: y_test, y_pred.

        Returns
        -------
        dict
            Dictionary with all previous metrics and all new own metrics.
        """
        for key, value in self.own_metrics.items():
            self.metrics[key] = value(self.classifier.y_test, self.classifier.y_pred)
        return self.metrics

    def set_main_metric(self, metric_name):
        """Select main metric for optimizing.

        Parameters
        ----------
        metric_name : str
            Name of metrics to be set as default. Choose from specificity_score, accuracy_score, precision_score, recall_score, f_beta_score OR any of own metrics.

        Returns
        -------
        None
        """
        self.calculate_metrics()
        if metric_name in self.metrics:
            self.main_metric = metric_name
            self.main_metric_score = self.metrics[metric_name]
            print("Current main_metric: ", self.main_metric)
        else:
            raise ValueError(
                "Wrong metric name. Choose from: specificity_score, accuracy_score, precision_score, recall_score, f_beta_score."
            )

    def get_main_metric(self):
        """Get main metric name and value.

        Returns
        -------
        dict
            Dictionary with {'name': name_of_main_metric, 'score': score_of_main_metric.}
        """
        self.main_metric_score = self.metrics[self.main_metric]
        return {"name": self.main_metric, "score": self.main_metric_score}

    def stratified_cross_val(self, n_splits=5):
        """
        Calculate average f beta score from StratifiedKfold

        Parameters
        ----------
        n_splits: int, default=5
            Number of folds. Must be at least 2.

        Returns
        -------
        None
        """
        temp_classifier = self.classifier

        X = np.array(
            pd.concat([temp_classifier.X_train, temp_classifier.X_test], ignore_index=True)
        )
        y = np.array(
            pd.concat([temp_classifier.y_train, temp_classifier.y_test], ignore_index=True)
        )
        scores = []
        for train_idx, test_idx in StratifiedKFold(
            n_splits=n_splits, random_state=temp_classifier.random_state, shuffle=True
        ).split(X, y):
            temp_classifier.X_train = X[train_idx]
            temp_classifier.y_train = y[train_idx]
            temp_classifier.X_test = X[test_idx]

            temp_classifier.fit_predict()

            self.calculate_metrics()
            scores.append(self.get_main_metric()["score"])

        print(
            f"""-------------------------- For stratified fold: {self.main_metric} score = \
        {np.mean(scores)}; std = {np.std(scores)} -------------------------\n"""
        )
