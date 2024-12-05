from sklearn.svm import LinearSVC

from azureml.studio.common.parameter_range import ParameterRangeSettings, Sweepable
from azureml.studio.modulehost.attributes import ModeParameter, BooleanParameter, FloatParameter, IntParameter, \
    ParameterRangeParameter, UntrainedLearnerOutputPort, ModuleMeta
from azureml.studio.internal.attributes.release_state import ReleaseState
from azureml.studio.modulehost.module_reflector import module_entry, BaseModule
from azureml.studio.modulehost.constants import FLOAT_MIN_POSITIVE, FLOAT_MAX, UINT32_MAX
from azureml.studio.modules.ml.common.base_learner import TaskType, CreateLearnerMode, RestoreInfo
from azureml.studio.modules.ml.common.base_learner_setting import BaseLearnerSetting
from azureml.studio.modules.ml.common.supervised_learners import BinaryClassificationLearner


class TwoClassSupportVectorMachineModuleDefaultParameters:
    Mode = CreateLearnerMode.SingleParameter
    NumIterations = 10
    PsNumIterations = "1; 10; 100"
    L1Lambda = 0.001
    PsL1Lambda = "0.00001; 0.0001; 0.001; 0.01; 0.1"
    NormalizeFeatures = True
    PerformProjection = False
    RandomNumberSeed = None
    AllowUnknownLevels = True

    @classmethod
    def to_dict(cls):
        return {
            "mode": cls.Mode,
            "num_iterations": cls.NumIterations,
            "ps_num_iterations": ParameterRangeSettings.from_literal(cls.PsNumIterations),
            "l1_lambda": cls.L1Lambda,
            "ps_l1_lambda": ParameterRangeSettings.from_literal(cls.PsL1Lambda),
            "normalize_features": cls.NormalizeFeatures,
            "perform_projection": cls.PerformProjection,
            "random_number_seed": cls.RandomNumberSeed,
            "allow_unknown_levels": cls.AllowUnknownLevels,
        }


