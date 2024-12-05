import azureml.studio.modules.ml.common.ml_utils as ml_utils
from azureml.studio.common.datatable.data_table import DataTable
from azureml.studio.common.datatable.data_table import DataTableColumnSelection
from azureml.studio.common.error import TooFewColumnsInDatasetError, ErrorMapping, \
    LearnerTypesNotCompatibleError
from azureml.studio.common.input_parameter_checker import InputParameterChecker
from azureml.studio.modulehost.constants import UINT32_MAX
from azureml.studio.modulehost.attributes import ModuleMeta, UntrainedLearnerInputPort, \
    DataTableInputPort, DataTableOutputPort, ColumnPickerParameter, SelectedColumnCategory, \
    ILearnerOutputPort, ModeParameter, IntParameter
from azureml.studio.internal.attributes.release_state import ReleaseState
from azureml.studio.modulehost.module_reflector import module_entry, BaseModule
from azureml.studio.modules.ml.common.base_learner import BaseLearner
from azureml.studio.modules.ml.common.learner_parameter_sweeper import (
    SweepMethods, BinaryClassificationMetricType, RegressionMetricType,
    LearnerParameterSweeperSetting, LearnerParameterSweeper
)
from azureml.studio.modules.ml.train.train_generic_model.train_generic_model import \
    insert_deployment_handler_into_learner


