import lightgbm
from lightgbm.basic import LightGBMError

from azureml.studio.common.error import ErrorMapping, ModuleOutOfMemoryError
from azureml.studio.common.parameter_range import ParameterRangeSettings
from azureml.studio.core.logger import time_profile, TimeProfile
from azureml.studio.internal.attributes.release_state import ReleaseState
from azureml.studio.modulehost.attributes import ModeParameter, FloatParameter, IntParameter, BooleanParameter, \
    ParameterRangeParameter, UntrainedLearnerOutputPort, ModuleMeta
from azureml.studio.modulehost.constants import FLOAT_MIN_POSITIVE, UINT32_MAX
from azureml.studio.modulehost.module_reflector import module_entry, BaseModule
from azureml.studio.modules.ml.common.base_learner import TaskType, CreateLearnerMode, RestoreInfo
from azureml.studio.modules.ml.common.supervised_learners import RegressionLearner
from azureml.studio.modules.ml.initialize_models.common_settings.boosted_decision_tree_setting import \
    BoostDecisionTreeSetting, BoostedDecisionTreeDefaultParameters, NUM_LEAVES_UPPER_BOUND


class BoostedDecisionTreeRegressionModule(BaseModule):

    @staticmethod
    @module_entry(ModuleMeta(
        name="Boosted Decision Tree Regression",
        description="Creates a regression model using the Boosted Decision Tree algorithm.",
        category="Machine Learning Algorithms/Regression",
        version="2.0",
        owner="Microsoft Corporation",
        family_id="0207D252-6C41-4C77-84C3-73BDF1AC5960",
        release_state=ReleaseState.Release,
        is_deterministic=True,
    ))
    def run(
            mode: ModeParameter(
                CreateLearnerMode,
                name="Create trainer mode",
                friendly_name="Create trainer mode",
                description="Create advanced learner options",
                default_value=BoostedDecisionTreeDefaultParameters.Mode,
            ),
            number_of_leaves: IntParameter(
                name="Maximum number of leaves per tree",
                friendly_name="Maximum number of leaves per tree",
                description="Specify the maximum number of leaves per tree",
                default_value=BoostedDecisionTreeDefaultParameters.NumberOfLeaves,
                parent_parameter="Create trainer mode",
                parent_parameter_val=(CreateLearnerMode.SingleParameter,),
                min_value=2,
                max_value=NUM_LEAVES_UPPER_BOUND,
            ),
            minimum_leaf_instances: IntParameter(
                name="Minimum number of training instances required to form a leaf",
                friendly_name="Minimum number of samples per leaf node",
                description="Specify the minimum number of cases required to form a leaf node",
                default_value=BoostedDecisionTreeDefaultParameters.MinimumLeafInstances,
                parent_parameter="Create trainer mode",
                parent_parameter_val=(CreateLearnerMode.SingleParameter,),
                min_value=1,
            ),
            learning_rate: FloatParameter(
                name="The learning rate",
                friendly_name="Learning rate",
                description="Specify the initial learning rate",
                default_value=BoostedDecisionTreeDefaultParameters.LearningRate,
                parent_parameter="Create trainer mode",
                parent_parameter_val=(CreateLearnerMode.SingleParameter,),
                min_value=FLOAT_MIN_POSITIVE,
                max_value=1,
            ),
            num_trees: IntParameter(
                name="Total number of trees constructed",
                friendly_name="Total number of trees constructed",
                description="Specify the maximum number of trees that can be created during training",
                default_value=BoostedDecisionTreeDefaultParameters.NumTrees,
                parent_parameter="Create trainer mode",
                parent_parameter_val=(CreateLearnerMode.SingleParameter,),
                min_value=1,
            ),
            ps_number_of_leaves: ParameterRangeParameter(
                name="Range for maximum number of leaves per tree",
                friendly_name="Maximum number of leaves per tree",
                description="Specify range for the maximum number of leaves allowed per tree",
                default_value=BoostedDecisionTreeDefaultParameters.PsNumberOfLeaves,
                parent_parameter="Create trainer mode",
                parent_parameter_val=(CreateLearnerMode.ParameterRange,),
                min_limit=2,
                max_limit=NUM_LEAVES_UPPER_BOUND,
                is_int=True,
                is_log=True,
                slider_min=1,
                slider_max=1000,
            ),
            ps_minimum_leaf_instances: ParameterRangeParameter(
                name="Range for minimum number of training instances required to form a leaf",
                friendly_name="Minimum number of samples per leaf node",
                description="Specify the range for the minimum number of cases required to form a leaf",
                default_value=BoostedDecisionTreeDefaultParameters.PsMinimumLeafInstances,
                parent_parameter="Create trainer mode",
                parent_parameter_val=(CreateLearnerMode.ParameterRange,),
                min_limit=1,
                max_limit=2147483647,
                is_int=True,
                is_log=True,
                slider_min=1,
                slider_max=1000,
            ),
            ps_learning_rate: ParameterRangeParameter(
                name="Range for learning rate",
                friendly_name="Learning rate",
                description="Specify the range for the initial learning rate",
                default_value=BoostedDecisionTreeDefaultParameters.PsLearningRate,
                parent_parameter="Create trainer mode",
                parent_parameter_val=(CreateLearnerMode.ParameterRange,),
                min_limit=FLOAT_MIN_POSITIVE,
                max_limit=1,
                is_int=False,
                is_log=True,
                slider_min=1E-06,
                slider_max=1,
            ),
            ps_num_trees: ParameterRangeParameter(
                name="Range for total number of trees constructed",
                friendly_name="Total number of trees constructed",
                description="Specify the range for the maximum number of trees that can be created during training",
                default_value=BoostedDecisionTreeDefaultParameters.PsNumTrees,
                parent_parameter="Create trainer mode",
                parent_parameter_val=(CreateLearnerMode.ParameterRange,),
                min_limit=1,
                max_limit=2147483647,
                is_int=True,
                is_log=True,
                slider_min=1,
                slider_max=10000,
            ),
            random_number_seed: IntParameter(
                name="Random number seed",
                friendly_name="Random number seed",
                min_value=0,
                max_value=UINT32_MAX,
                is_optional=True,
                description="Provide a seed for the random number generator used by the model. "
                            "Leave blank for default.",
            ),
            allow_unknown_levels: BooleanParameter(
                name="Allow unknown levels in categorical features",
                friendly_name="Allow unknown categorical levels",
                description="If true, create an additional level for each categorical column. "
                            "Levels in the test dataset not available in the training dataset "
                            "are mapped to this additional level.",
                default_value=BoostedDecisionTreeDefaultParameters.AllowUnknownLevels,
                release_state=ReleaseState.Alpha
            )
    ) -> (
            UntrainedLearnerOutputPort(
                name="Untrained model",
                friendly_name="Untrained model",
                description="An untrained regression model that can be connected to "
                            "the Train Generic Model or Cross Validate Model modules",
            ),
    ):
        input_values = locals()
        output_values = BoostedDecisionTreeRegressionModule.create_boosted_decision_tree_regression(**input_values)
        return output_values

    @staticmethod
    def create_boosted_decision_tree_regression(
            mode: CreateLearnerMode = BoostedDecisionTreeDefaultParameters.Mode,
            number_of_leaves: int = BoostedDecisionTreeDefaultParameters.NumberOfLeaves,
            ps_number_of_leaves: ParameterRangeSettings =
            BoostedDecisionTreeDefaultParameters.PsNumberOfLeaves,
            minimum_leaf_instances: int = BoostedDecisionTreeDefaultParameters.MinimumLeafInstances,
            ps_minimum_leaf_instances: ParameterRangeSettings =
            BoostedDecisionTreeDefaultParameters.PsMinimumLeafInstances,
            learning_rate: float = BoostedDecisionTreeDefaultParameters.LearningRate,
            ps_learning_rate: ParameterRangeSettings =
            BoostedDecisionTreeDefaultParameters.PsLearningRate,
            num_trees: int = BoostedDecisionTreeDefaultParameters.NumTrees,
            ps_num_trees: ParameterRangeSettings = BoostedDecisionTreeDefaultParameters.PsNumTrees,
            random_number_seed: int = BoostedDecisionTreeDefaultParameters.RandomNumberSeed,
            allow_unknown_levels: bool = BoostedDecisionTreeDefaultParameters.AllowUnknownLevels,
    ):
        setting = BoostDecisionTreeSetting.init(**locals())
        return tuple([BoostDecisionTreeRegressor(setting)])


