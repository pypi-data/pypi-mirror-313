import azureml.studio.common.error as error_setting
from azureml.studio.common.datatable.data_table import DataTable
from azureml.studio.core.data_frame_schema import DataFrameSchema
from azureml.studio.core.logger import module_logger, TimeProfile
from azureml.studio.internal.attributes.release_state import ReleaseState
from azureml.studio.modulehost.attributes import (DataTableInputPort, ModuleMeta, DataTableOutputPort,
                                                  DataTypes)
from azureml.studio.modulehost.handler.sidecar_files import BinaryClassifierEvaluationComparisionVisualizer, \
    SideCarFileBundle
from azureml.studio.modulehost.module_reflector import module_entry, BaseModule
from azureml.studio.modules.ml.common.ml_utils import filter_column_names_with_prefix, TaskType
from azureml.studio.modules.ml.common.constants import ScoreColumnConstants, BINARY_CLASS_SCORED_COLUMN_NAMES, \
    MULTI_CLASS_SCORED_COLUMN_NAMES, REGRESSION_SCORED_COLUMN_NAMES, CLUSTER_SCORED_COLUMN_NAMES, \
    ANOMALY_DETECTION_COLUMN_NAMES
from azureml.studio.modules.ml.initialize_models.evaluator import BinaryClassificationEvaluator, \
    MultiClassificationEvaluator, RegressionEvaluator, ClusterEvaluator, AnomalyDetectionEvaluator, \
    QuantileRegressionEvaluator
from azureml.studio.modules.ml.common.metrics_logger import common_evaluate_model_metrics_logger, \
    evaluate_binary_classification_metrics_logger, evaluate_cluster_metrics_logger


