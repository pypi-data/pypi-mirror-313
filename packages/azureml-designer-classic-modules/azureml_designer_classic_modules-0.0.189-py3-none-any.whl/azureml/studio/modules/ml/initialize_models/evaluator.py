from abc import abstractmethod
import numpy as np
import pandas as pd
from pandas.core.dtypes.common import is_categorical_dtype
from sklearn.metrics import (accuracy_score, confusion_matrix, mean_absolute_error, precision_score, r2_score,
                             recall_score, roc_auc_score)
import azureml.studio.modules.ml.common.metric_calculator as metric_calculator
from azureml.studio.common.datatable import data_type_conversion
from azureml.studio.common.error import (NotExpectedLabelColumnError, ErrorMapping, NotScoredDatasetError,
                                         InvalidDatasetError, FailedToCompleteOperationError)
from azureml.studio.core.schema import ColumnTypeName
from azureml.studio.core.logger import TimeProfile, module_logger
from azureml.studio.modulehost.constants import ElementTypeName
from azureml.studio.modules.datatransform.common.named_encoder import NamedLabelEncoder, BinaryNamedLabelEncoder
from azureml.studio.modules.ml.common.constants import META_PROPERTY_LABEL_ENCODER_KEY, ScoreColumnConstants
from azureml.studio.modules.ml.common.ml_utils import TaskType, drop_illegal_label_instances
from azureml.studio.modules.ml.common.report_data import ReportData, ReportNameConstants
from azureml.studio.modules.ml.common.plot import plot_confusion_matrix
from azureml.studio.common.datatable.data_type_conversion import convert_column_by_element_type
from azureml.studio.modules.ml.common.ml_utils import filter_column_names_with_prefix

SCORED_DATA_CM_NAME = 'left_port_confusion_matrix'
SCORED_DATA_TO_COMPARE_CM_NAME = 'right_port_confusion_matrix'
PLOT_NUM_CLASSES_LIMIT = 30


class BaseEvaluator:
    task_type = None
    default_predict_column = ScoreColumnConstants.ScoredProbabilitiesColumnName
    score_column_key = ScoreColumnConstants.CalibratedScoreType
    default_scored_label_column_name = None

    def __init__(self, to_compare=False):
        self.is_to_compare = to_compare
        self.label_column_name = None

    @abstractmethod
    def _evaluate(self, df, meta_data, output_metrics):
        pass

    def evaluate_data(self, scored_data, dataset_name, output_metrics=True):
        """Evaluate scored data, generate evaluation result and visualization information.

        :param scored_data: DataTable, scored dataset.
        :param dataset_name: str, scored dataset's friendly name.
        :param output_metrics: bool, whether to output metrics.
        :return: evaluate_result: dataframe
                 visualization information: Report Data. Only the binary-classifier will return non-None data.
        """
        self.dataset_name = dataset_name
        if scored_data is None:
            module_logger.info("Got an Empty Scored Data Instance")
            return None, None
        df = scored_data.data_frame
        self.label_column_name = scored_data.meta_data.label_column_name
        module_logger.info(f"Evaluate data set with {self.label_column_name} as Label Column.")
        self._drop_missing_label_instance(df)
        self._update_scored_label_column(meta_data=scored_data.meta_data)
        if isinstance(self.scored_label_column_name, list):
            for name in self.scored_label_column_name:
                if name not in df.columns:
                    ErrorMapping.throw(NotScoredDatasetError(dataset_name=dataset_name))
        elif self.scored_label_column_name not in df.columns:
            ErrorMapping.throw(NotScoredDatasetError(dataset_name=dataset_name))
        return self._evaluate(df, meta_data=scored_data.meta_data, output_metrics=output_metrics)

    def _drop_missing_label_instance(self, df):
        drop_illegal_label_instances(df, column_name=self.label_column_name, task_type=self.task_type)

    def _update_scored_label_column(self, meta_data):
        """Update scored label column name if score_column_names existing in data table

        default scored_label_column_name is set to compatible with previous version data table
        new version data table contains score column names info, so update score_column_name with new data table
        :param meta_data: DataFrameSchema
        :return: None
        self.score_label_column will be updated if score_column_names of scored data is not empty.
        """
        if self.score_column_key in meta_data.score_column_names:
            self.scored_label_column_name = meta_data.score_column_names[self.score_column_key]
        elif self._use_default_scored_column_names(meta_data):
            self.scored_label_column_name = self.default_scored_label_column_name

    @staticmethod
    def _drop_missing_scored_column_instance(df, required_scored_columns):
        module_logger.info(f"Remove missing scored column values instances, "
                           f"required scored column f{', '.join(required_scored_columns)}")
        with pd.option_context('use_inf_as_na', True):
            df.dropna(subset=required_scored_columns, inplace=True)
        df.reset_index(drop=True, inplace=True)

    @staticmethod
    def _use_default_scored_column_names(meta_data):
        scored_data_info = meta_data.extended_properties
        return (scored_data_info is None or
                not scored_data_info.get('is_scored_data', False) and
                not scored_data_info.get('learner_type', None))


