import pandas as pd
import numpy as np
from abc import abstractmethod
from azureml.studio.core.logger import module_logger, TimeProfile
from azureml.studio.modules.recommendation.evaluate_recommender.base_recommendation_evaluator import \
    BaseRecommendationEvaluator
from azureml.studio.common.datatable.data_table import DataTable
from azureml.studio.common.datatable.constants import ColumnTypeName, ElementTypeName
from azureml.studio.common.error import ErrorMapping, InvalidDatasetError
from azureml.studio.modules.recommendation.common.recommender_utils import get_rating_column_name, \
    get_user_column_name, get_item_column_name
from azureml.studio.modules.recommendation.common.score_column_names import USER_COLUMN, \
    RECOMMENDED_ITEM_RATING, TRUE_TOP_RATING, RATED_ITEM, RECOMMENDED_ITEM_HIT, ACTUAL_COUNT, RECOMMENDED_ITEM, \
    PortScheme
from azureml.studio.modules.recommendation.evaluate_recommender.metrics import rating_rel_ndcg, precision_at_k, \
    recall_at_k, ndcg_at_k, map_at_k


class BaseRankingRecommendationEvaluator(BaseRecommendationEvaluator):
    _RANK_COL = "Rank"

    def __init__(self, task):
        super().__init__(task)

    def _validate_data(self, scored_data: DataTable, test_data: DataTable = None):
        super()._validate_data(scored_data, test_data)
        # verify not duplicate user recommendation list
        if scored_data.data_frame[self.task.user_column].duplicated().any():
            ErrorMapping.throw(InvalidDatasetError(dataset1=scored_data.name,
                                                   reason="duplicated item recommendation list for one user"))

    def _process_data(self, scored_data: DataTable, test_data: DataTable = None):
        super()._process_data(scored_data, test_data)
        # convert user column in scored dataset to string type and drop missing users
        self._convert_column_to_string(dt=scored_data, column_key=self.task.user_column)
        self._drop_instances_with_missing_values(df=scored_data.data_frame, column_names=[self.task.user_column])
        if self.task.port_scheme == PortScheme.TwoPort:
            self._drop_instances_with_missing_values(df=test_data.data_frame,
                                                     column_names=[get_item_column_name(test_data.data_frame),
                                                                   get_user_column_name(test_data.data_frame)])

    @abstractmethod
    def _collect_data(self, scored_data: DataTable, test_data: DataTable = None):
        pass

    @abstractmethod
    def _calculate(self, **collected_data):
        pass

    def _check_users_valid(self, scored_data: DataTable, test_data: DataTable):
        test_data_df = test_data.data_frame
        test_users = test_data_df[get_user_column_name(test_data_df)].unique()
        scored_users = scored_data.data_frame[self.task.user_column]
        missing_users = scored_users[~scored_users.isin(test_users)].reset_index(drop=True)
        if missing_users.shape[0] > 0:
            ErrorMapping.throw(
                InvalidDatasetError(dataset1=scored_data.name,
                                    reason=f'cannot find user "{missing_users[0]}" in {test_data.name}'))

    @staticmethod
    def expand_item_recommendations(df: pd.DataFrame, fix, start, end, step, column_name):
        columns = df.columns
        expands = []
        fix_column = columns[fix]

        for i in range(start, end, step):
            expands.append(df[[fix_column, columns[i]]].rename(columns={columns[i]: column_name}))

        return pd.concat(expands)

    @classmethod
    def attach_rank_column(cls, df: pd.DataFrame, group_by: str):
        df[cls._RANK_COL] = df.groupby(by=group_by).cumcount() + 1

        return df

    @staticmethod
    def _filter_by(df: pd.DataFrame, by: str, valid_values: pd.Series):
        """Filter out rows in df, whose 'by' column values are not in valid_values."""
        valid_values = valid_values.unique()
        df = df[df[by].isin(valid_values)]

        return df


