from azureml.studio.common.parameter_range import ParameterRangeSettings, Sweepable
from azureml.studio.modules.ml.common.base_learner import CreateLearnerMode
from azureml.studio.modules.ml.common.base_learner_setting import BaseLearnerSetting


class LogisticRegressionDefaultParameters:
    Mode = CreateLearnerMode.SingleParameter
    OptimizationTolerance = 1e-07
    L1Weight = 1.0
    L2Weight = 1.0
    MemorySize = 20
    PsOptimizationTolerance = "0.00001; 0.00000001"
    PsL1Weight = "0.0; 0.01; 0.1; 1.0"
    PsL2Weight = "0.01; 0.1; 1.0"
    PsMemorySize = "5; 20; 50"
    RandomNumberSeed = None
    AllowUnknownLevels = True

    @classmethod
    def to_dict(cls):
        return {
            "mode": cls.Mode,
            "optimization_tolerance": cls.OptimizationTolerance,
            "l1_weight": cls.L1Weight,
            "l2_weight": cls.L2Weight,
            "memory_size": cls.MemorySize,
            "ps_optimization_tolerance": ParameterRangeSettings.from_literal(cls.PsOptimizationTolerance),
            "ps_l1_weight": ParameterRangeSettings.from_literal(cls.PsL1Weight),
            "ps_l2_weight": ParameterRangeSettings.from_literal(cls.PsL2Weight),
            "ps_memory_size": ParameterRangeSettings.from_literal(cls.PsMemorySize),
            "random_number_seed": cls.RandomNumberSeed,
            "allow_unknown_levels": cls.AllowUnknownLevels,
        }


class LogisticRegressionSetting(BaseLearnerSetting):
    """Logistic Regression

        Remaining some problem:
        1. v1 supports both l1 and l2 penalty meanwhile, but sklearn only supports l1 or l2.
        2. Memory size for L-BFGS was not supported.
    """

    def __init__(self, mode, optimization_tolerance: float = LogisticRegressionDefaultParameters.OptimizationTolerance,
                 l2_weight: float = LogisticRegressionDefaultParameters.L2Weight,
                 memory_size: int = LogisticRegressionDefaultParameters.MemorySize,
                 random_number_seed: int = LogisticRegressionDefaultParameters.RandomNumberSeed,
                 ps_optimization_tolerance=ParameterRangeSettings.from_literal(
                     LogisticRegressionDefaultParameters.PsOptimizationTolerance),
                 ps_l2_weight=ParameterRangeSettings.from_literal(LogisticRegressionDefaultParameters.PsL2Weight,
                                                                  ),
                 ps_memory_size=ParameterRangeSettings.from_literal(LogisticRegressionDefaultParameters.PsMemorySize)
                 ):
        """Initialize a LogisticRegressionSetting

        :param mode: CreateLearnerMode
        :param optimization_tolerance: float, optimization tolerance, tol
        :param l2_weight: float, l2 penalty term, 1/C
        :param memory_size: int, memory size for L-BFGS, not supported yet
        :param random_number_seed: int, Random number seed, random_state
        :param ps_optimization_tolerance: ParameterRange, range of Optimization tolerance, tol
        :param ps_l2_weight: ParameterRange, range of l2_weight, 1/C
        :param ps_memory_size: ParameterRange, range of memory size for L-BFGS, not supported yet
        """
        super().__init__()
        self.optimization_tolerance = optimization_tolerance
        self.l2_weight = l2_weight
        self.memory_size = memory_size
        self.random_number_seed = random_number_seed
        self.penalty = 'l2'
        self.create_learner_mode = mode
        s_l2_weight = Sweepable.from_prs("l2_weight", ps_l2_weight).attribute_value
        self.parameter_range = {
            'tol': Sweepable.from_prs("tol", ps_optimization_tolerance).attribute_value,
            'C': [1e22 if l2 < 1e-9 else 1 / l2 for l2 in s_l2_weight]
        }

    @staticmethod
    def init(mode, optimization_tolerance, ps_optimization_tolerance, l1_weight, ps_l1_weight, l2_weight, ps_l2_weight,
             memory_size, ps_memory_size, random_number_seed, allow_unknown_levels, ):
        if mode == CreateLearnerMode.SingleParameter:
            setting = LogisticRegressionSetting.init_single(
                optimization_tolerance=optimization_tolerance,
                l2_weight=l2_weight,
                memory_size=memory_size,
                random_number_seed=random_number_seed)
        else:
            setting = LogisticRegressionSetting.init_range(
                ps_optimization_tolerance=ps_optimization_tolerance,
                ps_l2_weight=ps_l2_weight,
                ps_memory_size=ps_memory_size,
                random_number_seed=random_number_seed
            )
        return setting

    @staticmethod
    def init_single(
            optimization_tolerance: float = LogisticRegressionDefaultParameters.OptimizationTolerance,
            l2_weight: float = LogisticRegressionDefaultParameters.L2Weight,
            memory_size: int = LogisticRegressionDefaultParameters.MemorySize,
            random_number_seed: int = LogisticRegressionDefaultParameters.RandomNumberSeed):
        return LogisticRegressionSetting(mode=CreateLearnerMode.SingleParameter, **locals())

    @staticmethod
    def init_range(
            ps_optimization_tolerance: ParameterRangeSettings = None,
            ps_l2_weight: ParameterRangeSettings = None,
            ps_memory_size: ParameterRangeSettings = None,
            random_number_seed: int = None):
        return LogisticRegressionSetting(mode=CreateLearnerMode.ParameterRange, **locals())
