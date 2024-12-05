from sklearn.linear_model import SGDRegressor, Ridge

from azureml.studio.common.parameter_range import ParameterRangeSettings, Sweepable
from azureml.studio.common.types import AutoEnum
from azureml.studio.modulehost.attributes import ModeParameter, BooleanParameter, FloatParameter, IntParameter, \
    ParameterRangeParameter, UntrainedLearnerOutputPort, ModuleMeta, ItemInfo
from azureml.studio.internal.attributes.release_state import ReleaseState
from azureml.studio.modulehost.module_reflector import module_entry, BaseModule
from azureml.studio.modulehost.constants import FLOAT_MIN_POSITIVE, FLOAT_MAX, UINT32_MAX
from azureml.studio.modules.ml.common.base_learner import TaskType, CreateLearnerMode, RestoreInfo
from azureml.studio.modules.ml.common.base_learner_setting import BaseLearnerSetting
from azureml.studio.modules.ml.common.supervised_learners import RegressionLearner


class CreateLinearRegressionModelSolutionMethod(AutoEnum):
    OnlineGradientDescent: ItemInfo(name="Online Gradient Descent",
                                    friendly_name="Online Gradient Descent") = ()
    OrdinaryLeastSquares: ItemInfo(name="Ordinary Least Squares",
                                   friendly_name="Ordinary Least Squares") = ()


class LinearRegressionModuleDefaultParameters:
    SolutionMethod = CreateLinearRegressionModelSolutionMethod.OrdinaryLeastSquares
    Mode = CreateLearnerMode.SingleParameter
    NormalizeFeatures = True
    Averaged = True
    LearningRate = 0.1
    NumIterations = 10
    PsLearningRate = "0.025; 0.05; 0.1; 0.2"
    PsNumIterations = "1; 10; 100"
    DecreaseLearningRate = True
    L2RegularizerWeightOgd = 0.001
    L2RegularizerWeightOls = 0.001
    PsL2RegularizerWeight = "0.001; 0.01; 0.1"
    RandomNumberSeed = None
    Bias = True
    AllowUnknownLevels = True

    @classmethod
    def to_dict(cls):
        return {
            "solution_method": cls.SolutionMethod,
            "mode": cls.Mode,
            "normalize_features": cls.NormalizeFeatures,
            "averaged": cls.Averaged,
            "learning_rate": cls.LearningRate,
            "num_iterations": cls.NumIterations,
            "ps_learning_rate": ParameterRangeSettings.from_literal(cls.PsLearningRate),
            "ps_num_iterations": ParameterRangeSettings.from_literal(cls.PsNumIterations),
            "decrease_learning_rate": cls.DecreaseLearningRate,
            "l2_regularizer_weight_ogd": cls.L2RegularizerWeightOgd,
            "l2_regularizer_weight_ols": cls.L2RegularizerWeightOls,
            "ps_l2_regularizer_weight": ParameterRangeSettings.from_literal(cls.PsL2RegularizerWeight),
            "random_number_seed": cls.RandomNumberSeed,
            "bias": cls.Bias,
            "allow_unknown_levels": cls.AllowUnknownLevels,
        }


