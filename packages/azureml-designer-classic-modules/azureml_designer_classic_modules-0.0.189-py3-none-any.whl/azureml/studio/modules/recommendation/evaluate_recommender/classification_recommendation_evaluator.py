import pandas as pd
import numpy as np
from azureml.studio.core.logger import module_logger, TimeProfile
from azureml.studio.modules.recommendation.evaluate_recommender.base_recommendation_evaluator import \
    BaseRecommendationEvaluator
from azureml.studio.common.datatable.data_table import DataTable
from azureml.studio.common.error import ErrorMapping, InvalidDatasetError, NotExpectedLabelColumnError
from azureml.studio.modules.recommendation.common.score_column_names import SCORED_PROB, SCORED_LABEL, \
    USER_COLUMN, ITEM_COLUMN, TRUE_LABEL, PortScheme
from azureml.studio.modules.recommendation.common.recommender_utils import get_user_column_name, get_item_column_name, \
    get_label_column_name
from azureml.studio.modules.datatransform.common.named_encoder import BinaryNamedLabelEncoder
from azureml.studio.modules.recommendation.evaluate_recommender.metrics import accuracy, logloss, f1, auc


class ClassificationRecommendationEvaluator(BaseRecommendationEvaluator):
    _THRESHOLD = 0.5
    metrics = (accuracy, logloss, f1, auc)

    def __init__(self, task):
        super().__init__(task)

    def _validate_data(self, scored_data: DataTable, test_data: DataTable = None):
        super()._validate_data(scored_data, test_data)
        self._verify_numeric_type(dt=scored_data, column_name=self.task.scored_prob_column)
        if self.task.port_scheme == PortScheme.TwoPort:
            ErrorMapping.verify_number_of_columns_greater_than_or_equal_to(
                curr_column_count=test_data.number_of_columns,
                required_column_count=3,
                arg_name=test_data.name)
            self._verify_duplicate_user_item_pairs(dt=scored_data, user_col=self.task.user_column,
                                                   item_col=self.task.item_column)

    def _verify_probability(self, scored_data: DataTable):
        probs = scored_data.get_column(col_key=self.task.scored_prob_column).replace(to_replace=[np.inf, -np.inf],
                                                                                     value=np.nan).dropna()
        min_prob = probs.min()
        max_prob = probs.max()
        if min_prob < 0 or max_prob > 1.0:
            ErrorMapping.throw(InvalidDatasetError(dataset1=scored_data.name,
                                                   reason=f"{self.task.scored_prob_column} values should "
                                                   "between 0.0 and 1.0."))

    def _verify_label(self, scored_data: DataTable, test_data: DataTable = None):
        # verify scored label classes not more than 2
        scored_labels = scored_data.get_column(self.task.scored_label_column).dropna().unique()
        self._verify_binary_label(labels=scored_labels, column_name=self.task.scored_label_column,
                                  dataset_name=scored_data.name)

        # verify true label classes not more than 2
        if self.task.port_scheme == PortScheme.OnePort:
            true_label_column = self.task.true_label_column
            true_labels = scored_data.get_column(col_key=true_label_column).dropna().unique()
            true_label_dataset = scored_data.name
        else:
            true_label_column = get_label_column_name(test_data.data_frame)
            true_labels = test_data.get_column(col_key=true_label_column).dropna().unique()
            true_label_dataset = test_data.name
        self._verify_binary_label(labels=true_labels, column_name=true_label_column, dataset_name=true_label_dataset)

        # verify true label and scored label classes not more than 2
        labels = np.concatenate([scored_labels, true_labels])
        if len(set(labels)) > 2:
            ErrorMapping.throw(
                NotExpectedLabelColumnError(dataset_name=true_label_dataset, column_name=true_label_column,
                                            reason=f"{true_label_column} column is not consistent "
                                            f"with {self.task.scored_label_column} column."))

    @staticmethod
    def _verify_binary_label(labels, column_name: str, dataset_name: str):
        if len(labels) > 2 or len(labels) < 1:
            ErrorMapping.throw(
                NotExpectedLabelColumnError(dataset_name=dataset_name, column_name=column_name,
                                            reason=f"the label class number of valid instances is "
                                            f"more than 2 or less than 1"))

    def _process_data(self, scored_data: DataTable, test_data: DataTable = None):
        super()._process_data(scored_data, test_data)
        self._drop_instances_with_missing_values(df=scored_data.data_frame, column_names=[self.task.scored_prob_column])
        self._verify_probability(scored_data)
        self._verify_label(scored_data, test_data)

        if self.task.port_scheme == PortScheme.TwoPort:
            self._convert_column_to_string(dt=scored_data, column_key=self.task.user_column)
            self._convert_column_to_string(dt=scored_data, column_key=self.task.item_column)

    def _collect_data(self, scored_data: DataTable, test_data: DataTable = None):
        # before label encoder has been built, any instances with valid prob should not been dropped
        # to avoid missing label info
        with TimeProfile("Build Label encoder"):
            if self.task.port_scheme == PortScheme.OnePort:
                label_encoder = self._build_label_encoder(scored_data)
            else:
                label_encoder = self._build_label_encoder(scored_data, test_data)

        # merge scored data and test data to meet the same format of one port scheme
        scored_data_df = scored_data.data_frame
        if self.task.port_scheme == PortScheme.OnePort:
            scored_data_df = scored_data_df.rename(columns={self.task.true_label_column: TRUE_LABEL,
                                                            self.task.scored_prob_column: SCORED_PROB,
                                                            self.task.scored_label_column: SCORED_LABEL})
        if self.task.port_scheme == PortScheme.TwoPort:
            scored_data_df = scored_data_df.rename(columns={self.task.scored_prob_column: SCORED_PROB,
                                                            self.task.scored_label_column: SCORED_LABEL,
                                                            self.task.user_column: USER_COLUMN,
                                                            self.task.item_column: ITEM_COLUMN})
            test_data_df = test_data.data_frame
            test_data_df = test_data_df.rename(columns={get_user_column_name(test_data_df): USER_COLUMN,
                                                        get_item_column_name(test_data_df): ITEM_COLUMN,
                                                        get_label_column_name(test_data_df): TRUE_LABEL})
            scored_data_df = pd.merge(left=test_data_df, right=scored_data_df, how='right',
                                      on=[USER_COLUMN, ITEM_COLUMN])
            self._drop_instances_with_missing_values(df=scored_data_df, column_names=[USER_COLUMN, ITEM_COLUMN])
            if scored_data_df[TRUE_LABEL].isnull().any():
                ErrorMapping.throw(InvalidDatasetError(dataset1=test_data.name,
                                                       reason=f"cannot find true label in {test_data.name}"))

        self._drop_instances_with_missing_values(df=scored_data_df, column_names=[TRUE_LABEL, SCORED_LABEL])
        # encode true labels and scored labels
        scored_data_df[TRUE_LABEL] = label_encoder.transform(scored_data_df[TRUE_LABEL])
        scored_data_df[SCORED_LABEL] = label_encoder.transform(scored_data_df[SCORED_LABEL])

        return scored_data_df[[TRUE_LABEL, SCORED_LABEL, SCORED_PROB]],

    def _calculate(self, label_prob_df: pd.DataFrame):
        """Calculate classification task metrics with label_prob_df.

        :param label_prob_df: pd.DataFrame. The column should be [TRUE_LABEL, SCORED_LABEL, SCORED_PROB],
        where TRUE_LABEL column indicates true labels, and SCORED_LABEL column indicates scored labels, and SCORED_PROB
        column indicates scored probabilities column.
        :return: dict, where key is metric name and value is metric value.
        """
        # if no valid instances, return NAN metrics
        if label_prob_df.shape[0] == 0:
            module_logger.info("Found no valid scored instances.")
            metric_values = dict((metric.name, np.nan) for metric in self.metrics)
            return metric_values

        true_label = label_prob_df[TRUE_LABEL]
        pred_label = label_prob_df[SCORED_LABEL]
        pred_prob = label_prob_df[SCORED_PROB]

        metric_values = {}
        for metric in self.metrics:
            with TimeProfile(f"Calculate {metric.name} metric"):
                metric_values[metric.name] = metric(true_label, pred_label, pred_prob)

        return metric_values

    def _build_label_encoder(self, scored_data: DataTable, test_data: DataTable = None):
        label_encoder = BinaryNamedLabelEncoder()
        scored_label_column = self.task.scored_label_column
        scored_prob_column = self.task.scored_prob_column

        scored_label_prob_df = scored_data.data_frame[[scored_label_column, scored_prob_column]]
        scored_label_prob_group = scored_label_prob_df.groupby(scored_label_column)

        scored_min_probs = scored_label_prob_group.min().reset_index()
        scored_max_probs = scored_label_prob_group.max().reset_index()

        # decide positive and negative labels
        if len(scored_label_prob_group.groups) == 1:
            if scored_min_probs[scored_prob_column].iloc[0] >= self._THRESHOLD:
                label_encoder.positive_label = scored_min_probs[scored_label_column].iloc[0]
            elif scored_max_probs[scored_prob_column].iloc[0] <= self._THRESHOLD:
                label_encoder.negative_label = scored_max_probs[scored_label_column].iloc[0]
        else:
            # collect label 0 infos
            scored_label_0 = scored_min_probs[scored_label_column].iloc[0]
            scored_label_0_min_prob = scored_min_probs[scored_prob_column].iloc[0]
            scored_label_0_max_prob = scored_max_probs[scored_prob_column].iloc[0]

            # collect label 1 infos
            scored_label_1 = scored_min_probs[scored_label_column].iloc[1]
            scored_label_1_min_prob = scored_min_probs[scored_prob_column].iloc[1]
            scored_label_1_max_prob = scored_max_probs[scored_prob_column].iloc[1]

            if scored_label_1_max_prob <= self._THRESHOLD <= scored_label_0_min_prob:
                label_encoder.positive_label = scored_label_0
                label_encoder.negative_label = scored_label_1
            elif scored_label_0_max_prob <= self._THRESHOLD <= scored_label_1_min_prob:
                label_encoder.positive_label = scored_label_1
                label_encoder.negative_label = scored_label_0

        if label_encoder.negative_label is None and label_encoder.positive_label is None:
            ErrorMapping.throw(
                NotExpectedLabelColumnError(dataset_name=scored_data.name, column_name=scored_label_column,
                                            reason="There is a mismatch between probability column and label column, "
                                                   "this dataset was not generated by a legal binary classifier."))

        # fill missing labels in scored labels according to the true labels
        if test_data is None:
            true_labels = scored_data.get_column(self.task.true_label_column).dropna().unique()
        else:
            true_labels = test_data.get_column(get_label_column_name(test_data.data_frame)).dropna().unique()

        missing_label = set(true_labels) - set(scored_data.get_column(scored_label_column).dropna().unique())
        if missing_label:
            label_encoder.fill_missing_label(label=missing_label.pop())

        return label_encoder
