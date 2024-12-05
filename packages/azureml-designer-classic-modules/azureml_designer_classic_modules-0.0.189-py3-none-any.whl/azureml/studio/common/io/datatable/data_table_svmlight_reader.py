import pandas as pd

from sklearn.datasets import load_svmlight_file

from azureml.studio.common.datatable.data_table import DataTable
from azureml.studio.common.datatypes import DataTypes
from azureml.studio.common.error import ErrorMapping, FileParsingFailedError
from azureml.studio.core.logger import time_profile, module_logger, TimeProfile


class DataTableSvmLightReader:
    SVMLIGHT_COLUMN_NAME_LABELS = "Labels"

    @staticmethod
    @time_profile
    def read(filepath_or_buffer):
        df = DataTableSvmLightReader.read_as_data_frame(filepath_or_buffer)

        with TimeProfile("DataTable Construction"):
            dt = DataTable(df=df)
            dt.meta_data.label_column_name = DataTableSvmLightReader.SVMLIGHT_COLUMN_NAME_LABELS

        return dt

    @staticmethod
    @time_profile
    def read_as_data_frame(filepath_or_buffer):
        try:
            module_logger.info("Read and parse SVMLight file with sklearn.datasets.load_svmlight_file() function.")
            sparse_matrix, labels = load_svmlight_file(f=filepath_or_buffer)
            module_logger.info("Construct SVMLight data as pd.DataFrame.")
            df = pd.DataFrame(sparse_matrix.todense())
        except BaseException as ex:
            ErrorMapping.rethrow(e=ex,
                                 err=FileParsingFailedError(file_format=DataTypes.SVM_LIGHT.value.file_extension))

        DataTableSvmLightReader._normalize_column_names(df)

        module_logger.info(f"Add label column {DataTableSvmLightReader.SVMLIGHT_COLUMN_NAME_LABELS}.")
        df[DataTableSvmLightReader.SVMLIGHT_COLUMN_NAME_LABELS] = labels

        return df

    @staticmethod
    def _normalize_column_names(df):
        module_logger.info("Normalize column names due to no header provided in source file.")
        for col_index in range(df.shape[1]):
            df.rename(columns={df.columns.tolist()[col_index]: f'Col{col_index+1}'}, inplace=True)
        module_logger.info(f"Normalized column names: {df.columns.values}")
