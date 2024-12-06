"""
Class to preprocessing data
"""

# pylint: disable=too-many-instance-attributes

import pandas as pd
import numpy as np
from scipy import stats
from sklearn.preprocessing import StandardScaler


class DataTransformer:
    """
    A class for preprocessing numerical data with various transformation methods.

    Parameters
    ----------
    data : pd.DataFrame
        DataFrame containing data to be transformed
    sqrt_col : list, optional
        Columns for square root transformation (requires non-negative values)
    log_default : list, optional
        Columns for logarithmic transformation with added constant 0.01
    ihs : list, optional
        Columns for inverse hyperbolic sine transformation
    extensive_log : list, optional
        Columns for extensive logarithmic transformation
    neglog : list, optional
        Columns for logarithmic transformation with negative values handling
    boxcox_zero : list, optional
        Columns for Box-Cox transformation with zero handling
    log_x_divide_2 : list, optional
        Columns for logarithmic transformation with half minimum non-zero value
    """

    def __init__(
        self,
        data,
        sqrt_col=[],
        log_default=[],
        ihs=[],
        extensive_log=[],
        neglog=[],
        boxcox_zero=[],
        log_x_divide_2=[],
    ):

        self.transform_data = data.copy()
        self.sqrt_col = sqrt_col
        self.log_default = log_default
        self.ihs = ihs
        self.extensive_log = extensive_log
        self.neglog = neglog
        self.boxcox_zero = boxcox_zero
        self.log_x_divide_2 = log_x_divide_2

    def sqrt_transformation(self, column):
        """Sqrt transformation

        Parameters
        ----------
        column : list
            List of column to transform.
        """
        if (self.transform_data[column] < 0).any():
            raise ValueError(f"Column {column} contains negative values")
        self.transform_data[column] = np.sqrt(self.transform_data[column])

    def log_default_transformation(self, column, value_add):
        """Log transformation

        Parameters
        ----------
        column : str
            Name of the column to transform.
        value_add : float
            Constant added before logarithmic transformation.
        """
        self.transform_data[column] = np.log(self.transform_data[column] + value_add)

    def ihs_transformation(self, column):
        """IHS transformation

        Parameters
        ----------
        column : list
            List of column to transform.
        """
        self.transform_data[column] = np.arcsinh(self.transform_data[column])

    def extensive_log_transformation(self, column):
        """Extensive log transformation

        Parameters
        ----------
        column : list
            List of column to transform.
        """
        min_data = self.transform_data[column].min()
        self.transform_data[column] = self.transform_data[column].apply(
            lambda x: np.log(x - (min_data - 1))
        )

    def neglog_transformation(self, column):
        """Neglog transformation

        Parameters
        ----------
        column : list
            List of column to transform.
        """
        self.transform_data[column] = self.transform_data[column].apply(
            lambda x: np.sign(x) * np.log(abs(x) + 1)
        )

    def boxcox_zero_transformation(self, column):
        """Boxcox transformation

        Parameters
        ----------
        column : list
            List of column to transform.
        """
        posdata = self.transform_data[self.transform_data[column] > 0][column]
        bcdata, lam = stats.boxcox(posdata)
        boxcox = np.empty_like(self.transform_data[column])
        boxcox[self.transform_data[column] > 0] = bcdata
        boxcox[self.transform_data[column] == 0] = -1 / lam
        self.transform_data[column] = boxcox

    def log_x_divide_2_transformation(self, column):
        """Log transformation

        Parameters
        ----------
        column : list
            List of column to transform.
        """
        min_non_zero = self.transform_data[self.transform_data[column] > 0][column].min()
        self.transform_data[column] = np.log(self.transform_data[column] + (min_non_zero / 2))

    def func_transform_data(self):
        """Function to transform all data.

        Returns
        -------
        pd.Dataframe
            Transformed dataframe.
        """
        transformations = {
            "log_default": (self.log_default, self.log_default_transformation, 0.01),
            "sqrt": (self.sqrt_col, self.sqrt_transformation),
            "ihs": (self.ihs, self.ihs_transformation),
            "extensive_log": (self.extensive_log, self.extensive_log_transformation),
            "boxcox_zero": (self.boxcox_zero, self.boxcox_zero_transformation),
            "neglog": (self.neglog, self.neglog_transformation),
            "log_x_divide_2": (self.log_x_divide_2, self.log_x_divide_2_transformation),
        }

        for transform_info in transformations.values():
            columns = transform_info[0]  # lista kolumn
            transform_func = transform_info[1]  # funkcja transformacji

            for column in columns:
                if column in self.transform_data.columns:
                    if len(transform_info) == 3:  # jeśli jest dodatkowy parametr (dla log_default)
                        transform_func(column, transform_info[2])
                    else:
                        transform_func(column)
        return self.transform_data