class RankingRecommendationEvaluator(BaseRankingRecommendationEvaluator):
    metrics = (precision_at_k, recall_at_k, ndcg_at_k, map_at_k)
    _HIT_COUNT_COL = "Hit count"

    def __init__(self, task):
        super().__init__(task)

    def _validate_data(self, scored_data: DataTable, test_data: DataTable = None):
        super()._validate_data(scored_data, test_data)
        if self.task.port_scheme == PortScheme.OnePort:
            # verify hit columns of boolean type
            for col in scored_data.column_names[2:-1:2]:
                self._verify_boolean_or_nan_type(dt=scored_data, column_name=col)
            self._verify_actual_count(scored_data)

    @staticmethod
    def _verify_boolean_or_nan_type(dt: DataTable, column_name):
        column_type = dt.get_column_type(col_key=column_name)
        if column_type != ColumnTypeName.BINARY and not dt.is_all_na_column(column_name):
            ErrorMapping.throw_invalid_column_type(type_=column_type, column_name=column_name, arg_name=dt.name)

    def _verify_actual_count(self, scored_data: DataTable):
        actual_count_column = self.task.actual_count_column
        ErrorMapping.verify_element_type(type_=scored_data.get_element_type(actual_count_column),
                                         expected_type=ElementTypeName.INT,
                                         column_name=actual_count_column,
                                         arg_name=scored_data.name)
        actual_count = scored_data.get_column(col_key=actual_count_column).replace(to_replace=[np.inf, -np.inf],
                                                                                   value=np.nan)
        if (actual_count <= 0).any():
            ErrorMapping.throw(InvalidDatasetError(dataset1=scored_data.name,
                                                   reason=f"some {actual_count_column} value(s) less or equal to 0"))

    def _process_data(self, scored_data: DataTable, test_data: DataTable = None):
        super()._process_data(scored_data, test_data)

        # convert item columns to string type
        if self.task.port_scheme == PortScheme.OnePort:
            for item_column in scored_data.column_names[1:-2:2]:
                self._convert_column_to_string(dt=scored_data, column_key=item_column)
                self._drop_instances_with_missing_values(scored_data.data_frame,
                                                         column_names=[self.task.actual_count_column])
        else:
            for item_column in scored_data.column_names[1:]:
                self._convert_column_to_string(dt=scored_data, column_key=item_column)

    def _collect_data(self, scored_data: DataTable, test_data: DataTable = None):
        scored_data_df = scored_data.data_frame
        if self.task.port_scheme == PortScheme.OnePort:
            scored_data_df = scored_data_df.rename(columns={self.task.user_column: USER_COLUMN,
                                                            self.task.actual_count_column: ACTUAL_COUNT})
            hit_df = self.expand_item_recommendations(df=scored_data_df, fix=0, start=2, end=self.task.top_k * 2 + 1,
                                                      step=2, column_name=RECOMMENDED_ITEM_HIT)
            hit_df[RECOMMENDED_ITEM_HIT][hit_df[RECOMMENDED_ITEM_HIT].isnull()] = False
            hit_count_df = hit_df.groupby(USER_COLUMN, as_index=False).agg({RECOMMENDED_ITEM_HIT: "sum"})
            hit_count_df = hit_count_df.rename(columns={RECOMMENDED_ITEM_HIT: self._HIT_COUNT_COL})
            actual_count_df = scored_data_df[[USER_COLUMN, ACTUAL_COUNT]]
            count_df = pd.merge(hit_count_df, actual_count_df, on=[USER_COLUMN])
            hit_rank_df = self.attach_rank_column(df=hit_df, group_by=USER_COLUMN)
        else:
            self._check_users_valid(scored_data, test_data)
            scored_data_df = scored_data_df.rename(columns={self.task.user_column: USER_COLUMN})
            test_data_df = test_data.data_frame
            test_data_df = test_data_df.rename(columns={get_user_column_name(test_data_df): USER_COLUMN,
                                                        get_item_column_name(test_data_df): RECOMMENDED_ITEM})
            hit_rank_df = self.expand_item_recommendations(df=scored_data_df, fix=0, start=1, end=self.task.top_k + 1,
                                                           step=1, column_name=RECOMMENDED_ITEM)
            hit_rank_df = self.attach_rank_column(df=hit_rank_df, group_by=USER_COLUMN)
            test_data_df[RECOMMENDED_ITEM_HIT] = True
            hit_rank_df = pd.merge(hit_rank_df, test_data_df, on=[USER_COLUMN, RECOMMENDED_ITEM], how="left")
            hit_rank_df[RECOMMENDED_ITEM_HIT] = hit_rank_df[RECOMMENDED_ITEM_HIT].notnull()
            hit_rank_df = hit_rank_df[[USER_COLUMN, RECOMMENDED_ITEM_HIT, self._RANK_COL]]

            test_data_df = self._filter_by(df=test_data_df, by=USER_COLUMN, valid_values=hit_rank_df[USER_COLUMN])
            count_df = test_data_df.groupby(USER_COLUMN, as_index=False).agg({RECOMMENDED_ITEM: "count"})
            hit_count_df = hit_rank_df.groupby(USER_COLUMN, as_index=False).agg({RECOMMENDED_ITEM_HIT: "sum"})
            count_df = pd.merge(count_df, hit_count_df, on=[USER_COLUMN])
            count_df = count_df.rename(columns={RECOMMENDED_ITEM: ACTUAL_COUNT,
                                                RECOMMENDED_ITEM_HIT: self._HIT_COUNT_COL})

        self._check_actual_hit_count(count_df=count_df, hit_count_col=self._HIT_COUNT_COL,
                                     actual_count_col=ACTUAL_COUNT, dataset_name=scored_data.name)
        return hit_rank_df, count_df

    def _calculate(self, hit_rank_df: pd.DataFrame, count_df: pd.DataFrame):
        """Calculate ranking task metrics with hit_rank_df and count_df.

        :param hit_rank_df: pd.DataFrame. The columns should be [USER_COLUMN, RECOMMENDED_ITEM_HIT, _RANK_COL]
        :param count_df: pd.DataFrame. The columns should be [USER_COLUMN, _HIT_COUNT_COL, ACTUAL_COUNT]
        :return: dict, where key is metric name and value is metric value.
        """
        # if no valid instances, return NAN metrics
        if count_df.shape[0] == 0:
            module_logger.info("Found no valid scored instances.")
            metric_values = dict((metric.name, np.nan) for metric in self.metrics)
            return metric_values

        metric_values = {}
        for metric in self.metrics:
            with TimeProfile(f"Calculate {metric.name} metric"):
                metric_values[metric.name] = metric(hit_rank_df=hit_rank_df,
                                                    count_df=count_df,
                                                    user_col=USER_COLUMN,
                                                    hit_col=RECOMMENDED_ITEM_HIT,
                                                    rank_col=self._RANK_COL,
                                                    hit_count_col=self._HIT_COUNT_COL,
                                                    actual_count_col=ACTUAL_COUNT)

        return metric_values

    @staticmethod
    def _check_actual_hit_count(count_df: pd.DataFrame, hit_count_col: str, actual_count_col: str, dataset_name: str):
        if (count_df[hit_count_col] > count_df[actual_count_col]).any():
            ErrorMapping.throw(InvalidDatasetError(dataset1=dataset_name,
                                                   reason=f"some hit item count(s) greater than actual item count(s). "
                                                   f"This may caused by duplicated item recommendations or wrong hit "
                                                   f"values"))


