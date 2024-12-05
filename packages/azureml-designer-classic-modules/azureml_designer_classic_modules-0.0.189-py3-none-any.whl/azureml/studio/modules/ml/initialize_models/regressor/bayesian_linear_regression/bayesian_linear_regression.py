import statistics

import numpy as np
import pandas as pd
from scipy.sparse import issparse
from sklearn.linear_model import BayesianRidge

from azureml.studio.common.error import ErrorMapping, TooFewRowsInDatasetError
from azureml.studio.core.logger import time_profile, TimeProfile
from azureml.studio.modulehost.attributes import FloatParameter, UntrainedLearnerOutputPort, ModuleMeta, \
    BooleanParameter
from azureml.studio.internal.attributes.release_state import ReleaseState
from azureml.studio.modulehost.constants import FLOAT_MIN_POSITIVE
from azureml.studio.modulehost.module_reflector import module_entry, BaseModule
from azureml.studio.modules.ml.common.base_learner import TaskType
from azureml.studio.modules.ml.common.base_learner_setting import BaseLearnerSetting
from azureml.studio.modules.ml.common.metric_calculator import safe_divide
from azureml.studio.modules.ml.common.supervised_learners import RegressionLearner


class BayesianLinearRegressionModule(BaseModule):
    @staticmethod
    @module_entry(
        ModuleMeta(
            name="Bayesian Linear Regression",
            description="Creates a Bayesian linear regression model.",
            category="Machine Learning Algorithms/Regression",
            version="1.0",
            owner="Microsoft Corporation",
            family_id="EE12DE50-2B34-4145-AEC0-23E0485DA308",
            release_state=ReleaseState.Beta,
            is_deterministic=True,
        )
    )
    def run(
            regularizer: FloatParameter(
                name="Regularization weight",
                friendly_name="Regularization weight",
                description="Type a constant to use in regularization. "
                            "The constant represents the ratio of the precision "
                            "of weight prior to the precision of noise.",
                default_value=1,
                min_value=FLOAT_MIN_POSITIVE,
            ),
            allow_unknown_levels: BooleanParameter(
                name="Allow unknown levels in categorical features",
                friendly_name="Allow unknown categorical levels",
                description="If true creates an additional level for each categorical column. "
                            "Any levels in the test dataset not available in the training dataset "
                            "are mapped to this additional level.",
                default_value=True,
            )
    ) -> (
            UntrainedLearnerOutputPort(
                name="Untrained model",
                friendly_name="Untrained model",
                description="An untrained Bayesian linear regression model",
            ),
    ):
        input_values = locals()
        output_values = BayesianLinearRegressionModule.create_bayesian_linear_regressor(**input_values)
        return output_values

    @staticmethod
    def create_bayesian_linear_regressor(regularizer: float = None, allow_unknown_levels: bool = True):
        setting = BayesianLinearRegressorSetting()
        setting.init_single(regularizer=regularizer)
        return BayesianLinearRegressor(setting),


class BayesianLinearRegressorSetting(BaseLearnerSetting):
    def __init__(self):
        super().__init__()
        self.weight_precision_parameter = 1e-06
        self.noise_precision_parameter = 1e-06
        self.n_iter = 1000
        self.regularizer = 1
        self.noise_fraction = 0.2
        self.noise_variance_uniform = 0.001

    def init_single(self, regularizer: float = 1):
        self.regularizer = regularizer

    def init_range(self):
        pass


class BayesianLinearRegressor(RegressionLearner):
    def __init__(self, setting: BayesianLinearRegressorSetting):
        super().__init__(setting=setting, task_type=TaskType.Regression)

    def init_model(self):
        # Parameter name source (https://scikit-learn.org/stable/modules/linear_model.html#bayesian-ridge-regression)
        self.model = BayesianRidge(
            tol=0.001,
            copy_X=True,
            normalize=False,
            verbose=False,
            compute_score=False,
            fit_intercept=True,
            n_iter=self.setting.n_iter,
            alpha_1=self.setting.noise_precision_parameter,
            lambda_1=self.setting.weight_precision_parameter
        )

    def set_init_method(self, data_set=None):
        """Set the model params according to dataset

        Reset weight_precision_parameter and noise_precision_parameter param
        The dataset is not NaN by default
        :param data_set: target data set
        :return: None
        Raise error if the dataset has single instance
        """
        if len(data_set) < 2:
            ErrorMapping.throw(
                TooFewRowsInDatasetError(required_rows_count=2,
                                         reason='Variance cannot be calculated based on single instance.'))

        # Calculate the target variance
        target_variance = statistics.variance(data_set)
        if target_variance == 0:
            noise_variance = self.setting.noise_variance_uniform
        else:
            noise_variance = self.setting.noise_fraction * target_variance

        # Parameter noise_precision_parameter is the noise precision parameter
        self.setting.noise_precision_parameter = np.abs(safe_divide(1, noise_variance))
        # Keeping the regularization parameter regularizer = weight_precision_parameter/noise_precision_parameter
        # Parameter weight_precision_parameter is the precision parameter for weights
        self.setting.weight_precision_parameter = self.setting.regularizer * self.setting.noise_precision_parameter
        self.model.set_params(alpha_1=self.setting.noise_precision_parameter)
        self.model.set_params(lambda_1=self.setting.weight_precision_parameter)

    def convert_sparse_to_dense_data(self, data):
        if issparse(data):
            return data.toarray()
        return data

    @time_profile
    def _train(self, train_x, train_y):
        # Reset init parameters according to dataset
        self.set_init_method(train_y)
        # Convert sparse to dense
        train_dense_x = self.convert_sparse_to_dense_data(train_x)
        train_dense_y = self.convert_sparse_to_dense_data(train_y)
        with TimeProfile("Training Model"):
            self.model.fit(train_dense_x, train_dense_y)

        self._is_trained = True

    @time_profile
    def _predict(self, test_x: pd.DataFrame):
        # Convert sparse to dense
        test_dense_x = self.convert_sparse_to_dense_data(test_x)
        with TimeProfile("Predicting regression value"):
            return self.model.predict(test_dense_x), None
