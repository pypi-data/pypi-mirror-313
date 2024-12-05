import pandas as pd
import numpy as np
import azureml.studio.core.utils.strutils as strutils
from sklearn.ensemble import RandomForestRegressor
from azureml.studio.common.error import ParameterParsingError, ErrorMapping
from azureml.studio.common.parameter_range import ParameterRangeSettings
from azureml.studio.core.logger import module_logger
from azureml.studio.core.logger import TimeProfile
from azureml.studio.core.utils.strutils import profile_column_names
from azureml.studio.internal.attributes.release_state import ReleaseState
from azureml.studio.modulehost.attributes import ModeParameter, FloatParameter, IntParameter, BooleanParameter, \
    StringParameter, ParameterRangeParameter, UntrainedLearnerOutputPort, ModuleMeta
from azureml.studio.modulehost.constants import UINT32_MAX
from azureml.studio.modulehost.module_reflector import module_entry, BaseModule
from azureml.studio.modules.ml.common.base_learner import TaskType, CreateLearnerMode, RestoreInfo
from azureml.studio.modules.ml.common.base_learner_setting import BaseLearnerSetting
from azureml.studio.modules.ml.common.constants import ScoreColumnConstants
from azureml.studio.modules.ml.common.supervised_learners import RegressionLearner
from azureml.studio.modules.ml.common.ml_utils import filter_column_names_with_prefix


def _parse_float_list(arg_name, arg_val):
    # here we accept both comma-separated and semicolon-separated string to parameter quantile_value_list
    arg_val = arg_val.replace(';', ',')
    float_list = strutils.float_str_to_float_list(arg_val)
    if float_list is None:
        ErrorMapping.throw(ParameterParsingError(arg_name_or_column=arg_name, to_type='float list'))
    # quantile value is between (0, 1), illegal value will be ignored as in V1
    float_list = [f for f in float_list if 0 < f < 1]
    # it will raise ParameterParsingError if all quantile values are not in desired range
    if len(float_list) == 0:
        ErrorMapping.throw(ParameterParsingError(arg_name_or_column=arg_name, to_type='float list'))
    return float_list


class DefaultParameters:
    Mode = CreateLearnerMode.SingleParameter
    NumTrees = 100
    NumLeaves = 20
    MinimumInstanceInLeaf = 10
    BaggingFraction = 0.7
    FeatureFraction = 0.7
    SplitFraction = 0.7
    QuantileSampleCount = 100
    QuantileValueList = "0.25; 0.5; 0.75"
    RandomNumberSeed = 42
    AllowUnknownLevels = True
    PsNumLeaves = "16; 32; 64"
    PsNumTrees = "16; 32; 64"
    PsMinimumInstanceInLeaf = "1; 5; 10"
    PsBaggingFraction = "0.25; 0.5; 0.75"
    PsFeatureFraction = "0.25; 0.5; 0.75"
    PsSplitFraction = "0.25; 0.5; 0.75"
    PsQuantileValueList = "0.25; 0.5; 0.75"


