from azureml.studio.core.utils.labeled_list import LabeledList


class ColumnTypeName:
    NUMERIC = 'Numeric'
    STRING = 'String'
    BINARY = 'Binary'
    OBJECT = 'Object'
    CATEGORICAL = 'Categorical'
    DATETIME = 'DateTime'
    TIMESPAN = 'TimeSpan'
    # NAN type is deprecated! Do not use it!
    NAN = 'NAN'

    BYTES = 'Bytes'


class ElementTypeName:
    INT = 'int64'
    FLOAT = 'float64'
    STRING = 'str'
    BOOL = 'bool'
    OBJECT = 'object'
    CATEGORY = 'category'
    DATETIME = 'datetime64'
    TIMESPAN = 'timedelta64'
    # NAN type is deprecated! Do not use it!
    NAN = 'NAN'

    BYTES = 'bytes'
    UNCATEGORY = 'uncategory'
    CONVERTABLE_LIST = [INT, FLOAT, STRING, BOOL, OBJECT, CATEGORY]
    NUMERIC_LIST = [INT, FLOAT, BOOL]

    UNDERLYING_LIST = {INT, FLOAT, STRING, BOOL, OBJECT, DATETIME, TIMESPAN, NAN, BYTES}


class Schema:
    def __init__(self, column_attributes: LabeledList):
        """

        :param column_attributes:  a LabeledList which indicates the attributes of all columns.
        """
        self._column_attributes = column_attributes

    @property
    def column_attributes(self):
        return self._column_attributes

    def to_dict(self):
        return {
            'columnAttributes': self.column_attributes.to_list(),
        }

    @classmethod
    def from_dict(cls, schema_data):
        return cls(column_attributes=LabeledList.from_list(schema_data['columnAttributes'], ColumnAttribute))

    def __eq__(self, other):
        return isinstance(other, Schema) and self.to_dict() == other.to_dict()


class ColumnAttribute:
    def __init__(self, name=None, column_type=None, element_type=None, is_feature=True,
                 properties=None,
                 underlying_element_type=None,
                 ):
        self._properties = properties if properties else {}
        self._name = name
        self._column_type = column_type
        self._is_feature = is_feature  # Need to be changed in the future
        self._element_type = element_type

        self._underlying_element_type = None
        # Use setter to set the underlying element type to make sure it is set correctly.
        if underlying_element_type:
            self.underlying_element_type = underlying_element_type

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def column_type(self):
        return self._column_type

    @column_type.setter
    def column_type(self, value):
        self._column_type = value

    @property
    def is_feature(self):
        return self._is_feature

    @is_feature.setter
    def is_feature(self, value):
        self._is_feature = value

    @property
    def element_type(self):
        return self._element_type

    @element_type.setter
    def element_type(self, value):
        self._element_type = value

    @property
    def properties(self):
        # This is for backward compatibility that loading old pickled data do not have _properties
        return self._properties if hasattr(self, '_properties') else {}

    @property
    def underlying_element_type(self):
        # If element_type is not category, return the real element_type, otherwise use _underlying_element_type
        if self._element_type != ElementTypeName.CATEGORY:
            return self._element_type
        # Use hasattr for backward compatibility that old pickled data do not have _underlying_element_type
        return self._underlying_element_type \
            if hasattr(self, '_underlying_element_type') and self._underlying_element_type \
            else None

    @underlying_element_type.setter
    def underlying_element_type(self, element_type):
        if self.element_type != ElementTypeName.CATEGORY:
            raise ValueError(f"Cannot set underlying element type for a non category column.")
        if element_type not in ElementTypeName.UNDERLYING_LIST:
            raise ValueError(f"Invalid underlying element type '{element_type}'. "
                             f"Valid types are: {', '.join(ElementTypeName.UNDERLYING_LIST)}")
        self._underlying_element_type = element_type

    def __eq__(self, other):
        return isinstance(other, ColumnAttribute) and \
            self.name == other.name and \
            self.column_type == other.column_type and \
            self.element_type == other.element_type and \
            self.properties == other.properties and \
            self.underlying_element_type == other.underlying_element_type

    def to_dict(self):
        # The dict structure follows v1 behavior.
        result = {
            'name': self.name,
            'type': self.column_type,
            'isFeature': self.is_feature,
            'elementType': {'typeName': self.element_type, "isNullable": False},
        }
        if self.properties:
            result['properties'] = self.properties
        if self.element_type == ElementTypeName.CATEGORY:
            result['underlyingElementType'] = self.underlying_element_type
        return result

    @classmethod
    def from_dict(cls, kvs):
        # The dict structure follows v1 behavior.
        return cls(
            name=kvs['name'], column_type=kvs['type'],
            element_type=kvs['elementType']['typeName'], is_feature=kvs.get('isFeature', True),
            properties=kvs.get('properties'),
            underlying_element_type=kvs.get('underlyingElementType')
        )