class TuneModelHyperParametersModule(BaseModule):
    @staticmethod
    @module_entry(ModuleMeta(
        name="Tune Model Hyperparameters",
        description="Perform a parameter sweep on the model to determine the optimum parameter settings.",
        category="Model Training",
        version="1.0",
        owner="Microsoft Corporation",
        family_id="038D91B6-C2F2-42A1-9215-1F2C20ED1B40",
        release_state=ReleaseState.Release,
        is_deterministic=True,
        has_serving_entry=False
    ))
    def run(
            predictor: UntrainedLearnerInputPort(
                name="Untrained model",
                friendly_name="Untrained model",
                description="Untrained model for parameter sweep",
            ),
            train_data: DataTableInputPort(
                name="Training dataset",
                friendly_name="Training dataset",
                description="Input dataset for training",
            ),
            validation_data: DataTableInputPort(
                name="Validation dataset",
                friendly_name="Optional validation dataset",
                is_optional=True,
                description="Input dataset for validation (for Train/Test validation mode)",
            ),
            sweeping_mode: ModeParameter(
                SweepMethods,
                name="Specify parameter sweeping mode",
                friendly_name="Specify parameter sweeping mode",
                description="Sweep entire grid on parameter space, or sweep with using a limited number of sample runs",
                default_value=SweepMethods.RandomSweep,
            ),
            max_num_of_runs: IntParameter(
                name="Maximum number of runs on random sweep",
                friendly_name="Maximum number of runs on random sweep",
                description="Execute maximum number of runs using random sweep",
                default_value=5,
                parent_parameter="Specify parameter sweeping mode",
                parent_parameter_val=(SweepMethods.RandomSweep,),
                min_value=1,
                max_value=10000,
            ),
            random_seed: IntParameter(
                name="Random seed",
                friendly_name="Random seed",
                min_value=0,
                max_value=UINT32_MAX,
                description="Provide a value to seed the random number generator",
                default_value=0,
                parent_parameter="Specify parameter sweeping mode",
                parent_parameter_val=(SweepMethods.RandomSweep,),
            ),
            max_num_of_runs1: IntParameter(
                name="Maximum number of runs on random grid",
                friendly_name="Maximum number of runs on random grid",
                description="Execute maximum number of runs using random grid",
                default_value=5,
                parent_parameter="Specify parameter sweeping mode",
                parent_parameter_val=(SweepMethods.RandomGrid,),
                min_value=1,
                max_value=10000,
                release_state=ReleaseState.Alpha
            ),
            random_seed1: IntParameter(
                name="Random seed for random grid",
                friendly_name="Random seed",
                min_value=0,
                max_value=UINT32_MAX,
                description="Provide a value to seed the random number generator for random grid",
                default_value=0,
                parent_parameter="Specify parameter sweeping mode",
                parent_parameter_val=(SweepMethods.RandomGrid,),
                release_state=ReleaseState.Alpha
            ),
            label_column_index_or_name: ColumnPickerParameter(
                name="Name or numerical index of the label column",
                friendly_name="Label column",
                description="Label column",
                column_picker_for="Training dataset",
                single_column_selection=True,
                column_selection_categories=(SelectedColumnCategory.All,),
            ),
            binary_classification_metric: ModeParameter(
                BinaryClassificationMetricType,
                name="Metric for measuring performance for classification",
                friendly_name="Metric for measuring performance for classification",
                description="Select the metric used for evaluating classification models",
                default_value=BinaryClassificationMetricType.Accuracy,
            ),
            regression_metric: ModeParameter(
                RegressionMetricType,
                name="Metric for measuring performance for regression",
                friendly_name="Metric for measuring performance for regression",
                description="Select the metric used for evaluating regression models",
                default_value=RegressionMetricType.MeanAbsoluteError,
            )
    ) -> (
            DataTableOutputPort(
                name="Sweep results",
                friendly_name="Sweep results",
                description="Results metric for parameter sweep runs",
            ),
            ILearnerOutputPort(
                name="Trained best model",
                friendly_name="Trained best model",
                description="Model with best performance on the training dataset",
            ),
    ):
        input_values = locals()
        output_values = TuneModelHyperParametersModule.tune_model_hyperparameter(**input_values)
        return output_values

    @classmethod
    def _validate_predictor(cls, predictor):
        _support_task_type = (
            ml_utils.TaskType.BinaryClassification, ml_utils.TaskType.MultiClassification,
            ml_utils.TaskType.Regression, ml_utils.TaskType.QuantileRegression)
        task_type = predictor.task_type
        if task_type not in _support_task_type:
            ErrorMapping.throw(LearnerTypesNotCompatibleError(
                actual_learner_type=task_type.name if task_type else 'None',
                expected_learner_type_list=str(_support_task_type)
            ))

    @classmethod
    def _validate_data_set(cls, data_set):
        InputParameterChecker.verify_data_table(data_table=data_set, friendly_name=data_set.name)
        if data_set.number_of_columns < 2:
            ErrorMapping.throw(TooFewColumnsInDatasetError(arg_name=data_set.name, required_columns_count=2))

    @classmethod
    def tune_model_hyperparameter(cls, predictor: BaseLearner, train_data: DataTable,
                                  sweeping_mode: SweepMethods,
                                  label_column_index_or_name: DataTableColumnSelection,
                                  binary_classification_metric: BinaryClassificationMetricType,
                                  regression_metric: RegressionMetricType,
                                  validation_data: DataTable = None,
                                  max_num_of_runs: int = None,
                                  max_num_of_runs1: int = None,
                                  random_seed: int = None,
                                  random_seed1: int = None,
                                  ):
        cls._validate_predictor(predictor)

        task_type = predictor.task_type
        cls._validate_data_set(data_set=train_data)
        if validation_data is not None:
            cls._validate_data_set(data_set=validation_data)
        # create tune parameter sweeper
        setting = LearnerParameterSweeperSetting(
            sweeping_mode=sweeping_mode,
            binary_classification_metric=binary_classification_metric,
            regression_metric=regression_metric,
            max_num_of_runs=max_num_of_runs, random_seed=random_seed)
        learner = LearnerParameterSweeper(setting=setting, task_type=task_type, learner=predictor)
        # start to sweep hyper-parameters

        learner.train(train_data, label_column_index_or_name, validation_data)

        best_model = learner.get_best_model()
        insert_deployment_handler_into_learner(best_model, train_data)
        return DataTable(learner.get_report()), best_model