class LinearRegressionModule(BaseModule):

    @staticmethod
    @module_entry(ModuleMeta(
        name="Linear Regression",
        description="Creates a linear regression model.",
        category="Machine Learning Algorithms/Regression",
        version="3.0",
        owner="Microsoft Corporation",
        family_id="{31960A6F-789B-4CF7-88D6-2E1152C0BD1A}",
        release_state=ReleaseState.Release,
        is_deterministic=True,
    ))
    def run(
            solution_method: ModeParameter(
                CreateLinearRegressionModelSolutionMethod,
                name="Solution method",
                friendly_name="Solution method",
                description="Choose an optimization method",
                default_value=LinearRegressionModuleDefaultParameters.SolutionMethod,
            ),
            mode: ModeParameter(
                CreateLearnerMode,
                name="Create trainer mode",
                friendly_name="Create trainer mode",
                description="Create advanced learner options",
                default_value=LinearRegressionModuleDefaultParameters.Mode,
                parent_parameter="Solution method",
                parent_parameter_val=(CreateLinearRegressionModelSolutionMethod.OnlineGradientDescent,),
            ),
            normalize_features: BooleanParameter(
                name="Should input instances be normalized",
                friendly_name="Normalize features",
                description="Indicate whether instances should be normalized",
                default_value=LinearRegressionModuleDefaultParameters.NormalizeFeatures,
                parent_parameter="Solution method",
                parent_parameter_val=(CreateLinearRegressionModelSolutionMethod.OnlineGradientDescent,),
            ),
            averaged: BooleanParameter(
                name="Final hypothesis is averaged",
                friendly_name="Average final hypothesis",
                description="Indicate whether the final hypothesis should be averaged",
                default_value=LinearRegressionModuleDefaultParameters.Averaged,
                parent_parameter="Solution method",
                parent_parameter_val=(CreateLinearRegressionModelSolutionMethod.OnlineGradientDescent,),
                release_state=ReleaseState.Alpha
            ),
            learning_rate: FloatParameter(
                name="Learning rate",
                friendly_name="Learning rate",
                description="Specify the initial learning rate for the stochastic gradient descent optimizer",
                default_value=LinearRegressionModuleDefaultParameters.LearningRate,
                parent_parameter="Create trainer mode",
                parent_parameter_val=(CreateLearnerMode.SingleParameter,),
                min_value=FLOAT_MIN_POSITIVE,
            ),
            num_iterations: IntParameter(
                name="Number of epochs over which algorithm iterates through examples",
                friendly_name="Number of training epochs",
                description="Specify how many times the algorithm should iterate through examples. "
                            "For datasets with a small number of examples, "
                            "this number should be large to reach convergence.",
                default_value=LinearRegressionModuleDefaultParameters.NumIterations,
                parent_parameter="Create trainer mode",
                parent_parameter_val=(CreateLearnerMode.SingleParameter,),
                min_value=0,
            ),
            ps_learning_rate: ParameterRangeParameter(
                name="Range for learning rate",
                friendly_name="Learning rate",
                description="Specify the range for the initial learning rate "
                            "for the stochastic gradient descent optimizer",
                default_value=LinearRegressionModuleDefaultParameters.PsLearningRate,
                parent_parameter="Create trainer mode",
                parent_parameter_val=(CreateLearnerMode.ParameterRange,),
                min_limit=FLOAT_MIN_POSITIVE,
                max_limit=FLOAT_MAX,
                is_int=False,
                is_log=True,
                slider_min=0.0001,
                slider_max=1,
            ),
            ps_num_iterations: ParameterRangeParameter(
                name="Range for number of epochs over which algorithm iterates through examples",
                friendly_name="Number of training epochs",
                description="Specify range for how many times the algorithm should iterate through examples. "
                            "For datasets with a small number of examples, "
                            "this number should be large to reach convergence.",
                default_value=LinearRegressionModuleDefaultParameters.PsNumIterations,
                parent_parameter="Create trainer mode",
                parent_parameter_val=(CreateLearnerMode.ParameterRange,),
                min_limit=0,
                max_limit=2147483647,
                is_int=True,
                is_log=False,
                slider_min=1,
                slider_max=100,
            ),
            decrease_learning_rate: BooleanParameter(
                name="Decrease learning rate as iterations progress",
                friendly_name="Decrease learning rate",
                description="Indicate whether the learning rate should decrease as iterations progress",
                default_value=LinearRegressionModuleDefaultParameters.DecreaseLearningRate,
                parent_parameter="Solution method",
                parent_parameter_val=(CreateLinearRegressionModelSolutionMethod.OnlineGradientDescent,),
            ),
            l2_regularizer_weight_ogd: FloatParameter(
                name="L2 regularization term weight",
                friendly_name="L2 regularization weight",
                description="Specify the weight for L2 regularization. Use a non-zero value to avoid overfitting.",
                default_value=LinearRegressionModuleDefaultParameters.L2RegularizerWeightOgd,
                parent_parameter="Create trainer mode",
                parent_parameter_val=(CreateLearnerMode.SingleParameter,),
                min_value=0,
            ),
            l2_regularizer_weight_ols: FloatParameter(
                name="L2 regularization weight",
                friendly_name="L2 regularization weight",
                description="Specify the weight for the L2 regularization. Use a non-zero value to avoid overfitting.",
                default_value=LinearRegressionModuleDefaultParameters.L2RegularizerWeightOls,
                parent_parameter="Solution method",
                parent_parameter_val=(CreateLinearRegressionModelSolutionMethod.OrdinaryLeastSquares,),
                min_value=0,
            ),
            ps_l2_regularizer_weight: ParameterRangeParameter(
                name="Range for L2 regularization term weight",
                friendly_name="L2 regularization weight",
                description="Specify the range for the weight for L2 regularization. "
                            "Use a non-zero value to avoid overfitting.",
                default_value=LinearRegressionModuleDefaultParameters.PsL2RegularizerWeight,
                parent_parameter="Create trainer mode",
                parent_parameter_val=(CreateLearnerMode.ParameterRange,),
                min_limit=0,
                max_limit=FLOAT_MAX,
                is_int=False,
                is_log=False,
                slider_min=0,
                slider_max=1,
            ),
            random_number_seed: IntParameter(
                name="Random number seed",
                friendly_name="Random number seed",
                min_value=0,
                max_value=UINT32_MAX,
                is_optional=True,
                description="Specify a value to seed the random number generator used by the model. "
                            "Leave blank for default.",
            ),
            bias: BooleanParameter(
                name="Include intercept term",
                friendly_name="Include intercept term",
                description="Indicate whether an additional term should be added for the intercept",
                default_value=LinearRegressionModuleDefaultParameters.Bias,
                parent_parameter="Solution method",
                parent_parameter_val=(CreateLinearRegressionModelSolutionMethod.OrdinaryLeastSquares,),
            ),
            allow_unknown_levels: BooleanParameter(
                name="Allow unknown levels in categorical features",
                friendly_name="Allow unknown categorical levels",
                description="Indicate whether an additional level should be created for each categorical column. "
                            "Any levels in the test dataset not available in the training dataset "
                            "are mapped to this additional level.",
                default_value=LinearRegressionModuleDefaultParameters.AllowUnknownLevels,
                release_state=ReleaseState.Alpha
            )
    ) -> (
            UntrainedLearnerOutputPort(
                name="Untrained model",
                friendly_name="Untrained model",
                description="An untrained regression model",
            ),
    ):
        input_values = locals()
        output_values = LinearRegressionModule.create_linear_regressor(**input_values)
        return output_values

    @staticmethod
    def create_linear_regressor(
            solution_method: CreateLinearRegressionModelSolutionMethod =
            LinearRegressionModuleDefaultParameters.SolutionMethod,
            mode: CreateLearnerMode = LinearRegressionModuleDefaultParameters.Mode,
            learning_rate: float = LinearRegressionModuleDefaultParameters.LearningRate,
            ps_learning_rate: ParameterRangeSettings = LinearRegressionModuleDefaultParameters.PsLearningRate,
            num_iterations: int = LinearRegressionModuleDefaultParameters.NumIterations,
            ps_num_iterations: ParameterRangeSettings = LinearRegressionModuleDefaultParameters.PsNumIterations,
            l2_regularizer_weight_ogd: float = LinearRegressionModuleDefaultParameters.L2RegularizerWeightOgd,
            l2_regularizer_weight_ols: float = LinearRegressionModuleDefaultParameters.L2RegularizerWeightOls,
            ps_l2_regularizer_weight: ParameterRangeSettings =
            LinearRegressionModuleDefaultParameters.PsL2RegularizerWeight,
            normalize_features: bool = LinearRegressionModuleDefaultParameters.NormalizeFeatures,
            averaged: bool = LinearRegressionModuleDefaultParameters.Averaged,
            decrease_learning_rate: bool = LinearRegressionModuleDefaultParameters.DecreaseLearningRate,
            bias: bool = LinearRegressionModuleDefaultParameters.Bias,
            random_number_seed: int = LinearRegressionModuleDefaultParameters.RandomNumberSeed,
            allow_unknown_levels: bool = LinearRegressionModuleDefaultParameters.AllowUnknownLevels,
    ):
        if solution_method == CreateLinearRegressionModelSolutionMethod.OnlineGradientDescent:
            setting = SGDLinearRegressorSetting()
            if mode == CreateLearnerMode.SingleParameter:
                setting.init_single(
                    learning_rate=learning_rate,
                    num_iterations=num_iterations,
                    l2_regularizer_weight=l2_regularizer_weight_ogd,
                    normalize_features=normalize_features,
                    averaged=averaged,
                    decrease_learning_rate=decrease_learning_rate,
                    random_number_seed=random_number_seed)
            else:
                setting.init_range(
                    ps_learning_rate=ps_learning_rate,
                    ps_num_iterations=ps_num_iterations,
                    ps_l2_regularizer_weight=ps_l2_regularizer_weight,
                    normalize_features=normalize_features,
                    averaged=averaged,
                    decrease_learning_rate=decrease_learning_rate,
                    random_number_seed=random_number_seed)
            return tuple([SGDLinearRegressor(setting)])
        elif solution_method == CreateLinearRegressionModelSolutionMethod.OrdinaryLeastSquares:
            setting = OrdinaryLeastSquaresRegressorSetting()
            setting.init_single(l2_regularizer_weight=l2_regularizer_weight_ols, bias=bias)
            return tuple([OrdinaryLeastSquaresRegressor(setting)])
        else:
            # todo : raise InvalidLearner error
            pass


