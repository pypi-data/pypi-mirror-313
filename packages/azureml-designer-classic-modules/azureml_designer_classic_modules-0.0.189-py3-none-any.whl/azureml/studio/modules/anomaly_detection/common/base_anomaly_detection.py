from abc import abstractmethod

import pandas as pd
from azureml.studio.common.datatable.data_table import DataTable
from azureml.studio.core.logger import module_logger, time_profile, TimeProfile
from azureml.studio.core.utils.strutils import profile_column_names
from azureml.studio.modulehost.attributes import AutoEnum, ItemInfo, ReleaseState
from azureml.studio.modules.ml.common.base_learner import BaseLearner
from azureml.studio.modules.ml.common.constants import ScoreColumnConstants
from azureml.studio.modules.ml.common.ml_utils import TaskType


class CreateLearnerMode(AutoEnum):
    SingleParameter: ItemInfo(name="SingleParameter", friendly_name="Single Parameter") = ()
    ParameterRange: ItemInfo(name="ParameterRange", friendly_name="Parameter Range",
                             release_state=ReleaseState.Alpha) = ()


class RestoreInfo:
    def __init__(self, param_name, inverse_func=None):
        """Restore the meaning of parameter from sklearn

        :param param_name: studio.parameter.friendly_name
        :param inverse_func: transform a scikit learn parameter value into the studio one.
                             If None, do not change the value
        """
        self.param_name = param_name
        self.inverse_func = inverse_func


class BaseAnomalyDetectionLearner(BaseLearner):
    def __init__(self, setting):
        super().__init__(setting=setting, task_type=TaskType.AnomalyDetection)

    @property
    def parameter_mapping(self):
        return dict()

    @abstractmethod
    def init_model(self):
        pass

    @property
    def is_trained(self):
        return self._is_trained

    @time_profile
    def train(self, data_table: DataTable):
        """Apply normalizing and training

        :param data_table: DataTable, training data
        :return: None
        """
        train_x, _ = self.preprocess_training_data(data_table)
        # initial model
        with TimeProfile("Initializing model"):
            self.init_model()
            self._enable_verbose()
        self._train(train_x)

    @time_profile
    def _train(self, train_x):
        # train model
        with TimeProfile("Training Model"):
            self.model.fit(train_x)
        self._is_trained = True

    @abstractmethod
    def _predict(self, test_x: pd.DataFrame):
        pass

    def _build_result_dataframe(self, label, prob):
        result_df = pd.DataFrame()
        module_logger.info('Anomaly Detection Task, Result Contains Scored Label.')
        result_df[ScoreColumnConstants.ScoredLabelsColumnName] = label
        result_df[ScoreColumnConstants.ScoredProbabilitiesColumnName] = prob
        return result_df

    def generate_score_column_meta(self, predict_df):
        """Build score_column_names dict
        Map AnomalyDetectionScoredLabelType to ScoredLabelsColumnName
        Map CalibratedScoreType To ScoredProbabilitiesColumnName
        When evaluating the scored data, infer the task task with the AnomalyDetectionScoredLabelType key.

        :return: built score column names dict
        """
        score_columns = dict()
        score_columns[
            ScoreColumnConstants.AnomalyDetectionScoredLabelType] = ScoreColumnConstants.ScoredLabelsColumnName
        score_columns[ScoreColumnConstants.CalibratedScoreType] = ScoreColumnConstants.ScoredProbabilitiesColumnName
        module_logger.info("Anomaly Detection Scored Columns are: ")
        module_logger.info(
            f'There are {len(score_columns.keys())} score columns: '
            f'"{profile_column_names(list(score_columns.keys()))}"')
        return score_columns
