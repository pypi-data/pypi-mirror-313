import numpy as np


def sigmoid(x):
    return 1.0 / (1 + np.exp(-x))


def reverse_sigmoid(x):
    if x >= 1 or x <= 0:
        return np.nan
    if x < 1e-9:
        return -np.inf
    if 1 - x < 1e-9:
        return np.inf
    return np.log(x / (1 - x))


def inf2nan(series):
    if np.any(np.isinf(series)):
        series[(series == np.inf) | (series == -np.inf)] = np.nan
    return series
