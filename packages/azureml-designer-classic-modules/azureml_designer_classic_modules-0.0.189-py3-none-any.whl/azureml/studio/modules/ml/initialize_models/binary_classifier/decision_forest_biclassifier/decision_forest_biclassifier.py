from sklearn.ensemble import RandomForestClassifier

from azureml.studio.common.parameter_range import ParameterRangeSettings
from azureml.studio.internal.attributes.release_state import ReleaseState
from azureml.studio.modulehost.attributes import ModeParameter, IntParameter, \
    ParameterRangeParameter, UntrainedLearnerOutputPort, ModuleMeta, BooleanParameter
from azureml.studio.modulehost.module_reflector import module_entry, BaseModule
from azureml.studio.modules.ml.common.base_learner import TaskType, CreateLearnerMode, RestoreInfo
from azureml.studio.modules.ml.common.supervised_learners import BinaryClassificationLearner
from azureml.studio.modules.ml.initialize_models.common_settings.decision_forest_setting import \
    DecisionForestDefaultParameters, ResamplingMethod, DecisionForestSetting


class TwoClassDecisionForestModule(BaseModule):

    @staticmethod
    @module_entry(ModuleMeta(
        name="Two-Class Decision Forest",
        description="Creates a two-class classification model using the decision forest algorithm.",
        category="Machine Learning Algorithms/Classification",
        version="2.0",
        owner="Microsoft Corporation",
        family_id="5A7D5466-9928-40C8-A19C-D5DE4882C77E",
        release_state=ReleaseState.Release,
        is_deterministic=True,
    ))
    def run(
            mode: ModeParameter(
                CreateLearnerMode,
                name="Create trainer mode",
                friendly_name="Create trainer mode",
                description="Create advanced learner options",
                default_value=DecisionForestDefaultParameters.Mode,
            ),
            resampling_method: ModeParameter(
                ResamplingMethod,
                name="Resampling method",
                friendly_name="Resampling method",
                description="Choose a resampling method",
                default_value=DecisionForestDefaultParameters.ResamplingMethod,
            ),
            tree_count: IntParameter(
                name="Number of decision trees",
                friendly_name="Number of decision trees",
                description="Specify the number of decision trees to create in the ensemble",
                default_value=DecisionForestDefaultParameters.TreeCount,
                parent_parameter="Create trainer mode",
                parent_parameter_val=(CreateLearnerMode.SingleParameter,),
                min_value=1,
            ),
            max_depth: IntParameter(
                name="Maximum depth of the decision trees",
                friendly_name="Maximum depth of the decision trees",
                description="Specify the maximum depth of any decision tree that can be created in the ensemble",
                default_value=DecisionForestDefaultParameters.MaxDepth,
                parent_parameter="Create trainer mode",
                parent_parameter_val=(CreateLearnerMode.SingleParameter,),
                min_value=1,
            ),
            random_split_count: IntParameter(
                name="Number of random splits per node",
                friendly_name="Number of random splits per node",
                description="Specify the number of splits generated per node, from which the optimal split is selected",
                default_value=DecisionForestDefaultParameters.RandomSplitCount,
                parent_parameter="Create trainer mode",
                parent_parameter_val=(CreateLearnerMode.SingleParameter,),
                min_value=1,
                release_state=ReleaseState.Alpha
            ),
            min_leaf_sample_count: IntParameter(
                name="Minimum number of samples per leaf node",
                friendly_name="Minimum number of samples per leaf node",
                description="Specify the minimum number of training samples required to generate a leaf node",
                default_value=DecisionForestDefaultParameters.MinLeafSampleCount,
                parent_parameter="Create trainer mode",
                parent_parameter_val=(CreateLearnerMode.SingleParameter,),
                min_value=1,
            ),
            ps_tree_count: ParameterRangeParameter(
                name="Range for number of decision trees",
                friendly_name="Number of decision trees",
                description="Specify range for the number of decision trees to create in the ensemble",
                default_value=DecisionForestDefaultParameters.PsTreeCount,
                parent_parameter="Create trainer mode",
                parent_parameter_val=(CreateLearnerMode.ParameterRange,),
                min_limit=1,
                max_limit=2147483647,
                is_int=True,
                is_log=True,
                slider_min=1,
                slider_max=1024,
            ),
            ps_max_depth: ParameterRangeParameter(
                name="Range for the maximum depth of the decision trees",
                friendly_name="Maximum depth of the decision trees",
                description="Specify range for the maximum depth of the decision trees",
                default_value=DecisionForestDefaultParameters.PsMaxDepth,
                parent_parameter="Create trainer mode",
                parent_parameter_val=(CreateLearnerMode.ParameterRange,),
                min_limit=1,
                max_limit=2147483647,
                is_int=True,
                is_log=True,
                slider_min=1,
                slider_max=1024,
            ),
            ps_random_split_count: ParameterRangeParameter(
                name="Range for the number of random splits per node",
                friendly_name="Number of random splits per node",
                description="Specify range for the number of random splits per node",
                default_value=DecisionForestDefaultParameters.PsRandomSplitCount,
                parent_parameter="Create trainer mode",
                parent_parameter_val=(CreateLearnerMode.ParameterRange,),
                min_limit=1,
                max_limit=2147483647,
                is_int=True,
                is_log=True,
                slider_min=1,
                slider_max=8196,
                release_state=ReleaseState.Alpha
            ),
            ps_min_leaf_sample_count: ParameterRangeParameter(
                name="Range for the minimum number of samples per leaf node",
                friendly_name="Minimum number of samples per leaf node",
                description="Specify range for the minimum number of samples per leaf node",
                default_value=DecisionForestDefaultParameters.PsMinLeafSampleCount,
                parent_parameter="Create trainer mode",
                parent_parameter_val=(CreateLearnerMode.ParameterRange,),
                min_limit=1,
                max_limit=2147483647,
                is_int=True,
                is_log=True,
                slider_min=1,
                slider_max=64,
            ),
            allow_unknown_levels: BooleanParameter(
                name="Allow unknown values for categorical features",
                friendly_name="Allow unknown values for categorical features",
                description="Indicate whether unknown values of existing categorical features "
                            "can be mapped to a new, additional feature",
                default_value=DecisionForestDefaultParameters.AllowUnknownLevels,
                release_state=ReleaseState.Alpha
            )
    ) -> (
            UntrainedLearnerOutputPort(
                name="Untrained model",
                friendly_name="Untrained model",
                description="An untrained binary classification model",
            ),
    ):
        input_values = locals()
        output_values = TwoClassDecisionForestModule.create_decision_forest_biclassifier(**input_values)
        return output_values

    @staticmethod
    def create_decision_forest_biclassifier(
            mode: CreateLearnerMode = DecisionForestDefaultParameters.Mode,
            resampling_method: ResamplingMethod = DecisionForestDefaultParameters.ResamplingMethod,
            tree_count: int = DecisionForestDefaultParameters.TreeCount,
            ps_tree_count: ParameterRangeSettings = DecisionForestDefaultParameters.PsTreeCount,
            max_depth: int = DecisionForestDefaultParameters.MaxDepth,
            ps_max_depth: ParameterRangeSettings = DecisionForestDefaultParameters.PsMaxDepth,
            random_split_count: int = DecisionForestDefaultParameters.RandomSplitCount,
            ps_random_split_count: ParameterRangeSettings =
            DecisionForestDefaultParameters.PsRandomSplitCount,
            min_leaf_sample_count: int = DecisionForestDefaultParameters.MinLeafSampleCount,
            ps_min_leaf_sample_count: ParameterRangeSettings =
            DecisionForestDefaultParameters.PsMinLeafSampleCount,
            allow_unknown_levels: bool = DecisionForestDefaultParameters.AllowUnknownLevels,
    ):
        setting = DecisionForestSetting.init(**locals())
        return tuple([DecisionForestBiClassifier(setting)])