class BinaryClassificationEvaluator(BaseEvaluator):
    task_type = TaskType.BinaryClassification
    scored_label_column_name = ScoreColumnConstants.ScoredLabelsColumnName
    score_column_key = ScoreColumnConstants.BinaryClassScoredLabelType
    # this scored label column name is for scored columns described with constant names
    default_scored_label_column_name = ScoreColumnConstants.BinaryClassScoredLabelColumnName
    default_scored_prob_column_name = ScoreColumnConstants.BinaryClassScoredProbabilitiesColumnName

    def _calculate(self, y_true, y_prob, y_pred_label):
        """Calculate Binary Classification Task Metrics"""
        with TimeProfile("Calculating confusion matrix, AUC, Accuracy, Precision, Recall, F1"):
            # if no valid instances, return expected metric results directly
            # these default metric values are set refer to V1 results
            metric_names = ['AUC', 'Accuracy', 'Precision', 'Recall', 'F1', 'True Negative', 'False Positive',
                            'False Negative', 'True Positive']
            if len(y_true) == 0:
                metric_values = [np.nan] + [0] * (len(metric_names) - 1)
                results = dict(zip(metric_names, metric_values))
                results['Precision'] = 1.0
                return pd.DataFrame([results])

            # in confusion_matrix, confusion_matrix[i,j] means the number of instances whose
            # true label is category i while predicted label is category j.
            flatten_metric = metric_calculator.confusion_metric_flat(y_true, y_pred_label)
            if len(flatten_metric) == 4:
                # legal binary classification scored data: return 4 items, including tn, fp, fn, tp.
                tn, fp, fn, tp = flatten_metric
            elif len(flatten_metric) == 1:
                # if the number of category(label+predicted label) is 1, the returned matrix dimension would be 1 * 1.
                # so the length of flatten confusion matrix would be 1.
                tn, fp, fn, tp = 0, 0, 0, 0
                if self.label_encoder.positive_label is not None:
                    # positive label is existing, then the input instances are positive instances.
                    tp, = flatten_metric
                else:
                    tn, = flatten_metric
            else:
                ErrorMapping.throw(NotExpectedLabelColumnError(
                    dataset_name=self.dataset_name,
                    column_name=','.join([self.label_column_name, self.scored_label_column_name]),
                    reason=f"The number of classes in {self.label_column_name} and {self.scored_label_column_name} "
                    f"should not be greater than 2."))

            label_category = np.unique(y_true)
            auc = roc_auc_score(y_true, y_prob) if len(label_category) == 2 else 0.0
            # Since the quantity has been counted, use the statistical data directly to avoid redundant computation.
            valid_instance_count = tn + fp + fn + tp
            accuracy = metric_calculator.safe_divide(tn + tp, valid_instance_count)
            precision = metric_calculator.safe_divide(tp, tp + fp)
            recall = metric_calculator.safe_divide(tp, tp + fn)
            f1 = 2 * metric_calculator.safe_divide(recall * precision, recall + precision)

            metric_values = [auc, accuracy, precision, recall, f1, tn, fp, fn, tp]
            results = dict(zip(metric_names, metric_values))
        return pd.DataFrame([results])

    def _evaluate(self, df, meta_data, output_metrics):
        self.prob_column_name = self._get_prob_column(meta_data)
        ErrorMapping.verify_element_type(type_=meta_data.get_column_type(self.prob_column_name),
                                         expected_type=ColumnTypeName.NUMERIC,
                                         column_name=self.prob_column_name,
                                         arg_name=self.dataset_name)
        # encode input labels into 0,1 label
        self._encode_label_column(df)
        y_true = df[self.label_column_name]
        y_pred_label = df[self.scored_label_column_name]
        y_prob = df[self.prob_column_name]
        result_df = self._calculate(y_true, y_prob, y_pred_label)
        # build visualization json
        report_name = ReportNameConstants.ToComparedDataReportName if self.is_to_compare \
            else ReportNameConstants.ScoredDataReportName
        report_res = ReportData(df=df[[self.prob_column_name, self.label_column_name]],
                                report_name=report_name,
                                auc=result_df['AUC'][0],
                                prob_column_name=self.prob_column_name,
                                label_column_name=self.label_column_name,
                                positive_label=self.label_encoder.positive_label,
                                negative_label=self.label_encoder.negative_label)
        return result_df, report_res

    def _get_prob_column(self, meta_data):
        if ScoreColumnConstants.CalibratedScoreType in meta_data.score_column_names:
            prob_column_name = meta_data.score_column_names[ScoreColumnConstants.CalibratedScoreType]
        elif self.default_scored_prob_column_name in meta_data.column_attributes.names:
            prob_column_name = self.default_scored_prob_column_name
        else:
            prob_column_name = ScoreColumnConstants.ScoredProbabilitiesColumnName

        # add scored prob column validation for bug 741372.
        if prob_column_name not in set(meta_data.column_attributes.names):
            ErrorMapping.throw(NotScoredDatasetError(
                column_name=prob_column_name,
                dataset_name=self.dataset_name,
                troubleshoot_hint=f'Please ensure "{prob_column_name}" column exists because it is required for '
                f'"{self.task_type.name}" evaluator to calculate metrics like "AUC".'))

        return prob_column_name

    def detect_label_mapping(self, df):
        """Detect label mapping with scored label column and scored probability column

        Here is a summary of the detection logic. For example, the input df is:
               Label  Prob
            0      0  0.01
            1      1  0.51
            2      0  0.49
            3      1  0.78

        Then, we groupby the df with label column and groupby result looks like:
            0: [0.01, 0.49]
            1: [0.51, 0.78]

        After that, we could use the min() and max() function to get the min/max probability values of each label.
        Finally, we use the min/max probability values to identify which label is positive and which is negative.
        """
        # verify if prob columns is in the [0,1] range
        if 0 > df[self.prob_column_name].min() or 1 < df[self.prob_column_name].max():
            ErrorMapping.throw(
                FailedToCompleteOperationError(failed_operation="Evaluating",
                                               reason=f"The {self.prob_column_name} column is not in the range [0,1]"))

        groupby_result = df.groupby(self.scored_label_column_name)
        min_prob_df = groupby_result.min().reset_index()

        threshold = 0.5  # 0.5 is the default threshold of the sigmoid function.
        label_count = len(groupby_result.groups)
        if label_count > 2:
            # since the evaluator evaluate the binary model scored data, the number of classes of the label columns
            # could not greater than 2
            ErrorMapping.throw(
                NotExpectedLabelColumnError(dataset_name=self.dataset_name, column_name=self.scored_label_column_name,
                                            reason="The number of classes in scored label is more than 2."))
        elif label_count == 1:
            label = min_prob_df[self.scored_label_column_name].iloc[0]
            min_prob = min_prob_df[self.prob_column_name].iloc[0]
            if min_prob >= threshold:
                self.label_encoder.positive_label = label
            else:
                self.label_encoder.negative_label = label
        elif label_count == 2:
            # label_count == 2
            max_prob_df = groupby_result.max().reset_index()

            label_0 = min_prob_df[self.scored_label_column_name].iloc[0]
            label_1 = min_prob_df[self.scored_label_column_name].iloc[1]

            label_0_min_prob = min_prob_df[self.prob_column_name].iloc[0]
            label_1_min_prob = min_prob_df[self.prob_column_name].iloc[1]

            label_0_max_prob = max_prob_df[self.prob_column_name].iloc[0]
            label_1_max_prob = max_prob_df[self.prob_column_name].iloc[1]

            if label_1_max_prob <= threshold <= label_0_min_prob:
                self.label_encoder.positive_label = label_0
                self.label_encoder.negative_label = label_1
            elif label_0_max_prob <= threshold <= label_1_min_prob:
                self.label_encoder.positive_label = label_1
                self.label_encoder.negative_label = label_0
            else:
                labels = df[self.scored_label_column_name].unique()
                if len(labels) == 1:
                    if labels[0] == label_1:
                        # when there is one label with valid probabilities, ensure the this label is represented by
                        # the label_0, and the other is in the label_1.
                        label_0, label_1 = label_1, label_0
                        label_0_min_prob, label_1_min_prob = label_1_min_prob, label_0_min_prob
                        label_0_max_prob, label_1_max_prob = label_1_max_prob, label_0_max_prob
                    if label_0_max_prob <= threshold:
                        self.label_encoder.positive_label = label_1
                        self.label_encoder.negative_label = label_0
                    elif label_0_min_prob >= threshold:
                        self.label_encoder.positive_label = label_0
                        self.label_encoder.negative_label = label_1
                elif len(labels) == 0:
                    self.label_encoder.positive_label, self.label_encoder.negative_label = label_0, label_1

                if self.label_encoder.positive_label is None or self.label_encoder.negative_label is None:
                    ErrorMapping.throw(NotExpectedLabelColumnError(
                        dataset_name=self.dataset_name,
                        column_name=self.scored_label_column_name,
                        reason="there is a mismatch between probability column and label column, this dataset "
                               "was not generated by a legal binary classifier"))

    def _encode_label_column(self, df):
        self.label_encoder = BinaryNamedLabelEncoder()
        self._drop_missing_scored_column_instance(df, required_scored_columns=[self.prob_column_name,
                                                                               self.scored_label_column_name])
        # Note that the detect_label_mapping method is not expected to handle nan and inf values
        self.detect_label_mapping(df[[self.prob_column_name, self.scored_label_column_name]])
        module_logger.info(f"Infer label mapping from scored label column: "
                           f"positive label is {self.label_encoder.positive_label} "
                           f"and negative label is {self.label_encoder.negative_label}.")
        if is_categorical_dtype(df[self.label_column_name]):
            # Since the train model module uncategory the label column, the scored label will not be 'category' type
            # To compare the label column and the scored label column, label column should be uncategoired as what
            # we do during training.
            df[self.label_column_name] = data_type_conversion.convert_column_by_element_type(
                column=df[self.label_column_name],
                new_type=ElementTypeName.UNCATEGORY)
        for label_str in df[self.label_column_name]:
            if label_str in self.label_encoder.transform_dict:
                continue
            # if the label column contains element which is not in the scored label column
            # then try to fill missing label mapping
            if self.label_encoder.fill_missing_label(label_str) is None:
                # label encoder does not contain missing value, which means label column is inconsistent with
                # training label throw an error to inform user.
                ErrorMapping.throw(
                    NotExpectedLabelColumnError(dataset_name=self.dataset_name, column_name=self.label_column_name,
                                                reason="Label column is not consistent with training label column."))

        module_logger.info(f"Infer label mapping from scored label and label column: "
                           f"positive label is {self.label_encoder.positive_label} "
                           f"and negative label is {self.label_encoder.negative_label}.")
        module_logger.info('Perform transforming category label into numeric label.')
        with TimeProfile("Encoding label column"):
            df[self.label_column_name] = self.label_encoder.transform(df[self.label_column_name])
            if self.label_column_name != self.scored_label_column_name:
                df[self.scored_label_column_name] = self.label_encoder.transform(df[self.scored_label_column_name])


