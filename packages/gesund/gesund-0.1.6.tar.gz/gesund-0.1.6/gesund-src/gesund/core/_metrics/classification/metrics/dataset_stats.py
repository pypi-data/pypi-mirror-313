import numpy as np
import pandas as pd
from sklearn.metrics import auc
import sklearn

from gesund.core._utils import ValidationUtils, Statistics
from typing import Any, Dict, List, Optional, Union


class DatasetStats:
    def calculate_class_distributions(self, true: pd.Series) -> List[Dict[Any, int]]:
        """
        Calculates statistics on classes.
        :param true: true labels as a list = [1,0,3,4] for 4 sample dataset
        :param pred_categorical: categorical predictions as a list = [1,0,3,4] for 4 sample dataset
        :param labels: order of classes inside list
        :return: dict that contains class dist. for validation/train dataset.
        """

        return [true.value_counts().to_dict()]

    def calculate_meta_distributions(
        self, meta: pd.DataFrame
    ) -> Dict[str, Dict[str, Any]]:
        """
        Calculates statistics on meta data.
        :param true: true labels as a list = [1,0,3,4] for 4 sample dataset
        :param pred_categorical: categorical predictions as a list = [1,0,3,4] for 4 sample dataset
        :param labels: order of classes inside list
        :return: dict that contains class dist. for validation/train dataset.
        """
        # Histogram charts for numerical values
        numerical_columns = [
            column
            for column in meta.columns
            if ValidationUtils.is_list_numeric(meta[column].values.tolist())
        ]

        histograms = {
            numerical_column: Statistics.calculate_histogram(
                meta[numerical_column],
                min_=meta[numerical_column].min(),
                max_=meta[numerical_column].max(),
                n_bins=10,
            )
            for numerical_column in numerical_columns
        }

        # Bar charts for categorical values

        categorical_columns = list(set(meta.columns) - set(numerical_columns))
        bars = {
            categorical_column: meta[categorical_column].value_counts().to_dict()
            for categorical_column in categorical_columns
        }

        return {"bar": bars, "histogram": histograms}