class DecisionForestBiClassifierSetting(DecisionForestSetting):
    # Compatible with old models
    pass


class DecisionForestBiClassifier(BinaryClassificationLearner):
    def __init__(self, setting: DecisionForestSetting):
        super().__init__(setting=setting, task_type=TaskType.BinaryClassification)

    @property
    def parameter_mapping(self):
        return {
            'n_estimators': RestoreInfo(TwoClassDecisionForestModule._args.tree_count.friendly_name),
            'max_depth': RestoreInfo(TwoClassDecisionForestModule._args.max_depth.friendly_name),
            'min_samples_leaf': RestoreInfo(TwoClassDecisionForestModule._args.min_leaf_sample_count.friendly_name)
        }

    def init_model(self):
        # Parameter 'random_split_count' is used in the V1 internal algo to specify the number of splits generated
        # per node, from which the optimal split is selected. However, it is not used in 'RandomForestClassifier'
        # to find the best split.
        # See https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html.
        self.model = RandomForestClassifier(
            bootstrap=(self.setting.resampling_method == ResamplingMethod.Bagging),
            n_estimators=self.setting.tree_count,
            max_depth=self.setting.max_depth,
            min_samples_leaf=self.setting.min_leaf_sample_count,
            random_state=self.setting.random_number_seed,
            n_jobs=-1,
            verbose=51
        )
