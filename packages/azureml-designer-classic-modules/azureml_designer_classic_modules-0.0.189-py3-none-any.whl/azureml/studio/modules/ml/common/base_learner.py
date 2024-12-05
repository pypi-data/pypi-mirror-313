from abc import abstractmethod

import pandas as pd
from scipy.special import softmax

import azureml.studio.modules.ml.common.mathematic_op as mathematic_op
import azureml.studio.modules.ml.common.normalizer as normalizer
from azureml.studio.core.schema import ColumnTypeName
from azureml.studio.common.datatable.data_table import DataTable
from azureml.studio.common.error import (ErrorMapping, InvalidColumnTypeError,
                                         LabelColumnDoesNotHaveLabeledPointsError, MissingFeaturesError,
                                         MultipleLabelColumnsError, NotLabeledDatasetError,
                                         FailedToCompleteOperationError)
from azureml.studio.core.logger import TimeProfile, module_logger, time_profile
from azureml.studio.modules.ml.model_deployment.model_deployment_handler import BaseLearnerDeploymentHandler
from azureml.studio.modulehost.attributes import AutoEnum, ItemInfo

from .base_learner_setting import BaseLearnerSetting
from .ml_utils import (TaskType, check_test_data_col_type_compatible, drop_illegal_label_instances,
                       get_label_column_names)


class CreateLearnerMode(AutoEnum):
    SingleParameter: ItemInfo(name="SingleParameter", friendly_name="Single Parameter") = ()
    ParameterRange: ItemInfo(name="ParameterRange", friendly_name="Parameter Range") = ()


class RestoreInfo:
    def __init__(self, param_name, inverse_func=None):
        """Restore the meaning of parameter from sklearn

        :param param_name: studio.parameter.friendly_name
        :param inverse_func: transform a scikit learn parameter value into the studio one.
                             If None, do not change the value
        """
        self.param_name = param_name
        self.inverse_func = inverse_func


