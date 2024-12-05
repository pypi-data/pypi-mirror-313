# import copy
# import pandas as pd
# import numpy as np
# from pandas.api.types import is_categorical_dtype
# from pandas.core.dtypes.common import is_bool_dtype, is_integer_dtype, is_float_dtype, is_string_like_dtype

# from azureml.studio.common.libraryerror.library_error import KeyDoesNotExistError, DuplicatedNameError,\
#     ExistsNameError, ArgumentOutOfRangeError, ColumnIndexNotIntegerError, NotLabeledListError, InvalidKeyTypeError, \
#     ColumnNameNotStringError, InvalidScoreColumnSetterError, InvalidLabelColumnKeyTypeError, NotDataFrameError, \
#     ColumnTypeNotSeriesError, AttributesAndDataframeNotMatchError, NotColumnAttributeError, NotFeatureChannelError
# from azureml.studio.common.logger import time_profile
# from azureml.studio.common.utils.datetimeutils import is_datetime_dtype, is_timespan_dtype
# from azureml.studio.common.utils.missing_value_utils import drop_na
# from azureml.studio.modulehost.constants import ColumnTypeName, ElementTypeName


# class SchemaConstants:
#     TrueLabelType = 'True Labels'
#     ERROR_ACTION_RAISE = 'raise'


# class LabeledList:

#     def __init__(self):
#         self._index_to_name = list()
#         self._name_to_index = dict()
#         self._items = list()

#     @property
#     def names(self):
#         return self._index_to_name

#     def set_name(self, old_name, new_name):
#         if old_name not in self.names:
#             raise KeyDoesNotExistError('old_name', old_name)

#         if old_name == new_name:
#             raise DuplicatedNameError('new_name')

#         if new_name in self.names:
#             raise ExistsNameError('new_name', new_name)

#         index = self.get_index(old_name)
#         self._index_to_name[index] = new_name
#         self._name_to_index[new_name] = self._name_to_index[old_name]
#         del self._name_to_index[old_name]

#     def get_index(self, name):
#         if isinstance(name, list):
#             return [self._get_index(x) for x in name]
#         return self._get_index(name)

#     def _get_index(self, name):
#         if name in self._name_to_index:
#             return self._name_to_index[name]
#         raise KeyDoesNotExistError('name', name)

#     def get_name(self, index):
#         if isinstance(index, list):
#             return [self._get_name(x) for x in index]
#         return self._get_name(index)

#     def _get_name(self, index):
#         if isinstance(index, int):
#             if 0 <= index < len(self._index_to_name):
#                 return self._index_to_name[index]
#             raise ArgumentOutOfRangeError('index')
#         else:
#             raise ColumnIndexNotIntegerError('index', index)

#     def __getitem__(self, key):
#         self.validate_key(key)
#         if isinstance(key, str):
#             return self._items[self._name_to_index[key]]
#         return self._items[key]

#     def __setitem__(self, key, value):
#         self.validate_key(key)
#         if isinstance(key, str):
#             self._items[self._name_to_index[key]] = value
#         else:
#             self._items[key] = value

#     def append(self, name, item):
#         self.validate_name(name)
#         self._index_to_name.append(name)
#         self._update_name_to_index(len(self._index_to_name)-1)
#         self._items.append(item)

#     def remove(self, key):
#         self.validate_key(key)

#         if isinstance(key, int):
#             del self._index_to_name[key]
#             del self._items[key]
#             self._update_name_to_index(key)
#         else:
#             self._index_to_name.remove(key)
#             del self._items[self._name_to_index[key]]
#             self._update_name_to_index(self._name_to_index[key])

#     def _update_name_to_index(self, start_index):
#         for i in range(start_index, len(self._index_to_name)):
#             name = self._index_to_name[i]
#             self._name_to_index[name] = i

#     def __len__(self):
#         return len(self._index_to_name)

#     def __eq__(self, other):
#         if not isinstance(other, LabeledList):
#             raise NotLabeledListError('other')

#         return self.names == other.names and  \
#             all(self[x] == other[y] for x, y in zip(self.names, other.names))

#     def validate_key(self, key):
#         if isinstance(key, str):
#             if key not in self._name_to_index:
#                 raise KeyDoesNotExistError('key', key)
#         elif isinstance(key, int):
#             if not 0 <= key < len(self._items):
#                 raise ArgumentOutOfRangeError('key')
#         else:
#             raise InvalidKeyTypeError('key')

#     def validate_name(self, name):
#         if name in self._name_to_index:
#             raise ExistsNameError('name', name)

