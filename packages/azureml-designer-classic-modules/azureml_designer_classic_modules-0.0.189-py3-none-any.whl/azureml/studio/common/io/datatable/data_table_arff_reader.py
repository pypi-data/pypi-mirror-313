import pandas as pd
from scipy.io import arff

from azureml.studio.common.datatable.constants import ElementTypeName
from azureml.studio.common.datatable.data_table import DataTable
from azureml.studio.common.datatypes import DataTypes
from azureml.studio.common.error import ErrorMapping, FileParsingFailedError
from azureml.studio.core.logger import time_profile, module_logger


class DataTableArffReader:
    _ARFF_TYPE_NOMINAL = "nominal"

    @staticmethod
    @time_profile
    def read(filepath_or_buffer):
        df, arff_meta = DataTableArffReader.read_as_data_frame(filepath_or_buffer)
        dt = DataTable(df=df)
        DataTableArffReader._update_meta_data(dt, arff_meta)

        return dt

    @staticmethod
    @time_profile
    def read_files(file_list):
        if not file_list:
            return list()

        dt_list = list()
        for file in file_list:
            dt = DataTableArffReader.read(
                filepath_or_buffer=file,
            )
            dt_list.append(dt)

        return dt_list

    @staticmethod
    @time_profile
    def read_as_data_frame(filepath_or_buffer):
        try:
            module_logger.info("Read and parse arff file with arff.loadarff() function.")
            arff_data, arff_meta = arff.loadarff(filepath_or_buffer)
            module_logger.info("Construct arff data as pd.DataFrame.")
            df = pd.DataFrame(arff_data)
        except BaseException as ex:
            ErrorMapping.rethrow(e=ex,
                                 err=FileParsingFailedError(file_format=DataTypes.ARFF.value.file_extension))
        return df, arff_meta

    @staticmethod
    def _update_meta_data(dt: DataTable, arff_meta):
        module_logger.info("Update arff meta into DataTable.")
        for attribute_name in arff_meta.names():
            attr_type, _ = arff_meta[attribute_name]
            if attr_type == DataTableArffReader._ARFF_TYPE_NOMINAL:
                col_index = dt.get_column_index(attribute_name)
                module_logger.info(f'Set column "{attribute_name}" (index={col_index})'
                                   f' to type {ElementTypeName.CATEGORY}.')
                dt.set_column_element_type(col_index, ElementTypeName.CATEGORY)
