import copy
from functools import wraps

import pandas as pd
from more_itertools import first
from pandas.api.types import is_categorical_dtype
from pandas.core.dtypes.common import is_object_dtype

from azureml.studio.common.datatable.constants import ColumnTypeName, ElementTypeName
from azureml.studio.common.datatable.data_type_conversion import convert_column_by_element_type
from azureml.studio.common.error import ErrorMapping, NoColumnsSelectedError, ColumnNotFoundError, \
    InvalidColumnIndexRangeError, ColumnIndexParsingError, DuplicatedColumnNameError
from azureml.studio.core.data_frame_schema import DataFrameSchema
from azureml.studio.core.io.data_frame_directory import DataFrameDirectory
from azureml.studio.core.logger import time_profile, module_logger, common_logger
from azureml.studio.core.utils.column_selection import ColumnSelection, ColumnSelectionBuilder
from azureml.studio.core.utils.column_selection import ColumnSelectionColumnNotFoundError, \
    ColumnSelectionIndexParsingError, ColumnSelectionInvalidRuleSetError, ColumnSelectionIndexRangeError
from azureml.studio.core.utils.missing_value_utils import has_na, is_na, get_number_of_na
from azureml.studio.core.utils.strutils import generate_cls_str, quote


class DataTable:

    def __init__(self, df=pd.DataFrame(), meta_data=None):
        if not isinstance(df, pd.DataFrame):
            raise TypeError('Argument "df": Not Dataframe.')

        if meta_data is not None and not isinstance(meta_data, DataFrameSchema):
            raise TypeError('Argument "meta_data": Invalid metadata type.')

        self._meta_data = meta_data if meta_data else DataFrameSchema(
            column_attributes=DataFrameSchema.generate_column_attributes(df=df))

        self._data_frame = self._convert_by_meta_data(df)

        if meta_data is not None:
            meta_data.validate(self._data_frame)

        self._update_legacy_meta_data()
        self._name = None

    def _convert_by_meta_data(self, df):
        """
        Make sure DataFrame's dtype is consistent with meta data's column type
        """
        for column_name in df.columns:

            element_type = self.get_element_type(column_name)

            # A fix for bug 411124: if column type by meta data is numeric yet the dtype is object,
            # convert dtype of df.
            if self.get_column_type(column_name) == ColumnTypeName.NUMERIC and is_object_dtype(df[column_name].dtype) \
                    and not is_na(df[column_name]):
                module_logger.info(f'Convert column {column_name} to {element_type} type')
                new_column = convert_column_by_element_type(df[column_name], element_type)
                df[column_name] = new_column
                # Int column might be converted into float column, so change column attribute in meta data accordingly.
                if self.get_element_type(column_name) != new_column.dtype:
                    self.meta_data.set_column_attribute(column_name, new_column)

            # A fix for bug 400075: category dtype will be lost when reading DataFrame back from parquet
            if element_type == ElementTypeName.CATEGORY and not is_categorical_dtype(df[column_name].dtype):
                module_logger.info(f'Convert column {column_name} to {ElementTypeName.CATEGORY} type')
                df[column_name] = convert_column_by_element_type(df[column_name], ElementTypeName.CATEGORY)

        return df

    def _update_legacy_meta_data(self):
        for col_name in self.column_names:
            element_type = self.get_element_type(col_name)
            if element_type == ElementTypeName.NAN:
                self.meta_data.set_column_attribute(col_name, self.get_column(col_name))
                module_logger.warning(f'Type {ElementTypeName.NAN} has been deprecated. '
                                      f'Column "{col_name}" has values of {self.get_element_type(col_name)} type.')

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def number_of_columns(self):
        return self._data_frame.shape[1]

    @property
    def number_of_rows(self):
        return self._data_frame.shape[0]

    @property
    def data_frame(self):
        return self._data_frame

    @property
    def meta_data(self):
        return self._meta_data

    @property
    def column_names(self):
        return self.meta_data.column_attributes.names

    @property
    def element_types(self):
        return {name: self.get_element_type(name) for name in self.column_names}

    def __str__(self):
        name = quote(self.name)
        shape = f"({self.number_of_rows} Rows, {self.number_of_columns} Cols)"
        return generate_cls_str(self, name, shape)

    def get_meta_data(self, if_clone=True):
        return self._meta_data.copy(if_clone=if_clone)

    def get_data_frame(self, if_clone=True):
        return self._data_frame.copy(deep=if_clone)

    def get_column_index(self, col_name):
        return self._meta_data.get_column_index(col_name)

    def get_column_type(self, col_key):
        return self._meta_data.get_column_type(col_key)

    def get_element_type(self, col_key):
        return self._meta_data.get_element_type(col_key)

    def get_underlying_element_type(self, col_key):
        elm_type = self.meta_data.get_underlying_element_type(col_key)
        # This is for backward compatibility that in old meta_data, underlying element type doesn't exist.
        # So we need to infer the element type and update the meta_data.
        if elm_type == ElementTypeName.CATEGORY or elm_type is None:
            self.meta_data.infer_underlying_element_type(self.data_frame)
            elm_type = self.meta_data.get_underlying_element_type(col_key)
        return elm_type

    def get_column_name(self, col_index):
        return self._meta_data.get_column_name(col_index)

    def get_slice_by_column_indexes(self, column_indexes, if_clone=True):
        # Compute the duplicated column indexes and raise error when there are duplicated indexes.
        index_set = set()
        duplicated = filter(lambda x: x in index_set or index_set.add(x), column_indexes)
        first_duplicated_idx = first(duplicated, default=None)
        if first_duplicated_idx is not None:
            name = self.get_column_name(first_duplicated_idx)
            raise DuplicatedColumnNameError(duplicated_name=name, details="Duplicated columns are selected.")

        for col_index in column_indexes:
            self._validate_column_key(col_index)
        selected_columns = self._data_frame.iloc[:, column_indexes].copy(deep=if_clone)
        selected_meta_data = self.meta_data.select_columns(column_indexes).copy(if_clone=if_clone)
        return DataTable(df=selected_columns, meta_data=selected_meta_data)

    def remove_columns_by_indexes(self, remove_indexes_set):
        """Remove target columns by their indexes

        :param remove_indexes_set: set
        :return: DataTable
        """
        permuted_indexes = [col for col in range(self.number_of_columns) if col not in remove_indexes_set]
        return self.get_slice_by_column_indexes(permuted_indexes)

    def get_column(self, col_key):
        self._validate_column_key(col_key)
        if isinstance(col_key, str):
            return self.data_frame[col_key]
        return self.data_frame.iloc[:, col_key]

    def set_column(self, col_key, column, update_meta=True, strictly_match=True):
        """Update one column at col_key.

        :param col_key: Indicate which column should be set.
        :param column: The new column to be set, an array-like object is supported.
        :param update_meta: Indicate whether the meta should be updated.
                            In default, new meta should be computed since new column is set.
                            But if we could ensure the new column has the same type,
                            we could set update_meta=False to avoid the significant computation cost of computing meta.
        :param strictly_match: if true, the column length should be equal to self.number_of_rows
                               else the column would be set by indexes.
        """
        self._validate_column_key(col_key)

        if isinstance(col_key, int):
            col_key = self._data_frame.iloc[:, col_key].name

        if not isinstance(column, pd.Series):
            raise TypeError(f'Column "{col_key}": Column type is not Pandas.Series.')

        if strictly_match and len(column) != self.number_of_rows:
            raise ValueError(f'Argument "column": Row number does not match. '
                             f'Expected {self.number_of_rows}, got {len(column)}.')

        self._data_frame[col_key] = column

        if update_meta:
            self.meta_data.set_column_attribute(col_key, column)

    def upsert_column(self, col_name, column, strictly_match=True):
        """Add or set a column to the data table

        When col_name exists, update the column with set_column method.
        When col_name does not exist, add a new column to the data table.
        The length of column could not be different from the data_table, as long as an indexes is provided.

        :param col_name: str.
        :param column: pd.Series, new column
        :param strictly_match: if true, the column length should be equal to self.number_of_rows
                               else the column will be set by indexes.
        """

        if col_name in self.column_names:
            self.set_column(col_name, column, strictly_match=strictly_match)
        else:
            self.add_column(col_name, column)
        return self

    def add_column(self, col_name, column, is_feature=True):
        self._validate_column_name(col_name)

        if not isinstance(column, pd.Series):
            raise TypeError(f'Column "{col_name}": Column type is not Pandas.Series.')

        self._data_frame[col_name] = column
        new_attribute = \
            self.meta_data.generate_column_attribute(column, col_name, is_feature=is_feature)
        self.meta_data.add_column_attribute(new_attribute)

    def get_row(self, row_index):
        self._check_row_index(row_index)
        return self.data_frame.iloc[row_index, :]

    def remove_row(self, row_index):
        if isinstance(row_index, list):
            map(self._check_row_index, row_index)
        else:
            self._check_row_index(row_index)

        self._data_frame.drop(row_index, inplace=True)
        self._data_frame.reset_index(drop=True, inplace=True)

    def get_number_of_missing_value(self, col_key):
        self._validate_column_key(col_key)
        return get_number_of_na(self.get_column(col_key))

    def has_na(self, col_keys=None, include_inf=False):
        """Determine if the specified sub-datatable has NaN

        :param col_keys: List-like obj, if None is given, all columns would be took into consideration.
        :return: True if the sub-datatable has NaN.
        """
        if isinstance(col_keys, str):
            raise TypeError("col_keys should be an iterable value or None.")
        if col_keys is None:
            col_keys = self.column_names
        return any(has_na(self.get_column(x), include_inf) for x in col_keys)

    def is_all_na_column(self, col_key):
        """Determine if a column has all nan values."""
        self._validate_column_key(col_key)
        return is_na(self.get_column(col_key))

    @time_profile
    def clone(self):
        return copy.deepcopy(self)

    def rename_column(self, col_key, new_col_name):
        if isinstance(col_key, str):
            column_name = col_key
        elif isinstance(col_key, int):
            column_name = self.get_column_name(col_key)
        else:
            raise KeyError('Invalid column key type.')

        self.meta_data.set_column_name(column_name, new_col_name)
        self._data_frame.rename(columns={column_name: new_col_name}, inplace=True)

    def reset_data_frame_index(self):
        self._data_frame.reset_index(drop=True, inplace=True)

    def _check_row_index(self, row_index):

        if not isinstance(row_index, int):
            raise TypeError(f'Argument "row_index": Row index "{row_index}" is not an integer type.')

        if not 0 <= row_index < self.number_of_rows:
            raise KeyError(f'Argument "row_index" is out of range from 0 to {self.number_of_rows - 1}.')

    def set_column_element_type(self, col_index, new_type, date_time_format=None, time_span_format=None):
        column = self.get_column(col_index)
        column_new = convert_column_by_element_type(column, new_type, date_time_format, time_span_format)
        old_type = self.get_element_type(col_index)
        self.set_column(col_index, column_new, update_meta=(old_type != new_type))

    def contains_column(self, col_name):
        return col_name in self.column_names

    def _validate_column_key(self, col_key):
        self.meta_data.column_attributes.validate_key(col_key)

    def _validate_column_name(self, col_name):
        self.meta_data.column_attributes.validate_name(col_name)

    def clear_features(self, col_indices):
        for col_index in col_indices:
            self.meta_data.get_column_attribute(col_index).is_feature = False

    def __eq__(self, other):
        if not self.data_frame.equals(other.data_frame):
            return False
        # Todo: Use self.meta_data == other.meta_data after meta_data is updated.
        return self.meta_data.column_attributes == other.meta_data.column_attributes

    @staticmethod
    def from_dfd(directory: DataFrameDirectory, data_table_meta=None):
        if not isinstance(directory, DataFrameDirectory):
            raise TypeError(f"Expected type is {DataFrameDirectory.__name__}, got {directory.__class__.__name__}")
        # If data_table_meta is provided, initialize DataTable with it
        if data_table_meta is not None:
            return DataTable(directory.data, data_table_meta)
        # If schema is in the directory, initialize DataTable with it
        elif directory.schema_data is not None:
            data_table_meta = DataFrameSchema.from_dict(directory.schema_data)
            common_logger.debug(f"Load schema successfully.")
            return DataTable(directory.data, data_table_meta)
        # Otherwise, initialize DataTable with the data directly
        common_logger.info(f"Load datatable without schema.")
        return DataTable(directory.data)

    @classmethod
    def from_raw_parquet(cls, load_from_dir: str):
        directory = DataFrameDirectory.load_raw_parquet(load_from_dir)
        return DataTable.from_dfd(directory)

    def get_samples(self):
        return DataFrameDirectory(data=self.data_frame, schema=self.meta_data).get_samples()


