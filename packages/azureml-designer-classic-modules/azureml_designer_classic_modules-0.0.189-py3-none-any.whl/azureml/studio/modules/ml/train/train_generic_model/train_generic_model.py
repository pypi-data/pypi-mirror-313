from azureml.studio.common.datatable.data_table import DataTable
from azureml.studio.common.datatable.data_table import DataTableColumnSelection
from azureml.studio.common.error import TooFewColumnsInDatasetError, InvalidLearnerError, ErrorMapping
from azureml.studio.common.input_parameter_checker import InputParameterChecker
from azureml.studio.core.logger import module_logger
from azureml.studio.internal.attributes.release_state import ReleaseState
from azureml.studio.modulehost.attributes import ModuleMeta, UntrainedLearnerInputPort, DataTableInputPort, \
    ColumnPickerParameter, SelectedColumnCategory, ILearnerOutputPort, BooleanParameter
from azureml.studio.modulehost.module_reflector import module_entry, BaseModule
from azureml.studio.modules.anomaly_detection.common.base_anomaly_detection import BaseAnomalyDetectionLearner
from azureml.studio.modules.ml.common.base_learner import BaseLearner
from azureml.studio.modules.ml.model_deployment.model_deployment_handler import BaseLearnerDeploymentHandler
from azureml.studio.core.logger import TimeProfile
from azureml.studio.modules.ml.common.mimic_explainer_wrapper import explain_model


class TrainModelModule(BaseModule):
    key_train_generic_model = {
        "learner": "Untrained model",
        "training_data": "Dataset",
        "otrained_model": "Trained model",
        "label_column_index_or_name": "Label column",
        "train_generic_model": "Train Model"
    }
    min_columns = 2

    @staticmethod
    @module_entry(ModuleMeta(
        name="Train Model",
        description="Trains a classification or regression model in a supervised manner.",
        category="Model Training",
        version="2.0",
        owner="Microsoft Corporation",
        family_id="{5CC7053E-AA30-450D-96C0-DAE4BE720977}",
        release_state=ReleaseState.Release,
        is_deterministic=True,
        has_serving_entry=False
    ))
    def run(
            learner: UntrainedLearnerInputPort(
                name="Untrained model",
                friendly_name="Untrained model",
                description="Untrained learner",
            ),
            training_data: DataTableInputPort(
                name="Dataset",
                friendly_name="Dataset",
                description="Training data",
            ),
            label_column_index_or_name: ColumnPickerParameter(
                name="Label column",
                friendly_name="Label column",
                description="Select the column that contains the label or outcome column",
                column_picker_for="Dataset",
                single_column_selection=True,
                column_selection_categories=(SelectedColumnCategory.All,),
            ),
            model_explanations: BooleanParameter(
                name="Model explanations",
                friendly_name="Model explanations",
                description="Whether to generate explanations for the trained model. "
                            "Default is unchecked to reduce extra compute overhead.",
                default_value=False,
                is_optional=True,
            ),
    ) -> (
            ILearnerOutputPort(
                name="Trained model",
                friendly_name="Trained model",
                description="Trained learner",
            ),
    ):
        input_values = locals()
        output_values = TrainModelModule.train_generic_model(**input_values)
        return output_values

    @classmethod
    def _validate_args(cls, learner, training_data):
        ErrorMapping.verify_not_null_or_empty(learner, cls._args.learner.friendly_name)
        # generic train model module should not support base anomaly detection learner.
        if isinstance(learner, BaseAnomalyDetectionLearner):
            ErrorMapping.throw(InvalidLearnerError(arg_name=cls._args.learner.friendly_name,
                                                   learner_type=learner.__class__.__name__))

        InputParameterChecker.verify_data_table(data_table=training_data, friendly_name=training_data.name)
        if training_data.number_of_columns < cls.min_columns:
            ErrorMapping.throw(TooFewColumnsInDatasetError(
                arg_name=cls._args.training_data.friendly_name,
                required_columns_count=cls.min_columns))

    @classmethod
    def train_generic_model(cls, learner: BaseLearner, training_data: DataTable,
                            label_column_index_or_name: DataTableColumnSelection, model_explanations=True):
        module_logger.info("Validate input data (learner and training data).")
        cls._validate_args(learner, training_data)

        insert_deployment_handler_into_learner(learner, training_data)
        learner.train(training_data, label_column_index_or_name)

        if model_explanations:
            with TimeProfile("Generate global explanation"):
                explain_model(learner, initialization_examples=training_data.data_frame,
                              evaluation_examples=training_data.data_frame)

        return learner,


def train_generic(learner, training_data, label_column_index_or_name, model_explanations=False):
    train_result, = TrainModelModule.train_generic_model(learner, training_data, label_column_index_or_name,
                                                         model_explanations=model_explanations)
    return train_result


def insert_deployment_handler_into_learner(learner: BaseLearner, dt: DataTable):
    with TimeProfile("Create deployment handler and inject schema and sample."):
        deployment_handler = BaseLearnerDeploymentHandler()
        deployment_handler.data_schema = dt.meta_data.to_dict()
        deployment_handler.sample_data = dt.get_samples()
        learner.deployment_handler = deployment_handler
