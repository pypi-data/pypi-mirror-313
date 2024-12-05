"""
Category-related utility functions
"""

import pandas as pd
from pandas.core.dtypes.common import is_categorical_dtype


def add_category(series, new_category, inplace=False):
    """
    Add a new category to categorical pandas Series

    :param series: pandas.Series
    :param new_category: basic type, must not be None, np.nan or pd.NaT
    :param inplace: bool
    :return: if inplace return Series, else None
    """
    if not isinstance(series, pd.Series):
        raise TypeError('Argument "series" must be a pandas Series.')

    if pd.isnull(new_category):
        raise ValueError('Argument "new_category" must not be None, np.nan or pd.NaT.')

    # Return if series's dtype is not category
    if not is_categorical_dtype(series):
        if not inplace:
            return series
        return

    # Add new_category if it is not included in current categories,
    # else return
    if new_category not in set(series.dtype.categories):
        if inplace:
            series.cat.add_categories([new_category], inplace=True)
        else:
            return series.cat.add_categories([new_category])
    else:
        if not inplace:
            return series


def append_categories(series, new_series):
    """Merge categories provided by two series

    :param series:
    :param new_series:
    :return:
    """
    if not is_categorical_dtype(series.dtype):
        raise TypeError("When merging categories, series should be categorical.")
    if not is_categorical_dtype(new_series.dtype):
        new_series = new_series.astype('category')
    return series.cat.add_categories(new_series.cat.categories.difference(series.cat.categories))
