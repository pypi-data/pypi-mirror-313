"""
Vertex Experiments
"""

from typing import Dict, Union
from datetime import datetime
import numpy as np
from google.cloud import aiplatform


# pylint: disable=raise-missing-from, too-many-instance-attributes, too-many-arguments


class VertexExperiment:
    """Class for logging results of experiments on Vertex Experiments.
    Parameters:
        name_experiment : str
            Name of the Vertex Experiments instance.
        model_name : str
            Type of the evaluated model.
        metrics : dict
            Dictionary containing calculated metrics.
        confusion_matrix : numpy.ndarray
            Raw confusion matrix for logging.
        model_params : dict
            Model hyperparameters for logging.
        data_path : str
            Directory path for data in DVC.
        labels : numpy.ndarray
            Array of labels for confusion matrix.
        project : str, optional
            Google Cloud project name (default: "sts-notebooks").
        location : str, optional
            Google Cloud location (default: "europe-west4").
    """

    def __init__(
        self,
        name_experiment: str,
        model_name: str,
        metrics: Dict[str, float],
        confusion_matrix: np.ndarray,
        model_params: Dict[str, Union[str, float, int]],
        data_path: str,
        labels: np.ndarray,
        project: str = "sts-notebooks",
        location: str = "europe-west4",
    ):
        self.name_experiment = name_experiment
        self.model_name = model_name.lower()
        self.metrics = metrics
        self.model_params = model_params
        self.data_path = data_path
        self.labels = labels
        self.project = project
        self.location = location
        self.confusion_matrix = confusion_matrix

    def log_confusion_matrix(self):
        """Calculate and write confusion matrix in vertex experiment."""
        aiplatform.log_classification_metrics(
            labels=self.labels.tolist(),
            matrix=self.confusion_matrix.tolist(),
            display_name="confusion-matrix",
        )

    def log_experiment_results_to_vertex(self):
        """The function saves all values (params, metrics) on Vertex experiments.
        Returns
        -------
        None
        """

        try:
            aiplatform.init(
                project=self.project,
                location=self.location,
                experiment=self.name_experiment,
                experiment_tensorboard=False,
            )
            run_name = f"""{self.model_name
                            }{datetime.now().strftime("%Y%m%d%H%M%S")}"""
            aiplatform.start_run(run_name)

            extended_params = self.model_params
            extended_params["data_path"] = self.data_path

            aiplatform.log_params(extended_params)
            aiplatform.log_metrics(self.metrics)
            self.log_confusion_matrix()
            aiplatform.end_run()

        except TypeError:
            aiplatform.end_run()
            experiment_run = aiplatform.ExperimentRun(
                run_name=run_name,
                experiment=self.name_experiment,
                project=self.project,
                location=self.location,
            )
            experiment_run.delete()
            raise TypeError(f"TypeError: Change parameters. Experiment_run {run_name} was removed.")

        except:
            aiplatform.end_run()
            experiment_run = aiplatform.ExperimentRun(
                run_name=run_name,
                experiment=self.name_experiment,
                project=self.project,
                location=self.location,
            )
            experiment_run.delete()
            raise RuntimeError(f"UnspecifiedRuntimeError: Experiment_run {run_name} was removed.")
