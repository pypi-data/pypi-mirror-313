import pandas as pd
import numpy as np
from abc import abstractmethod
from azureml.studio.common.error import ErrorMapping, InvalidDatasetError
from azureml.studio.common.datatable.constants import ColumnTypeName, ElementTypeName
from azureml.studio.common.datatable.data_table import DataTable
from azureml.studio.modules.recommendation.common.recommender_utils import get_user_column_name, get_item_column_name, \
    USER_COLUMN_INDEX, ITEM_COLUMN_INDEX
from azureml.studio.core.logger import TimeProfile
from azureml.studio.modules.recommendation.common.score_column_names import PortScheme


class BaseRecommendationEvaluator:
    def __init__(self, task):
        self.task = task

    def evaluate(self, scored_data: DataTable, test_data: DataTable = None):
        self._validate_data(scored_data, test_data)
        with TimeProfile("Process data"):
            self._process_data(scored_data, test_data)
        with TimeProfile("Collect data"):
            collected_data = self._collect_data(scored_data, test_data)
        metric_values = self._calculate(*collected_data)
        return self._build_metric_dt(metric_values=metric_values)

    def _validate_data(self, scored_data: DataTable, test_data: DataTable = None):
        ErrorMapping.verify_not_null_or_empty(x=scored_data, name="Scored dataset")
        ErrorMapping.verify_number_of_rows_greater_than_or_equal_to(curr_row_count=scored_data.number_of_rows,
                                                                    required_row_count=1,
                                                                    arg_name=scored_data.name)
        if self.task.port_scheme == PortScheme.TwoPort:
            ErrorMapping.verify_not_null_or_empty(x=test_data, name="Test dataset")
            ErrorMapping.verify_number_of_rows_greater_than_or_equal_to(curr_row_count=test_data.number_of_rows,
                                                                        required_row_count=1,
                                                                        arg_name=test_data.name)
            ErrorMapping.verify_number_of_columns_greater_than_or_equal_to(
                curr_column_count=test_data.number_of_columns, required_column_count=2, arg_name=test_data.name)
            self._verify_duplicate_user_item_pairs(dt=test_data, user_col=get_user_column_name(test_data.data_frame),
                                                   item_col=get_item_column_name(test_data.data_frame))

    def _process_data(self, scored_data: DataTable, test_data: DataTable = None):
        if self.task.port_scheme == PortScheme.TwoPort:
            self._convert_column_to_string(dt=test_data, column_key=USER_COLUMN_INDEX)
            self._convert_column_to_string(dt=test_data, column_key=ITEM_COLUMN_INDEX)

    @abstractmethod
    def _collect_data(self, scored_data: DataTable, test_data: DataTable = None):
        pass

    @abstractmethod
    def _calculate(self, **collected_data):
        pass

    @staticmethod
    def _verify_numeric_type(dt: DataTable, column_name):
        ErrorMapping.verify_element_type(type_=dt.get_column_type(column_name),
                                         expected_type=ColumnTypeName.NUMERIC,
                                         column_name=column_name,
                                         arg_name=dt.name)

    @staticmethod
    def _verify_duplicate_user_item_pairs(dt: DataTable, user_col, item_col):
        duplicated_index = dt.data_frame.index[dt.data_frame.duplicated(subset=[user_col, item_col])]
        if duplicated_index.shape[0] > 0:
            user = dt.data_frame[user_col][duplicated_index[0]]
            item = dt.data_frame[item_col][duplicated_index[0]]
            ErrorMapping.throw(InvalidDatasetError(
                dataset1=dt.name,
                reason=f'duplicated user-item pairs for user "{user}", item "{item}"'))

    @staticmethod
    def _convert_column_to_string(dt: DataTable, column_key):
        if dt.get_column_type(column_key) == ColumnTypeName.STRING:
            return
        dt.set_column_element_type(col_index=column_key, new_type=ElementTypeName.STRING)

    @staticmethod
    def _drop_instances_with_missing_values(df: pd.DataFrame, column_names):
        df.replace(to_replace=[np.inf, -np.inf], value=np.nan, inplace=True)
        df.dropna(subset=column_names, inplace=True)
        df.reset_index(drop=True, inplace=True)

    @staticmethod
    def _build_metric_dt(metric_values: dict):
        return DataTable(df=pd.DataFrame(dict((k, [v]) for k, v in metric_values.items())))
