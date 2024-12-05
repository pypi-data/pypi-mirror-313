from azureml.studio.modules.ml.common.report_data import ReportData


class ReportDataJsonConverter(object):

    def report_to_dict(self, report):
        if not isinstance(report, ReportData):
            raise TypeError(f"Expects <type: ReportData> but got a {type(report)}")

        return {
            "chart": self._encode_chart(report.chart),
            "reportName": report.report_name
        }

    def _encode_chart(self, chart):
        return {
            "auc": chart.auc,
            "min": chart.min_value,
            "max": chart.max_value,
            "data": self._encode_data_points(chart.data_points),
            "coarseData": self._encode_coarse_data(chart.coarse_data),
            "positiveLabel": None if chart.positive_label is None else chart.positive_label,
            "negativeLabel": None if chart.negative_label is None else chart.negative_label
        }

    def _encode_data_points(self, data_points):
        return [self._encode_single_data_point(x) for x in data_points]

    def _encode_coarse_data(self, coarse_data):
        return [self._encode_single_score_bin(x) for x in coarse_data]

    @staticmethod
    def _encode_single_data_point(x):
        return {
            "probability": round(x.bin_start, 3),
            "confusionMatrix": {
                "tp": x.true_positive,
                "tn": x.true_negative,
                "fp": x.false_positive,
                "fn": x.false_negative
            },
            "tpr": x.tpr,
            "fpr": x.fpr,
            "precision": x.precision,
            "recall": x.recall,
            "accuracy": x.accuracy,
            "truepositive": x.true_positive * 1.0,
            "yrate": x.y_rate,
            "f1": x.f1
        }

    @staticmethod
    def _encode_single_score_bin(x):
        return {
            "BinStart": x.bin_start,
            "BinEnd": x.bin_end,
            "tpr": x.tpr,
            "fpr": x.fpr,
            "precision": x.precision,
            "recall": x.recall,
            "negPrecision": x.neg_precision,
            "negRecall": x.neg_recall,
            "accuracy": x.accuracy,
            "f1": x.f1,
            "AUC": x.auc,
            "numPos": x.num_positive,
            "numNeg": x.num_negative,
            "Count": x.count,
            "tp": x.true_positive,
            "fp": x.false_positive,
            "tn": x.true_negative,
            "fn": x.false_negative
        }