class MultiClassificationEvaluator(BaseEvaluator):
    task_type = TaskType.MultiClassification
    scored_label_column_name = ScoreColumnConstants.ScoredLabelsColumnName
    score_column_key = ScoreColumnConstants.MultiClassScoredLabelType
    # this scored label column name is for scored columns described with constant names
    default_scored_label_column_name = ScoreColumnConstants.MultiClassScoredLabelColumnName

    def _calculate(self, y_true, y_pred):
        if len(y_pred.shape) != 1 and y_pred.shape[-1] != 1:
            y_pred = np.argmax(y_pred, axis=1)
        with TimeProfile("Calculating Overall_Accuracy, Micro_Precision, Macro_Precision, Micro_Recall, Macro_Recall"):
            results = {
                'Overall_Accuracy': accuracy_score(y_true, y_pred),
                'Micro_Precision': precision_score(y_true, y_pred, average='micro'),
                'Macro_Precision': precision_score(y_true, y_pred, average='macro'),
                'Micro_Recall': recall_score(y_true, y_pred, average='micro'),
                'Macro_Recall': recall_score(y_true, y_pred, average='macro'),
                # 'Confusion_Matrix': confusion_matrix(y_true, y_pred)
            }
        return pd.DataFrame([results])

    def _evaluate(self, df, meta_data, output_metrics):
        # Up till now, the visualization information of the multi-class classifier scored data is None.
        self._encode_label_column(df)
        y_true = df[self.label_column_name]
        y_pred_label = df[self.scored_label_column_name]
        result_df = self._calculate(y_true, y_pred_label)
        num_classes = len(self.label_encoder.label_mapping) if hasattr(self, 'label_encoder') else 0
        # plot within limited class num to avoid plt plot issue in large figure.
        if output_metrics and num_classes < PLOT_NUM_CLASSES_LIMIT:
            plot_name = SCORED_DATA_TO_COMPARE_CM_NAME if self.is_to_compare else SCORED_DATA_CM_NAME
            # plot confusion matrix plt figure as visualization information of multi-class classifier scored data.
            try:
                with TimeProfile("Plotting confusion matrix"):
                    plot_confusion_matrix(
                        confusion_matrix=confusion_matrix(y_true, y_pred_label, normalize='true'),
                        display_labels=[str(label) for label in self.label_encoder.label_mapping],
                        plot_name=plot_name)
            except Exception as e:
                module_logger.warning(f"Failed to plot confusion matrix because {e}.")

        return result_df, None

    def _encode_label_column(self, df):
        self._drop_missing_scored_column_instance(df, required_scored_columns=[self.scored_label_column_name])
        if df.shape[0] == 0:
            return
        self.label_encoder = NamedLabelEncoder('label_column')
        with TimeProfile("Encoding label column"):
            if is_categorical_dtype(df[self.label_column_name]):
                df[self.label_column_name] = data_type_conversion.convert_column_by_element_type(
                    column=df[self.label_column_name],
                    new_type=ElementTypeName.UNCATEGORY)
            if is_categorical_dtype(df[self.scored_label_column_name]):
                df[self.scored_label_column_name] = data_type_conversion.convert_column_by_element_type(
                    column=df[self.scored_label_column_name],
                    new_type=ElementTypeName.UNCATEGORY)

            all_labels = pd.concat(
                [df[self.label_column_name], df[self.scored_label_column_name]],
                axis=0
            )
            try:
                self.label_encoder.fit(all_labels)
            except TypeError as e:
                # the data type of the label column provided for evaluation is not consistent with the training one.
                if "argument must be a string or number" in str(e.args):
                    ErrorMapping.rethrow(e, NotExpectedLabelColumnError(
                        dataset_name=self.dataset_name,
                        column_name=self.label_column_name,
                        reason="Label column is not consistent with training label column."
                    ))
                raise e
            df[self.label_column_name] = self.label_encoder.transform(df[self.label_column_name])
            if self.label_column_name != self.scored_label_column_name:
                df[self.scored_label_column_name] = self.label_encoder.transform(df[self.scored_label_column_name])