class TwoClassSupportVectorMachineModule(BaseModule):

    @staticmethod
    @module_entry(ModuleMeta(
        name="Two-Class Support Vector Machine",
        description="Creates a binary classification model using the Support Vector Machine algorithm.",
        category="Machine Learning Algorithms/Classification",
        version="2.0",
        owner="Microsoft Corporation",
        family_id="12D8479B-74B4-4E67-B8DE-D32867380E20",
        release_state=ReleaseState.Release,
        is_deterministic=True,
    ))
    def run(
            mode: ModeParameter(
                CreateLearnerMode,
                name="Create trainer mode",
                friendly_name="Create trainer mode",
                description="Create advanced learner options",
                default_value=TwoClassSupportVectorMachineModuleDefaultParameters.Mode,
            ),
            num_iterations: IntParameter(
                name="Number of iterations",
                friendly_name="Number of iterations",
                description="The number of iterations.",
                default_value=TwoClassSupportVectorMachineModuleDefaultParameters.NumIterations,
                parent_parameter="Create trainer mode",
                parent_parameter_val=(CreateLearnerMode.SingleParameter,),
                min_value=1,
            ),
            ps_num_iterations: ParameterRangeParameter(
                name="Range for number of iterations",
                friendly_name="Number of iterations",
                description="The range for the number of iterations.",
                default_value=TwoClassSupportVectorMachineModuleDefaultParameters.PsNumIterations,
                parent_parameter="Create trainer mode",
                parent_parameter_val=(CreateLearnerMode.ParameterRange,),
                min_limit=1,
                max_limit=2147483647,
                is_int=True,
                is_log=True,
                slider_min=1,
                slider_max=1000,
            ),
            l1_lambda: FloatParameter(
                name="The value lambda",
                friendly_name="Lambda",
                description="Weight for L1 regularization. "
                            "Using a non-zero value avoids overfitting the model to the training dataset.",
                default_value=TwoClassSupportVectorMachineModuleDefaultParameters.L1Lambda,
                parent_parameter="Create trainer mode",
                parent_parameter_val=(CreateLearnerMode.SingleParameter,),
                min_value=FLOAT_MIN_POSITIVE,
            ),
            ps_l1_lambda: ParameterRangeParameter(
                name="Range for lambda",
                friendly_name="Lambda",
                description="Weight range for the for L1 regularization. "
                            "Using a non-zero value avoids overfitting the model to the training dataset.",
                default_value=TwoClassSupportVectorMachineModuleDefaultParameters.PsL1Lambda,
                parent_parameter="Create trainer mode",
                parent_parameter_val=(CreateLearnerMode.ParameterRange,),
                min_limit=FLOAT_MIN_POSITIVE,
                max_limit=FLOAT_MAX,
                is_int=False,
                is_log=True,
                slider_min=1E-06,
                slider_max=10,
            ),
            normalize_features: BooleanParameter(
                name="Normalize the features",
                friendly_name="Normalize features",
                description="If true normalize the features.",
                default_value=TwoClassSupportVectorMachineModuleDefaultParameters.NormalizeFeatures,
            ),
            perform_projection: BooleanParameter(
                name="Perform a projection to the unit-ball",
                friendly_name="Project to the unit-sphere",
                description="If true project the features to a unit circle.",
                default_value=TwoClassSupportVectorMachineModuleDefaultParameters.PerformProjection,
                release_state=ReleaseState.Alpha
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
                default_value=TwoClassSupportVectorMachineModuleDefaultParameters.AllowUnknownLevels,
                release_state=ReleaseState.Alpha
            )
    ) -> (
            UntrainedLearnerOutputPort(
                name="Untrained model",
                friendly_name="Untrained model",
                description="An untrained binary classification model that can be connected "
                            "to the Create One-vs-All Multiclass Classification Model or Train Generic Model "
                            "or Cross Validate Model modules.",
            ),
    ):
        input_values = locals()
        output_values = TwoClassSupportVectorMachineModule.create_support_vector_machine_biclassifier(**input_values)
        return output_values

    @staticmethod
    def create_support_vector_machine_biclassifier(
            mode: CreateLearnerMode,
            num_iterations: int = TwoClassSupportVectorMachineModuleDefaultParameters.NumIterations,
            ps_num_iterations: ParameterRangeSettings = None,
            l1_lambda: float = TwoClassSupportVectorMachineModuleDefaultParameters.L1Lambda,
            ps_l1_lambda: ParameterRangeSettings = None,
            random_number_seed: int = TwoClassSupportVectorMachineModuleDefaultParameters.RandomNumberSeed,
            perform_projection: bool = TwoClassSupportVectorMachineModuleDefaultParameters.PerformProjection,
            normalize_features: bool = TwoClassSupportVectorMachineModuleDefaultParameters.NormalizeFeatures,
            allow_unknown_levels: bool = TwoClassSupportVectorMachineModuleDefaultParameters.AllowUnknownLevels):
        setting = SupportVectorMachineBiClassifierSetting()
        if mode == CreateLearnerMode.SingleParameter:
            setting.init_single(
                num_iterations=num_iterations,
                l1_lambda=l1_lambda,
                random_number_seed=random_number_seed,
                perform_projection=perform_projection,
                normalize_features=normalize_features
            )
        else:
            setting.init_range(
                ps_num_iterations=ps_num_iterations, ps_l1_lambda=ps_l1_lambda,
                random_number_seed=random_number_seed, perform_projection=perform_projection,
                normalize_features=normalize_features)
        return tuple([SupportVectorMachineBiClassifier(setting)])


