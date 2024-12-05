from azureml.studio.common.datatable.data_table import DataTable
from azureml.studio.common.error import TooFewColumnsInDatasetError, ErrorMapping
from azureml.studio.common.input_parameter_checker import InputParameterChecker
from azureml.studio.core.logger import module_logger
from azureml.studio.modulehost.attributes import ModuleMeta, ReleaseState, UntrainedLearnerInputPort, \
    DataTableInputPort, ILearnerOutputPort
from azureml.studio.modulehost.module_reflector import module_entry, BaseModule
from azureml.studio.modules.anomaly_detection.common.base_anomaly_detection import BaseAnomalyDetectionLearner
from azureml.studio.modules.ml.train.train_generic_model.train_generic_model import \
    insert_deployment_handler_into_learner


class TrainAnomalyDetectionModelModule(BaseModule):
    _param_keys = {
        "learner": "Untrained model",
        "training_data": "Dataset",
    }
    min_columns = 1

    @staticmethod
    @module_entry(ModuleMeta(
        name="Train Anomaly Detection Model",
        description="Trains an anomaly detector model and labels data from the training set",
        category="Anomaly Detection",
        version="1.0",
        owner="Microsoft Corporation",
        family_id="D6ACBACE-A72D-44B9-9878-869115E02458",
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
                description="Input data source",
            )
    ) -> (
            ILearnerOutputPort(
                name="Trained model",
                friendly_name="Trained model",
                description="Trained anomaly detection model",
            ),
    ):
        input_values = locals()
        output_values = TrainAnomalyDetectionModelModule.run_impl(**input_values)
        return output_values

    @classmethod
    def run_impl(cls, learner: BaseAnomalyDetectionLearner, training_data: DataTable):
        module_logger.info("Validate input data (learner and training data).")
        cls._validate_args(learner, training_data)
        try:
            learner.train(training_data)
            insert_deployment_handler_into_learner(learner, training_data)
        except Exception as e:
            raise e
        return learner,

    @classmethod
    def _validate_args(cls, learner, training_data):
        ErrorMapping.verify_not_null_or_empty(learner, cls._args.learner.friendly_name)
        ErrorMapping.verify_model_type(learner, BaseAnomalyDetectionLearner, arg_name=cls._args.learner.friendly_name)
        InputParameterChecker.verify_data_table(data_table=training_data, friendly_name=training_data.name)
        if training_data.number_of_columns < cls.min_columns:
            ErrorMapping.throw(TooFewColumnsInDatasetError(str(cls.min_columns)))
