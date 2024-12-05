import pandas as pd
from collections import namedtuple, Iterable
from azureml.studio.modules.ml.common.report_data import ReportData
from azureml.core.run import Run
from azureml.studio.core.logger import module_logger
from typing import Union
from azureml.studio.common.error import ErrorMapping

MetricsLogItem = namedtuple("MetricsLogItem", ["name", "data"])


class AzureMLMetricsDumper:
    def __init__(self):
        self.run = Run.get_context()

    def dump_scalar_metrics(self, scalars: Union[MetricsLogItem, Iterable]):
        if isinstance(scalars, MetricsLogItem):
            scalars = (scalars,)

        uploaded_scalars = []
        try:
            for scalar in scalars:
                if not pd.isna(scalar.data):
                    module_logger.info(f'Log scalar metric "{scalar.name}".')
                    self.run.log(scalar.name, scalar.data)
                    uploaded_scalars.append(scalar)
                else:
                    module_logger.warning(f'Scalar metric "{scalar.name}" is null, not log to metrics tab.')

            self.run.flush()
        # before module version 0.0.138, we only caught AzureMLException, ServiceException exceptions, however,
        # in addition to the exceptions in azureml.exceptions, other exceptions can be thrown during metrics logging,
        # and these errors are not recorded in the official documents:
        # https://docs.microsoft.com/en-us/python/api/azureml-core/azureml.exceptions?view=azure-ml-py
        # msrest.exceptions.ClientRequestError is an example. Thus, we catch all exceptions to make sure module run
        # won't be interrupted by the metrics.
        except BaseException as e:
            module_logger.warning(
                f"Failed to upload evaluation metrics. Reason: {ErrorMapping.get_exception_message(e)}")

        return uploaded_scalars

    def dump_table_metrics(self, tables: Union[MetricsLogItem, Iterable]):
        if isinstance(tables, MetricsLogItem):
            tables = (tables,)

        try:
            for table in tables:
                module_logger.info(f'Log table metric "{table.name}".')
                for _, row in table.data.iterrows():
                    self.run.log_row(table.name, **row.to_dict())

            self.run.flush()
        # before module version 0.0.138, we only caught AzureMLException, ServiceException exceptions, however,
        # in addition to the exceptions in azureml.exceptions, other exceptions can be thrown during metrics logging,
        # and these errors are not recorded in the official documents:
        # https://docs.microsoft.com/en-us/python/api/azureml-core/azureml.exceptions?view=azure-ml-py
        # msrest.exceptions.ClientRequestError is an example. Thus, we catch all exceptions to make sure module run
        # won't be interrupted by the metrics.
        except BaseException as e:
            module_logger.warning(
                f"Failed to upload evaluation metrics. Reason: {ErrorMapping.get_exception_message(e)}")

        return tables


class CommonEvaluateModelMetricsLogger:
    # the suffix of metrics name is from binary classification metrics visualization tab naming
    LEFT_PORT_SUFFIX = " (left port)"
    RIGHT_PORT_SUFFIX = " (right port)"
    azureml_metrics_dumper = AzureMLMetricsDumper()

    def log_metrics(self, data: pd.DataFrame, data_to_compare: pd.DataFrame = None):
        scalar_metrics = []
        if data_to_compare is not None:
            scalar_metrics += [MetricsLogItem(name + self.LEFT_PORT_SUFFIX, value) for name, value in
                               data.iloc[0].items()]
            scalar_metrics += [MetricsLogItem(name + self.RIGHT_PORT_SUFFIX, value) for name, value in
                               data_to_compare.iloc[0].items()]
        else:
            scalar_metrics += [MetricsLogItem(name, value) for name, value in data.iloc[0].items()]

        return self.azureml_metrics_dumper.dump_scalar_metrics(scalar_metrics)