class SupportVectorMachineBiClassifierSetting(BaseLearnerSetting):
    def __init__(self):
        r"""
        there remains several problems.
        1. normalize_features seems also not be used in v1.
        2. sklearn do not support perform_projection
        3. we can not set L1 regularization weight in sklearn. so i use C = 1/(2*lambda) instead.
            Reason:
              sklearn: 0.5*||w|| + C*\sum{ci}
              v1: lambda * ||w|| + ?*\sum{ci}
              set ? = 1 and then,
              C = 1/(2*lambda
        """
        super().__init__()
        self.num_iterations = TwoClassSupportVectorMachineModuleDefaultParameters.NumIterations
        self.l1_lambda = TwoClassSupportVectorMachineModuleDefaultParameters.L1Lambda
        self.perform_projection = TwoClassSupportVectorMachineModuleDefaultParameters.PerformProjection
        self.normalize_features = TwoClassSupportVectorMachineModuleDefaultParameters.NormalizeFeatures
        self.create_learner_mode = TwoClassSupportVectorMachineModuleDefaultParameters.Mode
        s_l1_lambda = Sweepable.from_prs(
            "l1_lambda", ParameterRangeSettings.from_literal(
                TwoClassSupportVectorMachineModuleDefaultParameters.PsL1Lambda)).attribute_value
        self.parameter_range = {
            'max_iter': Sweepable.from_prs(
                "learning_rate_init", ParameterRangeSettings.from_literal(
                    TwoClassSupportVectorMachineModuleDefaultParameters.PsNumIterations)).attribute_value,
            'C': [1 / (2 * l1) for l1 in s_l1_lambda]
        }

    def init_single(self, num_iterations: int = TwoClassSupportVectorMachineModuleDefaultParameters.NumIterations,
                    l1_lambda: float = TwoClassSupportVectorMachineModuleDefaultParameters.L1Lambda,
                    random_number_seed: int = TwoClassSupportVectorMachineModuleDefaultParameters.RandomNumberSeed,
                    perform_projection: bool = TwoClassSupportVectorMachineModuleDefaultParameters.PerformProjection,
                    normalize_features: bool = TwoClassSupportVectorMachineModuleDefaultParameters.NormalizeFeatures):
        """

        :param num_iterations: int , Number of iterations. max_iter
        :param l1_lambda: float, >= 1e-6 .  Lambda. C=1/(2*lambda)
        :param random_number_seed: int, Random number seed. random_state
        :param perform_projection: bool, only implement False
        :param normalize_features: bool only implement True
        """
        self.create_learner_mode = CreateLearnerMode.SingleParameter
        self.num_iterations = num_iterations
        self.l1_lambda = l1_lambda
        self.random_number_seed = random_number_seed
        self.perform_projection = perform_projection
        self.normalize_features = normalize_features

    def init_range(self, ps_num_iterations: ParameterRangeSettings = None, ps_l1_lambda: ParameterRangeSettings = None,
                   random_number_seed: int = None, perform_projection: bool = False, normalize_features: bool = True):
        self.create_learner_mode = CreateLearnerMode.ParameterRange
        self.random_number_seed = random_number_seed
        self.perform_projection = perform_projection
        self.normalize_features = normalize_features

        self.add_sweepable(Sweepable.from_prs('max_iter', ps_num_iterations))
        s_l1_lambda = Sweepable.from_prs("l1_lambda", ps_l1_lambda).attribute_value
        self.add_list('C', [1 / (2 * l1) for l1 in s_l1_lambda])


class SupportVectorMachineBiClassifier(BinaryClassificationLearner):
    def __init__(self, setting: SupportVectorMachineBiClassifierSetting):
        super().__init__(setting, task_type=TaskType.BinaryClassification)

    @property
    def parameter_mapping(self):
        return {
            'max_iter': RestoreInfo(TwoClassSupportVectorMachineModule._args.num_iterations.friendly_name),
            'C': RestoreInfo(TwoClassSupportVectorMachineModule._args.l1_lambda.friendly_name,
                             inverse_func=lambda x: 0.5 / x)
        }

    def init_model(self):
        self.model = LinearSVC(
            penalty='l1',
            dual=False,
            max_iter=self.setting.num_iterations,
            C=1 / (2 * self.setting.l1_lambda),
            random_state=self.setting.random_number_seed
        )
