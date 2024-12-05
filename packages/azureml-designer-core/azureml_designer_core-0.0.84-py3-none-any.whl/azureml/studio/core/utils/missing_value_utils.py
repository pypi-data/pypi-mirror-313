__all__ = ['is_na', 'has_na', 'drop_na', 'fill_na', 'get_number_of_na', 'df_isnull']

import random
import functools
from collections.abc import Iterable

import numpy as np
import pandas as pd
from pandas.api.types import is_categorical_dtype
from azureml.studio.core.utils.categoryutils import add_category

N_TEST = 10


def is_na(value):
    """
    This function takes a scalar or an iterable and detects
    whether this scalar is missing (NaN in numeric arrays, None or NaN
    in object arrays, NaT in datetimelike).

    For an interable, this function will detect if it is empty or all elements are NA values.

    :param value: scalar or None
    :return:
    type: bool
    """

    if isinstance(value, pd.Series):
        # If nrows is 0, return True
        nrows, = value.shape
        if nrows == 0:
            return True
        # Randomly choose N_TEST elements to check whether they are not NA.
        # By this check, we can avoid compute isna() if we hit any no NA value.
        # Use 'pd.isna(xx) is True' instead of 'pd.isna(xx)' because 'xx' could be an iterable.
        # In this case, 'pd.isna(xx)' is not a scalar, but 'pd.isna(xx) is True' is a scalar.
        if not all(pd.isna(value.iloc[random.randint(0, nrows - 1)]) is True for _ in range(N_TEST)):
            return False
        # Using Series.isna().values because it is an ndarray in numpy which is very fast.
        # When the series contain many NA values, it's much faster than generator.
        return value.isna().values.all()

    # The logic is similar to Series
    elif isinstance(value, pd.DataFrame):
        nrows, ncols = value.shape
        if nrows == 0:
            return True
        if not all(pd.isna(value.iloc[random.randint(0, nrows - 1), random.randint(0, ncols - 1)]) is True
                   for _ in range(N_TEST)
                   ):
            return False
        return value.isna().values.all()

    # For other iterable objects, detect whether it is empty or contains only missing values.
    elif isinstance(value, Iterable):
        # For a dict, we check its values.
        if isinstance(value, dict):
            return all(pd.isna(v) is True for v in value.values())
        # For str or bytes, which are iterable, we check the value itself.
        elif isinstance(value, (str, bytes)):
            return pd.isna(value)
        # For others, we recursively detect it is empty or contains only missing values.
        # Using all not np.all because np.all will convert the generator to list, which is costly.
        return all(pd.isna(v) is True for v in value)
    else:
        # For a scalar, we directly return if it is an NA value
        return pd.isna(value)


def has_na(iterable, include_inf=False):
    """
    Determine if an array has NaN

    :param iterable: an iterator with __iter__ attribute
    :return:
    type: bool
    """
    if hasattr(iterable, '__iter__'):
        # This is a workaround for bug 998318. The root cause is when include_inf is True and iterable is categorical
        # type, pandas compares inf with the internal values. However, if internal type is DatetimeIndex,
        # the comparison will raise error, since the inf is float, and cannot be converted to int.
        # Upgrade pandas to 1.1.0 can fix this, since the _isna_ndarraylike method has been updated, for details:
        # https://github.com/pandas-dev/pandas/blob/d9fff2792bf16178d4e450fe7384244e50635733/
        # pandas/core/dtypes/missing.py#L193
        if isinstance(iterable, pd.Series):
            if is_categorical_dtype(iterable.dtype) and isinstance(iterable.cat.categories, pd.DatetimeIndex):
                return iterable.isnull().any()

        with pd.option_context('use_inf_as_na', include_inf):
            return any(pd.isnull(iterable))
    else:
        raise TypeError('Input array is not an iterator')


def drop_na(series, reset_index=False, include_inf=False):
    """
    Drop all NaN in an array

    :param series: pandas.Series
    :param inplace: bool, if True, do operation in place and return None
    :param reset_index: bool, if True, reset the index
    :param include_inf: bool, if True, drop np.inf and -np.inf as well
    :return: array or None

    """

    if not isinstance(series, pd.Series):
        raise TypeError('Input array must be pandas.Series')

    with pd.option_context('use_inf_as_na', include_inf):
        if reset_index:
            return series.dropna().reset_index(drop=True)
        return series.dropna()


def fill_na(array, replacement_value, inplace=False):
    """
    replace NaN in array with replacement_value

    :param array: object with fillna method
    :param replacement_value: Value to use to fill holes (e.g. 0),
            alternately a dict/Series/DataFrame of values specifying
            which value to use for each index (for a Series) or column (for a DataFrame).
    :param inplace: bool, if True, do operation in place and return None
    :return: array or None
    """
    if not hasattr(array, 'fillna'):
        raise TypeError('Input array must have attribute fillna')

    # For categorical series, add replacement_value to categories
    if isinstance(array, pd.Series) and is_categorical_dtype(array):
        if inplace:
            add_category(
                series=array,
                new_category=replacement_value,
                inplace=True
            )
        else:
            array = add_category(
                series=array,
                new_category=replacement_value
            )

    if inplace:
        array.fillna(replacement_value, inplace=True)
    else:
        return array.fillna(replacement_value)


def get_number_of_na(array):
    """
    Compute the number of missing values in array

    """
    # This implementation is better than sum(pd.isnull(array)),
    # both in speed and memory storage
    return len(array) - pd.Series(array).count()


def df_isnull(df: pd.DataFrame, column_names=None, column_indices=None, include_inf=False):
    """Detect missing values for DataFrame

    Return a boolean series indicating if the data rows has NA in selected columns.
    Check all columns in DataFrame if no column names or column indices provided.
    Similar as Series.isnull(), but faster, lower memory cost, and support regarding inf as missing value.

    :param df: pandas.DataFrame.
    :param column_names: A list of string.
    :param column_indices: A list of 0-based int.
    :param include_inf: bool, if True, df_isnull(np.inf) will be True
    :return: a boolean series.
    """

    # same as df[col_names].isnull().any(axis=1), but fast and low memory cost

    def _series_is_null(series):
        if include_inf:
            return pd.isnull(series) | np.isinf(series)
        else:
            return pd.isnull(series)

    if column_names is not None:
        # Guard a single str input.
        if type(column_names) not in (list, tuple):
            raise ValueError("'column_names' should be a list or tuple.")
        row_isnull_per_column = map(lambda col_name: _series_is_null(df[col_name]), column_names)
    elif column_indices is not None:
        if type(column_indices) not in (list, tuple):
            raise ValueError("'column_indices' should be a list or tuple.")
        row_isnull_per_column = map(lambda col_idx: _series_is_null(df.iloc[:, col_idx]), column_indices)
    else:
        row_isnull_per_column = map(lambda col_idx: _series_is_null(df.iloc[:, col_idx]), range(0, df.shape[1]))

    return functools.reduce(lambda a, b: a | b, row_isnull_per_column)
