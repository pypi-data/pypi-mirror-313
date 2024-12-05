import pandas as pd

from azureml.studio.modulehost.constants import UINT32_MAX
from azureml.studio.common.error import LearnerTypesNotCompatibleError, UnsupportedParameterTypeError, \
    InvalidLearnerError, UntrainedModelError, ErrorMapping
from azureml.studio.common.datatable.data_table import DataTable
from azureml.studio.core.logger import module_logger as logger
from azureml.studio.common.types import AutoEnum
from azureml.studio.modulehost.attributes import ItemInfo, ModuleMeta, ILearnerInputPort, \
    DataTableInputPort, IntParameter, ModeParameter, DataTableOutputPort
from azureml.studio.internal.attributes.release_state import ReleaseState
from azureml.studio.modulehost.module_reflector import module_entry, BaseModule
from azureml.studio.modules.ml.common.base_learner import BaseLearner
from azureml.studio.modules.ml.common.ml_utils import TaskType
import numpy as np

from azureml.studio.modules.ml.evaluate.evaluate_generic_module.evaluate_generic_module import evaluate_generic
from azureml.studio.modules.ml.score.score_generic_module.score_generic_module import score_generic


class EvaluationMetricType(AutoEnum):
    Accuracy: ItemInfo(name="Accuracy", friendly_name="Classification - Accuracy") = ()
    Precision: ItemInfo(name="Precision", friendly_name="Classification - Precision") = ()
    Recall: ItemInfo(name="Recall", friendly_name="Classification - Recall") = ()
    AverageLogLoss: ItemInfo(name="Average Log Loss",
                             friendly_name="Classification - Average Log Loss",
                             release_state=ReleaseState.Alpha) = ()
    MeanAbsoluteError: ItemInfo(name="Mean Absolute Error", friendly_name="Regression - Mean Absolute Error") = ()
    RootMeanSquaredError: ItemInfo(name="Root Mean Squared Error",
                                   friendly_name="Regression - Root Mean Squared Error") = ()
    RelativeAbsoluteError: ItemInfo(name="Relative Absolute Error",
                                    friendly_name="Regression - Relative Absolute Error") = ()
    RelativeSquaredError: ItemInfo(name="Relative Squared Error",
                                   friendly_name="Regression - Relative Squared Error") = ()
    CoefficientOfDetermination: ItemInfo(name="Coefficient of Determination",
                                         friendly_name="Regression - Coefficient of Determination") = ()


