import copy

import numpy as np
import pandas as pd
from pandas.api.types import infer_dtype
from pandas.core.dtypes.common import is_bool_dtype, is_integer_dtype, is_float_dtype, is_string_like_dtype
from pandas.core.dtypes.common import is_categorical_dtype, is_datetime64_ns_dtype, is_timedelta64_ns_dtype

from azureml.studio.core.schema import Schema, ColumnAttribute, ColumnTypeName, ElementTypeName
from azureml.studio.core.error import DataFrameSchemaValidationError
from azureml.studio.core.utils.labeled_list import LabeledList
from azureml.studio.core.utils.missing_value_utils import drop_na, is_na
from azureml.studio.core.utils.strutils import to_snake_case
from azureml.studio.core.logger import common_logger


# This mapping is used for detecting column types with infer_dtype
PANDAS_INFER_MAPPING = {
    'string': (ElementTypeName.STRING, ColumnTypeName.STRING),
}


class SchemaConstants:
    TrueLabelType = 'True Labels'
    ERROR_ACTION_RAISE = 'raise'


class DataFrameSchema(Schema):

    def __init__(
            self,
            column_attributes: LabeledList,
            score_column_names: dict = {},
            label_column_name: dict = {},
            feature_channels: dict = None,
            extended_properties: dict = None,
    ):
        """

        :param column_attributes:  a LabeledList
        :param score_column_names: dict {<Score Column Type>: <Column Name>}
        :param label_column_name: column name or dict {<Label Column Type>: <Column Name>}
        :param feature_channels: dict {<Feature Name>: <FeatureChannel>}
        :param extended_properties: an extensible property set
        """
        super().__init__(column_attributes)

        # both self._score_columns and self._label_columns save column_index as the value rather than a column name
        self._score_columns = {}
        self._label_columns = {}

        if score_column_names:
            # Use score_column_name.setter to initialize self._score_column_names
            self.score_column_names = score_column_names

        if label_column_name:
            # Use label_column_name.setter to initialize self._label_column_name
            self.label_column_name = label_column_name

        #  feature channel represents a group of DataTable
        #  columns which can be operated on as a group.
        self._feature_channels = feature_channels if feature_channels else {}

        # share some information between modules.
        # like, indicating data table's type[ data set, scored data set, result report]
        self._extended_properties = extended_properties if extended_properties else {}

    @property
    def score_column_names(self):
        """
        Property method to get all Score column names
        :return: Score column names
        """
        if not self._score_columns:
            return dict()
        return {col_type: self._get_column_name_by_key(col_index)
                for col_type, col_index in self._score_columns.items()}

    @score_column_names.setter
    def score_column_names(self, type_key_dict):
        """
        Setter method to initialize _score_columns from a dict {<Score Column Type>: <Column Name>}
        :param type_key_dict: dict of Score column types to column name
        :return:
        """
        if not isinstance(type_key_dict, dict):
            raise TypeError(f'Argument "type_key_dict": Score column must be set by a dictionary.')

        for col_type, col_key in type_key_dict.items():
            col_index = self._get_column_index_by_key(col_key)
            self._remove_from_label_score_feature(col_index)
            self._score_columns.update({col_type: col_index})

    @score_column_names.deleter
    def score_column_names(self):
        self._score_columns.clear()

    @property
    def label_column_name(self):
        if not self._label_columns:
            return None
        return self._get_column_name_by_key(list(self._label_columns.values())[0])

    @label_column_name.setter
    def label_column_name(self, col_key_or_type_key_dict):
        """
        Setter method to initialize _label_column_name from column name/index or a dict
        {<Label Column Type>: <Column Name>} When input is dict, only the first item will be applied
        :param col_key_or_type_key_dict: column name/index or a dict of Label column types to column name
        :return:
        """
        if isinstance(col_key_or_type_key_dict, dict):
            if col_key_or_type_key_dict:
                col_type, col_key = list(col_key_or_type_key_dict.items())[0]
            else:
                return
        elif isinstance(col_key_or_type_key_dict, int) or isinstance(col_key_or_type_key_dict, str):
            col_type = SchemaConstants.TrueLabelType
            col_key = col_key_or_type_key_dict
        else:
            raise TypeError(f'Argument "col_key_or_type_key_dict": Label column must be set by a dictionary or'
                            f' by column name or index.')

        col_index = self._get_column_index_by_key(col_key)
        self._remove_from_label_score_feature(col_index)
        self._label_columns[col_type] = col_index

    @label_column_name.deleter
    def label_column_name(self):
        self._label_columns.clear()

    # Might need to be changed in the future
    @property
    def feature_channels(self):
        return self._feature_channels

    @feature_channels.setter
    def feature_channels(self, value):
        self._feature_channels.update(value)

    @property
    def extended_properties(self):
        return self._extended_properties

    def get_feature_type(self, col_name):
        if self.column_attributes[col_name].is_feature:
            return 'Feature'
        elif col_name == self.label_column_name:
            return 'Label'
        # Here values are the score_column_names, the keys are used to indicate different score types.
        elif col_name in self.score_column_names.values():
            return 'Score'
        return None

    def get_column_index(self, col_name):
        return self.column_attributes.get_index(col_name)

    def get_column_type(self, col_key):
        return self.column_attributes[col_key].column_type

    def get_element_type(self, col_key):
        return self.column_attributes[col_key].element_type

    def get_underlying_element_type(self, col_key):
        return self.column_attributes[col_key].underlying_element_type

    def get_column_name(self, col_index):
        if not isinstance(col_index, int):
            raise TypeError(f'Argument "col_index": Column index "{col_index}" is not an integer type.')

        self.column_attributes.validate_key(col_index)
        return self.column_attributes.get_name(col_index)

    def to_dict(self):
        # Exclude "extended_properties" because "extended_properties" is not always json-serializable.
        return {
            'columnAttributes': self.column_attributes.to_list(),
            'featureChannels': [val.to_dict() for val in self.feature_channels.values()],
            'labelColumns': {col_type: self.column_attributes.names[col_index]
                             for col_type, col_index in self._label_columns.items()},
            'scoreColumns': self.score_column_names,
        }

    @classmethod
    def generate_column_attributes(cls, df: pd.DataFrame):
        if not isinstance(df, pd.DataFrame):
            raise TypeError('Argument "df": Not Dataframe.')

        return LabeledList.from_items(
            (cls.generate_column_attribute(df.iloc[:, idx], col) for idx, col in enumerate(df.columns))
        )

    @classmethod
    def generate_column_attribute(cls, column, col_name, is_feature=True):
        element_type, column_type = cls.get_column_element_type(column)
        underlying_element_type, _ = None, None
        if element_type == ElementTypeName.CATEGORY:
            # Once it is a categorical column, we then check its undelying column type.
            # Since it is categorical, the cost of the method would be at most O(# of categories).
            underlying_element_type, _ = cls.get_underlying_column_element_type(column)
        return ColumnAttribute(
            name=col_name,
            column_type=column_type,
            element_type=element_type,
            is_feature=is_feature,
            underlying_element_type=underlying_element_type,
        )

    def infer_underlying_element_type(self, df: pd.DataFrame):
        for i, attr in enumerate(self.column_attributes):
            if attr.name not in df.columns:
                raise ValueError(f"Invalid dataframe: column '{attr.name}'' is not in the dataframe.")
            if attr.element_type != ElementTypeName.CATEGORY:
                continue
            # If underlying_element_type has been inferred, pass.
            if attr.underlying_element_type:
                continue
            # Here we reuse the element_type of the original Attribute,
            # since it is costly to call generate_column_attribute and scan the whole column.
            # we only need to scan the category values which is much cheaper.
            elm_type, _ = self.get_underlying_column_element_type(df[attr.name])
            self.column_attributes[i] = ColumnAttribute(
                name=attr.name, column_type=attr.column_type, element_type=attr.element_type,
                is_feature=attr.is_feature, properties=attr.properties,
                underlying_element_type=elm_type,
            )

    @classmethod
    def get_underlying_series_of_categorical(cls, column: pd.Series):
        """Get the underlying series for checking the underlying dtype of the column.
        For a categorical column, return its categories, otherwise return itself.
        """
        # Special handling of column of all missing values
        if is_na(column) and is_categorical_dtype(column):
            # Convert column to numpy.array to drop the categorical type
            return pd.Series(np.asarray(column))
        return pd.Series(column.dtype.categories).infer_objects() if is_categorical_dtype(column) else column

    @classmethod
    def get_underlying_column_element_type(cls, column: pd.Series):
        """By calling get_underlying_series_of_categorical,
        a categorical column with length n will return a series with length c,
        while c is much smaller than n, so it would be much faster to compute the type.
        """
        return cls.get_column_element_type(cls.get_underlying_series_of_categorical(column))

    @classmethod
    def get_column_element_type(cls, column, col_name=None):
        """Get the type of the column,
        It costs O(n) to check if it is NA,
        O(1) to check its dtype, most types could be returned here,
        O(n) to dynamicly check the type by scanning all the items.
        """
        # Note that integer column with missing values, eg. [1, 3, np.nan], will give ElementTypeName.FLOAT
        if not isinstance(column, pd.Series):
            raise TypeError(f'Column "{col_name}": Column type is not Pandas.Series.')

        if column.empty:
            return ElementTypeName.OBJECT, ColumnTypeName.OBJECT

        if is_categorical_dtype(column):
            return ElementTypeName.CATEGORY, ColumnTypeName.CATEGORICAL
        if is_datetime64_ns_dtype(column):
            return ElementTypeName.DATETIME, ColumnTypeName.DATETIME
        if is_timedelta64_ns_dtype(column):
            return ElementTypeName.TIMESPAN, ColumnTypeName.TIMESPAN
        if is_bool_dtype(column):
            return ElementTypeName.BOOL, ColumnTypeName.BINARY
        if is_integer_dtype(column):
            return ElementTypeName.INT, ColumnTypeName.NUMERIC
        if is_float_dtype(column):
            return ElementTypeName.FLOAT, ColumnTypeName.NUMERIC
        if is_string_like_dtype(column):
            return ElementTypeName.STRING, ColumnTypeName.STRING

        return cls._dynamic_detect_element_type(column)

    @classmethod
    def _dynamic_detect_element_type(cls, column):
        # Currently, only the column with object dtype will call this method.
        # Most cases are string columns so infer_dtype could give a valid element type.
        # Only mixed typed column need further investigate.
        # infer_dtype is implemented by C and only goes through the values one time,
        # which is more efficient than dropna().apply(type).unique()
        dtype = infer_dtype(column, skipna=True)
        if dtype in PANDAS_INFER_MAPPING:
            return PANDAS_INFER_MAPPING[dtype]

        # Calling column.apply(type).unique() to reduce cost when detecting type.
        # It doesn't introduce much cost since apply, type, unique are all implemented in C.
        column_new = drop_na(column).apply(type).unique()

        # Column with all missing values such as np.nan, None, pd.NaT
        if not len(column_new):
            unique_values = column.unique()
            if any(e is pd.NaT for e in unique_values):
                return ElementTypeName.DATETIME, ColumnTypeName.DATETIME
            if None in unique_values:
                return ElementTypeName.STRING, ColumnTypeName.STRING
            return ElementTypeName.FLOAT, ColumnTypeName.NUMERIC

        # TODO: improve this part
        # Currently, use the simple function to get better performance since it will be implemented by C
        is_bool = 40
        is_int = 30
        is_float = 20
        is_str = 10
        is_object = 0

        def detect(x):
            if x == bool:
                return is_bool
            # np.int64 and np.int32 is not int type
            elif x in {int, np.int64, np.int32}:
                return is_int
            elif x == float:
                return is_float
            elif x == str:
                return is_str
            else:
                return is_object

        detected_type = min(detect(x) for x in column_new)

        if detected_type is is_bool:
            return ElementTypeName.BOOL, ColumnTypeName.BINARY
        elif detected_type is is_int:
            return ElementTypeName.INT, ColumnTypeName.NUMERIC
        elif detected_type is is_float:
            return ElementTypeName.FLOAT, ColumnTypeName.NUMERIC
        elif detected_type is is_str:
            return ElementTypeName.STRING, ColumnTypeName.STRING
        else:
            return ElementTypeName.OBJECT, ColumnTypeName.OBJECT

    def set_extended_property(self, name, value):
        self._extended_properties[name] = value

    def validate(self, df: pd.DataFrame):
        expected_names = self.column_attributes.names
        nrows, ncols = df.shape

        # Check column count
        if ncols != len(expected_names):
            raise DataFrameSchemaValidationError(f"the expected column count is {len(expected_names)}, got {ncols}")

        # Check column names
        for i, col in enumerate(df.columns):
            if col != expected_names[i]:
                raise DataFrameSchemaValidationError(
                    f"the expected name of column {i} is '{expected_names[i]}', got '{col}'")

        # For zero-row df, there is no need to check type.
        if nrows == 0:
            return

        # Check column types
        for i, col in enumerate(df.columns):
            element_type, _ = self.get_column_element_type(df[col])
            expected_type = self.column_attributes[i].element_type

            if expected_type == ElementTypeName.NAN:
                common_logger.warning(f'Column "{df.columns[i]}" has values of {ElementTypeName.NAN} type, '
                                      f' which is now deprecated.')
                continue

            if is_na(df[col]):
                # Skip validation for column of all missing values
                continue

            # If element_type is NAN, we don't raise exception,
            # because by design NAN could represent any type of value.
            if element_type != expected_type:
                raise DataFrameSchemaValidationError(
                    f"the expected type of column '{col}' is '{expected_type}', got '{element_type}'"
                )

    def set_column_attribute(self, col_key, column):
        col_name = self._get_column_name_by_key(col_key)
        DataFrameSchema._validate_column_type(column, col_name)

        self.column_attributes[col_key] = self.generate_column_attribute(
            column=column,
            col_name=col_name,
            # Keep is_feature attribute
            is_feature=self.column_attributes[col_key].is_feature
        )

    def get_column_attribute(self, col_key):
        return self.column_attributes[col_key]

    def add_column_attribute(self, col_attribute):
        self.column_attributes.validate_name(col_attribute.name)
        self.column_attributes.append(col_attribute.name, col_attribute)

    def set_column_name(self, col_key, new_col_name):
        col_name = self._get_column_name_by_key(col_key)
        self.column_attributes[col_key].name = new_col_name
        self.column_attributes.set_name(col_name, new_col_name)
        self._set_column_name_in_feature_channels(col_name, new_col_name)

    def copy(self, if_clone=False):
        if if_clone:
            return copy.deepcopy(self)
        return self

    def set_column_as_feature(self, col_key):
        # convert column key to column index for the requirement of _remove_from_label_score_feature
        col_idx = self._get_column_index_by_key(col_key)

        self._remove_from_label_score_feature(col_idx)
        self.get_column_attribute(col_idx).is_feature = True

    def select_columns(self, col_keys):
        column_attributes = LabeledList.from_items((self.column_attributes[i] for i in col_keys))

        col_indexes = [self._get_column_index_by_key(x) for x in col_keys]
        score_column_names = {score_type: self._get_column_name_by_key(col_index)
                              for score_type, col_index in self._score_columns.items()
                              if col_index in col_indexes}

        label_column_name = {label_type: self._get_column_name_by_key(col_index)
                             for label_type, col_index in self._label_columns.items()
                             if col_index in col_indexes}

        feature_channels = {}
        col_names_set = set(col_indexes)
        for feature_type, channel in self._feature_channels.items():
            selected_col_names = col_names_set.intersection(channel.feature_column_names)
            if selected_col_names:
                feature_channels[feature_type] = FeatureChannel(
                    channel.name, channel.is_normalized, selected_col_names)

        return DataFrameSchema(
            column_attributes=column_attributes,
            score_column_names=score_column_names,
            label_column_name=label_column_name,
            feature_channels=feature_channels,
            extended_properties=self.extended_properties,
        )

    def _get_column_name_by_key(self, col_key):
        if isinstance(col_key, int):
            return self.column_attributes.get_name(col_key)
        return col_key

    def _get_column_index_by_key(self, col_key):
        if isinstance(col_key, int):
            return col_key
        return self.column_attributes.get_index(col_key)

    def _remove_from_label_score_feature(self, col_index: int):
        """Remove a feature column from label column and score columns

        :param col_index: int, it must be the index of the selected column, since the values of _label_columns and
        score_columns is column index.
        :return:
        """
        for k, v in self._label_columns.items():
            if v == col_index:
                del self._label_columns[k]
                return

        for k, v in self._score_columns.items():
            if v == col_index:
                del self._score_columns[k]
                return

        self.get_column_attribute(col_index).is_feature = False

    def _set_column_name_in_feature_channels(self, col_name, new_col_name):
        for key, value in self._feature_channels.items():
            if col_name in value.feature_column_names:
                loc = value.feature_column_names.index(col_name)
                value.feature_column_names[loc] = new_col_name
                return

    @staticmethod
    def from_dict(schema_data):
        # Exclude "extended_properties" because "extended_properties" is also excluded in "to_dict" method.
        return DataFrameSchema(
            column_attributes=LabeledList.from_list(schema_data['columnAttributes'], ColumnAttribute),
            feature_channels={
                val['name']: FeatureChannel.from_dict(val) for val in schema_data['featureChannels']
            },
            label_column_name=schema_data['labelColumns'],
            score_column_names=schema_data['scoreColumns'],
        )

    @staticmethod
    def from_data_frame(df: pd.DataFrame):
        return DataFrameSchema(DataFrameSchema.generate_column_attributes(df=df))

    @staticmethod
    def data_frame_to_dict(df: pd.DataFrame):
        return DataFrameSchema.from_data_frame(df).to_dict()

    @staticmethod
    def _validate_column_type(column, col_name):
        if not isinstance(column, pd.Series):
            raise TypeError(f'Column "{col_name}": Column type is not Pandas.Series.')


class FeatureChannel():
    def __init__(self, name=None, is_normalized=None, feature_column_names=None):
        self._name = name
        self._is_normalized = is_normalized
        self._feature_column_names = feature_column_names

    def __eq__(self, other):
        if not isinstance(other, FeatureChannel):
            raise TypeError('Argument "other": Not feature channel.')

        return self.name == other.name and \
            self.is_normalized == other.is_normalized and \
            self.feature_column_names == other.feature_column_names

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def is_normalized(self):
        return self._is_normalized

    @property
    def feature_column_names(self):
        return self._feature_column_names

    def to_dict(self):
        result = {
            'name': self.name,
            'isNormalized': self.is_normalized,
            'featureColumns': self.feature_column_names
        }

        return result

    @classmethod
    def from_dict(cls, kvs):
        kvs = kvs.copy()
        kvs['featureColumnNames'] = kvs.pop('featureColumns')
        return cls(**{to_snake_case(key): val for key, val in kvs.items()})