class EvaluateModelModule(BaseModule):
    evaluation_results_as_json = None

    @staticmethod
    @module_entry(ModuleMeta(
        name="Evaluate Model",
        description="Evaluates the results of a classification or regression model with standard metrics.",
        category="Model Scoring & Evaluation",
        version="2.0",
        owner="Microsoft Corporation",
        family_id="{927D65AC-3B50-4694-9903-20F6C1672089}",
        release_state=ReleaseState.Release,
        is_deterministic=True,
    ))
    def run(
            scored_data: DataTableInputPort(
                name="Scored dataset",
                friendly_name="Scored dataset",
                description="Scored dataset",
            ),
            scored_data_to_compare: DataTableInputPort(
                name="Scored dataset to compare",
                friendly_name="Scored dataset to compare",
                is_optional=True,
                description="Scored dataset to compare (optional)",
            )
    ) -> (
            DataTableOutputPort(
                data_type=DataTypes.DATASET,
                name="Evaluation results",
                friendly_name="Evaluation results",
                description="Data evaluation result",
            ),
    ):
        input_values = locals()
        output_values = EvaluateModelModule.evaluate_generic(**input_values)
        return output_values

    @classmethod
    def _collect_from_extended_properties(cls, meta_data, dataset_name):
        """Compatible with previous method for passing on task types"""
        scored_data_info = meta_data.extended_properties
        if scored_data_info is not None and scored_data_info.get('is_scored_data', False):
            task_type = scored_data_info.get('learner_type', None)
        else:
            task_type = None
        return task_type

    @classmethod
    def _infer_from_score_columns(cls, meta_data: DataFrameSchema):
        """Infer task type based on LabelType of score_column_names"""
        score_columns = meta_data.score_column_names
        if ScoreColumnConstants.BinaryClassScoredLabelType in score_columns:
            return TaskType.BinaryClassification
        elif ScoreColumnConstants.MultiClassScoredLabelType in score_columns:
            return TaskType.MultiClassification
        elif ScoreColumnConstants.RegressionScoredLabelType in score_columns:
            return TaskType.Regression
        elif ScoreColumnConstants.ClusterScoredLabelType in score_columns:
            return TaskType.Cluster
        elif ScoreColumnConstants.AnomalyDetectionScoredLabelType in score_columns:
            return TaskType.AnomalyDetection
        elif filter_column_names_with_prefix(score_columns, prefix=ScoreColumnConstants.QuantileScoredLabelsColumnName):
            return TaskType.QuantileRegression
        return None

    @classmethod
    def _infer_from_score_column_names(cls, column_names):
        """Infer task type based on column names of the data_table."""

        def has_required_column_names(required_column_names):
            return all([name in column_names for name in required_column_names])

        if has_required_column_names(BINARY_CLASS_SCORED_COLUMN_NAMES):
            return TaskType.BinaryClassification
        elif has_required_column_names(MULTI_CLASS_SCORED_COLUMN_NAMES):
            return TaskType.MultiClassification
        elif has_required_column_names(REGRESSION_SCORED_COLUMN_NAMES):
            return TaskType.Regression
        elif has_required_column_names(CLUSTER_SCORED_COLUMN_NAMES):
            return TaskType.Cluster
        elif has_required_column_names(ANOMALY_DETECTION_COLUMN_NAMES):
            return TaskType.AnomalyDetection
        else:
            error_setting.ErrorMapping.throw(error_setting.NotScoredDatasetError())

    @classmethod
    def _collect_task_type(cls, data_table: DataTable, dataset_name):
        meta_data = data_table.meta_data
        if meta_data.score_column_names:
            task_type = cls._infer_from_score_columns(meta_data)
        else:
            task_type = cls._collect_from_extended_properties(meta_data, dataset_name)
            if task_type is None:
                # if cannot deduce task type from extended_properties, try to infer task type
                # from data_table column names
                task_type = cls._infer_from_score_column_names(column_names=data_table.column_names)

        if task_type is None:
            error_setting.ErrorMapping.throw(error_setting.UnableToEvaluateCustomModelError())
        return task_type

    @classmethod
    def _validate_data_table(cls, data_table: DataTable, task_type, dataset_name):
        # scored data should not be null or empty
        error_setting.ErrorMapping.verify_not_null_or_empty(data_table, name=dataset_name)
        label_column_name = data_table.meta_data.label_column_name
        # if a supervised learning result is evaluated, label column should be provided.
        if task_type != TaskType.Cluster:
            # label column should be found in data_table
            if label_column_name not in data_table.column_names:
                error_setting.ErrorMapping.throw(error_setting.NotLabeledDatasetError(dataset_name=dataset_name))
            # check if the label list contains notna value
            case_count = data_table.number_of_rows
            if data_table.get_number_of_missing_value(label_column_name) == case_count:
                error_setting.ErrorMapping.throw(
                    error_setting.LabelColumnDoesNotHaveLabeledPointsError(required_rows_count=1,
                                                                           dataset_name=dataset_name))

    @classmethod
    def _validate_input(cls, scored_data: DataTable, scored_data_to_compare=None):
        task_type = cls._collect_task_type(data_table=scored_data, dataset_name=cls._args.scored_data.friendly_name)
        cls._validate_data_table(data_table=scored_data,
                                 task_type=task_type,
                                 dataset_name=cls._args.scored_data.friendly_name)

        module_logger.info(f"Get a {task_type} Model Scored Data from InputPort1.")
        module_logger.info(
            f"Scored data from InputPort1 has {scored_data.number_of_rows} "
            f"Row(s) and {scored_data.number_of_columns} Columns.")
        if scored_data_to_compare is not None:
            task_type_to_compare = cls._collect_task_type(scored_data_to_compare,
                                                          cls._args.scored_data_to_compare.friendly_name)
            cls._validate_data_table(data_table=scored_data_to_compare,
                                     task_type=task_type_to_compare,
                                     dataset_name=cls._args.scored_data_to_compare.friendly_name)
            module_logger.info(f"Get a {task_type_to_compare} Model Scored Data from InputPort2.")
            module_logger.info(
                f"Scored data from InputPort2 has {scored_data_to_compare.number_of_rows} Row(s) "
                f"and {scored_data_to_compare.number_of_columns} Columns.")
            if task_type != task_type_to_compare:
                error_setting.ErrorMapping.throw(error_setting.LearnerTypesNotCompatibleError())

    @classmethod
    def evaluate_generic(cls, scored_data: DataTable, scored_data_to_compare=None, output_metrics=True):
        module_logger.info("Validate input data (Scored Data).")
        cls._validate_input(scored_data=scored_data, scored_data_to_compare=scored_data_to_compare)
        task_type = cls._collect_task_type(scored_data, cls._args.scored_data.friendly_name)
        module_logger.info("Validated input data.")

        # set evaluator class according to the task type
        if task_type == TaskType.BinaryClassification:
            evaluator_class = BinaryClassificationEvaluator
            module_logger.debug('Use Binary Classification Metric.')
        elif task_type == TaskType.MultiClassification:
            evaluator_class = MultiClassificationEvaluator
            module_logger.debug('Use Multi Classification Metric.')
        elif task_type == TaskType.Regression:
            evaluator_class = RegressionEvaluator
            module_logger.debug('Use Regression Metric.')
        elif task_type == TaskType.AnomalyDetection:
            evaluator_class = AnomalyDetectionEvaluator
            module_logger.debug('Use Anomaly Detection Metric.')
        elif task_type == TaskType.QuantileRegression:
            evaluator_class = QuantileRegressionEvaluator
            module_logger.debug('Use Quantile Regression Metric.')
        else:
            module_logger.debug('Use Clustering Metric.')
            evaluator_class = ClusterEvaluator

        visualizer = None

        scored_data_evaluator = evaluator_class()
        to_compare_data_evaluator = evaluator_class(to_compare=True)

        with TimeProfile("Evaluate Scored Data"):
            result_df, report_data = scored_data_evaluator.evaluate_data(
                scored_data=scored_data,
                dataset_name=cls._args.scored_data.friendly_name,
                output_metrics=output_metrics)
        with TimeProfile("Evaluate Scored Data to Compare"):
            result_df_to_compare, report_data_to_compare = to_compare_data_evaluator.evaluate_data(
                scored_data=scored_data_to_compare,
                dataset_name=cls._args.scored_data_to_compare.friendly_name,
                output_metrics=output_metrics)
        if task_type == TaskType.BinaryClassification:
            visualizer = BinaryClassifierEvaluationComparisionVisualizer(report_data,
                                                                         report_data_to_compare)
            if output_metrics:
                evaluate_binary_classification_metrics_logger.log_metrics(report_data, report_data_to_compare)
        elif task_type == TaskType.Cluster and output_metrics:
            evaluate_cluster_metrics_logger.log_metrics(result_df, result_df_to_compare)
        elif output_metrics:
            common_evaluate_model_metrics_logger.log_metrics(result_df, result_df_to_compare)

        if result_df_to_compare is not None:
            result_df = result_df.append(result_df_to_compare, ignore_index=True)
        dt = DataTable(result_df)
        result = SideCarFileBundle.create(dt, visualizer=visualizer) if visualizer else dt
        return result,


def evaluate_generic(scored_data, scored_data_to_compare=None, output_metrics=False):
    evaluation_result, = EvaluateModelModule.evaluate_generic(scored_data, scored_data_to_compare,
                                                              output_metrics=output_metrics)
    if isinstance(evaluation_result, SideCarFileBundle):
        return evaluation_result.data
    else:
        return evaluation_result