class RankingRatedRecommendationEvaluator(BaseRankingRecommendationEvaluator):
    metrics = (rating_rel_ndcg,)

    def __init__(self, task):
        super().__init__(task)

    def _validate_data(self, scored_data: DataTable, test_data: DataTable = None):
        super()._validate_data(scored_data, test_data)
        if self.task.port_scheme == PortScheme.OnePort:
            # verify rating columns of numeric or nan types
            scored_columns = scored_data.column_names
            for rating_column_name in scored_columns[2:self.task.top_k * 2 + 1:2]:
                self._verify_numeric_or_nan_type(dt=scored_data, column_name=rating_column_name)

            for true_rating_column_name in scored_columns[2 * self.task.top_k + 1:]:
                self._verify_numeric_or_nan_type(dt=scored_data, column_name=true_rating_column_name)
        else:
            ErrorMapping.verify_number_of_columns_equal_to(curr_column_count=test_data.number_of_columns,
                                                           required_column_count=3,
                                                           arg_name=test_data.name)
            self._verify_numeric_type(dt=test_data, column_name=get_rating_column_name(test_data.data_frame))

    @staticmethod
    def _verify_numeric_or_nan_type(dt: DataTable, column_name):
        column_type = dt.get_column_type(col_key=column_name)
        if column_type != ColumnTypeName.NUMERIC and not dt.is_all_na_column(column_name):
            ErrorMapping.throw_invalid_column_type(type_=column_type, column_name=column_name, arg_name=dt.name)

    def _process_data(self, scored_data: DataTable, test_data: DataTable = None):
        super()._process_data(scored_data, test_data)

        # convert item columns to string
        if self.task.port_scheme == PortScheme.OnePort:
            for item_column in scored_data.column_names[1:self.task.top_k * 2:2]:
                self._convert_column_to_string(dt=scored_data, column_key=item_column)
        else:
            for item_column in scored_data.column_names[1:]:
                self._convert_column_to_string(dt=scored_data, column_key=item_column)

    def _collect_data(self, scored_data: DataTable, test_data: DataTable = None):
        if self.task.port_scheme == PortScheme.OnePort:
            scored_data_df = scored_data.data_frame
            scored_data_df = scored_data_df.rename(columns={self.task.user_column: USER_COLUMN})
            pred_rating_df = self.expand_item_recommendations(scored_data_df, fix=0, start=2,
                                                              end=2 * self.task.top_k + 1, step=2,
                                                              column_name=RECOMMENDED_ITEM_RATING)
            true_rating_df = self.expand_item_recommendations(scored_data_df, fix=0, start=2 * self.task.top_k + 1,
                                                              end=scored_data_df.shape[1], step=1,
                                                              column_name=TRUE_TOP_RATING)
            min_rating = self._get_not_inf_min(pred_rating_df[RECOMMENDED_ITEM_RATING])
        else:
            min_rating = self._get_not_inf_min(test_data.data_frame[get_rating_column_name(test_data.data_frame)])
            true_rating_df, pred_rating_df = self._combine_scored_test_data(scored_data, test_data)

        self._drop_instances_with_missing_values(df=pred_rating_df, column_names=[RECOMMENDED_ITEM_RATING])
        self._drop_instances_with_missing_values(df=true_rating_df, column_names=[TRUE_TOP_RATING])

        # check if true item list and recommended item list length is equal
        if not self._check_group_count_equals(df1=pred_rating_df, df2=true_rating_df, group_key1=USER_COLUMN,
                                              group_key2=USER_COLUMN, count_key1=RECOMMENDED_ITEM_RATING,
                                              count_key2=TRUE_TOP_RATING):
            ErrorMapping.throw(InvalidDatasetError(dataset1=scored_data.name,
                                                   reason="recommended item true rating list length not equal "
                                                          "to true top rating list"))

        true_rating_df = self._normalize_rating(df=true_rating_df, rating_col=TRUE_TOP_RATING, min_rating=min_rating)
        pred_rating_df = self._normalize_rating(df=pred_rating_df, rating_col=RECOMMENDED_ITEM_RATING,
                                                min_rating=min_rating)
        self.attach_rank_column(df=true_rating_df, group_by=USER_COLUMN)
        self.attach_rank_column(df=pred_rating_df, group_by=USER_COLUMN)

        return true_rating_df, pred_rating_df

    def _calculate(self, true_rating_df, pred_rating_df):
        """Calculate ranking rated recommendation task metrics with true_rating_df and pred_rating_df.

        :param true_rating_df: pd.DataFrame. The columns should be [USER_COLUMN, RECOMMENDED_ITEM_RATING, _RANK_COL]
        :param pred_rating_df: pd.DataFrame. The columns should be [USER_COLUMN, TRUE_TOP_RATING, _RANK_COL]
        :return: dict, where key is metric name and value is metric value.
        """
        # if no valid instances, return NAN metrics
        if pred_rating_df.shape[0] == 0:
            module_logger.info("Found no valid scored instances.")
            metric_values = dict((metric.name, np.nan) for metric in self.metrics)
            return metric_values

        metric_values = {}
        for metric in self.metrics:
            with TimeProfile(f"Calculate {metric.name} metric"):
                metric_values[metric.name] = metric(true_rating_df=true_rating_df,
                                                    pred_rating_df=pred_rating_df,
                                                    user_col=USER_COLUMN,
                                                    true_rating_col=TRUE_TOP_RATING,
                                                    pred_rating_col=RECOMMENDED_ITEM_RATING,
                                                    rank_col=self._RANK_COL)

        return metric_values

    def _combine_scored_test_data(self, scored_data: DataTable, test_data: DataTable):
        scored_data_df = scored_data.data_frame
        test_data_df = test_data.data_frame

        self._check_users_valid(scored_data, test_data)
        scored_data_df = scored_data_df.rename(columns={self.task.user_column: USER_COLUMN})
        true_rating_df = test_data_df.rename(columns={get_user_column_name(test_data_df): USER_COLUMN,
                                                      get_item_column_name(test_data_df): RATED_ITEM,
                                                      get_rating_column_name(test_data_df): TRUE_TOP_RATING})

        pred_rating_df = self.expand_item_recommendations(scored_data_df, fix=0, start=1, end=self.task.top_k + 1,
                                                          step=1, column_name=RATED_ITEM)
        pred_rating_df = pd.merge(pred_rating_df, true_rating_df, on=[USER_COLUMN, RATED_ITEM], how="left")
        pred_rating_df = pred_rating_df.rename(columns={TRUE_TOP_RATING: RECOMMENDED_ITEM_RATING})

        self._check_items_rated(df=pred_rating_df, item_col=RATED_ITEM, rating_col=RECOMMENDED_ITEM_RATING,
                                dataset_name=scored_data.name)
        self._drop_instances_with_missing_values(df=pred_rating_df, column_names=[RATED_ITEM])
        # filter out extra users not in scored dataset
        true_rating_df = self._filter_by(df=true_rating_df, by=USER_COLUMN, valid_values=pred_rating_df[USER_COLUMN])
        with TimeProfile(f"Get true top k ratings for each user"):
            true_rating_df = self._get_top_k(df=true_rating_df, group_key=USER_COLUMN, sort_key=TRUE_TOP_RATING,
                                             top_k=self.task.top_k)
        if true_rating_df.shape[0] == 0:
            true_rating_df = pd.DataFrame(columns=[USER_COLUMN, TRUE_TOP_RATING])
            true_rating_df[TRUE_TOP_RATING] = true_rating_df[TRUE_TOP_RATING].astype(float)

        true_rating_df = true_rating_df[[USER_COLUMN, TRUE_TOP_RATING]]
        pred_rating_df = pred_rating_df[[USER_COLUMN, RECOMMENDED_ITEM_RATING]]
        return true_rating_df, pred_rating_df

    @staticmethod
    def _check_items_rated(df: pd.DataFrame, item_col, rating_col, dataset_name):
        """Check if there are unrated items, where items are not null, but ratings are null."""
        not_null_items = df[item_col].notnull()
        null_true_ratings = df[rating_col].replace(to_replace=[np.inf, -np.inf], value=np.nan).isnull()
        if (not_null_items & null_true_ratings).any():
            ErrorMapping.throw(InvalidDatasetError(dataset1=dataset_name, reason=f"dataset has unrated items"))

    @staticmethod
    def _get_top_k(df: pd.DataFrame, group_key: str, sort_key: str, top_k: int):
        """For each group by 'group_key', get instances whose values in 'sort_key' column are in 'top_k' largest."""
        df = df.groupby(group_key, as_index=False).apply(lambda x: x.nlargest(top_k, columns=sort_key)).reset_index(
            drop=True)

        return df

    @staticmethod
    def _check_group_count_equals(df1: pd.DataFrame, df2: pd.DataFrame, group_key1: str, group_key2: str,
                                  count_key1: str, count_key2: str):
        df1_count = df1.groupby(group_key1).count()[count_key1]
        df2_count = df2.groupby(group_key2).count()[count_key2]
        return df1_count.equals(df2_count)

    @staticmethod
    def _normalize_rating(df: pd.DataFrame, rating_col: str, min_rating):
        df[rating_col] = df[rating_col] - min_rating + 1
        return df

    @staticmethod
    def _get_not_inf_min(sr: pd.Series):
        return sr.replace(to_replace=[-np.inf], value=np.nan).min(skipna=True)
