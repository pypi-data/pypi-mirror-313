from sklearn.linear_model import Perceptron

from azureml.studio.common.parameter_range import ParameterRangeSettings, Sweepable
from azureml.studio.modulehost.attributes import ModeParameter, FloatParameter, IntParameter, \
    ParameterRangeParameter, UntrainedLearnerOutputPort, ModuleMeta, BooleanParameter
from azureml.studio.internal.attributes.release_state import ReleaseState
from azureml.studio.modulehost.module_reflector import module_entry, BaseModule
from azureml.studio.modulehost.constants import FLOAT_MIN_POSITIVE, FLOAT_MAX, UINT32_MAX
from azureml.studio.modules.ml.common.base_learner import TaskType, CreateLearnerMode, RestoreInfo
from azureml.studio.modules.ml.common.base_learner_setting import BaseLearnerSetting
from azureml.studio.modules.ml.common.supervised_learners import BinaryClassificationLearner


class TwoClassAveragedPerceptronModuleDefaultParameters:
    Mode = CreateLearnerMode.SingleParameter
    InitialLearningRate = 1.0
    MaximumNumberOfIterations = 10
    PsInitialLearningRate = "0.1; 0.5; 1.0"
    PsMaximumNumberOfIterations = "1; 10"
    RandomNumberSeed = None
    AllowUnknownLevels = True

    @classmethod
    def to_dict(cls):
        return {
            "mode": cls.Mode,
            "initial_learning_rate": cls.InitialLearningRate,
            "maximum_number_of_iterations": cls.MaximumNumberOfIterations,
            "ps_initial_learning_rate": ParameterRangeSettings.from_literal(cls.PsInitialLearningRate),
            "ps_maximum_number_of_iterations": ParameterRangeSettings.from_literal(cls.PsMaximumNumberOfIterations),
            "random_number_seed": cls.RandomNumberSeed,
            "allow_unknown_levels": cls.AllowUnknownLevels,
        }


class TwoClassAveragedPerceptronModule(BaseModule):

    @staticmethod
    @module_entry(ModuleMeta(
        name="Two-Class Averaged Perceptron",
        description="Creates an averaged perceptron binary classification model.",
        category="Machine Learning Algorithms/Classification",
        version="2.0",
        owner="Microsoft Corporation",
        family_id="5ED44CAA-5360-407D-AE6C-7A88C491474A",
        release_state=ReleaseState.Release,
        is_deterministic=True,
    ))
    def run(
            mode: ModeParameter(
                CreateLearnerMode,
                name="Create trainer mode",
                friendly_name="Create trainer mode",
                description="Create advanced learner options",
                default_value=TwoClassAveragedPerceptronModuleDefaultParameters.Mode,
            ),
            initial_learning_rate: FloatParameter(
                name="Initial learning rate",
                friendly_name="Learning rate",
                description="The initial learning rate for the Stochastic Gradient Descent optimizer. ",
                default_value=TwoClassAveragedPerceptronModuleDefaultParameters.InitialLearningRate,
                parent_parameter="Create trainer mode",
                parent_parameter_val=(CreateLearnerMode.SingleParameter,),
                min_value=FLOAT_MIN_POSITIVE,
            ),
            maximum_number_of_iterations: IntParameter(
                name="Maximum number of iterations",
                friendly_name="Maximum number of iterations",
                description="The number of Stochastic Gradient Descent iterations to be performed "
                            "over the training dataset. ",
                default_value=TwoClassAveragedPerceptronModuleDefaultParameters.MaximumNumberOfIterations,
                parent_parameter="Create trainer mode",
                parent_parameter_val=(CreateLearnerMode.SingleParameter,),
                min_value=1,
            ),
            ps_initial_learning_rate: ParameterRangeParameter(
                name="Range for initial learning rate",
                friendly_name="Learning rate",
                description="Range for initial learning rate for the Stochastic Gradient Descent optimizer. ",
                default_value=TwoClassAveragedPerceptronModuleDefaultParameters.PsInitialLearningRate,
                parent_parameter="Create trainer mode",
                parent_parameter_val=(CreateLearnerMode.ParameterRange,),
                min_limit=FLOAT_MIN_POSITIVE,
                max_limit=FLOAT_MAX,
                is_int=False,
                is_log=True,
                slider_min=0.0001,
                slider_max=1,
            ),
            ps_maximum_number_of_iterations: ParameterRangeParameter(
                name="Range for maximum number of iterations",
                friendly_name="Maximum number of iterations",
                description="Range for the number of Stochastic Gradient Descent iterations to be performed "
                            "over the training dataset. ",
                default_value=TwoClassAveragedPerceptronModuleDefaultParameters.PsMaximumNumberOfIterations,
                parent_parameter="Create trainer mode",
                parent_parameter_val=(CreateLearnerMode.ParameterRange,),
                min_limit=1,
                max_limit=2147483647,
                is_int=True,
                is_log=True,
                slider_min=1,
                slider_max=1000,
            ),
            random_number_seed: IntParameter(
                name="Random number seed",
                friendly_name="Random number seed",
                min_value=0,
                max_value=UINT32_MAX,
                is_optional=True,
                description="The seed for the random number generator used by the model. Leave blank for default.",
            ),
            allow_unknown_levels: BooleanParameter(
                name="Allow unknown levels in categorical features",
                friendly_name="Allow unknown categorical levels",
                description="If true creates an additional level for each categorical column. "
                            "Any levels in the test dataset not available in the training dataset "
                            "are mapped to this additional level.",
                default_value=TwoClassAveragedPerceptronModuleDefaultParameters.AllowUnknownLevels,
                release_state=ReleaseState.Alpha
            )
    ) -> (
            UntrainedLearnerOutputPort(
                name="Untrained model",
                friendly_name="Untrained model",
                description="An untrained binary classification model that can be connected "
                            "to the Create One-vs-All Multi-class Classifier or Train Generic Model "
                            "or Cross Validate Model modules.",
            ),
    ):
        input_values = locals()
        output_values = TwoClassAveragedPerceptronModule.create_average_perceptron_biclassifier(**input_values)
        return output_values

    @staticmethod
    def create_average_perceptron_biclassifier(
            mode: CreateLearnerMode = TwoClassAveragedPerceptronModuleDefaultParameters.Mode,
            initial_learning_rate: float = TwoClassAveragedPerceptronModuleDefaultParameters.InitialLearningRate,
            ps_initial_learning_rate: ParameterRangeSettings =
            TwoClassAveragedPerceptronModuleDefaultParameters.PsInitialLearningRate,
            maximum_number_of_iterations: int =
            TwoClassAveragedPerceptronModuleDefaultParameters.MaximumNumberOfIterations,
            ps_maximum_number_of_iterations: ParameterRangeSettings =
            TwoClassAveragedPerceptronModuleDefaultParameters.PsMaximumNumberOfIterations,
            random_number_seed: int = TwoClassAveragedPerceptronModuleDefaultParameters.RandomNumberSeed,
            allow_unknown_levels: bool = TwoClassAveragedPerceptronModuleDefaultParameters.AllowUnknownLevels,
    ):
        setting = AveragePerceptronBiClassifierSetting()
        if mode == CreateLearnerMode.SingleParameter:
            setting.init_single(
                initial_learning_rate=initial_learning_rate,
                maximum_number_of_iterations=maximum_number_of_iterations,
                random_number_seed=random_number_seed, )
        else:
            setting.init_range(
                ps_initial_learning_rate=ps_initial_learning_rate,
                ps_maximum_number_of_iterations=ps_maximum_number_of_iterations,
                random_number_seed=random_number_seed)
        return tuple([AveragePerceptronBiClassifier(setting)])


