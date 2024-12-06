"""
Hyperopt
"""

from functools import partial
from hyperopt import fmin, tpe, STATUS_OK, Trials, space_eval


class Hyperopt:
    """Class for obtaining best hyperparams by hyperopt.

    Parameters
    ----------
    classifier : Classifier
        Classifier object to optimize
    metricser : Metrics
        Metrics object that contains main_metric to be optimized
    is_loss_function : bool
        Defines if main_metric is loss_function or needs to be adjusted as loss function
    """

    def __init__(self, classifier, metricser, is_loss_function):
        self.classifier = classifier
        self.metricser = metricser
        self.is_loss_function = is_loss_function
        self.best_params = None
        self.trials = None

    def _fit_predict_metrics(self, params):
        """Fit predict classifier with given parameters and calculate metrics.

        Parameters
        ----------
        params : dict
            Parameters for classifier fitting
        """

        self.classifier.fit_predict(params)
        self.metricser.classifier = self.classifier
        self.metricser.calculate_metrics()

    def objective(self, params):
        """Function for hyperopt to fit predict and calculate loss.

        Parameters
        ----------
        params : dict
            Dict of hyperparameter for model

        Returns
        -------
        dict
            Dictionary containing loss value and status
        """

        self._fit_predict_metrics(params)
        main_metric_score = self.metricser.get_main_metric()["score"]
        hyperopt_multiplier = 1 if self.is_loss_function else -1
        return {"loss": hyperopt_multiplier * main_metric_score, "status": STATUS_OK}

    def calculate_hyperopt_best_params(self, space, n_startup_jobs=5, hyperopt_iter=100):
        """
        Calculate models and return the best parameters in variable self.best_params.

        Parameters
        ----------
        space : dict
            Dict of parameter space, example: "'C': hp.uniform('C', 0.1, 100)"
        n_startup_jobs : int, optional
            Number of random hyperparameters search, by default 5
        hyperopt_iter : int, optional
            Number of iteration for hyperopt, by default 100
        """

        self.trials = Trials()
        self.best_params = fmin(
            fn=self.objective,
            space=space,
            algo=partial(tpe.suggest, n_startup_jobs=n_startup_jobs),
            max_evals=hyperopt_iter,
            trials=self.trials,
        )

        self.best_params = space_eval(space, self.best_params)
        self._fit_predict_metrics(self.best_params)

        print(f"The best params: {self.best_params}\n")
