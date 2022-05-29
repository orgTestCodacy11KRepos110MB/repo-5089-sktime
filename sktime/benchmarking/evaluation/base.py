from typing import List
from abc import ABC, abstractmethod
from sktime.datasets import read_clusterer_result_from_uea_format

import os
import pandas as pd


class BaseEstimatorEvaluator(ABC):
    """Base class for an estimator evaluation.

    Parameters
    ----------
    results_path: str
        The path to the csv results generated by the estimators.
    evaluation_out_path: str
        The path to output the results of the evaluation
    experiment_name: str
        The name of the experiment (the directory that stores the results will be called
        this).
    """

    def __init__(
            self,
            results_path: str,
            evaluation_out_path: str,
            experiment_name: str,
    ):
        self.results_path = results_path
        self.evaluation_out_path = evaluation_out_path
        self.experiment_name = experiment_name

    def run_evaluation(self, estimators: List[str]):
        """Method to evaluate results

        Parameters
        ----------
        estimators: List[str]
            List of strings to evaluate estimators.
        """
        test_results = []
        train_results = []
        self._load_folds_for_dataset(estimators)

    @abstractmethod
    def evaluate_csv_data(self, csv_path: str):
        """Method to evaluate results

        Parameters
        ----------
        csv_path: str
            Path to csv containing the results to analyse.
        """
        ...

    def _load_folds_for_dataset(self, estimators: List[str]):
        dataset_results = {}
        for estimator in estimators:
            path = os.path.abspath(f"{self.results_path}/{estimator}/Predictions")
            for _, dirs, _ in os.walk(path):
                for dir in dirs:
                    dataset_dir = os.path.abspath(f"{path}/{dir}")
                    for _, _, files in os.walk(dataset_dir):
                        if len(files) > 1:
                            for file in files:
                                if file.endswith(".csv"):
                                    file_path = os.path.abspath(f"{dataset_dir}/{file}")
                                    self.evaluate_csv_data(file_path)