class RegressionEvaluator(BaseEvaluator):
    task_type = TaskType.Regression
    scored_label_column_name = ScoreColumnConstants.ScoredLabelsColumnName
    score_column_key = ScoreColumnConstants.RegressionScoredLabelType
    # this scored label column name is for scored columns described with constant names
    default_scored_label_column_name = ScoreColumnConstants.RegressionScoredLabelColumnName

    def _calculate(self, y_true, y_pred):
        with TimeProfile(
                "Calculating Mean_Absolute_Error, Root_Mean_Squared_Error, Relative_Squared_Error,"
                " Relative_Absolute_Error, Coefficient_of_Determination"):

            metric_names = ['Mean_Absolute_Error', 'Root_Mean_Squared_Error', 'Relative_Squared_Error',
                            'Relative_Absolute_Error', 'Coefficient_of_Determination']
            if len(y_true) > 0:
                metric_values = [mean_absolute_error(y_true, y_pred),
                                 metric_calculator.root_mean_squared_error(y_true, y_pred),
                                 metric_calculator.relative_squared_error(y_true, y_pred),
                                 metric_calculator.relative_absolute_error(y_true, y_pred),
                                 r2_score(y_true, y_pred)]
            else:
                # these default metric values are set refer to V1 results
                metric_values = [np.nan] * len(metric_names)
            results = dict(zip(metric_names, metric_values))

        return pd.DataFrame([results])

    def _encode_non_numeric_labels(self, df, meta_data):
        y_true = df[self.label_column_name]
        y_pred = df[self.scored_label_column_name]
        label_column_type = meta_data.get_column_type(self.label_column_name)
        scored_label_column_type = meta_data.get_column_type(self.scored_label_column_name)
        # if both label columns and scored label columns are of numeric type, no need to encode labels
        if label_column_type == ColumnTypeName.NUMERIC and scored_label_column_type == ColumnTypeName.NUMERIC:
            return y_true, y_pred

        label_encoder = meta_data.extended_properties.get(META_PROPERTY_LABEL_ENCODER_KEY, None)
        # refer to fit label column encoders in the normalizer, which transfers categorical type values before fit
        if is_categorical_dtype(df[self.label_column_name]):
            y_true = data_type_conversion.convert_column_by_element_type(
                df[self.label_column_name], ElementTypeName.UNCATEGORY)
        if is_categorical_dtype(df[self.scored_label_column_name]):
            y_pred = data_type_conversion.convert_column_by_element_type(df[self.scored_label_column_name],
                                                                         ElementTypeName.UNCATEGORY)

        if label_encoder is None:
            # Considering the scored dataset maybe not generated by the builtin models, where label encoder cannot
            # exist, the design here is to encode predicted/true result according to current data if it is not
            # numeric. Note that if neither of true label and predicted label is numeric, the label encoder should fit
            # these two kinds of labels, so the encoded labels are comparable.
            label_encoder = NamedLabelEncoder('label_column')
            labels = []
            if label_column_type != ColumnTypeName.NUMERIC:
                labels.append(y_true)
            if scored_label_column_type != ColumnTypeName.NUMERIC:
                labels.append(y_pred)
            unfitted_labels = pd.concat(labels)
            if len(unfitted_labels) > 0:
                label_encoder.fit(unfitted_labels.reset_index(drop=True))
            else:
                return y_true, y_pred

        try:
            if label_column_type != ColumnTypeName.NUMERIC and len(y_true) > 0:
                y_true = label_encoder.transform(y_true)
            if scored_label_column_type != ColumnTypeName.NUMERIC and len(y_pred) > 0:
                y_pred = label_encoder.transform(y_pred)
        except ValueError as e:
            if "Found unknown categories" in str(e.args):
                ErrorMapping.rethrow(e, InvalidDatasetError(
                    dataset1=self.dataset_name,
                    reason="failed to transform scored dataset label column: "
                    f"{ErrorMapping.get_exception_message(e)}",
                    troubleshoot_hint="Please make sure scored dataset label column have the same categories "
                                      "as that of train for non-numeric label in regression task, "
                    f"train data label categories are {label_encoder.label_mapping}."
                ))
            else:
                raise e

        return y_true, y_pred

    def _evaluate(self, df, meta_data, output_metrics):
        self._drop_missing_scored_column_instance(df=df, required_scored_columns=[self.scored_label_column_name])
        # Up till now, the visualization information of the regression scored data is None.
        y_true, y_pred = self._encode_non_numeric_labels(df=df, meta_data=meta_data)

        return self._calculate(y_true, y_pred), None


