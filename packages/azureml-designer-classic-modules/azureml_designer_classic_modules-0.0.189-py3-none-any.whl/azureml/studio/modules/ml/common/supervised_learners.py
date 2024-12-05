import pandas as pd
from azureml.studio.common.error import ErrorMapping, InvalidTrainingDatasetError
from azureml.studio.core.data_frame_schema import ElementTypeName
from azureml.studio.core.logger import module_logger
from azureml.studio.core.utils.strutils import profile_column_names
from azureml.studio.modules.datatransform.common.named_encoder import MAX_CATEGORY_COUNT
from azureml.studio.modules.ml.common.base_learner import BaseLearner
from azureml.studio.modules.ml.common.constants import ScoreColumnConstants
from azureml.studio.modules.ml.common.ml_utils import filter_column_names_with_prefix


class BinaryClassificationLearner(BaseLearner):
    def check_label_column(self, data_table):
        super().check_label_column(data_table)
        # For a binary classification task, the label column should contain two categories label.
        label_series = data_table.get_column(self.label_column_name)
        with pd.option_context('use_inf_as_na', True):
            categories = label_series.dropna().unique()
        if len(categories) != 2:
            ErrorMapping.throw(InvalidTrainingDatasetError(
                # Make sure data_name is not None to avoid exception template mismatch
                data_name='Dataset' if data_table.name is None else data_table.name,
                learner_type="Binary classifier",
                reason=f'The number of label classes should equal to 2, got {len(categories)} classes'))

    def _build_result_dataframe(self, label, prob):
        result_df = pd.DataFrame()
        # If prob contains the probabilities of each class, choose the positive class probability
        if len(prob.shape) == 2:
            # Tree model like boosted decision tree and decision forest support one class label data,
            # but the boosted decision tree will return [n, 2] with trained label in first column
            # while decision forest return [n, 1]
            # label_classes_len takes the number of classes
            # and choose the last one as the positive label column id.
            classes_attr = getattr(self.model, 'classes_', None)
            # classes_attr will be numpy.array or None,
            # So use classes_attr is not None to check it is not null,
            # use classes_attr.size != 0 to test it is not empty.
            # Simply use 'if classes_attr' will fail if classes_attr is array.
            if classes_attr is not None and classes_attr.size != 0:
                classes_num = classes_attr.size
                module_logger.info(f"Found {classes_num} label classes in classes_ attribute.")
                label_column_index = classes_num - 1
                module_logger.info(f"Using {label_column_index} as probability column.")
            else:
                label_column_index = 1
                module_logger.info(f"Take the second column as probability column by default.")

            prob = prob[:, label_column_index]
        result_df[ScoreColumnConstants.ScoredLabelsColumnName] = \
            self.normalizer.inverse_transform(label, label_column=self.label_column_name)
        result_df[ScoreColumnConstants.ScoredProbabilitiesColumnName] = prob
        return result_df

    def generate_score_column_meta(self, predict_df):
        """Build score_column_names dict
        Map BinaryClassScoredLabelType to ScoredLabelsColumnName
        Map CalibratedScoreType To ScoredProbabilitiesColumnName
        When evaluating the scored data, infer the task task with the {TaskType}ScoreLabelType key.

        :return: built score column names dict
        """
        score_columns = {}
        score_columns[ScoreColumnConstants.BinaryClassScoredLabelType] = ScoreColumnConstants.ScoredLabelsColumnName
        score_columns[ScoreColumnConstants.CalibratedScoreType] = ScoreColumnConstants.ScoredProbabilitiesColumnName
        module_logger.info("Binary Classification Model Scored Columns are: ")
        module_logger.info(
            f'There are {len(score_columns.keys())} score columns: '
            f'"{profile_column_names(list(score_columns.keys()))}"')
        return score_columns