class SGDLinearRegressorSetting(BaseLearnerSetting):
    def __init__(self):
        """
        there remains following problems:
        1. average_final_hypothesis, what is the usage of it?
        """
        super().__init__()
        self.learning_rate = LinearRegressionModuleDefaultParameters.LearningRate
        self.num_iterations = LinearRegressionModuleDefaultParameters.NumIterations
        self.l2_regularizer_weight = LinearRegressionModuleDefaultParameters.L2RegularizerWeightOgd
        self.normalize_features = LinearRegressionModuleDefaultParameters.NormalizeFeatures
        self.averaged = LinearRegressionModuleDefaultParameters.Averaged
        self.decrease_learning_rate = LinearRegressionModuleDefaultParameters.DecreaseLearningRate
        self.random_number_seed = LinearRegressionModuleDefaultParameters.RandomNumberSeed
        self.create_learner_mode = LinearRegressionModuleDefaultParameters.Mode
        self.parameter_range = {
            'eta0': Sweepable.from_prs(
                "eta0", ParameterRangeSettings.from_literal(
                    LinearRegressionModuleDefaultParameters.PsLearningRate)).attribute_value,
            'max_iter': Sweepable.from_prs(
                "max_iter", ParameterRangeSettings.from_literal(
                    LinearRegressionModuleDefaultParameters.PsNumIterations)).attribute_value,
            'alpha': Sweepable.from_prs(
                "alpha", ParameterRangeSettings.from_literal(
                    LinearRegressionModuleDefaultParameters.PsL2RegularizerWeight)).attribute_value,
        }

    def init_single(
            self,
            learning_rate: float = LinearRegressionModuleDefaultParameters.LearningRate,
            num_iterations: int = LinearRegressionModuleDefaultParameters.NumIterations,
            l2_regularizer_weight: float = LinearRegressionModuleDefaultParameters.L2RegularizerWeightOgd,
            normalize_features: bool = LinearRegressionModuleDefaultParameters.NormalizeFeatures,
            averaged: bool = LinearRegressionModuleDefaultParameters.Averaged,
            decrease_learning_rate: bool = LinearRegressionModuleDefaultParameters.DecreaseLearningRate,
            random_number_seed: int = LinearRegressionModuleDefaultParameters.RandomNumberSeed
    ):
        """
        :param learning_rate: float, Learning Rate, eta0(initial learning rate)
        :param num_iterations: int, Number of training epochs, max_iter
        :param l2_regularizer_weight: float, L2 regularization weight, penalty='l2', alpha=l2_regularization_weight
        :param normalize_features: bool, Normalize features and did not work in v1, x
        :param averaged: bool, if set to false, the training process will report error in studio v1. ?
        :param decrease_learning_rate: bool, Decrease learning rate, learning_rate='adaptive' if True else 'constant'
        :param random_number_seed: int,
        """
        self.create_learner_mode = CreateLearnerMode.SingleParameter
        self.learning_rate = learning_rate
        self.num_iterations = num_iterations
        self.l2_regularizer_weight = l2_regularizer_weight
        self.normalize_features = normalize_features
        self.averaged = averaged
        self.decrease_learning_rate = decrease_learning_rate
        self.random_number_seed = random_number_seed

    def init_range(self, ps_learning_rate: ParameterRangeSettings = None,
                   ps_num_iterations: ParameterRangeSettings = None,
                   ps_l2_regularizer_weight: ParameterRangeSettings = None,
                   normalize_features: bool = True, averaged: bool = True, decrease_learning_rate: bool = True,
                   random_number_seed: int = None):
        self.create_learner_mode = CreateLearnerMode.ParameterRange
        self.normalize_features = normalize_features
        self.averaged = averaged
        self.decrease_learning_rate = decrease_learning_rate
        self.random_number_seed = random_number_seed

        self.add_sweepable(Sweepable.from_prs('eta0', ps_learning_rate))
        self.add_sweepable(Sweepable.from_prs('max_iter', ps_num_iterations))
        self.add_sweepable(Sweepable.from_prs('alpha', ps_l2_regularizer_weight))


