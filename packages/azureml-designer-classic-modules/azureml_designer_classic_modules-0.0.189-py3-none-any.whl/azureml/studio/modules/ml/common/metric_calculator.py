# TODO: filename, metric_calculator.py or extend_metrics.py ?
import numpy as np
from sklearn.metrics import confusion_matrix, mean_squared_error, r2_score, mean_absolute_error, log_loss

from azureml.studio.modules.ml.common import mathematic_op


def safe_divide(numerator, denominator):
    if denominator < 1e-9:
        return 0.0
    return numerator / denominator


def confusion_metric_flat(y_true, y_pred):
    return confusion_matrix(y_true, y_pred).ravel()


def relative_squared_error(y_true, y_pred):
    r"""
    calculate squared error
    y = y_{true}

    \hat{y} = y_{pred}

    \bar{y} = average(y)

    rse = \frac{\sum_{i=0}^{n-1}(y_i-\hat{y_i})^2}{\sum_{i=0}^{n-1}(y_i-\bar{y})^2}
        = 1 - R^2

    :param y_true: label
    :param y_pred: predict result
    :return: relative_absolute_error, float
    """
    return 1 - r2_score(y_true=y_true, y_pred=y_pred)


def relative_absolute_error(y_true, y_pred):
    r"""
    calculate relative absolute error
    y = y_{true}

    \hat{y} = y_{pred}

    \bar{y} = average(y)

    rae = \frac{\sum_{i=0}^{n-1}|y_i-\hat{y_i}|}{\sum_{i=0}^{n-1}|y_i-\bar{y}|}
        = \frac{mean  absolute  error}{\frac{sum_{i=0}^{n-1}|y_i-\bar{y}|}{n}}

    :param y_true: label
    :param y_pred: predict result
    :return: relative_absolute_error, float. if sum_{i=0}^{n-1}|y_i-\bar{y}| == 0, return 0.0 as v1's setting.
    """
    y_mean = np.average(y_true)
    y_diff = y_true - y_mean
    y_abs_mean = np.average(np.absolute(y_diff))
    return safe_divide(mean_absolute_error(y_true, y_pred), y_abs_mean)


def root_mean_squared_error(y_true, y_pred):
    return np.sqrt(mean_squared_error(y_true=y_true, y_pred=y_pred))


def patch_log_loss(y_true, y_pred):
    y_pred = mathematic_op.sigmoid(y_pred)
    return log_loss(y_true, y_pred)