class FastForestQuantileRegressionModule(BaseModule):
    @staticmethod
    @module_entry(
        ModuleMeta(
            name="Fast Forest Quantile Regression",
            description="Creates a quantile regression model",
            category="Machine Learning Algorithms/Regression",
            version="1.0",
            owner="Microsoft Corporation",
            family_id="B9064DC3-2D69-4E06-B307-6CEBF324686A",
            release_state=ReleaseState.Release,
            is_deterministic=True,
        )
    )
    def run(
            mode: ModeParameter(
                CreateLearnerMode,
                name="Create trainer mode",
                friendly_name="Create trainer mode",
                description="Create advanced learner options",
                default_value=DefaultParameters.Mode,
            ),
            num_trees: IntParameter(
                name="Number of Trees",
                friendly_name="Number of Trees",
                description="Specifies the number of trees to be constructed",
                default_value=DefaultParameters.NumTrees,
                parent_parameter="Create trainer mode",
                parent_parameter_val=(CreateLearnerMode.SingleParameter,),
            ),
            num_leaves: IntParameter(
                name="Number of Leaves",
                friendly_name="Number of Leaves",
                description="Specifies the maximum number of leaves per tree. The default number is 20",
                default_value=DefaultParameters.NumLeaves,
                parent_parameter="Create trainer mode",
                parent_parameter_val=(CreateLearnerMode.SingleParameter,),
                # max_leaf_nodes must be larger than 1, required by sklearn.
                min_value=2,
            ),
            minimum_instance_in_leaf: IntParameter(
                name="Minimum number of training instances required to form a leaf",
                friendly_name="Minimum number of training instances required to form a leaf",
                description="Indicates the minimum number of training instances requried to form a leaf",
                default_value=DefaultParameters.MinimumInstanceInLeaf,
                parent_parameter="Create trainer mode",
                parent_parameter_val=(CreateLearnerMode.SingleParameter,),
            ),
            bagging_fraction: FloatParameter(
                name="Bagging fraction",
                friendly_name="Bagging fraction",
                description="Specifies the fraction of training data to use for each tree",
                default_value=DefaultParameters.BaggingFraction,
                parent_parameter="Create trainer mode",
                parent_parameter_val=(CreateLearnerMode.SingleParameter,),
            ),
            feature_fraction: FloatParameter(
                name="Feature fraction",
                friendly_name="Feature fraction",
                description="Specifies the fraction of features (chosen randomly) to use for each tree",
                default_value=DefaultParameters.FeatureFraction,
                parent_parameter="Create trainer mode",
                parent_parameter_val=(CreateLearnerMode.SingleParameter,),
                release_state=ReleaseState.Alpha,
            ),
            split_fraction: FloatParameter(
                name="Split fraction",
                friendly_name="Split fraction",
                description="Specifies the fraction of features (chosen randomly) to use for each split",
                default_value=DefaultParameters.SplitFraction,
                parent_parameter="Create trainer mode",
                parent_parameter_val=(CreateLearnerMode.SingleParameter,),
            ),
            quantile_sample_count: IntParameter(
                name="Quantile sample count",
                friendly_name="Quantile sample count",
                description="Specifies number of instances used in each node to estimate quantiles",
                default_value=DefaultParameters.QuantileSampleCount,
                parent_parameter="Create trainer mode",
                parent_parameter_val=(CreateLearnerMode.SingleParameter,),
                release_state=ReleaseState.Alpha,
            ),
            quantile_value_list: StringParameter(
                name="Quantiles to be estimated",
                friendly_name="Quantiles to be estimated",
                description="Specifies the quantile to be estimated",
                default_value=DefaultParameters.QuantileValueList,
                parent_parameter="Create trainer mode",
                parent_parameter_val=(CreateLearnerMode.SingleParameter,),
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
                default_value=DefaultParameters.AllowUnknownLevels,
                release_state=ReleaseState.Alpha,
            ),
            ps_num_trees: ParameterRangeParameter(
                name="Range for total number of trees constructed",
                friendly_name="Number of Trees",
                description="Specify the range for the maximum number of trees that can be created during training",
                default_value=DefaultParameters.PsNumTrees,
                parent_parameter="Create trainer mode",
                parent_parameter_val=(CreateLearnerMode.ParameterRange,),
                min_limit=1,
                max_limit=256,
                is_int=True,
                is_log=True,
                slider_min=16,
                slider_max=256,
            ),
            ps_num_leaves: ParameterRangeParameter(
                name="Range for maximum number of leaves per tree",
                friendly_name="Number of Leaves",
                description="Specify range for the maximum number of leaves allowed per tree",
                default_value=DefaultParameters.PsNumLeaves,
                parent_parameter="Create trainer mode",
                parent_parameter_val=(CreateLearnerMode.ParameterRange,),
                min_limit=16,
                max_limit=128,
                is_int=True,
                is_log=True,
                slider_min=16,
                slider_max=128,
            ),
            ps_minimum_instance_in_leaf: ParameterRangeParameter(
                name="Range for minimum number of training instances required to form a leaf",
                friendly_name="Minimum number of training instances required to form a leaf",
                description="Specify the range for the minimum number of cases required to form a leaf",
                default_value=DefaultParameters.PsMinimumInstanceInLeaf,
                parent_parameter="Create trainer mode",
                parent_parameter_val=(CreateLearnerMode.ParameterRange,),
                min_limit=1,
                max_limit=10,
                is_int=True,
                is_log=False,
                slider_min=1,
                slider_max=10,
            ),
            ps_bagging_fraction: ParameterRangeParameter(
                name="Range for bagging fraction",
                friendly_name="Bagging fraction",
                description="Specifies the range for fraction of training data to use for each tree",
                default_value=DefaultParameters.PsBaggingFraction,
                parent_parameter="Create trainer mode",
                parent_parameter_val=(CreateLearnerMode.ParameterRange,),
                min_limit=0.25,
                max_limit=1,
                is_int=False,
                is_log=False,
                slider_min=0.01,
                slider_max=1,
            ),
            ps_feature_fraction: ParameterRangeParameter(
                name="Range for feature fraction",
                friendly_name="Feature fraction",
                description="Specifies the range for fraction of features (chosen randomly) to use for each tree",
                default_value=DefaultParameters.PsFeatureFraction,
                parent_parameter="Create trainer mode",
                parent_parameter_val=(CreateLearnerMode.ParameterRange,),
                min_limit=0.25,
                max_limit=1,
                is_int=False,
                is_log=False,
                slider_min=0.01,
                slider_max=1,
                release_state=ReleaseState.Alpha,
            ),
            ps_split_fraction: ParameterRangeParameter(
                name="Range for split fraction",
                friendly_name="Split fraction",
                description="Specifies the range for fraction of features (chosen randomly) to use for each split",
                default_value=DefaultParameters.PsSplitFraction,
                parent_parameter="Create trainer mode",
                parent_parameter_val=(CreateLearnerMode.ParameterRange,),
                min_limit=0.25,
                max_limit=1,
                is_int=False,
                is_log=False,
                slider_min=0.01,
                slider_max=1,
            ),
            ps_quantile_value_list: StringParameter(
                name="Required quantile values",
                friendly_name="Quantiles to be estimated",
                description="Required quantile value used during parameter sweep",
                default_value=DefaultParameters.PsQuantileValueList,
                parent_parameter="Create trainer mode",
                parent_parameter_val=(CreateLearnerMode.ParameterRange,),
            )
    ) -> (
            UntrainedLearnerOutputPort(
                name="Untrained model",
                friendly_name="Untrained model",
                description="An untrained quantile regression model that can be connected "
                            "to the Train Generic Model or Cross Validate Model modules.",
            ),
    ):
        setting = FastForestQuantileRegressorSetting.init(**locals())
        return tuple([FastForestQuantileRegressor(setting)])


