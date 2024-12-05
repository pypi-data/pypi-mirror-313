import pandas as pd

from azureml.studio.common.datatable.constants import ElementTypeName
from azureml.studio.common.datatable.data_table import DataTable
from azureml.studio.core.data_frame_schema \
    import DataFrameSchema
from azureml.studio.common.datatable.data_type_conversion import convert_column_by_element_type
from azureml.studio.core.logger import time_profile
from azureml.studio.core.utils.missing_value_utils import is_na


class DataFrameSchemaConstructor:

    @classmethod
    @time_profile
    def create_data_table_schema_from_dict(cls, meta_data_dict):
        return DataFrameSchema.from_dict(meta_data_dict)


class DataTableConstructor:

    @classmethod
    @time_profile
    def create_data_table_from_dict(cls, data_dict, meta_data_dict):
        meta_data = DataFrameSchemaConstructor.create_data_table_schema_from_dict(meta_data_dict)

        if set(data_dict.keys()) != set(meta_data.column_attributes.names):
            different_names = set(meta_data.column_attributes.names).difference(set(data_dict.keys()))

            raise ValueError(f'Input data_dict must have the same column names as the meta data. '
                             f'Different columns are: {different_names}')

        df = pd.DataFrame()

        for column_name in meta_data.column_attributes.names:
            column = pd.Series(data_dict[column_name])
            target_type = meta_data.column_attributes[column_name].element_type
            if is_na(column) and target_type == ElementTypeName.NAN:
                # Do not convert otherwise error will be raised
                converted_column = column
            else:
                converted_column = convert_column_by_element_type(column, target_type)
            df[column_name] = converted_column

        return DataTable(df=df, meta_data=meta_data)