#         if not isinstance(name, str):
#             raise ColumnNameNotStringError('name', name)


# class DataTableSchema:
#     DEFAULT_LABEL_COLUMN_TYPE = SchemaConstants.TrueLabelType

#     def __init__(
#             self,
#             column_attributes: LabeledList,
#             score_column_names: dict = None,
#             label_column_name: dict = None,
#             feature_channels: dict = None):
#         """

#         :param column_attributes: a LabeledList
#         :param score_column_names: dict {<Score Column Type>: <Column Name>}
#         :param label_column_name: column name or dict {<Label Column Type>: <Column Name>}
#         :param feature_channels: dict {<Feature Name>： <FeatureChannel>}
#         """
#         self._column_attributes = column_attributes

#         # both self._score_columns and self._label_columns save column_index as the value rather than a column name
#         self._score_columns = dict()
#         self._label_columns = dict()

#         if score_column_names:
#             # Use score_column_name.setter to initialize self._score_columns
#             self.score_column_names = score_column_names

#         if label_column_name:
#             # Use label_column_name.setter to initialize self._label_columns
#             self.label_column_name = label_column_name

#         #  feature channel represents a group of DataTable
#         #  columns which can be operated on as a group.
#         self._feature_channels = feature_channels if feature_channels else dict()

#         # share some information between modules.
#         # like, indicating data table's type[ data set, scored data set, result report]
#         self._extended_properties = dict()

#     @property
#     def column_attributes(self):
#         return self._column_attributes

#     @property
#     def score_column_names(self):
#         """
#         Property method to get all Score column names
#         :return: Score column names
#         """
#         if not self._score_columns:
#             return dict()
#         return {col_type: self.column_attributes.get_name(col_index)
#                 for col_type, col_index in self._score_columns.items()}

#     @score_column_names.setter
#     def score_column_names(self, type_key_dict):
#         """
#         Setter method to initialize _score_columns from a dict {<Score Column Type>: <Column Name>}
#         :param type_key_dict: dict of Score column types to column name
#         :return:
#         """
#         if not isinstance(type_key_dict, dict):
#             raise InvalidScoreColumnSetterError('type_key_dict')

#         for col_type, col_key in type_key_dict.items():
#             self.validate_column_key(col_key)
#             col_index = self._get_column_index_by_key(col_key)
#             self._remove_from_label_score_feature(col_key)
#             self._score_columns.update({col_type: col_index})

#     @score_column_names.deleter
#     def score_column_names(self):
#         self._score_columns.clear()

#     @property
#     def label_column_name(self):
#         if not self._label_columns:
#             return None
# return
# self.column_attributes.get_name(list(self._label_columns.values())[0])

# @label_column_name.setter def label_column_name(self, col_key_or_type_key_dict): """ Setter method to initialize
# _label_columns from column name/index or a dict {<Label Column Type>: <Column Name>} When input is dict,
# only the first item will be applied :param col_key_or_type_key_dict: column name/index or a dict of Label column
# types to column name :return: """ if isinstance(col_key_or_type_key_dict, dict): col_type, col_key = list(
# col_key_or_type_key_dict.items())[0] elif isinstance(col_key_or_type_key_dict, int) or isinstance(
# col_key_or_type_key_dict, str): col_type = DataTableSchema.DEFAULT_LABEL_COLUMN_TYPE col_key =
# col_key_or_type_key_dict else: raise InvalidLabelColumnKeyTypeError(col_key_or_type_key_dict)

#         self.validate_column_key(col_key)
#         col_index = self._get_column_index_by_key(col_key)
#         self._remove_from_label_score_feature(col_index)
#         self._label_columns[col_type] = col_index

#     @label_column_name.deleter
#     def label_column_name(self):
#         self._label_columns.clear()

#     # Might need to be changed in the future
#     @property
#     def feature_channels(self):
#         return self._feature_channels

#     @feature_channels.setter
#     def feature_channels(self, value):
#         self._feature_channels.update(value)

#     @property
#     def extended_properties(self):
#         return self._extended_properties

#     @classmethod
#     def generate_column_attributes(cls, df):
#         if not isinstance(df, pd.DataFrame):
#             raise NotDataFrameError('df')

#         column_attributes = LabeledList()
#         for col_name in df.columns.tolist():
#             column_attribute = cls.generate_column_attribute(df[col_name], col_name)
#             column_attributes.append(col_name, column_attribute)
#         return column_attributes