class EvaluateClusterMetricsLogger(CommonEvaluateModelMetricsLogger):
    CLUSTERING_EVALUATION_TABLE_NAME = "Clustering evaluation"

    def log_metrics(self, data: pd.DataFrame, data_to_compare: pd.DataFrame = None):
        table_metrics = []
        if data_to_compare is not None:
            table_metrics.append(MetricsLogItem(self.CLUSTERING_EVALUATION_TABLE_NAME + self.LEFT_PORT_SUFFIX, data))
            table_metrics.append(
                MetricsLogItem(self.CLUSTERING_EVALUATION_TABLE_NAME + self.RIGHT_PORT_SUFFIX, data_to_compare))
        else:
            table_metrics.append(MetricsLogItem(self.CLUSTERING_EVALUATION_TABLE_NAME, data))

        return self.azureml_metrics_dumper.dump_table_metrics(table_metrics)


class EvaluateBinaryClassificationMetricsLogger(CommonEvaluateModelMetricsLogger):
    ROC_CURVE_NAME = "ROC curve"
    P_R_CURVE_NAME = "Precision-recall curve"
    LIFT_CURVE_NAME = "Lift curve"
    SCORED_BINS_NAME = "Scored bins"
    CONFUSION_MATRIX_NAME = "Confusion matrix"

    def log_metrics(self, report_data: ReportData, report_data_to_compare: ReportData = None):
        # if no valid bins (where there is no valid instances when evaluate), do not log any metrics
        if not report_data.chart.data_points:
            return []

        metric_loggers = [self._log_charts, self._log_threshold_scalar_metrics, self._log_confusion_matrix,
                          self._log_score_bins]
        metric_log_items = []
        if report_data_to_compare is not None:
            for logger in metric_loggers:
                metric_log_items += logger(report_data, self.LEFT_PORT_SUFFIX)
            for logger in metric_loggers:
                metric_log_items += logger(report_data_to_compare, self.RIGHT_PORT_SUFFIX)
        else:
            for logger in metric_loggers:
                metric_log_items += logger(report_data)

        return metric_log_items

    @staticmethod
    def _extract_chart_statistics(data_points):
        tpr = [x.tpr for x in data_points]
        fpr = [x.fpr for x in data_points]
        precision = [x.precision for x in data_points]
        recall = [x.recall for x in data_points]
        true_positive = [x.true_positive for x in data_points]
        y_rate = [x.y_rate for x in data_points]

        return tpr, fpr, precision, recall, true_positive, y_rate

    def _log_charts(self, report_data: ReportData, name_suffix=""):
        # compress bins to the max chart points
        tpr, fpr, precision, recall, true_positive, y_rate = self._extract_chart_statistics(
            report_data.chart.data_points)

        roc_curve = MetricsLogItem(f"{self.ROC_CURVE_NAME}{name_suffix}",
                                   pd.DataFrame({"False positive rate": fpr, "True positive rate": tpr}))
        pr_curve = MetricsLogItem(f"{self.P_R_CURVE_NAME}{name_suffix}",
                                  pd.DataFrame({"Recall": recall, "Precision": precision}))
        lift_curve = MetricsLogItem(f"{self.LIFT_CURVE_NAME}{name_suffix}",
                                    pd.DataFrame({"Positive rate": y_rate, "Number of true positive": true_positive}))
        charts_metrics = [roc_curve, pr_curve, lift_curve]

        return self.azureml_metrics_dumper.dump_table_metrics(charts_metrics)

    @staticmethod
    def _extract_score_bin_statistics(coarse_data, displayed_decimal=3):
        score_bin = [f'({round(x.bin_start, displayed_decimal)},{round(x.bin_end, displayed_decimal)}]' for x in
                     coarse_data]
        positive_example = [x.num_positive for x in coarse_data]
        negative_example = [x.num_negative for x in coarse_data]
        count = [x.count for x in coarse_data]
        fraction_above_threshold = [round(sum(count[i:]) / sum(count), displayed_decimal) for i in range(len(count))]
        accuracy = [round(x.accuracy, displayed_decimal) for x in coarse_data]
        f1 = [round(x.f1, displayed_decimal) for x in coarse_data]
        precision = [round(x.precision, displayed_decimal) for x in coarse_data]
        recall = [round(x.recall, displayed_decimal) for x in coarse_data]
        negative_precision = [round(x.neg_precision, displayed_decimal) for x in coarse_data]
        negative_recall = [round(x.neg_recall, displayed_decimal) for x in coarse_data]
        auc = [round(x.auc, displayed_decimal) for x in coarse_data]
        cumulative_auc = [round(sum(auc[i:]), displayed_decimal) for i in range(len(auc))]

        bins = pd.DataFrame({"Score bin": score_bin,
                             "Positive example": positive_example,
                             "Negative example": negative_example,
                             "Fraction above threshold": fraction_above_threshold,
                             "Accuracy": accuracy,
                             "F1 Score": f1,
                             "Precision": precision,
                             "Recall": recall,
                             "Negative precision": negative_precision,
                             "Negative recall": negative_recall,
                             "Cumulative AUC": cumulative_auc})
        return bins

    def _log_score_bins(self, report_data: ReportData, name_suffix=""):
        bins = self._extract_score_bin_statistics(report_data.chart.coarse_data)
        bins_table = MetricsLogItem(f"{self.SCORED_BINS_NAME}{name_suffix}", bins)

        return self.azureml_metrics_dumper.dump_table_metrics(bins_table)

    def _log_threshold_scalar_metrics(self, report_data: ReportData, name_suffix=""):
        coarse_data = report_data.chart.coarse_data
        threshold_bin = coarse_data[len(coarse_data) // 2]
        accuracy = threshold_bin.accuracy
        precision = threshold_bin.precision
        recall = threshold_bin.recall
        f1 = threshold_bin.f1
        auc = report_data.chart.auc

        scalar_metrics = [MetricsLogItem("Accuracy" + name_suffix, accuracy),
                          MetricsLogItem("Precision" + name_suffix, precision),
                          MetricsLogItem("Recall" + name_suffix, recall),
                          MetricsLogItem("F1 Score" + name_suffix, f1),
                          MetricsLogItem("AUC" + name_suffix, auc)]

        return self.azureml_metrics_dumper.dump_scalar_metrics(scalar_metrics)

    def _log_confusion_matrix(self, report_data: ReportData, name_suffix=""):
        predicted_label_column_name = "Predicted label"
        predicted_label_prefix = "Predicted"
        actual_label_prefix = "Actual"

        positive_label = report_data.chart.positive_label
        negative_label = report_data.chart.negative_label
        predicted_label_column = [f"{predicted_label_prefix}_{positive_label}",
                                  f"{predicted_label_prefix}_{negative_label}"]

        coarse_data = report_data.chart.coarse_data
        threshold_bin = coarse_data[len(coarse_data) // 2]
        actual_positive_label_column_name = f"{actual_label_prefix}_{positive_label}"
        actual_positive_label_column = [threshold_bin.true_positive, threshold_bin.false_negative]
        actual_negative_label_column_name = f"{actual_label_prefix}_{negative_label}"
        actual_negative_label_column = [threshold_bin.false_positive, threshold_bin.true_negative]

        confusion_matrix_df = pd.DataFrame({predicted_label_column_name: predicted_label_column,
                                            actual_positive_label_column_name: actual_positive_label_column,
                                            actual_negative_label_column_name: actual_negative_label_column})

        confusion_matrix_table = MetricsLogItem(f"{self.CONFUSION_MATRIX_NAME}{name_suffix}", confusion_matrix_df)
        module_logger.info(f'Log metrics table "{confusion_matrix_table.name}".')

        return self.azureml_metrics_dumper.dump_table_metrics(confusion_matrix_table)


common_evaluate_model_metrics_logger = CommonEvaluateModelMetricsLogger()
evaluate_cluster_metrics_logger = EvaluateClusterMetricsLogger()
evaluate_binary_classification_metrics_logger = EvaluateBinaryClassificationMetricsLogger()