class AnomalyDetectionEvaluator(BinaryClassificationEvaluator):
    task_type = TaskType.AnomalyDetection
    scored_label_column_name = ScoreColumnConstants.ScoredLabelsColumnName
    score_column_key = ScoreColumnConstants.AnomalyDetectionScoredLabelType
    # this scored label column name is for scored columns described with constant names
    default_scored_label_column_name = ScoreColumnConstants.AnomalyDetectionScoredLabelColumnName
    default_scored_prob_column_name = ScoreColumnConstants.AnomalyDetectionProbabilitiesColumnName

    def detect_label_mapping(self, df):
        groupby_result = df.groupby(self.label_column_name)
        min_prob_df = groupby_result.min().reset_index()
        threshold = 0.5  # 0.5 is the default threshold of the sigmoid function.
        label_count = len(groupby_result.groups)
        if label_count > 2:
            # since the evaluator evaluate the binary model scored data, the number of classes of the label columns
            # could not greater than 2
            ErrorMapping.throw(
                NotExpectedLabelColumnError(dataset_name=self.dataset_name, column_name=self.label_column_name,
                                            reason="The number of classes in scored label is more than 2."))
        elif label_count == 1:
            label = min_prob_df[self.label_column_name].iloc[0]
            min_prob = min_prob_df[self.prob_column_name].iloc[0]
            if min_prob >= threshold:
                self.label_encoder.positive_label = label
            else:
                self.label_encoder.negative_label = label
        else:
            module_logger.info('auto detect label mapping.')
            label_0 = min_prob_df[self.label_column_name].iloc[0]
            label_1 = min_prob_df[self.label_column_name].iloc[1]

            label_0_min_prob = min_prob_df[self.prob_column_name].iloc[0]
            label_1_min_prob = min_prob_df[self.prob_column_name].iloc[1]

            self.label_encoder.positive_label = label_0 if label_1_min_prob <= label_0_min_prob else label_1
            self.label_encoder.negative_label = label_1 if label_1_min_prob <= label_0_min_prob else label_0
            module_logger.info(f'positive label {self.label_encoder.positive_label}, '
                               f'negative label {self.label_encoder.negative_label}')

    def _encode_label_column(self, df):
        if self.label_column_name == self.prob_column_name:
            ErrorMapping.throw(
                NotExpectedLabelColumnError(dataset_name=self.dataset_name, column_name=self.label_column_name,
                                            reason="The label column cannot be scored probability column",
                                            troubleshoot_hint=f'Please use "Edit Metadata" module to set another '
                                            f'column as label column, instead of "{self.label_column_name}" column.'))

        self.label_encoder = BinaryNamedLabelEncoder()
        # fix bug 844022: convert category int label column to be uncategoried to support metric calculation.
        if is_categorical_dtype(df[self.label_column_name]):
            df[self.label_column_name] = data_type_conversion.convert_column_by_element_type(
                column=df[self.label_column_name],
                new_type=ElementTypeName.UNCATEGORY)

        # If input label series only has 0, 1, will not go encoding
        if set(df[self.label_column_name].unique()) == {0, 1}:
            self._drop_missing_scored_column_instance(df, required_scored_columns=[self.scored_label_column_name,
                                                                                   self.prob_column_name])
            # fix bug 1302761, the column may be a mix of int and bool, so the column type should be object,
            # for this case, we need to convert the column type
            df[self.label_column_name] = data_type_conversion.convert_column_by_element_type(
                column=df[self.label_column_name],
                new_type=ElementTypeName.INT)
            return

        self.detect_label_mapping(df[[self.prob_column_name, self.label_column_name]])
        module_logger.info(f"Infer label mapping from scored label column: "
                           f"positive label is {self.label_encoder.positive_label} "
                           f"and negative label is {self.label_encoder.negative_label}.")
        self._drop_missing_scored_column_instance(df, required_scored_columns=[self.scored_label_column_name,
                                                                               self.prob_column_name])
        # if scored labels contains values not are 0 or 1, then the scored labels also need to be encoded
        is_encode_scored_labels = not set(df[self.scored_label_column_name].unique()).issubset({0, 1})
        if is_encode_scored_labels:
            for label_str in df[self.scored_label_column_name]:
                if label_str in self.label_encoder.transform_dict:
                    continue
                # if the label column contains element which is not in the scored label column
                # then try to fill missing label mapping
                if self.label_encoder.fill_missing_label(label_str) is None:
                    # label encoder does not contain missing value, which means label column is inconsistent with
                    # training label throw an error to inform user.
                    ErrorMapping.throw(NotExpectedLabelColumnError(
                        dataset_name=self.dataset_name, column_name=self.label_column_name,
                        reason="Label column is not consistent with training label column."))

        module_logger.info(f"Infer label mapping from scored label and label column: "
                           f"positive label is {self.label_encoder.positive_label} "
                           f"and negative label is {self.label_encoder.negative_label}.")
        module_logger.info('Perform transforming category label into numeric label.')
        with TimeProfile("Encoding label column"):
            df[self.label_column_name] = self.label_encoder.transform(df[self.label_column_name])
            if is_encode_scored_labels and self.label_column_name != self.scored_label_column_name:
                df[self.scored_label_column_name] = self.label_encoder.transform(df[self.scored_label_column_name])


