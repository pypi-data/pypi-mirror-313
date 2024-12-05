import pandas as pd
from enum import Enum
import chardet
import os
from pathlib import PurePath

from pandas.core.dtypes.common import is_object_dtype

from azureml.studio.common.datatable.data_table import DataTable
from azureml.studio.common.datatypes import DataTypes
from azureml.studio.core.logger import TimeProfile, time_profile, module_logger
from azureml.studio.common.error import ErrorMapping, FileParsingFailedError, ColumnCountNotEqualError, MixedColumnError


class DataTableCsvSep(Enum):
    CSV = ','
    TSV = '\t'


class DataTableCsvReader:
    DEFAULT_CHARDET_BYTES = 1 * 1024 * 1024  # 1Mb

    @staticmethod
    @time_profile
    def read(filepath_or_buffer, sep: DataTableCsvSep, has_header: bool):
        df = DataTableCsvReader.read_as_data_frame(
            filepath_or_buffer=filepath_or_buffer,
            sep=sep,
            has_header=has_header
        )

        if has_header:
            # Pandas will trim the space for values automatically
            # We need to trim the column name by manual
            DataTableCsvReader._trim_column_names(df)

        with TimeProfile("DataTable Construction"):
            dt = DataTable(df=df)

        return dt

    @classmethod
    @time_profile
    def read_csv_files(cls, directory_path, sep: DataTableCsvSep = DataTableCsvSep.CSV, has_header: bool = True):

        file_list = [os.path.join(directory_path, f) for f in os.listdir(directory_path)]
        if not file_list:
            return DataTable()
        df_list = list()
        # To make sure the output dataframe has a fixed row order
        file_list.sort()
        for file in file_list:
            df = cls.read_as_data_frame(file, sep, has_header)
            df_list.append(df)

        try:
            with TimeProfile("Dataframe chunks concat"):
                df = pd.concat(df_list, ignore_index=True)
                return DataTable(df)
        except BaseException as ex:
            ErrorMapping.rethrow(
                e=ex,
                err=FileParsingFailedError(
                    file_format=DataTypes.GENERIC_CSV.value.file_extension,
                    failure_reason=str(ex)))

    @staticmethod
    @time_profile
    def read_as_data_frame(filepath_or_buffer, sep: DataTableCsvSep, has_header: bool, chunk_size=50000):
        """

        :param filepath_or_buffer: filepath or buffer used to read data
        :param sep: sep of CSV or TSV file
        :param has_header: if the CSV or TSV file has a header line
        :param chunk_size: the size of chunk to read
                50000 is recommended by pandas doc and also really good in common cases
                http://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#performance
        :return:
        """

        try:
            df_list = DataTableCsvReader._load_df_list_with_chardet(filepath_or_buffer, sep, has_header, chunk_size)
            DataTableCsvReader._validate_dtypes_in_chunks(df_list, chunk_size)
            with TimeProfile("Dataframe chunks concat"):
                df = pd.concat(df_list, ignore_index=True)
                return df

        except BaseException as ex:
            file_name = os.path.basename(filepath_or_buffer) if isinstance(filepath_or_buffer, str) else None
            ErrorMapping.rethrow(e=ex,
                                 err=FileParsingFailedError(file_format=DataTypes.GENERIC_CSV.value.file_extension,
                                                            file_name=file_name,
                                                            failure_reason=str(ex)))

    @classmethod
    def _load_df_list_with_chardet(cls, filepath_or_buffer, sep: DataTableCsvSep, has_header: bool, chunk_size=50000):
        try:
            return cls._load_df_list(filepath_or_buffer, sep, has_header, chunk_size)

        except UnicodeDecodeError:
            if isinstance(filepath_or_buffer, (str, PurePath)):
                encoding = None
                try:
                    encoding = cls._detect_encoding(filepath_or_buffer)
                    module_logger.debug(f"Detected encoding is '{encoding}'.")

                except BaseException as ex_inner:
                    module_logger.warning(f"Detect encoding failed: {ex_inner}")

                # reload file with detected encoding
                if encoding and encoding != 'utf-8':
                    module_logger.info(f"Reload file with encoding '{encoding}'")
                    return cls._load_df_list(filepath_or_buffer, sep, has_header, chunk_size, encoding=encoding)

            # detect failed, re-raise original error
            raise

    @classmethod
    def _load_df_list(cls, filepath_or_buffer, sep: DataTableCsvSep, has_header: bool, chunk_size=50000, encoding=None):
        df_list = list()
        header = 0 if has_header else None

        try:
            names = None if has_header else cls._generate_column_names(filepath_or_buffer, sep, encoding=encoding)

            with TimeProfile(f"DataFrame read csv/tsv in chunks with chunk size:{chunk_size}"):
                for df in pd.read_csv(filepath_or_buffer=filepath_or_buffer,
                                      sep=sep.value,
                                      header=header,
                                      names=names,
                                      chunksize=chunk_size,
                                      na_values='?',
                                      skipinitialspace=True,
                                      error_bad_lines=False,
                                      warn_bad_lines=True,
                                      encoding=encoding
                                      ):
                    df_list.append(df)
                    cls._print_read_chunk_progress(len(df_list))
            return df_list

        except BaseException as ex:
            module_logger.error(f"Got exception when reading chunk {len(df_list) + 1} with chunk size:{chunk_size}.")
            module_logger.error(f"{type(ex).__name__}: {ErrorMapping.get_exception_message(ex)}")
            raise

    @classmethod
    def _trim_column_names(cls, df):
        column_new_names = {column: column.strip() for column in df.columns if column != column.strip()}
        if column_new_names:
            module_logger.info(f"Trim column names: {column_new_names}")
            df.rename(columns=column_new_names, inplace=True)

    @staticmethod
    def _generate_column_names(filepath_or_buffer, sep: DataTableCsvSep, encoding=None):
        top_n = 10000
        module_logger.info("Pick top 10000 rows to generate column names due to no header provided in source file.")

        # Fix bug: 459161
        # Skip inconsistent rows in column name generation
        top_n_lines = pd.read_csv(filepath_or_buffer=filepath_or_buffer,
                                  sep=sep.value,
                                  error_bad_lines=False,
                                  warn_bad_lines=True,
                                  nrows=top_n,
                                  encoding=encoding)

        column_new_names = [f'Col{col_index+1}' for col_index in range(top_n_lines.shape[1])]
        # Limit the count of shown names in log to make the log readable.
        threshold = 10
        if len(column_new_names) <= threshold:
            module_logger.info(f"Generated {len(column_new_names)} column names: {column_new_names}")
        else:
            first_n_column_names = column_new_names[:threshold]
            module_logger.info(f"Generated {len(column_new_names)} column names,"
                               f" shown first {threshold}: {first_n_column_names}")

        if hasattr(filepath_or_buffer, 'seek'):
            module_logger.info(f"Reset file buffer to 0.")
            filepath_or_buffer.seek(0)

        return column_new_names

    @staticmethod
    def _detect_encoding(file_path, size=DEFAULT_CHARDET_BYTES):
        with open(file_path, 'rb') as f:
            file_bytes = f.read(size)
            det = chardet.detect(file_bytes)
            return det.get('encoding', None)

    @staticmethod
    def _print_read_chunk_progress(read_chunks_count):
        if read_chunks_count < 100 and read_chunks_count % 10 == 0 \
                or read_chunks_count >= 100 and read_chunks_count % 50 == 0:
            module_logger.info(f"Read {read_chunks_count} chunks already.")

    @staticmethod
    @time_profile
    def _validate_dtypes_in_chunks(chunk_list, chunk_size):
        """
        Pandas will detect the dtypes automatically while reading the csv file.
        However, when we read the file by chunks, the detected dtypes might be different between each chunk.
        For example, the input csv is:
            A
            1
            2
            a
            b
        If we read it with chunk size 4, all rows is read in one chunk only, the output column dtype would be object
        and the ndarray type of values would be str ndarray.

        If we read it with chunk size 2, rows are read into two chunks. The output column dtype would be int64 in first
        chunk and object in second one. The ndarray type of values would be int ndarray in first chunk and str ndarray
        in second one. And the most important thing is Pandas would keep the ndarray type even dataframes are
        concatenated into one dataframe. So, the concatenated dataframe would fail when writing to parquet due to
        the different ndarray types in underlying.
        :param chunk_list:
        :param chunk_size:
        :return:
        """
        def is_all_null(column):
            return all(column.isnull())

        def dtypes_are_incompatible(dtype_1, dtype_2):
            # Currently, we only cover the incompatible issue for object case.
            # For other cases, we will add them later.
            return dtype_1 != dtype_2 and (is_object_dtype(dtype_1) or is_object_dtype(dtype_2))

        first_chunk = chunk_list[0]
        for chunk_idx in range(1, len(chunk_list)):
            chunk = chunk_list[chunk_idx]
            if not pd.np.array_equal(first_chunk.dtypes.values, chunk.dtypes.values):
                # Theoretically speaking, there is no way to hit this error by pandas design.
                # But just in case, still add this check.
                if len(first_chunk.dtypes) != len(chunk.dtypes):
                    ErrorMapping.throw(
                        ColumnCountNotEqualError(chunk_id_1=1, chunk_id_2=chunk_idx + 1, chunk_size=chunk_size))

                # Find the different dtypes and check if they're compatible
                for column_idx in range(len(first_chunk.dtypes)):
                    # If one column is all null, it's compatible with another one.
                    if is_all_null(first_chunk.iloc[:, column_idx]) or is_all_null(chunk.iloc[:, column_idx]):
                        continue
                    if dtypes_are_incompatible(first_chunk.dtypes.values[column_idx], chunk.dtypes.values[column_idx]):
                        ErrorMapping.throw(MixedColumnError(column_id=column_idx + 1,
                                                            chunk_id_1=1,
                                                            chunk_id_2=chunk_idx + 1,
                                                            type_1=first_chunk.dtypes.values[column_idx],
                                                            type_2=chunk.dtypes.values[column_idx],
                                                            chunk_size=chunk_size))