class MultiClassificationLearner(BaseLearner):
    def check_label_column(self, data_table):
        super().check_label_column(data_table)
        # For a multi-class classification task, the label column should contain more than 1 categories.
        label_series = data_table.get_column(self.label_column_name)
        categories = label_series.dropna().unique()
        if len(categories) < 2:
            ErrorMapping.throw(InvalidTrainingDatasetError(
                data_name=data_table.name,
                learner_type="Multi-class classifier",
                reason=f'The number of label classes should > 1, got {len(categories)} classes'))
        if len(categories) > MAX_CATEGORY_COUNT:
            module_logger.warning("Too many unique values in the label column.")
            if data_table.get_element_type(self.label_column_name) == ElementTypeName.FLOAT:
                module_logger.warning("The label column is of float type and contains too many unique values. "
                                      "Regression Model is probably a better choice.")

    def _build_result_dataframe(self, label, prob):
        """Build scored probability column names with the training labels

        e.g. If the training dataset contains 4 different labels: bird, cat, dog and fish, then the column names
        of the scored dataset would be "Scored Probabilities_bird", "Scored Probabilities_cat",
        "Scored Probabilities_dog" and "Scored Probabilities_fish".
        """
        label_category_list = self.normalizer.label_column_encoders[self.label_column_name].label_mapping

        def _gen_scored_probability_column_name(label):
            """Generate scored probability column names with pattern "Scored Probabilities_label" """
            return '_'.join((ScoreColumnConstants.ScoredProbabilitiesMulticlassColumnNamePattern, str(label)))

        if len(prob.shape) == 1:
            # This is for bug 776394. The root cause is sklearn.multiclass. OneVsOneClassifier would generate
            # prob with shape (n_samples,) when label class number is 2 in the training dataset. For details, please
            # refer to OneVsOneClassifier document of sklearn.
            positive_prob = prob
            negative_prob = 1 - prob
            result_df = pd.DataFrame(dict(zip([_gen_scored_probability_column_name(i) for i in label_category_list],
                                              [negative_prob, positive_prob])))
        else:
            result_df = pd.DataFrame(data=prob,
                                     columns=[_gen_scored_probability_column_name(i) for i in label_category_list])
        result_df[ScoreColumnConstants.ScoredLabelsColumnName] = \
            self.normalizer.inverse_transform(label, label_column=self.label_column_name)
        return result_df

    def generate_score_column_meta(self, predict_df):
        """Build score_column_names dict
        Map MultiClassScoredLabelType to ScoredLabelsColumnName
        Map ScoredProbabilitiesMulticlassColumnTypePattern_X to
                ScoredProbabilitiesMulticlassColumnTypePattern_X FOR EVERY CLASS X

        :return: built score column names dict
        """
        score_columns = {x: x for x in filter_column_names_with_prefix(
            predict_df.columns, prefix=ScoreColumnConstants.ScoredProbabilitiesMulticlassColumnNamePattern)}
        score_columns[ScoreColumnConstants.MultiClassScoredLabelType] = ScoreColumnConstants.ScoredLabelsColumnName
        module_logger.info("Multi-class Classification Model Scored Columns are: ")
        module_logger.info(
            f'There are {len(score_columns.keys())} score columns: '
            f'"{profile_column_names(list(score_columns.keys()))}"')
        return score_columns


class RegressionLearner(BaseLearner):
    def check_label_column(self, data_table):
        # support non-numeric regression label as V1, will use OrdinalEncoder to convert non-numeric label to numeric.
        super().check_label_column(data_table)

    def _build_result_dataframe(self, label, prob):
        result_df = pd.DataFrame()
        result_df[ScoreColumnConstants.ScoredLabelsColumnName] = label
        return result_df

    def generate_score_column_meta(self, predict_df):
        """Build score_column_names dict
        Map RegressionScoredLabelType to ScoredLabelsColumnName
        :return: built score column names dict
        """
        score_columns = {}
        score_columns[ScoreColumnConstants.RegressionScoredLabelType] = ScoreColumnConstants.ScoredLabelsColumnName
        module_logger.info("Regression Model Scored Columns: ")
        module_logger.info(
            f'There are {len(score_columns.keys())} score columns: '
            f'"{profile_column_names(list(score_columns.keys()))}"')
        return score_columns
