from sklearn.linear_model import LogisticRegression

from azureml.studio.common.parameter_range import ParameterRangeSettings
from azureml.studio.internal.attributes.release_state import ReleaseState
from azureml.studio.modulehost.attributes import ModeParameter, FloatParameter, IntParameter, BooleanParameter, \
    ParameterRangeParameter, UntrainedLearnerOutputPort, ModuleMeta
from azureml.studio.modulehost.constants import FLOAT_MIN_POSITIVE, FLOAT_MAX, UINT32_MAX
from azureml.studio.modulehost.module_reflector import module_entry, BaseModule
from azureml.studio.modules.ml.common.base_learner import TaskType, CreateLearnerMode, RestoreInfo
from azureml.studio.modules.ml.common.supervised_learners import MultiClassificationLearner
from azureml.studio.modules.ml.initialize_models.common_settings.logistic_regression_setting import \
    LogisticRegressionDefaultParameters, LogisticRegressionSetting


class MulticlassLogisticRegressionModule(BaseModule):

    @staticmethod
    @module_entry(ModuleMeta(
        name="Multiclass Logistic Regression",
        description="Creates a multiclass logistic regression classification model.",
        category="Machine Learning Algorithms/Classification",
        version="2.0",
        owner="Microsoft Corporation",
        family_id="1D195FE5-98CD-4E1A-A1C8-076AAA3E02C3",
        release_state=ReleaseState.Release,
        is_deterministic=True,
    ))
    def run(
            mode: ModeParameter(
                CreateLearnerMode,
                name="Create trainer mode",
                friendly_name="Create trainer mode",
                description="Create advanced learner options",
                default_value=LogisticRegressionDefaultParameters.Mode,
            ),
            optimization_tolerance: FloatParameter(
                name="Optimization Tolerance",
                friendly_name="Optimization tolerance",
                description="Specify a tolerance value for the L-BFGS optimizer",
                default_value=LogisticRegressionDefaultParameters.OptimizationTolerance,
                parent_parameter="Create trainer mode",
                parent_parameter_val=(CreateLearnerMode.SingleParameter,),
                min_value=FLOAT_MIN_POSITIVE,
            ),
            l1_weight: FloatParameter(
                name="L1 Regularization weight",
                friendly_name="L1 regularization weight",
                description="Specify the L1 regularization weight. Use a non-zero value to avoid overfitting.",
                default_value=LogisticRegressionDefaultParameters.L1Weight,
                parent_parameter="Create trainer mode",
                parent_parameter_val=(CreateLearnerMode.SingleParameter,),
                min_value=0,
                release_state=ReleaseState.Alpha
            ),
            l2_weight: FloatParameter(
                name="L2 Regularizaton weight",
                friendly_name="L2 regularization weight",
                description="Specify the L2 regularization weight. Use a non-zero value to avoid overfitting.",
                default_value=LogisticRegressionDefaultParameters.L2Weight,
                parent_parameter="Create trainer mode",
                parent_parameter_val=(CreateLearnerMode.SingleParameter,),
                min_value=0,
            ),
            memory_size: IntParameter(
                name="Memory Size",
                friendly_name="Memory size for L-BFGS",
                description="Specify the amount of memory (in MB) to use for the L-BFGS optimizer. "
                            "When less memory is used, Training is faster but less accurate.",
                default_value=LogisticRegressionDefaultParameters.MemorySize,
                parent_parameter="Create trainer mode",
                parent_parameter_val=(CreateLearnerMode.SingleParameter,),
                min_value=1,
                release_state=ReleaseState.Alpha
            ),
            ps_optimization_tolerance: ParameterRangeParameter(
                name="Range for optimization tolerance",
                friendly_name="Optimization tolerance",
                description="Specify a range for the tolerance value for the L-BFGS optimizer",
                default_value=LogisticRegressionDefaultParameters.PsOptimizationTolerance,
                parent_parameter="Create trainer mode",
                parent_parameter_val=(CreateLearnerMode.ParameterRange,),
                min_limit=FLOAT_MIN_POSITIVE,
                max_limit=FLOAT_MAX,
                is_int=False,
                is_log=True,
                slider_min=1E-08,
                slider_max=0.001,
            ),
            ps_l1_weight: ParameterRangeParameter(
                name="Range for L1 regularization weight",
                friendly_name="L1 regularization weight",
                description="Specify the range for the L1 regularization weight. "
                            "Use a non-zero value to avoid overfitting.",
                default_value=LogisticRegressionDefaultParameters.PsL1Weight,
                parent_parameter="Create trainer mode",
                parent_parameter_val=(CreateLearnerMode.ParameterRange,),
                min_limit=0,
                max_limit=FLOAT_MAX,
                is_int=False,
                is_log=True,
                slider_min=0.0001,
                slider_max=1,
                release_state=ReleaseState.Alpha
            ),
            ps_l2_weight: ParameterRangeParameter(
                name="Range for L2 regularization weight",
                friendly_name="L2 regularization weight",
                description="Specify the range for the L2 regularization weight. "
                            "Use a non-zero value to avoid overfitting.",
                default_value=LogisticRegressionDefaultParameters.PsL2Weight,
                parent_parameter="Create trainer mode",
                parent_parameter_val=(CreateLearnerMode.ParameterRange,),
                min_limit=0,
                max_limit=FLOAT_MAX,
                is_int=False,
                is_log=True,
                slider_min=0.0001,
                slider_max=1,
            ),
            ps_memory_size: ParameterRangeParameter(
                name="Range for memory size for L-BFGS the lower the value the faster and less accurate the training",
                friendly_name="Memory size for L-BFGS",
                description="Specify the range for the amount of memory (in MB) to use for the L-BFGS optimizer. "
                            "The lower the value, the faster and less accurate the training.",
                default_value=LogisticRegressionDefaultParameters.PsMemorySize,
                parent_parameter="Create trainer mode",
                parent_parameter_val=(CreateLearnerMode.ParameterRange,),
                min_limit=1,
                max_limit=2147483647,
                is_int=True,
                is_log=False,
                slider_min=1,
                slider_max=100,
                release_state=ReleaseState.Alpha
            ),
            random_number_seed: IntParameter(
                name="Random number seed",
                friendly_name="Random number seed",
                min_value=0,
                max_value=UINT32_MAX,
                is_optional=True,
                description="Type a value to seed the random number generator used by the model. "
                            "Leave blank for default.",
            ),
            allow_unknown_levels: BooleanParameter(
                name="Allow unknown levels in categorical features",
                friendly_name="Allow unknown categorical levels",
                description="Indicate whether an additional level should be created for each categorical column. "
                            "Any levels in the test dataset not available in the training dataset "
                            "are mapped to this additional level.",
                default_value=LogisticRegressionDefaultParameters.AllowUnknownLevels,
                release_state=ReleaseState.Alpha
            )
    ) -> (
            UntrainedLearnerOutputPort(
                name="Untrained model",
                friendly_name="Untrained model",
                description="An untrained classificaiton model",
            ),
    ):
        input_values = locals()
        output_values = MulticlassLogisticRegressionModule.create_logistic_regression_multiclassifier(**input_values)
        return output_values

    @staticmethod
    def create_logistic_regression_multiclassifier(
            mode: CreateLearnerMode = LogisticRegressionDefaultParameters.Mode,
            optimization_tolerance: float = LogisticRegressionDefaultParameters.OptimizationTolerance,
            ps_optimization_tolerance: ParameterRangeSettings =
            LogisticRegressionDefaultParameters.PsOptimizationTolerance,
            l1_weight: float = LogisticRegressionDefaultParameters.L1Weight,
            ps_l1_weight: ParameterRangeSettings = LogisticRegressionDefaultParameters.PsL1Weight,
            l2_weight: float = LogisticRegressionDefaultParameters.L2Weight,
            ps_l2_weight: ParameterRangeSettings = LogisticRegressionDefaultParameters.PsL2Weight,
            memory_size: int = LogisticRegressionDefaultParameters.MemorySize,
            ps_memory_size: ParameterRangeSettings = LogisticRegressionDefaultParameters.PsMemorySize,
            random_number_seed: int = LogisticRegressionDefaultParameters.RandomNumberSeed,
            allow_unknown_levels: bool = LogisticRegressionDefaultParameters.AllowUnknownLevels,
    ):
        setting = LogisticRegressionSetting.init(**locals())

        return tuple([LogisticRegressionMultiClassifier(setting)])


class LogisticRegressionMultiClassifierSetting(LogisticRegressionSetting):
    # Compatible with old models
    pass


class LogisticRegressionMultiClassifier(MultiClassificationLearner):
    def __init__(self, setting: LogisticRegressionSetting):
        super().__init__(setting=setting, task_type=TaskType.MultiClassification)

    @property
    def parameter_mapping(self):
        return {
            'tol': RestoreInfo(MulticlassLogisticRegressionModule._args.optimization_tolerance.friendly_name),
            'C': RestoreInfo(MulticlassLogisticRegressionModule._args.l2_weight.friendly_name,
                             lambda x: 0 if x > 9e21 else 1 / x)
        }

    def init_model(self):
        # TODO: how to handle l2_weight == 0 ?
        if self.setting.l2_weight < 1e-9:
            param_c = 1e22
        else:
            param_c = 1 / self.setting.l2_weight
        self.model = LogisticRegression(
            penalty='l2',
            tol=self.setting.optimization_tolerance,
            C=param_c,
            random_state=self.setting.random_number_seed,
            solver='sag',
            multi_class='multinomial',
            verbose=False
        )
