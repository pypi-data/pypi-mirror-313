"""
Date time:
Date time is represented by Pandas.Timestamp class, which is the Pandas equivalent of
python's datetime.datetime class.

The dtype of a Pandas.Series with Pandas.Timestamp is datetime64[ns]


Time span:
Time span, which is the difference between two date times, is represented by Pandas.Timedelata
class.
The dtype of a Pandas.Series with Pandas.Timestamp is timedelta64[ns]

"""

import numpy as np
import pandas as pd
from pandas.api.types import is_datetime64_ns_dtype, is_timedelta64_ns_dtype
from pandas.core.dtypes.common import is_integer_dtype, is_float_dtype

from azureml.studio.core.utils.missing_value_utils import is_na


def is_datetime_dtype(argument):
    return is_datetime64_ns_dtype(argument)


def is_timespan_dtype(argument):
    return is_timedelta64_ns_dtype(argument)


def convert_to_datetime(series, date_time_format=None, unit='ns', errors='raise'):
    """Convert to datetime

    :param series: pandas Series
    :param date_time_format：str, pattern to parse time, eg. '%d%m%Y'
    :param unit: str, if series is int dtype, unit of its value
    :param errors: {'ignore', 'raise', 'coerce'}, default 'raise', denote the handling of
                    errors caused by invalid parsing
    :return:
    """

    if date_time_format is None:
        # If series is a int or float dtype, then convert according to unit
        if is_integer_dtype(series) or is_float_dtype(series):
            return pd.to_datetime(arg=series, errors=errors, unit=unit)

        return pd.to_datetime(arg=series, errors=errors, infer_datetime_format=True)
    return pd.to_datetime(arg=series, errors=errors, format=date_time_format)


def convert_to_time_span(argument, unit=None, errors='raise'):
    """Convert to timedelta

    :param argument:  str, timedelta, list-like or Series
    :param unit: str, default 'ns', denote the unit of column, such as 'days'
    :param errors: {'ignore', 'raise', 'coerce'}, default 'raise', denote the handling of
                    errors caused by invalid parsing
    :return:
    """
    return pd.to_timedelta(arg=argument, unit=unit, errors=errors)


def convert_to_ns(series):
    """Convert to nanoseconds

    :param series: pd.Series
    :return:
    """
    # Cannot use pandas.core.dtypes.common.is_datetime_or_timedelta_dtype
    # because it returns False for datetime64[ns, UTC] dtype.
    if is_datetime_dtype(series) or is_timespan_dtype(series):
        # Do not process NAN at this step, and treat NAT as NAN.
        series = series.apply(lambda x: np.nan if is_na(x) else x.value)

    return series
