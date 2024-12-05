import pytest
import pandas as pd
import numpy as np

from azureml.studio.core.io.data_frame_directory import DataFrameDirectory


"""
  Test column selection.
"""


def _get_column_selection_legacy_and_sdk_formats():
    return [
        # Test select all columns.
        (
            '{"isFilter":true,"rules":[{"ruleType":"AllColumns","exclude":false}]}',
            '["AllColumns"]'
        ),
        # Test select columns by names.
        (
            '{"isFilter":true,"rules":[{"ruleType":"ColumnNames",'
            '"columns":["float","int"],"exclude":false}]}',
            '[{"KeepInputDataOrder":true,"ColumnNames":["float","int"]}]'
        ),
        # Test select columns by indexes.
        (
            '{"isFilter":true,"rules":[{"ruleType":"ColumnIndexes","columns":["1","2"],'
            '"exclude":false}]}',
            '[{"KeepInputDataOrder":true,"ColumnIndices":[1,2]}]'
        ),
        # Test select columns by index ranges.
        (
            '{"isFilter":true,"rules":[{"exclude":false,"ruleType":"ColumnIndexes","columns":["1-3", "5"]}]}',
            '[{"KeepInputDataOrder":true,"ColumnIndices":["1-3", 5]}]'
        ),
        # Test select columns by index ranges and indexes.
        (
            '{"isFilter":true,"rules":[{"exclude":false,"ruleType":"ColumnIndexes","columns":["1-3"]}]}',
            '[{"KeepInputDataOrder":true,"ColumnIndices":["1-3"]}]'
        ),
        # Test select columns by all types.
        (
            '{"isFilter":true,"rules":[{"exclude":false,"ruleType":"ColumnTypes",'
            '"columnKinds":["All"],"columnTypes":["AllTypes"]}]}',
            '[{"ColumnTypes":["AllTypes"]}]'
        ),
        # Test select columns by specific types.
        (
            '{"isFilter":true,"rules":[{"exclude":false,"ruleType":"ColumnTypes","columnKinds":["All"],'
            '"columnTypes":["Integer"]}]}',
            '[{"ColumnTypes":["Integer"]}]'
        ),
        # Test select columns by specific kinds.
        (
            '{"isFilter":true,"rules":[{"exclude":false,"ruleType":"ColumnTypes",'
            '"columnTypes":["All"],"columnKinds":["Feature"]}]}',
            '[{"ColumnKinds":["Feature"]}]'
        ),
        # Test select columns by multiple rules.
        (
            '{"isFilter":true,"rules":[{"exclude":false,"ruleType":"AllColumns"},'
            '{"exclude":true,"ruleType":"ColumnIndexes","columns":["1","2"]},'
            '{"exclude":false,"ruleType":"ColumnTypes","columnKinds":["Feature"],'
            '"columnTypes":["All"]}, {"exclude":false,"ruleType":"AllColumns"}]}',
            '[{"ColumnIndices":[1,2],"exclude":true},{"ColumnKinds":["Feature"]},"AllColumns"]'
        ),
        # Test select columns for exclude is true.
        (
            '{"isFilter":true,"rules":[{"exclude":false,"ruleType":"AllColumns"},'
            '{"exclude":true,"ruleType":"ColumnNames","columns":["int","float"]}]}',
            '["AllColumns", {"exclude":true,"columnnames":["int","float"]}]'
        ),
        # Test select columns for is_filter is false.
        (
            '{"isFilter":false,"rules":[{"exclude":false,"ruleType":"ColumnNames",'
            '"columns":["int","float"]}]}',
            '[{"columnnames":["int","float"]}]'
        )
    ]


def df():
    return pd.DataFrame({'float': [1.0, 2.0],
                         'int': [1, 2],
                         'datetime': [pd.Timestamp('20180310'), pd.Timestamp('20190910')],
                         'string': ['foo', 'bar'],
                         'bool': [True, False],
                         'bool_category': pd.Series([True, False]).astype('category'),
                         'int_category': pd.Series([5, 3]).astype('category'),
                         'float_category': pd.Series([1.0, 2.0]).astype('category'),
                         'str_category': pd.Series(['foo', 'bar']).astype('category'),
                         'datetime_category': pd.Series(
                             [pd.Timestamp('20180310'), pd.Timestamp('20190910')]).astype('category'),
                         'nan': pd.Series([np.nan, np.nan]),
                         'none': pd.Series([None, None]),
                         'nat': pd.Series([pd.NaT, pd.NaT]),
                         'nan_category': pd.Series([np.nan, np.nan]).astype('category'),
                         'nat_category': pd.Series([pd.NaT, pd.NaT]).astype('category'),
                         'none_category': pd.Series([None, None]).astype('category'),
                         })


def data_frame_directory():
    dfd = DataFrameDirectory.create(df())
    dfd.schema_instance.score_column_names = {'score_column_type_1': 'int_category'}
    dfd.schema_instance.label_column_name = 'float_category'
    return dfd


@pytest.fixture(params=_get_column_selection_legacy_and_sdk_formats())
def column_selection_legacy_and_sdk_formats(request):
    return {
        "legacy_input": request.param[0],
        "sdk_input": request.param[1],
        "dfd": data_frame_directory(),
    }


"""
  Test read column of Int dtype.
"""


def _get_extended_int_dtype_test_samples():
    return [
        (pd.Series([1, np.nan], dtype="Int64"), "float64", pd.Series([1, np.nan])),
        (pd.Series([1, np.nan], dtype="Int32"), "float64", pd.Series([1, np.nan])),
        (pd.Series([1, np.nan], dtype="Int16"), "float64", pd.Series([1, np.nan])),
        (pd.Series([1, np.nan], dtype="Int8"), "float64", pd.Series([1, np.nan])),
        (pd.Series([1, np.nan], dtype="UInt8"), "float64", pd.Series([1, np.nan])),
        (pd.Series([1, np.nan], dtype="UInt16"), "float64", pd.Series([1, np.nan])),
        (pd.Series([1, np.nan], dtype="UInt32"), "float64", pd.Series([1, np.nan])),
        (pd.Series([1, np.nan], dtype="UInt64"), "float64", pd.Series([1, np.nan])),
        (pd.Series([np.nan, pd.NA, pd.NaT, None], dtype="Int64"), "float64",
         pd.Series([np.nan, np.nan, np.nan, np.nan])),
        (pd.Series([1, 2, 3], dtype="Int64"), "int64", pd.Series([1, 2, 3])),
    ]


@pytest.fixture(params=_get_extended_int_dtype_test_samples())
def get_extended_int_dtype_test_samples(request):
    return {
        "input_series": request.param[0],
        "expected_dtype": request.param[1],
        "expected_series": request.param[2],
    }
