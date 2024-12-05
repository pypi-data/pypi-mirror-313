import pandas as pd

from azureml.studio.common.datatable.data_table import DataTableColumnSelection
from azureml.studio.common.datatable.data_table import DataTable
from azureml.studio.common.error import ErrorMapping, ColumnNotFoundError, InvalidColumnTypeError
from azureml.studio.core.logger import module_logger, time_profile
from azureml.studio.common.types import AutoEnum
from azureml.studio.modulehost.constants import ColumnTypeName
from azureml.studio.modules.datatransform.common.base_transform import BaseTransform
from azureml.studio.modules.datatransform.common.named_encoder import NamedMinMaxEncoder, NamedLogisticEncoder, \
    NamedLogNormalEncoder, NamedTanhEncoder, NamedZScoreEncoder


class TransformationMethods(AutoEnum):
    ZScore = ()
    MinMax = ()
    Logistic = ()
    LogNormal = ()
    Tanh = ()


class NormalizeTransformer(BaseTransform):
    def __init__(self, data_set: DataTable, col_set: DataTableColumnSelection, method: TransformationMethods,
                 constant_column_option):
        self.method = method
        self.is_integral = self.method in [TransformationMethods.ZScore, TransformationMethods.MinMax,
                                           TransformationMethods.LogNormal]
        self.use_zero_for_constant_column = constant_column_option
        column_indexes = col_set.select_column_indexes(data_set)
        column_names = list(map(data_set.get_column_name, column_indexes))
        self.column_names = column_names
        module_logger.info(f"Columns {column_names} will be normalized.")
        self.column_encoder_dict = {}
        if self.method == TransformationMethods.ZScore:
            module_logger.info(f'Use ZScore to perform numeric normalization.')
            self.encoder_type = NamedZScoreEncoder
        elif self.method == TransformationMethods.Tanh:
            module_logger.info(f'Use Tanh to perform numeric normalization.')
            self.encoder_type = NamedTanhEncoder
        elif self.method == TransformationMethods.Logistic:
            module_logger.info(f'Use Logistic to perform numeric normalization.')
            self.encoder_type = NamedLogisticEncoder
        elif self.method == TransformationMethods.LogNormal:
            module_logger.info(f'Use LogNormal to perform numeric normalization.')
            self.encoder_type = NamedLogNormalEncoder
        else:
            module_logger.info(f'Use MinMax to perform numeric normalization.')
            self.encoder_type = NamedMinMaxEncoder
        self._fit_data(data_set=data_set)

    @time_profile
    def _fit_data(self, data_set):
        instance_number = data_set.number_of_rows
        for column_name in self.column_names:
            # Follow v1's setting, if [ZScore, MinMax, LogNormal] get an all nan column,
            # This column will not be normalized
            if self.is_integral and data_set.get_number_of_missing_value(column_name) == instance_number:
                continue
            self.column_encoder_dict[column_name] = self.encoder_type(column_name, self.use_zero_for_constant_column)
            self.column_encoder_dict[column_name].fit(data_set.get_column(column_name))

    @time_profile
    def apply(self, dt: DataTable):
        # Verify that input dataset contains columns with names memorized in the ITransform object
        # Verify that selected columns are numeric
        for column_name in self.column_encoder_dict:
            if not (column_name in dt.column_names):
                ErrorMapping.throw(ColumnNotFoundError(column_name))
            col_type = dt.get_column_type(column_name)
            if col_type != ColumnTypeName.NUMERIC:
                ErrorMapping.throw(InvalidColumnTypeError(ColumnTypeName.NUMERIC, column_name))
        instance_number = dt.number_of_rows
        out_dt = dt.clone()
        for column_name, encoder in self.column_encoder_dict.items():
            if dt.get_number_of_missing_value(column_name) == instance_number:
                continue
            series = dt.get_column(column_name)
            series = encoder.transform(series)
            out_dt.set_column(col_key=column_name, column=pd.Series(series))
        return out_dt
