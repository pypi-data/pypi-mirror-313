import azureml.studio.common.error as error_setting
from azureml.studio.common.datatable.data_table import DataTable
from azureml.studio.common.input_parameter_checker import InputParameterChecker
from azureml.studio.core.logger import module_logger
from azureml.studio.common.error import ErrorMapping, FailedToEvaluateScriptError
from azureml.studio.internal.attributes.release_state import ReleaseState
from azureml.studio.modulehost.attributes import (ILearnerInputPort, DataTableInputPort, BooleanParameter, ModuleMeta,
                                                  DataTableOutputPort, DataTypes)
from azureml.studio.modulehost.module_reflector import module_entry, BaseModule
from azureml.studio.modules.ml.common.base_learner import BaseLearner
from azureml.studio.modules.ml.common.constants import META_PROPERTY_LABEL_ENCODER_KEY
from azureml.studio.modules.ml.common.ml_utils import append_predict_result, TaskType
from azureml.studio.modules.python_language_modules.create_python_model.create_python_model import CustomModelProxy, \
    SCRIPT_LANGUAGE


class ScoreModelModule(BaseModule):

    @staticmethod
    @module_entry(ModuleMeta(
        name="Score Model",
        description="Scores predictions for a trained classification or regression model.",
        category="Model Scoring & Evaluation",
        version="2.0",
        owner="Microsoft Corporation",
        family_id="{401B4F92-E724-4D5A-BE81-D5B0FF9BDB33}",
        release_state=ReleaseState.Release,
        is_deterministic=True,
    ))
    def run(
            learner: ILearnerInputPort(
                name="Trained model",
                friendly_name="Trained model",
                description="Trained predictive model",
            ),
            test_data: DataTableInputPort(
                name="Dataset",
                friendly_name="Dataset",
                description="Input test dataset",
            ),
            append_or_result_only: BooleanParameter(
                name="Append score columns to output",
                friendly_name="Append score columns to output",
                description="If checked, append score columns to the result dataset, "
                            "otherwise only return the scores and true labels if available.",
                default_value=True,
            )
    ) -> (
            DataTableOutputPort(
                data_type=DataTypes.DATASET,
                name="Scored dataset",
                friendly_name="Scored dataset",
                description="Dataset with obtained scores",
            ),
    ):
        input_values = locals()
        output_values = ScoreModelModule.score_generic(**input_values)
        return output_values

    @classmethod
    def _validate_args(cls, learner, test_data):
        error_setting.ErrorMapping.verify_not_null_or_empty(learner)
        if not learner.is_trained:
            error_setting.ErrorMapping.throw(error_setting.UntrainedModelError())
        InputParameterChecker.verify_data_table(test_data, cls._args.test_data.friendly_name)

    @staticmethod
    def score_generic(learner: BaseLearner, test_data: DataTable, append_or_result_only: bool):
        ScoreModelModule._validate_args(learner, test_data)
        # reset the index of data frame
        test_data.reset_data_frame_index()
        # get a copy of the input dataframe to perform normalizing.
        test_data_df = test_data.data_frame.copy()
        module_logger.info(
            f"Validated testing data has {test_data_df.shape[0]} Row(s) and {test_data_df.shape[1]} Columns.")
        result_df = learner.predict(test_data_df=test_data_df)
        if result_df.shape[0] != test_data.number_of_rows:
            raise ValueError(f"Rows number not match: Scored result has {result_df.shape[0]} rows, "
                             f"while input test data has {test_data.number_of_rows} rows.")
        if append_or_result_only:
            # build output data table with the original data and scored result

            if isinstance(learner, CustomModelProxy) and not result_df.index.is_unique:
                ErrorMapping.throw(FailedToEvaluateScriptError(
                    script_language=SCRIPT_LANGUAGE,
                    message='For "Append score columns to output=True", the result DataFrame is not allowed to '
                            'contain duplicated indexes. Please consider to reindex the result DataFrame.'
                ))
            data_table = append_predict_result(data_table=test_data, predict_df=result_df)
        else:
            # build output data table with the score columns and the label column(if provided).
            data_table = DataTable(result_df)
            if learner.label_column_name in test_data.column_names:
                # Fix bug 706096, where learner.label_column_name is duplicated with score column name.
                if learner.label_column_name in data_table.column_names:
                    error_setting.ErrorMapping.throw(
                        error_setting.DuplicatedColumnNameError(
                            duplicated_name=learner.label_column_name,
                            details="label column name is duplicated with the score column name"))
                data_table.add_column(learner.label_column_name, test_data.get_column(learner.label_column_name))

        # keep original label column if 'Anomaly Detection' task.
        if learner.task_type == TaskType.AnomalyDetection and test_data.meta_data.label_column_name is not None:
            data_table.meta_data.label_column_name = test_data.meta_data.label_column_name
        # warning if data table and learn has conflict label column
        # the label_column_name in data table will be overwrote.
        elif data_table.meta_data.label_column_name is not None \
                and data_table.meta_data.label_column_name != learner.label_column_name \
                and learner.label_column_name in data_table.column_names:
            module_logger.warning(
                f"{learner.label_column_name} will be regarded as label column according to the training setting.")
            data_table.meta_data.label_column_name = learner.label_column_name
        elif learner.label_column_name in data_table.column_names:
            data_table.meta_data.label_column_name = learner.label_column_name

        # set score column names meta data
        score_columns = learner.generate_score_column_meta(predict_df=result_df)
        data_table.meta_data.score_column_names = score_columns
        # save label encoder in scored data meta data if non-numeric regression label
        if (learner.task_type == TaskType.Regression or learner.task_type == TaskType.QuantileRegression) and \
                len(learner.normalizer.label_column_encoders) > 0:
            label_encoder = learner.normalizer.label_column_encoders[learner.label_column_name]
            data_table.meta_data.extended_properties[META_PROPERTY_LABEL_ENCODER_KEY] = label_encoder

        return tuple([data_table])


def score_generic(learner, test_data, append_or_result_only):
    score_result, = ScoreModelModule.score_generic(learner, test_data, append_or_result_only)
    return score_result