class AveragePerceptronBiClassifierSetting(BaseLearnerSetting):
    def __init__(self):
        super().__init__()
        self.initial_learning_rate = TwoClassAveragedPerceptronModuleDefaultParameters.InitialLearningRate
        self.maximum_number_of_iterations = TwoClassAveragedPerceptronModuleDefaultParameters.MaximumNumberOfIterations
        self.create_learner_mode = TwoClassAveragedPerceptronModuleDefaultParameters.Mode
        self.parameter_range = {
            'eta0': Sweepable.from_prs("eta0", ParameterRangeSettings.from_literal(
                TwoClassAveragedPerceptronModuleDefaultParameters.PsInitialLearningRate)).attribute_value,
            'max_iter': Sweepable.from_prs("max_iter", ParameterRangeSettings.from_literal(
                TwoClassAveragedPerceptronModuleDefaultParameters.PsMaximumNumberOfIterations)).attribute_value,
        }

    def init_single(
            self,
            initial_learning_rate: float = TwoClassAveragedPerceptronModuleDefaultParameters.InitialLearningRate,
            maximum_number_of_iterations: int =
            TwoClassAveragedPerceptronModuleDefaultParameters.MaximumNumberOfIterations,
            random_number_seed: int = TwoClassAveragedPerceptronModuleDefaultParameters.RandomNumberSeed
    ):
        self.initial_learning_rate = initial_learning_rate
        self.maximum_number_of_iterations = maximum_number_of_iterations
        self.random_number_seed = random_number_seed
        self.create_learner_mode = CreateLearnerMode.SingleParameter

    def init_range(self, ps_initial_learning_rate: ParameterRangeSettings = None,
                   ps_maximum_number_of_iterations: ParameterRangeSettings = None,
                   random_number_seed: int = None
                   ):
        self.create_learner_mode = CreateLearnerMode.ParameterRange
        self.random_number_seed = random_number_seed

        self.add_sweepable(Sweepable.from_prs('eta0', ps_initial_learning_rate))
        self.add_sweepable(Sweepable.from_prs('max_iter', ps_maximum_number_of_iterations))


class AveragePerceptronBiClassifier(BinaryClassificationLearner):
    def __init__(self, setting: AveragePerceptronBiClassifierSetting):
        super().__init__(setting, task_type=TaskType.BinaryClassification)

    @property
    def parameter_mapping(self):
        return {
            'eta0': RestoreInfo(TwoClassAveragedPerceptronModule._args.initial_learning_rate.friendly_name),
            'max_iter': RestoreInfo(TwoClassAveragedPerceptronModule._args.maximum_number_of_iterations.friendly_name)
        }

    def init_model(self):
        self.model = Perceptron(
            eta0=self.setting.initial_learning_rate,
            max_iter=self.setting.maximum_number_of_iterations,
            tol=1e-5,
            random_state=self.setting.random_number_seed,
        )
