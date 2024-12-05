from azureml.studio.common.parameter_range import ParameterRangeSettings, Sweepable
from azureml.studio.modules.ml.common.base_learner import CreateLearnerMode
from azureml.studio.modules.ml.common.base_learner_setting import BaseLearnerSetting

# LightGBM has hard coded upper bound check for parameter 'num_leaves' value. Find more info in
# https://github.com/microsoft/LightGBM/blob/aab8fc18a259ca9ca95db5bac203b81cb2e1ad49/src/io/config_auto.cpp#L326
NUM_LEAVES_UPPER_BOUND = 131072


class BoostedDecisionTreeDefaultParameters:
    Mode = CreateLearnerMode.SingleParameter
    NumberOfLeaves = 20
    MinimumLeafInstances = 10
    LearningRate = 0.2
    NumTrees = 100
    PsNumberOfLeaves = "2; 8; 32; 128"
    PsMinimumLeafInstances = "1; 10; 50"
    PsLearningRate = "0.025; 0.05; 0.1; 0.2; 0.4"
    PsNumTrees = "20; 100; 500"
    RandomNumberSeed = None
    AllowUnknownLevels = True

    @classmethod
    def to_dict(cls):
        return {
            "mode": cls.Mode,
            "number_of_leaves": cls.NumberOfLeaves,
            "minimum_leaf_instances": cls.MinimumLeafInstances,
            "learning_rate": cls.LearningRate,
            "num_trees": cls.NumTrees,
            "ps_number_of_leaves": ParameterRangeSettings.from_literal(cls.PsNumberOfLeaves),
            "ps_minimum_leaf_instances": ParameterRangeSettings.from_literal(cls.PsMinimumLeafInstances),
            "ps_learning_rate": ParameterRangeSettings.from_literal(cls.PsLearningRate),
            "ps_num_trees": ParameterRangeSettings.from_literal(cls.PsNumTrees),
            "random_number_seed": cls.RandomNumberSeed,
            "allow_unknown_levels": cls.AllowUnknownLevels,
        }


class BoostDecisionTreeSetting(BaseLearnerSetting):
    def __init__(self,
                 mode=BoostedDecisionTreeDefaultParameters.Mode,
                 number_of_leaves=BoostedDecisionTreeDefaultParameters.NumberOfLeaves,
                 minimum_leaf_instances=BoostedDecisionTreeDefaultParameters.MinimumLeafInstances,
                 learning_rate=BoostedDecisionTreeDefaultParameters.LearningRate,
                 num_trees=BoostedDecisionTreeDefaultParameters.NumTrees,
                 random_number_seed=BoostedDecisionTreeDefaultParameters.RandomNumberSeed,
                 ps_number_of_leaves=ParameterRangeSettings.from_literal(
                     BoostedDecisionTreeDefaultParameters.PsNumberOfLeaves),
                 ps_minimum_leaf_instances=ParameterRangeSettings.from_literal(
                     BoostedDecisionTreeDefaultParameters.PsMinimumLeafInstances),
                 ps_learning_rate=ParameterRangeSettings.from_literal(
                     BoostedDecisionTreeDefaultParameters.PsLearningRate),
                 ps_num_trees=ParameterRangeSettings.from_literal(BoostedDecisionTreeDefaultParameters.PsNumTrees)
                 ):
        """Initialize a boosted decision tree

        :param mode: CreateLearnerMode
        :param number_of_leaves: int, the maximum number of leaves per tree, must be a positive integer. num_leaves
        :param minimum_leaf_instances: int, minimum number of training instances required to form a leaf.
               min_child_samples
        :param learning_rate: float, the learning rate, must be a positive double. learning_rate
        :param num_trees: int, total number of trees constructed, must be a positive integer. n_estimators
        :param random_number_seed: int, seed used to initialize the random number generator used by the trainer
        :param ps_number_of_leaves: ParameterRange, range of the maximum number of leaves per tree, num_leaves
        :param ps_minimum_leaf_instances: ParameterRange, range of minimum number of training instances required to
               form a leaf. min_child_samples
        :param ps_learning_rate: ParameterRange, range of the learning rate. learning_rate
        :param ps_num_trees: ParameterRange, range of total number of trees constructed. n_estimators
        """
        super().__init__()
        self.create_learner_mode = mode
        self.number_of_leaves = number_of_leaves
        self.minimum_leaf_instances = minimum_leaf_instances
        self.learning_rate = learning_rate
        self.num_trees = num_trees
        self.random_number_seed = random_number_seed

        self.parameter_range = {
            'num_leaves': Sweepable.from_prs("num_leaves", ps_number_of_leaves).attribute_value,
            'min_child_samples': Sweepable.from_prs("min_child_samples", ps_minimum_leaf_instances).attribute_value,
            'learning_rate': Sweepable.from_prs("learning_rate", ps_learning_rate).attribute_value,
            'n_estimators': Sweepable.from_prs("n_estimators", ps_num_trees).attribute_value,
        }

    @staticmethod
    def init(mode, number_of_leaves, ps_number_of_leaves, minimum_leaf_instances, ps_minimum_leaf_instances,
             learning_rate, ps_learning_rate, num_trees, ps_num_trees, random_number_seed, allow_unknown_levels):
        if mode == CreateLearnerMode.SingleParameter:
            setting = BoostDecisionTreeSetting.init_single(
                number_of_leaves=number_of_leaves,
                minimum_leaf_instances=minimum_leaf_instances,
                learning_rate=learning_rate,
                num_trees=num_trees,
                random_number_seed=random_number_seed)
        else:
            setting = BoostDecisionTreeSetting.init_range(
                ps_number_of_leaves=ps_number_of_leaves,
                ps_minimum_leaf_instances=ps_minimum_leaf_instances,
                ps_learning_rate=ps_learning_rate,
                ps_num_trees=ps_num_trees,
                random_number_seed=random_number_seed)
        return setting

    @staticmethod
    def init_single(
            number_of_leaves: int = BoostedDecisionTreeDefaultParameters.NumberOfLeaves,
            minimum_leaf_instances: int = BoostedDecisionTreeDefaultParameters.MinimumLeafInstances,
            learning_rate: float = BoostedDecisionTreeDefaultParameters.LearningRate,
            num_trees: int = BoostedDecisionTreeDefaultParameters.NumTrees,
            random_number_seed: int = BoostedDecisionTreeDefaultParameters.RandomNumberSeed
    ):
        return BoostDecisionTreeSetting(mode=CreateLearnerMode.SingleParameter, **locals())

    @staticmethod
    def init_range(ps_number_of_leaves: ParameterRangeSettings = None,
                   ps_minimum_leaf_instances: ParameterRangeSettings = None,
                   ps_learning_rate: ParameterRangeSettings = None,
                   ps_num_trees: ParameterRangeSettings = None,
                   random_number_seed: int = None):
        return BoostDecisionTreeSetting(mode=CreateLearnerMode.ParameterRange, **locals())