class SGDLinearRegressor(RegressionLearner):
    def __init__(self, setting: SGDLinearRegressorSetting):
        super(SGDLinearRegressor, self).__init__(setting=setting, task_type=TaskType.Regression)

    @property
    def parameter_mapping(self):
        return {
            'alpha': RestoreInfo(LinearRegressionModule._args.l2_regularizer_weight_ogd.friendly_name),
            'max_iter': RestoreInfo(LinearRegressionModule._args.num_iterations.friendly_name),
            'eta0': RestoreInfo(LinearRegressionModule._args.learning_rate.friendly_name)
        }

    def init_model(self):
        self.model = SGDRegressor(
            eta0=self.setting.learning_rate,
            max_iter=self.setting.num_iterations, tol=1e-5,
            alpha=self.setting.l2_regularizer_weight, penalty='l2',
            learning_rate='invscaling' if self.setting.decrease_learning_rate else 'constant',
            random_state=self.setting.random_number_seed,
        )


class OrdinaryLeastSquaresRegressorSetting(BaseLearnerSetting):
    def __init__(self):
        super().__init__()
        self.l2_regularizer_weight = LinearRegressionModuleDefaultParameters.L2RegularizerWeightOls
        self.bias = LinearRegressionModuleDefaultParameters.Bias
        self.create_learner_mode = LinearRegressionModuleDefaultParameters.Mode

    def init_single(
            self,
            l2_regularizer_weight: float = LinearRegressionModuleDefaultParameters.L2RegularizerWeightOls,
            bias: bool = LinearRegressionModuleDefaultParameters.Bias,
            random_number_seed: int = LinearRegressionModuleDefaultParameters.RandomNumberSeed
    ):
        """

        :param l2_regularizer_weight: float, L2 regularization weight. alpha
        :param bias: bool, Include intercept term, fit_intercept = bias
        :param random_number_seed: random_number_seed: int,
        """
        self.create_learner_mode = CreateLearnerMode.SingleParameter
        self.l2_regularizer_weight = l2_regularizer_weight
        self.bias = bias
        self.random_number_seed = random_number_seed

    def init_range(self, l2_regularizer_weight: float = 0.001, bias: bool = True, random_number_seed: int = None):
        """

        :param l2_regularizer_weight: float, L2 regularization weight. alpha
        :param bias: bool, Include intercept term, fit_intercept = bias
        :param random_number_seed: random_number_seed: int,
        """
        self.create_learner_mode = CreateLearnerMode.ParameterRange
        self.l2_regularizer_weight = l2_regularizer_weight
        self.bias = bias
        self.random_number_seed = random_number_seed


class OrdinaryLeastSquaresRegressor(RegressionLearner):
    def __init__(self, setting: OrdinaryLeastSquaresRegressorSetting):
        super().__init__(setting=setting, task_type=TaskType.Regression)

    def init_model(self):
        self.model = Ridge(
            alpha=self.setting.l2_regularizer_weight, tol=1e-5,
            fit_intercept=self.setting.bias,
            random_state=self.setting.random_number_seed,
        )