class ClusterEvaluator(BaseEvaluator):
    task_type = TaskType.Cluster
    scored_label_column_name = ScoreColumnConstants.ClusterAssignmentsColumnName
    score_column_key = ScoreColumnConstants.ClusterScoredLabelType
    # this scored label column name is for scored columns described with constant names
    default_scored_label_column_name = ScoreColumnConstants.ClusterAssignmentsColumnName

    @staticmethod
    def _rebuild_result_df(df):
        df.index.name = "Result Description"
        df.rename(index=lambda x: 'Evaluation For Cluster No.' + str(x), inplace=True)
        df.reset_index(inplace=True)

    def _get_all_scored_data(self, data_frame, meta_data):
        if meta_data.score_column_names:
            # if score column names exists, just consider columns in score_column_names
            scored_columns = [x for x in data_frame.columns if x in meta_data.score_column_names.values()]
            data_frame = data_frame[scored_columns]

        distance_metrics_column_names = [name for name in data_frame.columns if
                                         name.startswith(ScoreColumnConstants.ClusterDistanceMetricsColumnNamePattern)]
        cluster_ids_in_distance_metrics_columns = pd.Series(
            [name[len(ScoreColumnConstants.ClusterDistanceMetricsColumnNamePattern):] for name in
             distance_metrics_column_names])
        assignments = convert_column_by_element_type(data_frame[self.scored_label_column_name], ElementTypeName.STRING)
        cluster_ids_in_assignments = assignments.dropna().unique()

        # check if all cluster ids in assignments has corresponding distance metrics columns
        for cluster_id in cluster_ids_in_assignments:
            if cluster_id not in cluster_ids_in_distance_metrics_columns.values:
                ErrorMapping.throw(InvalidDatasetError(
                    dataset1=self.dataset_name,
                    reason=f"not exist corresponding distance metrics column "
                    f"for cluster {cluster_id} found in {self.scored_label_column_name}."))

        if cluster_ids_in_assignments.shape[0] == 0:
            return pd.DataFrame({})
        # because scored columns defined by the column names feature is enabled, we can not limit the cluster ids
        # are of numeric type and start from 0, so just encode this cluster ids to be integers starts from 0
        cluster_id_encoder = NamedLabelEncoder('cluster_ids')
        cluster_id_encoder.fit(cluster_ids_in_distance_metrics_columns)
        assignments_without_na = cluster_id_encoder.transform(assignments.dropna())
        assignments[assignments.notna()] = assignments_without_na
        # reorder distance metrics columns by the order of the encoder label mapping
        distance_metrics_column_names = [ScoreColumnConstants.ClusterDistanceMetricsColumnNamePattern + x for x in
                                         cluster_id_encoder.label_mapping]
        scored_data = data_frame[[self.scored_label_column_name] + distance_metrics_column_names]
        scored_data[self.scored_label_column_name] = assignments
        scored_data = scored_data.rename(
            columns={name: ScoreColumnConstants.ClusterDistanceMetricsColumnNamePattern + str(i) for i, name in
                     enumerate(distance_metrics_column_names)})

        return scored_data

    def _evaluate(self, data_frame, meta_data, output_metrics):
        DISTANCE_TO_ASSIGNED_CLUSTER_NAME = 'Distance to Cluster Center'
        DISTANCE_TO_OTHER_CLUSTER_NAME = 'Distance to Other Center'

        def _get_assigned_cluster_distance(x):
            """
            return distance to cluster i , i = assignment in this row.
            :param x: pandas.Series in row, [assignments, dis 0, dis 1, dis 2 ...]
            :return: cluster index, distance to assigned cluster center, distance to the second closest
            """

            min_cluster = int(x[0])
            min_dis = x[min_cluster + 1]
            x[min_cluster + 1] = np.inf
            x[0] = np.inf
            return min_cluster, min_dis, x.min()

        scored_data = self._get_all_scored_data(data_frame=data_frame, meta_data=meta_data)
        # drop nan rows
        nd = scored_data.dropna(axis=0).values

        # the shape of new_nd should be (N, 3) that 3 columns corresponds to the
        # cluster index, distance to assigned cluster center, distance to the second
        # closest respectively.
        if nd.shape[0] > 0:
            new_nd = np.apply_along_axis(_get_assigned_cluster_distance, 1, nd)
        else:
            # if all samples contain nan values, just init an empty array. We assign the column number
            # to 3 explicitly to assure that the shape is consistent with results of np.apply_along_axis.
            new_nd = np.empty(shape=(0, 3))

        # calculate distance to assigned cluster and other cluster by assigned index.
        data_frame = pd.DataFrame(data=new_nd,
                                  columns=[self.scored_label_column_name,
                                           DISTANCE_TO_ASSIGNED_CLUSTER_NAME,
                                           DISTANCE_TO_OTHER_CLUSTER_NAME])
        data_frame[self.scored_label_column_name] = data_frame[self.scored_label_column_name].astype(int)

        total_average_df = data_frame.agg({DISTANCE_TO_OTHER_CLUSTER_NAME: 'mean',
                                           DISTANCE_TO_ASSIGNED_CLUSTER_NAME: 'mean'})

        # aggregate by cluster
        res_df = data_frame.groupby(self.scored_label_column_name).agg(
            {DISTANCE_TO_OTHER_CLUSTER_NAME: 'mean', DISTANCE_TO_ASSIGNED_CLUSTER_NAME: ['mean', 'count', 'max']})
        res_df.columns = ['Average ' + DISTANCE_TO_OTHER_CLUSTER_NAME, 'Average ' + DISTANCE_TO_ASSIGNED_CLUSTER_NAME,
                          'Number of Points', 'Maximal ' + DISTANCE_TO_ASSIGNED_CLUSTER_NAME]

        ClusterEvaluator._rebuild_result_df(res_df)
        # add combined evaluation
        combined_evaluation = {
            'Result Description': 'Combined Evaluation',
            'Average ' + DISTANCE_TO_ASSIGNED_CLUSTER_NAME: total_average_df[DISTANCE_TO_ASSIGNED_CLUSTER_NAME],
            'Average ' + DISTANCE_TO_OTHER_CLUSTER_NAME: total_average_df[DISTANCE_TO_OTHER_CLUSTER_NAME],
            'Number of Points': res_df['Number of Points'].sum(),
            'Maximal ' + DISTANCE_TO_ASSIGNED_CLUSTER_NAME: res_df['Maximal ' + DISTANCE_TO_ASSIGNED_CLUSTER_NAME].max()
        }
        res_df = res_df.append(combined_evaluation, ignore_index=True)
        # Up till now, the visualization information of the cluster scored data is None.
        return res_df, None


