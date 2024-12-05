import numpy as np
from sklearn.metrics import balanced_accuracy_score, confusion_matrix
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.metrics import roc_auc_score, accuracy_score, precision_score, recall_score, f1_score, roc_curve

from azureml.studio.modules.ml.common import metric_calculator


class MetricBase:
    def __init__(self, func, result_name, require_prob=False):
        self.func = func
        self.result_name = result_name
        self.require_prob = require_prob
        self.func_param = dict()


class BinaryMetricBase(MetricBase):
    def get_evaluate_result(self, y_true, y_pred, threshold=None):
        if not self.require_prob:
            if threshold is None:
                threshold = 0.5
            y_pred = (y_pred >= threshold)
        return self.result_name, self.func(y_true, y_pred)


class MultiClassMetricBase(MetricBase):
    def get_evaluate_result(self, y_true, y_pred, threshold=None):
        if (not self.require_prob) and len(y_pred.shape) != 1 and y_pred.shape[-1] != 1:
            y_pred = np.argmax(y_pred, axis=1)
        return self.result_name, self.func(y_true, y_pred, **self.func_param)


class RegressionMetricBase(MetricBase):
    def get_evaluate_result(self, y_true, y_pred, threshold=None):
        return self.result_name, self.func(y_true, y_pred, **self.func_param)


class BiAUCMetric(BinaryMetricBase):
    def __init__(self):
        super().__init__(self, roc_auc_score, result_name='AUC', require_prob=True)


class BiAccuracyMetric(BinaryMetricBase):
    def __init__(self):
        super().__init__(self, accuracy_score, result_name='Accuracy')


class BiPrecisionMetric(BinaryMetricBase):
    def __init__(self):
        super().__init__(self, precision_score, result_name='Precision')


class BiRecallMetric(BinaryMetricBase):
    def __init__(self):
        super().__init__(self, recall_score, result_name='Recall')


class BiF1Metric(BinaryMetricBase):
    def __init__(self):
        super().__init__(self, f1_score, result_name='F1')


class BiROCMetric(BinaryMetricBase):
    def __init__(self):
        super().__init__(self, roc_curve, result_name='ROC', require_prob=True)


class BiConfusionMatrixMetric(BinaryMetricBase):
    def __init__(self):
        super().__init__(self, metric_calculator.confusion_metric_flat, result_name='tn_fp_fn_tp',
                         require_prob=False)


class MultiOverallAccuracyMetric(MultiClassMetricBase):
    def __init__(self):
        super().__init__(self, accuracy_score, result_name='Overall_Accuracy', require_prob=False)


class MultiAverageAccuracyMetric(MultiClassMetricBase):
    def __init__(self):
        super().__init__(self, balanced_accuracy_score, result_name='Average_Accuracy', require_prob=False)


class MultiMicroPrecisionMetric(MultiClassMetricBase):
    def __init__(self):
        super().__init__(self, precision_score, result_name='Micro_Precision', require_prob=False)
        self.func_param = {'average': 'micro'}


class MultiMacroPrecisionMetric(MultiClassMetricBase):
    def __init__(self):
        super().__init__(self, precision_score, result_name='Macro_Precision', require_prob=False)
        self.func_param = {'average': 'macro'}


class MultiMicroRecallMetric(MultiClassMetricBase):
    def __init__(self):
        super().__init__(self, recall_score, result_name='Micro_Recall', require_prob=False)
        self.func_param = {'average': 'micro'}


class MultiMacroRecallMetric(MultiClassMetricBase):
    def __init__(self):
        super().__init__(self, recall_score, result_name='Macro_Recall', require_prob=False)
        self.func_param = {'average': 'macro'}


class MultiConfusionMatrixMetric(MultiClassMetricBase):
    def __init__(self):
        super().__init__(self, confusion_matrix, result_name='Confusion_Matrix', require_prob=False)


class RegressionMeanAbsoluteErrorMetric(RegressionMetricBase):
    def __init__(self):
        super().__init__(self, mean_absolute_error, result_name='Mean_Absolute_Error')


class RegressionRootMeanSquaredErrorMetric(RegressionMetricBase):
    def __init__(self):
        super().__init__(self, metric_calculator.root_mean_squared_error,
                         result_name='Root_Mean_Squared_Error')


class RegressionRelativeSquaredErrorMetric(RegressionMetricBase):
    def __init__(self):
        super().__init__(self, metric_calculator.relative_squared_error,
                         result_name='Relative_Squared_Error')


class RegressionRelativeAbsoluteErrorMetric(RegressionMetricBase):
    def __init__(self):
        super().__init__(self, metric_calculator.relative_absolute_error,
                         result_name='Relative_Absolute_Error')


class RegressionCoefficientOfDeterminationMetric(RegressionMetricBase):
    def __init__(self):
        super().__init__(self, r2_score, result_name='Coefficient_of_Determination')