class BaseLearner:
    def __init__(self, setting: BaseLearnerSetting, task_type=None):
        self.model = None
        self._is_trained = False
        self.init_feature_columns_names = None
        self.label_column_name = None
        self.normalized_feature_columns_names = None
        self.normalizer = None
        self.task_type = task_type
        self.setting = setting
        # encode label for task types except anomaly detection
        self.encode_label = self.task_type != TaskType.AnomalyDetection
        self._deployment_handler = None

    def collect_label_column_name(self, data_table, label_column_selection):
        """Get the selected column names.

        :param data_table: DataTable input data.
        :param label_column_selection: ColumnSelection
        """
        label_column_names = get_label_column_names(training_data=data_table,
                                                    column_selection=label_column_selection)
        if not label_column_names:
            ErrorMapping.throw(NotLabeledDatasetError(dataset_name=data_table.name))
        elif len(label_column_names) != 1:
            ErrorMapping.throw(MultipleLabelColumnsError(dataset_name=data_table.name))
        self.label_column_name = label_column_names[0]
        module_logger.info(f"{self.label_column_name} as Label Column.")

    def check_label_column(self, data_table):
        required_rows_count = 1
        case_count = data_table.number_of_rows
        if self.label_column_name not in data_table.column_names:
            ErrorMapping.throw(NotLabeledDatasetError(dataset_name=data_table.name))
        # For regression, only encode label for non-numeric label.
        if self.task_type == TaskType.Regression or self.task_type == TaskType.QuantileRegression:
            self.encode_label = data_table.get_column_type(self.label_column_name) != ColumnTypeName.NUMERIC

        invalid_count = data_table.get_number_of_missing_value(self.label_column_name)
        if case_count - invalid_count < required_rows_count:
            ErrorMapping.throw(LabelColumnDoesNotHaveLabeledPointsError(required_rows_count=required_rows_count))
        # To fix bug 715446: forbid 'Object, NAN, BYTES' label column types.
        supported_label_column_types = {
            ColumnTypeName.NUMERIC, ColumnTypeName.STRING, ColumnTypeName.BINARY, ColumnTypeName.CATEGORICAL,
            ColumnTypeName.DATETIME, ColumnTypeName.TIMESPAN}
        label_column_type = data_table.get_column_type(self.label_column_name)
        if label_column_type not in supported_label_column_types:
            ErrorMapping.throw(InvalidColumnTypeError(
                col_name=self.label_column_name,
                col_type=label_column_type,
                reason=f'label column type cannot be {label_column_type}',
                troubleshoot_hint=f"Please use supported label column types: {supported_label_column_types}."))

    @abstractmethod
    def generate_score_column_meta(self, predict_df):
        """Build score_column_names dict

        When evaluating the scored data, infer the task task with the {TaskType}ScoreLabelType key.
        :param predict_df: data frame with scored columns
        :return: built score column names dict
        """
        return {}

    @property
    def parameter_mapping(self):
        return dict()

    @property
    def is_trained(self):
        return self._is_trained

    @property
    def parameter_range(self):
        return self.setting.parameter_range

    @property
    def deployment_handler(self):
        return self._deployment_handler

    @deployment_handler.setter
    def deployment_handler(self, value):
        if not isinstance(value, BaseLearnerDeploymentHandler):
            raise TypeError(f'deployment_handler must be an instance of class {BaseLearnerDeploymentHandler.__name__}')
        self._deployment_handler = value

    @abstractmethod
    def init_model(self):
        pass

    def _enable_verbose(self):
        if not self.setting.enable_log:
            module_logger.info("Skipped to enable the training log since the setting.enable_log is False.")
            return
        verbose = getattr(self.model, 'verbose', None)
        if verbose is not None and verbose is not False and verbose == 0:
            """
            if verbose is None, verbose is not supported by this model
            if default verbose is False(not 0), enable it will cause two verbose output.
            only enable the model which was not enabled verbose.
            so only enable verbose when default verbose value is not (None, False).
            """
            module_logger.info("Enable the training log.")
            self.model.set_params(verbose=1)

    @time_profile
    def _normalize_data(self, df):
        self._fit_normalize(df)
        return self._apply_normalize(df, df.columns.tolist())

    def _record_feature_column_names(self, dt: DataTable):
        """Record feature column names in the DataTable.
        :param dt: DataTable, the DataTable to be record feature columns
        :return: None
        """
        self.init_feature_columns_names = []
        for col_name in dt.column_names:
            if dt.meta_data.get_column_attribute(col_name).is_feature:
                self.init_feature_columns_names.append(col_name)
        if self.label_column_name in self.init_feature_columns_names:
            self.init_feature_columns_names.remove(self.label_column_name)

    def _clean_training_data(self, df):
        """Drop not labeled instances when training a supervised model.

        :param df: pandas.DataFrame, training data
        :return: pandas.DataFrame, cleaned training data which does not contains not labeled instances
        """
        if self.label_column_name is not None:
            with TimeProfile("Removing instances with illegal label"):
                drop_illegal_label_instances(df, column_name=self.label_column_name, task_type=self.task_type)
        module_logger.info(f"validated training data has {df.shape[0]} Row(s) and {df.shape[1]} Columns.")
        return df

    def preprocess_training_data(self, data_table: DataTable, fit=True):
        self._record_feature_column_names(data_table)
        df = data_table.data_frame
        # This will return a new data frame
        df = df.reset_index(drop=True)
        df = self._clean_training_data(df)
        if fit:
            train_x, train_y = self._normalize_data(df)
        else:
            train_x, train_y = self._apply_normalize(df)
        return train_x, train_y

    @time_profile
    def train(self, data_table: DataTable, label_column_selection):
        """Apply normalizing and training

        :param data_table: DataTable, training data
        :param label_column_selection: ColumnSelection
        :return: None
        """
        self.collect_label_column_name(data_table, label_column_selection)
        self.check_label_column(data_table=data_table)

        train_x, train_y = self.preprocess_training_data(data_table)
        # initial model
        with TimeProfile("Initializing model"):
            self.init_model()
            self._enable_verbose()
        self._train(train_x, train_y)

    @time_profile
    def _apply_normalize(self, df, df_transform_column_list=None):
        with TimeProfile("Applying feature normalization"):
            return self.normalizer.transform(df, df_transform_column_list)

    @time_profile
    def _fit_normalize(self, df):
        # normalize the data
        with TimeProfile("Initialing feature normalizer"):
            self.normalizer = normalizer.Normalizer()
            normalize_number = getattr(self.setting, 'normalize_features', True)
            self.normalizer.build(
                df=df,
                feature_columns=self.init_feature_columns_names,
                label_column_name=self.label_column_name,
                normalize_number=normalize_number,
                encode_label=self.encode_label
            )
        with TimeProfile("Fitting feature normalizer"):
            self.normalizer.fit(df)

    @time_profile
    def _train(self, train_x, train_y):
        # train model
        with TimeProfile("Training Model"):
            try:
                self.model.fit(train_x, train_y)
            except OverflowError as err:
                if "Python int too large to convert to C long" in ErrorMapping.get_exception_message(err):
                    ErrorMapping.throw(FailedToCompleteOperationError(failed_operation="fit",
                                                                      reason=ErrorMapping.get_exception_message(err)))
        if hasattr(self.model, 'loss_'):
            module_logger.info(f'Training Loss: {self.model.loss_}.')
        if hasattr(self.model, 'n_iter_ '):
            module_logger.info(f'Inter Number: {self.model.n_iter_}.')
        self._is_trained = True

    @time_profile
    def _predict(self, test_x: pd.DataFrame):
        if hasattr(self.model, 'predict_proba'):
            with TimeProfile("Predicting probability"):
                prob = self.model.predict_proba(test_x)
            with TimeProfile("calculating argmax(Probability)"):
                label = prob.argmax(axis=1)
            return label, prob
        if hasattr(self.model, 'decision_function'):
            module_logger.info("Start calculating score.")
            with TimeProfile("Calculating Score"):
                prob = self.model.decision_function(test_x)
            with TimeProfile("Calculating Probability"):
                if len(prob.shape) == 2:
                    # The output is a matrix, matrix[i,j] indicates the score that
                    # the instances[i] is belong to the category[j].
                    # So, we normalize the score to get probabilities using the softmax function.
                    module_logger.info("Calculating Probability with the softmax function")
                    prob = softmax(prob, axis=1)
                    label = prob.argmax(axis=1)
                else:
                    # The output is a single column, indicates the score of being a positive label.
                    # So, we normalize the score to get probabilities using the sigmoid funciton.
                    module_logger.info("Calculating Probability with the sigmoid function")
                    label = prob > 1e-9
                    prob = mathematic_op.sigmoid(prob)
            return label, prob
        else:
            with TimeProfile("Predicting regression value"):
                return self.model.predict(test_x), None

    def _build_result_dataframe(self, label, prob):
        """Build scored result dataframe, with predefined column names.

        """
        pass

    def predict(self, test_data_df):
        self._validate_no_missing_feature(input_feature_list=test_data_df.columns.tolist())
        test_x = test_data_df[self.init_feature_columns_names]
        module_logger.info(f'Check if column types of test data are consistent with train data')
        check_test_data_col_type_compatible(test_x,
                                            self.normalizer.feature_columns_categorized_by_type,
                                            self.setting, self.task_type)
        module_logger.info(f'Successfully checked column types. Predicting.')
        test_x, _ = self._apply_normalize(test_x, test_x.columns.tolist())
        label, prob = self._predict(test_x)
        module_logger.info(f'Successfully predicted.')
        return self._build_result_dataframe(label, prob)

    def _validate_no_missing_feature(self, input_feature_list):
        missing_feature_list = [feature for feature in self.init_feature_columns_names if
                                feature not in input_feature_list]

        if missing_feature_list:
            ErrorMapping.throw(MissingFeaturesError(required_feature_name=';'.join(missing_feature_list)))

    @property
    def label_classes(self):
        if not self.normalizer or not self.normalizer.label_column_name or \
                self.normalizer.label_column_name not in self.normalizer.label_column_encoders:
            return None

        return self.normalizer.label_column_encoders[self.normalizer.label_column_name].label_mapping
