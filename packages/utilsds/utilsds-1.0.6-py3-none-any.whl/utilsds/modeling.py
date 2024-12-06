"""
Model class
"""

import pandas as pd
import numpy as np

from .classifier import Classifier
from .metrics import Metrics
from .confusion_matrix import ConfusionMatrix
from .experiments import VertexExperiment
from .hyperopt import Hyperopt

# pylint: disable=attribute-defined-outside-init
# pylint: disable=raise-missing-from
# pylint: disable=invalid-name
# pylint: disable=dangerous-default-value
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
# pylint: disable=too-many-instance-attributes


class Modeling:
    """Modeling, metrics and vertex logging.
    Parameters
    ----------
    model : object
        Model class (scikit-learn compatible) that implements fit/predict methods
    X_train : pd.DataFrame
        Training features
    X_test : pd.DataFrame
        Test features
    y_train : pd.DataFrame
        Training labels
    y_test : pd.DataFrame
        Test labels
    is_binary_class : bool
        If True, treats as binary classification problem
    main_metric : str
        Metric name to optimize during hyperparameter tuning
    model_params : dict, optional
        Initial hyperparameters for model initialization
    proba : float, default=0.5
        Classification threshold for binary problems
    own_metrics : dict, optional
        Custom metrics as {'name': callable(y_true, y_pred)}
    metrics_average : str, default='binary'
        Averaging method for precision/recall in multiclass case
    beta : float, default=2
        Beta value for fbeta_score calculation
    fbeta_average : str, default='binary'
        Averaging method for fbeta_score in multiclass case
    fbeta_weights : list, default=[0.5, 0.5]
        Class weights for fbeta_score calculation
    name_experiment : str, optional
        Name of the experiment in Vertex AI
    data_path : str, optional
        Path to data files in DVC
    labels : list, optional
        Class labels for confusion matrix
    project : str, optional
        Vertex AI project name
    location : str, optional
        Vertex AI location
    """

    def __init__(
        self,
        model,
        X_train: pd.DataFrame,
        X_test: pd.DataFrame,
        y_train: pd.Series,
        y_test: pd.Series,
        is_binary_class: bool,
        main_metric: str,
        model_params: dict = None,
        proba: float = 0.5,
        own_metrics: dict = None,
        metrics_average="binary",
        beta=2,
        fbeta_average="binary",
        fbeta_weights=[0.5, 0.5],
        name_experiment: str = None,
        data_path: str = None,
        labels: list = None,
        project: str = "sts-notebooks",
        location: str = "europe-west4",
    ):

        self.classifier = Classifier(
            model, X_train, X_test, y_train, y_test, is_binary_class, model_params, proba
        )
        self.metricser = Metrics(
            self.classifier,
            main_metric=main_metric,
            metrics_average=metrics_average,
            beta=beta,
            fbeta_average=fbeta_average,
            fbeta_weights=fbeta_weights,
            own_metrics=own_metrics,
        )
        self.confusion_matrixer = ConfusionMatrix(self.classifier)
        if labels:
            self.labels = labels
        else:
            self.labels = np.sort(y_test[y_test.columns[0]].unique()).astype(str)
        self.name_experiment = name_experiment
        self.data_path = data_path
        self.project = project
        self.location = location
        self.log_vertex_experiments()

    def log_vertex_experiments(self):
        """Log results of model to Vertex Experiments."""
        if not self.metricser.metrics:
            self.metricser.calculate_metrics()
        vertex_experiment = VertexExperiment(
            self.name_experiment,
            self.classifier.model_name,
            self.metricser.metrics,
            self.confusion_matrixer.get_raw_confusion_matrix(),
            self.classifier.hyperparams_model(),
            self.data_path,
            self.labels,
            self.project,
            self.location,
        )
        vertex_experiment.log_experiment_results_to_vertex()
        self.get_general_metrics()

    def calculate_hyperopt_best_params(
        self, space, n_startup_jobs, hyperopt_iter, is_loss_function=False
    ):
        """Calculate optimal hyperparameters using hyperopt.

        Parameters
        ----------
        space : dict
            Hyperparameter search space definition
        n_startup_jobs : int
            Number of random initialization trials
        hyperopt_iter : int
            Total number of optimization iterations
        is_loss_function : bool, default=False
            If True, metric should be minimized instead of maximized

        """
        self.hyperopt = Hyperopt(self.classifier, self.metricser, is_loss_function=is_loss_function)
        self.hyperopt.calculate_hyperopt_best_params(space, n_startup_jobs, hyperopt_iter)

    def get_general_metrics(self):
        """Get all metrics and combined confusion_matrix."""
        print(self.metricser.get_main_metric())
        print(self.metricser.metrics)
        self.confusion_matrixer.plot_combined_confusion_matrix()
