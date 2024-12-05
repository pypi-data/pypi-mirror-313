from contextlib import contextmanager
import os
from pickle import PicklingError
from sklearn.multiclass import OneVsRestClassifier
import tempfile

from azureml.studio.common.error import ErrorMapping, InvalidLearnerError, ModuleOutOfMemoryError
from azureml.studio.core.logger import time_profile, module_logger
from azureml.studio.modulehost.attributes import UntrainedLearnerInputPort, UntrainedLearnerOutputPort, \
    ModuleMeta
from azureml.studio.internal.attributes.release_state import ReleaseState
from azureml.studio.modulehost.module_reflector import module_entry, BaseModule
from azureml.studio.modules.ml.common.base_learner import BaseLearner
from azureml.studio.modules.ml.common.ml_utils import TaskType
from azureml.studio.modules.ml.common.supervised_learners import MultiClassificationLearner


class OneVsAllMulticlassModule(BaseModule):
    @staticmethod
    @module_entry(ModuleMeta(
        name="One-vs-All Multiclass",
        description="Creates a one-vs-all multiclass classification model from an ensemble of binary classification "
                    "models.",
        category="Machine Learning Algorithms/Classification",
        version="1.0",
        owner="Microsoft Corporation",
        family_id="7191EFAE-B4B1-4D03-A6F8-7205F87BE664",
        release_state=ReleaseState.Release,
        is_deterministic=True,
    ))
    def run(
            learner: UntrainedLearnerInputPort(
                name="Untrained binary classification model",
                friendly_name="Untrained binary classification model",
                description="An untrained binary classification model",
            )
    ) -> (
            UntrainedLearnerOutputPort(
                name="Untrained model",
                friendly_name="Untrained model",
                description="An untrained multi-class classification",
            ),
    ):
        input_values = locals()
        output_values = OneVsAllMulticlassModule.create_one_vs_all_multiclassifier(**input_values)
        return output_values

    @classmethod
    def create_one_vs_all_multiclassifier(cls, learner: BaseLearner):
        if learner.task_type != TaskType.BinaryClassification:
            # The input learner must be a binary classifier
            ErrorMapping.throw(
                InvalidLearnerError(arg_name=cls._args.learner.friendly_name, learner_type=learner.__class__.__name__))

        one_vs_all_classifier = OneVsAllMultiClassifier(learner.setting, task_type=TaskType.MultiClassification,
                                                        sub_model=learner)
        return one_vs_all_classifier,


class OneVsAllMultiClassifier(MultiClassificationLearner):
    _PARAMETER_PREFIX = 'estimator__'

    def __init__(self, setting, task_type, sub_model):
        super().__init__(setting=setting, task_type=task_type)
        self.sub_model = sub_model

    def gen_inter_name(self, name):
        return self._PARAMETER_PREFIX + name

    @property
    def parameter_mapping(self):
        sub_mapping = self.sub_model.parameter_mapping
        return {self.gen_inter_name(key): val for key, val in sub_mapping.items()}

    @property
    def parameter_range(self):
        sub_parameter_range = self.sub_model.parameter_range
        return {self.gen_inter_name(key): val for key, val in sub_parameter_range.items()}

    def init_model(self):
        self.sub_model.init_model()
        self.model = OneVsRestClassifier(self.sub_model.model)

    @time_profile
    def _train(self, train_x, train_y):
        # This is a folder to be used by the pool for memmapping large arrays for sharing memory with worker
        # processes. Set it as a temp dir, usually a larger disk path than default path '/dev/shm'.
        # See https://joblib.readthedocs.io/en/latest/generated/joblib.Parallel.html for details.
        with set_os_env("JOBLIB_TEMP_FOLDER", tempfile.mkdtemp()):
            try:
                # OVR classifier is easier to encounter OOM error in training large dataset
                # because it consumes the whole dataset in fitting every estimator.
                self.model.fit(train_x, train_y)
            except PicklingError as e:
                if e.__cause__ and 'No space left on device' in str(e.__cause__.args):
                    ErrorMapping.rethrow(e, ModuleOutOfMemoryError(
                        "Cannot allocate more memory. Please upgrade VM Sku."))

        self._is_trained = True


@contextmanager
def set_os_env(os_env_key, value):
    prev_value = os.environ.get(os_env_key, None)
    os.environ[os_env_key] = value
    module_logger.info(f"Change os env '{os_env_key}' from '{prev_value}' to '{value}'.")
    yield
    if prev_value is None:
        os.environ.pop(os_env_key, None)
    else:
        os.environ[os_env_key] = prev_value
    module_logger.info(f"Reset os env '{os_env_key}'.")