class PermutationFeatureImportanceModule(BaseModule):
    FEATURE_COLUMN_NAME = 'Feature'
    SCORE_COLUMN_NAME = 'Score'

    _classification_metrics = {
        EvaluationMetricType.Accuracy,
        EvaluationMetricType.Precision,
        EvaluationMetricType.Recall,
        EvaluationMetricType.AverageLogLoss
    }

    _regression_metrics = {
        EvaluationMetricType.RootMeanSquaredError,
        EvaluationMetricType.CoefficientOfDetermination,
        EvaluationMetricType.RelativeAbsoluteError,
        EvaluationMetricType.MeanAbsoluteError,
        EvaluationMetricType.RelativeSquaredError
    }

    _negative_metrics = {
        EvaluationMetricType.RootMeanSquaredError,
        EvaluationMetricType.RelativeAbsoluteError,
        EvaluationMetricType.MeanAbsoluteError,
        EvaluationMetricType.RelativeSquaredError,
        EvaluationMetricType.AverageLogLoss
    }

    _task_type_metric_name_mapping = {
        TaskType.BinaryClassification: {
            EvaluationMetricType.Accuracy: "Accuracy",
            EvaluationMetricType.Precision: "Precision",
            EvaluationMetricType.Recall: "Recall",
        },
        TaskType.MultiClassification: {
            EvaluationMetricType.Accuracy: "Overall_Accuracy",
            EvaluationMetricType.Precision: "Macro_Precision",
            EvaluationMetricType.Recall: "Macro_Recall",
        },
        TaskType.Regression: {
            EvaluationMetricType.RootMeanSquaredError: "Root_Mean_Squared_Error",
            EvaluationMetricType.CoefficientOfDetermination: "Coefficient_of_Determination",
            EvaluationMetricType.RelativeAbsoluteError: "Relative_Absolute_Error",
            EvaluationMetricType.MeanAbsoluteError: "Mean_Absolute_Error",
            EvaluationMetricType.RelativeSquaredError: "Relative_Squared_Error"
        }
    }

    @staticmethod
    @module_entry(ModuleMeta(
        name="Permutation Feature Importance",
        description="Computes the permutation feature importance scores of feature variables"
                    " given a trained model and a test dataset.",
        category="Feature Selection",
        version="1.0",
        owner="Microsoft Corporation",
        family_id="2E010EE4-714E-44E9-933E-62D8C41818A9",
        release_state=ReleaseState.Release,
        is_deterministic=True,
    ))
    def run(
            learner: ILearnerInputPort(
                name="Trained model",
                friendly_name="Trained model",
                description="Trained model to be used for scoring",
            ),
            dataset: DataTableInputPort(
                name="Test data",
                friendly_name="Test data",
                description="Test dataset for scoring and evaluating a model after permutation of feature values",
            ),
            random_seed: IntParameter(
                name="Random seed",
                friendly_name="Random seed",
                min_value=0,
                max_value=UINT32_MAX,
                description="Random number generator seed value",
                default_value=0,
            ),
            evaluation_metric: ModeParameter(
                EvaluationMetricType,
                name="Metric for measuring performance",
                friendly_name="Metric for measuring performance",
                description="Evaluation metric",
                default_value=EvaluationMetricType.Accuracy,
            )
    ) -> (
            DataTableOutputPort(
                name="Feature importance",
                friendly_name="Feature importance",
                description="Feature importance results",
            ),
    ):
        input_values = locals()
        output_values = PermutationFeatureImportanceModule.run_impl(**input_values)
        return output_values

    @classmethod
    def run_impl(
            cls,
            learner: BaseLearner,
            dataset: DataTable,
            random_seed: int,
            evaluation_metric: EvaluationMetricType
    ):
        if not isinstance(learner, BaseLearner):
            ErrorMapping.throw(InvalidLearnerError(arg_name=cls._args.learner.friendly_name))

        task_type = learner.task_type
        logger.info(f"Task type of the input learner is {task_type}.")
        if task_type == TaskType.BinaryClassification or task_type == TaskType.MultiClassification:
            cls._validate_metric_type(evaluation_metric, cls._classification_metrics)
        elif task_type == TaskType.Regression:
            cls._validate_metric_type(evaluation_metric, cls._regression_metrics)
        else:

            ErrorMapping.throw(LearnerTypesNotCompatibleError(
                actual_learner_type=task_type.name if task_type else 'None',
                expected_learner_type_list=str([
                    # pylint: disable=E1101
                    TaskType.BinaryClassification.name,
                    TaskType.MultiClassification.name,
                    TaskType.Regression.name
                ])
            ))

        if not learner.is_trained:
            ErrorMapping.throw(UntrainedModelError(arg_name=cls._args.learner.friendly_name))

        if learner.label_column_name is None or learner.init_feature_columns_names is None:
            ErrorMapping.throw(InvalidLearnerError(arg_name=cls._args.learner.friendly_name))

        ErrorMapping.verify_number_of_rows_greater_than_or_equal_to(
            curr_row_count=dataset.number_of_rows,
            required_row_count=1,
            arg_name=cls._args.dataset.friendly_name
        )

        feature_column_score_results = cls._evaluate_permutations(learner, dataset, random_seed, evaluation_metric)
        return feature_column_score_results,

    @classmethod
    def _evaluate_permutations(
            cls,
            learner: BaseLearner,
            dataset: DataTable,
            random_seed: int,
            evaluation_metric: EvaluationMetricType):
        """This method will reorder the feature columns one by one with a random permutation sequence,
        and recalculate the evaluation metrics against the permuted dataset.
        Use differences in evaluation metric to indicate the importance of each feature column.
        :param learner:
        :param dataset:
        :param random_seed:
        :param evaluation_metric:
        :return:
        """

        # Get the evaluation result of the origin dataset and use the metric value as base_metric
        logger.info(f"Score and evaluate the learner with the input dataset to get the base metric.")
        base_evaluate_results = cls._score_and_evaluate(learner, dataset)
        base_metric = cls._get_evaluation_metric(learner, base_evaluate_results, evaluation_metric)

        number_of_rows = dataset.number_of_rows
        random_permutation = np.random.RandomState(seed=random_seed).permutation(number_of_rows)
        metric_sign = -1 if evaluation_metric in cls._negative_metrics else 1

        logger.info(f"{len(learner.init_feature_columns_names)} feature columns are defined in learner.")
        feature_columns = [col_name for col_name in learner.init_feature_columns_names
                           if col_name in dataset.column_names]
        logger.info(f"Found {len(feature_columns)} feature columns in the input dataset.")

        feature_column_scores = []
        for col_name in feature_columns:
            # Retain the origin feature column
            origin_column = dataset.data_frame[col_name].copy()

            # Reorder one feature column with the random permutation
            # Set the random permuted column back to the dataset
            permuted_column = origin_column.iloc[random_permutation].reset_index(drop=True)
            dataset.data_frame[col_name] = permuted_column

            # Get the evaluation result of the random permuted column
            permuted_evaluate_results = cls._score_and_evaluate(learner, dataset)
            permuted_metric = cls._get_evaluation_metric(learner, permuted_evaluate_results, evaluation_metric)

            # Compare with the base metric and calculate a score out.
            score = metric_sign * (base_metric - permuted_metric)
            feature_column_scores.append([col_name, score])

            # Reset the origin feature column
            dataset.data_frame[col_name] = origin_column

        logger.info(f"Score and evaluate the learner with the input dataset to get the base metric.")
        sorted_feature_column_scores = sorted(feature_column_scores, key=lambda x: x[1], reverse=True)
        result = DataTable(pd.DataFrame(
            data=sorted_feature_column_scores,
            columns=[cls.FEATURE_COLUMN_NAME, cls.SCORE_COLUMN_NAME]
        ))
        return result

    @classmethod
    def _score_and_evaluate(
            cls,
            learner: BaseLearner,
            dataset: DataTable
    ):
        dataset = dataset.clone()
        scored_data = score_generic(
            learner=learner,
            test_data=dataset,
            append_or_result_only=True)

        return evaluate_generic(scored_data=scored_data)

    @classmethod
    def _get_evaluation_metric(
            cls,
            learner: BaseLearner,
            base_evaluate_results: DataTable,
            evaluation_metric: EvaluationMetricType
    ):
        metric_name = cls._task_type_metric_name_mapping[learner.task_type][evaluation_metric]
        return base_evaluate_results.data_frame[metric_name].iloc[0]

    @classmethod
    def _validate_metric_type(cls, evaluation_metric, valid_metrics):
        if evaluation_metric not in valid_metrics:
            ErrorMapping.throw(UnsupportedParameterTypeError(
                parameter_name=cls._args.evaluation_metric.friendly_name,
                reason="The input metric isn't supported by the input learner."
            ))