def column_selection_error_handling(func):
    @wraps(func)
    def new_func(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ColumnSelectionColumnNotFoundError as err:
            ErrorMapping.rethrow(err, ColumnNotFoundError(column_id=err.column_index))
        except ColumnSelectionIndexRangeError as err:
            ErrorMapping.rethrow(err, InvalidColumnIndexRangeError(column_range=err.column_range))
        except ColumnSelectionIndexParsingError as err:
            ErrorMapping.rethrow(err, ColumnIndexParsingError(column_index_or_range=err.column_index_or_range))

    return new_func


class DataTableColumnSelection(ColumnSelection):

    def __init__(self, json_query=None, dict_rule_set=None):
        try:
            super().__init__(json_query, dict_rule_set)
        except ColumnSelectionInvalidRuleSetError as err:
            ErrorMapping.rethrow(err, NoColumnsSelectedError())

    def select(self, dt: DataTable, if_clone=True):
        included_column_indexes = self.select_column_indexes(dt)
        return dt.get_slice_by_column_indexes(included_column_indexes, if_clone)

    @column_selection_error_handling
    def select_column_indexes(self, dt: DataTable):
        return super().select_column_indexes(dt.data_frame, schema=dt.meta_data)


class DataTableColumnSelectionBuilder(ColumnSelectionBuilder):

    def build(self):
        return DataTableColumnSelection(dict_rule_set=self._obj)


def set_empty_columns_to_str_type(dt: DataTable):
    for col_name in dt.column_names:
        if dt.is_all_na_column(col_name) and dt.get_element_type(col_name) != ElementTypeName.STRING:
            dt.set_column_element_type(col_name, ElementTypeName.STRING)