#     @classmethod
#     def generate_column_attribute(cls, column, col_name):
#         (element_type, column_type) = cls.get_column_element_type(column)
#         return ColumnAttribute(col_name, column_type, element_type)

#     @classmethod
#     def get_column_element_type(cls, column):
#         # Note that integer column with missing values, eg. [1, 3, np.nan], will give ElementTypeName.FLOAT
#         if not isinstance(column, pd.Series):
#             raise ColumnTypeNotSeriesError('column')

#         if all(pd.isna(x) for x in column):
#             return ElementTypeName.NAN, ColumnTypeName.NAN

#         if is_categorical_dtype(column):
#             return ElementTypeName.CATEGORY, ColumnTypeName.CATEGORICAL
#         if is_datetime_dtype(column):
#             return ElementTypeName.DATETIME, ColumnTypeName.DATETIME
#         if is_timespan_dtype(column):
#             return ElementTypeName.TIMESPAN, ColumnTypeName.TIMESPAN
#         if is_bool_dtype(column):
#             return ElementTypeName.BOOL, ColumnTypeName.BINARY
#         if is_integer_dtype(column):
#             return ElementTypeName.INT, ColumnTypeName.NUMERIC
#         if is_float_dtype(column):
#             return ElementTypeName.FLOAT, ColumnTypeName.NUMERIC
#         if is_string_like_dtype(column):
#             return ElementTypeName.STRING, ColumnTypeName.STRING

#         return cls._dynamic_detect_element_type(column)

#     @classmethod
#     def _dynamic_detect_element_type(cls, column):
#         column_new = drop_na(column, include_inf=True)

#         # TODO: improve this part
#         # Currently, use the simple function to get better performance since it will be implemented by C
#         is_bool = 40
#         is_int = 30
#         is_float = 20
#         is_str = 10
#         is_object = 0

#         def detect(x):
#             if isinstance(x, bool):
#                 return is_bool
#             # np.int64 and np.int32 is not int type
#             elif isinstance(x, (int, np.int64, np.int32)):
#                 return is_int
#             elif isinstance(x, float):
#                 return is_float
#             elif isinstance(x, str):
#                 return is_str
#             else:
#                 return is_object
#         detected_type = min(detect(x) for x in column_new)

#         if detected_type is is_bool:
#             return ElementTypeName.BOOL, ColumnTypeName.BINARY
#         elif detected_type is is_int:
#             return ElementTypeName.INT, ColumnTypeName.NUMERIC
#         elif detected_type is is_float:
#             return ElementTypeName.FLOAT, ColumnTypeName.NUMERIC
#         elif detected_type is is_str:
#             return ElementTypeName.STRING, ColumnTypeName.STRING
#         else:
#             return ElementTypeName.OBJECT, ColumnTypeName.OBJECT

#     def set_column_attribute(self, col_key, column):
#         self.validate_column_key(col_key)

#         if not isinstance(column, pd.Series):
#             raise ColumnTypeNotSeriesError('column')
#         col_name = self._get_column_name_by_key(col_key)

#         self.column_attributes[col_key] = self.generate_column_attribute(column, col_name)

#     def set_extended_property(self, name, value):
#         self._extended_properties[name] = value

#     @time_profile
#     def validate(self, df):
#         # Zero row does not need to check
#         if df.shape[0] == 0:
#             return

#         column_attributes_by_df = self.generate_column_attributes(df)
#         if len(column_attributes_by_df) == len(self.column_attributes):
#             for column_index in range(len(column_attributes_by_df)):

#                 # NAN type matches with all type
#                 if column_attributes_by_df[column_index].element_type is ColumnTypeName.NAN:
#                     continue

#                 if column_attributes_by_df[column_index] != self.column_attributes[column_index]:
#                     raise AttributesAndDataframeNotMatchError('meta_data', 'df')
#             return

#         raise AttributesAndDataframeNotMatchError('meta_data', 'df')

#     def get_column_attribute(self, col_key):
#         self.validate_column_key(col_key)
#         return self.column_attributes[col_key]

#     def add_column_attribute(self, col_attribute):
#         self.column_attributes.validate_name(col_attribute.name)
#         self.column_attributes.append(col_attribute.name, col_attribute)

#     def set_column_name(self, col_key, new_col_name):
#         self.validate_column_key(col_key)
#         col_name = self._get_column_name_by_key(col_key)
#         self.column_attributes[col_key].name = new_col_name
#         self.column_attributes.set_name(col_name, new_col_name)
#         self._set_column_name_in_feature_channels(col_name, new_col_name)

