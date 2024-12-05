import pandas as pd
import numpy as np
from azureml.studio.common.datatable.data_table import DataTable
from azureml.studio.common.error import ErrorMapping, InvalidDatasetError
from azureml.studio.core.logger import module_logger, TimeProfile
from azureml.studio.modules.recommendation.common.recommender_utils import get_rating_column_name, \
    get_user_column_name, get_item_column_name
from azureml.studio.modules.recommendation.evaluate_recommender.base_recommendation_evaluator import \
    BaseRecommendationEvaluator
from azureml.studio.modules.recommendation.common.score_column_names import USER_COLUMN, ITEM_COLUMN, \
    TRUE_RATING, SCORED_RATING, PortScheme
from azureml.studio.modules.recommendation.evaluate_recommender.metrics import mae, rmse, rsquared, exp_var


class RegressionRecommendationEvaluator(BaseRecommendationEvaluator):
    metrics = (mae, rmse, rsquared, exp_var)

    def __init__(self, task):
        super().__init__(task)

    def _validate_data(self, scored_data: DataTable, test_data: DataTable = None):
        super()._validate_data(scored_data, test_data)
        self._verify_numeric_type(dt=scored_data, column_name=self.task.scored_rating_column)
        if self.task.port_scheme == PortScheme.OnePort:
            self._verify_numeric_type(dt=scored_data, column_name=self.task.true_rating_column)
        else:
            ErrorMapping.verify_number_of_columns_greater_than_or_equal_to(
                curr_column_count=test_data.number_of_columns,
                required_column_count=3,
                arg_name=test_data.name)
            self._verify_numeric_type(dt=test_data, column_name=get_rating_column_name(test_data.data_frame))
            self._verify_duplicate_user_item_pairs(dt=scored_data, user_col=self.task.user_column,
                                                   item_col=self.task.item_column)

    def _process_data(self, scored_data: DataTable, test_data: DataTable = None):
        super()._process_data(scored_data, test_data)
        if self.task.port_scheme == PortScheme.OnePort:
            self._drop_instances_with_missing_values(df=scored_data.data_frame,
                                                     column_names=[self.task.true_rating_column,
                                                                   self.task.scored_rating_column])
        else:
            self._convert_column_to_string(dt=scored_data, column_key=self.task.user_column)
            self._convert_column_to_string(dt=scored_data, column_key=self.task.item_column)
            self._drop_instances_with_missing_values(df=scored_data.data_frame,
                                                     column_names=[self.task.user_column, self.task.item_column,
                                                                   self.task.scored_rating_column])
            self._drop_instances_with_missing_values(df=test_data.data_frame,
                                                     column_names=[get_rating_column_name(test_data.data_frame)])

    def _collect_data(self, scored_data: DataTable, test_data: DataTable = None):
        scored_data_df = scored_data.data_frame

        # merge scored data and test data to meet the same format of one port scheme
        if self.task.port_scheme == PortScheme.OnePort:
            scored_data_df = scored_data_df.rename(columns={self.task.true_rating_column: TRUE_RATING,
                                                            self.task.scored_rating_column: SCORED_RATING})
        else:
            scored_data_df = scored_data_df.rename(columns={self.task.user_column: USER_COLUMN,
                                                            self.task.item_column: ITEM_COLUMN,
                                                            self.task.scored_rating_column: SCORED_RATING})
            test_data_df = test_data.data_frame
            test_data_df = test_data_df.rename(columns={get_user_column_name(test_data_df): USER_COLUMN,
                                                        get_item_column_name(test_data_df): ITEM_COLUMN,
                                                        get_rating_column_name(test_data_df): TRUE_RATING})
            scored_data_df = pd.merge(left=test_data_df, right=scored_data_df, how='right',
                                      on=[USER_COLUMN, ITEM_COLUMN])
            missing_ratings_index = scored_data_df.index[scored_data_df[TRUE_RATING].isnull()]
            if missing_ratings_index.shape[0] > 0:
                missing_user = scored_data_df[USER_COLUMN][missing_ratings_index[0]]
                missing_item = scored_data_df[ITEM_COLUMN][missing_ratings_index[0]]
                ErrorMapping.throw(InvalidDatasetError(dataset1=test_data.name,
                                                       reason=f'cannot find true rating for user "{missing_user}" and '
                                                       f'item "{missing_item}" pair in {test_data.name}'))
        return scored_data_df[[TRUE_RATING, SCORED_RATING]],

    def _calculate(self, rating_df: pd.DataFrame):
        """Calculate regression task metrics with rating_df.

        :param rating_df: pd.DataFrame. The column should be [TRUE_RATING, SCORED_RATING], where TRUE_RATING column
        indicates true ratings, and SCORED_RATING column indicates scored ratings.
        :return: dict, where key is metric name and value is metric value.
        """
        # if no valid instances, return NAN metrics
        if rating_df.shape[0] == 0:
            module_logger.info("Found no valid scored instances.")
            metric_values = dict((metric.name, np.nan) for metric in self.metrics)
            return metric_values

        y_true = rating_df[TRUE_RATING]
        y_pred = rating_df[SCORED_RATING]

        metric_values = {}
        for metric in self.metrics:
            with TimeProfile(f"Calculate {metric.name} metric"):
                metric_values[metric.name] = metric(y_true, y_pred)

        return metric_values
