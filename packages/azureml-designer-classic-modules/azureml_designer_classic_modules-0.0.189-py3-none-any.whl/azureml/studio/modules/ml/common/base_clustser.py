from abc import abstractmethod

import azureml.studio.modules.ml.common.normalizer as normalizer
from azureml.studio.core.logger import module_logger, TimeProfile, time_profile
from azureml.studio.modules.ml.common.ml_utils import TaskType
from azureml.studio.modules.ml.model_deployment.model_deployment_handler import ClusterModelDeploymentHandler


class BaseCluster:
    def __init__(self, setting):
        self.model = None
        self._is_trained = False
        self.init_feature_columns_names = None
        self.label_column_name = None
        self.normalized_feature_columns_names = None
        self.normalizer = None
        self.sub_model = None
        self.task_type = TaskType.Cluster
        self.setting = setting
        self.cluster_label = None
        self._deployment_handler = None

    @abstractmethod
    def init_model(self):
        pass

    @property
    def is_trained(self):
        return self._is_trained

    @property
    def deployment_handler(self):
        return self._deployment_handler

    @deployment_handler.setter
    def deployment_handler(self, value):
        if not isinstance(value, ClusterModelDeploymentHandler):
            raise TypeError(f'deployment_handler must be an instance of class {ClusterModelDeploymentHandler.__name__}')
        self._deployment_handler = value

    @abstractmethod
    def train(self, df, label_column_name):
        pass

    def _apply_normalize(self, df, df_transform_column_list=None):
        with TimeProfile("Applying feature normalization"):
            return self.normalizer.transform(df, df_transform_column_list)

    def _fit_normalize(self, df):
        # normalize the data
        with TimeProfile("Initializing feature normalizer"):
            self.normalizer = normalizer.Normalizer()
            normalize_number = self.setting.normalize_features
            self.normalizer.build(
                df=df,
                feature_columns=self.init_feature_columns_names,
                label_column_name=None,  # cluster model does not need label column.
                normalize_number=normalize_number,
                encode_label=False
            )
        with TimeProfile("Fitting feature normalizer"):
            self.normalizer.fit(df)

    @time_profile
    def _train(self, train_x):
        # train model
        with TimeProfile("Training Model"):
            self.model.fit(train_x)
        module_logger.info(
            f'Sum of squared distances of samples to their closest cluster center: {self.model.inertia_}.')
        module_logger.info(f'Number of iterations run: {self.model.n_iter_}.')
        self._is_trained = True

    @abstractmethod
    def predict(self, df):
        pass