class QuantileRegressionEvaluator(BaseEvaluator):
    task_type = TaskType.QuantileRegression
    scored_label_column_name = ScoreColumnConstants.ScoredLabelsColumnName
    score_column_key = ScoreColumnConstants.ScoredLabelsColumnName

    def _drop_missing_scored_label_instance(self, df):
        drop_illegal_label_instances(df, column_name=self.scored_label_column_name, task_type=self.task_type)

    def _calculate(self, y_true, df, quantile_values):
        total_quantile_loss = 0
        quantile_loss_label = list()
        quantile_loss = list()
        for scored_label_name, quantile_value in zip(self.scored_label_column_name, quantile_values):
            quantile_loss_label.append("Quantile Loss:" + "%.3f" % float(quantile_value))
            y_pred = df[scored_label_name]
            loss = self._calculate_quantile_loss(y_true, y_pred, float(quantile_value))
            quantile_loss.append(loss)
            total_quantile_loss += loss
        quantile_loss_label.append("Average Quantile Loss")
        quantile_loss.append(metric_calculator.safe_divide(total_quantile_loss, len(self.scored_label_column_name)))
        results = dict(zip(quantile_loss_label, quantile_loss))

        return pd.DataFrame([results])

    def _evaluate(self, df, meta_data, output_metrics):
        self._drop_missing_scored_label_instance(df=df)
        y_true = df[self.label_column_name]
        # use saved label encoder to transform y_true to numeric series
        label_column_type = meta_data.get_column_type(self.label_column_name)
        if label_column_type != ColumnTypeName.NUMERIC:
            # Convert categorical label into uncategorical type, as label encoder doesn't support categorical type
            if is_categorical_dtype(df[self.label_column_name]):
                y_true = data_type_conversion.convert_column_by_element_type(
                    df[self.label_column_name], ElementTypeName.UNCATEGORY)

            label_encoder = meta_data.extended_properties.get(META_PROPERTY_LABEL_ENCODER_KEY, None)
            if label_encoder is None:
                # if training data label is numeric but scored data label is non-numeric,
                # will throw 'NotExpectedLabelColumnError' because of no label encoder.
                ErrorMapping.throw(NotExpectedLabelColumnError(
                    column_name=self.label_column_name,
                    dataset_name=self.dataset_name,
                    reason=f"scored dataset label is '{label_column_type}' but train data label "
                    f"is '{ColumnTypeName.NUMERIC}'",
                    troubleshoot_hint='Please make sure train and scored dataset label column types are the same.'))
            elif len(y_true) > 0:
                try:
                    y_true = label_encoder.transform(y_true)
                except ValueError as e:
                    if "Found unknown categories" in str(e.args):
                        ErrorMapping.rethrow(e, InvalidDatasetError(
                            dataset1=self.dataset_name,
                            reason="failed to transform scored dataset label column: "
                            f"{ErrorMapping.get_exception_message(e)}",
                            troubleshoot_hint="Please make sure scored dataset label column have the same categories "
                                              "as that of train for non-numeric label in regression task, "
                            f"train data label categories are {label_encoder.label_mapping}."
                        ))
                    else:
                        raise e

        # calculate quantile values in the order of self.scored_label_column_name
        score_column_names_to_keys = {v: k for k, v in meta_data.score_column_names.items()}
        quantile_values = [
            score_column_names_to_keys[score_label_column][len(ScoreColumnConstants.QuantileScoredLabelsColumnName):]
            for
            score_label_column in self.scored_label_column_name]

        return self._calculate(y_true, df, quantile_values), None

    def _update_scored_label_column(self, meta_data):
        self.scored_label_column_name = list()
        # need to filter columns by keys with specific prefix, or there can be extra score columns
        for name in filter_column_names_with_prefix(meta_data.score_column_names,
                                                    prefix=ScoreColumnConstants.QuantileScoredLabelsColumnName):
            self.scored_label_column_name.append(meta_data.score_column_names[name])

    def _calculate_quantile_loss(self, y_true, y_pred, quantile_value):
        """Quantile value is defined as follows
        let error = y - yhat
        loss(y, yhat, q) = q * error * I(y gt yhat) - (1 - q) * error * I( y le yhat)
        """
        with TimeProfile("Calculating Quantile Loss: " + str(quantile_value)):
            loss = 0
            number_valid_entries = 0
            for i in range(len(y_true)):
                if y_true[i] is None or y_pred[i] is None:
                    continue
                error = y_true[i] - y_pred[i]
                if error > 0:
                    loss += quantile_value * error
                else:
                    loss += (quantile_value - 1) * error
                number_valid_entries += 1
            return metric_calculator.safe_divide(loss, number_valid_entries)