class FastForestQuantileRegressorSetting(BaseLearnerSetting):
    """ Fast Forest Quantile Regression

        there remains two problems:
        1. feature fraction is not supported by sklearn.ensemble.RandomForestRegressor
        2. quantile sample count is not supported by sklearn.ensemble.RandomForestRegressor
    """

    def __init__(self, mode: DefaultParameters.Mode,
                 num_trees: int = DefaultParameters.NumTrees,
                 num_leaves: int = DefaultParameters.NumLeaves,
                 minimum_instance_in_leaf: int = DefaultParameters.MinimumInstanceInLeaf,
                 bagging_fraction: float = DefaultParameters.BaggingFraction,
                 feature_fraction: float = DefaultParameters.FeatureFraction,
                 split_fraction: float = DefaultParameters.SplitFraction,
                 quantile_sample_count: int = DefaultParameters.QuantileSampleCount,
                 quantile_value_list: list = DefaultParameters.QuantileValueList,
                 random_number_seed: int = DefaultParameters.RandomNumberSeed,
                 ps_num_leaves=ParameterRangeSettings.from_literal(DefaultParameters.PsNumLeaves),
                 ps_num_trees=ParameterRangeSettings.from_literal(DefaultParameters.PsNumTrees),
                 ps_minimum_instance_in_leaf=ParameterRangeSettings.from_literal(
                     DefaultParameters.PsMinimumInstanceInLeaf),
                 ps_bagging_fraction=ParameterRangeSettings.from_literal(DefaultParameters.PsBaggingFraction),
                 ps_feature_fraction=ParameterRangeSettings.from_literal(DefaultParameters.PsFeatureFraction),
                 ps_split_fraction=ParameterRangeSettings.from_literal(DefaultParameters.PsSplitFraction),
                 ):
        """
        :param num_trees: int, specifies number of trees to be constructed
        :param num_leaves: int, specifies the maximum number of leaves per tree
        :param minimum_instance_in_leaf: int, indicates the minimum number of training instances requried to form a leaf
        :param bagging_fraction: float, specifies the fraction of training data to use for each tree
        :param feature_fraction: float, specifies the fraction of features (chosen randomly) to use for each tree
        :param split_fraction: float, specifies the fraction of features (chosen randomly) to use for each split
        :param quantile_sample_count: int, specifies number of instances used in each node to estimate quantiles
        :param quantile_value_list: list(int),  specifies the quantile to be estimated
        :param random_number_seed: int, provides a seed for the random number generator used by the model.

        """
        super().__init__()
        name_mapping = {
            'n_estimators': ps_num_trees,
            'max_leaf_nodes': ps_num_leaves,
            'min_samples_leaf': ps_minimum_instance_in_leaf,
            'max_features': ps_split_fraction,
            'max_samples': ps_bagging_fraction,
        }
        self.create_learner_mode = mode
        self.num_trees = num_trees
        self.num_leaves = num_leaves
        self.minimum_instance_in_leaf = minimum_instance_in_leaf
        self.bagging_fraction = bagging_fraction
        self.feature_fraction = feature_fraction  # TODO : sklearn had not supported it yet
        self.quantile_sample_count = quantile_sample_count  # TODO : sklearn had not supported it yet
        self.split_fraction = split_fraction
        self.quantile_value_list = quantile_value_list
        self.random_number_seed = random_number_seed
        self.parameter_range = {
            name: self.get_sweepable(name, literal_value) for name, literal_value in name_mapping.items()}

    @staticmethod
    def init(mode, num_trees, num_leaves, minimum_instance_in_leaf, bagging_fraction, feature_fraction, split_fraction,
             quantile_sample_count, quantile_value_list, random_number_seed, allow_unknown_levels, ps_num_leaves,
             ps_num_trees, ps_minimum_instance_in_leaf, ps_bagging_fraction, ps_feature_fraction, ps_split_fraction,
             ps_quantile_value_list
             ):
        if mode == CreateLearnerMode.SingleParameter:
            quantile_value_list = _parse_float_list("quantile_value_list", quantile_value_list)
            setting = FastForestQuantileRegressorSetting.init_single(
                num_trees=num_trees,
                num_leaves=num_leaves,
                minimum_instance_in_leaf=minimum_instance_in_leaf,
                bagging_fraction=bagging_fraction,
                feature_fraction=feature_fraction,
                split_fraction=split_fraction,
                quantile_sample_count=quantile_sample_count,
                quantile_value_list=quantile_value_list,
                random_number_seed=random_number_seed)
        else:
            ps_quantile_value_list = _parse_float_list("ps_quantile_value_list", ps_quantile_value_list)
            setting = FastForestQuantileRegressorSetting.init_range(
                ps_num_leaves=ps_num_leaves,
                ps_num_trees=ps_num_trees,
                ps_minimum_instance_in_leaf=ps_minimum_instance_in_leaf,
                ps_bagging_fraction=ps_bagging_fraction,
                ps_feature_fraction=ps_feature_fraction,
                ps_split_fraction=ps_split_fraction,
                quantile_sample_count=quantile_sample_count,
                quantile_value_list=ps_quantile_value_list,
                random_number_seed=random_number_seed)
        return setting

    @staticmethod
    def init_single(
            num_trees: int = DefaultParameters.NumTrees,
            num_leaves: int = DefaultParameters.NumLeaves,
            minimum_instance_in_leaf: int = DefaultParameters.MinimumInstanceInLeaf,
            bagging_fraction: float = DefaultParameters.BaggingFraction,
            feature_fraction: float = DefaultParameters.FeatureFraction,
            split_fraction: float = DefaultParameters.SplitFraction,
            quantile_sample_count: int = DefaultParameters.QuantileSampleCount,
            quantile_value_list: list = DefaultParameters.QuantileValueList,
            random_number_seed: int = DefaultParameters.RandomNumberSeed,
    ):
        setting = FastForestQuantileRegressorSetting(mode=CreateLearnerMode.SingleParameter, **locals())
        return setting

    @staticmethod
    def init_range(
            random_number_seed: int = None,
            quantile_sample_count: int = None,
            quantile_value_list: list = None,
            ps_num_leaves: ParameterRangeSettings = None,
            ps_num_trees: ParameterRangeSettings = None,
            ps_minimum_instance_in_leaf: ParameterRangeSettings = None,
            ps_bagging_fraction: ParameterRangeSettings = None,
            ps_feature_fraction: ParameterRangeSettings = None,
            ps_split_fraction: ParameterRangeSettings = None,
    ):
        setting = FastForestQuantileRegressorSetting(mode=CreateLearnerMode.ParameterRange, **locals())
        return setting