class BoostDecisionTreeRegressorSetting(BoostDecisionTreeSetting):
    # Compatible with old models
    pass


class BoostDecisionTreeRegressor(RegressionLearner):
    def __init__(self, setting: BoostDecisionTreeSetting):
        super().__init__(setting=setting, task_type=TaskType.Regression)

    @property
    def parameter_mapping(self):
        return {
            'num_leaves': RestoreInfo(BoostedDecisionTreeRegressionModule._args.number_of_leaves.friendly_name),
            'min_child_samples': RestoreInfo(
                BoostedDecisionTreeRegressionModule._args.minimum_leaf_instances.friendly_name),
            'learning_rate': RestoreInfo(BoostedDecisionTreeRegressionModule._args.learning_rate.friendly_name),
            'n_estimators': RestoreInfo(BoostedDecisionTreeRegressionModule._args.num_trees.friendly_name)
        }

    @time_profile
    def _train(self, train_x, train_y):
        # Fix bug 640458: LightGBM requires at least 2 samples to train the model
        ErrorMapping.verify_number_of_rows_greater_than_or_equal_to(curr_row_count=len(train_y),
                                                                    required_row_count=2,
                                                                    arg_name="Dataset")
        # train model
        with TimeProfile("Training Model"):
            try:
                self.model.fit(train_x, train_y)
            except LightGBMError as e:
                # When LGBMClassifier runs out of memory, a cpp error(std::bad_alloc) would be thrown.
                # So here a patch is added to catch it and rethrow it as ModuleOutOfMemoryError
                if "std::bad_alloc" in str(e.args):
                    ErrorMapping.rethrow(e, ModuleOutOfMemoryError(
                        "Cannot allocate more memory. Please check if the hyper-parameters are not appropriate."))
                raise e
        self._is_trained = True

    def init_model(self):
        self.model = lightgbm.LGBMRegressor(
            # set maximum tree depth to no limit
            max_depth=-1,
            num_leaves=self.setting.number_of_leaves,
            min_child_samples=self.setting.minimum_leaf_instances,
            n_estimators=self.setting.num_trees,
            learning_rate=self.setting.learning_rate,
            random_state=self.setting.random_number_seed,
            subsample=0.6,  # use sub sample lead to reduction of variance and an increase in bias.
            colsample_bytree=0.6,
            verbosity=1,
            n_jobs=-1,
        )
