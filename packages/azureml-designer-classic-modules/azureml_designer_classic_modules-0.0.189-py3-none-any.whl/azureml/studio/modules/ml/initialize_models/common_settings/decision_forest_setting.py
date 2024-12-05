from azureml.studio.common.parameter_range import ParameterRangeSettings, Sweepable
from azureml.studio.common.types import AutoEnum
from azureml.studio.modulehost.attributes import ItemInfo
from azureml.studio.modules.ml.common.base_learner import CreateLearnerMode
from azureml.studio.modules.ml.common.base_learner_setting import BaseLearnerSetting


class ResamplingMethod(AutoEnum):
    Bagging: ItemInfo(name='Bagging Resampling', friendly_name="Bagging Resampling") = ()
    Replicate: ItemInfo(name="Replicate Resampling", friendly_name="Replicate Resampling") = ()


class DecisionForestDefaultParameters:
    Mode = CreateLearnerMode.SingleParameter
    ResamplingMethod = ResamplingMethod.Bagging
    TreeCount = 8
    MaxDepth = 32
    RandomSplitCount = 128
    MinLeafSampleCount = 1
    PsTreeCount = "1; 8; 32"
    PsMaxDepth = "1; 16; 64"
    PsRandomSplitCount = "1; 128; 1024"
    PsMinLeafSampleCount = "1; 4; 16"
    AllowUnknownLevels = True

    @classmethod
    def to_dict(cls):
        return {
            "mode": cls.Mode,
            "resampling_method": cls.ResamplingMethod,
            "tree_count": cls.TreeCount,
            "max_depth": cls.MaxDepth,
            "random_split_count": cls.RandomSplitCount,
            "min_leaf_sample_count": cls.MinLeafSampleCount,
            "ps_tree_count": ParameterRangeSettings.from_literal(cls.PsTreeCount),
            "ps_max_depth": ParameterRangeSettings.from_literal(cls.PsMaxDepth),
            "ps_random_split_count": ParameterRangeSettings.from_literal(cls.PsRandomSplitCount),
            "ps_min_leaf_sample_count": ParameterRangeSettings.from_literal(cls.PsMinLeafSampleCount),
            "allow_unknown_levels": cls.AllowUnknownLevels,
        }


class DecisionForestSetting(BaseLearnerSetting):
    """ DecisionForest Setting

        remaining problems:
        1. Decision Forest is a gemini model, not TLC model, only be used in inter-microsoft.
           There, we use Random Forest Algorithm instead.
            And may use nimbusML.decision forest in the future.
        2. max_features should be in (0, n_features)
    """

    def __init__(self,
                 create_learner_mode=DecisionForestDefaultParameters.Mode,
                 resampling_method=DecisionForestDefaultParameters.ResamplingMethod,
                 tree_count=DecisionForestDefaultParameters.TreeCount,
                 max_depth=DecisionForestDefaultParameters.MaxDepth,
                 random_split_count=DecisionForestDefaultParameters.RandomSplitCount,
                 min_leaf_sample_count=DecisionForestDefaultParameters.MinLeafSampleCount,
                 ps_tree_count=ParameterRangeSettings.from_literal(DecisionForestDefaultParameters.PsTreeCount),
                 ps_max_depth=ParameterRangeSettings.from_literal(DecisionForestDefaultParameters.PsMaxDepth),
                 ps_random_split_count=ParameterRangeSettings.from_literal(
                     DecisionForestDefaultParameters.PsRandomSplitCount),
                 ps_min_leaf_sample_count=ParameterRangeSettings.from_literal(
                     DecisionForestDefaultParameters.PsMinLeafSampleCount)
                 ):
        """ Initialize DecisionForestSetting

        :param resampling_method: resamplingMethod.  bootstrap: bagging is mapped to True, and replicate to False.
        :param tree_count: int, the number of decision trees to create. n_estimators
        :param max_depth: int, the maximum depth of any decision tree that can be created. max_depth
        :param random_split_count: int, the number of splits generated per node. not supported yet
        :param min_leaf_sample_count: int, the minimum number of training samples require. min_samples_leaf
        :param ps_tree_count, ParameterRange, range of the minimum number of training samples required. n_estimators
        :param ps_max_depth, ParameterRange, range of the maximum depth. max_depth
        :param ps_random_split_count, ParameterRange, range of the number of splits generated per node. not supported
        :param ps_min_leaf_sample_count, ParameterRange, range of the minimum number of training samples required.
               min_sample_leaf
        """
        super().__init__()
        self.create_learner_mode = create_learner_mode
        self.resampling_method = resampling_method
        self.tree_count = tree_count
        self.max_depth = max_depth
        self.random_split_count = random_split_count
        self.min_leaf_sample_count = min_leaf_sample_count
        self.parameter_range = {
            'n_estimators': Sweepable.from_prs(
                "n_estimators", ps_tree_count).attribute_value,
            'max_depth': Sweepable.from_prs(
                "max_depth", ps_max_depth).attribute_value,
            # 'max_features': Sweepable.from_prs("max_features", ps_random_split_count).attribute_value,
            'min_samples_leaf': Sweepable.from_prs(
                "min_samples_leaf", ps_min_leaf_sample_count).attribute_value,
        }

    @staticmethod
    def init(mode, resampling_method, tree_count, ps_tree_count, max_depth, ps_max_depth, random_split_count,
             ps_random_split_count, min_leaf_sample_count, ps_min_leaf_sample_count, allow_unknown_levels,
             ):
        if mode == CreateLearnerMode.SingleParameter:
            setting = DecisionForestSetting.init_single(
                resampling_method=resampling_method,
                tree_count=tree_count,
                max_depth=max_depth,
                random_split_count=random_split_count,
                min_leaf_sample_count=min_leaf_sample_count
            )
        else:
            setting = DecisionForestSetting.init_range(
                resampling_method=resampling_method,
                ps_tree_count=ps_tree_count, ps_max_depth=ps_max_depth,
                ps_random_split_count=ps_random_split_count,
                ps_min_leaf_sample_count=ps_min_leaf_sample_count)
        return setting

    @staticmethod
    def init_single(
            resampling_method: ResamplingMethod = DecisionForestDefaultParameters.ResamplingMethod,
            tree_count: int = DecisionForestDefaultParameters.TreeCount,
            max_depth: int = DecisionForestDefaultParameters.MaxDepth,
            random_split_count: int = DecisionForestDefaultParameters.RandomSplitCount,
            min_leaf_sample_count: int = DecisionForestDefaultParameters.MinLeafSampleCount
    ):
        return DecisionForestSetting(create_learner_mode=CreateLearnerMode.SingleParameter, **locals())

    @staticmethod
    def init_range(resampling_method: ResamplingMethod = ResamplingMethod.Bagging,
                   ps_tree_count: ParameterRangeSettings = None,
                   ps_max_depth: ParameterRangeSettings = None, ps_random_split_count: ParameterRangeSettings = None,
                   ps_min_leaf_sample_count: ParameterRangeSettings = 1):
        return DecisionForestSetting(create_learner_mode=CreateLearnerMode.ParameterRange, **locals())