#     def copy(self, if_clone=False):
#         if if_clone:
#             return copy.deepcopy(self)
#         return self

#     def set_column_as_feature(self, col_key):
#         self.validate_column_key(col_key)
#         col_index = self._get_column_index_by_key(col_key)

#         self._remove_from_label_score_feature(col_index)
#         self.get_column_attribute(col_index).is_feature = True

#     def select_columns(self, col_keys):
#         for col_key in col_keys:
#             self.validate_column_key(col_key)
#         col_indexes = [self._get_column_index_by_key(x) for x in col_keys]
#         col_names = [self._get_column_name_by_key(x) for x in col_keys]

#         selected_attributes = LabeledList()
#         for col_key in col_keys:
#             selected_attributes.append(self.column_attributes[col_key].name, self.column_attributes[col_key])

#         selected_label_columns = dict()
#         for label_type, label_index in self._label_columns.items():
#             if label_index in col_indexes:
#                 selected_label_columns[label_type] = col_indexes.index(label_index)

#         selected_score_columns = dict()
#         for score_type, score_index in self._score_columns.items():
#             if score_index in col_indexes:
#                 selected_score_columns[score_type] = col_indexes.index(score_index)

#         selected_feature_channels = dict()
#         for type_, channel in self._feature_channels.items():
#             if set(col_names) & set(channel.feature_column_names):
#                 new_col_names = col_names.copy()
#                 new_col_names = set(new_col_names).intersection(channel.feature_column_names)
#                 selected_feature_channels[type_] = FeatureChannel(
#                     channel.name, channel.is_normalized, new_col_names)

#         return DataTableSchema(column_attributes=selected_attributes,
#                                label_column_name=selected_label_columns,
#                                score_column_names=selected_score_columns,
#                                feature_channels=selected_feature_channels)

#     def validate_column_key(self, col_key):
#         self.column_attributes.validate_key(col_key)

#     def _get_column_name_by_key(self, col_key):
#         if isinstance(col_key, int):
#             return self.column_attributes.get_name(col_key)
#         return col_key

#     def _get_column_index_by_key(self, col_key):
#         if isinstance(col_key, int):
#             return col_key
#         return self.column_attributes.get_index(col_key)

#     def _remove_from_label_score_feature(self, col_index):
#         for k, v in self._label_columns.items():
#             if v == col_index:
#                 del self._label_columns[k]
#                 return

#         for k, v in self._score_columns.items():
#             if v == col_index:
#                 del self._score_columns[k]
#                 return

#         self.get_column_attribute(col_index).is_feature = False

#     def _set_column_name_in_feature_channels(self, col_name, new_col_name):
#         for key, value in self._feature_channels.items():
#             if col_name in value.feature_column_names:
#                 loc = value.feature_column_names.index(col_name)
#                 value.feature_column_names[loc] = new_col_name
#                 return


# class ColumnAttribute:
#     def __init__(self, name=None, column_type=None, element_type=None, is_feature=True):
#         self._name = name
#         self._column_type = column_type
#         self._is_feature = is_feature  # Need to be changed in the future
#         self._element_type = element_type

#     @property
#     def name(self):
#         return self._name

#     @name.setter
#     def name(self, value):
#         self._name = value

#     @property
#     def column_type(self):
#         return self._column_type

#     @property
#     def is_feature(self):
#         return self._is_feature

#     @is_feature.setter
#     def is_feature(self, value):
#         self._is_feature = value

#     @property
#     def element_type(self):
#         return self._element_type

#     def __eq__(self, other):
#         if not isinstance(other, ColumnAttribute):
#             raise NotColumnAttributeError('other')

#         return self.name == other.name and \
#             self.column_type == other.column_type and \
#             self.element_type == other.element_type


# class FeatureChannel:
#     def __init__(self, name=None, is_normalized=None, feature_column_names=None):
#         self._name = name
#         self._is_normalized = is_normalized
#         self._feature_column_names = feature_column_names

#     def __eq__(self, other):
#         if not isinstance(other, FeatureChannel):
#             raise NotFeatureChannelError('other')

#         return self.name == other.name and \
#             self.is_normalized == other.is_normalized and \
#             self.feature_column_names == other.feature_column_names

#     @property
#     def name(self):
#         return self._name

#     @name.setter
#     def name(self, value):
#         self._name = value

#     @property
#     def is_normalized(self):
#         return self._is_normalized

#     @property
#     def feature_column_names(self):
#         return self._feature_column_names
