import os
import pandas as pd
import numpy as np
from pandas.api.types import infer_dtype

from azureml.studio.common.datatable.data_table import DataTable
from azureml.studio.common.datatable.data_type_conversion import convert_column_by_element_type
from azureml.studio.common.datatypes import DataTypes
from azureml.studio.common.io.pickle_utils import write_with_pickle, read_with_pickle_from_file
from azureml.studio.core.io.data_frame_utils import data_frame_to_parquet, data_frame_from_parquet
from azureml.studio.core.logger import common_logger as log, TimeProfile
from azureml.studio.core.utils.fileutils import get_file_name
from azureml.studio.common.datatable.constants import ElementTypeName
from azureml.studio.core.utils.missing_value_utils import is_na
from azureml.studio.core.io.data_frame_directory import DataFrameDirectory
from azureml.studio.core.data_frame_schema import DataFrameSchema


_PARQUET_ENGINE = "pyarrow"
_PARQUET_EXTENSION = ".parquet"


def read_data_table(file_name):
    """
    Read DataTable from files
    :param file_name: the file_name should be ended with ".dataset.parquet"
    :return: DataTable
    """
    meta_data_file = get_meta_data_file_path(file_name)
    parquet_file = file_name

    # Raise error if both meta_data_file and parquet_file are missing
    if not os.path.isfile(meta_data_file) and not os.path.isfile(parquet_file):
        raise FileNotFoundError(f"Both meta data file {meta_data_file} "
                                f"and parquet file {parquet_file} are not found")

    # Warning if only parquet_file is missing
    if not os.path.isfile(parquet_file):
        log.warning(f"Parquet file not found: {parquet_file}. "
                    f"Will generate a zero-row DataFrame object from meta data")

    # Warning if only meta_data_file is missing
    if not os.path.isfile(meta_data_file):
        log.warning(f"Meta data file not found: {meta_data_file}. "
                    f"Will re-generate meta data from parquet file")
        meta_data = None
    else:
        meta_data = read_with_pickle_from_file(meta_data_file)

    with TimeProfile(f"Read data table from parquet file '{get_file_name(parquet_file)}'"):
        df = data_frame_from_parquet(parquet_file)
        # Fix bug: 445804
        if df.empty:
            log.warning(f"Generate DataFrame with the column names recorded from meta data")
            df = pd.DataFrame(columns=meta_data.column_attributes.names)
        log.info(f"Read data: Rows: {df.shape[0]}, Columns: {df.shape[1]}.")

        # A categorical-type column of all missing values will be non-categorical
        # when reading back from parquet. If so, then convert to categorical type
        for col_name in df.columns:
            if is_na(df[col_name]) \
                    and meta_data is not None \
                    and meta_data.get_element_type(col_name) == ElementTypeName.CATEGORY:
                df[col_name] = convert_column_by_element_type(df[col_name], ElementTypeName.CATEGORY)

        # This is to update column type in schema according to dataframe.
        if meta_data:
            DataFrameDirectory.update_schema_according_to_data(df, meta_data)
    return DataTable(df=df, meta_data=meta_data)


def write_data_table(dt: DataTable, file_name):
    """
    Write DataTable to files
    :param dt: the DataTable instance to be persisted
    :param file_name: the file_name should be ended with ".dataset.parquet"
    """
    write_data_table_meta_data_to_pickle(dt.meta_data, file_name)

    parquet_file = file_name

    with TimeProfile(f"Write to parquet file '{get_file_name(parquet_file)}'. "
                     f"Rows: {dt.data_frame.shape[0]}, Columns: {dt.data_frame.shape[1]}."):
        # Bug ID: 461519
        # Convert the column to the same type to avoid error when writing parquet.
        # Example 1: int, bool               =>   int
        # Example 2: int, bool, float        =>   float
        # Example 3: int, bool, float, str   =>   str
        # The type is detected in azureml.studio.core.data_frame_schema.ColumnAttribute._dynamic_detect_element_type
        for col_idx, column_name in enumerate(dt.column_names):
            element_type = dt.get_element_type(column_name)
            # UNCATEGORY are not defined in pandas and they will not cause the mixed column type error.
            if element_type == ElementTypeName.UNCATEGORY:
                continue

            column = dt.get_column(column_name)
            # If dtype is not object, the column must not be a mixed type column.
            if column.dtype != 'object':
                continue

            # If dtype is object but element type is bool,
            # it is the case that a bool column contains missing value.
            # In this case, one concern is that pd.NaT cannot be saved correctly,
            # thus we need to convert pd.NaT to np.nan by fillna for saving parquet correctly.
            if element_type == ElementTypeName.BOOL:
                if np.any(pd.isna(column)):
                    column.fillna(np.nan, inplace=True)
                continue

            try:
                if element_type == ElementTypeName.STRING:
                    # In this case, we need to make sure the column only contain string values to avoid saving bugs.
                    # By calling infer_dtype, we know whether the column only contain string values.
                    # If not all values are string, we need to convert the values to string.
                    if infer_dtype(column, skipna=True) != 'string':
                        dt.set_column_element_type(col_idx, element_type)
                else:
                    # Otherwise, the nan value is still nan value after astype.
                    # Here we don't update meta since we convert the type according to the type in meta.
                    if not dt.is_all_na_column(column_name):
                        dt.set_column(column_name, column.astype(element_type, copy=False), update_meta=False)
            except BaseException as e:
                raise TypeError(f'Cannot convert to type "{element_type}": {str(e)}') from e

        data_frame_to_parquet(dt.data_frame, parquet_file)


def get_meta_data_file_path(dataset_file_path: str):
    if dataset_file_path.endswith(DataTypes.DATASET.value.file_extension):
        return dataset_file_path[:-len(_PARQUET_EXTENSION)]
    else:
        raise ValueError(f"Invalid parquet file path: {dataset_file_path}")


def _get_legacy_parquet_file_path(dataset_file_path):
    base_name = os.path.basename(dataset_file_path)
    dir_name = os.path.dirname(dataset_file_path)
    return os.path.join(dir_name, f"{base_name}{_PARQUET_EXTENSION}")


def write_data_table_meta_data_to_pickle(meta_data: DataFrameSchema, data_file_path: str):
    meta_data_file = get_meta_data_file_path(data_file_path)
    with TimeProfile(f"Write pickle file '{get_file_name(meta_data_file)}'"):
        write_with_pickle(meta_data, meta_data_file)