class FastForestQuantileRegressor(RegressionLearner):
    def __init__(self, setting: FastForestQuantileRegressorSetting):
        super().__init__(setting=setting, task_type=TaskType.QuantileRegression)

    @property
    def parameter_mapping(self):
        return {
            'n_estimators': RestoreInfo(FastForestQuantileRegressionModule._args.num_trees.friendly_name),
            'max_leaf_nodes': RestoreInfo(FastForestQuantileRegressionModule._args.num_leaves.friendly_name),
            'min_samples_leaf': RestoreInfo(
                FastForestQuantileRegressionModule._args.minimum_instance_in_leaf.friendly_name),
            'max_features': RestoreInfo(FastForestQuantileRegressionModule._args.split_fraction.friendly_name),
            'min_samples_split': RestoreInfo(
                FastForestQuantileRegressionModule._args.quantile_sample_count.friendly_name),
            'max_samples': RestoreInfo(FastForestQuantileRegressionModule._args.bagging_fraction.friendly_name)
        }

    def init_model(self):
        self.model = RandomForestRegressor(
            # Todo:
            #  feature_fraction: specifies the fraction of features (chosen randomly) to use for each tree. (0, 1)
            #  quantile_sample_count: specifies number of instances used in each node to estimate quantiles
            n_estimators=self.setting.num_trees,
            min_samples_leaf=self.setting.minimum_instance_in_leaf,
            max_leaf_nodes=self.setting.num_leaves,
            random_state=self.setting.random_number_seed,
            max_features=self.setting.split_fraction,
            max_samples=self.setting.bagging_fraction,
            n_jobs=-1)

    def _train(self, train_x, train_y):
        # train model
        with TimeProfile("Training Model"):
            # minimum_instance_in_leaf should not be larger than train sample count
            self.model.set_params(min_samples_leaf=min(self.setting.minimum_instance_in_leaf, train_x.shape[0]))
            self.model.fit(train_x, train_y)
        self._is_trained = True

    def _predict(self, test_x: pd.DataFrame):
        # predict model
        try:
            with TimeProfile("Predicting fast forest quantile regression value"):
                predicted_list = list()
                # fetch every trainer in the model, each tree constructs such a trainer
                for estimator in self.model.estimators_:
                    predicted_list.append(estimator.predict(test_x))
                predicted_list = np.array(predicted_list).T
                result = list()
                # use np.percentile to get predict value based on quantile value
                for q in self.setting.quantile_value_list:
                    result.append(np.percentile(predicted_list, round(q * 100), axis=1))
                return np.array(result), None
        except Exception as e:
            raise e

    def _build_result_dataframe(self, label, prob):
        """Build score for quantile column names

        e.g. If the quantile value list has 3 values: 0.25, 0.5 and 0.75, then the column names
        of the scored dataset would be "Scores for quantile:0.250", "Scores for quantile:0.500" and
        "Scores for quantile:0.750".
        """
        label_category_list = self.setting.quantile_value_list

        def _gen_scored_probability_column_name(score):
            """Generate quantile column names with pattern "Scores for quantile:score" """
            return ''.join((ScoreColumnConstants.QuantileScoredLabelsColumnName, "%.3f" % score))

        result_df = pd.DataFrame(data=label.T,
                                 columns=[_gen_scored_probability_column_name(i) for i in label_category_list])
        return result_df

    def generate_score_column_meta(self, predict_df):
        """Build score_column_names dict

        Map to QuantileScoredLabelsColumnName
        :return: built score column names dict
        """
        # should make sure the key and value is the same for the fast forest quantile regressor, since the
        # evaluator needs to calculate quantile values from the keys.
        score_columns = {x: x for x in filter_column_names_with_prefix(
            predict_df.columns, prefix=ScoreColumnConstants.QuantileScoredLabelsColumnName)}
        module_logger.info("Fast Forest Quantile Regression Model Scored Columns: ")
        module_logger.info(
            f'There are {len(score_columns.keys())} score columns: '
            f'"{profile_column_names(list(score_columns.keys()))}"')

        return score_columns
